import streamlit as st

def menu():
    st.sidebar.page_link("app.py", label="Matches")
    st.sidebar.page_link("pages/leagues.py", label="Leagues")
    st.sidebar.page_link("pages/teams.py", label="Individual Teams")