
import streamlit as st
import pandas as pd

# Title
st.title("MLB DraftKings Optimizer")

# Sample DataFrame - in real use, replace with projections from a live or uploaded source
sample_data = {
    "Player": ["Mike Trout", "Aaron Judge", "Shohei Ohtani", "Mookie Betts", "Freddie Freeman", "Ronald Acuña Jr."],
    "Team": ["LAA", "NYY", "LAA", "LAD", "LAD", "ATL"],
    "Position": ["OF", "OF", "UTIL", "OF", "1B", "OF"],
    "Salary": [5800, 6100, 6200, 6000, 5900, 6300],
    "Projection": [10.2, 11.4, 12.0, 10.8, 10.5, 12.3]
}

df = pd.DataFrame(sample_data)

# Show data
st.subheader("Available Players")
st.dataframe(df)

# Optimization: select top players under $50,000 salary cap
salary_cap = 50000
df_sorted = df.sort_values(by="Projection", ascending=False)

lineup = []
total_salary = 0

for _, row in df_sorted.iterrows():
    if total_salary + row["Salary"] <= salary_cap:
        lineup.append(row)
        total_salary += row["Salary"]

lineup_df = pd.DataFrame(lineup)

# Show lineup
st.subheader("Optimal Lineup")
st.dataframe(lineup_df)

# Download button
csv = lineup_df.to_csv(index=False).encode("utf-8")
st.download_button("Download Lineup as CSV", csv, "optimal_lineup.csv", "text/csv")
