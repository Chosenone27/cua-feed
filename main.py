from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI(title="CUA Operator Placeholder")

@app.post("/metrics")
async def metrics(payload: dict):
    """
    Endpoint provvisorio.
    Accetta un body JSON (payload) e restituisce due campi fittizi.
    """
    return JSONResponse(
        content={
            "ERA_HOME_PRED": 3.79,
            "ERA_AWAY_PRED": 4.44
        }
    )

