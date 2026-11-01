import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load final dataset
df = pd.read_csv("final_analysis_dataset.csv")

df["date"] = pd.to_datetime(df["date"])

sns.set_theme(style="whitegrid")

# 1. Average AQI by city
plt.figure(figsize=(9, 5))
sns.barplot(data=df, x="city", y="india_aqi_pm")
plt.title("Average AQI by City")
plt.xlabel("City")
plt.ylabel("Average AQI")
plt.tight_layout()
plt.savefig("average_aqi_by_city.png")
plt.show()

# 2. Fire activity over time
fire_daily = df.drop_duplicates(subset=["date"])

plt.figure(figsize=(12, 5))
plt.plot(
    fire_daily["date"],
    fire_daily["fire_count"]
)
plt.title("Daily Fire Detections in Punjab-Haryana Study Area")
plt.xlabel("Date")
plt.ylabel("Fire Count")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("daily_fire_trend.png")
plt.show()

# 3. AQI trend by city
plt.figure(figsize=(12, 5))
sns.lineplot(
    data=df,
    x="date",
    y="india_aqi_pm",
    hue="city"
)
plt.title("Daily AQI Trend Across Three Cities")
plt.xlabel("Date")
plt.ylabel("AQI")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("aqi_trend_by_city.png")
plt.show()

# 4. Correlation heatmap
numeric_columns = [
    "india_aqi_pm",
    "pm2_5_mean",
    "fire_count",
    "total_frp",
    "temperature_2m_mean",
    "relative_humidity_2m_mean",
    "wind_speed_10m_mean"
]

plt.figure(figsize=(10, 7))
sns.heatmap(
    df[numeric_columns].corr(),
    annot=True,
    cmap="coolwarm",
    fmt=".2f"
)
plt.title("Correlation Between AQI, Fire and Weather")
plt.tight_layout()
plt.savefig("correlation_heatmap.png")
plt.show()

print("EDA completed successfully!")
print("\nAverage AQI by city:")
print(df.groupby("city")["india_aqi_pm"].mean())

print("\nAverage PM2.5 by city:")
print(df.groupby("city")["pm2_5_mean"].mean())

print("\nTotal regional fire detections:")
print(fire_daily["fire_count"].sum())