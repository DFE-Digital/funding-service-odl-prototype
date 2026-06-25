import requests

url = "https://preprod.externalapi.digital-forms.education.gov.uk/api/getResponseQuestionData"

payload = {}
headers = {
  'StartDate': '2026-05-05',
  'FormId': '7c6iy7ajyi',
  'EndDate': '2026-06-20'
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)
