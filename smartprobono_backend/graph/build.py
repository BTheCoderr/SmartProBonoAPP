"""
LangGraph graph builder for SmartProBono multi-agent system
"""
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from .state import SPBState
from .nodes import (
    intake_node, 
    research_node, 
    drafting_node, 
    safety_node, 
    supervisor_node
)

def build_graph():
    """Build the SmartProBono multi-agent graph"""
    # Create the graph
    graph = StateGraph(SPBState)
    
    # Add nodes
    graph.add_node("intake", intake_node)
    graph.add_node("research", research_node)
    graph.add_node("draft", drafting_node)
    graph.add_node("safety", safety_node)
    graph.add_node("supervisor", supervisor_node)
    
    # Define the flow
    graph.add_edge(START, "intake")
    graph.add_edge("intake", "research")
    graph.add_edge("research", "draft")
    graph.add_edge("draft", "safety")
    graph.add_edge("safety", "supervisor")
    graph.add_edge("supervisor", END)
    
    # Compile with memory checkpointing
    return graph.compile(checkpointer=MemorySaver())

def build_simple_graph():
    """Build a simplified graph for testing"""
    graph = StateGraph(SPBState)
    
    # Add only essential nodes
    graph.add_node("intake", intake_node)
    graph.add_node("research", research_node)
    graph.add_node("draft", drafting_node)
    graph.add_node("safety", safety_node)
    
    # Simple linear flow
    graph.add_edge(START, "intake")
    graph.add_edge("intake", "research")
    graph.add_edge("research", "draft")
    graph.add_edge("draft", "safety")
    graph.add_edge("safety", END)
    
    return graph.compile()
