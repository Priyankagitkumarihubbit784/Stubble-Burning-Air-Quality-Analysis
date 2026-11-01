import pandas as pd

# Load regional fire data
fire_df = pd.read_csv("regional_fire_data.csv")

fire_df["acq_date"] = pd.to_datetime(fire_df["acq_date"])

# Calculate daily fire statistics
daily_fire = fire_df.groupby("acq_date").agg(
    fire_count=("latitude", "count"),
    total_frp=("frp", "sum"),
    average_frp=("frp", "mean")
)

# Create complete date range
all_dates = pd.date_range(
    start="2022-01-01",
    end="2022-11-30",
    freq="D"
)

# Include dates with zero detections
daily_fire = daily_fire.reindex(all_dates)

daily_fire.index.name = "date"
daily_fire = daily_fire.reset_index()

# Fill missing fire counts and FRP totals with zero
daily_fire["fire_count"] = daily_fire["fire_count"].fillna(0)
daily_fire["total_frp"] = daily_fire["total_frp"].fillna(0)
daily_fire["average_frp"] = daily_fire["average_frp"].fillna(0)

# Save final dataset
daily_fire.to_csv("daily_fire_counts.csv", index=False)

print("Daily fire dataset prepared successfully!")
print("\nDataset shape:", daily_fire.shape)
print("\nTotal fire detections:", daily_fire["fire_count"].sum())
print("\nDays with zero detections:",
      (daily_fire["fire_count"] == 0).sum())

print("\nFirst five records:")
print(daily_fire.head())