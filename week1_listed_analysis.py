import pandas as pd
from pathlib import Path

listed_folder = Path("raw/listed")
listed_files = sorted(listed_folder.glob("CRMLSListing*.csv"))

dfs = []
for file in listed_files:
    df = pd.read_csv(file, low_memory=False)
    dfs.append(df)

# combine all files
listed_all = pd.concat(dfs, ignore_index=True)

# remove duplicate rows
listed_all = listed_all.drop_duplicates()

# remove completely blank rows
listed_all = listed_all.dropna(how="all")

# keep only residential
listed_residential = listed_all[
    listed_all["PropertyType"] == "Residential"
].copy()

# save clean CSV
listed_residential.to_csv(
    "listed_combined_residential.csv",
    index=False
)

print("Listed rows:", len(listed_residential))
