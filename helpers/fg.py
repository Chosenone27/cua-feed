# helpers/fg.py
# ──────────────────────────────────────────────────────────────────
import io
import requests
import pandas as pd
from datetime import datetime

FG_ROOT = "https://www.fangraphs.com/api/"

# ──────────────────────────────────────────────────────────────────
def _csv(url: str) -> pd.DataFrame:
    """Download a CSV from FanGraphs and trim spurious blank columns."""
    df = pd.read_csv(io.StringIO(requests.get(url).text))
    df.columns = df.columns.str.strip()        # rimuove eventuali spazi
    return df


# ──────────────────────────────────────────────────────────────────
def _ip_to_dec(ip) -> float:
    """
    Convert FanGraphs IP value (e.g. 5.2 = 5 inning + 2/3) to decimal inning.
    0.2 → 2/3 inning, 0.1 → 1/3 inning.
    """
    ip = float(ip)
    whole, frac = divmod(ip, 1)
    thirds = round(frac * 10)        # 1 → ⅓, 2 → ⅔
    return whole + thirds / 3


def _fix_era(df: pd.DataFrame) -> pd.DataFrame:
    """If ERA column is missing, compute it as (ER / IP) × 9."""
    if "ERA" not in df.columns and {"ER", "IP"}.issubset(df.columns):
        df = df.copy()
        ip_dec = df["IP"].apply(_ip_to_dec)
        # evita divisione per zero
        df["ERA"] = (df["ER"] / ip_dec.replace(0, pd.NA)) * 9
    return df


# ──────────────────────────────────────────────────────────────────
def starter_season(team_id: int) -> pd.DataFrame:
    """
    Season‑to‑date stats for the starting pitcher of the given team.
    Calcola ERA se non presente.
    """
    url = f"{FG_ROOT}teams/pitching?teamid={team_id}&split=season&csv=1"
    df = _csv(url)
    return _fix_era(df)


def starter_14days(team_id: int) -> pd.DataFrame:
    """
    14‑day trend stats for the starting pitcher of the given team.
    Calcola ERA se non presente.
    """
    url = f"{FG_ROOT}teams/pitching?teamid={team_id}&split=14day&csv=1"
    df = _csv(url)
    return _fix_era(df)


# ──────────────────────────────────────────────────────────────────
# Facoltativo: utility per ricerche veloci da notebook/shell
if __name__ == "__main__":
    tid_map = {"PIT": 134, "CWS": 190}  # esempi
    for abbr, tid in tid_map.items():
        print(f"\n=== {abbr} season ERA ===")
        print(starter_season(tid)[["player_name", "ERA"]].head())
