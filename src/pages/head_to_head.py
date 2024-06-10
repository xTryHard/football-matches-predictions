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
            'HomeTeam': 'Team', 'HomeTeamGoalsCurrentSeason': 'Goals Scored', 'HomeTeamGoalsConcededCurrentSeason': 'Goals Conceded'
        }),
        match_df[['AwayTeam', 'AwayTeamGoalsCurrentSeason', 'AwayTeamGoalsConcededCurrentSeason']].rename(columns={
            'AwayTeam': 'Team', 'AwayTeamGoalsCurrentSeason': 'Goals Scored', 'AwayTeamGoalsConcededCurrentSeason': 'Goals Conceded'
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
                 title='Goals Scored H2H', barmode='group')
    grid.plotly_chart(fig)


def get_h2h_rates_match_df(grid):
    matches = match_df["HeadToHeadMatches"].iloc[0]
    win_rate_data = match_df[['HeadToHeadHomeWinRate', 'HeadToHeadAwayWinRate', 'HeadToHeadDrawRate']]
    win_rate_data.rename(columns={
        'HeadToHeadHomeWinRate': 'Home Win Rate',
        'HeadToHeadAwayWinRate': 'Away Win Rate',
        'HeadToHeadDrawRate': 'Draw Rate'
    }, inplace=True)
    df_melted = win_rate_data.melt(var_name='Result', value_name='Rate')
    fig = px.pie(df_melted, names='Result', values='Rate', title=f'Head to Head Rates (on the {matches} previous matches)')
    grid.plotly_chart(fig)




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
