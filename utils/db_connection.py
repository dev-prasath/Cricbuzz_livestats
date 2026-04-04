import psycopg2
import streamlit as st

@st.cache_resource
def get_connection():
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="Cricbuzz_Capstone",
            user="postgres",
            password="280402",
            port="5432"
        )
        return conn
    except Exception as e:
        st.error(f"PostgreSQL connection failed: {e}")
        return None