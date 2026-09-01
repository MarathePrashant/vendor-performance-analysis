import pandas as pd
from pathlib import Path
from sqlalchemy import create_engine
import logging
import time

# PROJECT DIRECTORIES

BASE_DIR = Path(__file__).resolve().parent

DATA_DIR = BASE_DIR / "data"

LOG_DIR = BASE_DIR / "logs"

# Create logs folder
LOG_DIR.mkdir(exist_ok=True)


# LOGGING

logging.basicConfig(
    filename=LOG_DIR / "ingestion_db.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filemode="a")

# DATABASE

DATABASE_PATH = BASE_DIR / "inventory.db"

engine = create_engine(f"sqlite:///{DATABASE_PATH}")

# INGEST DATA INTO DATABASE

def ingest_db(df, table_name, engine):

    df.to_sql(
        table_name,
        con=engine,
        if_exists="replace",
        index=False
    )

    logging.info(
        f"Successfully loaded table '{table_name}' "
        f"with {len(df)} rows."
    )

# Load CSV Files


def load_raw_data():
    start = time.time()

    logging.info("Starting data ingestion")

    # Check data folder
    if not DATA_DIR.exists():
        logging.error(f"Data folder not found: {DATA_DIR}")

        print(f"ERROR: Data folder not found: {DATA_DIR}")
        return

    # Find CSV files
    csv_files = list(DATA_DIR.glob("*.csv"))

    if not csv_files:
        logging.warning(f"No CSV files found in {DATA_DIR}")
        print(f"No CSV files found in: {DATA_DIR}")
        return

    # Process each CSV
    for file in csv_files:
        try:
            print(f"Reading: {file.name}")
            logging.info(f"Reading file: {file.name}")

            # Read CSV
            df = pd.read_csv(file)

            print(f"Loaded: {file.name} | "
                f"Rows: {df.shape[0]} | "
                f"Columns: {df.shape[1]}")

            logging.info(
                f"File: {file.name} | "
                f"Rows: {df.shape[0]} | "
                f"Columns: {df.shape[1]}")

            # CSV filename becomes database table name
            table_name = file.stem

            # Insert into database
            ingest_db(df,table_name,engine)

            print(f"Successfully ingested: {table_name}")
        except Exception as e:
            logging.error(f"Error processing {file.name}: {e}",exc_info=True)
            print(f"ERROR processing {file.name}: {e}")

    # Calculate execution time
    end = time.time()

    total_time = (end - start) / 60

    logging.info(f"Total Time Taken: {total_time:.2f} minutes")
    logging.info("Ingestion Complete")

    print()
    print("Ingestion Complete")
    print(f"Total Time Taken: {total_time:.2f} minutes")

# RUN PROGRAM
if __name__ == "__main__":
    load_raw_data()