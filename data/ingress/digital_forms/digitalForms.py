import requests
import json
import pandas as pd
from loguru import logger
import sys

# Remove default handlers
logger.remove()
logger.add(sys.stderr, level="INFO")
# Create a new log file every day, keep logs for 30 days, zip the old ones
# and only log INFO or higher
logger.add(
    "C:/Users/bmartin2/code_projects/funding-service-odl-prototype/logs/"
    "digital_forms_pipeline_{time:YYYY-MM-DD}.log",
    rotation="1 day",
    retention="30 days",
    compression="zip",
    level="INFO")

listFormConfigurations_url = "https://preprod.externalapi.digital-forms.educ" \
 "ation.gov.uk/api/listFormConfigurations"
getResponses_url = "https://preprod.externalapi.digital-forms.education.gov." \
 "uk/api/getResponses"
getResponseQuestion_url = "https://preprod.externalapi.digital-forms.educati" \
 "on.gov.uk/api/getResponseQuestion"
getResponseQuestionData_url = "https://preprod.externalapi.digital-forms.edu" \
 "cation.gov.uk/api/getResponseQuestionData"

endpoint_list = ['getResponses',
                 'getResponseQuestion',
                 'getResponseQuestionData']

BASE_URL = "https://preprod.externalapi.digital-forms.education.gov.uk/api/"


class DigitalForms:
    """This class can be instantiated with the API headers. Data from the 4
    APIs can be retrieved by calling an instance of this class."""
    def __init__(self, start_date: str, end_date: str, form_ids: list[str]):
        """Initialises DigitalForms with both parameterised attributes and
        a session opening default-initialised attribute. Note that multiple
        form_ids can be passed."""
        self.start_date = start_date
        self.end_date = end_date
        self.form_ids = form_ids
        self.session = requests.Session()

    def get_endpoint_url(self, endpoint_name: str):
        """Returns an endpoint URL from an endpoint reference."""
        return BASE_URL + endpoint_name

    def get_headers(self, formid) -> dict:
        """Returns the headers including the form_id."""
        return {'StartDate': self.start_date,
                'EndDate': self.end_date,
                'FormId': formid}

    def get_data(self):
        """Returns Digital Forms data from the 4 APIs."""
        logger.info("Downloading Digital Forms data...")
        all_data = {}

        try:
            endpoint = 'listFormConfigurations'
            url = self.get_endpoint_url(endpoint)
            api_response = self.session.get(url)
            api_data = api_response.text
            if api_response.status_code == 204:
                logger.warning("No data found for API "
                               f"{endpoint} (code: "
                               f"{api_response.status_code}).")
            else:
                logger.info("Data found for API "
                            f"{endpoint} (code: "
                            f"{api_response.status_code}). "
                            f"Time: "
                            f"{api_response.elapsed
                               .total_seconds():.3f}"
                            "s")

            # JSON validity check
            try:
                json.loads(api_data)
            except json.JSONDecodeError:
                logger.error(
                    f"Invalid JSON for API {endpoint} "
                    f"(code: {api_response.status_code}).")

            all_data[endpoint] = api_data

            for form_id in self.form_ids:
                for endpoint in endpoint_list:
                    headers = self.get_headers(form_id)
                    urls = self.get_endpoint_url(endpoint)
                    api_response = self.session.get(urls, headers=headers)
                    api_data = api_response.text
                    if api_response.status_code == 204:
                        logger.warning("No data found for form "
                                       f"{form_id} and API {endpoint} "
                                       f"(code: {api_response.status_code}).")
                    else:
                        logger.info("Data found for form "
                                    f"{form_id} and API {endpoint} "
                                    f"(code: {api_response.status_code}). "
                                    f"Time: "
                                    f"{api_response.elapsed
                                       .total_seconds():.3f}"
                                    "s")

                    # JSON validity check
                    try:
                        json.loads(api_data)
                    except json.JSONDecodeError:
                        logger.error(
                            f"Invalid JSON for form {form_id} and API "
                            f"{endpoint} (code: {api_response.status_code}).")

                    all_data[form_id + "|" + endpoint] = api_data
            logger.info("Digital Forms data downloaded.")

        except Exception:
            logger.exception("Error downloading Digital Forms data.")
            raise

        return all_data

    def write_data(self, excel):
        """Writes the output of get_data() to an excel."""
        try:
            with pd.ExcelWriter(excel) as writer:
                for sheet_name, json_text in self.get_data().items():
                    data = json.loads(json_text)
                    df = pd.json_normalize(data)
                    df.to_excel(writer, sheet_name=sheet_name[:31],
                                index=False)
            logger.success(f"Data has been written to the {excel} excel.")

        except Exception:
            logger.exception("Error writing Digital Forms data to the excel.")
            raise


digi_forms = DigitalForms('2020-05-05', '2026-06-20', ['7c6iy7ajyi',
                                                       '59m0cqvlku',
                                                       'cb7bii5gx2',
                                                       'o50um3ao3a',
                                                       'x1xtt7u3p0',
                                                       '_igkp1ft5_',
                                                       '59m0cqvlku'])
digi_forms.write_data("DigitalForms2.xlsx")
