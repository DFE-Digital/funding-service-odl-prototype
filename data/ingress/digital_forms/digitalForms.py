import requests
import json
import pandas as pd
from loguru import logger
import sys
from pathlib import Path

# Remove default handlers
logger.remove()
logger.add(sys.stderr, level="INFO")
# Create a new log file every day, keep logs for 30 days, zip the old ones
# and only log INFO or higher
log_path = Path(__file__).parent / 'logs'
log_path.mkdir(exist_ok=True)

logger.add(
    log_path / "digital_forms_pipeline_{time:YYYY-MM-DD}.log",
    rotation="1 day",
    retention="30 days",
    compression="zip",
    level="INFO")

endpoint_list = ['getResponses',
                 'getResponseQuestion',
                 'getResponseQuestionData']

BASE_URL = "https://preprod.externalapi.digital-forms.education.gov.uk/api/"


class DigitalForms:
    """This class can be instantiated with the API headers. Data from the 4
    APIs can be retrieved by calling an instance of this class."""
    def __init__(self, start_date: str, end_date: str, form_ids: list[str],
                 time_out: int = 300):
        """Initialises DigitalForms with both parameterised attributes and
        a session opening default-initialised attribute. Note that multiple
        form_ids can be passed."""
        self.start_date = start_date
        self.end_date = end_date
        self.form_ids = form_ids
        self.time_out = time_out
        self.session = requests.Session()
        self.api_data = None
        self.api_data_json = None

    def get_endpoint_url(self, endpoint_name: str) -> str:
        """Returns an endpoint URL from an endpoint reference."""
        return BASE_URL + endpoint_name

    def get_headers(self, formid: str) -> dict:
        """Returns the headers including the form_id."""
        return {'StartDate': self.start_date,
                'EndDate': self.end_date,
                'FormId': formid}

    def data_check(self, endpoint, form_id, response):
        """Logs based on the responses status code."""
        check_prefix = f"form {form_id} and API {endpoint}" if form_id else \
            f"API {endpoint}"
        if response.status_code == 204:
            logger.warning(f"No data found for {check_prefix} (code: "
                           f"{response.status_code}).")
        else:
            logger.info(
                f"Data found for {check_prefix} (code: {response.status_code}"
                "). "
                f"Time: {response.elapsed.total_seconds():.3f}s"
                )

    def validate_json(self, api_data, context):
        """JSON validation that terminates ingestion if it fails."""
        try:
            json.loads(api_data)
        except json.JSONDecodeError:
            logger.error(f"Invalid JSON for {context}")
            raise

    def get_data(self) -> dict:
        """Returns Digital Forms data from the 4 APIs."""
        logger.info("Downloading Digital Forms data...")
        all_data = {}
        all_data_json = {}

        try:
            endpoint = 'listFormConfigurations'
            url = self.get_endpoint_url(endpoint)
            api_response = self.session.get(url, timeout=self.time_out)
            api_data = api_response.text

            # JSON validity check
            self.validate_json(api_data, f"API {endpoint} (code: "
                               f"{api_response.status_code}).")

            api_data_json = api_response.json()

            self.data_check(endpoint, None, api_response)

            all_data[endpoint] = api_data
            all_data_json[endpoint] = api_data_json

            for form_id in self.form_ids:
                for ep in endpoint_list:
                    headers = self.get_headers(form_id)
                    urls = self.get_endpoint_url(ep)
                    api_response = self.session.get(urls, headers=headers,
                                                    timeout=self.time_out)
                    api_data = api_response.text

                    # JSON validity check
                    self.validate_json(api_data, f"form {form_id} and API "
                                       f"{ep} (code: "
                                       f"{api_response.status_code}).")

                    api_data_json = api_response.json()

                    self.data_check(ep, form_id, api_response)

                    all_data[form_id + "|" + ep] = api_data
                    all_data_json[form_id + "|" + ep] = api_data_json

            logger.info("Digital Forms data downloaded.")

        except Exception:
            logger.exception("Error downloading Digital Forms data.")
            raise

        self.api_data = all_data
        self.api_data_json = all_data_json

    def write_to_excel(self, excel_prefix: str) -> None:
        """Writes the output of get_data() to excel files."""
        excels = ['listFormConfigurations']
        excels.extend(endpoint_list)
        excels = [excel_prefix+"_"+endpoint+".xlsx" for endpoint in excels]

        try:

            for exc in excels:
                with pd.ExcelWriter(exc) as writer:
                    for sheet_name, json_text in self.api_data.items():
                        if sheet_name.split("|")[-1] != exc.\
                         split("_")[-1].replace(".xlsx", ""):
                            continue
                        df = pd.json_normalize(json.loads(json_text))
                        df.to_excel(writer, sheet_name=sheet_name[:31],
                                    index=False)
            logger.success(f"Data has been written to the {excel_prefix} "
                           "excels.")

        except Exception:
            logger.exception("Error writing Digital Forms data to excel.")
            raise

    def write_to_JSON(self, json_prefix: str) -> None:
        """Writes the output of get_data() to JSON files."""
        jsons = ['listFormConfigurations']
        jsons.extend(endpoint_list)
        jsons = [json_prefix+"_"+endpoint+".json" for endpoint in jsons]

        try:
            for js in jsons:
                with open(js, 'w', encoding='utf-8') as file:
                    filtered_data = {k: v for k, v in self.api_data_json
                                     .items() if k.split("|")[-1] == js
                                     .split("_")[-1].replace(".json", "")}
                    json.dump(filtered_data, file, indent=4)
            logger.success(f"Data has been written to the {json_prefix} "
                           "JSON files.")

        except Exception:
            logger.exception("Error writing Digital Forms data.")
            raise


def run_process(write_excel=False, write_JSON=True) -> None:
    """Orchestrates getting and writing the data for a hardcoded forms list."""
    relevant_forms = [
        '7c6iy7ajyi',
        '59m0cqvlku',
        'cb7bii5gx2',
        'o50um3ao3a',
        'x1xtt7u3p0',
        '_igkp1ft5_',
        '59m0cqvlku'
    ]

    digi_forms = DigitalForms('2020-05-05', '2026-06-20', relevant_forms)
    digi_forms.get_data()

    prefix = "Digital_Forms"

    if write_excel is True:
        digi_forms.write_to_excel(prefix)

    if write_JSON is True:
        digi_forms.write_to_JSON(prefix)


if __name__ == '__main__':
    run_process(write_excel=True, write_JSON=True)
