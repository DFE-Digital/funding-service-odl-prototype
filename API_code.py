from my_secrets import DATABRICKS_HOST, TOKEN, WAREHOUSE_ID
import requests
import pandas as pd
#test with GP off!

class DatabricksAPI:
    def __init__(self, host=DATABRICKS_HOST, token=TOKEN,
                 warehouse_id=WAREHOUSE_ID):
        self.host = host
        self.token = token
        self.warehouse_id = warehouse_id
        self.statements_general = '/api/2.0/sql/statements'
        self.jobs_general = '/api/2.1/jobs/'
        self.statement_id = ''
        self.df = pd.DataFrame({'Endpoint_name': ['data', 'statement_status',
                                                  'statement_cancel',
                                                  'trigger', 'job_cancel',
                                                  'job_status', 'output',
                                                  'list'],
                                'API': ['Statement', 'Statement', 'Statement',
                                        'Job', 'Job', 'Job', 'Job',
                                        'Job'],
                                'Method': ['POST', 'GET', 'POST', 'POST',
                                           'POST', 'GET', 'GET',
                                           'GET'],
                                'Suffix': ['', f"/{self.statement_id}",
                                             f"/{self.statement_id}/cancel",
                                             '/run-now',
                                             '/runs/cancel', '/runs/get',
                                             '/runs/get-output',
                                             '/list'],
                                'Payload': [["warehouse_id", "statement"],
                                            [],
                                            [],
                                            ["job_id", "job_parameters"],
                                            ["run_id"],
                                            ["run_id"],
                                            ["run_id"],
                                            ["limit"]]}).set_index('Endpoint_name')
        self.df['Headers'] = self.df['Method'].map(self.headers)

    def headers(self, method='POST'):
        if method == "GET":
            return {"Authorization": f"Bearer {self.token}"}
        else:
            return {"Authorization": f"Bearer {self.token}",
                    "Content-Type": "application/json"}

    def endpoint(self, endpoint_name, statement_id=''):
        # If you don't pass a statement_id, the instance attribute gets reset to ''.
        # This would be easy to prevent but means having more code and it's harmless I think
        general_choice = {'Statement': self.statements_general,
                          'Job': self.jobs_general}
        self.statement_id = statement_id
        prefix = self.host + general_choice[self.df.loc[endpoint_name,
                                                        'API']]
        suffix = self.df.loc[endpoint_name, 'Suffix']
        return prefix + suffix

    def payload(self, endpoint_name, sql='', timeout="10s", statement_id='', job_id='', job_parameters={}, run_id='', limit=10):
        payload_dict = {"warehouse_id": self.warehouse_id,
                        "statement": sql,
                        "job_id": job_id,
                        "job_parameters": job_parameters,
                        "run_id": run_id,
                        "limit": limit,
                        "wait-timeout": timeout,
                        "format": "JSON_ARRAY"}
        return {key: payload_dict[key] for key in self.df.loc[endpoint_name, "Payload"]}

    def call(self, endpoint_name, sql='', timeout="10s", statement_id='', job_id='', job_parameters={}, run_id='', limit=10):
        url = self.endpoint(endpoint_name, statement_id)
        method = self.df.loc[endpoint_name, 'Method']
        headers = self.df.loc[endpoint_name, 'Headers']
        payload = self.payload(endpoint_name, sql, timeout, statement_id, job_id, job_parameters, run_id, limit)
        if method == 'POST':
            response = requests.post(url, headers=headers, json=payload)
        else:
            response = requests.get(url, headers=headers, params=payload)
        response.raise_for_status()
        print(response.json())


api = DatabricksAPI()


sql_statement = "SELECT * from catalog_30_bronze.pims.vw_pims_modifieddata " \
                "LIMIT 10"

api.call('data', sql=sql_statement)


#    def statements_specific(self, statement_id):
#        # status still pulls the data
#        self.statement_id = statement_id
#        specific = self.df.loc
#        methods = dict(zip(specific.keys(), ['POST', 'GET', 'POST']))
#        return {'specific': specific, 'methods': methods}
#
#
#def jobs_specific(job_id, run_id=''):
#    # I didn't include the /create jobs one because we won't need that
#    specific = {'trigger': '/run-now', 'adhoc_task': 'runs/submit',
#                'cancel': '/runs/cancel', 'status': '/runs/get',
#                'output': '/runs/get-output', 'list': '/list'}
#    methods = dict(zip(specific.keys(), ['POST', 'POST', 'POST', 'GET', 'GET',
#                                         'GET']))
#    return {'specific': specific, 'methods': methods}


#def endpoint(endpoint_type='statement', id='', variation='data'):
#    general = DATABRICKS_HOST
#    if endpoint_type == 'statement':
#        general += statements_general
#        specific = statements_specific(id)['specific'][variation]
#    else:
#        general += jobs_general
#        specific = jobs_specific(id)['specific'][variation]
#
#    return general+specific


#def headers(is_get=False):
#    if is_get is True:
#        return {"Authorization": f"Bearer {TOKEN}"}
#    else:
#        return {"Authorization": f"Bearer {TOKEN}",
#                "Content-Type": "application/json"}


#def payload(sql, timeout="10s"):
#    return {"warehouse_id": WAREHOUSE_ID,
#            "statement": sql,
#            "wait-timeout": timeout,
#            "format": "JSON_ARRAY"}



