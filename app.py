import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

# ==============================
# Page Config
# ==============================
st.set_page_config(page_title="Air Crashes Pro Dashboard", layout="wide")

st.title("✈️ Global Air Crashes Pro Analytics (1908 - 2023)")
st.write("Advanced interactive and statistical analysis of global air crash data.")

# ==============================
# Load Data
# ==============================
@st.cache_data
def load_data():
    df = pd.read_csv("Data/air_crashes.csv", encoding="latin1")
    return df

df = load_data()

# ==============================
# Data Cleaning
# ==============================
df['Fatalities (air)'] = pd.to_numeric(df['Fatalities (air)'], errors='coerce').fillna(0)
df['Aboard'] = pd.to_numeric(df['Aboard'], errors='coerce').fillna(0)

df['Year'] = pd.to_numeric(df['Year'], errors='coerce')
df = df.dropna(subset=['Year'])
df['Year'] = df['Year'].astype(int)

# ==============================
# Sidebar Filters
# ==============================
st.sidebar.header("Filters")

year_range = st.sidebar.slider(
    "Year Range",
    int(df['Year'].min()),
    int(df['Year'].max()),
    (2000, 2023)
)

countries = st.sidebar.multiselect(
    "Country / Region",
    sorted(df['Country/Region'].dropna().unique()),
    default=sorted(df['Country/Region'].dropna().unique())
)

filtered_df = df[
    (df['Year'] >= year_range[0]) &
    (df['Year'] <= year_range[1]) &
    (df['Country/Region'].isin(countries))
]

# ==============================
# KPI METRICS
# ==============================
st.subheader("Key Metrics")

col1, col2, col3 = st.columns(3)

col1.metric("Total Crashes", len(filtered_df))
col2.metric("Total Fatalities", int(filtered_df['Fatalities (air)'].sum()))
col3.metric("Avg Fatalities / Crash", round(filtered_df['Fatalities (air)'].mean(), 2))

st.write("---")

# ==============================
# TABS LAYOUT
# ==============================
tab1, tab2, tab3, tab4 = st.tabs([
    "Trends",
    "Geography",
    "Statistics",
    "Forecast"
])

# ==============================
# TAB 1 — TRENDS (PLOTLY)
# ==============================
with tab1:

    st.subheader("Crashes Over Time")

    crashes_per_year = filtered_df.groupby('Year').size().reset_index(name='Crashes')

    fig1 = px.line(
        crashes_per_year,
        x='Year',
        y='Crashes',
        markers=True
    )
    st.plotly_chart(fig1, use_container_width=True)

    st.subheader("Fatalities Over Time")

    fatalities_per_year = filtered_df.groupby('Year')['Fatalities (air)'].sum().reset_index()

    fig2 = px.scatter(
        fatalities_per_year,
        x='Year',
        y='Fatalities (air)',
        trendline="ols"
    )
    st.plotly_chart(fig2, use_container_width=True)

# ==============================
# TAB 2 — MAP
# ==============================
with tab2:

    st.subheader("Crash Locations Map")

    # Only works if lat/lon exists
    if 'Latitude' in filtered_df.columns and 'Longitude' in filtered_df.columns:

        map_df = filtered_df.dropna(subset=['Latitude', 'Longitude'])

        fig_map = px.scatter_geo(
            map_df,
            lat='Latitude',
            lon='Longitude',
            hover_name='Location'
        )

        st.plotly_chart(fig_map, use_container_width=True)

    else:
        st.info("Latitude and Longitude columns not found in dataset.")

    st.subheader("Top Countries")

    top_countries = (
        filtered_df['Country/Region']
        .value_counts()
        .head(10)
        .reset_index()
    )

    top_countries.columns = ['Country', 'Crashes']

    fig_country = px.bar(
        top_countries,
        x='Crashes',
        y='Country',
        orientation='h',
        text='Crashes'
    )

    st.plotly_chart(fig_country, use_container_width=True)

# ==============================
# TAB 3 — STATISTICS (SEABORN)
# ==============================
with tab3:

    st.subheader("Aboard vs Fatalities")

    fig3, ax3 = plt.subplots()
    sns.scatterplot(
        data=filtered_df,
        x='Aboard',
        y='Fatalities (air)',
        ax=ax3
    )
    st.pyplot(fig3)

    st.subheader("Fatalities Distribution")

    fig4, ax4 = plt.subplots()
    sns.histplot(filtered_df['Fatalities (air)'], bins=30, kde=True, ax=ax4)
    st.pyplot(fig4)

# ==============================
# TAB 4 — FORECAST (TREND PROJECTION)
# ==============================
with tab4:

    st.subheader("Crash Trend Projection")

    crashes_year = filtered_df.groupby('Year').size().reset_index(name='Crashes')

    crashes_year['Rolling Avg'] = crashes_year['Crashes'].rolling(5).mean()

    fig_forecast = px.line(
        crashes_year,
        x='Year',
        y=['Crashes', 'Rolling Avg']
    )

    st.plotly_chart(fig_forecast, use_container_width=True)

    st.info("Rolling average used as simple trend projection (not ML prediction).")

# ==============================
# DOWNLOAD
# ==============================
st.write("---")
st.subheader("⬇️ Download Filtered Data")

csv = filtered_df.to_csv(index=False).encode('utf-8')

st.download_button(
    "Download CSV",
    csv,
    "filtered_air_crashes.csv",
    "text/csv"
)

# ==============================
# FOOTER
# ==============================
st.write("---")
st.caption("Air Crashes Pro Dashboard | Python + Streamlit + Plotly + Seaborn")
