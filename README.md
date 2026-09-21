# End-to-End Vendor Performance & Supply Chain Analytics

Date: 04/09/2026  
Prepared By: Prashant Marathe  
Target Role: Junior Data Analyst / Data Analyst  
Tech Stack: Python (Pandas, NumPy, SciPy, Matplotlib, Seaborn), SQL (SQLite, CTEs, Joins), Power BI

## Turning Vendor and Sales Data into Actionable Business Insights

Managing vendors is not just about tracking how much they sell.  
Businesses also need to understand **which vendors contribute the most revenue, where profit is coming from, how purchasing compares with sales, and where potential supply-chain inefficiencies exist.**

This project analyzes vendor, purchasing, sales, pricing, and profitability data to answer those questions using **Python, SQL/SQLite concepts, and Power BI**.

The final result is an interactive Power BI dashboard designed to help business teams quickly understand vendor and product performance and make more data-driven procurement decisions.


## 📌 Project Overview

The objective of this project was to analyze vendor and product-level sales data and transform raw transactional information into a business intelligence solution.

I worked through the analysis from **data validation → transformation → data modeling → KPI development → dashboard design → business insights**.

The analysis focuses on:

- Vendor performance
- Sales and purchasing trends
- Gross profitability
- Gross margin
- Product/brand performance
- Sales-to-purchase relationship
- Procurement efficiency
- Potential inventory and supply-chain risks

## 🎯 Business Questions

The project was designed around practical business questions:

- Which vendors generate the highest sales?
- Which vendors contribute the most gross profit?
- How does purchasing compare with sales?
- Which brands/products generate strong revenue?
- Which brands contribute the most profit?
- How does profitability vary across vendors and products?
- Which vendors have stronger sales-to-purchase ratios?
- Where can procurement and inventory decisions be improved?


## 📊 Dataset

The dataset contains 10,648 records and 19 columns at the vendor/brand level.

### Key fields

| Category | Fields |
|---|---|
| Vendor | VendorNumber, VendorName |
| Product | Brand, Description |
| Purchasing | PurchasePrice, TotalPurchaseQuantity, TotalPurchaseDollars |
| Sales | ActualPrice, TotalSalesQuantity, TotalSalesDollars |
| Costs | FreightCost, TotalExciseTax |
| Profitability | GrossProfit, GrossMarginPct |
| Inventory | Volume, StockTurnover |
| Pricing | AveragePurchasePrice, AverageSalesPrice |
| Efficiency | SalesToPurchaseRatio |


## 🛠️ Tools & Technologies

### Data Analysis
- Python
- Pandas
- NumPy

### Business Intelligence
- Power BI Desktop
- Power Query
- DAX

### Data & Querying
- CSV
- SQL / SQLite concepts

### Data Modeling
- Fact and dimension tables
- One-to-many relationships
- Filter context
- KPI measures

## 🔄 Project Workflow

### 1. Data Understanding
I first examined the structure, columns, data types, missing values, and overall quality of the dataset.

This helped establish the grain of the data and identify which metrics could be reliably used for analysis.

### 2. Data Cleaning & Transformation
Using Power Query, the dataset was prepared for reporting by:

- Reviewing column quality
- Validating data types
- Checking missing values
- Removing unnecessary transformation steps
- Validating vendor and brand uniqueness
- Preparing the data for Power BI modeling

An important finding was that some records had missing sales-related metrics because they had **zero sales quantity and zero sales revenue**. These values were treated as meaningful business nulls rather than blindly replacing them with zero.

### 3. Data Validation
I created validation queries to check whether important financial calculations reconciled correctly.

Examples include:
Purchase Dollars ≈ Purchase Price × Purchase Quantity

Sales Dollars ≈ Actual Price × Sales Quantity

Gross Profit = Sales Dollars − Purchase Dollars

Gross Margin % = Gross Profit / Sales
