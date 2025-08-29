"""
FastAPI main application for SmartProBono multi-agent system
"""
import os
import time
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from pydantic import BaseModel
from dotenv import load_dotenv

from haystack import Pipeline
from haystack.dataclasses import Document, ByteStream
from haystack.components.converters.pypdf import PyPDFToDocument
from haystack.components.preprocessors import DocumentCleaner, DocumentSplitter
from haystack.components.embedders import SentenceTransformersDocumentEmbedder
from haystack.components.writers import DocumentWriter

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rag.pipelines import build_query_pipeline, build_indexing_pipeline
from graph.build import build_graph
from utils.safety import needs_escalation, add_disclaimer

# Load environment variables
load_dotenv()

# Create FastAPI app
app = FastAPI(
    title="SmartProBono Multi-Agent System",
    description="AI-powered legal assistance with multi-agent orchestration",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
try:
    INDEX_PIPE: Pipeline = build_indexing_pipeline()
    QUERY_PIPE: Pipeline = build_query_pipeline()
    GRAPH = build_graph()
    print("✅ All components initialized successfully")
except Exception as e:
    print(f"❌ Error initializing components: {e}")
    INDEX_PIPE = None
    QUERY_PIPE = None
    GRAPH = None

# Pydantic models
class QueryRequest(BaseModel):
    query: str
    user_id: Optional[str] = None
    history: Optional[List[dict]] = None

class QueryResponse(BaseModel):
    answer: str
    citations: List[dict]
    jurisdiction: Optional[str]
    escalate: bool
    confidence: float
    processing_time: float
    agent_used: str

# Health check endpoint
@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "ok",
        "message": "SmartProBono Multi-Agent System is running",
        "version": "1.0.0",
        "components": {
            "indexing_pipeline": INDEX_PIPE is not None,
            "query_pipeline": QUERY_PIPE is not None,
            "graph": GRAPH is not None
        }
    }

# Document ingestion endpoint
@app.post("/api/ingest/pdf")
async def ingest_pdf(files: List[UploadFile] = File(...)):
    """Ingest PDF documents into the knowledge base"""
    if not INDEX_PIPE:
        raise HTTPException(status_code=500, detail="Indexing pipeline not available")
    
    try:
        # Convert uploads to ByteStreams
        streams = []
        for file in files:
            content = await file.read()
            streams.append(ByteStream(
                data=content, 
                meta={"filename": file.filename}
            ))
        
        # Run indexing pipeline
        result = INDEX_PIPE.run({"pdf": {"sources": streams}})
        
        return {
            "success": True,
            "files_processed": len(files),
            "chunks_created": len(result["write"]["documents_written"])
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing files: {str(e)}")

# Simple query endpoint (RAG only)
@app.post("/api/query", response_model=QueryResponse)
async def query(request: QueryRequest):
    """Simple query using RAG pipeline only"""
    if not QUERY_PIPE:
        raise HTTPException(status_code=500, detail="Query pipeline not available")
    
    start_time = time.time()
    
    try:
        # Run RAG pipeline
        result = QUERY_PIPE.run({"q_embed": {"text": request.query}})
        
        answer = result["llm"]["replies"][0]
        docs = result["retrieve"]["documents"]
        citations = [{"content": d.content[:200], "meta": d.meta} for d in docs]
        
        # Check if escalation is needed
        escalate = needs_escalation(answer)
        
        # Add disclaimer if needed
        if escalate:
            answer = add_disclaimer(answer)
        
        return QueryResponse(
            answer=answer,
            citations=citations,
            jurisdiction=None,
            escalate=escalate,
            confidence=0.8 if docs else 0.3,
            processing_time=time.time() - start_time,
            agent_used="rag-pipeline"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")

# Multi-agent assist endpoint
@app.post("/api/assist", response_model=QueryResponse)
async def assist(request: QueryRequest):
    """Multi-agent assistance using LangGraph orchestration"""
    if not GRAPH:
        raise HTTPException(status_code=500, detail="Multi-agent graph not available")
    
    start_time = time.time()
    
    try:
        # Prepare state for graph
        state = {
            "query": request.query,
            "user_id": request.user_id,
            "messages": request.history or []
        }
        
        # Run the multi-agent graph
        final_state = GRAPH.invoke(state)
        
        # Extract results
        answer = final_state.get("draft", "I'm sorry, I couldn't generate a response.")
        citations = final_state.get("citations", [])
        jurisdiction = final_state.get("jurisdiction")
        escalate = final_state.get("escalate", False)
        confidence = final_state.get("confidence", 0.5)
        
        # Add disclaimer if needed
        if escalate:
            answer = add_disclaimer(answer)
        
        return QueryResponse(
            answer=answer,
            citations=citations,
            jurisdiction=jurisdiction,
            escalate=escalate,
            confidence=confidence,
            processing_time=time.time() - start_time,
            agent_used=final_state.get("agent_used", "multi-agent-system")
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in multi-agent system: {str(e)}")

# Get available agents
@app.get("/api/agents")
async def get_agents():
    """Get information about available agents"""
    return {
        "agents": [
            {
                "name": "Intake Agent",
                "description": "Normalizes user questions and extracts jurisdiction",
                "type": "intake"
            },
            {
                "name": "Research Agent", 
                "description": "Searches legal documents and precedents",
                "type": "research"
            },
            {
                "name": "Drafting Agent",
                "description": "Generates clear legal responses",
                "type": "drafting"
            },
            {
                "name": "Safety Agent",
                "description": "Ensures compliance and prevents UPL",
                "type": "safety"
            }
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
