import os

import pandas as pd
import numpy as np
import streamlit as st



def load_dataset(filename, encoding = 'utf-8'):
    data_dir = os.path.join('src', 'data')
    file_path = os.path.join(data_dir, filename)
    if not os.path.isfile(file_path):
        st.error(f"File not found: {file_path}")
        return None
    return pd.read_csv(file_path)

def get_dataframes():
    df_bundesliga = load_dataset(filename='dataset-bundesliga-combined.csv')
    df_laliga = load_dataset(filename='dataset-laliga-combined.csv')
    df_pl = load_dataset(filename='dataset-pl-combined.csv', encoding='windows-1252')
    df_seriea = load_dataset(filename='dataset-seriea-combined.csv')
    df_ligue1 = load_dataset(filename='dataset-ligue1-combined.csv')

    return df_bundesliga, df_laliga, df_pl, df_seriea, df_ligue1


df_bundesliga, df_laliga, df_pl, df_seriea, df_ligue1 = get_dataframes()


def get_league_df(league):
    if league == bundesliga:
        return df_bundesliga

    elif league == laliga:
        return df_laliga

    elif league == pl:
        return df_pl

    elif league == seriea:
        return df_seriea

    elif league == ligue1:
        return df_ligue1


def get_teams(league):
    df = get_league_df(league)
    teams = np.unique(df[['HomeTeam', 'AwayTeam']].values)
    return teams


def get_seasons(league):
    df = get_league_df(league)
    unique_years = pd.to_datetime(df['Date']).dt.year.unique()
    unique_years.sort()

    seasons = []
    for i in range(0, len(unique_years) - 1):
        seasons.append(f'{unique_years[i]}-{unique_years[i + 1]}')
    return seasons


def get_filtered_df(league, season, home_team, away_team, h2h=False, is_season_num=False):
    df = get_league_df(league)

    if season:
        if not is_season_num:
            num_season = get_seasons(league).index(season) + 1
        else:
            num_season = season
    else:
        num_season = None

    mask = pd.Series([True] * len(df))

    if num_season is not None:
        mask &= (df['Season'] == num_season)

    if h2h:
        mask &= ((df['HomeTeam'] == home_team) & (df['AwayTeam'] == away_team) | (
                (df['HomeTeam'] == away_team) & (df['AwayTeam'] == home_team)))
    else:
        if home_team is not None:
            mask &= (df['HomeTeam'] == home_team)

        if away_team is not None:
            mask &= (df['AwayTeam'] == away_team)

    return df[mask]


def toggle_h2h_button():
    st.session_state.h2h_button_disabled = not st.session_state.h2h_button_disabled


def show_dataframe(league, season, home_team, away_team, h2h=False):
    results = get_filtered_df(league, season, home_team, away_team, h2h)
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


bundesliga = 'Bundesliga'
laliga = 'La Liga EA Sports'
pl = 'Premier League'
seriea = 'Seria A TIM'
ligue1 = "Ligue 1 McDonald's"
