# 📦 Vendor Performance & Procurement SLA Analytics

[![SQL](https://img.shields.io/badge/SQL-Advanced%20Queries-CC292B?style=flat-square&logo=postgresql)](#)
[![Power BI](https://img.shields.io/badge/Power_BI-Interactive_Dashboard-F2C811?style=flat-square&logo=powerbi)](#)
[![Excel](https://img.shields.io/badge/Excel-Data_Modeling-217346?style=flat-square&logo=microsoftexcel)](#)

## 📌 Business Problem
Supply chain disruptions and supplier delays significantly inflate inventory carrying costs and reduce customer fulfillment rates. This project evaluates supplier lead times, delivery reliability (On-Time In-Full / OTIF), defect rates, and unit pricing variance across multiple vendors to identify SLA compliance gaps and optimize procurement spend.

---

## 🛠️ Data Pipeline & Architecture
* **Data Modeling:** Built a normalized Star Schema linking procurement purchase orders, vendor master tables, and defect logs using Power BI and SQL.
* **KPI Engineering:** Formatted DAX measures to calculate `On-Time Delivery Rate (%)`, `Defect Free Rate (%)`, `Vendor Spend Share`, and `Procurement Lead Time Variance`.
* **Dashboard Design:** Designed an interactive executive dashboard featuring dynamic vendor scorecards, delivery risk matrices, and spend concentration breakdowns.

```text
├── data/               # Procurement purchase orders, vendor master, inspection records
├── dashboards/         # Power BI (.pbix) files and high-res report screenshots
├── sql/                # SQL scripts for data cleaning, aggregation, and SLA calculations
└── README.md
