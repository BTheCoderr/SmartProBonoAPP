"""
Advanced LangGraph Implementation for SmartProBono
Based on official LangGraph documentation patterns
"""

from typing import Dict, Any, Callable, Literal
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
from .supabase_client import insert_intake, patch_intake
from .nodes.types import Ctx
from .human_in_loop import require_human_review
from .parallel_execution import parallel_specialists, specialist_pool

# Define state structure (following official patterns)
class SmartProBonoState(Dict[str, Any]):
    """State for SmartProBono legal intake workflow"""
    intake_id: str
    user_id: str | None
    raw_text: str
    meta: dict
    
    # Workflow state
    case_type: str | None = None
    summary: str | None = None
    specialist_analysis: str | None = None
    plain_english_answer: str | None = None
    
    # Quality control
    needs_revision: bool = False
    revision_count: int = 0
    max_revisions: int = 2
    
    # Status tracking
    status: str = "started"
    current_step: str = "intake"

def _wrap(fn: Callable[[Ctx], SmartProBonoState]):
    """Wrapper to convert Ctx-based functions to state-based functions"""
    def inner(state: SmartProBonoState) -> SmartProBonoState:
        return fn(Ctx(state))
    return inner

# Node Functions (following official patterns)
def classify_case_type(ctx: Ctx) -> SmartProBonoState:
    """Classifier node - determines case type"""
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    
    system_prompt = """
    You are a legal case classifier. Analyze the user's legal question and classify it into one of these categories:
    - criminal: Criminal law, charges, pleas, appeals
    - housing: Landlord-tenant, eviction, lease disputes
    - family: Divorce, custody, domestic issues
    - employment: Workplace issues, discrimination, wages
    - immigration: Visa, citizenship, deportation
    - other: Any other legal matter
    
    Respond with ONLY the category name.
    """
    
    response = llm.invoke([
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": ctx.state["raw_text"]}
    ])
    
    ctx.state["case_type"] = response.content.strip().lower()
    ctx.state["current_step"] = "classified"
    return ctx.state

@parallel_specialists(["criminal_lawyer", "criminal_procedure_expert"])
def criminal_specialist(ctx: Ctx) -> SmartProBonoState:
    """Criminal law specialist node with parallel execution"""
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    
    system_prompt = """
    You are a criminal law specialist. Provide detailed legal analysis for criminal law questions.
    Include relevant statutes, case law, and practical implications.
    Be thorough but accessible.
    """
    
    response = llm.invoke([
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": ctx.state["raw_text"]}
    ])
    
    ctx.state["specialist_analysis"] = response.content
    ctx.state["current_step"] = "specialist_analysis"
    return ctx.state

@parallel_specialists(["housing_lawyer", "tenant_rights_expert"])
def housing_specialist(ctx: Ctx) -> SmartProBonoState:
    """Housing law specialist node with parallel execution"""
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    
    system_prompt = """
    You are a housing law specialist. Provide detailed legal analysis for landlord-tenant and housing questions.
    Include relevant state laws, tenant rights, and practical steps.
    Be thorough but accessible.
    """
    
    response = llm.invoke([
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": ctx.state["raw_text"]}
    ])
    
    ctx.state["specialist_analysis"] = response.content
    ctx.state["current_step"] = "specialist_analysis"
    return ctx.state

@parallel_specialists(["family_lawyer", "divorce_specialist"])
def family_specialist(ctx: Ctx) -> SmartProBonoState:
    """Family law specialist node with parallel execution"""
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    
    system_prompt = """
    You are a family law specialist. Provide detailed legal analysis for family law questions.
    Include relevant laws, procedures, and practical considerations.
    Be thorough but accessible.
    """
    
    response = llm.invoke([
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": ctx.state["raw_text"]}
    ])
    
    ctx.state["specialist_analysis"] = response.content
    ctx.state["current_step"] = "specialist_analysis"
    return ctx.state

def other_specialist(ctx: Ctx) -> SmartProBonoState:
    """General legal specialist node"""
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    
    system_prompt = """
    You are a general legal specialist. Provide detailed legal analysis for general legal questions.
    Include relevant laws, procedures, and practical considerations.
    Be thorough but accessible.
    """
    
    response = llm.invoke([
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": ctx.state["raw_text"]}
    ])
    
    ctx.state["specialist_analysis"] = response.content
    ctx.state["current_step"] = "specialist_analysis"
    return ctx.state

@require_human_review("critic_review", "quality_check", timeout_minutes=30)
def critic_review(ctx: Ctx) -> SmartProBonoState:
    """Critic node - reviews specialist analysis with human oversight"""
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    
    system_prompt = """
    You are a legal quality reviewer. Review the specialist analysis and determine if it needs revision.
    Check for:
    1. Accuracy and completeness
    2. Clarity and accessibility
    3. Missing important details
    4. Appropriate tone for non-lawyers
    
    Respond with "APPROVE" if the analysis is good, or "REVISE" if it needs improvement.
    If REVISE, provide specific feedback on what needs to be improved.
    """
    
    response = llm.invoke([
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Original question: {ctx.state['raw_text']}\n\nSpecialist analysis: {ctx.state['specialist_analysis']}"}
    ])
    
    if "REVISE" in response.content.upper():
        ctx.state["needs_revision"] = True
        ctx.state["revision_count"] += 1
    else:
        ctx.state["needs_revision"] = False
    
    ctx.state["current_step"] = "critic_review"
    return ctx.state

def rewriter(ctx: Ctx) -> SmartProBonoState:
    """Rewriter node - improves specialist analysis"""
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    
    system_prompt = """
    You are a legal writing specialist. Improve the specialist analysis based on the critic's feedback.
    Make it more accurate, complete, clear, and accessible to non-lawyers.
    Maintain all the important legal information while improving presentation.
    """
    
    response = llm.invoke([
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Original question: {ctx.state['raw_text']}\n\nCurrent analysis: {ctx.state['specialist_analysis']}\n\nCritic feedback: {ctx.state.get('critic_feedback', 'Improve clarity and accessibility')}"}
    ])
    
    ctx.state["specialist_analysis"] = response.content
    ctx.state["current_step"] = "rewritten"
    return ctx.state

def plain_english_explainer(ctx: Ctx) -> SmartProBonoState:
    """Plain English explainer node"""
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    
    system_prompt = """
    You are a legal communication specialist. Convert the specialist analysis into plain English that any person can understand.
    Use simple language, avoid legal jargon, and provide practical next steps.
    Include a disclaimer that this is not legal advice.
    """
    
    response = llm.invoke([
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Original question: {ctx.state['raw_text']}\n\nSpecialist analysis: {ctx.state['specialist_analysis']}"}
    ])
    
    ctx.state["plain_english_answer"] = response.content
    ctx.state["current_step"] = "explained"
    ctx.state["status"] = "completed"
    return ctx.state

# Routing Functions (following official patterns)
def route_by_case_type(state: SmartProBonoState) -> Literal["criminal_specialist", "housing_specialist", "family_specialist", "other_specialist"]:
    """Route to appropriate specialist based on case type"""
    case_type = state.get("case_type", "other")
    
    if case_type == "criminal":
        return "criminal_specialist"
    elif case_type == "housing":
        return "housing_specialist"
    elif case_type == "family":
        return "family_specialist"
    else:
        return "other_specialist"

def route_after_critic(state: SmartProBonoState) -> Literal["rewriter", "plain_english_explainer"]:
    """Route after critic review - revise or proceed to explainer"""
    if state.get("needs_revision", False) and state.get("revision_count", 0) < state.get("max_revisions", 2):
        return "rewriter"
    else:
        return "plain_english_explainer"

def route_after_rewriter(state: SmartProBonoState) -> Literal["critic_review", "plain_english_explainer"]:
    """Route after rewriter - back to critic or proceed"""
    if state.get("revision_count", 0) >= state.get("max_revisions", 2):
        return "plain_english_explainer"  # Max revisions reached
    else:
        return "critic_review"  # Back to critic for another review

# Graph Builder (following official patterns)
def build_advanced_graph():
    """Build the advanced SmartProBono graph with official LangGraph patterns"""
    
    # Create the graph
    g = StateGraph(SmartProBonoState)
    
    # Add nodes
    g.add_node("classify", _wrap(classify_case_type))
    g.add_node("criminal_specialist", _wrap(criminal_specialist))
    g.add_node("housing_specialist", _wrap(housing_specialist))
    g.add_node("family_specialist", _wrap(family_specialist))
    g.add_node("other_specialist", _wrap(other_specialist))
    g.add_node("critic_review", _wrap(critic_review))
    g.add_node("rewriter", _wrap(rewriter))
    g.add_node("plain_english_explainer", _wrap(plain_english_explainer))
    
    # Set entry point
    g.set_entry_point("classify")
    
    # Add conditional edges (official pattern)
    g.add_conditional_edges(
        "classify",
        route_by_case_type,
        {
            "criminal_specialist": "criminal_specialist",
            "housing_specialist": "housing_specialist",
            "family_specialist": "family_specialist",
            "other_specialist": "other_specialist"
        }
    )
    
    # All specialists go to critic
    g.add_edge("criminal_specialist", "critic_review")
    g.add_edge("housing_specialist", "critic_review")
    g.add_edge("family_specialist", "critic_review")
    g.add_edge("other_specialist", "critic_review")
    
    # Critic routes to rewriter or explainer
    g.add_conditional_edges(
        "critic_review",
        route_after_critic,
        {
            "rewriter": "rewriter",
            "plain_english_explainer": "plain_english_explainer"
        }
    )
    
    # Rewriter routes back to critic or to explainer
    g.add_conditional_edges(
        "rewriter",
        route_after_rewriter,
        {
            "critic_review": "critic_review",
            "plain_english_explainer": "plain_english_explainer"
        }
    )
    
    # Explainer goes to end
    g.add_edge("plain_english_explainer", END)
    
    return g.compile()

# Create the advanced graph
ADVANCED_GRAPH = build_advanced_graph()

def run_advanced_flow(user_id: str | None, raw_text: str, meta: dict) -> SmartProBonoState:
    """Run the advanced SmartProBono workflow"""
    
    # Insert intake record
    intake_id = insert_intake(user_id, raw_text, meta)
    
    # Initialize state
    initial_state: SmartProBonoState = {
        "intake_id": intake_id,
        "user_id": user_id,
        "raw_text": raw_text,
        "meta": meta,
        "case_type": None,
        "summary": None,
        "specialist_analysis": None,
        "plain_english_answer": None,
        "needs_revision": False,
        "revision_count": 0,
        "max_revisions": 2,
        "status": "started",
        "current_step": "intake"
    }
    
    # Run the graph
    result = ADVANCED_GRAPH.invoke(initial_state)
    
    # Update database
    patch_intake(intake_id, {
        "status": result.get("status", "completed"),
        "summary": result.get("plain_english_answer"),
        "case_type": result.get("case_type"),
        "specialist_analysis": result.get("specialist_analysis")
    })
    
    return result
