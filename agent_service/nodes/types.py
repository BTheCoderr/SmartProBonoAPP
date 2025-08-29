from typing import Any, Dict
from supabase import Client
from ..supabase_client import sb

class Ctx:
    def __init__(self, state: Dict[str, Any]):
        self.state = state
        self.supabase: Client = sb()
