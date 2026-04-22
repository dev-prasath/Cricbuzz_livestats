import streamlit as st
import pandas as pd
from utils.db_connection import get_connection


# PAGE CONFIG

st.set_page_config(page_title="SQL Analytics", layout="wide")
st.title("🧮 SQL Analytics Dashboard")
st.markdown("---")


# DB CONNECTION

conn = get_connection()


# QUERY CONFIG

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
"Q7: Highest Individual Score per Format": {
    "query": """
        SELECT 
            format AS match_format,
            category,
            player_name,
            highest_score
        FROM all_time_records
        ORDER BY category, highest_score DESC;
    """,
    "description": "Displays the highest individual batting scores for each format (Test, ODI, T20) for both men and women."
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
"Q9: All-Rounders (1000 Runs & 50 Wickets)": {
    "query": """
        SELECT 
            p.player_name,
            ps.total_runs,
            ps.total_wickets,
            ps.batting_average,
            ps.bowling_average
        FROM players p
        JOIN player_stats ps
            ON p.player_id = ps.player_id
        WHERE ps.total_runs > 1000
          AND ps.total_wickets > 50
        ORDER BY ps.total_runs DESC;
    """,
    "description": "All-rounders with more than 1000 runs and 50 wickets."
},
"Q10: Last 20 Completed Matches": {
    "query": """
        SELECT 
            m.match_desc,
            t1.team_name AS team1,
            t2.team_name AS team2,
            tw.team_name AS winner,

            -- Extract victory margin
            CASE 
                WHEN m.status ILIKE '%won by%' 
                THEN split_part(m.status, 'won by ', 2)
                ELSE NULL
            END AS victory_margin,

            -- Extract victory type
            CASE 
                WHEN m.status ILIKE '%runs%' THEN 'Runs'
                WHEN m.status ILIKE '%wkts%' OR m.status ILIKE '%wickets%' THEN 'Wickets'
                ELSE 'Other'
            END AS victory_type,

            m.venue

        FROM matches m

        JOIN teams t1 
            ON m.team1_id = t1.team_id

        JOIN teams t2 
            ON m.team2_id = t2.team_id

        LEFT JOIN teams tw 
            ON m.winner_team_id = tw.team_id

        -- ONLY COMPLETED MATCHES
        WHERE m.status ILIKE '%won%'

        ORDER BY m.start_date DESC
        LIMIT 20;
    """,
    "description": "Last 20 completed matches with winner, margin, and victory type."
},
"Q11: Player Performance Across Formats": {
    "query": """
        SELECT 
            p.player_name,

            SUM(CASE WHEN ps.format_type = 'Test' THEN ps.runs ELSE 0 END) AS test_runs,
            SUM(CASE WHEN ps.format_type = 'ODI' THEN ps.runs ELSE 0 END) AS odi_runs,
            SUM(CASE WHEN ps.format_type = 'T20' THEN ps.runs ELSE 0 END) AS t20_runs,

            SUM(ps.runs) AS total_runs,
            SUM(ps.matches) AS total_matches,

            ROUND(
                SUM(ps.runs) * 1.0 / NULLIF(SUM(ps.matches), 0),
                2
            ) AS overall_avg

        FROM players p
        JOIN player_format_stats ps
            ON p.player_id = ps.player_id

        GROUP BY p.player_name
        HAVING COUNT(DISTINCT ps.format_type) >= 2
        ORDER BY overall_avg DESC;
    """,
    "description": "Compare player performance across Test, ODI, and T20 formats."
},
"Q12: Home vs Away Performance": {
    "query": """
        SELECT 
            t.team_name,

            CASE 
                WHEN v.home_team ILIKE '%' || t.team_name || '%'
                THEN 'Home'
                ELSE 'Away'
            END AS match_location,

            COUNT(*) AS matches_played,

            COUNT(CASE 
                WHEN m.winner_team_id = t.team_id THEN 1 
            END) AS wins,

            ROUND(
                COUNT(CASE WHEN m.winner_team_id = t.team_id THEN 1 END) * 100.0
                / NULLIF(COUNT(*), 0),
                2
            ) AS win_percentage

        FROM matches m

        JOIN teams t 
            ON t.team_id IN (m.team1_id, m.team2_id)

        LEFT JOIN venues v
            ON m.venue = v.venue_name

        WHERE m.status ILIKE '%won%'

        GROUP BY t.team_name, match_location

        ORDER BY t.team_name, match_location;
    """,
    "description": "Team performance comparison in home vs away matches using venue home_team mapping."
},
"Q13: Batting Partnerships (≥50 runs)": {
    "query": """
        SELECT 
            player1,
            player2,
            partnership_runs,
            innings
        FROM partnerships
        WHERE partnership_runs >= 50
        ORDER BY partnership_runs DESC;
    """,
    "description": "Batting partnerships where two consecutive batsmen scored 50+ runs in the same innings."
},
"Q14: Bowling Performance Analysis": {
    "query": """
        SELECT 
            bp.player_name,

            COUNT(*) AS matches_played,

            ROUND(AVG(bp.economy)::numeric, 2) AS avg_economy,

            SUM(bp.wickets) AS total_wickets

        FROM bowling_performance_v2 bp

        WHERE bp.overs >= 4

        GROUP BY bp.player_name

        ORDER BY total_wickets DESC;
    """,
    "description": "Analyzes bowling performance for players who bowled at least 4 overs per match and played at least 3 matches."
},
"Q15: Performance in Close Matches": {
    "query": """
        WITH close_matches AS (
            SELECT 
                match_id,
                winner_team_id
            FROM matches_v2
            WHERE 
                (win_type = 'runs' AND win_margin < 50)
                OR
                (win_type = 'wickets' AND win_margin < 5)
        )

        SELECT 
            p.player_name,

            COUNT(*) AS total_close_matches,

            ROUND(AVG(pmp.runs)::numeric, 2) AS avg_runs,

            SUM(
                CASE 
                    WHEN pmp.team_id = cm.winner_team_id THEN 1
                    ELSE 0
                END
            ) AS matches_won_when_batted

        FROM player_match_performance_v2 pmp

        JOIN close_matches cm 
            ON pmp.match_id = cm.match_id

        JOIN players p 
            ON p.player_id = pmp.player_id

        GROUP BY p.player_name

        HAVING COUNT(*) >= 1

        ORDER BY avg_runs DESC;
    """,
    "description": "Identifies players performing well in close matches and their contribution to wins."
},
"Q16: Top Performers in Each Match": {
    "query": """
        SELECT 
            m.match_id,
            p.player_name,
            pmp.runs,
            
            RANK() OVER (
                PARTITION BY m.match_id 
                ORDER BY pmp.runs DESC
            ) AS rank_in_match

        FROM player_match_performance pmp
        JOIN players p
            ON pmp.player_id = p.player_id
        JOIN matches_v2 m
            ON pmp.match_id = m.match_id

        WHERE pmp.runs IS NOT NULL

        ORDER BY m.match_id, rank_in_match;
    """,
    "description": "Ranks players based on their performance (runs scored) within each match."
},
"Q17: Toss Advantage Analysis (Detailed)": {
    "query": """
        WITH toss_analysis AS (
            SELECT 
                m.match_id,
                m.match_format,
                m.venue,

                t1.team_name AS team1,
                t2.team_name AS team2,
                tw.team_name AS winner,

                mt.toss_decision,
                tt.team_name AS toss_winner,

                CASE 
                    WHEN mt.toss_winner_team_id = m.winner_team_id THEN 'Yes'
                    ELSE 'No'
                END AS toss_helped_win

            FROM match_toss mt

            JOIN matches_v2 m
                ON mt.match_id = m.match_id

            JOIN teams t1
                ON m.team1_id = t1.team_id

            JOIN teams t2
                ON m.team2_id = t2.team_id

            LEFT JOIN teams tw
                ON m.winner_team_id = tw.team_id

            LEFT JOIN teams tt
                ON mt.toss_winner_team_id = tt.team_id

            WHERE m.winner_team_id IS NOT NULL
        )

        SELECT 
            match_id,
            match_format,
            venue,
            team1,
            team2,
            toss_winner,
            toss_decision,
            winner,
            toss_helped_win

        FROM toss_analysis

        ORDER BY match_format, match_id DESC;
    """,
    "description": "Detailed match-level analysis showing teams, venue, toss winner, decision, match winner, and whether winning the toss contributed to victory."
},
"Q18: Most Economical Bowlers (ODI & T20)": {
    "query": """
        SELECT 
            player_name,
            total_matches,
            total_wickets,
            ROUND(economy, 2) AS economy_rate
        FROM bowler_economy_stats
        WHERE total_matches >= 10
        ORDER BY economy ASC, total_wickets DESC
        LIMIT 10;
    """,
    "description": "Top economical bowlers in ODI and T20 formats based on combined economy rate and wickets (min 10 matches, avg 2 overs per match)."
},
"Q19: Player Consistency Analysis": {
    "query": """
        SELECT 
            p.player_name,

            COUNT(*) AS matches_played,

            ROUND(AVG(pmp.runs)::numeric, 2) AS avg_runs,

            ROUND(STDDEV(pmp.runs)::numeric, 2) AS std_dev_runs

        FROM player_match_performance_v2 pmp

        JOIN players p 
            ON p.player_id = pmp.player_id

        WHERE pmp.runs IS NOT NULL

        GROUP BY p.player_name

        HAVING 
            COUNT(*) >= 3
            AND AVG(pmp.runs) >= 10   -- filters real batsmen

        ORDER BY avg_runs DESC, std_dev_runs ASC;
    """,
    "description": "Ranks consistent batsmen by prioritizing higher average runs, then lower standard deviation for consistency."
},
"Q20: Matches Played & Batting Avg by Format": {
    "query": """
        WITH player_totals AS (
            SELECT 
                player_id,
                SUM(matches) AS total_matches
            FROM player_format_stats
            GROUP BY player_id
        )

        SELECT 
            p.player_name,
            pt.total_matches,

            -- Match Counts
            SUM(CASE WHEN ps.format_type = 'Test' THEN ps.matches ELSE 0 END) AS test_matches,
            SUM(CASE WHEN ps.format_type = 'ODI' THEN ps.matches ELSE 0 END) AS odi_matches,
            SUM(CASE WHEN ps.format_type = 'T20' THEN ps.matches ELSE 0 END) AS t20_matches,

            -- Batting Averages
            ROUND(AVG(CASE WHEN ps.format_type = 'Test' THEN ps.batting_average END), 2) AS test_avg,
            ROUND(AVG(CASE WHEN ps.format_type = 'ODI' THEN ps.batting_average END), 2) AS odi_avg,
            ROUND(AVG(CASE WHEN ps.format_type = 'T20' THEN ps.batting_average END), 2) AS t20_avg

        FROM players p

        JOIN player_format_stats ps
            ON p.player_id = ps.player_id

        JOIN player_totals pt
            ON p.player_id = pt.player_id

        WHERE pt.total_matches >= 20

        GROUP BY p.player_name, pt.total_matches

        ORDER BY pt.total_matches DESC;
    """,
    "description": "Shows number of matches played and batting averages across Test, ODI, and T20 formats for players with at least 20 total matches."
},
"Q21: Player Performance Score": {
    "query": """
        WITH player_stats AS (
            SELECT 
                p.player_id,
                p.player_name,

                COUNT(DISTINCT pmp.match_id) AS matches_played,

                SUM(pmp.runs) AS total_runs

            FROM player_match_performance_v2 pmp

            JOIN players p
                ON p.player_id = pmp.player_id

            WHERE pmp.runs IS NOT NULL

            GROUP BY p.player_id, p.player_name
        )

        SELECT 
            player_name,
            matches_played,
            total_runs,

            ROUND(total_runs * 1.0 / NULLIF(matches_played, 0), 2) AS batting_avg,

            -- 🔥 PERFORMANCE SCORE (BATSMAN FOCUSED)
            ROUND(
                (total_runs * 0.02) +                          -- volume scoring
                ((total_runs * 1.0 / NULLIF(matches_played, 0)) * 0.8)  -- consistency
            , 2) AS performance_score

        FROM player_stats

        WHERE total_runs > 0

        ORDER BY performance_score DESC;
    """,
    "description": "Ranks players based on batting performance using total runs and consistency (adapted due to lack of bowling data)."
},
"Q22: Head-to-Head Team Analysis": {
    "query": """
        WITH match_data AS (
            SELECT 
                m.match_id,
                m.team1_id,
                m.team2_id,
                m.winner_team_id,
                m.win_margin,
                m.venue

            FROM matches_v2 m

            WHERE m.winner_team_id IS NOT NULL
        ),

        team_pairs AS (
            SELECT 
                LEAST(team1_id, team2_id) AS team_a,
                GREATEST(team1_id, team2_id) AS team_b,
                *
            FROM match_data
        ),

        aggregated AS (
            SELECT 
                team_a,
                team_b,

                COUNT(*) AS total_matches,

                COUNT(CASE WHEN winner_team_id = team_a THEN 1 END) AS team_a_wins,
                COUNT(CASE WHEN winner_team_id = team_b THEN 1 END) AS team_b_wins,

                ROUND(AVG(win_margin), 2) AS avg_margin

            FROM team_pairs
            GROUP BY team_a, team_b
            HAVING COUNT(*) >= 2
        )

        SELECT 
            ta.team_name AS team_a,
            tb.team_name AS team_b,

            ag.total_matches,
            ag.team_a_wins,
            ag.team_b_wins,

            ROUND(ag.team_a_wins * 100.0 / ag.total_matches, 2) AS team_a_win_pct,
            ROUND(ag.team_b_wins * 100.0 / ag.total_matches, 2) AS team_b_win_pct,

            ag.avg_margin

        FROM aggregated ag

        JOIN teams ta ON ag.team_a = ta.team_id
        JOIN teams tb ON ag.team_b = tb.team_id

        ORDER BY ag.total_matches DESC;
    """,
    "description": "Head-to-head analysis between teams based on available dataset (minimum 2 matches)."
},
"Q23: Player Form & Momentum": {
    "query": """
        WITH ranked_matches AS (
            SELECT 
                pmp.player_id,
                p.player_name,
                pmp.runs,
                m.start_date,

                ROW_NUMBER() OVER (
                    PARTITION BY pmp.player_id
                    ORDER BY m.start_date DESC
                ) AS rn

            FROM player_match_performance_v2 pmp

            JOIN matches_v2 m 
                ON pmp.match_id = m.match_id

            JOIN players p
                ON p.player_id = pmp.player_id

            WHERE pmp.runs IS NOT NULL
        ),

        last_10 AS (
            SELECT *
            FROM ranked_matches
            WHERE rn <= 10
        )

        SELECT 
            player_name,

            COUNT(*) AS matches_considered,

            ROUND(AVG(runs)::numeric, 2) AS avg_runs_last_10,

            ROUND(AVG(CASE WHEN rn <= 5 THEN runs END)::numeric, 2) AS avg_runs_last_5,

            COUNT(CASE WHEN runs >= 50 THEN 1 END) AS fifties,

            ROUND(STDDEV(runs)::numeric, 2) AS consistency_score

        FROM last_10

        GROUP BY player_name

        HAVING COUNT(*) >= 3

        ORDER BY avg_runs_last_10 DESC;
    """,
    "description": "Evaluates player form using recent matches (last 10 & last 5), including consistency and scoring ability."
},
"Q24: Partnership Impact Analysis": {
    "query": """
        WITH partnership_base AS (
            SELECT 
                p.player1,
                p.player2,
                p.match_id,
                p.innings,
                p.partnership_runs,
                m.start_date

            FROM partnerships p
            JOIN matches_v2 m 
                ON p.match_id = m.match_id
        ),

        ranked_partnerships AS (
            SELECT *,
                ROW_NUMBER() OVER (
                    PARTITION BY player1, player2
                    ORDER BY start_date DESC
                ) AS rn
            FROM partnership_base
        ),

        last_10_partnerships AS (
            SELECT *
            FROM ranked_partnerships
            WHERE rn <= 10
        )

        SELECT 
            player1,
            player2,

            COUNT(*) AS partnerships_played,

            ROUND(AVG(partnership_runs), 2) AS avg_partnership_runs,

            ROUND(AVG(CASE WHEN rn <= 5 THEN partnership_runs END), 2) 
                AS avg_last_5_partnerships,

            MAX(partnership_runs) AS highest_partnership,

            COUNT(CASE WHEN partnership_runs >= 50 THEN 1 END) 
                AS fifty_plus_stands,

            COUNT(CASE WHEN partnership_runs >= 100 THEN 1 END) 
                AS hundred_partnerships,

            ROUND(STDDEV(partnership_runs), 2) 
                AS consistency_score

        FROM last_10_partnerships

        GROUP BY player1, player2

        HAVING COUNT(*) >= 3

        ORDER BY avg_partnership_runs DESC;
    """,
    "description": "Evaluates batting partnerships based on recent performance, consistency, and impact (last 10 partnerships)."
},
"Q25: Player Career Progression & Trend Analysis": {
    "query": """
        WITH base AS (
            SELECT 
                p.player_id,
                p.player_name,
                DATE_TRUNC('quarter', m.start_date) AS quarter,
                pmp.runs

            FROM player_match_performance_v2 pmp

            JOIN matches_v2 m 
                ON pmp.match_id = m.match_id

            JOIN players p 
                ON p.player_id = pmp.player_id

            WHERE pmp.runs IS NOT NULL
        ),

        quarterly_stats AS (
            SELECT 
                player_id,
                player_name,
                quarter,
                COUNT(*) AS matches_played,
                ROUND(AVG(runs)::numeric, 2) AS avg_runs

            FROM base

            GROUP BY player_id, player_name, quarter

            HAVING COUNT(*) >= 1
        ),

        with_lag AS (
            SELECT 
                *,
                LAG(avg_runs) OVER (
                    PARTITION BY player_id ORDER BY quarter
                ) AS prev_runs

            FROM quarterly_stats
        ),

        trend_calc AS (
            SELECT 
                *,

                CASE 
                    WHEN prev_runs IS NULL THEN 'Stable'
                    WHEN avg_runs > prev_runs THEN 'Improving'
                    WHEN avg_runs < prev_runs THEN 'Declining'
                    ELSE 'Stable'
                END AS performance_trend

            FROM with_lag
        ),

        player_summary AS (
            SELECT 
                player_id,
                player_name,

                COUNT(*) AS quarters_played,

                ROUND(AVG(avg_runs)::numeric, 2) AS overall_avg_runs,

                SUM(CASE WHEN performance_trend = 'Improving' THEN 1 ELSE 0 END) AS improving_count,
                SUM(CASE WHEN performance_trend = 'Declining' THEN 1 ELSE 0 END) AS declining_count,
                SUM(CASE WHEN performance_trend = 'Stable' THEN 1 ELSE 0 END) AS stable_count

            FROM trend_calc

            GROUP BY player_id, player_name

            HAVING COUNT(*) >= 2
        )

        SELECT 
            player_name,
            quarters_played,
            overall_avg_runs,
            improving_count,
            declining_count,
            stable_count,

            CASE 
                WHEN improving_count > declining_count THEN 'Career Ascending'
                WHEN declining_count > improving_count THEN 'Career Declining'
                ELSE 'Career Stable'
            END AS career_phase

        FROM player_summary

        ORDER BY overall_avg_runs DESC;
    """,
    "description": "Analyzes player performance trends over time using quarterly averages to identify career progression (improving, declining, or stable)."
}
}


# SELECT QUESTION

selected_query = st.selectbox(
    "📌 Select Question",
    list(QUERY_CONFIG.keys())
)

config = QUERY_CONFIG[selected_query]

st.markdown("---")


# DESCRIPTION

st.info(config.get("description", ""))


# SHOW QUERY

show_query = st.toggle("🧾 Show SQL Query")

if show_query:
    st.code(config["query"], language="sql")


# RUN BUTTON

run = st.button("🚀 Run Query", use_container_width=True)


# EXECUTION

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