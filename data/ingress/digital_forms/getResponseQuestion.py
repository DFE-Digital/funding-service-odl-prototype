import requests

url = "https://preprod.externalapi.digital-forms.education.gov.uk/api/getResponseQuestion"

payload = {}
headers = {
  'StartDate': '2026-05-05',
  'FormId': '7c6iy7ajyi',
  'EndDate': '2026-06-20',
  'Cookie': 'BNIS___utm_is1=iOhL/yEZovIFKNeArS2Ynm5E3krDMFhhvawqqwn2BZrMdhp74duH9QnEwKgLqRDD2jp24zCpTEnersbm4bjSqMyArkI+wBxiHhuvWFW6NI9n1If+pzqsaQ==; BNIS___utm_is2=EFgCQgAaEXLw3hLzBng+v7njvN2G4iIoK/xrcILLEN+g1qm3fc0KZl09WWDch//pR2i8825+pJ4=; BNIS___utm_is3=suvQyLhFSyq+S/jbW+6/0rIkJkC7MiJY4aaGmwjfZ0WIjM90rJEYcAIsnJQevrfkQI0J3asCYACYu6pY1ExffF5yqOKiuYQl0JOeIzZ3wuk=; BNIS_vid=Y8C70dUv6TGhd5aLcDn3BOsAXv50SeMUvz/pmhbyZidvnKTMmQ2Xz21a+yyIXrdcTNx5HiChFu1kjEcapg5ztb8CEUF9V8VNKVUttfAaVns='
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)
