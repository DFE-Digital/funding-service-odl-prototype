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

        headers_structures = []
        #headers_structures becomes a list of lists.
        for api in apis:
            headers_structures.append(headers_structure(*apis)[api])
        
        arguments = []
        #arguments becomes a list of lists with the actual instantiated header
        # arguments for each API submitted.
        #It will be in the order that the apis were submitted, not the
        # api_options order.
        #For instance:
        #[['Cookie'], ['StartDate', 'FormId', 'EndDate', 'Cookie'],
        # ['StartDate', 'FormId', 'EndDate', 'Cookie'],
        # ['StartDate', 'FormId', 'EndDate']]
        for i in range(0,len(headers_structures)):
            arguments.append([])
            for argument in headers_structures[i]:
                arguments[-1].append(headers_arguments[argument])

        #headers_list is a dictionary where headers_structures are the keys
        # and arguments are the values.
        return [dict(zip(k, v)) for k, v in zip(headers_structures, arguments)]
    
    def urls(self,*apis):

        #urls is a list of endpoints.
        urls = []
        for api in apis:
            if api == 'listFormConfigurations':
                urls.append(listFormConfigurations_url)
            if api == 'getResponses':
                urls.append(getResponses_url)
            if api == 'getResponseQuestion':
                urls.append(getResponseQuestion_url)
            if api == 'getResponseQuestionData':
                urls.append(getResponseQuestionData_url)
        
        return urls
    
    def __call__(self,*apis):
        outer_list = []
        count = 0
        for form in self.form_id:
            if count == 1 and len(apis) > 1:
                apis = [a for a in apis if a != 'listFormConfigurations']  
            response_data = []
            payload = {}
            for i in range(0,len(apis)):
                response_data.append(requests.request("GET", self.urls(*apis)[i],
                                                      headers = self.headers_list(self.headers_structure,form,*apis)[i],
                                                      data = payload).text)
            outer_list.append(response_data)
            count += 1
        return outer_list
    
    
 
instance = GetDF('2026-05-05', '2026-06-20', '7c6iy7ajyi','i3If3JGHw8','cb7bii5gx2','o50um3ao3a','x1xtt7u3p0','_igkp1ft5_','59m0cqvlku')
instance_call = instance('listFormConfigurations', 'getResponses',
                   'getResponseQuestion', 'getResponseQuestionData')



#print(instance('listFormConfigurations'))

for api in instance_call:
    print(type(api))
    for i in range(0,len(api)):
        print(len(api[i]))


