import streamlit as st
import http.client
import json
import math
import pandas as pd

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------
st.set_page_config(page_title="Live Matches", layout="wide")
st.title("🏏 Live Cricket Matches")
st.caption("Select a match to view live score & scorecard")
st.markdown("---")

# -------------------------------------------------
# API CONFIG
# -------------------------------------------------
HOST = "cricbuzz-cricket.p.rapidapi.com"
API_KEY = "d1d1206e78mshb418f1da663697ap109e25jsn86275d1f5944"

HEADERS = {
    "x-rapidapi-key": API_KEY,
    "x-rapidapi-host": HOST
}

# -------------------------------------------------
# FETCH LIVE MATCHES
# -------------------------------------------------
conn = http.client.HTTPSConnection(HOST)
conn.request("GET", "/matches/v1/live", headers=HEADERS)
res = conn.getresponse()
data = json.loads(res.read().decode("utf-8"))

# -------------------------------------------------
# PARSE MATCHES
# -------------------------------------------------
matches = []

for mt in data.get("typeMatches", []):
    for series in mt.get("seriesMatches", []):
        if "seriesAdWrapper" not in series:
            continue

        series_data = series["seriesAdWrapper"]
        series_name = series_data.get("seriesName", "Unknown Series")

        for match in series_data.get("matches", []):
            info = match.get("matchInfo", {})
            if "team1" not in info or "team2" not in info:
                continue

            state = info.get("stateTitle", "").lower()
            if state in ["complete", "abandon", "abandoned"]:
                continue

            label = f"{info['team1']['teamName']} vs {info['team2']['teamName']} ({info.get('matchDesc','')})"

            matches.append({
                "label": label,
                "match_id": info["matchId"],
                "info": info,
                "score": match.get("matchScore", {}),
                "series": series_name
            })

if not matches:
    st.warning("No live or ongoing matches available.")
    st.stop()

# -------------------------------------------------
# DROPDOWN
# -------------------------------------------------
selected_label = st.selectbox(
    "🎯 Select a match",
    [m["label"] for m in matches]
)

selected = next(m for m in matches if m["label"] == selected_label)
info = selected["info"]
score = selected["score"]

# -------------------------------------------------
# MATCH META INFO
# -------------------------------------------------
st.markdown("### 🏟 Match Details")

meta_col1, meta_col2, meta_col3 = st.columns(3)

with meta_col1:
    st.write(f"**Series:** {selected['series']}")
    st.write(f"**Format:** {info.get('matchFormat')}")

with meta_col2:
    venue = info.get("venueInfo", {})
    st.write(f"**Venue:** {venue.get('ground')}")
    st.write(f"**City:** {venue.get('city')}")

with meta_col3:
    st.write(f"**Status:** {info.get('stateTitle')}")
    st.write(f"**Match Info:** {info.get('status')}")

st.markdown("---")

# -------------------------------------------------
# BIG SCORE DISPLAY
# -------------------------------------------------
st.markdown("## 📊 Live Score")

score_cols = st.columns(2)

def display_score(team_key, col):
    if team_key in score:
        inng = score[team_key].get("inngs1", {})
        runs = inng.get("runs", 0)
        wkts = inng.get("wickets", 0)
        overs = inng.get("overs", 0)
        rr = round(runs / overs, 2) if overs else 0

        col.metric(
            label=info[team_key.replace("Score", "")]["teamName"],
            value=f"{runs}/{wkts}",
            delta=f"{overs} overs | RR {rr}"
        )

display_score("team1Score", score_cols[0])
display_score("team2Score", score_cols[1])

st.markdown("---")

# -------------------------------------------------
# FETCH SCORECARD
# -------------------------------------------------
conn = http.client.HTTPSConnection(HOST)
conn.request("GET", f"/mcenter/v1/{selected['match_id']}/hscard", headers=HEADERS)
res = conn.getresponse()
scorecard_data = json.loads(res.read().decode("utf-8"))

if "scorecard" not in scorecard_data:
    st.info("Scorecard not available yet.")
    st.stop()

# -------------------------------------------------
# RUN PROGRESS (APPROX RUN WORM)
# -------------------------------------------------
st.markdown("## 📈 Run Progress (Approx)")

innings = scorecard_data["scorecard"][0]
total_runs = innings["score"]
total_overs = innings["overs"]

overs_list = list(range(1, math.ceil(total_overs) + 1))
runs_per_over = total_runs / total_overs
run_progress = [round(runs_per_over * o, 1) for o in overs_list]

df = pd.DataFrame({
    "Over": overs_list,
    "Runs": run_progress
})

st.line_chart(df, x="Over", y="Runs")

st.caption("Note: This is an approximate run progression based on current run rate.")

st.markdown("---")

# -------------------------------------------------
# SCORECARD DETAILS
# -------------------------------------------------
st.markdown("## 🏏 Detailed Scorecard")

for idx, inns in enumerate(scorecard_data["scorecard"], start=1):

    with st.expander(
        f"Innings {idx} — {inns['batteamname']} "
        f"{inns['score']}/{inns['wickets']} ({inns['overs']} overs)",
        expanded=(idx == 1)
    ):

        tab1, tab2 = st.tabs(["🏏 Batting", "🎯 Bowling"])

        with tab1:
            batting = [{
                "Batsman": b["name"],
                "R": b["runs"],
                "B": b["balls"],
                "4s": b["fours"],
                "6s": b["sixes"],
                "SR": b["strkrate"],
                "Dismissal": b["outdec"]
            } for b in inns["batsman"]]

            st.dataframe(batting, use_container_width=True, hide_index=True)

        with tab2:
            bowling = [{
                "Bowler": b["name"],
                "Overs": b["overs"],
                "Runs": b["runs"],
                "Wkts": b["wickets"],
                "Eco": b["economy"]
            } for b in inns["bowler"]]

            st.dataframe(bowling, use_container_width=True, hide_index=True)