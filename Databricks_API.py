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

    def orchestrate(self):
        statement_id = self.post_for_statement_id()

        state = "PENDING"
        while state not in ("SUCCEEDED", "FAILED", "CANCELED"):
            result = self.get_data_from_statement_id(statement_id=statement_id)
            state = result["status"]["state"]

            if state == "SUCCEEDED":
                return result["result"]
            if state in ("FAILED", "CANCELED"):
                raise Exception(f"QUERY {state}: {result['status'].get('error message', 'No error message provided')}")

            time.sleep(1)
            





sql_statement = "SELECT * from catalog_30_bronze.pims.vw_pims_modifieddata " \
                "LIMIT 5"

setup_request = DatabricksStatementAPI(sql_statement)
run_request = setup_request.orchestrate()
print(run_request)

