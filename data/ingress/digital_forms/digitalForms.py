import requests

listFormConfigurations_url = "https://preprod.externalapi.digital-forms.education.gov.uk/api/listFormConfigurations"
getResponses_url = "https://preprod.externalapi.digital-forms.education.gov.uk/api/getResponses"
getResponseQuestion_url = "https://preprod.externalapi.digital-forms.education.gov.uk/api/getResponseQuestion"
getResponseQuestionData_url = "https://preprod.externalapi.digital-forms.education.gov.uk/api/getResponseQuestionData"

class GetDF:
    """This class can be instantiated with the required arguments to filter
    data across the 4 Digital Forms APIs."""
    def __init__(self,start_date,end_date,*form_id):

        self.start_date = start_date
        self.end_date = end_date
        self.form_id = form_id
        self.listFormConfigurations_pattern = []
        self.getResponses_pattern = ['StartDate','EndDate','FormId']
        self.getResponseQuestion_pattern = ['StartDate','EndDate','FormId']
        self.getResponseQuestionData_pattern = ['StartDate','EndDate','FormId']
    
    """Data from the 4 APIs can be retrieved by calling an instance of this
    class. Change this now."""
    def headers_structure(self,*apis):
        """This instance method can be called with a subset or all 4 Digital
        Forms APIs, using the arbitrary positional arguments parameter (*APIs)
        to retrieve the data"""
        api_options = ['listFormConfigurations', 'getResponses',
                       'getResponseQuestion', 'getResponseQuestionData']
        for submit in apis:
            if submit not in api_options:
                raise ValueError(f"Unsupported API name. Enter " \
                                 "one or more of the following: {api_options}")

        return dict(zip(api_options,[self.listFormConfigurations_pattern,
                                     self.getResponses_pattern,
                                     self.getResponseQuestion_pattern,
                                     self.getResponseQuestionData_pattern]))
    
    def headers_list(self,headers_structure,form_id,*apis):
        
        headers_arguments = dict(zip(['StartDate', 'EndDate', 'FormId'],
                                     [self.start_date, self.end_date, form_id]))

        headers_structures = [headers_structure(*apis)[api] for api in apis]
        #headers_structures becomes a list of lists.
        
        #arguments becomes a list of lists with the actual instantiated header
        # arguments for each API submitted.
        #It will be in the order that the apis were submitted, not the
        # api_options order.
        #For instance:
        #[['Cookie'], ['StartDate', 'FormId', 'EndDate', 'Cookie'],
        # ['StartDate', 'FormId', 'EndDate', 'Cookie'],
        # ['StartDate', 'FormId', 'EndDate']]
        
        arguments = [
            [headers_arguments[argument] for argument in struct]
            for struct in headers_structures
        ]
        
        print("headers_structures")
        print(headers_structures)
        print("arguments")
        print(arguments)

        #headers_list is a dictionary where headers_structures are the keys
        # and arguments are the values.
        return [dict(zip(k, v)) for k, v in zip(headers_structures, arguments)]
    
    def urls(self,*apis):

        """Returns a list of endpoints."""
        url_dict = {'listFormConfigurations': listFormConfigurations_url,
             'getResponses': getResponses_url,
             'getResponseQuestion': getResponseQuestion_url,
             'getResponseQuestionData': getResponseQuestionData_url}
        
        urls = [url_dict[api] for api in apis]
        
        return urls
    
    def __call__(self,*apis):
        outer_list = {}
        payload = {}
        if 'listFormConfigurations' in apis:
            outer_list.update({'listFormConfigurations': requests.request("GET", self.urls('listFormConfigurations')[0],
                                                      headers = self.headers_list(self.headers_structure,self.form_id[0],'listFormConfigurations')[0],
                                                      data = payload).text})
            

        apis = [a for a in apis if a != 'listFormConfigurations']
        
        for form in self.form_id:
            for api, url, header in zip(
                apis,
                self.urls(*apis),
                self.headers_list(self.headers_structure,form,*apis)
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
