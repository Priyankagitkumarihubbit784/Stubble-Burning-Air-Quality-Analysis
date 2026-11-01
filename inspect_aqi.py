import pandas as pd

# Load AQI dataset
aqi_df = pd.read_csv("air_quality_daily.csv")

aqi_df["date"] = pd.to_datetime(aqi_df["date"])

print("AQI DATASET SHAPE:")
print(aqi_df.shape)

print("\nCOLUMN NAMES:")
print(aqi_df.columns.tolist())

print("\nAVAILABLE CITIES:")
print(aqi_df["city"].value_counts())

print("\nDATE COVERAGE:")
print(aqi_df["date"].min(), "to", aqi_df["date"].max())

print("\nMISSING VALUES:")
print(aqi_df.isnull().sum())

print("\nFIRST FIVE RECORDS:")
print(aqi_df.head())