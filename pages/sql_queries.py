import streamlit as st
import pandas as pd
from utils.db_connection import get_connection

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="SQL Analytics", layout="wide")
st.title("🧮 SQL Analytics Dashboard")
st.markdown("---")

# -----------------------------
# DB CONNECTION
# -----------------------------
conn = get_connection()

# -----------------------------
# QUERY CONFIG
# -----------------------------
QUERY_CONFIG = {

    # ✅ FIXED Q1
    "Q1: Players from India": {
        "query": """
            SELECT 
                p.player_name,
                p.role,
                p.batting_style,
                p.bowling_style
            FROM players p
            JOIN teams t ON p.team_id = t.team_id
            WHERE LOWER(t.team_name) = 'india';
        """,
        "description": "Players representing India with role and styles."
    },

    # ✅ FIXED Q2 (NO VENUES TABLE)
    "Q2: Recent Matches": {
        "query": """
            SELECT 
                m.match_desc,
                t1.team_name AS team1,
                t2.team_name AS team2,
                m.venue,
                TO_CHAR(m.start_date, 'DD Mon YYYY, HH24:MI') AS match_time
            FROM matches m
            JOIN teams t1 ON m.team1_id = t1.team_id
            JOIN teams t2 ON m.team2_id = t2.team_id
            ORDER BY m.start_date DESC
            LIMIT 20;
        """,
        "description": "Recent matches with teams and venue."
    },

    # ✅ Q3 OK
    "Q3: Top 10 ODI Run Scorers": {
        "query": """
            SELECT 
                player_name,
                runs,
                batting_average,
                rank_position
            FROM top_run_scorers
            WHERE format_type = 'ODI'
            ORDER BY runs DESC
            LIMIT 10;
        """,
        "description": "Top 10 highest run scorers in ODI cricket."
    },

    # ✅ Q4 OK
    "Q4: Large Capacity Venues": {
        "query": """
            SELECT 
                venue_name,
                city,
                country,
                capacity
            FROM venues
            WHERE capacity > 25000
            ORDER BY capacity DESC
            LIMIT 10;
        """,
        "description": "Venues with capacity greater than 25,000."
    },
    "Q5: Matches Won by Each Team": {
    "query": """
        SELECT 
            t.team_name,
            COUNT(m.match_id) AS total_wins
        FROM matches m
        JOIN teams t 
            ON m.winner_team_id = t.team_id
        WHERE m.winner_team_id IS NOT NULL
        GROUP BY t.team_name
        ORDER BY total_wins DESC;
    """,
    "description": "Total number of matches won by each team."
},
"Q6: Player Count by Role": {
    "query": """
        SELECT 
            role,
            COUNT(*) AS player_count
        FROM players
        WHERE role IS NOT NULL
        GROUP BY role
        ORDER BY player_count DESC;
    """,
    "description": "Number of players in each role category."
},
"Q8: Series Match Breakdown": {
    "query": """
        SELECT 
            s.series_name,
            s.start_date AS series_start_date,
            COUNT(m.match_id) OVER (PARTITION BY s.series_id) AS total_matches,
            m.match_desc,
            m.match_format,
            m.start_date AS match_date,
            t1.team_name AS team1,
            t2.team_name AS team2
        FROM series s
        LEFT JOIN matches m 
            ON s.series_id = m.series_id
        LEFT JOIN teams t1 
            ON m.team1_id = t1.team_id
        LEFT JOIN teams t2 
            ON m.team2_id = t2.team_id
        WHERE EXTRACT(YEAR FROM s.start_date) = 2026
        ORDER BY s.series_name, m.start_date;
    """,
    "description": "Detailed series breakdown with each match shown separately."
},
}

# -----------------------------
# SELECT QUESTION
# -----------------------------
selected_query = st.selectbox(
    "📌 Select Question",
    list(QUERY_CONFIG.keys())
)

config = QUERY_CONFIG[selected_query]

st.markdown("---")

# -----------------------------
# DESCRIPTION
# -----------------------------
st.info(config.get("description", ""))

# -----------------------------
# SHOW QUERY
# -----------------------------
show_query = st.toggle("🧾 Show SQL Query")

if show_query:
    st.code(config["query"], language="sql")

# -----------------------------
# RUN BUTTON
# -----------------------------
run = st.button("🚀 Run Query", use_container_width=True)

# -----------------------------
# EXECUTION
# -----------------------------
if run:
    try:
        df = pd.read_sql(config["query"], conn)

        if df.empty:
            st.warning("No results found.")
        else:
            st.success(f"✅ Retrieved {len(df)} records")

            # -------------------------
            # METRICS
            # -------------------------
            col1, col2 = st.columns(2)

            with col1:
                st.metric("Rows", len(df))

            with col2:
                st.metric("Columns", len(df.columns))

            # -------------------------
            # SEARCH
            # -------------------------
            search = st.text_input("🔍 Search in results")

            if search:
                df = df[df.apply(
                    lambda row: row.astype(str).str.contains(search, case=False).any(),
                    axis=1
                )]

            # -------------------------
            # CONDITIONAL CHART
            # -------------------------
            if selected_query == "Q4: Large Capacity Venues":
                st.bar_chart(df.set_index("venue_name")["capacity"])

            # -------------------------
            # DISPLAY
            # -------------------------
            st.dataframe(df, use_container_width=True, hide_index=True)

    except Exception as e:
        st.error(f"Query failed: {e}")