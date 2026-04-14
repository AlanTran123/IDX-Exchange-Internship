import pandas as pd
from pathlib import Path

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