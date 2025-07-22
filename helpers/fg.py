import pandas as pd, io, requests
from datetime import datetime

FG_ROOT = "https://www.fangraphs.com/api/"

def _csv(url: str) -> pd.DataFrame:
    """Download a CSV from FanGraphs and trim spurious blank columns."""
    df = pd.read_csv(io.StringIO(requests.get(url).text))
    df.columns = df.columns.str.strip()         # rimuove eventuali spazi
    return df

def starter_season(team_id: int) -> pd.DataFrame:
    """
    Season‑to‑date stats for the starting pitcher of the given team.
    • Calcola ERA se non presente.
    """
    url = f"{FG_ROOT}teams/pitching?teamid={team_id}&split=season&csv=1"
    df = _csv(url)

    # Assicura presenza ERA
    if "ERA" not in df:
        if {"ER", "IP"}.issubset(df.columns):
            df["ERA"] = (df["ER"] / df["IP"].replace(0, pd.NA)) * 9
        else:
            raise ValueError("ERA columns missing in FanGraphs feed")

    return df.head(1)          # torna solo riga aggregata

def starter_14days(team_id: int) -> pd.DataFrame:
    """Last‑14‑days stats for the starting pitcher of the team."""
    url = f"{FG_ROOT}teams/pitching?teamid={team_id}&split=14days&csv=1"
    df = _csv(url)
    if "ERA" not in df:
        if {"ER", "IP"}.issubset(df.columns):
            df["ERA"] = (df["ER"] / df["IP"].replace(0, pd.NA)) * 9
        else:
            raise ValueError("ERA columns missing in FanGraphs feed")
    return df.head(1)
