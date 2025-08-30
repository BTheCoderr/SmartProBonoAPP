from langchain_ollama import ChatOllama
from .types import Ctx

SYS = ("You are a legal intake summarizer. Extract parties, issue, "
       "jurisdiction if present, key facts, and requested help. Be concise.")

def run(ctx: Ctx):
    # Use Ollama with a local model - llama3.2:3b is good for summarization
    llm = ChatOllama(model="llama3.2:3b", temperature=0)
    user = ctx.state["raw_text"]
    
    # Create a prompt with system and user messages
    prompt = f"System: {SYS}\n\nUser: {user}\n\nAssistant:"
    msg = llm.invoke(prompt)
    
    ctx.state["summary"] = msg.content
    ctx.state["status"] = "summarized"
    return ctx.state
