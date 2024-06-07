import streamlit as st
from menu import menu
from streamlit_extras.row import row
from streamlit_extras.grid import grid
from streamlit_extras.chart_container import chart_container
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
    grid.bar_chart(goals_data, x="Team", y=["Full Time Goals", "Half Time Goals"], color=["#e63946", "#0077b6"])


def get_shots_match_df(grid):
    shots_data = pd.concat([
        match_df[['HomeTeam', 'HS']].rename(columns={
            'HomeTeam': 'Team', 'HS': 'Shots'
        }),
        match_df[['AwayTeam', 'AS']].rename(columns={
            'AwayTeam': 'Team', 'AS': 'Shots'
        })
    ], ignore_index=True)
    grid.bar_chart(shots_data, x="Team", y='Shots', color=["#0077b6"])


def get_corners_match_df(grid):
    corners_data = pd.concat([
        match_df[['HomeTeam', 'HC']].rename(columns={
            'HomeTeam': 'Team', 'HC': 'Corners'
        }),
        match_df[['AwayTeam', 'AC']].rename(columns={
            'AwayTeam': 'Team', 'AC': 'Corners'
        })
    ], ignore_index=True)
    grid.bar_chart(corners_data, x="Team", y='Corners', color=["#e63946"])


def get_fouls_match_df(grid):
    fouls_data = pd.concat([
        match_df[['HomeTeam', 'HF']].rename(columns={
            'HomeTeam': 'Team', 'HF': 'Fouls Committed'
        }),
        match_df[['AwayTeam', 'AF']].rename(columns={
            'AwayTeam': 'Team', 'AF': 'Fouls Committed'
        })
    ], ignore_index=True)
    grid.bar_chart(fouls_data, x="Team", y='Fouls Committed', color=["#a8dadc"])


def get_yellow_cards_match_df(grid):
    yellow_cards_data = pd.concat([
        match_df[['HomeTeam', 'HY']].rename(columns={
            'HomeTeam': 'Team', 'HY': 'Yellow Cards'
        }),
        match_df[['AwayTeam', 'AY']].rename(columns={
            'AwayTeam': 'Team', 'AY': 'Yellow Cards'
        })
    ], ignore_index=True)
    grid.bar_chart(yellow_cards_data, x="Team", y='Yellow Cards', color=["#e9c46a"])


def get_red_cards_match_df(grid):
    red_cards_data = pd.concat([
        match_df[['HomeTeam', 'HR']].rename(columns={
            'HomeTeam': 'Team', 'HR': 'Red Cards'
        }),
        match_df[['AwayTeam', 'AR']].rename(columns={
            'AwayTeam': 'Team', 'AR': 'Red Cards'
        })
    ], ignore_index=True)
    grid.bar_chart(red_cards_data, x="Team", y='Red Cards', color=["#e63946"])


def graphs():
    st.markdown("##### Match Visualizations")
    my_grid = grid([1, 0.1, 1, 0.1, 1], [1, 0.1, 1, 0.1, 1], [1, 0.1, 1, 0.1, 1], [1, 0.1, 1, 0.1, 1],
                   vertical_align="top")

    # Row 1
    my_grid.text("Full Time and Half Time Goals by Team")
    my_grid.empty()
    my_grid.text("Shots by Team")
    my_grid.empty()
    my_grid.text("Corners by Team")

    get_scored_goals_match_df(my_grid)
    my_grid.empty()

    get_shots_match_df(my_grid)
    my_grid.empty()

    get_corners_match_df(my_grid)

    # Row 2
    my_grid.text("Fouls Committed by Team")
    my_grid.empty()
    my_grid.text("Yellow Cards by Team")
    my_grid.empty()
    my_grid.text("Red Cards by Team")

    get_fouls_match_df(my_grid)
    my_grid.empty()

    get_yellow_cards_match_df(my_grid)
    my_grid.empty()

    get_red_cards_match_df(my_grid)


def tabs_section():
    with st.container(border=False):
        tabs = ['Match Stats', 'H2H Stats', 'Odds vs Prediction', 'Past H2H Results']
        match_stats_tab, h2h_stats_tabs, odds_pred_tab, past_h2h_tab = st.tabs(tabs)

        with match_stats_tab:
            st.subheader("Match Stats", divider='gray')
            match_summary()
            graphs()

        with h2h_stats_tabs:
            st.subheader("H2H Stats", divider='gray')

        with odds_pred_tab:
            st.subheader("Odds vs Prediction", divider='gray')

        with past_h2h_tab:
            st.subheader("Past H2H Results", divider='gray')
            past_h2h_df = get_filtered_df(league=st.session_state.selected_league, season=None,
                                          home_team=selected_row_data["HomeTeam"],
                                          away_team=selected_row_data["AwayTeam"], h2h=True)
            st.write("Retrieved results: ", past_h2h_df.shape[0])
            st.dataframe(past_h2h_df, selection_mode='single-row', hide_index=True)


match_date()
result_header()
tabs_section()
