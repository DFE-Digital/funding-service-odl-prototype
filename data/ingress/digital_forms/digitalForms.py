import requests
from listFormConfigurations import url as listFormConfigurations_url
from getResponses import url as getResponses_url
from getResponseQuestion import url as getResponseQuestion_url
from getResponseQuestionData import url as getResponseQuestionData_url

class GetDF:
    """This class can be instantiated with the required arguments to filter
    data across the 4 Digital Forms APIs."""
    def __init__(self,start_date,end_date,form_id):

        self.start_date = start_date
        self.enddate = end_date
        self.formid = form_id
        self.listFormConfigurations_pattern = ['Cookie']
        self.getResponses_pattern = ['StartDate','FormId','EndDate','Cookie']
        self.getResponseQuestion_pattern = ['StartDate','FormId','EndDate','Cookie']
        self.getResponseQuestionData_pattern = ['StartDate','FormId','EndDate']
    

    
    def get(self,*apis):
        """This instance method can be called with a subset or all 4 Digital
        Forms APIs, using the arbitrary positional arguments parameter (*APIs)
        to retrieve the data"""
        api_options = ['listFormConfigurations', 'getResponses',
                       'getResponseQuestion', 'getResponseQuestionData']
        for submit in apis:
            if submit not in api_options:
                raise ValueError(f"Unsupported API name. Enter" \
                                 "one or more of the following: {api_options}")
        
        cookie = 'BNIS___utm_is1=iOhL/yEZovIFKNeArS2Ynm5E3krDMFhhvawqqwn2BZr' \
        'Mdhp74duH9QnEwKgLqRDD2jp24zCpTEnersbm4bjSqMyArkI+wBxiHhuvWFW6NI9n1I' \
        'f+pzqsaQ==; BNIS___utm_is2=EFgCQgAaEXLw3hLzBng+v7njvN2G4iIoK/xrcILL' \
        'EN+g1qm3fc0KZl09WWDch//pR2i8825+pJ4=; BNIS___utm_is3=suvQyLhFSyq+S/' \
        'jbW+6/0rIkJkC7MiJY4aaGmwjfZ0WIjM90rJEYcAIsnJQevrfkQI0J3asCYACYu6pY1' \
        'ExffF5yqOKiuYQl0JOeIzZ3wuk=; BNIS_vid=Y8C70dUv6TGhd5aLcDn3BOsAXv50S' \
        'eMUvz/pmhbyZidvnKTMmQ2Xz21a+yyIXrdcTNx5HiChFu1kjEcapg5ztb8CEUF9V8VN' \
        'KVUttfAaVns='
        payload = {}

        headers_structure = dict(zip(api_options,[self.listFormConfigurations_pattern,
                                                  self.getResponses_pattern,
                                                  self.getResponseQuestion_pattern,
                                                  self.getResponseQuestionData_pattern]))
        headers_arguments = dict(zip(['StartDate', 'FormId', 'EndDate', 'Cookie'],
                                     [self.start_date, self.formid, self.enddate,
                                      cookie]))

        headers_structures = []
        #becomes a list of lists
        for api in apis:
            headers_structures.append(headers_structure[api])
        
        #print(headers_structures)
        
        arguments = []
        #becomes a list of lists with the actual instantiated header arguments
        #for each API submitted
        #it will be in the order that the APIs were submitted, not the
        #API_options order
        #for instance:
        #[['Cookie'], ['StartDate', 'FormId', 'EndDate', 'Cookie'],
        # ['StartDate', 'FormId', 'EndDate', 'Cookie'],
        # ['StartDate', 'FormId', 'EndDate']]
        for i in range(0,len(headers_structures)):
            arguments.append([])
            for argument in headers_structures[i]:
                arguments[-1].append(headers_arguments[argument])

        #print(arguments)

        #Now need to make dictionaries where headers_structures are the keys
        #and arguments are the values
        headers_list = [dict(zip(k, v)) for k, v in zip(headers_structures, arguments)]
        #print(headers_list)

        #Now to get the URLs in a list
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

        
        response_data = []
        for i in range(0,len(apis)):
            response_data.append(requests.request("GET", urls[i],
                                                  headers=headers_list[i],
                                                  data=payload).text)


  
        return response_data
    
 
instance = GetDF('2026-05-05', '2026-06-20', '7c6iy7ajyi')
print(instance.get('listFormConfigurations', 'getResponses',
                   'getResponseQuestion', 'getResponseQuestionData'))