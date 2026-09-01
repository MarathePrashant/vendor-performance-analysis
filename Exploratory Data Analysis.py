import pandas as pd
import sqlite3
import os
import time
import numpy as np

# creating database connection
conn = sqlite3.connect(
    r'C:\Users\prash\OneDrive\Documents\PERSONAL LIBRARY\Programming\GitHub\Vendor\inventory.db'
)

# checking tables in database
tables = pd.read_sql_query(
    "SELECT name FROM sqlite_master WHERE type='table'",
    conn
)

for table in tables['name']:
    print('-' * 50, f'{table}', '-' * 50)

    print(
        'Count of records:',
        pd.read_sql_query(
            f"SELECT COUNT(*) AS count FROM {table}",
            conn
        )['count'].values[0]
    )

    print(
        pd.read_sql_query(
            f"SELECT * FROM {table} LIMIT 5",
            conn
        )
    )


# checking purchase data for a particular vendor
purchase = pd.read_sql_query(
    "SELECT * FROM purchases WHERE VendorNumber = 4466",
    conn
)

print(purchase)


# checking purchase prices for a particular vendor
purchase_prices = pd.read_sql_query(
    "SELECT * FROM purchase_prices WHERE VendorNumber = 4466",
    conn
)

print(purchase_prices)


# checking vendor invoice data for a particular vendor
vendor_invoice = pd.read_sql_query(
    "SELECT * FROM vendor_invoice WHERE VendorNumber = 4466",
    conn
)

print(vendor_invoice)


# checking sales data for a particular vendor
sales = pd.read_sql_query(
    "SELECT * FROM sales WHERE VendorNo = 4466",
    conn
)

print(sales)


# checking purchase summary
print(
    purchase.groupby(
        ["Brand", "PurchasePrice"]
    )[['Quantity', 'Dollars']].sum()
)


# checking purchase prices
print(purchase_prices)


# checking vendor invoice
print(vendor_invoice)


# checking number of unique purchase orders
print(vendor_invoice['PONumber'].nunique())


# checking sales summary
print(
    sales.groupby('Brand')[
        ['SalesDollars', 'SalesPrice', 'SalesQuantity']
    ].sum()
)


"""
The purchases table contains actual purchase data, including:
- date of purchase
- products/brands purchased
- quantity purchased
- amount paid

The purchase_prices table provides:
- actual product price
- purchase price
- volume

The combination of VendorNumber and Brand is unique
in the purchase_prices table.

The vendor_invoice table contains:
- purchase order information
- quantity
- dollars
- freight cost

The sales table contains:
- products/brands sold
- sales quantity
- sales price
- sales dollars
- excise tax

Since the data required for analysis is distributed
across different tables, we create a summary table containing:

- purchase transactions
- sales transactions
- vendor freight costs
- actual product prices
"""


# checking vendor invoice columns
print(vendor_invoice.columns)


# checking duplicate VendorNumber and Brand combinations
purchase_price_duplicates = pd.read_sql_query(
    """
    SELECT
        VendorNumber,
        Brand,
        COUNT(*) AS count

    FROM purchase_prices

    GROUP BY
        VendorNumber,
        Brand

    HAVING COUNT(*) > 1
    """,
    conn
)

print(
    "Duplicate VendorNumber and Brand combinations:"
)

print(purchase_price_duplicates)


# creating freight summary
Freight_summary = pd.read_sql_query(
    """
    SELECT
        VendorNumber,
        SUM(Freight) AS FreightCost

    FROM vendor_invoice

    GROUP BY VendorNumber
    """,
    conn
)

print(Freight_summary)


# creating purchase summary
purchase_summary = pd.read_sql_query(
    """
    SELECT
        p.VendorNumber,
        p.VendorName,
        p.Brand,
        p.Description,
        p.PurchasePrice,
        pp.Volume,
        pp.Price AS ActualPrice,

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
        pp.Volume,
        pp.Price

    ORDER BY TotalPurchaseDollars DESC
    """,
    conn
)

print(purchase_summary.head())


# checking sales columns
print(sales.columns)


# creating sales summary
sales_summary = pd.read_sql_query(
    """
    SELECT
        VendorNo,
        VendorName,
        Brand,

        SUM(SalesDollars) AS TotalSalesDollars,

        SUM(SalesQuantity) AS TotalSalesQuantity,

        SUM(SalesDollars)
        / NULLIF(SUM(SalesQuantity), 0)
        AS AverageSalesPrice,

        SUM(ExciseTax) AS TotalExciseTax

    FROM sales

    GROUP BY
        VendorNo,
        VendorName,
        Brand

    ORDER BY TotalSalesDollars DESC
    """,
    conn
)

print(sales_summary.head())


# creating final vendor sales and purchase summary

start = time.time()

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
            AS AverageSalesPrice,

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
        ss.AverageSalesPrice,
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

end = time.time()

print(
    "Time taken:",
    end - start,
    "seconds"
)


# checking final table
print(vendor_sales_summary.head())

print(vendor_sales_summary.columns)

print(
    "Number of records:",
    len(vendor_sales_summary)
)


# checking datatypes
print(vendor_sales_summary.dtypes)


# checking missing values
print(vendor_sales_summary.isnull().sum())


# printing unique values
print(vendor_sales_summary['VendorName'].unique())

print(vendor_sales_summary['Description'].unique())


# changing data type
vendor_sales_summary["Volume"] = (
    pd.to_numeric(
        vendor_sales_summary['Volume'],
        errors='coerce'
    )
)


# removing spaces from VendorName
vendor_sales_summary['VendorName'] = (
    vendor_sales_summary["VendorName"].str.strip()
)


# removing spaces from Description
vendor_sales_summary['Description'] = (
    vendor_sales_summary["Description"].str.strip()
)


# filling missing numeric values
numeric_columns = [
    'TotalPurchaseQuantity',
    'TotalPurchaseDollars',
    'TotalSalesQuantity',
    'TotalSalesDollars',
    'TotalExciseTax',
    'FreightCost'
]

vendor_sales_summary[numeric_columns] = (
    vendor_sales_summary[numeric_columns].fillna(0)
)


# creating new columns

# calculating gross profit
vendor_sales_summary['GrossProfit'] = (
    vendor_sales_summary["TotalSalesDollars"]
    - vendor_sales_summary["TotalPurchaseDollars"]
)


# calculating gross margin percentage
vendor_sales_summary['GrossMarginPct'] = (
    vendor_sales_summary["GrossProfit"]
    / vendor_sales_summary["TotalSalesDollars"].replace(0, np.nan)
) * 100


# calculating stock turnover
vendor_sales_summary['StockTurnover'] = (
    vendor_sales_summary["TotalSalesQuantity"]
    / vendor_sales_summary["TotalPurchaseQuantity"].replace(0, np.nan)
)


# calculating sales to purchase ratio
vendor_sales_summary['SalesToPurchaseRatio'] = (
    vendor_sales_summary["TotalSalesDollars"]
    / vendor_sales_summary["TotalPurchaseDollars"].replace(0, np.nan)
)


# calculating average purchase price
vendor_sales_summary['AveragePurchasePrice'] = (
    vendor_sales_summary["TotalPurchaseDollars"]
    / vendor_sales_summary["TotalPurchaseQuantity"].replace(0, np.nan)
)


# replacing infinite values
vendor_sales_summary.replace(
    [np.inf, -np.inf],
    np.nan,
    inplace=True
)


# checking final missing values
print(
    "Missing values after cleaning:"
)

print(
    vendor_sales_summary.isnull().sum()
)


# checking final dataframe
print(vendor_sales_summary.head())


# saving final summary table into database
vendor_sales_summary.to_sql(
    'vendor_sales_summary',
    conn,
    if_exists='replace',
    index=False
)


# checking saved table
print(
    pd.read_sql_query(
        "SELECT * FROM vendor_sales_summary LIMIT 5",
        conn
    )
)

# checking number of records in final table
print(
    pd.read_sql_query(
        "SELECT COUNT(*) AS count FROM vendor_sales_summary",
        conn
    )
)
# closing database connection
conn.close()


# 1:03  
