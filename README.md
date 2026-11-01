
# Stubble Burning and Winter Air Quality Analysis

## Project Overview

This project analyzes the relationship between agricultural stubble burning and winter air pollution in North India, focusing on Delhi, Chandigarh, and Ludhiana.

It examines whether increased fire activity in the approximate Punjab-Haryana study region is associated with rising AQI and PM2.5 levels. The project also investigates delayed effects of fire activity and studies the influence of weather conditions such as temperature, humidity, and wind speed.

## Objectives

- Analyze daily fire activity in the Punjab-Haryana study region.
- Study AQI and PM2.5 trends in Delhi, Chandigarh, and Ludhiana.
- Identify the time lag between fire activity and changes in AQI.
- Examine the relationship between fire counts and air quality.
- Evaluate the influence of weather conditions using regression analysis.
- Present findings through visualizations and an interactive Tableau dashboard.

## Technologies and Tools

- Python
- Pandas and NumPy
- Matplotlib and Seaborn
- Statsmodels
- Tableau Public
- Jupyter Notebook / VS Code
- Git and GitHub

## Data Sources

1. **NASA FIRMS:** VIIRS satellite fire detection data.
2. **India Weather and Air Quality Dataset:** Daily air quality data from Hugging Face.
3. **Open-Meteo Historical Weather API:** Historical temperature, humidity, and wind speed data.

## Study Details

- Cities: Delhi, Chandigarh, and Ludhiana.
- Fire study region: Approximate Punjab-Haryana geographic bounding box.
- Analysis period: 5 August 2022 to 30 November 2022.
- Total analysis records: 354 city-date records.
- Daily observations: 118 dates.

## Methodology

1. **Data Collection:** Collected satellite fire detections, air quality data, and historical weather information.
2. **Data Preprocessing:** Filtered the fire dataset geographically, selected the three cities, handled missing dates, and prepared daily fire counts.
3. **Data Integration:** Combined fire, AQI, PM2.5, and weather datasets using date and city.
4. **Exploratory Data Analysis:** Created charts and correlation heatmaps to understand patterns.
5. **Lag Analysis:** Tested fire-AQI correlations for delays from 0 to 5 days.
6. **Regression Analysis:** Used multiple linear regression with weather controls to examine the relationship between fire activity and AQI.
7. **Visualization:** Developed an interactive Tableau dashboard.

## Key Findings

- Average AQI was highest in Delhi (160.34), followed by Ludhiana (111.35) and Chandigarh (76.21).
- Fire activity increased during the October-November period.
- The strongest observed fire-AQI correlation occurred at a two-day lag, with a correlation of approximately 0.559.
- The regression model achieved an R-squared value of approximately 0.624.
- The fire-count coefficient was positive, but its Newey-West robust p-value was approximately 0.051. Therefore, it was borderline and did not meet the conventional 5% significance threshold.
- Weather variables also showed relationships with AQI.

## Tableau Dashboard

Explore the interactive dashboard:

[View Stubble Burning and Air Quality Dashboard](https://public.tableau.com/app/profile/priyanka.kumari7444/viz/Book1Stubble_Burning_Air_Quality_Analysis_twbx/Dashboard1?publish=yes)

## Project Structure

```text
Stubble_Burning_Air_Quality_Analysis/
│
├── download_weather.py
├── inspect_fire.py
├── inspect_aqi.py
├── prepare_fire.py
├── prepare_aqi.py
├── prepare_weather.py
├── merge_datasets.py
├── eda_analysis.py
├── lag_analysis.py
├── regression_analysis.py
│
├── daily_fire_counts.csv
├── regional_fire_data.csv
├── selected_aqi_data.csv
├── selected_weather_data.csv
├── weather_data.csv
├── final_analysis_dataset.csv
├── lag_analysis_results.csv
├── regression_results.csv
│
├── average_aqi_by_city.png
├── daily_fire_trend.png
├── aqi_trend_by_city.png
├── correlation_heatmap.png
├── lag_correlation.png
│
├── .gitignore
└── README.md
```

## Limitations

- The fire study region was selected using approximate latitude and longitude boundaries, not exact state borders.
- The air quality dataset uses CAMS model estimates at approximately 45 km grid resolution, not direct CPCB ground-station measurements.
- The analysis covers only the overlapping period from August to November 2022.
- Correlation and regression results show statistical associations and do not establish causation.
- The regression analysis has potential time-series autocorrelation, so robust Newey-West standard errors were also considered.

## Conclusion

The analysis identifies a positive relationship between regional fire activity and air quality indicators, with the strongest observed correlation at a two-day lag. However, the regression results indicate that the fire-count effect is borderline after accounting for weather conditions. Further analysis using longer time periods, exact state boundaries, and ground-based air quality observations would help strengthen the findings.

## Author

**Priyanka Tiwari**

MCA (Artificial Intelligence and Machine Learning)
