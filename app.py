
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# ---------------- PAGE CONFIGURATION ----------------

st.set_page_config(
    page_title="Stubble Burning & Air Quality Analytics",
    page_icon="🌍",
    layout="wide"
)

BASE_DIR = Path(__file__).resolve().parent

# ---------------- LOAD DATA ----------------

@st.cache_data
def load_data():
    main = pd.read_csv(BASE_DIR / "final_analysis_dataset.csv")
    lag = pd.read_csv(BASE_DIR / "lag_analysis_results.csv")
    regression = pd.read_csv(BASE_DIR / "regression_results.csv")

    main["date"] = pd.to_datetime(main["date"])

    return main, lag, regression


try:
    df, lag_df, regression_df = load_data()
except Exception as e:
    st.error(f"Unable to load project datasets: {e}")
    st.stop()

# ---------------- HEADER ----------------

st.title("🌍 Stubble Burning & Air Quality Analytics")

st.markdown(
    """
    Explore the relationship between agricultural fire activity
    and winter air pollution in Delhi, Chandigarh and Ludhiana.
    """
)

st.caption("Study period: 5 August 2022 to 30 November 2022")

st.divider()

# ---------------- SIDEBAR ----------------

st.sidebar.title("Analysis Controls")

cities = sorted(df["city"].dropna().unique())

selected_city = st.sidebar.selectbox(
    "Select City",
    ["All Cities"] + cities
)

min_date = df["date"].min().date()
max_date = df["date"].max().date()

date_range = st.sidebar.date_input(
    "Select Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

if isinstance(date_range, tuple) and len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date, end_date = min_date, max_date

filtered = df[
    (df["date"].dt.date >= start_date) &
    (df["date"].dt.date <= end_date)
].copy()

if selected_city != "All Cities":
    filtered = filtered[filtered["city"] == selected_city]

if filtered.empty:
    st.warning("No data available for this selection.")
    st.stop()

# ---------------- SUMMARY METRICS ----------------

st.subheader("Air Quality Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Average AQI",
    f"{filtered['india_aqi_pm'].mean():.2f}"
)

col2.metric(
    "Average PM2.5",
    f"{filtered['pm2_5_mean'].mean():.2f}"
)

# Fire counts are regional and repeated for each city.
# Use one record per date to avoid counting them multiple times.

fire_data = (
    filtered.sort_values("date")
    .drop_duplicates(subset=["date"])
)

col3.metric(
    "Total Fire Detections",
    f"{int(fire_data['fire_count'].sum()):,}"
)

col4.metric(
    "Cities Selected",
    filtered["city"].nunique()
)

st.divider()

# ---------------- TABS ----------------

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 AQI Analysis",
    "🔥 Fire Activity",
    "⏳ Lag Analysis",
    "📈 Regression",
    "📁 Explore Data"
])

# ---------------- TAB 1: AQI ANALYSIS ----------------

with tab1:

    st.subheader("Daily AQI Trend")

    fig = px.line(
        filtered,
        x="date",
        y="india_aqi_pm",
        color="city",
        markers=True,
        title="Daily AQI Across Selected Cities",
        labels={
            "date": "Date",
            "india_aqi_pm": "AQI",
            "city": "City"
        }
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("PM2.5 Trend")

    fig2 = px.line(
        filtered,
        x="date",
        y="pm2_5_mean",
        color="city",
        markers=True,
        title="Daily Average PM2.5",
        labels={
            "date": "Date",
            "pm2_5_mean": "PM2.5"
        }
    )

    st.plotly_chart(fig2, use_container_width=True)

    city_summary = (
        filtered.groupby("city", as_index=False)
        .agg(
            Average_AQI=("india_aqi_pm", "mean"),
            Average_PM25=("pm2_5_mean", "mean")
        )
    )

    st.subheader("City-wise Comparison")

    fig3 = px.bar(
        city_summary,
        x="city",
        y="Average_AQI",
        color="city",
        title="Average AQI by City",
        text_auto=".2f"
    )

    st.plotly_chart(fig3, use_container_width=True)


# ---------------- TAB 2: FIRE ACTIVITY ----------------

with tab2:

    st.subheader("Regional Fire Activity")

    daily_fire = (
        fire_data.groupby("date", as_index=False)
        .agg(fire_count=("fire_count", "max"))
    )

    fig4 = px.area(
        daily_fire,
        x="date",
        y="fire_count",
        title="Daily Fire Detections in the Study Region",
        labels={
            "date": "Date",
            "fire_count": "Fire Detections"
        }
    )

    st.plotly_chart(fig4, use_container_width=True)

    st.info(
        "Fire detections represent the approximate Punjab-Haryana "
        "study region. They are regional counts, not city-specific counts."
    )

    st.metric(
        "Fire Detections in Selected Period",
        f"{int(daily_fire['fire_count'].sum()):,}"
    )


# ---------------- TAB 3: LAG ANALYSIS ----------------

with tab3:

    st.subheader("Fire Activity vs AQI: Lag Analysis")

    st.write(
        "This analysis checks how the relationship between fire "
        "activity and AQI changes over delays of 0 to 5 days."
    )

    lag_columns = lag_df.columns.tolist()

    lag_col = next(
        (c for c in lag_columns if "lag" in c.lower()),
        lag_columns[0]
    )

    corr_col = next(
        (
            c for c in lag_columns
            if "corr" in c.lower()
            or "pearson" in c.lower()
        ),
        lag_columns[-1]
    )

    fig5 = px.bar(
        lag_df,
        x=lag_col,
        y=corr_col,
        text_auto=".3f",
        title="Correlation at Different Time Lags",
        labels={
            lag_col: "Lag (Days)",
            corr_col: "Correlation"
        }
    )

    st.plotly_chart(fig5, use_container_width=True)

    best_row = lag_df.loc[lag_df[corr_col].idxmax()]

    st.success(
        f"Strongest observed correlation: {best_row[corr_col]:.3f} "
        f"at {best_row[lag_col]}."
    )

    st.caption(
        "Correlation indicates association, not causation."
    )


# ---------------- TAB 4: REGRESSION ----------------

with tab4:

    st.subheader("Multiple Linear Regression")

    st.write(
        "The regression analysis examines the relationship between "
        "fire activity and AQI while controlling for weather variables."
    )

    st.dataframe(
        regression_df,
        use_container_width=True,
        hide_index=True
    )

    st.info(
        "The model R-squared is approximately 0.624. "
        "The fire coefficient has a Newey-West robust p-value "
        "of approximately 0.051, which is borderline and does "
        "not meet the conventional 5% significance threshold."
    )


# ---------------- TAB 5: DATA EXPLORER ----------------

with tab5:

    st.subheader("Explore the Dataset")

    st.write(
        "View the filtered records and download the selected data."
    )

    st.dataframe(
        filtered,
        use_container_width=True,
        hide_index=True
    )

    csv = filtered.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="⬇ Download Filtered Data as CSV",
        data=csv,
        file_name="filtered_air_quality_data.csv",
        mime="text/csv"
    )

    st.download_button(
        label="⬇ Download Lag Analysis Results",
        data=lag_df.to_csv(index=False).encode("utf-8"),
        file_name="lag_analysis_results.csv",
        mime="text/csv"
    )

# ---------------- FOOTER ----------------

st.divider()

st.markdown(
    """
    **Project:** Stubble Burning and Winter Air Quality Analysis

    **Tools:** Python, Pandas, Plotly, Streamlit and Tableau

    **Author:** Priyanka Tiwari
    """
)

st.markdown(
    "[View Interactive Tableau Dashboard](https://public.tableau.com/app/profile/priyanka.kumari7444/viz/Book1Stubble_Burning_Air_Quality_Analysis_twbx/Dashboard1?publish=yes)"
)
