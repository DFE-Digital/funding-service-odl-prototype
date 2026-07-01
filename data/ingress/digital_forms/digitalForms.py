import requests

listFormConfigurations_url = "https://preprod.externalapi.digital-forms.education.gov.uk/api/listFormConfigurations"
getResponses_url = "https://preprod.externalapi.digital-forms.education.gov.uk/api/getResponses"
getResponseQuestion_url = "https://preprod.externalapi.digital-forms.education.gov.uk/api/getResponseQuestion"
getResponseQuestionData_url = "https://preprod.externalapi.digital-forms.education.gov.uk/api/getResponseQuestionData"

class GetDF:
    """This class can be instantiated with the required arguments to filter
    data across the 4 Digital Forms APIs. Data from the 4 APIs can be
    retrieved by calling an instance of this class."""

    def __init__(self,start_date: str, end_date: str, *form_id: str):
        """Initialises GetDF with both parameterised attributes and
        default-initialised attributes. Note that multiple form_ids can be
        passed."""
        self.start_date = start_date
        self.end_date = end_date
        self.form_id = form_id
        self.listFormConfigurations_pattern = []
        self.getResponses_pattern = ['StartDate','EndDate','FormId']
        self.getResponseQuestion_pattern = ['StartDate','EndDate','FormId']
        self.getResponseQuestionData_pattern = ['StartDate','EndDate','FormId']
    
    def _headers_structure(self, *apis: str) -> dict:
        """Returns a dictionary with the APIs as keys and the names of headers
        needed as values."""
        api_options = ['listFormConfigurations', 'getResponses',
                       'getResponseQuestion', 'getResponseQuestionData']
        for submit in apis:
            if submit not in api_options:
                raise ValueError(f"Unsupported API name. Enter " \
                                 "one or more of the following: {api_options}")
        print(dict(zip(api_options,[self.listFormConfigurations_pattern,
                                     self.getResponses_pattern,
                                     self.getResponseQuestion_pattern,
                                     self.getResponseQuestionData_pattern])))
        return dict(zip(api_options,[self.listFormConfigurations_pattern,
                                     self.getResponses_pattern,
                                     self.getResponseQuestion_pattern,
                                     self.getResponseQuestionData_pattern]))
    
    def _headers_list(self, headers_structure, form_id: str, *apis: str) -> list:
        """Returns lists of dictionaries for each form and the headers."""
        headers_arguments = dict(zip(['StartDate', 'EndDate', 'FormId'],
                                     [self.start_date, self.end_date, form_id]))

        headers_structures = [headers_structure(*apis)[api] for api in apis] 
        # list of lists
        
        arguments = [
            [headers_arguments[argument] for argument in struct]
            for struct in headers_structures
        ] # list of lists
        
        return [dict(zip(k, v)) for k, v in zip(headers_structures, arguments)]
    
    def _urls(self, *apis: str):

        """Returns a list of endpoints."""
        url_dict = {'listFormConfigurations': listFormConfigurations_url,
             'getResponses': getResponses_url,
             'getResponseQuestion': getResponseQuestion_url,
             'getResponseQuestionData': getResponseQuestionData_url}
        
        urls = [url_dict[api] for api in apis]
        
        return urls
    
    def __call__(self, *apis: str):
        outer_list = {}
        payload = {}
        if 'listFormConfigurations' in apis:
            outer_list.update({'listFormConfigurations': requests.request("GET", self._urls('listFormConfigurations')[0],
                                                      headers = self._headers_list(self._headers_structure,self.form_id[0],'listFormConfigurations')[0],
                                                      data = payload).text})
            

        apis = [a for a in apis if a != 'listFormConfigurations']
        
        for form in self.form_id:
            for api, url, header in zip(
                apis,
                self._urls(*apis),
                self._headers_list(self._headers_structure,form,*apis)
            ):
                outer_list.update({form + "|" + api:
                                   requests.request("GET", url,
                                                      headers = header,
                                                      data = payload).text
                })
                
        return outer_list
    
    
 
instance = GetDF('2026-05-05', '2026-06-20', '7c6iy7ajyi','i3If3JGHw8','cb7bii5gx2','o50um3ao3a','x1xtt7u3p0','_igkp1ft5_','59m0cqvlku')
instance_call = instance('listFormConfigurations', 'getResponses',
                   'getResponseQuestion', 'getResponseQuestionData')



#print(instance('listFormConfigurations'))


print(instance_call.keys())
