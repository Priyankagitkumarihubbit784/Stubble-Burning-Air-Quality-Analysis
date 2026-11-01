
import requests
import pandas as pd

# Coordinates of our three study cities
cities = {
    "Delhi": (28.6139, 77.2090),
    "Chandigarh": (30.7333, 76.7794),
    "Ludhiana": (30.9010, 75.8573)
}

weather_frames = []

for city, (latitude, longitude) in cities.items():

    print(f"Downloading weather for {city}...")

    url = "https://archive-api.open-meteo.com/v1/archive"

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "start_date": "2022-01-01",
        "end_date": "2025-12-31",
        "daily": [
            "temperature_2m_mean",
            "relative_humidity_2m_mean",
            "wind_speed_10m_mean",
            "wind_direction_10m_dominant"
        ],
        "timezone": "Asia/Kolkata"
    }

    response = requests.get(url, params=params, timeout=120)
    response.raise_for_status()

    data = response.json()

    city_df = pd.DataFrame(data["daily"])
    city_df["city"] = city

    weather_frames.append(city_df)

    print(f"{city}: {len(city_df)} records downloaded.")

# Combine all three cities
weather_df = pd.concat(weather_frames, ignore_index=True)

# Rename date column
weather_df.rename(columns={"time": "date"}, inplace=True)

# Save dataset
weather_df.to_csv("weather_data.csv", index=False)

print("\nWeather dataset downloaded successfully!")
print("Dataset shape:", weather_df.shape)

print("\nFirst five records:")
print(weather_df.head())

print("\nMissing values:")
print(weather_df.isnull().sum())
