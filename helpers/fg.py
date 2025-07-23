import pandas as pd, io, requests
from datetime import datetime

FG_ROOT = "https://www.fangraphs.com/api/"

# ---------- funzioni di utilità ---------- #
def _csv(url: str) -> pd.DataFrame:
    """Scarica un CSV da FanGraphs e normalizza i nomi colonna."""
    df = pd.read_csv(io.StringIO(requests.get(url).text))
    # rimuove spazi / TAB a destra–sinistra dei nomi
    df.columns = df.columns.str.strip()
    return df

def _ensure_era(df: pd.DataFrame) -> pd.DataFrame:
    """
    Assicura la presenza della colonna ERA.
    Se mancano ERA o IP/ER prova a ricavarle, altrimenti lascia NaN.
    """
    cols = df.columns
    if "ERA" not in cols:
        if {"ER", "IP"}.issubset(cols):
            # IP potrebbe essere "0.0": evito div/0
            df["ERA"] = (df["ER"] / df["IP"].replace(0, pd.NA)) * 9
        else:
            # inserisco colonna ERA piena di NaN per evitare KeyError
            df["ERA"] = pd.NA
    return df

# ---------- endpoint di download ---------- #
def starter_season(team_id: int) -> pd.DataFrame:
    """Statistiche stagione‐corrente per il partente della squadra indicata."""
    url = f"{FG_ROOT}teams/pitching?teamid={team_id}&split=season&csv=1"
    return _ensure_era(_csv(url))

def starter_14days(team_id: int) -> pd.DataFrame:
    """Statistiche ultime 14 giorni per il partente della squadra indicata."""
    url = f"{FG_ROOT}teams/pitching?teamid={team_id}&split=14day&csv=1"
    return _ensure_era(_csv(url))

# Facoltativo: test rapido da shell
if __name__ == "__main__":
    tid_map = {"PIT": 134, "CWS": 190}
    for abbr, tid in tid_map.items():
        print(f"\n--- {abbr} season ERA ---")
        print(starter_season(tid)[["Player_Name", "ERA"]].head())
