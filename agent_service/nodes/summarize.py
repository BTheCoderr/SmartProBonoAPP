from langchain_openai import ChatOpenAI
from .types import Ctx

SYS = ("You are a legal intake summarizer. Extract parties, issue, "
       "jurisdiction if present, key facts, and requested help. Be concise.")

def run(ctx: Ctx):
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    user = ctx.state["raw_text"]
    msg = llm.invoke([{"role":"system","content":SYS},
                      {"role":"user","content":user}])
    ctx.state["summary"] = msg.content
    ctx.state["status"] = "summarized"
    return ctx.state
