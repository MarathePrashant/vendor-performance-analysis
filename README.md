# 📦 Vendor Performance & Procurement SLA Analytics

[![SQL](https://img.shields.io/badge/SQL-Advanced%20Queries-CC292B?style=flat-square&logo=postgresql)](#)
[![Power BI](https://img.shields.io/badge/Power_BI-Interactive_Dashboard-F2C811?style=flat-square&logo=powerbi)](#)
[![Excel](https://img.shields.io/badge/Excel-Data_Modeling-217346?style=flat-square&logo=microsoftexcel)](#)
[![Status](https://img.shields.io/badge/Status-Completed-success?style=flat-square)](#)

## 📌 Executive Summary & Business Problem

Supply chain disruptions, supplier delays, and non-conforming goods directly inflate carrying costs, interrupt operations, and erode gross margins.

This project evaluates supplier delivery timeliness, procurement lead times, defect rates, and unit pricing compliance across multiple vendors. The primary objective is to identify SLA compliance deficits, quantify financial and operational risk exposure, and provide actionable recommendations to optimize procurement spend and supplier allocations.

## 🖥️ Executive Dashboard Preview

![Vendor Performance Dashboard Preview](assets/dashboard_preview.png)

## 🛠️ Data Pipeline & Technical Architecture

- **Data Modeling & Schema Design:** Built a normalized Star Schema connecting Purchase Orders, Vendor Master records, Delivery Logs, and Quality Defect tables using SQL and Power BI.
- **KPI & Metric Engineering:** Formatted robust DAX measures and SQL transformations to calculate core operational metrics:
  - On-Time In-Full (OTIF) Rate (%)
  - Defect-Free Delivery Rate (%)
  - Average Lead Time (Days) & Delivery Variance
  - Spend Concentration Index (%)
- **ETL & Data Hygiene:** Cleaned missing delivery timestamps, standardized unit pricing variations, and eliminated duplicate vendor records via Power Query and SQL.

```text
├── assets/             # Executive dashboard previews and report visuals
├── data/               # Purchase orders, vendor master, and defect datasets
├── dashboards/         # Power BI report files (.pbix)
├── sql/                # SQL queries for ETL, KPIs, and aggregations
└── README.md           # Business case study and project overview
