# IDX Exchange Internship

## Overview

IDX Exchange is a technology company operating at the intersection of real estate, data science, and AI. They build machine learning models for property valuation, natural language property search platforms, and market and competitive analytics dashboards that help real estate professionals make better decisions.

---

## Week 1 Tasks

* Generated the **March 2026 CRMLS raw CSV files** using the provided extraction scripts
* Organized all raw monthly files from **January 2024 through March 2026** into separate folders:
  * `raw/listed`
  * `raw/sold`
* Created **two separate Python preparation pipelines**:
  * `week1_listed_prep.py`
  * `week1_sold_prep.py`
* Appended all monthly CSV files into one master dataset per transaction type
* Removed duplicate rows and completely blank rows
* Filtered the data to **Residential properties only**
* Exported final **clean combined CSV outputs** ready for Tableau dashboard development

---

## Output Files

The Week 1 preparation scripts generate:

* `listed_combined_residential.csv`
* `sold_combined_residential.csv`

---

## Week 2 Tasks

* Performed **dataset structuring and validation** on the combined Residential listing and sold datasets
* Reviewed dataset **shape, column names, and data types**
* Confirmed **Residential-only PropertyType values**
* Generated **missing value summary reports** for all columns
* Flagged columns with **more than 90% missing values**
* Created **numeric distribution summaries** for key market fields:
  * `ClosePrice`
  * `ListPrice`
  * `OriginalListPrice`
  * `LivingArea`
  * `LotSizeAcres`
  * `BedroomsTotal`
  * `BathroomsTotalInteger`
  * `DaysOnMarket`
  * `YearBuilt`
* Built **separate validation pipelines**:
  * `week2_listed_validation.py`
  * `week2_sold_validation.py`
* Built a **numeric distribution EDA workflow**:
  * `week2_numeric_distribution_graphs.py`
* Used **histograms, boxplots, and percentile summaries** to identify extreme outliers for later Week 7 filtering

---

## Output Files

The Week 2 validation and EDA scripts generate:

* `listed_missing_value_report.csv`
* `listed_high_missing_columns.csv`
* `listed_numeric_distribution_summary.csv`
* `sold_missing_value_report.csv`
* `sold_high_missing_columns.csv`
* `sold_numeric_distribution_summary.csv`

---

