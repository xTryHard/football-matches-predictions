import streamlit as st


def menu():
    st.set_page_config(
        page_title="European Football Predictions",
        page_icon="⚽",
        layout="wide",
        initial_sidebar_state="collapsed",
    )
    st.sidebar.page_link("app.py", label="Matches")
    st.sidebar.page_link("pages/leagues.py", label="Leagues")
    st.sidebar.page_link("pages/teams.py", label="Individual Teams")
