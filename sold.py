import pandas as pd
from pathlib import Path

# =========================
# Week 1: Aggregation + Residential Filter
# =========================

sold_folder = Path("raw/sold")
sold_files = sorted(sold_folder.glob("CRMLSSold*.csv"))

dfs = []

# row count for each individual file before append
print("Row count for each sold file before append:")
for file in sold_files:
    df = pd.read_csv(file, low_memory=False)
    print(f"{file.name}: {len(df)} rows")
    dfs.append(df)

# combine all files
sold_all = pd.concat(dfs, ignore_index=True)

# row count of the combined/appended dataset after concatenation
print("\nCombined sold dataset row count after concatenation:")
print(len(sold_all))

# remove duplicate rows
sold_all = sold_all.drop_duplicates()

# remove completely blank rows
sold_all = sold_all.dropna(how="all")

# frequency table of PropertyType before filtering
print("\nPropertyType frequency table before Residential filter:")
print(sold_all["PropertyType"].value_counts(dropna=False))

# keep only residential
sold_residential = sold_all[
    sold_all["PropertyType"] == "Residential"
].copy()

# row count after applying PropertyType == 'Residential'
print("\nSold row count after applying PropertyType == 'Residential':")
print(len(sold_residential))

# frequency table of PropertyType after filtering
print("\nPropertyType frequency table after Residential filter:")
print(sold_residential["PropertyType"].value_counts(dropna=False))

# save clean CSV
sold_residential.to_csv(
    "sold_combined_residential.csv",
    index=False
)

print("Rows:", len(sold_residential))
print("Duplicate rows:", sold_residential.duplicated().sum())
print("Completely empty rows:",
      sold_residential.isna().all(axis=1).sum())

print("\nPropertyType check:")
print(sold_residential["PropertyType"].value_counts(dropna=False))


# =========================
# Week 2: Validation + Missing Value Reports
# =========================


# Load Week 1 Residential sold dataset
sold = sold_residential.copy()

# Show dataset structure
print("=== SOLD DATASET STRUCTURE ===")
print("\nShape:")
print(sold.shape)

print("\nColumns:")
print(sold.columns.tolist())

print("\nData types:")
print(sold.dtypes)

print("\nFirst 5 rows:")
print(sold.head())

# Check PropertyType values
print("\n=== PROPERTY TYPE CHECK ===")
if "PropertyType" in sold.columns:
    print(sold["PropertyType"].value_counts(dropna=False))
else:
    print("PropertyType column not found.")

# Missing value summary
print("\n=== MISSING VALUE REPORT ===")
null_counts = sold.isnull().sum()
null_percentages = (null_counts / len(sold)) * 100

missing_report = pd.DataFrame({
    "column": sold.columns,
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
existing_numeric_cols = [col for col in numeric_cols if col in sold.columns]

if existing_numeric_cols:
    numeric_summary = sold[existing_numeric_cols].describe(
        percentiles=[0.25, 0.50, 0.75, 0.90, 0.95]
    )
    print(numeric_summary)

# Save reports
missing_report.to_csv("sold_missing_value_report.csv", index=False)
high_missing.to_csv("sold_high_missing_columns.csv", index=False)

if existing_numeric_cols:
    numeric_summary.to_csv("sold_numeric_distribution_summary.csv")

print("\nSold validation complete.")


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

# Step 3 – Create year_month key from CloseDate
sold["year_month"] = pd.to_datetime(sold["CloseDate"]).dt.to_period("M")

# Step 4 – Merge mortgage rates onto sold data
sold = sold.merge(mortgage_monthly, on="year_month", how="left")

# Step 5 – Validate merge
print("Sold null mortgage rates:", sold["rate_30yr_fixed"].isnull().sum())

print("\n=== SOLD PREVIEW ===")
print(
    sold[
        ["CloseDate", "year_month", "ClosePrice", "rate_30yr_fixed"]
    ].head()
)

# Save Week 3 cumulative sold output
sold.to_csv("sold_mortgage_residential.csv", index=False)


# =========================
# Week 4: Data Cleaning
# =========================


print("\n=== WEEK 4: DATA CLEANING ===")

# Before cleaning row/column count
before_rows = len(sold)
before_cols = len(sold.columns)

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
    if col in sold.columns:
        sold[col] = pd.to_datetime(sold[col], errors="coerce")

print("\nDate columns converted:")
print(sold[[col for col in date_cols if col in sold.columns]].dtypes)

# Remove redundant .1 columns
duplicate_cols = [col for col in sold.columns if col.endswith(".1")]

print("\nDuplicate .1 columns removed:")
print(duplicate_cols)

sold = sold.drop(columns=duplicate_cols)

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
    if col in sold.columns:
        sold[col] = pd.to_numeric(sold[col], errors="coerce")

print("\nNumeric columns converted:")
print(sold[[col for col in numeric_cols if col in sold.columns]].dtypes)


# Flag invalid numeric values
if "ClosePrice" in sold.columns:
    sold["invalid_close_price_flag"] = sold["ClosePrice"] <= 0

if "LivingArea" in sold.columns:
    sold["invalid_living_area_flag"] = sold["LivingArea"] <= 0

if "DaysOnMarket" in sold.columns:
    sold["invalid_days_on_market_flag"] = sold["DaysOnMarket"] < 0

if "BedroomsTotal" in sold.columns:
    sold["invalid_bedrooms_flag"] = sold["BedroomsTotal"] < 0

if "BathroomsTotalInteger" in sold.columns:
    sold["invalid_bathrooms_flag"] = sold["BathroomsTotalInteger"] < 0

print("\nInvalid numeric value flag counts:")
flag_cols = [col for col in sold.columns if col.startswith("invalid_")]
print(sold[flag_cols].sum())

total_invalid_numeric_flags = sold[flag_cols].sum().sum()
rows_with_any_invalid_numeric = sold[flag_cols].any(axis=1).sum()

print(f"Total invalid numeric flags: {total_invalid_numeric_flags}")
print(f"Rows with at least one invalid numeric value: {rows_with_any_invalid_numeric}")



# Date consistency flags
if "ListingContractDate" in sold.columns and "CloseDate" in sold.columns:
    sold["listing_after_close_flag"] = sold["ListingContractDate"] > sold["CloseDate"]

if "PurchaseContractDate" in sold.columns and "CloseDate" in sold.columns:
    sold["purchase_after_close_flag"] = sold["PurchaseContractDate"] > sold["CloseDate"]

if "ListingContractDate" in sold.columns and "PurchaseContractDate" in sold.columns:
    sold["negative_timeline_flag"] = sold["PurchaseContractDate"] < sold["ListingContractDate"]

print("\nDate consistency flag counts:")
date_flag_cols = [
    "listing_after_close_flag",
    "purchase_after_close_flag",
    "negative_timeline_flag"
]

existing_date_flags = [col for col in date_flag_cols if col in sold.columns]
print(sold[existing_date_flags].sum())


# Geographic data quality flags
if "Latitude" in sold.columns and "Longitude" in sold.columns:
    sold["missing_coordinates_flag"] = sold["Latitude"].isnull() | sold["Longitude"].isnull()
    sold["zero_coordinates_flag"] = (sold["Latitude"] == 0) | (sold["Longitude"] == 0)
    sold["positive_longitude_flag"] = sold["Longitude"] > 0

    # Approximate California coordinate bounds
    sold["implausible_coordinates_flag"] = (
        (sold["Latitude"] < 32) |
        (sold["Latitude"] > 42) |
        (sold["Longitude"] < -125) |
        (sold["Longitude"] > -114)
    )

print("\nGeographic data quality flag counts:")
geo_flag_cols = [
    "missing_coordinates_flag",
    "zero_coordinates_flag",
    "positive_longitude_flag",
    "implausible_coordinates_flag"
]

existing_geo_flags = [col for col in geo_flag_cols if col in sold.columns]
print(sold[existing_geo_flags].sum())


# After cleaning summary
after_rows = len(sold)
after_cols = len(sold.columns)

print("\nAfter cleaning:")
print(f"Rows: {after_rows}")
print(f"Columns: {after_cols}")
print(f"Rows removed: {before_rows - after_rows}")
print(f"Columns removed: {before_cols - after_cols}")


# Save cleaned dataset
sold.to_csv("sold_cleaned_residential.csv", index=False)

print("\nSold Week 4 cleaning complete.")
print("Saved: sold_cleaned_residential.csv")