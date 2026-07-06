import requests
import json
import pandas as pd

listFormConfigurations_url = "https://preprod.externalapi.digital-forms.educ" \
 "ation.gov.uk/api/listFormConfigurations"
getResponses_url = "https://preprod.externalapi.digital-forms.education.gov." \
 "uk/api/getResponses"
getResponseQuestion_url = "https://preprod.externalapi.digital-forms.educati" \
 "on.gov.uk/api/getResponseQuestion"
getResponseQuestionData_url = "https://preprod.externalapi.digital-forms.edu" \
 "cation.gov.uk/api/getResponseQuestionData"

# 1) URL 
# 2) Headers 
# 3) FormID as context

endpoint_list = ['getResponses',
                 'getResponseQuestion',
                 'getResponseQuestionData']

BASE_URL = "https://preprod.externalapi.digital-forms.education.gov.uk/api/"


class DigitalForms:
    def __init__(self, start_date: str, end_date: str, form_ids: list[str]):
        """Initialises GetDF with both parameterised attributes and
        default-initialised attributes. Note that multiple form_ids can be
        passed."""
        self.start_date = start_date
        self.end_date = end_date
        self.form_ids = form_ids
        self.session = requests.Session()

    def get_endpoint_url(self, endpoint_name: str):
        return BASE_URL + endpoint_name

    def get_headers(self, formid) -> dict:
        return {
                'StartDate': self.start_date,
                'EndDate': self.end_date,
                'FormId': formid
            }

    def get_data(self):

        # call listFormConfigurations
        all_data = {}
        endpoint = 'listFormConfigurations'
        url = self.get_endpoint_url(endpoint)
        api_data = self.session.get(url).text
        all_data[endpoint] = api_data

        for form_id in self.form_ids:
            for endpoint in endpoint_list:
                headers = self.get_headers(form_id)
                urls = self.get_endpoint_url(endpoint)
                api_data = self.session.get(urls, headers=headers).text
                all_data[form_id + "|" + endpoint] = api_data

        return all_data

    def write_data(self):

        with pd.ExcelWriter("DigitalForms2.xlsx") as writer:
            for sheet_name, json_text in self.get_data().items():
                data = json.loads(json_text)
                df = pd.json_normalize(data)
                df.to_excel(writer, sheet_name=sheet_name[:31], index=False)


digi_forms = DigitalForms('2020-05-05', '2026-06-20', ['7c6iy7ajyi',
                                                       'i3If3JGHw8'])
digi_forms.write_data()

#'cb7bii5gx2', 'o50um3ao3a', 'x1xtt7u3p0', '_igkp1ft5_','59m0cqvlku


#class GetDF:
#    """This class can be instantiated with the required arguments to filter
#    data across the 4 Digital Forms APIs. Data from the 4 APIs can be
#    retrieved by calling an instance of this class."""

#     def __init__(self, start_date: str, end_date: str, *form_id: str):
#         """Initialises GetDF with both parameterised attributes and
#         default-initialised attributes. Note that multiple form_ids can be
#         passed."""
#         self.start_date = start_date
#         self.end_date = end_date
#         self.form_id = form_id
#         self.listFormConfigurations_pattern = []
#         self.getResponses_pattern = ['StartDate', 'EndDate', 'FormId']
#         self.getResponseQuestion_pattern = ['StartDate', 'EndDate', 'FormId']
#         self.getResponseQuestionData_pattern = ['StartDate', 'EndDate',
#                                                 'FormId']
#         # Create one session for all
#         self.session = requests.Session()
#         self.headers_structure = None  # Updated once when the object is called

#     def _headers_structure(self, *apis: str) -> dict:
#         """Returns a dictionary with the APIs as keys and the names of headers
#         needed as values."""
#         api_options = ['listFormConfigurations', 'getResponses',
#                        'getResponseQuestion', 'getResponseQuestionData']
#         for submit in apis:
#             if submit not in api_options:
#                 raise ValueError(f"Unsupported API name. Enter one or more "
#                                  f"of the following: {api_options}")
#         diction = dict(zip(api_options, [self.listFormConfigurations_pattern,
#                                          self.getResponses_pattern,
#                                          self.getResponseQuestion_pattern,
#                                          self.getResponseQuestionData_pattern])
#                        )
#         # List of lists - inner lists are headers patterns
#         return [diction[api] for api in apis]

#     def _headers_list(self, headers_structure, form_id: str) -> list:
#         """Returns lists of dictionaries for each form and the headers."""
#         headers_arguments = dict(zip(['StartDate', 'EndDate', 'FormId'],
#                                      [self.start_date, self.end_date, form_id])
#                                  )
#         # Produces a mirror list of lists to _headers_structure with the actual
#         # arguments passed
#         # List of lists and in __call__ this is done per form
#         arguments = [[headers_arguments[argument] for argument in struct]
#                      for struct in headers_structure]

#         return [dict(zip(k, v)) for k, v in zip(headers_structure, arguments)]

#     def _urls(self, *apis: str):
#         """Returns a list of endpoints."""
#         url_dict = {'listFormConfigurations': listFormConfigurations_url,
#                     'getResponses': getResponses_url,
#                     'getResponseQuestion': getResponseQuestion_url,
#                     'getResponseQuestionData': getResponseQuestionData_url}
#         urls = [url_dict[api] for api in apis]
#         return urls  # list of endpoints in scope

#     def __call__(self, *apis: str) -> dict:
#         outer_list = {}
#         # List of lists - inner lists are headers patterns (scoped endpoints)
#         self.headers_structure = self._headers_structure(*apis)
#         payload = {}
#         if 'listFormConfigurations' in apis:
#             outer_list.update({'listFormConfigurations': self.session.get(
#                 self._urls('listFormConfigurations')[0],
#                 headers=self._headers_list(self.headers_structure,
#                                            self.form_id[0])[0],  # any form_id
#                 data=payload).text})
#         apis = [a for a in apis if a != 'listFormConfigurations']
#         for form in self.form_id:
#             for api, url, header in zip(
#                 apis,
#                 self._urls(*apis),
#                 self._headers_list(self.headers_structure, form)
#             ):
#                 outer_list.update({form + "|" + api:
#                                    self.session.get(url, headers=header,
#                                                     data=payload).text})
#         return outer_list


# instance = GetDF('2020-05-05', '2026-06-20', '7c6iy7ajyi', 'i3If3JGHw8',
#                  'cb7bii5gx2', 'o50um3ao3a', 'x1xtt7u3p0', '_igkp1ft5_',
#                  '59m0cqvlku')
# instance_call = instance('listFormConfigurations', 'getResponses',
#                          'getResponseQuestion', 'getResponseQuestionData')
# print(instance_call.keys())

# with pd.ExcelWriter("DigitalForms.xlsx") as writer:
#     for sheet_name, json_text in instance_call.items():
#         data = json.loads(json_text)
#         df = pd.json_normalize(data)
#         df.to_excel(writer, sheet_name=sheet_name[:31], index=False)
# #        try:
# #            data = json.loads(json_text)
# #            df = pd.json_normalize(data)
# #            df.to_excel(writer, sheet_name=sheet_name[:31], index=False)
# #        except json.JSONDecodeError:
# #            # Fallback: write raw text if not JSON
# #            df = pd.DataFrame({"raw_text": [json_text]})
# #            df.to_excel(writer, sheet_name=sheet_name[:31], index=False)
