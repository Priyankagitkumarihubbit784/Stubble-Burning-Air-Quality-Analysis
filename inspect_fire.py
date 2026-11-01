import pandas as pd

fire_df = pd.read_csv("fire_data.csv")

# Filter dates
fire_df["acq_date"] = pd.to_datetime(fire_df["acq_date"])

# Approximate geographic bounds for Punjab and Haryana
regional_fires = fire_df[
    (fire_df["latitude"] >= 27.5) &
    (fire_df["latitude"] <= 32.6) &
    (fire_df["longitude"] >= 73.8) &
    (fire_df["longitude"] <= 77.7)
].copy()

print("Original India fire records:", len(fire_df))
print("Regional fire records:", len(regional_fires))

print("\nDate-wise regional detections:")
print(regional_fires.groupby(
    regional_fires["acq_date"].dt.month
).size())

print("\nConfidence distribution:")
print(regional_fires["confidence"].value_counts())

# Save filtered data
regional_fires.to_csv("regional_fire_data.csv", index=False)

print("\nRegional dataset saved successfully!")