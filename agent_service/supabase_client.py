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
