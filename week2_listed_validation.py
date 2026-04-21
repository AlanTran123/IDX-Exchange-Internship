import pandas as pd

# Load Week 1 Residential listed dataset
listed = pd.read_csv("listed_combined_residential.csv")

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
numeric_cols = ["ClosePrice", "LivingArea", "DaysOnMarket"]
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
