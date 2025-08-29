from typing import Dict, Any, Callable
from langgraph.graph import StateGraph, END
from .supabase_client import insert_intake, patch_intake
from .nodes.types import Ctx
from .nodes import summarize as n_sum

State = Dict[str, Any]

def _wrap(fn: Callable[[Ctx], State]):
    def inner(state: State) -> State:
        return fn(Ctx(state))
    return inner

def build_graph():
    g = StateGraph(State)
    g.add_node("summarize", _wrap(n_sum))
    g.set_entry_point("summarize")
    g.add_edge("summarize", END)
    return g.compile()

GRAPH = build_graph()

def run_flow(user_id: str | None, raw_text: str, meta: dict) -> State:
    intake_id = insert_intake(user_id, raw_text, meta)
    init: State = {"intake_id": intake_id, "user_id": user_id, "raw_text": raw_text, "meta": meta}
    out = GRAPH.invoke(init)
    patch_intake(intake_id, {
        "status": out.get("status", "done"),
        "summary": out.get("summary")
    })
    return out | {"intake_id": intake_id}
