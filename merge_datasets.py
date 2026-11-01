import pandas as pd

# Load prepared datasets
aqi = pd.read_csv("selected_aqi_data.csv")
weather = pd.read_csv("selected_weather_data.csv")
fire = pd.read_csv("daily_fire_counts.csv")

# Convert date columns
aqi["date"] = pd.to_datetime(aqi["date"])
weather["date"] = pd.to_datetime(weather["date"])
fire["date"] = pd.to_datetime(fire["date"])

# Merge AQI and weather using date and city
merged = pd.merge(
    aqi,
    weather,
    on=["date", "city"],
    how="inner"
)

# Merge regional fire counts using date
merged = pd.merge(
    merged,
    fire,
    on="date",
    how="left"
)

# Check missing values
print("Missing values before cleaning:")
print(merged.isnull().sum())

# Save combined dataset
merged.to_csv("final_analysis_dataset.csv", index=False)

print("\nAll datasets merged successfully!")

print("\nFinal dataset shape:", merged.shape)

print("\nRecords per city:")
print(merged.groupby("city").size())

print("\nDate coverage:")
print(merged["date"].min(), "to", merged["date"].max())

print("\nFirst five records:")
print(merged.head())

print("\nFinal missing values:")
print(merged.isnull().sum())