import pandas as pd


def get_dataframes():
    df_bundesliga = pd.read_csv('src\data\dataset_bundesliga.csv', encoding='utf-8')
    df_laliga = pd.read_csv('src\data\dataset_laliga.csv', encoding='utf-8')
    df_pl = pd.read_csv('src\data\dataset_premier.csv', encoding='windows-1252')
    df_seriea = pd.read_csv('src\data\dataset_seriea.csv', encoding='utf-8')
    df_ligue1 = pd.read_csv('src\data\dataset_ligue1.csv', encoding='utf-8')

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


bundesliga = 'Bundesliga'
laliga = 'La Liga EA Sports'
pl = 'Premier League'
seriea = 'Seria A TIM'
ligue1 = "Ligue 1 McDonald's"
