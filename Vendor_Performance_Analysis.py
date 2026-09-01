import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
import sqlite3
from pathlib import Path
from scipy.stats import ttest_ind
import scipy.stats as stats
from IPython.display import display

warnings.filterwarnings("ignore")

# Loading Dataset and Connecting to SQLite

# Get the folder where this Python file is located
BASE_DIR = Path(__file__).resolve().parent

# Database is in the same folder as this Python file
DB_PATH = BASE_DIR / "inventory.db"

print("DATABASE CHECK")
print("Database:", DB_PATH)
print("Database exists:", DB_PATH.exists())

if not DB_PATH.exists():
    raise FileNotFoundError(f"Database not found at: {DB_PATH}")

# Connect to SQLite database
conn = sqlite3.connect(DB_PATH)

# Check Available Tables

print("\nTables in database:")

tables = pd.read_sql_query(
    """
    SELECT name
    FROM sqlite_master
    WHERE type = 'table'
    ORDER BY name
    """,
    conn
)

print(tables.to_string(index=False))

# Check Vendor Summary Table

if "vendor_sales_summary" not in tables["name"].values:
    conn.close()
    raise RuntimeError("Table 'vendor_sales_summary' does not exist in the database.")

# Fetch Vendor Summary Data

df = pd.read_sql_query("SELECT * FROM vendor_sales_summary", conn)

print("\nVENDOR SALES SUMMARY")
print(df.head())
print("\nDataset shape:")
print(df.shape)
print("\nColumns:")
print(df.columns.tolist())

# Exploratory Data Analysis

# As we examined various tables in the database to identify key variables,
# understand their relationships, and determine which ones should be included
# in the final analysis.
#
# Now let's analyze the resultant table to gain insights into the distribution
# of each column, which helps understand patterns, identify anomalies, and
# ensure data quality before proceeding with further analysis.

# Summary Statistics

print("\nSUMMARY STATISTICS")
print(df.describe().T)

# Numerical Columns

numerical_cols = df.select_dtypes(include=np.number).columns

# Distribution Plots for Numerical Columns

plt.figure(figsize=(18, 22))
rows = int(np.ceil(len(numerical_cols) / 4))

for i, column in enumerate(numerical_cols):
    plt.subplot(rows, 4, i + 1)
    sns.histplot(df[column].dropna(), kde=True)
    plt.title(column, fontsize=10)

plt.tight_layout()
plt.show()

# Outliers Detection using Boxplot

plt.figure(figsize=(18, 22))
rows = int(np.ceil(len(numerical_cols) / 4))

for i, col in enumerate(numerical_cols):
    plt.subplot(rows, 4, i + 1)
    sns.boxplot(y=df[col].dropna())
    plt.title(col, fontsize=10)

plt.tight_layout()
plt.show()

# Summary Statistics Insights

# Negative & Zero Values:
#
# Gross Profit: Minimum value is negative, indicating losses.
# Some products or transactions may be selling at a loss due to high costs
# or selling at discounts lower than the purchase price.
#
# Gross Margin Percentage: Negative values may indicate products being
# sold below their effective cost.
#
# Total Sales Quantity & Sales Dollars: Minimum values of 0 mean some
# products were purchased but never sold.
#
# These could be slow-moving or obsolete stock.

# Outliers:
#
# Purchase Price and Actual Price have very high maximum values compared
# with their average values, indicating potential premium products.
#
# Freight Cost has large variation, suggesting differences in shipping
# quantities and logistics costs.
#
# Stock Turnover has a wide range, meaning some products sell quickly
# while others remain in inventory for longer periods.

# Filtering Data to Remove Inconsistencies

df = pd.read_sql_query(
    """
    SELECT *
    FROM vendor_sales_summary
    WHERE GrossProfit > 0
    AND GrossMarginPct > 0
    AND TotalSalesQuantity > 0
    """,
    conn
)

print("\nFILTERED DATA")
print(df.head())
print("\nFiltered Dataset Shape:")
print(df.shape)

# Export vendor_sales_summary to CSV
csv_path = BASE_DIR / "vendor_sales_summary.csv"
df = pd.read_sql_query("SELECT * FROM vendor_sales_summary",conn)
df.to_csv(csv_path, index=False)
print("CSV created successfully:")
print(csv_path)


# Close Database Connection

conn.close()

print("\nDatabase connection closed.")
print("SUCCESS")

# Recalculate Numerical Columns After Filtering

numerical_cols = df.select_dtypes(include=np.number).columns

# Distribution Plots After Filtering

plt.figure(figsize=(18, 22))
rows = int(np.ceil(len(numerical_cols) / 4))

for i, column in enumerate(numerical_cols):
    plt.subplot(rows, 4, i + 1)
    sns.histplot(df[column].dropna(), kde=True)
    plt.title(column, fontsize=10)

plt.tight_layout()
plt.show()

# Count Plots for Categorical Columns

categorical_cols = ["VendorName", "Description"]

plt.figure(figsize=(16, 8))

for i, col in enumerate(categorical_cols):
    plt.subplot(1, 2, i + 1)
    sns.countplot(y=df[col], order=df[col].value_counts().index[:10])
    plt.title(f"Top 10 {col}", fontsize=12)

plt.tight_layout()
plt.show()

# Correlation Heatmap

plt.figure(figsize=(16, 12))
correlation_matrix = df[numerical_cols].corr()

sns.heatmap(
    correlation_matrix,
    annot=True,
    fmt=".2f",
    cmap="coolwarm",
    linewidth=0.5
)

plt.title("Correlation Heatmap")
plt.tight_layout()
plt.show()

'''
Correlation Insights -

- PurchasePrice has weak correlations with TotalSalesDollars and
  GrossProfit, suggesting that price variations alone do not strongly
  determine sales revenue or profit.

- TotalPurchaseQuantity and TotalSalesQuantity have a very strong
  correlation, indicating that products purchased in larger quantities
  are generally sold in larger quantities.

- GrossMarginPct can have relationships with pricing and profitability,
  helping identify products with stronger or weaker margins.

- StockTurnover helps identify products that move quickly versus products
  that remain in inventory for longer periods.
'''

# Business Problems

'''
Q1. Identify Brand that needs Promotional or Pricing Adjustments
which exhibit lower sales performance but higher profit margins.
'''

# Q1. Low Sales but High Profit Margin Brands

brand_performance = df.groupby("Description").agg({
    "TotalSalesDollars": "sum",
    "GrossMarginPct": "mean"
}).reset_index()

low_sales_threshold = brand_performance["TotalSalesDollars"].quantile(0.15)
high_margin_threshold = brand_performance["GrossMarginPct"].quantile(0.85)

print("\nLow Sales Threshold:")
print(low_sales_threshold)

print("\nHigh Margin Threshold:")
print(high_margin_threshold)

# Filtering brands with low sales but high profit margins

target_brands = brand_performance[
    (brand_performance["TotalSalesDollars"] <= low_sales_threshold) &
    (brand_performance["GrossMarginPct"] >= high_margin_threshold)
]

print("\nBrand with Low Sales but High Profit Margins:")

display(target_brands.sort_values("TotalSalesDollars"))

# Q1 Visualization

plt.figure(figsize=(10, 6))

sns.scatterplot(
    data=brand_performance,
    x="TotalSalesDollars",
    y="GrossMarginPct",
    color="blue",
    label="All Brands",
    alpha=0.2
)

sns.scatterplot(
    data=target_brands,
    x="TotalSalesDollars",
    y="GrossMarginPct",
    color="red",
    label="Target Brands"
)

plt.axhline(
    high_margin_threshold,
    linestyle="--",
    color="black",
    label="High Margin Threshold"
)

plt.axvline(
    low_sales_threshold,
    linestyle="--",
    color="black",
    label="Low Sales Threshold"
)

plt.xlabel("Total Sales ($)")
plt.ylabel("Gross Margin (%)")
plt.title("Brands for Promotional or Pricing Adjustments")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

'''
Q2. Which vendors and brands demonstrate the highest sales performance
'''

def format_dollars(value):
    if value >= 1_000_000:
        return f"{value / 1_000_000:.2f}M"
    elif value >= 1_000:
        return f"{value / 1_000:.2f}K"
    else:
        return f"{value:.2f}"

# Top Vendors and Brands

top_vendors = (
    df.groupby("VendorName")["TotalSalesDollars"]
      .sum()
      .nlargest(10)
)

top_brands = (
    df.groupby("Description")["TotalSalesDollars"]
      .sum()
      .nlargest(10)
)

print("\nTOP 10 VENDORS BY SALES")
print(top_vendors)

print("\nTOP 10 BRANDS BY SALES")
print(top_brands)

print("\nFormatted Top Brand Sales:")
print(top_brands.apply(lambda x: format_dollars(x)))

# Bar Plot

plt.figure(figsize=(15, 5))

# Plot for Top Vendors

plt.subplot(1, 2, 1)

ax1 = sns.barplot(
    y=top_vendors.index,
    x=top_vendors.values,
    palette="Blues_r"
)

plt.title("Top 10 Vendors by Sales")

for bar in ax1.patches:
    ax1.text(
        bar.get_width() + (bar.get_width() * 0.02),
        bar.get_y() + bar.get_height() / 2,
        format_dollars(bar.get_width()),
        ha="left",
        va="center",
        fontsize=10,
        color="black"
    )

# Plot for Top Brands

plt.subplot(1, 2, 2)

ax2 = sns.barplot(
    y=top_brands.index.astype(str),
    x=top_brands.values,
    palette="Reds_r"
)

plt.title("Top 10 Brands by Sales")

for bar in ax2.patches:
    ax2.text(
        bar.get_width() + (bar.get_width() * 0.02),
        bar.get_y() + bar.get_height() / 2,
        format_dollars(bar.get_width()),
        ha="left",
        va="center",
        fontsize=10,
        color="black"
    )

plt.tight_layout()
plt.show()

'''
Q3. Which vendors contribute the most to total purchase dollars?
'''

vendor_performance = df.groupby("VendorName").agg({
    "TotalPurchaseDollars": "sum",
    "GrossProfit": "sum",
    "TotalSalesDollars": "sum"
}).reset_index()

# Calculate total purchase dollars

total_purchase_dollars = vendor_performance["TotalPurchaseDollars"].sum()

# Calculate purchase contribution percentage

vendor_performance["PurchaseContribution%"] = (
    vendor_performance["TotalPurchaseDollars"]
    / total_purchase_dollars
    * 100
)

# Sort vendors by purchase contribution

vendor_performance = (
    vendor_performance
    .sort_values("PurchaseContribution%", ascending=False)
    .reset_index(drop=True)
)

# Calculate cumulative contribution

vendor_performance["CumulativeContribution%"] = (
    vendor_performance["PurchaseContribution%"].cumsum()
)

# Select Top 10 Vendors

top_vendors_purchase = vendor_performance.head(10).copy()

print("\nTOP 10 VENDORS BY PURCHASE CONTRIBUTION")

display(
    top_vendors_purchase[
        [
            "VendorName",
            "TotalPurchaseDollars",
            "GrossProfit",
            "TotalSalesDollars",
            "PurchaseContribution%",
            "CumulativeContribution%"
        ]
    ]
)

# Pareto Chart

fig, ax1 = plt.subplots(figsize=(12, 6))

# Bar plot for Purchase Contribution %

bars = ax1.bar(
    top_vendors_purchase["VendorName"],
    top_vendors_purchase["PurchaseContribution%"],
    color="steelblue"
)

# Add percentage labels

for bar, value in zip(
    bars,
    top_vendors_purchase["PurchaseContribution%"]
):
    ax1.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 0.2,
        f"{value:.1f}%",
        ha="center",
        va="bottom",
        fontsize=9
    )

ax1.set_ylabel("Purchase Contribution %", color="blue")
ax1.set_xlabel("Vendors")
ax1.set_title("Pareto Chart: Vendor Contribution to Total Purchases")
ax1.tick_params(axis="x", rotation=90)

# Line for Cumulative Contribution

ax2 = ax1.twinx()

ax2.plot(
    top_vendors_purchase["VendorName"],
    top_vendors_purchase["CumulativeContribution%"],
    color="red",
    marker="o",
    linestyle="dashed",
    linewidth=2,
    label="Cumulative Contribution"
)

ax2.set_ylabel("Cumulative Contribution %", color="red")
ax2.set_ylim(0, 105)

# 80% reference line

ax2.axhline(
    y=80,
    color="gray",
    linestyle="dashed",
    alpha=0.7,
    label="80% Reference"
)

ax2.legend(loc="upper left")

plt.tight_layout()
plt.show()

'''
Q4. How much of total procurement is dependent on the
top vendors?
'''

top_10_purchase_contribution = top_vendors_purchase["PurchaseContribution%"].sum()

print(
    f"\nTotal Purchase Contribution of the Top 10 Vendors is "
    f"{top_10_purchase_contribution:.2f}%"
)

# Calculate remaining contribution

remaining_contribution = 100 - top_10_purchase_contribution

print(
    f"Purchase Contribution of Other Vendors is "
    f"{remaining_contribution:.2f}%"
)

# Prepare Data for Donut Chart

vendors = [
    "Top 10 Vendors",
    "Other Vendors"
]

purchase_contributions = [
    top_10_purchase_contribution,
    remaining_contribution
]

# Donut Chart

fig, ax = plt.subplots(figsize=(8, 8))

wedges, texts, autotexts = ax.pie(
    purchase_contributions,
    labels=vendors,
    autopct="%1.1f%%",
    startangle=140,
    pctdistance=0.80,
    colors=["#4C78A8", "#D9D9D9"],
    wedgeprops=dict(width=0.35)
)

# Format percentage labels

for autotext in autotexts:
    autotext.set_fontsize(12)
    autotext.set_fontweight("bold")

# Add Total Contribution annotation in the center

ax.text(
    0,
    0,
    f"{top_10_purchase_contribution:.1f}%\nTop 10 Vendors",
    ha="center",
    va="center",
    fontsize=14,
    fontweight="bold"
)

plt.title("Top 10 Vendor's Purchase Contribution (%)", fontsize=14)
plt.tight_layout()
plt.show()

'''
Q5. Does purchasing in bulk reduce the unit price, and what is the optimal
purchase volume for cost savings?
'''

df["UnitPurchasePrice"] = np.where(
    df["TotalPurchaseQuantity"] > 0,
    df["TotalPurchaseDollars"] / df["TotalPurchaseQuantity"],
    np.nan
)

df["OrderSize"] = pd.qcut(
    df["TotalPurchaseQuantity"],
    q=3,
    labels=["Small", "Medium", "Large"],
    duplicates="drop"
)

print("\nPurchase Quantity by Order Size:")
print(df[["OrderSize", "TotalPurchaseQuantity"]].head())

order_price_summary = (
    df.groupby("OrderSize", observed=True)["UnitPurchasePrice"]
    .mean()
    .reindex(["Small", "Medium", "Large"])
)

print("\nAverage Unit Purchase Price by Order Size:")
print(order_price_summary)

if pd.notna(order_price_summary["Small"]) and pd.notna(order_price_summary["Large"]):
    price_reduction = (
        (order_price_summary["Small"] - order_price_summary["Large"])
        / order_price_summary["Small"]
        * 100
    )
    print(f"\nUnit Price Reduction from Small to Large Orders: {price_reduction:.2f}%")

optimal_order_size = order_price_summary.idxmin()
optimal_unit_price = order_price_summary.min()

print(
    f"Optimal Order Size for Cost Savings: {optimal_order_size} "
    f"with Average Unit Purchase Price of ${optimal_unit_price:.2f}"
)

plt.figure(figsize=(10, 6))

sns.boxplot(
    data=df,
    x="OrderSize",
    y="UnitPurchasePrice",
    hue="OrderSize",
    palette="Set2",
    legend=False
)

plt.title("Impact of Bulk Purchase Price")
plt.xlabel("Order Size")
plt.ylabel("Unit Purchase Price")
plt.tight_layout()
plt.show()

'''
- Vendors buying in bulk generally get a lower unit purchase price.
- The Large order category represents the lowest average unit purchase price.
- This suggests that larger purchase quantities may provide cost savings,
  provided that inventory can be managed efficiently.
'''

'''
Q6. Which Vendors have low inventory turnover, indicating excess stock
and slow-moving products?
'''

low_turnover_vendors = (
    df[df["StockTurnover"] < 1]
    .groupby("VendorName")["StockTurnover"]
    .mean()
    .sort_values(ascending=True)
    .head(10)
)

print("\nTOP 10 VENDORS WITH LOW INVENTORY TURNOVER:")
print(low_turnover_vendors)

'''
Q7. How much capital is locked in unsold inventory per vendor, and which
vendor contributes the most of it?
'''

df["UnsoldInventoryQuantity"] = (
    df["TotalPurchaseQuantity"] - df["TotalSalesQuantity"]
)

df["UnsoldInventoryValue"] = (
    df["UnsoldInventoryQuantity"] * df["PurchasePrice"]
)

total_unsold_capital = df["UnsoldInventoryValue"].sum()

print(
    "\nTotal Unsold Capital:",
    format_dollars(total_unsold_capital)
)

# Aggregate Capital Locked per Vendor

inventory_value_per_vendor = (
    df.groupby("VendorName")["UnsoldInventoryValue"]
    .sum()
    .reset_index()
)

# Sort Vendors with the Highest Locked Capital

inventory_value_per_vendor = (
    inventory_value_per_vendor
    .sort_values(
        by="UnsoldInventoryValue",
        ascending=False
    )
    .reset_index(drop=True)
)

print("\nTOP 10 VENDORS BY UNSOLD INVENTORY CAPITAL:")

display(
    inventory_value_per_vendor.head(10).assign(
        UnsoldInventoryValue=lambda x:
        x["UnsoldInventoryValue"].apply(format_dollars)
    )
)

'''
Q8. What are the 95% confidence intervals for profit margins of
top-performing and low-performing vendors?
'''

# Aggregate performance at Vendor level

vendor_analysis = (
    df.groupby("VendorName")
    .agg(
        TotalSalesDollars=("TotalSalesDollars", "sum"),
        TotalGrossProfit=("GrossProfit", "sum")
    )
    .reset_index()
)

# Calculate Vendor Level Profit Margin

vendor_analysis["ProfitMargin"] = (
    vendor_analysis["TotalGrossProfit"]
    / vendor_analysis["TotalSalesDollars"]
    * 100
)

# Define top and low performing vendor thresholds

top_threshold = vendor_analysis["TotalSalesDollars"].quantile(0.75)
low_threshold = vendor_analysis["TotalSalesDollars"].quantile(0.25)

# Select Top Performing Vendors

top_vendors_margin = (
    vendor_analysis[
        vendor_analysis["TotalSalesDollars"] >= top_threshold
    ]["ProfitMargin"]
    .dropna()
)

# Select Low Performing Vendors

low_vendors_margin = (
    vendor_analysis[
        vendor_analysis["TotalSalesDollars"] <= low_threshold
    ]["ProfitMargin"]
    .dropna()
)

print("\nTop Performing Vendors Profit Margins:")
print(top_vendors_margin)

print("\nLow Performing Vendors Profit Margins:")
print(low_vendors_margin)

# Confidence Interval Function

def confidence_interval(data, confidence=0.95):
    data = data.dropna()
    if len(data) < 2:
        return np.mean(data), np.nan, np.nan
    mean_val = np.mean(data)
    std_err = np.std(data, ddof=1) / np.sqrt(len(data))
    t_critical = stats.t.ppf((1 + confidence) / 2, df=len(data) - 1)
    margin_of_error = t_critical * std_err
    return mean_val, mean_val - margin_of_error, mean_val + margin_of_error

# Calculate Confidence Intervals

top_mean, top_lower, top_upper = confidence_interval(top_vendors_margin)
low_mean, low_lower, low_upper = confidence_interval(low_vendors_margin)

print(
    f"\nTop Vendors 95% CI: ({top_lower:.2f}, {top_upper:.2f}), "
    f"Mean: {top_mean:.2f}%"
)

print(
    f"Low Vendors 95% CI: ({low_lower:.2f}, {low_upper:.2f}), "
    f"Mean: {low_mean:.2f}%"
)

# Final Visualization

plt.figure(figsize=(12, 6))

# Top Vendors Plot

sns.histplot(
    top_vendors_margin,
    kde=True,
    color="blue",
    bins=15,
    alpha=0.5,
    label="Top Vendors"
)

plt.axvline(
    top_lower,
    color="blue",
    linestyle="--",
    label=f"Top Lower: {top_lower:.2f}%"
)

plt.axvline(
    top_upper,
    color="blue",
    linestyle="--",
    label=f"Top Upper: {top_upper:.2f}%"
)

plt.axvline(
    top_mean,
    color="blue",
    linestyle="-",
    label=f"Top Mean: {top_mean:.2f}%"
)

# Low Vendors Plot

sns.histplot(
    low_vendors_margin,
    kde=True,
    color="red",
    bins=15,
    alpha=0.5,
    label="Low Vendors"
)

plt.axvline(
    low_lower,
    color="red",
    linestyle="--",
    label=f"Low Lower: {low_lower:.2f}%"
)

plt.axvline(
    low_upper,
    color="red",
    linestyle="--",
    label=f"Low Upper: {low_upper:.2f}%"
)

plt.axvline(
    low_mean,
    color="red",
    linestyle="-",
    label=f"Low Mean: {low_mean:.2f}%"
)

# Finalize Plot

plt.title("95% Confidence Interval Comparison: Top Vs Low Vendors")
plt.xlabel("Profit Margin (%)")
plt.ylabel("Frequency")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

'''
- The confidence interval for low-performing vendors can be compared with
  the confidence interval for top-performing vendors to understand the
  difference in their average profit margins.
- If the intervals are clearly separated, this provides evidence that
  low-performing vendors may have higher profit margins than top-performing
  vendors.
- For High-Performing Vendors: If they aim to improve profitability, they
  could explore selective price adjustments, cost optimization, or
  bundling strategies.
- For Low-Performing Vendors: Despite higher margins, their low sales volume
  might indicate a need for better marketing, competitive pricing, or
  improved distribution strategies.
'''

'''
Q9. Is there a Significant Difference in Profit Margins between
Top-Performing and Low-Performing Vendors?
'''

# Hypothesis Testing

# H0: There is no significant difference in profit margins between
#     top-performing and low-performing vendors.
#
# H1: There is a significant difference in profit margins between
#     top-performing and low-performing vendors.

top_threshold = vendor_analysis["TotalSalesDollars"].quantile(0.75)
low_threshold = vendor_analysis["TotalSalesDollars"].quantile(0.25)

# Select Top Performing Vendors

top_vendors = (
    vendor_analysis[
        vendor_analysis["TotalSalesDollars"] >= top_threshold
    ]["ProfitMargin"]
    .dropna()
)

# Select Low Performing Vendors

low_vendors = (
    vendor_analysis[
        vendor_analysis["TotalSalesDollars"] <= low_threshold
    ]["ProfitMargin"]
    .dropna()
)

print("\nTop Performing Vendor Profit Margins:")
print(top_vendors)

print("\nLow Performing Vendor Profit Margins:")
print(low_vendors)

print(f"\nNumber of Top Performing Vendors: {len(top_vendors)}")
print(f"Number of Low Performing Vendors: {len(low_vendors)}")

# Two Sample Test

if len(top_vendors) >= 2 and len(low_vendors) >= 2:
    t_stat, p_value = ttest_ind(
        top_vendors,
        low_vendors,
        equal_var=False
    )

    print("\nHYPOTHESIS TEST RESULT")
    print(f"T-Statistics: {t_stat:.4f}")
    print(f"P-Value: {p_value:.6f}")

    # Result

    alpha = 0.05

    if p_value < alpha:
        print(
            "Reject H0: There is a significant difference in profit margins "
            "between top-performing and low-performing vendors."
        )
    else:
        print(
            "Fail to Reject H0: There is no significant difference in profit "
            "margins between top-performing and low-performing vendors."
        )
else:
    print(
        "\nNot enough vendors available in one or both groups to perform "
        "the independent two-sample t-test."
    )
print("\nAnalysis Completed Successfully.")