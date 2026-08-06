import streamlit as st
import pandas as pd

# Page Title
st.title("🏏 MI vs RCB Head-to-Head")

# CSV file load
df = pd.read_csv("matches.csv")

# Team names
mi = "Mumbai Indians"
rcb = "Royal Challengers Bangalore"

# MI vs RCB matches
matches = df[
    ((df["team1"] == mi) & (df["team2"] == rcb)) |
    ((df["team1"] == rcb) & (df["team2"] == mi))
]

# Total matches
total_matches = len(matches)

# Wins
mi_wins = len(matches[matches["winner"] == mi])
rcb_wins = len(matches[matches["winner"] == rcb])

# No Result
no_result = len(matches[matches["winner"].isna()])

# Display Results
st.subheader("Head-to-Head Statistics")

st.write(f"**Total Matches :** {total_matches}")
st.write(f"**Mumbai Indians Wins :** {mi_wins}")
st.write(f"**RCB Wins :** {rcb_wins}")
st.write(f"**No Result :** {no_result}")

# Optional: Show all MI vs RCB matches
st.subheader("Match Details")
st.dataframe(matches)