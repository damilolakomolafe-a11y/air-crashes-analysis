import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Air Crashes Analysis", layout="wide")

st.title("Air Crashes Analysis (1908-2023)")
st.write("An interactive analysis of global air crash data.")

@st.cache_data
def load_data():
 df = pd.read_csv("Data/air_crashes.csv")

    df['Year'] = pd.to_numeric(df['Year'], errors='coerce')
    df['Fatalities (air)'] = pd.to_numeric(df['Fatalities (air)'], errors='coerce').fillna(0)
    df['Aboard'] = pd.to_numeric(df['Aboard'], errors='coerce').fillna(0)
    
    df['Country/Region'] = df['Country/Region'].fillna("Unknown")
    df['Aircraft'] = df['Aircraft'].fillna("Unknown")
    
    return df

df = load_data()

# Sidebar filter
st.sidebar.header("Filter Data")
min_year = int(df['Year'].min())
max_year = int(df['Year'].max())

year_range = st.sidebar.slider(
    "Select Year Range",
    min_year,
    max_year,
    (min_year, max_year)
)

filtered_df = df[(df['Year'] >= year_range[0]) & (df['Year'] <= year_range[1])]

# Summary metrics
col1, col2, col3 = st.columns(3)
col1.metric("Total Crashes", len(filtered_df))
col2.metric("Total Fatalities", int(filtered_df['Fatalities (air)'].sum()))
col3.metric("Total Passengers Aboard", int(filtered_df['Aboard'].sum()))

st.markdown("---")

# Crashes per year
crashes_per_year = filtered_df.groupby("Year").size()

st.subheader("Number of Crashes Per Year")
fig, ax = plt.subplots(figsize=(10,5))
crashes_per_year.plot(ax=ax, color='tomato', marker='o')
ax.set_xlabel("Year")
ax.set_ylabel("Number of Crashes")
ax.set_title("Air Crashes Per Year")
st.pyplot(fig)

st.write("""
Observation:
Air crashes increased significantly during the mid-20th century 
and gradually reduced in recent decades due to improved aviation safety.
""")

# Top Countries
st.subheader("Top 10 Countries with Most Crashes")
top_countries = filtered_df['Country/Region'].value_counts().head(10)

fig2, ax2 = plt.subplots(figsize=(10,5))
top_countries.plot(kind='bar', ax=ax2, color='skyblue')
ax2.set_xlabel("Country")
ax2.set_ylabel("Number of Crashes")
ax2.set_title("Top 10 Countries by Air Crashes")
plt.xticks(rotation=45)
st.pyplot(fig2)

# Relationship Between Crashes and Fatalities
st.subheader("Relationship Between Crashes and Fatalities")

fatalities_per_year = filtered_df.groupby("Year")['Fatalities (air)'].sum()

# Ensure indices align
relationship_df = pd.DataFrame({
    'Crashes': crashes_per_year,
    'Fatalities': fatalities_per_year
}).dropna()

fig3, ax3 = plt.subplots(figsize=(8,5))
ax3.scatter(relationship_df['Crashes'], relationship_df['Fatalities'], color='green', alpha=0.6)
ax3.set_xlabel("Number of Crashes")
ax3.set_ylabel("Total Fatalities")
ax3.set_title("Crashes vs Fatalities")
st.pyplot(fig3)

st.write("""
Observation:
There is a positive relationship between crash frequency and total fatalities.
Years with more crashes tend to record higher fatalities.
""")

st.markdown("---")
st.write("Developed by Damilola Fasanmi | 2025")
