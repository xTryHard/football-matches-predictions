import streamlit as st
from menu import menu
from streamlit_extras.row import row
from datetime import datetime
import calendar

from utils import get_league_df, bundesliga, laliga, pl, seriea, ligue1
from badges import bundesliga_badges, laliga_badges, pl_badges, seriea_badges, ligue1_badges

if 'selected_league' not in st.session_state or 'selected_row' not in st.session_state:
    st.switch_page('app.py')

st.session_state.h2h_button_disabled = True
menu()

df = get_league_df(st.session_state.selected_league)
selected_row_data = st.session_state.selected_row

st.title('Match and Past H2H encounters')
st.write("See details of the current and past matches between the selected teams")
st.divider()


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
                result_row = row([1, 2, 1], vertical_align="top", gap="small")
                result_row.markdown(f"#### {selected_row_data['FTHG']}")
                result_row.markdown("#### Full time result")
                result_row.markdown(f"#### {selected_row_data['FTAG']}")
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


match_date()
result_header()
