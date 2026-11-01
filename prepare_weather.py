import pandas as pd

# Load weather dataset
weather_df = pd.read_csv("weather_data.csv")

# Convert date
weather_df["date"] = pd.to_datetime(weather_df["date"])

# Select three cities
selected_cities = ["Delhi", "Chandigarh", "Ludhiana"]

weather_df = weather_df[
    weather_df["city"].isin(selected_cities)
].copy()

# Select required weather columns
weather_df = weather_df[
    [
        "date",
        "city",
        "temperature_2m_mean",
        "relative_humidity_2m_mean",
        "wind_speed_10m_mean"
    ]
]

# Filter analysis period
weather_df = weather_df[
    (weather_df["date"] >= "2022-08-05") &
    (weather_df["date"] <= "2022-11-30")
]

# Save prepared dataset
weather_df.to_csv("selected_weather_data.csv", index=False)

print("Weather dataset prepared successfully!")

print("\nDataset shape:", weather_df.shape)

print("\nRecords per city:")
print(weather_df.groupby("city").size())

print("\nDate coverage:")
print(weather_df["date"].min(), "to", weather_df["date"].max())

print("\nMissing values:")
print(weather_df.isnull().sum())

print("\nFirst five records:")
print(weather_df.head())