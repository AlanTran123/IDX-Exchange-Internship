import pandas as pd
from pathlib import Path

sold_folder = Path("raw/sold")
sold_files = sorted(sold_folder.glob("CRMLSSold*.csv"))

dfs = []
for file in sold_files:
    df = pd.read_csv(file, low_memory=False)
    dfs.append(df)

# combine all files
sold_all = pd.concat(dfs, ignore_index=True)

# remove duplicate rows
sold_all = sold_all.drop_duplicates()

# remove completely blank rows
sold_all = sold_all.dropna(how="all")

# keep only residential
sold_residential = sold_all[
    sold_all["PropertyType"] == "Residential"
].copy()

# save clean CSV
sold_residential.to_csv(
    "sold_combined_residential.csv",
    index=False
)

print("Sold rows:", len(sold_residential))
