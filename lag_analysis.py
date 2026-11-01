import pandas as pd
import matplotlib.pyplot as plt

# Load final dataset
df = pd.read_csv("final_analysis_dataset.csv")

df["date"] = pd.to_datetime(df["date"])

# Aggregate AQI across the three cities
daily_aqi = df.groupby("date").agg(
    average_aqi=("india_aqi_pm", "mean"),
    average_pm25=("pm2_5_mean", "mean")
).reset_index()

# Extract one regional fire count per date
daily_fire = df[
    ["date", "fire_count"]
].drop_duplicates(subset=["date"])

# Merge daily AQI and fire activity
daily = pd.merge(
    daily_aqi,
    daily_fire,
    on="date",
    how="inner"
)

# Calculate correlations for lags 0 to 5
results = []

for lag in range(6):

    daily[f"fire_lag_{lag}"] = daily["fire_count"].shift(lag)

    correlation = daily[
        ["average_aqi", f"fire_lag_{lag}"]
    ].corr().iloc[0, 1]

    results.append({
        "Lag_Days": lag,
        "Correlation": correlation
    })

# Display results
results_df = pd.DataFrame(results)

print("\nLAG ANALYSIS RESULTS:")
print(results_df.round(3))

# Identify strongest correlation
best = results_df.loc[
    results_df["Correlation"].abs().idxmax()
]

print("\nStrongest correlation:")
print("Lag:", best["Lag_Days"], "days")
print("Correlation:", round(best["Correlation"], 3))

# Plot lag correlations
plt.figure(figsize=(9, 5))

plt.bar(
    results_df["Lag_Days"],
    results_df["Correlation"]
)

plt.title("Fire Activity and AQI: Lag Correlation Analysis")
plt.xlabel("Fire Activity Lag (Days)")
plt.ylabel("Pearson Correlation")

plt.xticks(range(6))
plt.tight_layout()

plt.savefig("lag_correlation.png")
plt.show()

# Save results
results_df.to_csv("lag_analysis_results.csv", index=False)

print("\nLag analysis completed successfully!")