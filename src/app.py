import streamlit as st
from menu import menu

menu()

st.title('Main view - Matches')
st.divider()
st.text('Choose league. This will enable filtering by season, teams, and matchdays.')

def leagues():
    return ['Bundesliga', 'La Liga EA Sports', 'Premier League', 'Seria A TIM', "Ligue 1 McDonald´s"]

def filtering_options():
    selected_league = st.selectbox("League", leagues())
    selected_season = st.selectbox("Season", season(selected_league))
    teams = teams(selected_league)
    selected_home_team = st.selectbox("Home Team", teams)
    selected_away_team = st.selectbox("Away Team", teams)

