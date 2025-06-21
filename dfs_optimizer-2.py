
import streamlit as st
import pandas as pd
import numpy as np
from pulp import LpMaximize, LpProblem, lpSum, LpVariable

# -------------------------------
# Sample auto-generated projections (placeholder)
# -------------------------------
data = [
    {"Name": "Player A", "Position": "1B", "Team": "BOS", "Salary": 4800, "Proj_Points": 11.2},
    {"Name": "Player B", "Position": "2B", "Team": "BOS", "Salary": 4500, "Proj_Points": 10.5},
    {"Name": "Player C", "Position": "3B", "Team": "LAD", "Salary": 5000, "Proj_Points": 12.1},
    {"Name": "Player D", "Position": "SS", "Team": "LAD", "Salary": 4700, "Proj_Points": 9.8},
    {"Name": "Player E", "Position": "OF", "Team": "LAD", "Salary": 5200, "Proj_Points": 10.2},
    {"Name": "Player F", "Position": "OF", "Team": "ATL", "Salary": 5100, "Proj_Points": 11.0},
    {"Name": "Player G", "Position": "OF", "Team": "ATL", "Salary": 4900, "Proj_Points": 9.5},
    {"Name": "Player H", "Position": "C",  "Team": "ATL", "Salary": 4300, "Proj_Points": 8.9},
    {"Name": "Player I", "Position": "P",  "Team": "NYY", "Salary": 9800, "Proj_Points": 18.5},
    {"Name": "Player J", "Position": "P",  "Team": "HOU", "Salary": 9200, "Proj_Points": 17.8},
]
df = pd.DataFrame(data)

# -------------------------------
# Streamlit App
# -------------------------------
st.title("DraftKings MLB DFS Optimizer - 1 Optimal Lineup")

st.write("### Auto-Generated Projections")
st.dataframe(df)

# Create optimizer problem
prob = LpProblem("DK_MLB_Optimizer", LpMaximize)

# Variables for player inclusion
vars = {row.Name: LpVariable(row.Name, cat='Binary') for idx, row in df.iterrows()}

# Objective: Maximize total projected points
prob += lpSum(vars[row.Name] * row.Proj_Points for idx, row in df.iterrows())

# Constraint: Salary cap
prob += lpSum(vars[row.Name] * row.Salary for idx, row in df.iterrows()) <= 50000

# Constraint: Positional requirements
positions = {
    'P': 2,
    'C': 1,
    '1B': 1,
    '2B': 1,
    '3B': 1,
    'SS': 1,
    'OF': 3
}

for pos, required in positions.items():
    prob += lpSum(vars[row.Name] for idx, row in df.iterrows() if row.Position == pos) == required

# Constraint: Max 5 players from same team
teams = df['Team'].unique()
for team in teams:
    prob += lpSum(vars[row.Name] for idx, row in df.iterrows() if row.Team == team) <= 5

# Solve the problem
prob.solve()

# Display optimal lineup
selected_players = [row for row in data if vars[row['Name']].varValue == 1]

st.write("### Optimal Lineup")
st.table(pd.DataFrame(selected_players))

# Download option
output_df = pd.DataFrame(selected_players)
output_csv = output_df.to_csv(index=False).encode('utf-8')
st.download_button("Download Lineup as CSV", output_csv, "optimal_lineup.csv", "text/csv")
