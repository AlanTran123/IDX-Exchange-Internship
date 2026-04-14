import pandas as pd
import matplotlib.pyplot as plt

sold = pd.read_csv("sold_combined_residential.csv")

numeric_fields = [
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

existing_fields = [col for col in numeric_fields if col in sold.columns]

for col in existing_fields:
    print(f"\n=== {col} SUMMARY ===")
    print(
        sold[col].describe(
            percentiles=[0.01, 0.05, 0.25, 0.50, 0.75, 0.95, 0.99]
        )
    )

    # Histogram
    plt.figure(figsize=(10, 4))
    plt.hist(sold[col].dropna(), bins=50)
    plt.title(f"{col} Histogram")
    plt.xlabel(col)
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.savefig(f"{col}_histogram.png")
    plt.close()

    # Boxplot
    plt.figure(figsize=(10, 2))
    plt.boxplot(sold[col].dropna(), vert=False)
    plt.title(f"{col} Boxplot")
    plt.tight_layout()
    plt.savefig(f"{col}_boxplot.png")
    plt.close()

print("\nAll plots saved.")
