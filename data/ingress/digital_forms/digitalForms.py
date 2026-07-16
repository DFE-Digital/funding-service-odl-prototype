import json
import sys
from pathlib import Path

import requests
from loguru import logger

# Remove default handlers
logger.remove()
logger.add(sys.stderr, level="INFO")
# Create a new log file every day, keep logs for 30 days, zip the old ones
# and only log INFO or higher
log_path = Path(__file__).parent / "logs"
log_path.mkdir(exist_ok=True)

logger.add(
    log_path / "digital_forms_pipeline_{time:YYYY-MM-DD}.log",
    rotation="1 day",
    retention="30 days",
    compression="zip",
    level="INFO",
)

endpoint_list = ["getResponses", "getResponseQuestion",
                 "getResponseQuestionData"]

BASE_URL = "https://preprod.externalapi.digital-forms.education.gov.uk/api/"


class DigitalForms:
    """This class can be instantiated with the API headers. Data from the 4
    APIs can be retrieved by calling an instance of this class."""

    def __init__(
        self, start_date: str, end_date: str, form_ids: list[str],
            time_out: int = 300
            ):
        """Initialises DigitalForms with both parameterised attributes and
        a session opening default-initialised attribute. Note that multiple
        form_ids can be passed."""
        self.start_date = start_date
        self.end_date = end_date
        self.form_ids = form_ids
        self.time_out = time_out
        self.session = requests.Session()
        self.api_data = None

    def get_endpoint_url(self, endpoint_name: str) -> str:
        """Returns an endpoint URL from an endpoint reference."""
        return BASE_URL + endpoint_name

    def get_headers(self, formid: str) -> dict:
        """Returns the headers including the form_id."""
        return {
            "StartDate": self.start_date,
            "EndDate": self.end_date,
            "FormId": formid,
        }

    def safe_get(self, url, headers=None):
        response = self.session.get(url, headers=headers,
                                    timeout=self.time_out)
        response.raise_for_status()
        return response

    def data_check(self, endpoint, form_id, response):
        """Logs based on the responses status code."""
        check_prefix = (
            f"form {form_id} and API {endpoint}" if form_id else f"API "
            f"{endpoint}"
        )
        if response.status_code == 204:
            logger.warning(
                f"No data found for {check_prefix} (code: "
                f"{response.status_code})."
            )
        else:
            logger.info(
                f"Data found for {check_prefix} (code: {response.status_code}"
                "). "
                f"Time: {response.elapsed.total_seconds():.3f}s"
            )

    def api_data_json(self, api_response, endpoint):
        """JSON validation that terminates ingestion if it fails."""
        try:
            return api_response.json()
        except json.JSONDecodeError:
            logger.error(f"Invalid JSON for API {endpoint} "
                         f"(code: {api_response.status_code}).")
            raise

    def close_session(self):
        self.session.close()

    def get_data(self) -> dict:
        """Returns Digital Forms data from the 4 APIs."""
        logger.info("Downloading Digital Forms data...")
        all_data = {}

        try:
            endpoint = "listFormConfigurations"
            url = self.get_endpoint_url(endpoint)
            api_response = self.safe_get(url)

            api_data = self.api_data_json(api_response, endpoint)

            self.data_check(endpoint, None, api_response)

            all_data[endpoint] = api_data

            for form_id in self.form_ids:
                for ep in endpoint_list:
                    headers = self.get_headers(form_id)
                    urls = self.get_endpoint_url(ep)
                    api_response = self.safe_get(urls, headers)

                    api_data = self.api_data_json(api_response, ep)

                    self.data_check(ep, form_id, api_response)

                    all_data[form_id + "|" + ep] = api_data

            logger.info("Digital Forms data downloaded.")

        except Exception:
            logger.exception("Error downloading Digital Forms data.")
            raise

        self.api_data = all_data

    def write_to_JSON(self, json_prefix: str) -> None:
        """Writes the output of get_data() to JSON files."""
        jsons = ["listFormConfigurations"]
        jsons.extend(endpoint_list)
        jsons = [json_prefix + "_" + endpoint + ".json" for endpoint in jsons]

        try:
            for js in jsons:
                with open(js, "w", encoding="utf-8") as file:
                    filtered_data = {
                        k: v
                        for k, v in self.api_data.items()
                        if k.split("|")[-1] == js.split("_")[-1]
                        .replace(".json", "")
                    }
                    json.dump(filtered_data, file, indent=4)
            logger.success(f"Data has been written to the {json_prefix} JSON "
                           "files.")

        except Exception:
            logger.exception("Error writing Digital Forms data.")
            raise


def run_process(scoped_forms: list[str]) -> None:
    """Orchestrates getting and writing the data."""

    digi_forms = DigitalForms("2020-05-05", "2026-06-20", scoped_forms)
    digi_forms.get_data()

    prefix = "Digital_Forms"
    digi_forms.write_to_JSON(prefix)

    digi_forms.close_session()


if __name__ == "__main__":
    run_process([
        "7c6iy7ajyi",
        "59m0cqvlku",
        "cb7bii5gx2",
        "o50um3ao3a",
        "x1xtt7u3p0",
        "_igkp1ft5_",
    ])
