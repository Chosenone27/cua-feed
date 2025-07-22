from helpers import sc, fg
import numpy as np

## --- Pitcher Starter ---

TEAM_ID_MAP = {"PIT": 23, "CWS": 5}  # aggiungi altri team se necessario

def build_pitcher_starter_pred(home_abbr: str, away_abbr: str):
    """Return dict di metriche PRED per starter di entrambe le squadre."""
    out = {}
    for abbr in (home_abbr, away_abbr):
        team_id = TEAM_ID_MAP[abbr]
        # Stagionale
        df_season = fg.starter_season(team_id)
        era_season = df_season["ERA"].iloc[0]
        # Trend 14 giorni
        df_trend = fg.starter_14days(team_id)
        era_trend = df_trend["ERA"].iloc[0]
        side = "HOME" if abbr == home_abbr else "AWAY"
        out[f"ERA_{side}_PRED"] = round(era_season * 0.35 + era_trend * 0.65, 2)
    return out

def build_pitcher_starter_game(game_pk: str):
    df = sc.game_statcast(game_pk)
    out = {}
    for side, home in (("HOME", True), ("AWAY", False)):
        box = sc.starter_boxscore(df, home)
        ip = box["inning"].max()          # semplificazione
        er = box["events"].notna().sum()
        era_game = (er / ip) * 9 if ip else np.nan
        out[f"ERA_{side}_GAME"] = round(era_game, 2)
    return out

# -------- builder di alto livello --------
def build_core_pred(game_id: str):
    home, away = game_id.split("@")[1], game_id.split("@")[0][-3:]
    metrics = {}
    metrics.update(build_pitcher_starter_pred(home, away))
    return metrics

def build_core_game(game_pk: str):
    return build_pitcher_starter_game(game_pk)

