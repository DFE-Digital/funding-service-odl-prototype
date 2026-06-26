import io
import sys

import requests
import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine, text
from utils import camel_to_snake_case, clean_column

# Configuration
BASE_URL = " https://ea-edubase-api-prod.azurewebsites.net/edubase/downloads/public/"  
DATASETS_TABLE_NAMES={"edubasealldata":"establishment_all_fields", 
                    "links_edubasealldata":"establishment_links",
                    "edubaseallacademiesandfree":"academies_and_free_school_ﬁelds",
                    "links_edubaseallacademiesandfree":"academies_and_free_school_links",
                    "edubaseallstatefunded":"state-funded_school_ﬁelds",
                    "links_edubaseallstatefunded":"state-funded_school_links",
                    "edubaseallchildrencentre":"childrens_centre_ﬁelds",
                    "links_edubaseallchildrencentre":"all_open_childrens_centres_links",
                    "academiesmatmembership":"SAT_and_MAT_membership_history",
                    "allgroupsdata":"all_group_records",
                    "alllinksdata":"all_group_links_records",
                    "grouplinks_edubaseallacademiesandfree":"academy_sponsor_and_trust_links",
                    "governancealldata":"governor_ﬁelds",
                    "governancematdata":"all_multiacademy_trust_governance_records",
                    "governanceacaddata":"all_academy_governance_records",
                    "governanceladata":"all_local_authority_maintained_governance_records",
                    }
today = datetime.now().strftime("%Y%m%d")
FILE_TYPE = ".csv"

# Set up dolt connection
DOLT_CONN = "mysql+pymysql://root@127.0.0.1:3306/gias"
engine = create_engine(DOLT_CONN)

#Keep log of any failed datasets
failed_datasets={}

for _, (DATASET, TABLE_NAME) in enumerate(DATASETS_TABLE_NAMES.items()):
    print(f"\nProcessing Dataset: {DATASET}:")
    try:
        # # Build url
        url = f"{BASE_URL}{DATASET}{today}{FILE_TYPE}"
        print(f"Downloading: {url}")

        # # Download file
        response = requests.get(url)

        if response.status_code != 200:
            raise Exception(f"Download failed for {DATASET}: {response.status_code}")

        # Read in data
        df = pd.read_csv(io.BytesIO(response.content), encoding="latin1", low_memory=False)

        # Clean columns
        #df.columns = [camel_to_snake_case(c) for c in df.columns]
        df.columns = [clean_column(c) for c in df.columns]



        # Load data in 
        df.to_sql(TABLE_NAME, engine, if_exists="replace", index=False)
        print(f"Loaded {len(df)} rows into {TABLE_NAME}")

    except Exception as e:
        print(f"Error processing dataset '{DATASET}': {e}", file=sys.stderr)
        failed_datasets[DATASET] = str(e)
        continue

print("\n-----Pipeline Summary-----\n")

if failed_datasets:
    print(f"Pipeline completed with {len(failed_datasets)} error(s):")
    failed_dataset_names=[]
    for dataset, err in failed_datasets.items():
        failed_dataset_names.append(dataset)
        print(f"  - {dataset}: {err}")
    commit_message = f"All GIAS tables loaded in for {today} except {failed_dataset_names}"    
else:
    print("All datasets processed and loaded successfully")
    commit_message = f"All GIAS tables loaded in for {today}"

try:
    print("\nStaging and committing changes to Dolt history:")
    
    with engine.connect() as conn:
        conn.execute(text("CALL DOLT_ADD('-A');"))
        conn.execute(
            text("CALL DOLT_COMMIT('-m', :msg);"), 
            {"msg": commit_message}
        )
        
    print("Successfully commited GIAS data to Dolt")

except Exception as e:
    print(f"GIAS data loaded, but Dolt commit failed: {e}", file=sys.stderr)