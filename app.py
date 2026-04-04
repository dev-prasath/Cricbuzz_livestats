import streamlit as st

# -------------------------
# PAGE CONFIG
# -------------------------
st.set_page_config(
    page_title="Cricbuzz LiveStats",
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

# -------------------------
# HERO SECTION
# -------------------------
st.title("🏏 Cricbuzz LiveStats")
st.subheader("Real-Time Cricket Insights & Analytics Platform")

st.markdown("---")

# -------------------------
# INTRO
# -------------------------
st.info("""
Welcome to **Cricbuzz LiveStats** 🎯  

This platform delivers:
- 📡 Live cricket match updates  
- 👤 Player statistics  
- 🧮 SQL-powered analytics  
- 🛠️ Full CRUD operations on rankings  

Built using **Streamlit + PostgreSQL + Cricbuzz API**
""")

# -------------------------
# FEATURES (VISUAL)
# -------------------------
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 🏏 Live Matches")
    st.caption("Track real-time scores and match status")

with col2:
    st.markdown("### 📊 Player Stats")
    st.caption("Analyze player performance across formats")

with col3:
    st.markdown("### 🧠 Analytics")
    st.caption("SQL-driven insights & ranking management")

st.markdown("---")

# -------------------------
# CALL TO ACTION
# -------------------------
st.markdown("## 🚀 Ready to Explore?")

col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    if st.button("👉 Let's Go", use_container_width=True):
        st.switch_page("pages/home.py")

# -------------------------
# FOOTER
# -------------------------
st.markdown("---")
st.caption("Cricbuzz Capstone Project | Built with ❤️ using Streamlit")