import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .schemas import IntakeIn
from .graph import run_flow

app = FastAPI(title="SmartProBono LangGraph MVP")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_methods=["*"], allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/intake/run")
def intake_run(payload: IntakeIn):
    return {"result": run_flow(payload.user_id, payload.full_text, payload.meta)}
