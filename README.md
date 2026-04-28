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

## Week 3 Tasks

* Integrated external economic data by fetching the **30-year fixed mortgage rate (MORTGAGE30US)** from FRED
* Converted weekly mortgage rate data into **monthly averages** for time-based analysis
* Created a **year_month key** to align mortgage data with MLS datasets
* Merged mortgage rate data onto:
  * Sold dataset using `CloseDate`
  * Listed dataset using `ListingContractDate`
* Validated the merge by confirming **no missing mortgage rate values**
* Previewed merged data to ensure correct alignment of dates and rates
* Saved enriched datasets for downstream analysis and Tableau integration

---

## Output Files

The Week 3 enrichment pipeline generates:

* `sold_combined_residential_with_mortgage.csv`
* `listed_combined_residential_with_mortgage.csv`

---

## Week 4–5 Tasks

* Built a **continuous, cumulative data pipeline** by consolidating all weekly scripts into:
  * `sold.py`
  * `listings.py`
* Converted key date fields into proper datetime format for time-based analysis:
  * `CloseDate`
  * `PurchaseContractDate`
  * `ListingContractDate`
  * `ContractStatusChangeDate`
* Removed redundant and duplicate columns (e.g., `.1` columns created during data joins)
* Converted key numeric fields to appropriate data types to ensure analytical consistency:
  * Pricing, property attributes, and mortgage rate fields
* Identified and **flagged invalid numeric values** instead of removing them:
  * Negative or zero values in price, living area, days on market, bedrooms, and bathrooms
* Created **data quality flag columns** to preserve transparency and support downstream filtering
* Implemented **date consistency checks**:
  * Listings occurring after close dates
  * Purchase contract dates occurring after close dates
  * Negative timeline inconsistencies between listing and purchase events
* Built **geographic data quality checks**:
  * Missing coordinates
  * Zero-value coordinates
  * Positive longitude values (invalid for U.S. data)
  * Out-of-bounds latitude/longitude values outside expected California ranges
* Retained high-missing columns to preserve flexibility for stakeholder analysis rather than prematurely dropping data
* Generated **summary outputs** including:
  * Before vs after row and column counts
  * Invalid numeric value counts
  * Date consistency flag counts
  * Geographic data quality summaries
* Produced **final cleaned, analysis-ready datasets** for Tableau dashboard ingestion

---

## Output Files

The Week 4–5 data cleaning pipeline generates:

* `sold_cleaned_residential.csv`
* `listed_cleaned_residential.csv`