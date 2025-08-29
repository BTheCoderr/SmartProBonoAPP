"""
LangGraph nodes for SmartProBono multi-agent system
"""
import re
import time
from typing import Dict
from haystack import Pipeline
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rag.pipelines import build_query_pipeline
from utils.safety import needs_escalation
from utils.prompts import get_agent_prompts

# Shared RAG pipeline instance
RAG_PIPE: Pipeline = build_query_pipeline()

def intake_node(state: Dict) -> Dict:
    """Intake agent: normalize user questions, gather facts, flag jurisdiction"""
    query = state["query"]
    start_time = time.time()
    
    # Extract jurisdiction from query
    jurisdiction_patterns = [
        r"\b(MA|Massachusetts|RI|Rhode Island|CT|Connecticut|NY|New York|CA|California|TX|Texas|FL|Florida)\b",
        r"\b(federal|state|local)\b"
    ]
    
    jurisdiction = None
    for pattern in jurisdiction_patterns:
        match = re.search(pattern, query, flags=re.I)
        if match:
            jurisdiction = match.group(0)
            break
    
    # Determine if this is a complex legal question
    complex_keywords = [
        'lawsuit', 'litigation', 'court', 'trial', 'appeal',
        'contract dispute', 'employment law', 'criminal charges',
        'family law', 'immigration', 'bankruptcy'
    ]
    
    is_complex = any(keyword in query.lower() for keyword in complex_keywords)
    
    state.update({
        "jurisdiction": jurisdiction,
        "is_complex": is_complex,
        "intake_time": time.time() - start_time
    })
    
    return state

def research_node(state: Dict) -> Dict:
    """Research agent: Haystack pipeline for document retrieval"""
    start_time = time.time()
    
    try:
        # Run RAG pipeline
        result = RAG_PIPE.run({"q_embed": {"text": state["query"]}})
        
        docs = result["retrieve"]["documents"]
        state.update({
            "docs": docs,
            "research_time": time.time() - start_time,
            "docs_found": len(docs)
        })
        
    except Exception as e:
        print(f"Research error: {e}")
        state.update({
            "docs": [],
            "research_time": time.time() - start_time,
            "docs_found": 0,
            "research_error": str(e)
        })
    
    return state

def drafting_node(state: Dict) -> Dict:
    """Drafting agent: generate response using retrieved documents"""
    start_time = time.time()
    
    try:
        # Use the same RAG pipeline for generation
        result = RAG_PIPE.run({
            "q_embed": {"text": state["query"]}
        })
        
        reply = result["llm"]["replies"][0]
        
        # Extract citations
        citations = re.findall(r"\[(\d+)\]", reply)
        
        state.update({
            "draft": reply,
            "citations": citations,
            "drafting_time": time.time() - start_time
        })
        
    except Exception as e:
        print(f"Drafting error: {e}")
        state.update({
            "draft": "I'm sorry, I encountered an error generating a response. Please try again or consult with an attorney.",
            "citations": [],
            "drafting_time": time.time() - start_time,
            "drafting_error": str(e)
        })
    
    return state

def safety_node(state: Dict) -> Dict:
    """Safety agent: check outputs for unauthorized legal advice"""
    start_time = time.time()
    
    draft = state.get("draft", "")
    
    # Check for unauthorized practice of law
    escalate = needs_escalation(draft)
    
    # Calculate confidence based on available information
    confidence = 0.8 if state.get("docs_found", 0) > 0 else 0.3
    
    state.update({
        "escalate": escalate,
        "confidence": confidence,
        "safety_time": time.time() - start_time,
        "agent_used": "multi-agent-system"
    })
    
    return state

def supervisor_node(state: Dict) -> Dict:
    """Supervisor: route and enforce stop conditions"""
    start_time = time.time()
    
    # Add final metadata
    state.update({
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "processing_time": time.time() - start_time,
        "status": "completed"
    })
    
    return state
