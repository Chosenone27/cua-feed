import pandas as pd
from datetime import datetime, timedelta
from pybaseball import statcast_single_game, statcast

def game_statcast(game_pk: str) -> pd.DataFrame:
    """Download Statcast data for a single gamePk."""
    return statcast_single_game(game_pk)

def starter_boxscore(game_df: pd.DataFrame, home: bool) -> pd.DataFrame:
    """Return rows for the starting pitcher (home=True/False) in that game dataframe."""
    home_team = game_df["home_team_name"].iloc[0]
    away_team = game_df["away_team_name"].iloc[0]
    team = home_team if home else away_team
    starter_name = (
        game_df[game_df["pitcher_team_name"] == team]
        .sort_values("inning", ascending=True)
        .iloc[0]["player_name"]
    )
    return game_df[game_df["player_name"] == starter_name]

def season_statcast(team_abbr: str) -> pd.DataFrame:
    """Return Statcast data for this team in the current season (year to date)."""
    year = datetime.now().year
    return statcast(start=f"{year}-03-01", end=datetime.now().strftime("%Y-%m-%d"), team=team_abbr)
