import streamlit as st
import pandas as pd
from datetime import date
from utils.db_connection import get_connection

# -------------------------
# PAGE CONFIG
# -------------------------
st.set_page_config(page_title="Player Rankings CRUD", layout="wide")
st.title("📊 ICC Player Rankings Management")
st.markdown("---")

# -------------------------
# DB CONNECTION
# -------------------------
conn = get_connection()
cursor = conn.cursor()

# -------------------------
# CREATE TABLE
# -------------------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS player_rankings (
    player_id BIGINT,
    player_name TEXT,
    country TEXT,
    ranking_type TEXT,
    format_type TEXT,
    rank INTEGER,
    rating INTEGER,
    points INTEGER,
    trend TEXT,
    last_updated DATE,
    source TEXT,
    PRIMARY KEY (player_id, ranking_type, format_type)
)
""")
conn.commit()

# -------------------------
# ENSURE SOURCE COLUMN EXISTS
# -------------------------
cursor.execute("""
ALTER TABLE player_rankings 
ADD COLUMN IF NOT EXISTS source TEXT;
""")
conn.commit()

# -------------------------
# MARK OLD DATA AS API
# -------------------------
cursor.execute("""
UPDATE player_rankings
SET source = 'api'
WHERE source IS NULL;
""")
conn.commit()

# -------------------------
# TABS
# -------------------------
tab1, tab2, tab3, tab4 = st.tabs([
    "➕ Add Ranking",
    "📄 View Rankings",
    "✏️ Update Ranking",
    "❌ Delete Ranking"
])

# =====================================================
# ➕ ADD
# =====================================================
with tab1:
    st.subheader("➕ Add Player Ranking")

    with st.form("add_form", clear_on_submit=True):
        col1, col2, col3 = st.columns(3)

        player_id = col1.number_input("Player ID", min_value=1)
        player_name = col2.text_input("Player Name")
        country = col3.text_input("Country")

        col4, col5, col6 = st.columns(3)

        ranking_type = col4.selectbox("Ranking Type", ["batsman", "bowler", "allrounder"])
        format_type = col5.selectbox("Format", ["test", "odi", "t20"])
        rank = col6.number_input("Rank", min_value=1)

        col7, col8 = st.columns(2)

        rating = col7.number_input("Rating", min_value=0)
        points = col8.number_input("Points", min_value=0)

        trend = st.selectbox("Trend", ["Up", "Down", "Flat"])
        last_updated = st.date_input("Last Updated", value=date.today())

        submit = st.form_submit_button("Add Ranking")

        if submit:
            try:
                cursor.execute("""
                    INSERT INTO player_rankings 
                    (player_id, player_name, country, ranking_type, format_type,
                     rank, rating, points, trend, last_updated, source)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    int(player_id),
                    player_name.strip(),
                    country.strip(),
                    ranking_type.lower().strip(),
                    format_type.lower().strip(),
                    int(rank),
                    int(rating),
                    int(points),
                    trend,
                    str(last_updated),
                    "manual"
                ))
                conn.commit()
                st.success("✅ Added successfully!")
            except Exception as e:
                st.error(f"Error: {e}")

# =====================================================
# 📄 VIEW
# =====================================================
with tab2:
    st.subheader("📄 Player Rankings")

    col1, col2 = st.columns(2)

    ranking_filter = col1.selectbox(
        "Ranking Type",
        ["batsman", "bowler", "allrounder"],
        index=0
    )

    format_filter = col2.selectbox(
        "Format",
        ["test", "odi", "t20"],
        index=0
    )

    query = """
        SELECT * FROM player_rankings
        WHERE LOWER(TRIM(ranking_type)) = LOWER(TRIM(%s))
        AND LOWER(TRIM(format_type)) = LOWER(TRIM(%s))
    """

    df = pd.read_sql_query(query, conn, params=(ranking_filter, format_filter))

    if df.empty:
        st.warning("No data available.")
    else:
        search = st.text_input("🔍 Search Player")

        if search:
            df = df[df["player_name"].str.contains(search, case=False)]

        df = df.sort_values("rank")

        # Reorder columns
        df = df[
            [
                "rank",
                "player_name",
                "country",
                "rating",
                "points",
                "trend",
                "last_updated"
            ]
        ]

        if df.empty:
            st.warning("No data after filtering.")
        else:
            st.dataframe(df, use_container_width=True, hide_index=True)
            st.metric("🏆 Top Player", df.iloc[0]["player_name"])

# =====================================================
# ✏️ UPDATE (ONLY MANUAL)
# =====================================================
with tab3:
    st.subheader("✏️ Update Ranking")

    df = pd.read_sql_query(
        "SELECT * FROM player_rankings WHERE source='manual'",
        conn
    )

    if df.empty:
        st.warning("No manual records available.")
    else:
        options = df.apply(
            lambda x: f"{x['player_name']} ({x['format_type']} - {x['ranking_type']})",
            axis=1
        )

        selected = st.selectbox("Select Record", options)

        selected_row = df.iloc[options.tolist().index(selected)]

        new_rank = st.number_input("Rank", value=int(selected_row["rank"]))
        new_rating = st.number_input("Rating", value=int(selected_row["rating"]))
        new_points = st.number_input("Points", value=int(selected_row["points"]))

        if st.button("Update"):
            cursor.execute("""
                UPDATE player_rankings
                SET rank=%s, rating=%s, points=%s
                WHERE player_id=%s AND ranking_type=%s AND format_type=%s
            """, (
                int(new_rank),
                int(new_rating),
                int(new_points),
                int(selected_row["player_id"]),
                str(selected_row["ranking_type"]),
                str(selected_row["format_type"])
            ))
            conn.commit()
            st.success("Updated successfully")

# =====================================================
# ❌ DELETE (ONLY MANUAL)
# =====================================================
# =====================================================
# ❌ DELETE (ONLY MANUAL + CONFIRMATION)
# =====================================================
with tab4:
    st.subheader("❌ Delete Ranking")

    df = pd.read_sql_query(
        "SELECT * FROM player_rankings WHERE source='manual'",
        conn
    )

    if df.empty:
        st.warning("No manual records available.")
    else:
        options = df.apply(
            lambda x: f"{x['player_name']} ({x['format_type']} - {x['ranking_type']})",
            axis=1
        )

        selected = st.selectbox(
            "Select Record to Delete",
            options,
            key="delete_select"
        )

        selected_row = df.iloc[options.tolist().index(selected)]

        # -------------------------
        # SESSION STATE FLAG
        # -------------------------
        if "confirm_delete" not in st.session_state:
            st.session_state.confirm_delete = False

        # -------------------------
        # STEP 1: Ask Confirmation
        # -------------------------
        if not st.session_state.confirm_delete:
            if st.button("Delete"):
                st.session_state.confirm_delete = True

        # -------------------------
        # STEP 2: Confirm Delete
        # -------------------------
        else:
            st.warning("⚠️ Are you sure you want to delete this record?")

            col1, col2 = st.columns(2)

            with col1:
                if st.button("✅ Yes, Delete"):
                    cursor.execute("""
                        DELETE FROM player_rankings
                        WHERE player_id=%s AND ranking_type=%s AND format_type=%s
                    """, (
                        int(selected_row["player_id"]),
                        str(selected_row["ranking_type"]),
                        str(selected_row["format_type"])
                    ))
                    conn.commit()

                    st.success("🗑️ Deleted successfully!")

                    # Reset state
                    st.session_state.confirm_delete = False

                    # Refresh UI
                    st.rerun()

            with col2:
                if st.button("❌ Cancel"):
                    st.session_state.confirm_delete = False
# -------------------------
# FOOTER
# -------------------------
st.markdown("---")
st.caption("PostgreSQL CRUD | Cricbuzz Project")