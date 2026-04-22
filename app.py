import streamlit as st


# PAGE CONFIG

st.set_page_config(
    page_title="Cricbuzz LiveStats",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# GLOBAL STYLING

st.markdown("""
<style>
/* Hide sidebar */
[data-testid="stSidebar"] {display: none;}

/* Main background */
.main {
    background: linear-gradient(120deg, #0f2027, #203a43, #2c5364);
    color: white;
}

/* Title styling */
.title {
    font-size: 3rem;
    font-weight: 700;
    text-align: center;
}

/* Subtitle */
.subtitle {
    text-align: center;
    font-size: 1.2rem;
    color: #dcdcdc;
    margin-bottom: 20px;
}

/* Card styling */
.card {
    background: rgba(255,255,255,0.05);
    padding: 25px;
    border-radius: 15px;
    text-align: center;
    transition: 0.3s;
    border: 1px solid rgba(255,255,255,0.1);
}

.card:hover {
    transform: translateY(-8px);
    box-shadow: 0px 10px 25px rgba(0,0,0,0.3);
}

/* Button */
.stButton>button {
    background: linear-gradient(90deg, #ff512f, #dd2476);
    color: white;
    font-size: 18px;
    border-radius: 10px;
    padding: 10px;
    border: none;
}

.stButton>button:hover {
    transform: scale(1.05);
}
</style>
""", unsafe_allow_html=True)


# HERO SECTION

st.markdown('<div class="title">🏏 Cricbuzz LiveStats</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Real-Time Cricket Insights & Analytics Platform</div>', unsafe_allow_html=True)

st.markdown("---")


# INTRO

st.markdown("""
### 🎯 About the Platform

Welcome to **Cricbuzz LiveStats** — a powerful cricket analytics platform that combines  
real-time data with deep statistical insights.

**What you get:**
- 📡 Live match tracking from Cricbuzz API  
- 👤 Player performance analytics  
- 🧮 Advanced SQL insights  
- 🛠️ Full CRUD database operations  
""")

st.markdown("---")


# FEATURES (CARDS UI)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="card">
        <h3>🏏 Live Matches</h3>
        <p>Track real-time scores, match progress, and live updates instantly.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="card">
        <h3>📊 Player Stats</h3>
        <p>Analyze performance across formats with detailed statistics.</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="card">
        <h3>🧠 Advanced Analytics</h3>
        <p>Powerful SQL-driven insights and intelligent ranking systems.</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


# CTA SECTION

st.markdown("## 🚀 Start Exploring")

col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    if st.button("👉 Enter Dashboard", use_container_width=True):
        st.switch_page("pages/home.py")


# FOOTER

st.markdown("---")
st.markdown("""
<div style='text-align:center; font-size:14px; color:lightgray;'>
Built with ❤️ using Streamlit | Cricbuzz Capstone Project  
</div>
""", unsafe_allow_html=True)