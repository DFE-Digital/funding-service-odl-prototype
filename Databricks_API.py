from my_secrets import DATABRICKS_HOST, TOKEN, WAREHOUSE_ID
import requests
import pandas as pd
import time
from loguru import logger
import pyarrow.ipc as ipc
from io import BytesIO

class DatabricksStatementAPI:
    def __init__(self, sql_query):
        self.sql_query = sql_query

    def _get_url(self, cancel_endpoint=False, statement_id=''):
        if cancel_endpoint is False:
            return f"{DATABRICKS_HOST}/api/2.0/sql/statements/{statement_id}"
        else:
            return f"{DATABRICKS_HOST}/api/2.0/sql/statements/{statement_id}/cancel"


    def _assemble_headers(self, method='POST'):
        if method == "GET":
            return {"Authorization": f"Bearer {TOKEN}"}
        else:
            return {"Authorization": f"Bearer {TOKEN}",
                    "Content-Type": "application/json"}

    def post_for_statement_id(self):
        logger.info("Posting SQL statement to Databricks API for execution.")
        url = self._get_url()
        headers = self._assemble_headers()
        body = {
            "warehouse_id": WAREHOUSE_ID,
            "statement": self.sql_query,
            "disposition": "EXTERNAL_LINKS",
            "format": "ARROW_STREAM",
            "wait_timeout": "0s"
        }
        response = requests.post(url, headers=headers, json=body, timeout=30)
        response.raise_for_status()

        response_data = response.json()
        statement_id = response_data["statement_id"]

        logger.info(f"Received statement_id: {statement_id}")
        return statement_id

    def get_data_from_statement_id(self, statement_id):
        logger.info(f"Attempting to fetch data for statement_id: {statement_id}")
        url = self._get_url(statement_id=statement_id)
        headers = self._assemble_headers(method='GET')
        body = {}
        response = requests.get(url, headers=headers, params=body, timeout=30)
        
        json = response.json()
        logger.info(f"Status is: {json['status']['state']}")
        return json

    def download_from_external_link(self, link, output_format):
        logger.info(f"Attempting to download data from external link: {link}")
        get_link = requests.get(link, timeout=30)
        get_link.raise_for_status()
        
        reader = ipc.open_stream(BytesIO(get_link.content))
        table = reader.read_all()
        df = table.to_pandas()
        logger.info(f"Downloaded data for link: {link}")
        print(df.head())
        
        if output_format == "DataFrame":
            return df
        else:
            dict_form = df.to_dict(orient="records")
            logger.info("Converted data to dictionary format")
            print(dict_form)
            return dict_form

    def orchestrate(self, output_format="DataFrame"):
        statement_id = self.post_for_statement_id()

        state = "PENDING"
        start_time = time.time()
        while state not in ("SUCCEEDED", "FAILED", "CANCELED"):

            if time.time() - start_time > 300:
                raise TimeoutError("The request timed out after 5 minutes.")

            result = self.get_data_from_statement_id(statement_id=statement_id)
            state = result["status"]["state"]

            if state == "SUCCEEDED":
                success_results = result["result"]
                print(success_results)

                link = success_results["external_links"][0]["external_link"]
                print(link)

                self.download_from_external_link(link, output_format=output_format)

            if state in ("FAILED", "CANCELED"):
                raise Exception(f"QUERY {state}: {result['status'].get('error message', 'No error message provided')}")

            time.sleep(1)
            





sql_statement = "SELECT * from catalog_30_bronze.pims.vw_pims_modifieddata " \
                "LIMIT 5"

setup_request = DatabricksStatementAPI(sql_statement)
run_request = setup_request.orchestrate(output_format="DataFrame")
run_request

