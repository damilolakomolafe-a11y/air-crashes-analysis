AIR CRASHES ANALYSIS REPORT (1908–2023)
1. Introduction

This project analyzes global air crash data from 1908 to 2023 to identify historical trends, high-risk periods, aircraft patterns, geographical distribution, and the relationship between crash frequency and fatalities.

The objective is to uncover meaningful insights that can contribute to aviation safety awareness.

Dataset Information
Time Period: 1908–2023
Key Columns:
Year
Month
Day
Country/Region
Aircraft
Operator
Fatalities (air)
Aboard

2. Data Cleaning Process

The dataset was cleaned using the following steps:

Converted Month column from text to numeric format.

Combined Year, Month, and Day columns to create a proper Date column.

Removed rows with invalid dates.

Filled missing numerical values such as “Fatalities (air)” and “Aboard” with 0.

Replaced missing categorical values (Country, Aircraft, Operator) with “Unknown”.

Removed unnecessary temporary columns.

This ensured accurate time-based and statistical analysis.

3. Exploratory Data Analysis (EDA)
Research Question 1:

How has the number of air crashes changed over time?

Air crashes increased significantly between the 1940s and 1970s, likely due to expansion in global aviation. However, crashes have gradually reduced in recent decades due to improved aviation technology and regulations.

Research Question 2:

Which years recorded the highest number of crashes?

The years between the 1950s and early 1970s recorded the highest number of air crashes.

Research Question 3:

What are the deadliest air crashes in history?

The deadliest crashes involved large commercial aircraft and resulted in high fatality counts. These incidents often occurred during periods of rapid aviation expansion.

Research Question 4:

Which aircraft types are most frequently involved in crashes?

Certain aircraft types appear more frequently in crash records. However, this may reflect higher usage rather than lower safety.

Research Question 5:

Which locations experience the most crashes?

Some countries recorded more crashes than others. This may be influenced by:

Air traffic volume

Size of aviation industry

Reporting systems

Research Question 6:

Is there a relationship between year and number of fatalities?

There is a positive relationship between number of crashes and total fatalities per year.

Periods with more crashes generally recorded higher fatalities. However, modern aviation shows fewer crashes and lower fatality trends compared to mid-20th century data.

Key Findings;

Air crashes peaked during the mid-20th century.

Fatalities followed similar patterns to crash frequency.

Aviation safety has improved significantly in recent decades.

Aircraft frequency in crashes often reflects usage volume.

Recommendations;

Continue enforcing strict aviation safety regulations.

Improve aircraft maintenance monitoring systems.

Strengthen pilot training programs.

Encourage modernization of older aircraft fleets.

Invest in predictive safety analytics using data science.

Tools & Technologies Used
Python
Pandas
NumPy
Matplotlib
Seaborn
Jupyter Notebook
Streamlit

Project Structure;
Air-Crashes-Analysis-2025/
│
├── data/
│   └── air_crashes.csv
│
├── Notebook/
│   └── air_crash_analysis.ipynb
│
├── app.py
├── requirements.txt
└── README.md

