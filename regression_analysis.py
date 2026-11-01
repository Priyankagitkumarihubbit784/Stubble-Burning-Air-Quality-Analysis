import pandas as pd
import statsmodels.api as sm

# Load final dataset
df = pd.read_csv("final_analysis_dataset.csv")

df["date"] = pd.to_datetime(df["date"])

# Aggregate AQI and weather by date
daily = df.groupby("date").agg(
    average_aqi=("india_aqi_pm", "mean"),
    temperature=("temperature_2m_mean", "mean"),
    humidity=("relative_humidity_2m_mean", "mean"),
    wind_speed=("wind_speed_10m_mean", "mean"),
    fire_count=("fire_count", "first")
).reset_index()

# Create 2-day lag of fire activity
daily["fire_lag_2"] = daily["fire_count"].shift(2)

# Remove rows with missing lag values
daily = daily.dropna()

# Define independent and dependent variables
X = daily[
    [
        "fire_lag_2",
        "temperature",
        "humidity",
        "wind_speed"
    ]
]

y = daily["average_aqi"]

# Add intercept
X = sm.add_constant(X)

# Fit regression model
model = sm.OLS(y, X).fit()

# Display results
print("\nMULTIPLE LINEAR REGRESSION RESULTS")
print(model.summary())

# Save coefficients
coefficients = pd.DataFrame({
    "Variable": model.params.index,
    "Coefficient": model.params.values,
    "P_Value": model.pvalues.values
})

coefficients.to_csv(
    "regression_results.csv",
    index=False
)

print("\nRegression results saved successfully!")

print("\nR-squared:", round(model.rsquared, 3))
print("Adjusted R-squared:", round(model.rsquared_adj, 3))

# Robustness check using HAC standard errors
hac_model = model.get_robustcov_results(
    cov_type="HAC",
    maxlags=3
)

print("\nHAC ROBUST REGRESSION RESULTS")
print(hac_model.summary())