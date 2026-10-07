# 📦 Vendor Procurement & SLA Analytics

> **End-to-end procurement analytics project using SQL, Python, Power BI, DAX, and data modeling to evaluate vendor performance, delivery reliability, procurement spend, and operational risk.**

## 📌 Business Problem

Supplier delays, inconsistent delivery performance, quality issues, and high supplier concentration can increase procurement costs and disrupt operations.

This project analyzes vendor-level procurement and delivery data to answer key business questions:

* Which suppliers contribute the most procurement spend?
* Which vendors consistently meet delivery SLAs?
* Where are late deliveries and quality issues concentrated?
* How volatile are supplier lead times?
* Which vendors require closer monitoring or corrective action?
* How can procurement teams reduce supplier dependency and operational risk?

---

## 🎯 Project Objectives

The analysis focuses on four major areas:

1. **Vendor Performance** — measure delivery reliability and SLA compliance.
2. **Procurement Analytics** — analyze supplier spend and concentration.
3. **Operational Risk** — identify delivery delays, defects, and lead-time volatility.
4. **Business Recommendations** — translate analytical findings into procurement actions.

---

## 🛠️ Tech Stack

| Area                  | Tools / Technologies |
| --------------------- | -------------------- |
| Data Analysis         | Python, Pandas       |
| Database / SQL        | SQL                  |
| Data Transformation   | Power Query          |
| Business Intelligence | Power BI             |
| Calculations          | DAX                  |
| Data Modeling         | Star Schema          |
| Visualization         | Power BI             |
| Reporting             | Power BI Dashboard   |

---

## 🔄 End-to-End Analytics Workflow

```text
Raw Procurement Data
        ↓
Data Cleaning & Validation
        ↓
Data Transformation
        ↓
SQL Analysis
        ↓
KPI & Metric Engineering
        ↓
Data Modeling
        ↓
Power BI Dashboard
        ↓
Business Insights
        ↓
Procurement Recommendations
```

---

## 📊 Key KPIs

The analysis focuses on operational and procurement KPIs including:

* **OTIF Rate (%)**
* **Defect-Free Delivery Rate (%)**
* **Average Lead Time**
* **Lead-Time Variance**
* **Procurement Spend**
* **Supplier Spend Concentration**
* **Delivery Delay Rate**
* **Operational Throughput Impact**

These metrics provide a consolidated view of supplier reliability, procurement exposure, and operational risk.

---

## 🔍 Key Business Insights

### 1. Supplier Concentration Risk

The **top 3 suppliers account for 64% of total procurement expenditure**, creating significant dependency on a small supplier group.

**Business implication:**
A disruption at one major supplier could have a disproportionate impact on procurement continuity.

### 2. OTIF / SLA Performance Gap

Two major suppliers recorded an average **28% late-shipment rate during peak manufacturing periods**.

**Business implication:**
Repeated SLA failures can affect production planning, inventory availability, and downstream operations.

### 3. Defect-Related Operational Impact

Underperforming suppliers contributed to an estimated **8.5% operational throughput loss** through returned or defective lots.

**Business implication:**
Supplier quality should be evaluated alongside price and delivery performance.

### 4. Lead-Time Volatility

Secondary-tier vendors experienced approximately **1.6× higher lead-time variance** when automated purchase-order confirmation processes were unavailable.

**Business implication:**
Lead-time monitoring can help procurement teams identify emerging delivery risks earlier.

---

## 💡 Business Recommendations

### 🔹 Implement Vendor Scorecards

Create quarterly supplier scorecards combining:

* OTIF performance
* Defect rate
* Lead-time reliability
* Procurement spend
* SLA compliance

Use vendor performance thresholds to guide future order allocation.

### 🔹 Reduce Supplier Concentration

Introduce qualified secondary suppliers for critical product categories to reduce dependency on a small number of vendors.

### 🔹 Automate SLA Monitoring

Track contractual delivery commitments and automatically flag shipments exceeding agreed grace periods.

### 🔹 Establish Early-Warning Indicators

Monitor consecutive increases in supplier lead times and trigger procurement reviews before delays become operational bottlenecks.

---

## 📈 Power BI Dashboard

The Power BI dashboard provides an interactive view of:

* Vendor performance
* Procurement spend
* SLA / OTIF performance
* Lead-time analysis
* Defect-related performance
* Supplier comparison
* Procurement risk indicators

**Dashboard file:** `Vendor_Analysis.pbix`

---

## 🧮 Analytical Approach

### Data Preparation

* Handled missing and inconsistent delivery information.
* Standardized supplier and pricing data.
* Removed duplicate vendor records.
* Prepared analytical datasets for SQL and Power BI.

### SQL Analysis

SQL was used to transform and analyze procurement data, including:

* Vendor-level aggregations
* Delivery performance analysis
* SLA calculations
* Spend analysis
* Supplier comparisons

### Power BI & DAX

Power BI was used to create an interactive analytical layer with:

* KPI cards
* Vendor-level analysis
* Spend analysis
* SLA monitoring
* Performance comparisons
* Business-focused visualizations

---

## 📂 Project Structure

```text
vendor-procurement-sla-analysis/
│
├── data/
│   ├── begin_inventory.csv
│   ├── end_inventory.csv
│   ├── purchase_prices.csv
│   └── vendor_sales_summary.csv
│
├── python/
│   ├── Exploratory_Data_Analysis.py
│   ├── Vendor_Analysis.py
│   ├── Vendor_Performance_Analysis.py
│   └── get_vendor_summary.py
│
├── powerbi/
│   └── Vendor_Analysis.pbix
│
├── reports/
│   └── Vendor_Performance_Analysis_Report.pdf
│
├── screenshots/
│   └── dashboard screenshots
│
└── README.md
```

> **Note:** Create these folders and move the existing files into them before using this structure. Do not leave the README claiming folders that do not exist.

---

## 🎓 Skills Demonstrated

* SQL Analytics
* Python Data Analysis
* Pandas
* Data Cleaning
* Exploratory Data Analysis
* Power BI
* DAX
* Power Query
* KPI Development
* Data Modeling
* Procurement Analytics
* Supply Chain Analytics
* Vendor Performance Analysis
* SLA / OTIF Analysis
* Business Intelligence
* Data-Driven Decision Making

---

## 🚀 Business Value

This project demonstrates how raw procurement data can be transformed into a **business intelligence solution** that helps procurement and operations teams:

* Identify underperforming suppliers
* Monitor SLA compliance
* Understand procurement concentration
* Detect delivery risks
* Evaluate supplier reliability
* Support supplier allocation decisions
* Improve operational visibility

---

## 👤 About Me

**Prashant Marathe**
B.Tech — Artificial Intelligence & Data Science

**Target Roles:** Data Analyst | BI Analyst | Business Analyst

📍 Pune, Maharashtra, India

* [LinkedIn](https://www.linkedin.com/in/prashantmarathe17?utm_source=chatgpt.com)
* [Portfolio](https://prashant-marathe.framer.website/?utm_source=chatgpt.com)
* [GitHub](https://github.com/MarathePrashant?utm_source=chatgpt.com)
* Email: [p04747391@gmail.com](mailto:p04747391@gmail.com)
