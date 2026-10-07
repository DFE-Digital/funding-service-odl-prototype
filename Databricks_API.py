from my_secrets import DATABRICKS_HOST, TOKEN, WAREHOUSE_ID
import requests
import pandas as pd
import time
from loguru import logger
import pyarrow.ipc as ipc
from io import BytesIO

REQUEST_TIMEOUT = 30
QUERY_TIMEOUT = 300
POLL_INTERVAL = 1

class DatabricksStatementAPI:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({"Authorization": f"Bearer {TOKEN}"})

    def _get_url(self, cancel_endpoint=False, statement_id=''):
        base = f"{DATABRICKS_HOST}/api/2.0/sql/statements/{statement_id}"
        return f"{base}/cancel" if cancel_endpoint else base

    def post_for_statement_id(self, sql_query):
        logger.info("Posting SQL statement to Databricks API for execution.")
        url = self._get_url()
        #headers = self._assemble_headers()
        body = {
            "warehouse_id": WAREHOUSE_ID,
            "statement": sql_query,
            "disposition": "EXTERNAL_LINKS",
            "format": "ARROW_STREAM",
            "wait_timeout": "0s"
        }
        response = self.session.post(url, json=body, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()

        response_data = response.json()
        statement_id = response_data["statement_id"]

        logger.info(f"Received statement_id: {statement_id}")
        return statement_id

    def get_data_from_statement_id(self, statement_id):
        logger.info(f"Attempting to fetch data for statement_id: {statement_id}")
        url = self._get_url(statement_id=statement_id)
        response = self.session.get(url, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()

        response_json = response.json()
        logger.info(f"Status is: {response_json['status']['state']}")
        return response_json

    def cancel_statement(self, statement_id):
        logger.info(f"Attempting to cancel statement_id: {statement_id}")
        url = self._get_url(cancel_endpoint=True, statement_id=statement_id)
        response = self.session.post(url, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()

    def poll_to_completion(self, statement_id):
        logger.info(f"Waiting for completion of statement_id: {statement_id}")
        state = "PENDING"
        start_time = time.monotonic()
        while state not in ("SUCCEEDED", "FAILED", "CANCELED"):
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
                raise Exception(f"QUERY {state}: {error}")

            if state == "SUCCEEDED":
                logger.success(f"Statement {statement_id} succeeded.")
                return result

            time.sleep(POLL_INTERVAL)

    def download_from_external_link(self, link):
        logger.info(f"Attempting to download data from external link: {link}")
        get_link = requests.get(link, timeout=REQUEST_TIMEOUT)
        get_link.raise_for_status()

        reader = ipc.open_stream(BytesIO(get_link.content))
        table = reader.read_all()
        df = table.to_pandas()
        logger.success(f"Downloaded data for link: {link}")
        logger.debug(df.head())

        return df

    def download_from_all_external_links(self, result, output_format="DataFrame"):
        success_results = result.get("result", {})
        logger.debug(success_results)
        
        link_data = []
        for link in success_results.get("external_links", []):
            logger.debug(link)
            link_data.append(self.download_from_external_link(
                link["external_link"]))
        
        if not link_data:
            raise ValueError(
                            "Query succeeded but returned no external links."
                            )
        
        concatenated_df = pd.concat(link_data, ignore_index=True)
        logger.debug(concatenated_df.head())
        
        if output_format == "DataFrame":
           return concatenated_df
        else:
            return concatenated_df.to_dict(orient="records")
        

    def orchestrate(self, sql_query, output_format="DataFrame"):
        statement_id = self.post_for_statement_id(sql_query)

        result = self.poll_to_completion(statement_id=statement_id)

        logger.debug(result)

        return self.download_from_all_external_links(result=result,
                                              output_format="DataFrame")






sql_statement = "SELECT * from catalog_30_bronze.pims.vw_pims_modifieddata " \
                "LIMIT 5"

api = DatabricksStatementAPI()
api.orchestrate(sql_query=sql_statement, output_format="DataFrame")
