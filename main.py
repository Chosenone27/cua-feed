from fastapi import FastAPI
from fastapi.responses import JSONResponse

# importa i builder reali
from metrics_core import build_core_pred, build_core_game

app = FastAPI(title="CUA Operator")

@app.post("/metrics")
async def metrics(payload: dict):
    """
    Gateway per le metriche.
    Body JSON atteso: {"game_id": "<GAME_ID>", "post": false}
    • se post == false → restituisce *_PRED
    • se post == true  → restituisce *_GAME  (singola partita)
    """
    game_id = payload.get("game_id", "")
    post_mode = payload.get("post", False)

    if post_mode:
        # per ora ci serve solo ERA_GAME; useremo game_pk = parte prima dell’underscore
        core = build_core_game(game_id.split("_")[0])
        suffix = "_GAME"
    else:
        core = build_core_pred(game_id)
        suffix = "_PRED"

    # rinomina chiavi in modo coerente (es.: ERA_HOME_PRED)
    metrics_out = {f"{k}{suffix}" if not k.endswith(suffix) else k: v
                   for k, v in core.items()}

    return JSONResponse(content=metrics_out)
