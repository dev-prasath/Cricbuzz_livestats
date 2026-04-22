import streamlit as st
import http.client
import json
import pandas as pd

# PAGE CONFIG
st.set_page_config(page_title="Player Stats", layout="wide")
st.title("👤 Player Statistics")
st.caption("Search a player and view career batting & bowling stats")
st.markdown("---")

# API CONFIG
HOST = "cricbuzz-cricket.p.rapidapi.com"
API_KEY = "2767392619mshf3f20e34f8b3117p1ddd4fjsnb30bd89e03ed"

HEADERS = {
    "x-rapidapi-key": API_KEY,
    "x-rapidapi-host": HOST
}

# SAFE STATS PARSER
def parse_stats(data):
    if not isinstance(data, dict):
        return None

    if "values" not in data or not data["values"]:
        return None

    if "headers" in data and len(data["headers"]) > 1:
        columns = data["headers"][1:]
    else:
        col_count = len(data["values"][0]["values"]) - 1
        columns = [f"Format {i+1}" for i in range(col_count)]

    rows = []
    for row in data["values"]:
        vals = row.get("values", [])
        if len(vals) < 2:
            continue
        rows.append([vals[0]] + vals[1:])

    if not rows:
        return None

    df = pd.DataFrame(rows, columns=["Stat"] + columns)
    df.set_index("Stat", inplace=True)
    return df

# PLAYER SEARCH INPUT
player_name = st.text_input(
    "🔍 Search player by name",
    placeholder="e.g. Virat Kohli, KL Rahul"
)

if not player_name:
    st.info("Please enter a player name to search.")
    st.stop()

# SEARCH PLAYER API
try:
    conn = http.client.HTTPSConnection(HOST, timeout=10)
    conn.request(
        "GET",
        f"/stats/v1/player/search?plrN={player_name}",
        headers=HEADERS
    )
    res = conn.getresponse()
    search_data = json.loads(res.read().decode("utf-8"))
except Exception:
    st.error("Failed to connect to player search service.")
    st.stop()

players = search_data.get("player", [])

# ❌ NO PLAYER FOUND
if not players:
    st.warning(f"No players found for '{player_name}'.")
    st.stop()

# PLAYER SELECTION
player_map = {
    f"{p['name']} ({p.get('teamName','')})": p["id"]
    for p in players
}

selected_player = st.selectbox(
    "🎯 Select player",
    list(player_map.keys())
)

player_id = player_map[selected_player]

st.markdown("---")

# FETCH PLAYER PROFILE
try:
    conn = http.client.HTTPSConnection(HOST, timeout=10)
    conn.request("GET", f"/stats/v1/player/{player_id}", headers=HEADERS)
    res = conn.getresponse()
    profile = json.loads(res.read().decode("utf-8"))
except Exception:
    st.error("Unable to fetch player profile.")
    st.stop()

# PLAYER OVERVIEW
st.markdown("## 🧾 Player Overview")

c1, c2, c3 = st.columns(3)

with c1:
    st.metric("Name", profile.get("name", "N/A"))
    st.metric("Country", profile.get("intlTeam", "N/A"))

with c2:
    st.metric("Role", profile.get("role", "N/A"))
    st.metric("Batting Style", profile.get("bat", "N/A"))

with c3:
    st.metric("Bowling Style", profile.get("bowl", "N/A"))
    st.metric("DOB", profile.get("DoBFormat", "N/A"))

st.markdown("---")

# FETCH & DISPLAY BATTING STATS
st.markdown("## 🏏 Batting Career Stats")

try:
    conn = http.client.HTTPSConnection(HOST, timeout=10)
    conn.request("GET", f"/stats/v1/player/{player_id}/batting", headers=HEADERS)
    res = conn.getresponse()
    batting_data = json.loads(res.read().decode("utf-8"))

    bat_df = parse_stats(batting_data)
    if bat_df is None:
        st.info("Batting statistics not available for this player.")
    else:
        st.dataframe(bat_df, use_container_width=True)

except Exception:
    st.error("Failed to fetch batting statistics.")

st.markdown("---")

# FETCH & DISPLAY BOWLING STATS
st.markdown("## 🎯 Bowling Career Stats")

try:
    conn = http.client.HTTPSConnection(HOST, timeout=10)
    conn.request("GET", f"/stats/v1/player/{player_id}/bowling", headers=HEADERS)
    res = conn.getresponse()
    bowling_data = json.loads(res.read().decode("utf-8"))

    bowl_df = parse_stats(bowling_data)
    if bowl_df is None:
        st.info("Bowling statistics not available for this player.")
    else:
        st.dataframe(bowl_df, use_container_width=True)

except Exception:
    st.error("Failed to fetch bowling statistics.")