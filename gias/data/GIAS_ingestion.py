import io
import json
import os
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
import pandas as pd
from pandas import DataFrame
import requests
from loguru import logger
from sqlalchemy import create_engine, text
from utils import clean_column
from requests import Response

# Configure Loguru to write to both console and a rotating log file
logger.remove()  # Remove default handler
logger.add(sys.stderr, level="INFO")
logger.add("logs/gias_pipeline_{time:YYYY-MM-DD}.log", rotation="10 MB", level="DEBUG")

class GIASIngestion:
    def __init__(self, base_url: str, datasets: dict, storage_dir: str = "GIAS_data"):
        self.base_url = base_url
        self.datasets = datasets
        self.storage_dir = Path(storage_dir)
        self.today = datetime.now().strftime("%Y%m%d")
        self.failed_datasets = {}

        # Ensure backup directory exists
        self.storage_dir.mkdir(parents=True, exist_ok=True)

    def get_dataset_url(self, dataset: str) -> str:
        """Return dataset url.

        Args:
            dataset (str): dataset to download
        """
        return f"{self.base_url}{dataset}{self.today}.csv"

    def download_dataset(self, url:str) -> bytes:
        """ Download the GIAS dataset and get content

        Args:
            url (str): url to download GIAS data from

        Raises:
            RuntimeError: shows download error and response status code

        Returns:
            Response: content of downloaded csv
        """
        
        logger.info(f"Downloading {url}")
        try:
            response = requests.get(url, timeout=30)
            if response.status_code != 200:
                raise RuntimeError(f"HTTP download failed with status: {response.status_code}")
            return response.content
        except Exception as e:
            logger.error(f"Error downloading URL {url}: {e}")
            raise
        
    
    def clean_data(self, data: bytes) -> DataFrame:
        """Convert from bytes to DataFrame and clean columns 

        Args:
            data (bytes): downloaded csv data in bytes

        Returns:
            DataFrame: Pandas dataframe of downloaded GIAS data
        """
        try:
            df = pd.read_csv(io.BytesIO(data), encoding="latin1", low_memory=False)
            df.columns = [clean_column(c) for c in df.columns]
            return df
        except Exception as e:
            logger.error(f"Error parsing/cleaning columns: {e}")
            raise
        
    def save_to_json(self, df:DataFrame, dataset_name:str) -> None:
        """Save the ingested GIAS data

        Args:
            df (DataFrame): DataFrame object of GIAS data
            dataset_name (str): dataset name taken from GIAS website
        """
        try:
            json_file_path = self.storage_dir / f"{dataset_name}_{self.today}.json"
            df.to_json(json_file_path, orient="records", date_format="iso", indent=4)
            logger.success(f"Json file written for {dataset_name} written to {json_file_path}")
        except Exception as e:
            logger.error(f"Failed to write json file for {dataset_name}:{e}")
            raise
        
        
    def run(self):
        """Orchestrates the entire execution runtime wrapper lifecycle."""
      
        logger.info(f"Starting GIAS Ingestion for {self.today}")

        for dataset, table_name in self.datasets.items():
            try:
                url= self.get_dataset_url(dataset)
                data=self.download_dataset(url)
                df=self.clean_data(data)
                self.save_to_json(df=df, dataset_name=table_name)

            except Exception as e:
                logger.error(f"Pipeline component '{dataset}' failed processing.")
                self.failed_datasets[dataset] = str(e)
                continue
  
        logger.info("Finshed downloading datasets")
        if self.failed_datasets:
            logger.warning(f"Ingestion completed with {len(self.failed_datasets)} dataset failure(s).")
        else:
            logger.success("Injestion completed successfully for all datasets.")

if __name__ == "__main__":
    gias_base_url = " https://ea-edubase-api-prod.azurewebsites.net/edubase/downloads/public/"  
        
    gias_datasets={"edubasealldata":"establishment_all_fields", 
                    "links_edubasealldata":"establishment_links",
                    "edubaseallacademiesandfree":"academies_and_free_school_ﬁelds",
                    "edubaseallchildrencentre":"childrens_centre_ﬁelds",
                    "academiesmatmembership":"SAT_and_MAT_membership_history",
                    "allgroupsdata":"all_group_records",
                    "alllinksdata":"all_group_links_records",
                    "grouplinks_edubaseallacademiesandfree":"academy_sponsor_and_trust_links",
                    "governancealldata":"governor_ﬁelds",
                    "governancematdata":"all_multiacademy_trust_governance_records",
                    "governanceacaddata":"all_academy_governance_records",
                    "governanceladata":"all_local_authority_maintained_governance_records",
                    }


    # run ingestion
    gias_injestion=GIASIngestion(base_url= gias_base_url, datasets=gias_datasets)

    gias_injestion.run()