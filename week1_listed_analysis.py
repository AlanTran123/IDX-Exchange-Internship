import pandas as pd
from pathlib import Path

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
