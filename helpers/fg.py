import pandas as pd, io, requests
from datetime import datetime

FG_ROOT = "https://www.fangraphs.com/api/"

def _csv(url: str) -> pd.DataFrame:
    """Download a CSV from FanGraphs and strip spurious blank columns."""
    df = pd.read_csv(io.StringIO(requests.get(url).text))
    df.columns = df.columns.str.strip()           # rimuove eventuali spazi
    return df


def _fix_era(df: pd.DataFrame) -> pd.DataFrame:
    """
    Assicura che la colonna ERA sia sempre presente.
    Se manca, la ricava da ER e IP ( 9 * ER / IP ).
    """
    if "ERA" not in df:
        if {"ER", "IP"}.issubset(df.columns):
            # Calcola ERA; sostituisce divisioni per zero con NaN
            df["ERA"] = (9 * df["ER"] / df["IP"]).replace([float("inf"), -float("inf")], pd.NA)
        else:
            # Se mancano i dati necessari, crea la colonna vuota
            df["ERA"] = pd.NA
    return df


def starter_season(team_id: int) -> pd.DataFrame:
    """
    Season‑to‑date stats for the starting pitcher of the given team.
    Calcola ERA se non presente.
    """
    url = f"{FG_ROOT}teams/pitching?teamid={team_id}&split=season&csv=1"
    df  = _csv(url)
    return _fix_era(df)


def starter_14days(team_id: int) -> pd.DataFrame:
    """
    14‑day trend stats for the starting pitcher of the given team.
    Calcola ERA se non presente.
    """
    url = f"{FG_ROOT}teams/pitching?teamid={team_id}&split=14day&csv=1"
    df  = _csv(url)
    return _fix_era(df)


# ----------------------------------------------------------------------
# (facoltativo) quick‑test da notebook/shell
if __name__ == "__main__":
    tid_map = {"PIT": 134, "CWS": 190}  # esempi
    for abbr, tid in tid_map.items():
        print(f"\n=== {abbr} season ERA ===")
        print(starter_season(tid)[["Player_name", "ERA"]].head())
