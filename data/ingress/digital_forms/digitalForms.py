import requests
from listFormConfigurations import url as listFormConfigurations_url
from getResponses import url as getResponses_url
from getResponseQuestion import url as getResponseQuestion_url
from getResponseQuestionData import url as getResponseQuestionData_url

class get_DF:
    def __init__(self,start_date,end_date,form_id):
        self.startdate = start_date
        self.enddate = end_date
        self.formid = form_id
        self.listFormConfigurations_pattern = ['Cookie']
        self.getResponses_pattern = ['StartDate','FormId','EndDate','Cookie']
        self.getResponseQuestion_pattern = ['StartDate','FormId','EndDate','Cookie']
        self.getResponseQuestionData_pattern = ['StartDate','FormId','EndDate']
    

    
    def get(self,*APIs):
        API_options = ['listFormConfigurations','getResponses','getResponseQuestion','getResponseQuestionData']
        for submit in APIs:
            if submit not in API_options:
                raise ValueError(f"Unsupported API name. Enter one or more of the following: {API_options}")
        
        cookie = 'BNIS___utm_is1=iOhL/yEZovIFKNeArS2Ynm5E3krDMFhhvawqqwn2BZrMdhp74duH9QnEwKgLqRDD2jp24zCpTEnersbm4bjSqMyArkI+wBxiHhuvWFW6NI9n1If+pzqsaQ==; BNIS___utm_is2=EFgCQgAaEXLw3hLzBng+v7njvN2G4iIoK/xrcILLEN+g1qm3fc0KZl09WWDch//pR2i8825+pJ4=; BNIS___utm_is3=suvQyLhFSyq+S/jbW+6/0rIkJkC7MiJY4aaGmwjfZ0WIjM90rJEYcAIsnJQevrfkQI0J3asCYACYu6pY1ExffF5yqOKiuYQl0JOeIzZ3wuk=; BNIS_vid=Y8C70dUv6TGhd5aLcDn3BOsAXv50SeMUvz/pmhbyZidvnKTMmQ2Xz21a+yyIXrdcTNx5HiChFu1kjEcapg5ztb8CEUF9V8VNKVUttfAaVns='
        payload = {}

        headers_structure = dict(zip(API_options,[self.listFormConfigurations_pattern,self.getResponses_pattern,self.getResponseQuestion_pattern,self.getResponseQuestionData_pattern]))
        headers_arguments = dict(zip(['StartDate','FormId','EndDate','Cookie'],[self.startdate,self.formid,self.enddate,cookie]))

        for API in APIs:
            headers_arguments[headers_structure[API]]
            
        response = requests.request("GET", url, headers=headers, data=payload)
        return response.text
    
