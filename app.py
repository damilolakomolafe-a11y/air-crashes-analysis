import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Page configuration
st.set_page_config(page_title="Air Crashes Analysis", layout="wide")

st.title("✈ Air Crashes Analysis (1908 – 2023)")
st.write("An interactive analysis of global air crash data.")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("data/Air_Crashes_Full_Data.csv")
    return df

df = load_data()

# Data Cleaning
df['Fatalities (air)'] = df['Fatalities (air)'].fillna(0)
df['Aboard'] = df['Aboard'].fillna(0)
df = df.dropna(subset=['Year'])
df['Year'] = df['Year'].astype(int)

# Sidebar Filters
st.sidebar.header("Filter Data")

year_range = st.sidebar.slider(
    "Select Year Range",
    int(df['Year'].min()),
    int(df['Year'].max()),
    (2000, 2023)
)

filtered_df = df[(df['Year'] >= year_range[0]) & (df['Year'] <= year_range[1])]

# ==============================
# 1. Crashes Per Year
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
fatalities_per_year.plot(ax=ax2)
ax2.set_xlabel("Year")
ax2.set_ylabel("Fatalities")

st.pyplot(fig2)

# ==============================
# 3. Top 10 Countries
# ==============================

st.subheader("🌍 Top 10 Countries with Most Crashes")

top_countries = filtered_df['Country/Region'].value_counts().head(10)

fig3, ax3 = plt.subplots()
sns.barplot(x=top_countries.values, y=top_countries.index, ax=ax3)

st.pyplot(fig3)

# ==============================
# 4. Aboard vs Fatalities
# ==============================

st.subheader("👥 Aboard vs Fatalities")

fig4, ax4 = plt.subplots()
sns.scatterplot(
    data=filtered_df,
    x='Aboard',
    y='Fatalities (air)',
    ax=ax4
)

st.pyplot(fig4)

# ==============================
# Footer
# ==============================

st.write("---")
st.write("Project by Damilola Komolafe | Python Project 2025")



