import streamlit as st

# PAGE CONFIG
st.set_page_config(
    page_title="Home | Cricbuzz LiveStats",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Hide sidebar
st.markdown("""
<style>
[data-testid="stSidebar"] {
    display: none;
}
</style>
""", unsafe_allow_html=True)

# MAIN CONTENT
st.title("🏏 Cricbuzz LiveStats")
st.subheader("Real-Time Cricket Insights & SQL-Based Analytics")

st.markdown("---")

st.info("""
This dashboard provides live cricket match updates,
player statistics, and SQL-based analytics using Cricbuzz API.
""")

# FEATURES
st.subheader("📌 Features")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    - Live cricket scores and match status  
    - Match insights and tracking  
    """)

with col2:
    st.markdown("""
    - Player statistics and performance  
    - CRUD operations on rankings  
    """)

st.markdown("---")


# TECH STACK
st.subheader("🛠️ Tech Stack")

st.markdown("""
- Python  
- Streamlit  
- PostgreSQL  
- REST API (Cricbuzz via RapidAPI)
""")

st.markdown("---")

# QUICK NAV
st.subheader("🚀 Get Started")

col1, col2, col3,col4 = st.columns(4)

with col1:
    if st.button("🏏 Live Matches", use_container_width=True):
        st.switch_page("pages/livematches.py")

with col2:
    if st.button("📊 Player Stats", use_container_width=True):
        st.switch_page("pages/top_stats.py")

with col3:
    if st.button("✍️ CRUD Operations", use_container_width=True):
        st.switch_page("pages/crud_operations.py")

with col4:
    if st.button("✍️ SQL Queries", use_container_width=True):
        st.switch_page("pages/sql_queries.py")

st.markdown("---")
st.caption("Cricbuzz Capstone Project | Streamlit + PostgreSQL")