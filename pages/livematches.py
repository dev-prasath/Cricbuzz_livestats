import streamlit as st
import http.client
import json
import math
import pandas as pd

# PAGE CONFIG
st.set_page_config(page_title="Cricket Matches", layout="wide")
st.title("🏏 Live & Recent Cricket Matches")
st.caption("Live matches shown first. If none, recent matches will appear.")
st.markdown("---")

# API CONFIG
HOST = "cricbuzz-cricket.p.rapidapi.com"
API_KEY = "2767392619mshf3f20e34f8b3117p1ddd4fjsnb30bd89e03ed"  

HEADERS = {
    "x-rapidapi-key": API_KEY,
    "x-rapidapi-host": HOST
}

# FETCH FUNCTION
def fetch_matches(endpoint):
    try:
        conn = http.client.HTTPSConnection(HOST)
        conn.request("GET", endpoint, headers=HEADERS)
        res = conn.getresponse()

        raw = res.read().decode("utf-8")

        if not raw or raw.strip() == "":
            return {}

        return json.loads(raw)

    except json.JSONDecodeError:
        # Happens when API returns non-JSON
        return {}

    except Exception:
        return {}
# PARSE FUNCTION (FIXED)
def parse_matches(data, include_completed=False):
    matches = []

    for mt in data.get("typeMatches", []):
        for series in mt.get("seriesMatches", []):

            wrapper = series.get("seriesAdWrapper")
            if not wrapper:
                continue

            series_name = wrapper.get("seriesName", "Unknown Series")

            for match in wrapper.get("matches", []):
                info = match.get("matchInfo")

                if not info:
                    continue

                team1 = info.get("team1")
                team2 = info.get("team2")

                if not team1 or not team2:
                    continue

                state = info.get("state", "").lower()

                # 🔴 LIVE FILTER
                if not include_completed:
                    if state not in ["in progress", "live"]:
                        continue

                label = f"{team1.get('teamName')} vs {team2.get('teamName')} ({info.get('matchDesc','')})"

                matches.append({
                    "label": label,
                    "match_id": info.get("matchId"),
                    "info": info,
                    "score": match.get("matchScore", {}),
                    "series": series_name,
                    "status": info.get("status", "")
                })

    return matches

# STEP 1: LIVE MATCHES
live_data = fetch_matches("/matches/v1/live")
matches = parse_matches(live_data, include_completed=False)

# STEP 2: FALLBACK TO RECENT
if not matches:
    st.warning("⚠ No live matches. Showing recent matches instead.")

    recent_data = fetch_matches("/matches/v1/recent")
    matches = parse_matches(recent_data, include_completed=True)

# FINAL CHECK
if not matches:
    st.error("❌ No matches available. Check API key or quota.")
    st.stop()

# SELECT MATCH
selected_label = st.selectbox(
    "🎯 Select a match",
    [m["label"] for m in matches]
)

selected = next(m for m in matches if m["label"] == selected_label)
info = selected["info"]
score = selected["score"]

# MATCH DETAILS
st.markdown("### 🏟 Match Details")

col1, col2, col3 = st.columns(3)

with col1:
    st.write(f"**Series:** {selected['series']}")
    st.write(f"**Format:** {info.get('matchFormat')}")

with col2:
    venue = info.get("venueInfo", {})
    st.write(f"**Venue:** {venue.get('ground')}")
    st.write(f"**City:** {venue.get('city')}")

with col3:
    st.write(f"**Status:** {selected['status']}")
    st.write(f"**Info:** {info.get('status')}")

st.markdown("---")

# SCORE DISPLAY
st.markdown("## 📊 Match Score")

cols = st.columns(2)

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

display_score("team1Score", cols[0])
display_score("team2Score", cols[1])

st.markdown("---")

# FETCH SCORECARD
try:
    conn = http.client.HTTPSConnection(HOST)
    conn.request("GET", f"/mcenter/v1/{selected['match_id']}/hscard", headers=HEADERS)
    res = conn.getresponse()
    scorecard_data = json.loads(res.read().decode("utf-8"))
except:
    st.info("Scorecard not available.")
    st.stop()

if "scorecard" not in scorecard_data:
    st.info("Scorecard not available.")
    st.stop()

# RUN PROGRESS
import altair as alt

st.markdown("## 📈 Run Progress Comparison")

scorecards = scorecard_data.get("scorecard", [])

chart_data = []

for inns in scorecards[:2]:
    team_name = inns.get("batteamname", "Team")
    total_runs = inns.get("score", 0)
    total_overs = inns.get("overs", 0)

    if not total_overs or total_overs == 0:
        continue

    overs_list = list(range(1, math.ceil(total_overs) + 1))
    runs_per_over = total_runs / total_overs

    run_progress = [round(runs_per_over * o, 1) for o in overs_list]

    for over, runs in zip(overs_list, run_progress):
        chart_data.append({
            "Over": over,
            "Runs": runs,
            "Team": team_name
        })

if chart_data:
    df = pd.DataFrame(chart_data)

    chart = alt.Chart(df).mark_line(
        interpolate='monotone'   # 🔥 THIS MAKES IT CURVED
    ).encode(
        x='Over:Q',
        y='Runs:Q',
        color='Team:N',
        tooltip=['Team', 'Over', 'Runs']
    ).properties(
        height=400
    )

    st.altair_chart(chart, use_container_width=True)

    st.caption("Smoothed run progression comparison between teams.")
else:
    st.info("Not enough data for chart.")
# SCORECARD TABLE
st.markdown("## 🏏 Detailed Scorecard")

for idx, inns in enumerate(scorecard_data["scorecard"], start=1):

    with st.expander(
        f"Innings {idx} — {inns.get('batteamname')} "
        f"{inns.get('score')}/{inns.get('wickets')} ({inns.get('overs')} overs)",
        expanded=(idx == 1)
    ):

        tab1, tab2 = st.tabs(["Batting", "Bowling"])

        with tab1:
            batting = [{
                "Batsman": b.get("name"),
                "Runs": b.get("runs"),
                "Balls": b.get("balls"),
                "4s": b.get("fours"),
                "6s": b.get("sixes"),
                "SR": b.get("strkrate")
            } for b in inns.get("batsman", [])]

            st.dataframe(batting, use_container_width=True)

        with tab2:
            bowling = [{
                "Bowler": b.get("name"),
                "Overs": b.get("overs"),
                "Runs": b.get("runs"),
                "Wickets": b.get("wickets"),
                "Economy": b.get("economy")
            } for b in inns.get("bowler", [])]

            st.dataframe(bowling, use_container_width=True)