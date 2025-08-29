from pydantic import BaseModel, Field
from typing import Optional, Dict, Any

class IntakeIn(BaseModel):
    user_id: Optional[str] = None
    full_text: str
    meta: Dict[str, Any] = Field(default_factory=dict)
