"""
LangGraph state definition for SmartProBono multi-agent system
"""
from typing import TypedDict, List, Optional, Any

class SPBState(TypedDict, total=False):
    """State for SmartProBono multi-agent system"""
    # Input
    query: str
    user_id: Optional[str]
    
    # Processing
    jurisdiction: Optional[str]
    messages: List[dict]        # chat history
    docs: List[Any]            # retrieved documents
    draft: str                 # generated response
    citations: List[str]       # citation references
    
    # Safety and routing
    escalate: bool             # needs human review
    agent_used: str           # which agent handled the request
    confidence: float         # confidence score
    
    # Metadata
    timestamp: str
    processing_time: float
