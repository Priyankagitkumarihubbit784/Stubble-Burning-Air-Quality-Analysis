import pandas as pd

# Load AQI dataset
aqi_df = pd.read_csv("air_quality_daily.csv")

# Convert date column
aqi_df["date"] = pd.to_datetime(aqi_df["date"])

# Select our three study cities
selected_cities = ["Delhi", "Chandigarh", "Ludhiana"]

aqi_df = aqi_df[
    aqi_df["city"].isin(selected_cities)
].copy()

# Select useful columns
aqi_df = aqi_df[
    [
        "date",
        "city",
        "pm2_5_mean",
        "pm2_5_max",
        "india_aqi_pm",
        "india_aqi_pm_category",
        "dominant_pollutant"
    ]
]

# Keep only the overlapping fire-data period
aqi_df = aqi_df[
    (aqi_df["date"] >= "2022-08-05") &
    (aqi_df["date"] <= "2022-11-30")
]

# Save prepared dataset
aqi_df.to_csv("selected_aqi_data.csv", index=False)

print("AQI dataset prepared successfully!")

print("\nDataset shape:", aqi_df.shape)

print("\nRecords per city:")
print(aqi_df.groupby("city").size())

print("\nDate coverage:")
print(aqi_df["date"].min(), "to", aqi_df["date"].max())

print("\nFirst five records:")
print(aqi_df.head())