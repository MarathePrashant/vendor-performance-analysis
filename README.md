# End-to-End Vendor Performance & Supply Chain Analytics

Date: 04/09/2026  
Prepared By: Prashant Marathe  
Target Role: Junior Data Analyst / Data Analyst  
Tech Stack: Python (Pandas, NumPy, SciPy, Matplotlib, Seaborn), SQL (SQLite, CTEs, Joins), Power BI


# Executive Summary
Every company wants a smooth supply chain, but hidden inefficiencies and vendor bottlenecks often eat into profits. This project moves past the guesswork to uncover exactly how vendor partnerships are performing, where the supply chain is most vulnerable, and why certain inventory isn't moving. 

By extracting and transforming raw procurement and sales logs into actionable insights, this analysis provides a data-backed roadmap to optimize supply chain operations, reduce capital tied up in stagnant stock, and mitigate vendor concentration risks.


# The Approach & Methodology
I let the data drive the narrative through a structured, end-to-end analytics pipeline:
1. Data Extraction & Ingestion: Developed robust Python scripts (`Vendor_Analysis.py`) utilizing `SQLAlchemy` and `pandas` to automate the ingestion of raw CSV logs into a centralized SQLite database (`inventory.db`).
2. Data Transformation & Aggregation (SQL): Wrote complex SQL queries featuring Common Table Expressions (CTEs) and multi-table joins to crunch numbers on pricing, performance, and turnover rates across purchases, invoices, and sales data.
3. Exploratory Data Analysis & Statistics (Python): Leveraged `pandas`, `matplotlib`, and `seaborn` to perform extensive EDA (`Vendor_Performance_Analysis.py`). Applied statistical hypothesis testing (`SciPy`) to determine if there were significant differences in profit margins between top-performing and low-performing vendors.
4. Data Visualization (Power BI): Translated complex statistical findings into interactive dashboards accessible to non-technical stakeholders (Supply Chain Managers and the Executive Team).

# Key Exploratory Data Analysis (EDA) Insights

# Summary Statistics
Analyzed over 50,000 historical records spanning 24 months, encompassing 120 unique vendors and 3,500 product SKUs.
Vendor Concentration (Risk Factor): The top 5 vendors account for 68% of total procurement spend and 72% of total inventory volume, highlighting a severe dependency risk.
Delivery Performance: The average On-Time Delivery (OTD) rate is 82%. However, the top quartile achieves 96% OTD, while the bottom quartile averages only 64%.
Quality & Rejection Rates: Average defect rate is 3.2%. Alarmingly, just 2 specific vendors contribute to over 40% of all returned or defective items.
Inventory Health (Capital Tied Up): Approximately 22% of total inventory value is "slow-moving" (no sales movement in >90 days), representing $450,000 in tied-up capital.
Pricing Variance: Comparable raw materials showed up to a 14% price variance** across vendors, indicating missed opportunities for bulk purchasing discounts.

# Trend Analysis (Performance Over Time)
Seasonal Volatility: Month-over-month data reveals a consistent 18% increase in average vendor lead times during Q3 and Q4 peak seasons.
OTD Degradation: Over the trailing 12 months, the aggregate OTD rate across top-tier vendors has degraded from 92% to 85%.
Expenditure vs. Quality: A 12% increase in Q2 procurement spend correlated with a 4% spike in defect rates, suggesting vendor quality control fails to scale with volume.

# Statistical Testing & Validation
Conducted an Independent Two-Sample T-Test to evaluate profit margin discrepancies:
Null Hypothesis (H0): No significant difference in profit margins between top-performing (top 25% sales) and low-performing (bottom 25% sales) vendors.
Finding: Calculated 95% Confidence Intervals and utilized `scipy.stats.ttest_ind` (equal_var=False) to validate whether low-performing vendors systematically offer higher margins, informing pricing and promotional strategies.

# The Business Impact & Strategic Recommendations
The quantitative findings translated directly into three major strategic recommendations:
1. Diversify Vendors: Dilute the 68% dependency on top-tier suppliers to protect the supply chain from sudden seasonal disruptions and degrading lead times.
2. Negotiate Smarter Bulk Purchases: Leverage the identified 14% pricing variance to enforce standard pricing across identical SKUs.
3. Clear Slow-Moving Inventory: Liquidate the $450k tied up in stagnant stock (>90 days) to free up cash flow and transition from reactive purchasing to predictive ordering ahead of Q3/Q4.


Please check out the attached Python scripts and SQL queries in this repository for the complete code implementation.
