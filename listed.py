import pandas as pd
from pathlib import Path


# =========================
# Week 1: Aggregation + Residential Filter
# =========================


listed_folder = Path("raw/listed")
listed_files = sorted(listed_folder.glob("CRMLSListing*.csv"))

dfs = []

# row count for each individual file before append
print("Row count for each listed file before append:")
for file in listed_files:
    df = pd.read_csv(file, low_memory=False)
    print(f"{file.name}: {len(df)} rows")
    dfs.append(df)

# combine all files
listed_all = pd.concat(dfs, ignore_index=True)

# row count of the combined/appended dataset after concatenation
print("\nCombined listed dataset row count after concatenation:")
print(len(listed_all))

# remove duplicate rows
listed_all = listed_all.drop_duplicates()

# remove completely blank rows
listed_all = listed_all.dropna(how="all")

# frequency table of PropertyType before filtering
print("\nPropertyType frequency table before Residential filter:")
print(listed_all["PropertyType"].value_counts(dropna=False))

# keep only residential
listed_residential = listed_all[
    listed_all["PropertyType"] == "Residential"
].copy()

# row count after applying PropertyType == 'Residential'
print("\nListed row count after applying PropertyType == 'Residential':")
print(len(listed_residential))

# frequency table of PropertyType after filtering
print("\nPropertyType frequency table after Residential filter:")
print(listed_residential["PropertyType"].value_counts(dropna=False))

# save clean CSV
listed_residential.to_csv(
    "listed_combined_residential.csv",
    index=False
)

print("\nFinal listed rows saved:", len(listed_residential))

print("Rows:", len(listed_residential))
print("Duplicate rows:", listed_residential.duplicated().sum())
print("Completely empty rows:",
      listed_residential.isna().all(axis=1).sum())

print("\nPropertyType check:")
print(listed_residential["PropertyType"].value_counts(dropna=False))


# =========================
# Week 2: Validation + Missing Value Reports
# =========================


# Load Week 1 Residential listed dataset
listed = listed_residential.copy()

# Basic dataset structure
print("=== LISTED DATASET STRUCTURE ===")
print("\nShape:")
print(listed.shape)

print("\nColumns:")
print(listed.columns.tolist())

print("\nData types:")
print(listed.dtypes)

print("\nFirst 5 rows:")
print(listed.head())

# Confirm PropertyType values
print("\n=== PROPERTY TYPE CHECK ===")
if "PropertyType" in listed.columns:
    print(listed["PropertyType"].value_counts(dropna=False))
else:
    print("PropertyType column not found.")

# Missing value summary
print("\n=== MISSING VALUE REPORT ===")
null_counts = listed.isnull().sum()
null_percentages = (null_counts / len(listed)) * 100

missing_report = pd.DataFrame({
    "column": listed.columns,
    "null_count": null_counts.values,
    "null_percentage": null_percentages.values
}).sort_values(by="null_percentage", ascending=False)

print(missing_report)

# Columns above 90% null
print("\n=== COLUMNS WITH > 90% NULL ===")
high_missing = missing_report[missing_report["null_percentage"] > 90]

total_columns = len(missing_report)
flagged_columns = len(high_missing)
remaining_columns = total_columns - flagged_columns

print(f"Total columns: {total_columns}")
print(f"Columns flagged (>90% null): {flagged_columns}")
print(f"Remaining columns after flagging: {remaining_columns}")

if high_missing.empty:
    print("No columns above 90% null.")
else:
    print(high_missing)

# Numeric distribution summary
print("\n=== NUMERIC SUMMARY ===")
numeric_cols = [
    "ClosePrice",
    "ListPrice",
    "OriginalListPrice",
    "LivingArea",
    "LotSizeAcres",
    "BedroomsTotal",
    "BathroomsTotalInteger",
    "DaysOnMarket",
    "YearBuilt"
]
existing_numeric_cols = [col for col in numeric_cols if col in listed.columns]

if existing_numeric_cols:
    numeric_summary = listed[existing_numeric_cols].describe(
        percentiles=[0.25, 0.50, 0.75, 0.90, 0.95]
    )
    print(numeric_summary)

# Save reports
missing_report.to_csv("listed_missing_value_report.csv", index=False)
high_missing.to_csv("listed_high_missing_columns.csv", index=False)

if existing_numeric_cols:
    numeric_summary.to_csv("listed_numeric_distribution_summary.csv")

print("\nListed validation complete.")


# =========================
# Week 3: Mortgage Rate Enrichment
# =========================


# Step 1 – Fetch mortgage data
url = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=MORTGAGE30US"
mortgage = pd.read_csv(url)

mortgage.columns = ["date", "rate_30yr_fixed"]
mortgage["date"] = pd.to_datetime(mortgage["date"])

# Step 2 – Convert weekly mortgage rates to monthly averages
mortgage["year_month"] = mortgage["date"].dt.to_period("M")

mortgage_monthly = (
    mortgage.groupby("year_month")["rate_30yr_fixed"]
    .mean()
    .reset_index()
)

# Step 3 – Create year_month key from ListingContractDate
listed["year_month"] = pd.to_datetime(
    listed["ListingContractDate"]
).dt.to_period("M")

# Step 4 – Merge mortgage rates onto listed data
listed = listed.merge(mortgage_monthly, on="year_month", how="left")

# Step 5 – Validate merge
print("Listed null mortgage rates:", listed["rate_30yr_fixed"].isnull().sum())

print("\n=== LISTED PREVIEW ===")
print(
    listed[
        ["ListingContractDate", "year_month", "ListPrice", "rate_30yr_fixed"]
    ].head()
)

# Save Week 3 cumulative listed output
listed.to_csv("listed_mortgage_residential.csv", index=False)


# =========================
# Week 4: Data Cleaning
# =========================


print("\n=== WEEK 4: DATA CLEANING ===")

# Before cleaning row/column count
before_rows = len(listed)
before_cols = len(listed.columns)

print("\nBefore cleaning:")
print(f"Rows: {before_rows}")
print(f"Columns: {before_cols}")

# Convert date fields
date_cols = [
    "CloseDate",
    "PurchaseContractDate",
    "ListingContractDate",
    "ContractStatusChangeDate"
]

for col in date_cols:
    if col in listed.columns:
        listed[col] = pd.to_datetime(listed[col], errors="coerce")

print("\nDate columns converted:")
print(listed[[col for col in date_cols if col in listed.columns]].dtypes)

# Remove redundant .1 columns
duplicate_cols = [col for col in listed.columns if col.endswith(".1")]

print("\nDuplicate .1 columns removed:")
print(duplicate_cols)

listed = listed.drop(columns=duplicate_cols)

# Convert numeric fields
numeric_cols = [
    "ClosePrice",
    "ListPrice",
    "OriginalListPrice",
    "LivingArea",
    "LotSizeAcres",
    "BedroomsTotal",
    "BathroomsTotalInteger",
    "DaysOnMarket",
    "YearBuilt",
    "rate_30yr_fixed"
]

for col in numeric_cols:
    if col in listed.columns:
        listed[col] = pd.to_numeric(listed[col], errors="coerce")

print("\nNumeric columns converted:")
print(listed[[col for col in numeric_cols if col in listed.columns]].dtypes)

# Flag invalid numeric values
if "ClosePrice" in listed.columns:
    listed["invalid_close_price_flag"] = listed["ClosePrice"] <= 0

if "LivingArea" in listed.columns:
    listed["invalid_living_area_flag"] = listed["LivingArea"] <= 0

if "DaysOnMarket" in listed.columns:
    listed["invalid_days_on_market_flag"] = listed["DaysOnMarket"] < 0

if "BedroomsTotal" in listed.columns:
    listed["invalid_bedrooms_flag"] = listed["BedroomsTotal"] < 0

if "BathroomsTotalInteger" in listed.columns:
    listed["invalid_bathrooms_flag"] = listed["BathroomsTotalInteger"] < 0

print("\nInvalid numeric value flag counts:")
flag_cols = [col for col in listed.columns if col.startswith("invalid_")]
print(listed[flag_cols].sum())

total_invalid_numeric_flags = listed[flag_cols].sum().sum()
rows_with_any_invalid_numeric = listed[flag_cols].any(axis=1).sum()

print(f"Total invalid numeric flags: {total_invalid_numeric_flags}")
print(f"Rows with at least one invalid numeric value: {rows_with_any_invalid_numeric}")

# Date consistency flags
if "ListingContractDate" in listed.columns and "CloseDate" in listed.columns:
    listed["listing_after_close_flag"] = listed["ListingContractDate"] > listed["CloseDate"]

if "PurchaseContractDate" in listed.columns and "CloseDate" in listed.columns:
    listed["purchase_after_close_flag"] = listed["PurchaseContractDate"] > listed["CloseDate"]

if "ListingContractDate" in listed.columns and "PurchaseContractDate" in listed.columns:
    listed["negative_timeline_flag"] = listed["PurchaseContractDate"] < listed["ListingContractDate"]

print("\nDate consistency flag counts:")
date_flag_cols = [
    "listing_after_close_flag",
    "purchase_after_close_flag",
    "negative_timeline_flag"
]

existing_date_flags = [col for col in date_flag_cols if col in listed.columns]
print(listed[existing_date_flags].sum())

# Geographic data quality flags
if "Latitude" in listed.columns and "Longitude" in listed.columns:
    listed["missing_coordinates_flag"] = listed["Latitude"].isnull() | listed["Longitude"].isnull()
    listed["zero_coordinates_flag"] = (listed["Latitude"] == 0) | (listed["Longitude"] == 0)
    listed["positive_longitude_flag"] = listed["Longitude"] > 0

    # Approximate California coordinate bounds
    listed["implausible_coordinates_flag"] = (
        (listed["Latitude"] < 32) |
        (listed["Latitude"] > 42) |
        (listed["Longitude"] < -125) |
        (listed["Longitude"] > -114)
    )

print("\nGeographic data quality flag counts:")
geo_flag_cols = [
    "missing_coordinates_flag",
    "zero_coordinates_flag",
    "positive_longitude_flag",
    "implausible_coordinates_flag"
]

existing_geo_flags = [col for col in geo_flag_cols if col in listed.columns]
print(listed[existing_geo_flags].sum())

# After cleaning summary
after_rows = len(listed)
after_cols = len(listed.columns)

print("\nAfter cleaning:")
print(f"Rows: {after_rows}")
print(f"Columns: {after_cols}")
print(f"Rows removed: {before_rows - after_rows}")
print(f"Columns removed: {before_cols - after_cols}")

# Save cleaned dataset
listed.to_csv("listed_cleaned_residential.csv", index=False)

print("\nListed Week 4 cleaning complete.")
print("Saved: listed_cleaned_residential.csv")