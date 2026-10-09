import os
from dotenv import load_dotenv
import requests
import pandas as pd
import time
from loguru import logger
import pyarrow.ipc as ipc
from io import BytesIO
from requests.exceptions import (
    ConnectionError, 
    ReadTimeout, 
    Timeout, 
    HTTPError)
from requests import Response


load_dotenv()  # Load environment variables from .env file

DATABRICKS_HOST = os.getenv("DATABRICKS_HOST")
TOKEN = os.getenv("TOKEN")
WAREHOUSE_ID = os.getenv("WAREHOUSE_ID")

REQUEST_TIMEOUT = 30
QUERY_TIMEOUT = 300
POLL_INTERVAL = 1

MAX_RETRIES = 3
RETRY_STATUS_CODES = {429, 500, 502, 503, 504}

TERMINAL_STATES = {"SUCCEEDED", "FAILED", "CANCELED"}


class DatabricksStatementAPI:
    def __init__(self, host, token, warehouse_id) -> None:
        self.host = host
        self.token = token
        self.warehouse_id = warehouse_id

        self.session = requests.Session()
        self.session.headers.update({"Authorization": f"Bearer {self.token}"})

    def _get_url(self, cancel_endpoint=False, statement_id='') -> str:
        base = f"{self.host}/api/2.0/sql/statements/{statement_id}"
        return f"{base}/cancel" if cancel_endpoint else base

    def _make_request(self, external_request, request_type, url, **kwargs) -> Response:
        request_type = request_type.upper()
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                if external_request is False:
                    if request_type == "POST":
                        response = self.session.post(url=url,
                                                     timeout=REQUEST_TIMEOUT,
                                                     **kwargs)
                    elif request_type == "GET":
                        response = self.session.get(url=url,
                                                    timeout=REQUEST_TIMEOUT,
                                                    **kwargs)
                    else:
                        raise ValueError("request_type must be 'POST' or 'GET'")
                elif external_request is True:
                    if request_type == "POST":
                        response = requests.post(url=url,
                                                 timeout=REQUEST_TIMEOUT,
                                                 **kwargs)
                    elif request_type == "GET":
                        response = requests.get(url=url,
                                                timeout=REQUEST_TIMEOUT,
                                                **kwargs)
                    else:
                        raise ValueError("request_type must be 'POST' or "
                                         "'GET'")
                else:
                    raise ValueError("external_request must be True or False")
                response.raise_for_status()
                return response
            except (ConnectionError, ReadTimeout, Timeout) as e:
                logger.warning(f"Attempt {attempt} out of {MAX_RETRIES} "
                               f"failed with error: {e}. Retrying...")
                if attempt == MAX_RETRIES:
                    logger.error("Max retries reached. Raising exception.")
                    raise
                time.sleep(2)
            except HTTPError as e:
                status_code = (e.response.status_code if e.response is not
                               None else "Unknown")
                if status_code in RETRY_STATUS_CODES:
                    logger.warning(f"Attempt {attempt} out of {MAX_RETRIES} "
                                   "failed with HTTP status code: "
                                   f"{status_code}. Retrying...")
                    if attempt == MAX_RETRIES:
                        logger.error("Max retries reached. Raising exception.")
                        raise
                    time.sleep(2)
                else:
                    logger.error("Non-retryable HTTP error received: "
                                 f"{status_code}")
                    raise

    def post_for_statement_id(self, sql_query) -> str:
        logger.info("Posting SQL statement to Databricks API for execution.")
        url = self._get_url()
        body = {
            "warehouse_id": self.warehouse_id,
            "statement": sql_query,
            "disposition": "EXTERNAL_LINKS",
            "format": "ARROW_STREAM",
            "wait_timeout": "0s"
        }

        response = self._make_request(external_request=False, request_type="POST", url=url, json=body)

        response_data = response.json()
        statement_id = response_data.get("statement_id")

        if not statement_id:
            raise ValueError("No statement_id returned from Databricks API")

        logger.info(f"Received statement_id: {statement_id}")
        return statement_id

    def get_data_from_statement_id(self, statement_id) -> dict:
        logger.info(f"Attempting to fetch data for statement_id: {statement_id
                                                                  }")
        url = self._get_url(statement_id=statement_id)

        response = self._make_request(external_request=False, request_type="GET", url=url)

        response_json = response.json()
        logger.info(f"Status is: {response_json.get('status', {}).get('state'
                                                                      )}")
        return response_json

    def cancel_statement(self, statement_id) -> None:
        logger.info(f"Attempting to cancel statement_id: {statement_id}")
        url = self._get_url(cancel_endpoint=True, statement_id=statement_id)

        self._make_request(external_request=False, request_type="POST", url=url)

    def poll_to_completion(self, statement_id) -> dict:
        logger.info(f"Waiting for completion of statement_id: {statement_id}")
        state = "PENDING"
        start_time = time.monotonic()
        while state not in TERMINAL_STATES:
            if time.monotonic() - start_time > QUERY_TIMEOUT:
                self.cancel_statement(statement_id)
                raise TimeoutError("The request timed out after 5 minutes.")

            result = self.get_data_from_statement_id(statement_id=statement_id)
            state = result.get("status", {}).get("state")
            logger.info(f"Current state: {state}")

            if state in ("FAILED", "CANCELED"):
                error = (
                    result.get("status", {})
                          .get("error", {})
                          .get("message", "No error message provided")
                )
                raise RuntimeError(f"QUERY {state}: {error}")

            if state == "SUCCEEDED":
                logger.success(f"Statement {statement_id} succeeded.")
                return result

            time.sleep(POLL_INTERVAL)

    def download_from_external_link(self, link) -> pd.DataFrame:
        logger.info(f"Attempting to download data from external link: {link}")

        get_link = self._make_request(external_request=True, request_type="GET", url=link)

        reader = ipc.open_stream(BytesIO(get_link.content))
        table = reader.read_all()
        df = table.to_pandas()
        logger.success(f"Downloaded data for link: {link}")

        return df

    def download_all_external_links(self, result,
                                    output_format="DataFrame") -> pd.DataFrame | list[dict]:
        success_results = result.get("result", {})
        logger.debug(success_results)

        link_data = [self.download_from_external_link(link["external_link"])
                     for link in success_results.get("external_links", [])]

        if not link_data:
            raise ValueError(
                            "Query succeeded but returned no external links."
                            )

        concatenated_df = pd.concat(link_data, ignore_index=True) if len(
            link_data) > 1 else link_data[0]

        logger.info(
        f"Retrieved {len(concatenated_df):,} rows "
        f"across {len(link_data)} external link(s)"
        )

        if output_format == "DataFrame":
            return concatenated_df

        if output_format == "JSON":
            return concatenated_df.to_dict(orient="records")

        raise ValueError("output_format must be 'DataFrame' or 'JSON'")

    def orchestrate(self, sql_query, output_format="DataFrame") -> pd.DataFrame | list[dict]:
        """
        Execute a Databricks SQL query and return the result
        as either a pandas DataFrame or JSON records.
        """
        statement_id = self.post_for_statement_id(sql_query)

        result = self.poll_to_completion(statement_id=statement_id)

        logger.debug(result)

        return self.download_all_external_links(result=result,
                                                output_format=output_format)


def main():
    sql_statement = "SELECT * from catalog_30_bronze.pims." \
                    "vw_pims_modifieddata LIMIT 5"
    api = DatabricksStatementAPI(host=DATABRICKS_HOST, token=TOKEN,
                                 warehouse_id=WAREHOUSE_ID)
    return api.orchestrate(sql_query=sql_statement, output_format="DataFrame")


if __name__ == "__main__":
    output = main()
    print(output)
