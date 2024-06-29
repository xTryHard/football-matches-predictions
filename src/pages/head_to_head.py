import os

import joblib
import numpy as np
import streamlit as st
from menu import menu
from streamlit_extras.row import row
from streamlit_extras.grid import grid
import plotly.express as px
from datetime import datetime
import calendar
import pandas as pd
from utils import get_league_df, bundesliga, laliga, pl, seriea, ligue1, get_filtered_df
from badges import bundesliga_badges, laliga_badges, pl_badges, seriea_badges, ligue1_badges

if 'selected_league' not in st.session_state or 'selected_row' not in st.session_state:
    st.switch_page('app.py')

st.session_state.h2h_button_disabled = True
menu()

selected_row_data = st.session_state.selected_row

st.title('Match and Past H2H encounters')
st.write("See details of the current and past matches between the selected teams")
st.divider()
match_df = get_filtered_df(league=st.session_state.selected_league, season=selected_row_data['Season'],
                           home_team=selected_row_data["HomeTeam"], away_team=selected_row_data["AwayTeam"],
                           is_season_num=True)


def get_badge(league, team):
    if league == bundesliga:
        if not bundesliga_badges[team]:
            return 'https://www.thesportsdb.com/images/media/league/badge/teqh1b1679952008.png'
        return bundesliga_badges[team]

    elif league == laliga:
        if team not in laliga_badges:
            return 'https://www.thesportsdb.com/images/media/league/badge/ja4it51687628717.png'
        return laliga_badges[team]

    elif league == pl:
        if team not in pl_badges:
            return 'https://www.thesportsdb.com/images/media/league/badge/dsnjpz1679951317.png'
        return pl_badges[team]

    elif league == seriea:
        if team not in seriea_badges:
            return 'https://www.thesportsdb.com/images/media/league/badge/67q3q21679951383.png'
        return seriea_badges[team]

    elif league == ligue1:
        if team not in ligue1_badges:
            return 'https://www.thesportsdb.com/images/media/league/badge/qhslta1701386289.png'
        return ligue1_badges[team]


def result_header():
    with st.container():
        styles = """
            <style>
                div[data-testid="stVerticalBlockBorderWrapper"] div[data-testid="stHorizontalBlock"] {
                    text-align: center;
                    align-items: center;
                }
            </style>
        """
        st.html(styles)

        col1, col2, col3, col4, col5 = st.columns((1, 3, 4, 3, 1))
        with col1:
            pass

        with col2:
            with st.container(border=True, height=90):
                home_row = row([4, 1], vertical_align="centered", gap="small")
                home_team = selected_row_data["HomeTeam"]
                home_team_badge = get_badge(st.session_state.selected_league, home_team)

                home_row.markdown(f"##### {home_team}")
                home_row.image(home_team_badge, width=60)
        with col3:
            with st.container(border=True, height=90):
                result_row = row([1.5, 5, 1], vertical_align="top", gap="small")
                result_row.markdown(f"### {selected_row_data['FTHG']}")
                result_row.markdown('''### Match result''', unsafe_allow_html=True)
                result_row.markdown(f"### {selected_row_data['FTAG']}")
        with col4:
            with st.container(border=True, height=90):
                away_row = row([1, 5], vertical_align="centered", gap="small")
                away_team = selected_row_data["AwayTeam"]
                away_team_badge = get_badge(st.session_state.selected_league, away_team)

                away_row.image(away_team_badge, width=60)
                away_row.markdown(f"##### {away_team}")

        with col5:
            pass


def match_date():
    with st.container():
        col1, col2, col3 = st.columns((1, 3, 1))
        with col1:
            pass

        with col2:
            date_object = datetime.strptime(selected_row_data["Date"], '%Y-%m-%d')
            day_name = calendar.day_name[selected_row_data["MatchDayOfWeek"].item()]
            formatted_date = date_object.strftime('%B %d, %Y')
            st.markdown(f":snow[{st.session_state.selected_league} - {day_name}, {formatted_date}]")

        with col3:
            pass


def match_summary():
    st.markdown("##### Match Summary")

    match_result_row = row(1, vertical_align="centered", gap="small")
    match_result_row.table(match_df[
                               ["Date", "HomeTeam", "AwayTeam", "FTHG", "FTAG", "HTHG", "HTAG", 'HS', 'AS', 'HF', 'AF',
                                'HC', 'AC', 'HY', 'AY', 'HR', 'AR']])


def get_scored_goals_match_df(grid):
    goals_data = pd.concat([
        match_df[['HomeTeam', 'FTHG', 'HTHG']].rename(columns={
            'HomeTeam': 'Team', 'FTHG': 'Full Time Goals', 'HTHG': 'Half Time Goals'
        }),
        match_df[['AwayTeam', 'FTAG', 'HTAG']].rename(columns={
            'AwayTeam': 'Team', 'FTAG': 'Full Time Goals', 'HTAG': 'Half Time Goals'
        })
    ], ignore_index=True)
    fig = px.bar(goals_data, x="Team", y=["Full Time Goals", "Half Time Goals"],
                 title='Full Time & Half Time Goals by Team', barmode='group', labels={'value': 'Goals'})
    grid.plotly_chart(fig)


def get_shots_match_df(grid):
    shots_data = pd.concat([
        match_df[['HomeTeam', 'HS']].rename(columns={
            'HomeTeam': 'Team', 'HS': 'Shots'
        }),
        match_df[['AwayTeam', 'AS']].rename(columns={
            'AwayTeam': 'Team', 'AS': 'Shots'
        })
    ], ignore_index=True)
    fig = px.bar(shots_data, x="Team", y="Shots", title='Shots by Team', color='Team')
    grid.plotly_chart(fig)


def get_corners_match_df(grid):
    corners_data = pd.concat([
        match_df[['HomeTeam', 'HC']].rename(columns={
            'HomeTeam': 'Team', 'HC': 'Corners'
        }),
        match_df[['AwayTeam', 'AC']].rename(columns={
            'AwayTeam': 'Team', 'AC': 'Corners'
        })
    ], ignore_index=True)
    fig = px.bar(corners_data, x="Team", y="Corners", title='Corners by Team', color='Team')
    grid.plotly_chart(fig)


def get_fouls_match_df(grid):
    fouls_data = pd.concat([
        match_df[['HomeTeam', 'HF']].rename(columns={
            'HomeTeam': 'Team', 'HF': 'Fouls Committed'
        }),
        match_df[['AwayTeam', 'AF']].rename(columns={
            'AwayTeam': 'Team', 'AF': 'Fouls Committed'
        })
    ], ignore_index=True)
    fig = px.bar(fouls_data, x="Team", y="Fouls Committed", title='Fouls Committed by Team', color='Team')
    grid.plotly_chart(fig)


def get_yellow_cards_match_df(grid):
    yellow_cards_data = pd.concat([
        match_df[['HomeTeam', 'HY']].rename(columns={
            'HomeTeam': 'Team', 'HY': 'Yellow Cards'
        }),
        match_df[['AwayTeam', 'AY']].rename(columns={
            'AwayTeam': 'Team', 'AY': 'Yellow Cards'
        })
    ], ignore_index=True)
    fig = px.bar(yellow_cards_data, x="Team", y="Yellow Cards", title='Yellow Cards by Team', color='Team')
    grid.plotly_chart(fig)


def get_red_cards_match_df(grid):
    red_cards_data = pd.concat([
        match_df[['HomeTeam', 'HR']].rename(columns={
            'HomeTeam': 'Team', 'HR': 'Red Cards'
        }),
        match_df[['AwayTeam', 'AR']].rename(columns={
            'AwayTeam': 'Team', 'AR': 'Red Cards'
        })
    ], ignore_index=True)
    fig = px.bar(red_cards_data, x="Team", y="Red Cards", title='Red Cards by Team', color='Team')
    grid.plotly_chart(fig)


def get_elo_match_df(grid):
    elo_data = pd.concat([
        match_df[['HomeTeam', 'HomeElo']].rename(columns={
            'HomeTeam': 'Team', 'HomeElo': 'Elo'
        }),
        match_df[['AwayTeam', 'AwayElo']].rename(columns={
            'AwayTeam': 'Team', 'AR': 'Elo'
        })
    ], ignore_index=True)
    fig = px.bar(elo_data, x="Team", y="Elo", title='Elo by Team', color='Team')
    grid.plotly_chart(fig)


def get_goals_current_season_match_df(grid):
    goals_data = pd.concat([
        match_df[['HomeTeam', 'HomeTeamGoalsCurrentSeason', 'HomeTeamGoalsConcededCurrentSeason']].rename(columns={
            'HomeTeam': 'Team', 'HomeTeamGoalsCurrentSeason': 'Goals Scored',
            'HomeTeamGoalsConcededCurrentSeason': 'Goals Conceded'
        }),
        match_df[['AwayTeam', 'AwayTeamGoalsCurrentSeason', 'AwayTeamGoalsConcededCurrentSeason']].rename(columns={
            'AwayTeam': 'Team', 'AwayTeamGoalsCurrentSeason': 'Goals Scored',
            'AwayTeamGoalsConcededCurrentSeason': 'Goals Conceded'
        })
    ], ignore_index=True)
    fig = px.bar(goals_data, x="Team", y=["Goals Scored", "Goals Conceded"],
                 title='Scored & Conceded Goals by Team (Current Season)', barmode='group', labels={'value': 'Goals'})
    grid.plotly_chart(fig)


def get_win_rate_current_season_match_df(grid):
    win_rate_data = pd.concat([
        match_df[['HomeTeam', 'HomeTeamWinRateSeason']].rename(columns={
            'HomeTeam': 'Team', 'HomeTeamWinRateSeason': 'Win Rate'
        }),
        match_df[['AwayTeam', 'AwayTeamWinRateSeason']].rename(columns={
            'AwayTeam': 'Team', 'AwayTeamWinRateSeason': 'Win Rate'
        })
    ], ignore_index=True)
    fig = px.bar(win_rate_data, x="Team", y="Win Rate", title='Win Rate by Team (Current Season)', color='Team')
    grid.plotly_chart(fig)


def get_h2h_goals_match_df(grid):
    goals_data = pd.concat([
        match_df[['HomeTeam', 'HeadToHeadHomeGoals']].rename(columns={
            'HomeTeam': 'Team', 'HeadToHeadHomeGoals': 'Goals Scored',
        }),
        match_df[['AwayTeam', 'HeadToHeadAwayGoals']].rename(columns={
            'AwayTeam': 'Team', 'HeadToHeadAwayGoals': 'Goals Scored',
        })
    ], ignore_index=True)
    fig = px.bar(goals_data, x="Team", y='Goals Scored',
                 title='Goals Scored H2H', barmode='group', color='Team')
    grid.plotly_chart(fig)


def get_h2h_rates_match_df(grid):
    home_team = match_df["HomeTeam"].iloc[0]
    away_team = match_df["AwayTeam"].iloc[0]
    matches = match_df["HeadToHeadMatches"].iloc[0]
    win_rate_data = match_df[['HeadToHeadHomeWinRate', 'HeadToHeadAwayWinRate', 'HeadToHeadDrawRate']]
    win_rate_data.rename(columns={
        'HeadToHeadHomeWinRate': f'{home_team} Win Rate',
        'HeadToHeadAwayWinRate': f'{away_team} Win Rate',
        'HeadToHeadDrawRate': 'Draw Rate'
    }, inplace=True)
    df_melted = win_rate_data.melt(var_name='Result', value_name='Rate')
    fig = px.pie(df_melted, names='Result', values='Rate',
                 title=f'Head to Head Rates (on the {matches} previous matches)')
    grid.plotly_chart(fig)



def load_model_scaler(filename, league):
    data_dir = os.path.join('src', 'models-and-scalers', league)
    file_path = os.path.join(data_dir, filename)
    if not os.path.isfile(file_path):
        st.error(f"File not found: {file_path}")
        return None
    return joblib.load(file_path)

def get_models_bundesliga():
    binary_in_game = load_model_scaler('best_model_bundesliga_binary_in_game.pkl', 'bundesliga')
    binary_pre_game = load_model_scaler('best_model_bundesliga_binary_pre_game.pkl', 'bundesliga')
    multiclass_in_game = load_model_scaler('best_model_bundesliga_multi_in_game.pkl', 'bundesliga')
    multiclass_pre_game = load_model_scaler('best_model_bundesliga_multi_pre_game.pkl', 'bundesliga')

    return binary_in_game, binary_pre_game, multiclass_in_game, multiclass_pre_game


def get_models_laliga():
    binary_in_game = load_model_scaler('best_model_laliga_binary_in_game.pkl', 'laliga')
    binary_pre_game = load_model_scaler('best_model_laliga_binary_pre_game.pkl', 'laliga')
    multiclass_in_game = load_model_scaler('best_model_laliga_multi_in_game.pkl', 'laliga')
    multiclass_pre_game = load_model_scaler('best_model_laliga_multi_pre_game.pkl', 'laliga')

    return binary_in_game, binary_pre_game, multiclass_in_game, multiclass_pre_game


def get_models_ligue1():

    binary_in_game = load_model_scaler('best_model_ligue1_binary_in_game.pkl', 'ligue1')
    binary_pre_game = load_model_scaler('best_model_ligue1_binary_pre_game.pkl', 'ligue1')
    multiclass_in_game = load_model_scaler('best_model_ligue1_multi_in_game.pkl', 'ligue1')
    multiclass_pre_game = load_model_scaler('best_model_ligue1_multi_pre_game.pkl', 'ligue1')

    return binary_in_game, binary_pre_game, multiclass_in_game, multiclass_pre_game


def get_models_pl():
    binary_in_game = load_model_scaler('best_model_pl_binary_in_game.pkl', 'pl')
    binary_pre_game = load_model_scaler('best_model_pl_binary_pre_game.pkl', 'pl')
    multiclass_in_game = load_model_scaler('best_model_pl_multi_in_game.pkl', 'pl')
    multiclass_pre_game = load_model_scaler('best_model_pl_multi_pre_game.pkl', 'pl')

    return binary_in_game, binary_pre_game, multiclass_in_game, multiclass_pre_game


def get_models_seriea():
    binary_in_game = load_model_scaler('best_model_seriea_binary_in_game.pkl', 'seriea')
    binary_pre_game = load_model_scaler('best_model_seriea_binary_pre_game.pkl', 'seriea')
    multiclass_in_game = load_model_scaler('best_model_seriea_multi_in_game.pkl', 'seriea')
    multiclass_pre_game = load_model_scaler('best_model_seriea_multi_pre_game.pkl', 'seriea')

    return binary_in_game, binary_pre_game, multiclass_in_game, multiclass_pre_game


def get_scalers_bundesliga():
    in_game = load_model_scaler('scaler_bundesliga_multi_in_game.pkl', 'bundesliga')
    pre_game = load_model_scaler('scaler_bundesliga_multi_pre_game.pkl', 'bundesliga')

    return in_game, pre_game


def get_scalers_laliga():
    in_game = load_model_scaler('scaler_laliga_multi_in_game.pkl', 'laliga')
    pre_game = load_model_scaler('scaler_laliga_multi_pre_game.pkl', 'laliga')

    return in_game, pre_game


def get_scalers_ligue1():
    in_game = load_model_scaler('scaler_ligue1_multi_in_game.pkl', 'ligue1')
    pre_game = load_model_scaler('scaler_ligue1_multi_pre_game.pkl', 'ligue1')

    return in_game, pre_game


def get_scalers_pl():
    in_game = load_model_scaler('scaler_pl_multi_in_game.pkl', 'pl')
    pre_game = load_model_scaler('scaler_pl_multi_pre_game.pkl', 'pl')

    return in_game, pre_game


def get_scalers_seriea():
    in_game = load_model_scaler('scaler_seriea_multi_in_game.pkl', 'seriea')
    pre_game = load_model_scaler('scaler_seriea_multi_pre_game.pkl', 'seriea')

    return in_game, pre_game


def calculate_proba(mod_binary_in_game, mod_binary_pre_game, mod_multiclass_in_game, mod_multiclass_pre_game,
                    sc_in_game, sc_pre_game):
    drop_columns_in_game = ['Date', 'FTHG', 'FTAG', 'FTR', 'HTR', 'HomeTeam', 'AwayTeam', 'FTREncoded']
    drop_columns_pre_game = ['Date', 'FTHG', 'FTAG', 'FTR', 'HTR', 'HTREncoded', 'HomeTeam', 'AwayTeam', 'HTHG', 'HTAG',
                             'HS', 'AS', 'HF', 'AF', 'HC', 'AC', 'HY', 'AY', 'HR', 'AR', 'FTREncoded']

    df_in_game = match_df.drop(columns=drop_columns_in_game)
    df_pre_game = match_df.drop(columns=drop_columns_pre_game)

    exclude_columns = ['Season', 'MatchDayOfWeek', 'MatchMonth', 'HTREncoded', 'HomeTeamTargetEncoded_0',
                       'AwayTeamTargetEncoded_0', 'HomeTeamTargetEncoded_2', 'AwayTeamTargetEncoded_2',
                       'HomeTeamTargetEncoded_1', 'AwayTeamTargetEncoded_1']
    columns_to_scale_in_game = df_in_game.columns.difference(exclude_columns)
    columns_to_scale_pre_game = df_pre_game.columns.difference(exclude_columns)

    df_in_game[columns_to_scale_in_game] = sc_in_game.transform(df_in_game[columns_to_scale_in_game])
    df_pre_game[columns_to_scale_pre_game] = sc_pre_game.transform(df_pre_game[columns_to_scale_pre_game])

    y_proba_multiclass_in_game = mod_multiclass_in_game.predict_proba(df_in_game)
    y_proba_multiclass_pre_game = mod_multiclass_pre_game.predict_proba(df_pre_game)

    y_proba_binary_in_game = mod_binary_in_game.predict_proba(df_in_game)
    y_proba_binary_pre_game = mod_binary_pre_game.predict_proba(df_pre_game)

    return y_proba_binary_in_game, y_proba_binary_pre_game, y_proba_multiclass_in_game, y_proba_multiclass_pre_game


def get_predictions(league):
    mod_binary_in_game = None
    mod_binary_pre_game = None
    mod_multiclass_in_game = None
    mod_multiclass_pre_game = None

    sc_in_game = None
    sc_pre_game = None

    if league == bundesliga:
        mod_binary_in_game, mod_binary_pre_game, mod_multiclass_in_game, mod_multiclass_pre_game = get_models_bundesliga()
        sc_in_game, sc_pre_game = get_scalers_bundesliga()
    elif league == laliga:
        mod_binary_in_game, mod_binary_pre_game, mod_multiclass_in_game, mod_multiclass_pre_game = get_models_laliga()
        sc_in_game, sc_pre_game = get_scalers_laliga()
    elif league == ligue1:
        mod_binary_in_game, mod_binary_pre_game, mod_multiclass_in_game, mod_multiclass_pre_game = get_models_ligue1()
        sc_in_game, sc_pre_game = get_scalers_ligue1()
    elif league == pl:
        mod_binary_in_game, mod_binary_pre_game, mod_multiclass_in_game, mod_multiclass_pre_game = get_models_pl()
        sc_in_game, sc_pre_game = get_scalers_pl()
    elif league == seriea:
        mod_binary_in_game, mod_binary_pre_game, mod_multiclass_in_game, mod_multiclass_pre_game = get_models_seriea()
        sc_in_game, sc_pre_game = get_scalers_seriea()

    (y_proba_binary_in_game,
     y_proba_binary_pre_game,
     y_proba_multiclass_in_game,
     y_proba_multiclass_pre_game) = calculate_proba(mod_binary_in_game, mod_binary_pre_game,
                                                    mod_multiclass_in_game, mod_multiclass_pre_game,
                                                    sc_in_game, sc_pre_game)

    return y_proba_binary_in_game, y_proba_binary_pre_game, y_proba_multiclass_in_game, y_proba_multiclass_pre_game


def odds_to_prob(df, home_col, draw_col, away_col):
    prob_home = 1 / df[home_col]
    prob_draw = 1 / df[draw_col]
    prob_away = 1 / df[away_col]

    total_prob = prob_home + prob_draw + prob_away
    prob_home /= total_prob
    prob_draw /= total_prob
    prob_away /= total_prob

    return prob_home, prob_draw, prob_away


def process_bookies_odds():
    bookies_df = match_df[['FTREncoded']].copy()
    bookies_df['B365HProb'], bookies_df['B365DProb'], bookies_df['B365AProb'] = odds_to_prob(match_df, 'B365H', 'B365D',
                                                                                             'B365A')
    # Convert IW odds to probabilities
    bookies_df['IWHProb'], bookies_df['IWDProb'], bookies_df['IWAProb'] = odds_to_prob(match_df, 'IWH', 'IWD', 'IWA')
    # Convert WH odds to probabilities
    bookies_df['WHHProb'], bookies_df['WHDProb'], bookies_df['WHAProb'] = odds_to_prob(match_df, 'WHH', 'WHD', 'WHA')
    b365_list = bookies_df[['B365HProb', 'B365DProb', 'B365AProb']].iloc[0].tolist()
    iw_list = bookies_df[['IWHProb', 'IWDProb', 'IWAProb']].iloc[0].tolist()
    wh_list = bookies_df[['WHHProb', 'WHDProb', 'WHAProb']].iloc[0].tolist()

    return b365_list, iw_list, wh_list

def find_max_element(pred_list):
    return np.argmax(pred_list)


def format_title(label, title):
    return f'{title} <br><sup>{label}</sup>'

def pred_pie_chart(grid, predictions, title, is_binary=False):
    home_team = match_df["HomeTeam"].iloc[0]
    away_team = match_df["AwayTeam"].iloc[0]

    if not is_binary:
        labels = [f'{home_team} Win', 'Draw', f'{away_team} Win']
    else:
        labels = [f'{away_team} Win', f'{home_team} Win/Draw']

    formatted_title = format_title(labels[find_max_element(predictions)], title)

    # Create the pie chart with additional customization
    fig = px.pie(values=predictions, names=labels, title=formatted_title,
                 hole=0.3, labels={'values': 'Percentage', 'label': 'Event'})
    grid.plotly_chart(fig)

def prediction_graphs():
    st.markdown("##### Predictions Visualizations")
    my_grid = grid([1, 0.1, 1], [1, 0.1, 1], [1, 0.1, 1, 0.1, 1], vertical_align="top")
    (y_proba_binary_in_game,
     y_proba_binary_pre_game,
     y_proba_multiclass_in_game,
     y_proba_multiclass_pre_game) = get_predictions(st.session_state.selected_league)

    b365_list, iw_list, wh_list = process_bookies_odds()

    # Row 1
    pred_pie_chart(my_grid, y_proba_multiclass_pre_game[0], title="Multiclass pre-game")
    my_grid.empty()
    pred_pie_chart(my_grid, y_proba_multiclass_in_game[0], title="Multiclass in-game")

    # Row 2
    pred_pie_chart(my_grid, y_proba_binary_pre_game[0], title="Binary pre-game", is_binary=True)
    my_grid.empty()
    pred_pie_chart(my_grid, y_proba_binary_in_game[0], title="Binary in-game", is_binary=True)

    # Row 3
    pred_pie_chart(my_grid, b365_list, title="Bet365")
    my_grid.empty()
    pred_pie_chart(my_grid, iw_list, title="Interwetten ")
    my_grid.empty()
    pred_pie_chart(my_grid, wh_list, title="William Hill")

def match_graphs():
    st.markdown("##### Match Visualizations")
    my_grid = grid([1, 0.1, 1, 0.1, 1], [1, 0.1, 1, 0.1, 1], [1, 0.1, 1, 0.1, 1], vertical_align="top")

    # Row 1
    get_scored_goals_match_df(my_grid)
    my_grid.empty()

    get_shots_match_df(my_grid)
    my_grid.empty()

    get_corners_match_df(my_grid)

    # Row 2
    get_fouls_match_df(my_grid)
    my_grid.empty()

    get_yellow_cards_match_df(my_grid)
    my_grid.empty()

    get_red_cards_match_df(my_grid)

    # Row 3
    get_elo_match_df(my_grid)
    my_grid.empty()

    get_goals_current_season_match_df(my_grid)
    my_grid.empty()

    get_win_rate_current_season_match_df(my_grid)


def h2h_graphs():
    st.markdown("##### H2H Visualizations")
    my_grid = grid([1, 0.1, 1], [1, 0.1, 1, 0.1, 1], vertical_align="top")
    # Row 1
    get_h2h_rates_match_df(my_grid)
    my_grid.empty()
    get_h2h_goals_match_df(my_grid)
    # get_shots_match_df(my_grid)
    # my_grid.empty()
    #
    # get_corners_match_df(my_grid)
    #
    # # Row 2
    # get_fouls_match_df(my_grid)
    # my_grid.empty()
    #
    # get_yellow_cards_match_df(my_grid)
    # my_grid.empty()
    #
    # get_red_cards_match_df(my_grid)


def tabs_section():
    with st.container(border=False):
        tabs = ['Match Stats', 'H2H Stats', 'Odds vs Prediction', 'Past H2H Results']
        match_stats_tab, h2h_stats_tabs, odds_pred_tab, past_h2h_tab = st.tabs(tabs)

        with match_stats_tab:
            st.subheader("Match Stats", divider='gray')
            match_summary()
            match_graphs()

        with h2h_stats_tabs:
            st.subheader("H2H Stats", divider='gray')
            h2h_graphs()
        with odds_pred_tab:
            st.subheader("Odds vs Prediction", divider='gray')
            prediction_graphs()
        with past_h2h_tab:
            st.subheader("All H2H Results", divider='gray')
            past_h2h_df = get_filtered_df(league=st.session_state.selected_league, season=None,
                                          home_team=selected_row_data["HomeTeam"],
                                          away_team=selected_row_data["AwayTeam"], h2h=True)
            st.write("Retrieved results: ", past_h2h_df.shape[0])
            st.dataframe(past_h2h_df, selection_mode='single-row', hide_index=True)


match_date()
result_header()
tabs_section()
