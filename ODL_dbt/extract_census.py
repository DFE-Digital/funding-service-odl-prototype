import os
import sys
import duckdb
from databricks import sql
import pandas as pd
from dotenv import load_dotenv
from loguru import logger

# load env variables to connect to Databricks
load_dotenv()

# configure loguru to write to both console and a rotating log file
logger.remove()  # remove default handler
logger.add(sys.stderr, level="INFO")
logger.add(
    "logs/census_pipeline_{time:YYYY-MM-DD}.log",
    rotation="10 MB",
    level="DEBUG",
)


class CensusIngestion:
    """Ingest census data from ADA databricks"""

    def __init__(self):
        pass

    def get_databricks_config(self):

        server_hostname = os.getenv("DATABRICKS_SERVER_HOSTNAME")
        http_path = os.getenv("DATABRICKS_HTTP_PATH")
        access_token = os.getenv("DATABRICKS_ACCESS_TOKEN")
        if not all([server_hostname, http_path, access_token]):
            raise ValueError(
                "Missing required Databricks environment variables!"
            )
        return server_hostname, http_path, access_token

    def initialise_local_db(self):
        try:
            # initialise local db
            local_db = duckdb.connect("dev.duckdb")
            local_db.execute("CREATE SCHEMA IF NOT EXISTS main;")
            return local_db
        except Exception as e:
            logger.error(f"Failed to initialise local duckdb instance: {e}")
            raise

    def get_census_data(self, batch_chunk_size: int = 10000):

        server_hostname, http_path, access_token = self.get_databricks_config()
        local_db = self.initialise_local_db()

        try:
            with sql.connect(
                server_hostname=server_hostname,
                http_path=http_path,
                access_token=access_token,
            ) as conn:
                with conn.cursor() as cursor:
                    logger.info("Executing query on Databricks view...")
                    cursor.execute("""select
                AcademicYear,
                CensusTerm as census,
                URN,
                la as LA_Number,
                LAEstab,
                EnrolStatus
                from catalog_30_bronze.tier1.censusseasonssa_masterview
                WHERE AcademicYear IN (202122, 202425)
                AND LA IN (201,202, 203)
                AND (
                        CensusDate BETWEEN DATE '2022-01-01' AND DATE '2022-01-31'
                        OR
                        CensusDate BETWEEN DATE '2025-01-01' AND DATE '2025-01-31'
                    )
                """)  # noqa: E501

                    columns = [desc[0] for desc in cursor.description]

                    # load in chunks
                    is_first_chunk = True
                    chunk_count = 1

                    logger.info("Starting incremental batch extraction...")
                    while True:
                        rows = cursor.fetchmany(batch_chunk_size)
                        if not rows:
                            break

                        logger.info(
                            f"Processing chunk {chunk_count}({len(rows)} rows)"
                        )
                        df = pd.DataFrame(rows, columns=columns)

                        for col in df.columns:
                            try:
                                # convert numeric values to float
                                df[col] = pd.to_numeric(
                                    df[col], errors="coerce"
                                )
                            except Exception:
                                # if string pass as string
                                pass

                        # Register chunk with duckdb
                        local_db.register("chunk_df", df)

                        if is_first_chunk:
                            try:
                                # create table on first chunk
                                local_db.execute(
                                    "CREATE OR REPLACE TABLE main.raw_census AS SELECT * FROM chunk_df"  # noqa: E501
                                )
                                is_first_chunk = False
                            except Exception as e:
                                logger.error(
                                    f"failed to create table"
                                    f" main.raw_census: {e}"
                                )
                                raise
                        else:
                            # append rest of chunks to table
                            try:
                                local_db.execute(
                                    "INSERT INTO main.raw_census "
                                    "SELECT * FROM chunk_df"
                                )
                            except Exception as e:
                                logger.error(
                                    f"failed to insert data for chunk"
                                    f"{chunk_count} into main.raw_census: {e}"
                                )
                                raise

                        chunk_count += 1

                    local_db.close()
                    logger.info(
                        f" Extracted {chunk_count - 1}"
                        f" chunks safely into local dev.duckdb."
                    )
        except Exception as e:
            logger.error(f"Error whilst extracting census data: {e}")
            raise


if __name__ == "__main__":
    census_ingestion = CensusIngestion()
    census_ingestion.get_census_data()
