import streamlit as st
import pandas as pd
import plotly.express as px

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="IPL Head-to-Head Dashboard",
    page_icon="🏏",
    layout="wide"
)

# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------
st.markdown("""
<style>
    .main {
        background-color: #f5f7fb;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    .title {
        font-size: 42px;
        font-weight: 800;
        text-align: center;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        color: #6b7280;
        font-size: 17px;
        margin-bottom: 30px;
    }

    .metric-card {
        background: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 3px 12px rgba(0,0,0,0.08);
        text-align: center;
    }

    .metric-title {
        color: #6b7280;
        font-size: 15px;
    }

    .metric-value {
        font-size: 30px;
        font-weight: 800;
        margin-top: 5px;
    }

    .section-title {
        font-size: 24px;
        font-weight: 700;
        margin-top: 25px;
        margin-bottom: 15px;
    }
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# LOAD CSV
# --------------------------------------------------
df = pd.read_excel("matches.xlsx")

# Remove accidental spaces from column names
df.columns = df.columns.str.strip()

# --------------------------------------------------
# CLEAN TEAM / WINNER DATA
# --------------------------------------------------
for col in ["team1", "team2", "winner"]:
    df[col] = df[col].astype(str).str.strip()

# Remove rows where winner is missing/invalid
df = df[
    df["winner"].notna() &
    (df["winner"] != "") &
    (df["winner"].str.lower() != "nan")
]

# --------------------------------------------------
# GET ALL TEAMS
# --------------------------------------------------
teams = sorted(
    set(df["team1"].dropna().unique()) |
    set(df["team2"].dropna().unique())
)

# --------------------------------------------------
# HEADER
# --------------------------------------------------
st.markdown(
    '<div class="title">🏏 IPL Head-to-Head Dashboard</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">IPL Match Analysis • 2008 – 2024</div>',
    unsafe_allow_html=True
)

# --------------------------------------------------
# TEAM SELECTION
# --------------------------------------------------
col1, col2 = st.columns(2)

with col1:
    selected_team = st.selectbox(
        "🏏 Select Team",
        teams
    )

# Opponents for selected team
opponents = [
    team for team in teams
    if team != selected_team
]

with col2:
    selected_opponent = st.selectbox(
        "⚔️ Select Opponent",
        ["All Opponents"] + opponents
    )

# --------------------------------------------------
# CREATE HEAD-TO-HEAD DATA
# --------------------------------------------------

# Matches where selected team participated
team_matches = df[
    (df["team1"] == selected_team) |
    (df["team2"] == selected_team)
].copy()

# Find opponent for every match
team_matches["opponent"] = team_matches.apply(
    lambda row:
        row["team2"]
        if row["team1"] == selected_team
        else row["team1"],
    axis=1
)

# --------------------------------------------------
# SELECTED OPPONENT
# --------------------------------------------------
if selected_opponent != "All Opponents":

    h2h = team_matches[
        team_matches["opponent"] == selected_opponent
    ]

    wins = (h2h["winner"] == selected_team).sum()

    losses = (
        (h2h["winner"] == selected_opponent)
    ).sum()

    total_matches = len(h2h)

    win_percentage = (
        (wins / total_matches) * 100
        if total_matches > 0
        else 0
    )

    # --------------------------------------------------
    # METRIC CARDS
    # --------------------------------------------------
    st.markdown(
        '<div class="section-title">📊 Head-to-Head Record</div>',
        unsafe_allow_html=True
    )

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">Total Matches</div>
                <div class="metric-value">{total_matches}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c2:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">🏆 Wins</div>
                <div class="metric-value">{wins}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c3:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">❌ Losses</div>
                <div class="metric-value">{losses}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c4:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">Win %</div>
                <div class="metric-value">{win_percentage:.1f}%</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # --------------------------------------------------
    # CHART
    # --------------------------------------------------
    chart_data = pd.DataFrame({
        "Result": ["Wins", "Losses"],
        "Matches": [wins, losses]
    })

    fig = px.bar(
        chart_data,
        x="Result",
        y="Matches",
        text="Matches",
        title=f"{selected_team} vs {selected_opponent}",
        template="plotly_white"
    )

    fig.update_traces(
        textposition="outside"
    )

    fig.update_layout(
        height=450,
        showlegend=False,
        title_x=0.5
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# --------------------------------------------------
# ALL OPPONENTS
# --------------------------------------------------
else:

    summary = []

    for opponent in opponents:

        matches = team_matches[
            team_matches["opponent"] == opponent
        ]

        wins = (
            matches["winner"] == selected_team
        ).sum()

        losses = (
            matches["winner"] == opponent
        ).sum()

        total = len(matches)

        win_percentage = (
            (wins / total) * 100
            if total > 0
            else 0
        )

        summary.append({
            "Team": selected_team,
            "Opponent": opponent,
            "Matches": total,
            "Wins": wins,
            "Losses": losses,
            "Win %": round(win_percentage, 1)
        })

    summary_df = pd.DataFrame(summary)

    # --------------------------------------------------
    # TOTAL STATS
    # --------------------------------------------------
    total_matches = len(team_matches)

    total_wins = (
        team_matches["winner"] == selected_team
    ).sum()

    total_losses = (
        team_matches["winner"] != selected_team
    ).sum()

    overall_win_percentage = (
        (total_wins / total_matches) * 100
        if total_matches > 0
        else 0
    )

    st.markdown(
        '<div class="section-title">📊 Overall Performance</div>',
        unsafe_allow_html=True
    )

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">Total Matches</div>
                <div class="metric-value">{total_matches}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c2:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">🏆 Total Wins</div>
                <div class="metric-value">{total_wins}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c3:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">❌ Total Losses</div>
                <div class="metric-value">{total_losses}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c4:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">Win %</div>
                <div class="metric-value">{overall_win_percentage:.1f}%</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # --------------------------------------------------
    # TABLE
    # --------------------------------------------------
    st.markdown(
        '<div class="section-title">⚔️ Team vs Opponent</div>',
        unsafe_allow_html=True
    )

    st.dataframe(
        summary_df,
        use_container_width=True,
        hide_index=True
    )

    # --------------------------------------------------
    # WINS CHART
    # --------------------------------------------------
    st.markdown(
        '<div class="section-title">🏆 Wins Against Each Opponent</div>',
        unsafe_allow_html=True
    )

    wins_chart = summary_df.sort_values(
        "Wins",
        ascending=False
    )

    fig = px.bar(
        wins_chart,
        x="Opponent",
        y="Wins",
        text="Wins",
        title=f"{selected_team} - Wins Against Opponents",
        template="plotly_white"
    )

    fig.update_traces(
        textposition="outside"
    )

    fig.update_layout(
        height=500,
        title_x=0.5
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # --------------------------------------------------
    # LOSSES CHART
    # --------------------------------------------------
    st.markdown(
        '<div class="section-title">❌ Losses Against Each Opponent</div>',
        unsafe_allow_html=True
    )

    losses_chart = summary_df.sort_values(
        "Losses",
        ascending=False
    )

    fig2 = px.bar(
        losses_chart,
        x="Opponent",
        y="Losses",
        text="Losses",
        title=f"{selected_team} - Losses Against Opponents",
        template="plotly_white"
    )

    fig2.update_traces(
        textposition="outside"
    )

    fig2.update_layout(
        height=500,
        title_x=0.5
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

# --------------------------------------------------
# FOOTER
# --------------------------------------------------
st.markdown("---")

st.markdown(
    """
    <div style="text-align:center; color:#6b7280;">
        🏏 IPL Head-to-Head Analytics Dashboard<br>
        Data: IPL 2008 – 2024
    </div>
    """,
    unsafe_allow_html=True
)
