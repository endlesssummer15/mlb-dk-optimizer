import streamlit as st
import pandas as pd

st.title("Daily MLB DraftKings Optimizer (Auto Mode)")

@st.cache_data
def load_sample_projections():
    hitters = pd.DataFrame({
        "Player": ["Aaron Judge", "Shohei Ohtani", "Ronald Acuña Jr.", "Freddie Freeman", "Mookie Betts"],
        "Team": ["NYY", "LAA", "ATL", "LAD", "LAD"],
        "Position": ["OF", "UTIL", "OF", "1B", "OF"],
        "Salary": [6100, 6200, 6300, 5900, 6000],
        "Projection": [12.4, 12.0, 11.7, 11.2, 10.8]
    })

    pitchers = pd.DataFrame({
        "Player": ["Gerrit Cole", "Zac Gallen", "Corbin Burnes", "Logan Webb", "Max Fried"],
        "Team": ["NYY", "ARI", "BAL", "SFG", "ATL"],
        "Position": ["P", "P", "P", "P", "P"],
        "Salary": [10300, 9700, 9800, 9400, 9100],
        "Projection": [19.5, 18.2, 17.9, 17.6, 17.2]
    })

    return hitters, pitchers

hitters, pitchers = load_sample_projections()

st.subheader("Auto-Pulled Hitter Projections")
st.dataframe(hitters)

st.subheader("Auto-Pulled Pitcher Projections")
st.dataframe(pitchers)

combined = pd.concat([hitters, pitchers], ignore_index=True)
combined_sorted = combined.sort_values(by="Projection", ascending=False)

salary_cap = 50000
lineup = []
total_salary = 0
pitcher_added = False

for _, row in combined_sorted.iterrows():
    if total_salary + row["Salary"] > salary_cap:
        continue
    if row["Position"] == "P":
        if not pitcher_added:
            lineup.append(row)
            total_salary += row["Salary"]
            pitcher_added = True
    else:
        lineup.append(row)
        total_salary += row["Salary"]
    if len(lineup) == 9:
        break

lineup_df = pd.DataFrame(lineup)

st.subheader("✅ Optimized DraftKings Lineup")
st.dataframe(lineup_df)

csv = lineup_df.to_csv(index=False).encode("utf-8")
st.download_button("Download CSV", csv, "dk_optimizer_lineup.csv", "text/csv")
