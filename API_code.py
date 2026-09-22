import requests
from secrets import DATABRICKS_HOST, TOKEN, WAREHOUSE_ID

statements_general = '/api/2.0/sql/statements'


def statements_specific(statement_id):
    # GET status still pulls the data
    return {'POST data': '', 'GET status': f"/{statement_id}",
            'POST cancel': f"/{statement_id}/cancel"}


def endpoint(variation='POST data', statement_id=''):
    general = f"{DATABRICKS_HOST}{statements_general}"
    specific = statements_specific(statement_id)[variation]
    return general+specific


def headers(is_get=False):
    if is_get is True:
        return {"Authorization": f"Bearer {TOKEN}"}
    else:
        return {"Authorization": f"Bearer {TOKEN}",
                "Content-Type": "application/json"}


def payload(sql, timeout="10s"):
    return {"warehouse_id": WAREHOUSE_ID,
            "statement": sql,
            "wait-timeout": timeout,
            "format": "JSON_ARRAY"}


sql_statement = "SELECT * from catalog_30_bronze.pims.vw_pims_modifieddata " \
                "LIMIT 10"

response = requests.post(endpoint(), headers=headers(),
                         json=payload(sql_statement))
response.raise_for_status()
result = response.json()
print(result)
