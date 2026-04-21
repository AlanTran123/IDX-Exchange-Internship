import pandas as pd

# Load datasets
sold = pd.read_csv("sold_combined_residential.csv")
listed = pd.read_csv("listed_combined_residential.csv")

# Step 1 – Fetch mortgage data
url = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=MORTGAGE30US"
mortgage = pd.read_csv(url)

mortgage.columns = ['date', 'rate_30yr_fixed']
mortgage['date'] = pd.to_datetime(mortgage['date'])

# Step 2 – Convert weekly → monthly
mortgage['year_month'] = mortgage['date'].dt.to_period('M')

mortgage_monthly = (
    mortgage.groupby('year_month')['rate_30yr_fixed']
    .mean()
    .reset_index()
)

# Step 3 – Create year_month keys
sold['year_month'] = pd.to_datetime(sold['CloseDate']).dt.to_period('M')

listed['year_month'] = pd.to_datetime(
    listed['ListingContractDate']
).dt.to_period('M')

# Step 4 – Merge
sold_with_rates = sold.merge(mortgage_monthly, on='year_month', how='left')
listed_with_rates = listed.merge(mortgage_monthly, on='year_month', how='left')

# Step 5 – Validate
print("Sold null mortgage rates:", sold_with_rates['rate_30yr_fixed'].isnull().sum())
print("Listed null mortgage rates:", listed_with_rates['rate_30yr_fixed'].isnull().sum())

# Preview 
print("\n=== PREVIEW ===")
print(
    sold_with_rates[
        ['CloseDate', 'year_month', 'ClosePrice', 'rate_30yr_fixed']
    ].head()
)

# Save outputs
sold_with_rates.to_csv("sold_mortgage_residential.csv", index=False)
listed_with_rates.to_csv("listed_mortgage_residential.csv", index=False)
