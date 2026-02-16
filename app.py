import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pydeck as pdk

# ==============================
# Page Configuration
# ==============================
st.set_page_config(page_title="Air Crashes Analysis", layout="wide")

# ==============================
# Title and Project Overview
# ==============================
st.title("✈ Air Crashes Analysis (1908 – 2023)")
st.write(
    "An interactive analysis of global air crash data. "
    "Explore historical trends, deadliest crashes, aircraft patterns, and geographic distribution."
)

# ==============================
# Load Data
# ==============================
@st.cache_data
def load_data():
    df = pd.read_csv("data/Air_Crashes_Full_Data.csv")
    return df

df = load_data()

# ==============================
# Data Cleaning
# ==============================
df['Fatalities (air)'] = df['Fatalities (air)'].fillna(0)
df['Aboard'] = df['Aboard'].fillna(0)
df = df.dropna(subset=['Year'])
df['Year'] = df['Year'].astype(int)
df['Fatalities (air)'] = df['Fatalities (air)'].astype(int)
df['Aboard'] = df['Aboard'].astype(int)

# ==============================
# Sidebar Filters
# ==============================
st.sidebar.header("Filter Data")
year_range = st.sidebar.slider(
    "Select Year Range",
    int(df['Year'].min()),
    int(df['Year'].max()),
    (2000, 2023)
)

filtered_df = df[(df['Year'] >= year_range[0]) & (df['Year'] <= year_range[1])]

# ==============================
# 1. Number of Crashes Per Year
# ==============================
st.subheader("📈 Number of Crashes Per Year")
crashes_per_year = filtered_df.groupby('Year').size()

fig1, ax1 = plt.subplots()
crashes_per_year.plot(ax=ax1)
ax1.set_xlabel("Year")
ax1.set_ylabel("Number of Crashes")
st.pyplot(fig1)

# ==============================
# 2. Fatalities Per Year
# ==============================
st.subheader("💀 Fatalities Per Year")
fatalities_per_year = filtered_df.groupby('Year')['Fatalities (air)'].sum()

fig2, ax2 = plt.subplots()
fatalities_per_year.plot(ax=ax2, color='red')
ax2.set_xlabel("Year")
ax2.set_ylabel("Fatalities")
st.pyplot(fig2)

# ==============================
# 3. Top 10 Countries with Most Crashes
# ==============================
st.subheader("🌍 Top 10 Countries with Most Crashes")
top_countries = filtered_df['Country/Region'].value_counts().head(10)

fig3, ax3 = plt.subplots()
sns.barplot(x=top_countries.values, y=top_countries.index, ax=ax3)
ax3.set_xlabel("Number of Crashes")
ax3.set_ylabel("Country/Region")
st.pyplot(fig3)

# ==============================
# 4. Top 10 Deadliest Crashes
# ==============================
st.subheader("☠️ Top 10 Deadliest Crashes")
deadliest_crashes = filtered_df.sort_values(by='Fatalities (air)', ascending=False).head(10)
st.dataframe(
    deadliest_crashes[['Year', 'Operator', 'Aircraft', 'Country/Region', 'Fatalities (air)']]
)

# ==============================
# 5. Most Common Aircraft Types in Crashes
# ==============================
st.subheader("✈️ Most Common Aircraft Types in Crashes")
top_aircraft = filtered_df['Aircraft'].value_counts().head(10)

fig4, ax4 = plt.subplots()
sns.barplot(x=top_aircraft.values, y=top_aircraft.index, ax=ax4)
ax4.set_xlabel("Number of Crashes")
ax4.set_ylabel("Aircraft Type")
st.pyplot(fig4)

# ==============================
# 6. Aboard vs Fatalities
# ==============================
st.subheader("👥 Number of People Aboard vs Fatalities")
fig5, ax5 = plt.subplots()
sns.scatterplot(
    data=filtered_df,
    x='Aboard',
    y='Fatalities (air)',
    ax=ax5
)
ax5.set_xlabel("Number of People Aboard")
ax5.set_ylabel("Fatalities")
st.pyplot(fig5)

# ==============================
# 7. Interactive Map of Crashes
# ==============================
st.subheader("🗺️ Interactive Map of Crashes")

# Make sure your CSV has 'Latitude' and 'Longitude' columns
map_df = filtered_df.dropna(subset=['Latitude', 'Longitude'])

if not map_df.empty:
    st.map(map_df[['Latitude', 'Longitude']])
else:
    st.write("No geographic data available for the selected year range.")

# ==============================
# Footer
# ==============================
st.write("---")
st.write("Project by Damilola Komolafe | Python Project 2025")


