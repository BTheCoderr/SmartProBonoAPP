# LangGraph Learning Guide for SmartProBono

Based on the [official LangGraph documentation](https://langchain-ai.github.io/langgraph/), this guide shows how to implement advanced multi-agent patterns in your SmartProBono application.

## 🎯 Official LangGraph Core Benefits

### 1. **Durable Execution**
- Agents persist through failures and resume exactly where they left off
- Built-in checkpointing for long-running workflows
- Automatic recovery from interruptions

### 2. **Human-in-the-Loop**
- Inspect and modify agent state at any point during execution
- Pause workflows for human input or approval
- Real-time monitoring and intervention

### 3. **Comprehensive Memory**
- Short-term working memory for ongoing reasoning
- Long-term persistent memory across sessions
- State management across multiple agents

### 4. **Debugging with LangSmith**
- Deep visibility into agent behavior
- Execution path visualization
- State transition tracking
- Runtime metrics and performance analysis

### 5. **Production-Ready Deployment**
- Scalable infrastructure for stateful workflows
- Built-in error handling and retry logic
- Monitoring and observability tools

## 🏗️ Your Current vs. Advanced Implementation

### **Current Implementation** (`agent_service/graph.py`)
```python
# Simple linear graph
g = StateGraph(State)
g.add_node("summarize", _wrap(n_sum))
g.set_entry_point("summarize")
g.add_edge("summarize", END)
```

### **Advanced Implementation** (`agent_service/graph_advanced.py`)
```python
# Multi-agent graph with conditional routing and loops
g = StateGraph(SmartProBonoState)
g.add_node("classify", _wrap(classify_case_type))
g.add_node("criminal_specialist", _wrap(criminal_specialist))
g.add_node("housing_specialist", _wrap(housing_specialist))
g.add_node("family_specialist", _wrap(family_specialist))
g.add_node("other_specialist", _wrap(other_specialist))
g.add_node("critic_review", _wrap(critic_review))
g.add_node("rewriter", _wrap(rewriter))
g.add_node("plain_english_explainer", _wrap(plain_english_explainer))

# Conditional routing
g.add_conditional_edges("classify", route_by_case_type, {...})
g.add_conditional_edges("critic_review", route_after_critic, {...})
g.add_conditional_edges("rewriter", route_after_rewriter, {...})
```

## 🔄 Official LangGraph Patterns Implemented

### **Pattern 1: Supervisor/Worker Architecture**
```
[User Input] → [Classifier] → [Specialist Agent] → [Critic] → [Explainer] → [Output]
```

**How it works:**
- **Supervisor** (Classifier): Routes cases to appropriate specialists
- **Workers** (Specialists): Handle specific legal domains
- **Quality Control** (Critic): Reviews and ensures quality
- **Finalizer** (Explainer): Converts to plain English

### **Pattern 2: Critic & Revision Loop**
```
[Specialist] → [Critic] → [Rewriter] → [Critic] → [Explainer]
                ↑                        ↓
                └─── (if needs revision) ─┘
```

**How it works:**
- **Critic** reviews specialist analysis
- **Conditional routing** based on quality assessment
- **Loop back** to rewriter if revision needed
- **Max revision limit** to prevent infinite loops

### **Pattern 3: State Management**
```python
class SmartProBonoState(Dict[str, Any]):
    # Input data
    intake_id: str
    user_id: str | None
    raw_text: str
    meta: dict
    
    # Workflow state
    case_type: str | None = None
    specialist_analysis: str | None = None
    plain_english_answer: str | None = None
    
    # Quality control
    needs_revision: bool = False
    revision_count: int = 0
    max_revisions: int = 2
    
    # Status tracking
    status: str = "started"
    current_step: str = "intake"
```

## 🚀 How to Run the Advanced Implementation

### **1. Test the Advanced Graph**
```bash
# Run the test script
python test_advanced_langgraph.py
```

### **2. Use in Your API**
```python
# In your main.py, replace the simple graph with advanced
from .graph_advanced import run_advanced_flow

@app.post("/intake/run")
def intake_run(payload: IntakeIn):
    return {"result": run_advanced_flow(payload.user_id, payload.full_text, payload.meta)}
```

### **3. Monitor with LangSmith**
```python
# Add LangSmith tracing
import os
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = "your-langsmith-key"
```

## 🧠 Key Learning Points

### **1. Conditional Edges**
```python
# Route based on state
g.add_conditional_edges(
    "classify",
    route_by_case_type,  # Function that checks state
    {
        "criminal": "criminal_specialist",
        "housing": "housing_specialist",
        "family": "family_specialist"
    }
)
```

### **2. State-Based Routing**
```python
def route_by_case_type(state: SmartProBonoState) -> str:
    case_type = state.get("case_type", "other")
    if case_type == "criminal":
        return "criminal_specialist"
    # ... more routing logic
```

### **3. Loop Control**
```python
def route_after_critic(state: SmartProBonoState) -> str:
    if (state.get("needs_revision", False) and 
        state.get("revision_count", 0) < state.get("max_revisions", 2)):
        return "rewriter"  # Loop back
    else:
        return "plain_english_explainer"  # Exit loop
```

### **4. State Updates**
```python
def critic_review(ctx: Ctx) -> SmartProBonoState:
    # ... review logic ...
    if "REVISE" in response.content.upper():
        ctx.state["needs_revision"] = True
        ctx.state["revision_count"] += 1
    else:
        ctx.state["needs_revision"] = False
    
    ctx.state["current_step"] = "critic_review"
    return ctx.state
```

## 🎯 Next Steps for Learning

### **1. Experiment with Patterns**
- Try adding parallel execution (multiple specialists at once)
- Implement a roundtable discussion pattern
- Add human-in-the-loop pauses

### **2. Add Advanced Features**
- **Checkpointing**: Save state at each step
- **Streaming**: Real-time updates to frontend
- **Error Handling**: Graceful failure recovery
- **Metrics**: Performance monitoring

### **3. Production Considerations**
- **Rate Limiting**: Prevent API abuse
- **Caching**: Store common responses
- **Scaling**: Handle multiple concurrent users
- **Security**: Validate inputs and outputs

## 📚 Official Documentation References

- [LangGraph Quickstart](https://langchain-ai.github.io/langgraph/)
- [Prebuilt Agents](https://langchain-ai.github.io/langgraph/concepts/prebuilt-agents/)
- [State Management](https://langchain-ai.github.io/langgraph/concepts/low_level/#state)
- [Conditional Edges](https://langchain-ai.github.io/langgraph/concepts/low_level/#conditional-edges)
- [Human-in-the-Loop](https://langchain-ai.github.io/langgraph/concepts/human_in_the_loop/)

## 🔧 Testing Your Implementation

Run the test script to see the advanced patterns in action:

```bash
python test_advanced_langgraph.py
```

This will demonstrate:
- ✅ Case type classification
- ✅ Specialist routing
- ✅ Critic review process
- ✅ Revision loops
- ✅ Plain English explanation
- ✅ State management throughout

The test shows how your SmartProBono system can now handle complex legal workflows with multiple AI agents working together, just like the official LangGraph documentation examples!
