# 📦 Vendor Performance & Procurement SLA Analytics

[![SQL](https://img.shields.io/badge/SQL-Advanced%20Queries-CC292B?style=flat-square&logo=postgresql)](#)
[![Power BI](https://img.shields.io/badge/Power_BI-Interactive_Dashboard-F2C811?style=flat-square&logo=powerbi)](#)
[![Excel](https://img.shields.io/badge/Excel-Data_Modeling-217346?style=flat-square&logo=microsoftexcel)](#)
[![Status](https://img.shields.io/badge/Status-Completed-success?style=flat-square)](#)

## 📌 Executive Summary & Business Problem

Supply chain disruptions, supplier delays, and non-conforming goods directly inflate carrying costs, interrupt operations, and erode gross margins.

This project evaluates supplier delivery timeliness, procurement lead times, defect rates, and unit pricing compliance across multiple vendors. The primary objective is to identify SLA compliance deficits, quantify financial and operational risk exposure, and provide actionable recommendations to optimize procurement spend and supplier allocations.

## 🛠️ Data Pipeline & Technical Architecture

- **Data Modeling & Schema Design:** Built a normalized Star Schema connecting Purchase Orders, Vendor Master records, Delivery Logs, and Quality Defect tables using SQL and Power BI.
- **KPI & Metric Engineering:** Formatted robust DAX measures and SQL transformations to calculate core operational metrics:
  - On-Time In-Full (OTIF) Rate (%)
  - Defect-Free Delivery Rate (%)
  - Average Lead Time (Days) & Delivery Variance
  - Spend Concentration Index (%)
- **ETL & Data Hygiene:** Cleaned missing delivery timestamps, standardized unit pricing variations, and eliminated duplicate vendor records via Power Query and SQL.

## 📊 Key Business Insights

- **Supplier Concentration:** Top 3 suppliers accounted for **64% of total procurement expenditure**, presenting high supply-chain dependency risk.
- **OTIF Compliance Deficit:** Two primary suppliers failed minimum SLA targets, averaging a **28% late shipment rate** across peak manufacturing quarters.
- **Defect Cost Burden:** Returned lots from underperforming suppliers resulted in an estimated **8.5% loss in operational throughput**.
- **Lead-Time Volatility:** Unplanned lead-time variance spiked by **1.6x** among secondary tier vendors without automated PO confirmation protocols.

## 💡 Strategic Business Recommendations

- **Tiered Vendor Scorecards:** Implement quarterly contract reviews tying repeat order allocations to vendor OTIF performance thresholds (>92%).
- **Dual-Sourcing Strategy:** Introduce secondary regional suppliers for critical product lines to mitigate high-dependency single-supplier bottlenecks.
- **Automated SLA Penalty Tracking:** Automate chargeback calculations for deliveries delayed beyond agreed contractual grace periods (>48 hours delay).
- **Early Risk Escalation:** Establish threshold alerts within procurement workflows when supplier lead times trend upwards for two consecutive billing cycles.

## 🚀 How to Explore This Project

1. **Review SQL Scripts:** Open `/sql` to inspect data cleaning, transformation, and SLA aggregation queries.
2. **Open Power BI Dashboard:** Download the `.pbix` file located in `/dashboards` to interact with slicers, vendor scorecards, and spend analytics.
3. **Review Data Dictionary:** Inspect `/data` for table schemas, field definitions, and transactional sample records.

## 👤 Author

**Prashant Marathe**
- LinkedIn: [linkedin.com/in/prashantmarathe17](https://www.linkedin.com/in/prashantmarathe17)[cite: 1]
- Portfolio Website: [prashant-marathe.framer.website](https://prashant-marathe.framer.website/)[cite: 1]
- Email: [p04747391@gmail.com](mailto:p04747391@gmail.com)[cite: 1]
- Location: Pune, Maharashtra, India[cite: 1]
