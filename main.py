from fastapi import FastAPI
from fastapi.responses import JSONResponse
from metrics_core import build_core_pred, build_core_game

app = FastAPI(title="CUA Operator")

@app.api_route("/metrics", methods=["GET", "POST"])
async def metrics(payload: dict | None = None,
                  game_id: str | None = None,
                  post: bool = False):
    """
    • POST  body JSON → {"game_id": "...", "post": false}
    • GET   query      → /metrics?game_id=...&post=true
    """
    # recupera parametri a prescindere dal metodo
    if payload is None:
        payload = {}
    if game_id:
        payload["game_id"] = game_id
    payload.setdefault("post", post)

    gid = payload.get("game_id", "")
    if payload.get("post"):
        core = build_core_game(gid.split("_")[0])
        suffix = "_GAME"
    else:
        core = build_core_pred(gid)
        suffix = "_PRED"

    return JSONResponse({f"{k}{suffix}" if not k.endswith(suffix) else k: v
                         for k, v in core.items()})
