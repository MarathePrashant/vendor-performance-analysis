import pandas as pd
from pathlib import Path
from sqlalchemy import create_engine
import logging
import time


# ============================================================
# 1. PROJECT DIRECTORIES
# ============================================================

# Get the folder where Vendor_Analysis.py is located
BASE_DIR = Path(__file__).resolve().parent

# Data folder
DATA_DIR = BASE_DIR / "data"

# Logs folder
LOG_DIR = BASE_DIR / "logs"

# Create logs folder if it doesn't exist
LOG_DIR.mkdir(exist_ok=True)


# ============================================================
# 2. LOGGING CONFIGURATION
# ============================================================

logging.basicConfig(
    filename=LOG_DIR / "ingestion_db.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filemode="a"
)


# ============================================================
# 3. DATABASE CONNECTION
# ============================================================

# SQLite database will be created in the same folder
# as Vendor_Analysis.py

DATABASE_PATH = BASE_DIR / "inventory.db"

engine = create_engine(
    f"sqlite:///{DATABASE_PATH}"
)


# ============================================================
# 4. INGEST DATAFRAME INTO DATABASE
# ============================================================

def ingest_db(df, table_name, engine):
    """
    Ingest a pandas DataFrame into a SQLite database table.
    """

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


# ============================================================
# 5. LOAD CSV FILES
# ============================================================

def load_raw_data():
    """
    Load all CSV files from the data folder
    and ingest them into the SQLite database.
    """

    start = time.time()

    logging.info("========================================")
    logging.info("Starting data ingestion")
    logging.info("========================================")

    # Check whether data folder exists
    if not DATA_DIR.exists():

        logging.error(
            f"Data folder not found: {DATA_DIR}"
        )

        print(f"ERROR: Data folder not found: {DATA_DIR}")

        return

    # Find all CSV files
    csv_files = list(DATA_DIR.glob("*.csv"))

    # Check whether CSV files exist
    if not csv_files:

        logging.warning(
            f"No CSV files found in {DATA_DIR}"
        )

        print(f"No CSV files found in: {DATA_DIR}")

        return

    # Process each CSV file
    for file in csv_files:

        try:

            logging.info(
                f"Reading file: {file.name}"
            )

            print(f"Reading: {file.name}")

            # Read CSV
            df = pd.read_csv(file)

            # Display information
            print(
                f"Loaded: {file.name} | "
                f"Rows: {df.shape[0]} | "
                f"Columns: {df.shape[1]}"
            )

            logging.info(
                f"File: {file.name} | "
                f"Rows: {df.shape[0]} | "
                f"Columns: {df.shape[1]}"
            )

            # Use filename without .csv as table name
            table_name = file.stem

            # Ingest into database
            ingest_db(
                df,
                table_name,
                engine
            )

            print(
                f"Successfully ingested: {table_name}"
            )

        except Exception as e:

            logging.error(
                f"Error processing {file.name}: {e}",
                exc_info=True
            )

            print(
                f"ERROR processing {file.name}: {e}"
            )

    # Calculate total time
    end = time.time()

    total_time = (end - start) / 60

    logging.info(
        f"Total Time Taken: {total_time:.2f} minutes"
    )

    logging.info("Ingestion Complete")
    logging.info("========================================")

    print()
    print("========================================")
    print("Ingestion Complete")
    print(
        f"Total Time Taken: {total_time:.2f} minutes"
    )
    print("========================================")


# ============================================================
# 6. RUN SCRIPT
# ============================================================

if __name__ == "__main__":
    load_raw_data()
