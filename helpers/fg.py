import pandas as pd, io, requests

FG_ROOT = "https://www.fangraphs.com/api/"

def _csv(url: str) -> pd.DataFrame:
    return pd.read_csv(io.StringIO(requests.get(url).text))

def starter_season(team_id: int) -> pd.DataFrame:
    url = f"{FG_ROOT}teams/pitching?teamid={team_id}&split=season&csv=1"
    return _csv(url)

def starter_14days(team_id: int) -> pd.DataFrame:
    url = f"{FG_ROOT}teams/pitching?teamid={team_id}&split=14days&csv=1"
    return _csv(url)
