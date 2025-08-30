import os
from supabase import create_client, Client

SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_KEY = os.environ["SUPABASE_SERVICE_ROLE_KEY"]

def sb() -> Client:
    return create_client(SUPABASE_URL, SUPABASE_KEY)

def insert_intake(user_id: str | None, raw_text: str, meta: dict):
    return sb().table("case_intakes").insert({
        "user_id": user_id, "raw_text": raw_text, "meta": meta, "status": "started"
    }).execute().data[0]["id"]

def patch_intake(intake_id: str, patch: dict):
    sb().table("case_intakes").update(patch).eq("id", intake_id).execute()

def get_intake(intake_id: str):
    """Get a specific intake by ID"""
    result = sb().table("case_intakes").select("*").eq("id", intake_id).execute()
    if result.data:
        return result.data[0]
    else:
        raise ValueError(f"Intake {intake_id} not found")

def list_intakes(user_id: str | None = None, limit: int = 10):
    """List intakes, optionally filtered by user_id"""
    query = sb().table("case_intakes").select("*").order("created_at", desc=True).limit(limit)
    if user_id:
        query = query.eq("user_id", user_id)
    return query.execute().data
