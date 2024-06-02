import streamlit as st
import pandas as pd
import numpy as np
from menu import menu
from utils import get_league_df, bundesliga, laliga, pl, seriea, ligue1


def get_leagues():
    return [laliga, bundesliga, pl, seriea, ligue1]


def filtering_options():
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        selected_league = st.selectbox("League", get_leagues())
        st.session_state.selected_league = selected_league

    with col2:
        seasons = get_seasons(selected_league)
        selected_season = st.selectbox("Season", seasons, index=len(seasons) - 1)

    teams = get_teams(selected_league)
    with col3:
        selected_home_team = st.selectbox("Home Team", teams, index=None, placeholder="Select team")

    with col4:
        selected_away_team = st.selectbox("Away Team", teams, index=None, placeholder="Select team")

    return selected_league, selected_season, selected_home_team, selected_away_team


def get_seasons(league):
    df = get_league_df(league)
    unique_years = pd.to_datetime(df['Date']).dt.year.unique()
    unique_years.sort()

    seasons = []
    for i in range(0, len(unique_years) - 1):
        seasons.append(f'{unique_years[i]}-{unique_years[i + 1]}')
    return seasons


def get_teams(league):
    df = get_league_df(league)
    teams = np.unique(df[['HomeTeam', 'AwayTeam']].values)
    return teams


def get_filtered_df(league, season, home_team, away_team):
    df = get_league_df(league)
    num_season = get_seasons(league).index(season) + 1
    mask = pd.Series([True] * len(df))

    if num_season is not None:
        mask &= (df['Season'] == num_season)

    if home_team is not None:
        mask &= (df['HomeTeam'] == home_team)

    if away_team is not None:
        mask &= (df['AwayTeam'] == away_team)

    return df[mask]


def toggle_h2h_button():
    st.session_state.h2h_button_disabled = not st.session_state.h2h_button_disabled


def show_dataframe(league, season, home_team, away_team):
    results = get_filtered_df(league, season, home_team, away_team)
    col1, col2, col3, col4, col5 = st.columns((1, 1, 2, 2, 2))

    with col1:
        st.write("Retrieved results: ", results.shape[0])
    with col2:
        st.page_link("pages/head_to_head.py", label="Go to H2H", icon=":material/sports:",
                     disabled=st.session_state.h2h_button_disabled)

    event = st.dataframe(results, selection_mode='single-row', hide_index=False, on_select=toggle_h2h_button)
    if len(event.selection.rows) == 1:
        st.session_state.selected_row = results.iloc[event.selection.rows[0]]
    else:
        st.session_state.selected_row = None


menu()

if 'selected_row' not in st.session_state:
    st.session_state.selected_row = None

if 'h2h_button_disabled' not in st.session_state:
    st.session_state.h2h_button_disabled = True

if 'selected_league' not in st.session_state:
    st.session_state.selected_league = bundesliga


st.title('Main view - Matches')
st.text('Choose a league. This will enable filtering by season, home team, and away team')
st.divider()

selected_league, selected_season, selected_home_team, selected_away_team = filtering_options()
show_dataframe(selected_league, selected_season, selected_home_team, selected_away_team)
st.write(get_teams(laliga))