import sqlite3
import pandas as pd
import logging
from pathlib import Path

# creating database path
BASE_DIR = Path(__file__).resolve().parent

DB_PATH = BASE_DIR / 'inventory.db'

# creating log directory
LOG_DIR = BASE_DIR / 'logs'

LOG_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    filename=LOG_DIR / "get_vendor_summary.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filemode="a")


def create_vendor_summary(conn):
    '''
    This function will merge the different tables
    to get the overall vendor summary and add new
    columns in the resultant data
    '''

    vendor_sales_summary = pd.read_sql_query(
        """
        WITH FreightSummary AS (

            SELECT
                VendorNumber,
                SUM(Freight) AS FreightCost

            FROM vendor_invoice

            GROUP BY VendorNumber
        ),

        PurchaseSummary AS (

            SELECT
                p.VendorNumber,
                p.VendorName,
                p.Brand,
                p.Description,
                p.PurchasePrice,
                pp.Price AS ActualPrice,
                pp.Volume,

                SUM(p.Quantity) AS TotalPurchaseQuantity,
                SUM(p.Dollars) AS TotalPurchaseDollars

            FROM purchases p

            JOIN purchase_prices pp
                ON p.VendorNumber = pp.VendorNumber
                AND p.Brand = pp.Brand

            WHERE p.PurchasePrice > 0

            GROUP BY
                p.VendorNumber,
                p.VendorName,
                p.Brand,
                p.Description,
                p.PurchasePrice,
                pp.Price,
                pp.Volume
        ),

        SalesSummary AS (

            SELECT
                VendorNo,
                Brand,

                SUM(SalesQuantity) AS TotalSalesQuantity,
                SUM(SalesDollars) AS TotalSalesDollars,

                SUM(SalesDollars)
                / NULLIF(SUM(SalesQuantity), 0)
                AS TotalSalesPrice,

                SUM(ExciseTax) AS TotalExciseTax

            FROM sales

            GROUP BY
                VendorNo,
                Brand
        )

        SELECT
            ps.VendorNumber,
            ps.VendorName,
            ps.Brand,
            ps.Description,

            ps.PurchasePrice,
            ps.ActualPrice,
            ps.Volume,

            ps.TotalPurchaseQuantity,
            ps.TotalPurchaseDollars,

            ss.TotalSalesQuantity,
            ss.TotalSalesDollars,
            ss.TotalSalesPrice,
            ss.TotalExciseTax,

            fs.FreightCost

        FROM PurchaseSummary ps

        LEFT JOIN SalesSummary ss
            ON ps.VendorNumber = ss.VendorNo
            AND ps.Brand = ss.Brand

        LEFT JOIN FreightSummary fs
            ON ps.VendorNumber = fs.VendorNumber

        ORDER BY ps.TotalPurchaseDollars DESC
        """,
        conn
    )

    return vendor_sales_summary


def clean_data(df):
    '''
    This function will clean the data
    '''

    # changing datatype to float
    df['Volume'] = pd.to_numeric(
        df['Volume'],
        errors='coerce'
    )

    # filling missing values with 0
    df.fillna(0, inplace=True)

    # removing space from categorical columns
    df['VendorName'] = df['VendorName'].str.strip()
    df['Description'] = df['Description'].str.strip()

    # creating new columns for better analysis

    # calculating gross profit
    df['GrossProfit'] = (
        df['TotalSalesDollars']
        - df['TotalPurchaseDollars']
    )

    # calculating profit margin
    df['ProfitMargin'] = (
        df['GrossProfit']
        / df['TotalSalesDollars'].replace(0, pd.NA)
    ) * 100

    # calculating stock turnover
    df['StockTurnover'] = (
        df['TotalSalesQuantity']
        / df['TotalPurchaseQuantity'].replace(0, pd.NA)
    )

    # calculating sales to purchase ratio
    df['SalesToPurchaseRatio'] = (
        df['TotalSalesDollars']
        / df['TotalPurchaseDollars'].replace(0, pd.NA)
    )

    return df


if __name__ == '__main__':

    # checking database path
    print(
        "Database path:",
        DB_PATH
    )

    print(
        "Database exists:",
        DB_PATH.exists()
    )


    # database connection
    conn = sqlite3.connect(DB_PATH)

    try:

        logging.info('Creating Vendor Summary Table')

        summary_df = create_vendor_summary(conn)

        logging.info(summary_df.head())

        logging.info('Cleaning Data')

        clean_df = clean_data(summary_df)

        logging.info(clean_df.head())

        logging.info('Ingesting data')

        clean_df.to_sql(
            'vendor_sales_summary',
            conn,
            if_exists='replace',
            index=False
        )

        logging.info('Completed')

        # checking saved table
        print(
            pd.read_sql_query(
                """
                SELECT *
                FROM vendor_sales_summary
                LIMIT 5
                """,
                conn
            )
        )

        # checking number of records
        print(
            pd.read_sql_query(
                """
                SELECT
                    COUNT(*) AS count
                FROM vendor_sales_summary
                """,
                conn
            )
        )

    except Exception:
        logging.exception(
            'Error occurred while creating vendor summary'
        )

        raise

    finally:

        # closing database connection
        conn.close()
