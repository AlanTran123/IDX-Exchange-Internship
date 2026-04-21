import pandas as pd

# Load Week 1 Residential sold dataset
sold = pd.read_csv("sold_combined_residential.csv")

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
numeric_cols = ["ClosePrice", "LivingArea", "DaysOnMarket"]
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
