import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .schemas import IntakeIn
from .graph import run_flow
from .graph_advanced import run_advanced_flow
from .human_in_loop import create_review_endpoint

# Enable LangSmith tracing for debugging
os.environ.setdefault("LANGCHAIN_TRACING_V2", "true")
os.environ.setdefault("LANGCHAIN_PROJECT", "SmartProBono-Advanced")

# Enable advanced features
os.environ.setdefault("ENABLE_HUMAN_REVIEW", "true")
os.environ.setdefault("ENABLE_PARALLEL_EXECUTION", "true")

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
    """Simple intake flow (original implementation)"""
    return {"result": run_flow(payload.user_id, payload.full_text, payload.meta)}

@app.post("/intake/advanced")
def intake_advanced(payload: IntakeIn):
    """Advanced multi-agent intake flow with LangGraph patterns"""
    return {"result": run_advanced_flow(payload.user_id, payload.full_text, payload.meta)}

@app.get("/intake/status/{intake_id}")
def get_intake_status(intake_id: str):
    """Get the status of a specific intake"""
    from .supabase_client import get_intake
    try:
        intake = get_intake(intake_id)
        return {"intake": intake}
    except Exception as e:
        return {"error": str(e), "intake_id": intake_id}

@app.get("/intakes")
def list_intakes(user_id: str = None, limit: int = 10):
    """List recent intakes"""
    from .supabase_client import list_intakes
    try:
        intakes = list_intakes(user_id, limit)
        return {"intakes": intakes}
    except Exception as e:
        return {"error": str(e)}

@app.get("/graph/info")
def graph_info():
    """Get information about the available graphs"""
    return {
        "graphs": {
            "simple": {
                "description": "Basic summarization workflow",
                "endpoint": "/intake/run"
            },
            "advanced": {
                "description": "Multi-agent workflow with classification, specialists, critic, and explainer",
                "endpoint": "/intake/advanced",
                "features": [
                    "Case type classification",
                    "Specialist routing (criminal, housing, family, other)",
                    "Quality review with critic",
                    "Revision loops with limits",
                    "Plain English explanation"
                ]
            }
        },
        "langsmith_tracing": os.environ.get("LANGCHAIN_TRACING_V2") == "true",
        "human_review_enabled": os.environ.get("ENABLE_HUMAN_REVIEW") == "true",
        "parallel_execution_enabled": os.environ.get("ENABLE_PARALLEL_EXECUTION") == "true"
    }

# Add human review endpoints
create_review_endpoint(app)
