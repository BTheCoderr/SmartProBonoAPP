import os
import json
from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel
from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import RealDictCursor
import requests

load_dotenv()

# Database configuration
DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_PORT = os.environ.get("DB_PORT", "5432")
DB_NAME = os.environ.get("DB_NAME", "smartprobono_db")
DB_USER = os.environ.get("DB_USER", "baheemferrell")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "")

# AI configuration
OLLAMA_BASE = os.environ.get("OLLAMA_BASE", "http://localhost:11434")
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "mistral")

def get_db_connection():
    """Get database connection"""
    try:
        return psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
    except Exception as e:
        print(f"Database connection failed: {e}")
        return None

app = FastAPI(title="SmartProBono Document AI Worker - Minimal")

class ProcessBody(BaseModel):
    document_id: str
    language: str | None = "eng"

class AskBody(BaseModel):
    document_id: str
    question: str

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "Minimal worker is running"}

@app.post("/upload")
async def upload_doc(file: UploadFile = File(...), user_id: str = None, title: str = None):
    """Upload a document (simplified)"""
    try:
        print(f"Received upload request for file: {file.filename}")
        
        # Read file content
        file_content = await file.read()
        print(f"File size: {len(file_content)} bytes")
        
        # For now, just return success
        return {
            "ok": True,
            "document_id": "test-123",
            "path": f"/tmp/{file.filename}",
            "message": "Document uploaded successfully (minimal mode)",
            "text_length": len(file_content),
            "filename": file.filename
        }
        
    except Exception as e:
        print(f"Upload error: {e}")
        raise HTTPException(500, f"Upload failed: {str(e)}")

@app.post("/process")
def process_doc(body: ProcessBody):
    """Process a document (simplified)"""
    try:
        print(f"Processing document: {body.document_id}")
        
        # For now, just return success
        return {
            "ok": True,
            "chunks": 1,
            "message": "Document processed successfully (minimal mode)",
            "document_id": body.document_id
        }
    except Exception as e:
        print(f"Processing error: {e}")
        raise HTTPException(500, f"Processing failed: {str(e)}")

@app.post("/ask")
def ask_doc(body: AskBody):
    """Ask a question (simplified)"""
    try:
        print(f"Question asked: {body.question}")
        
        # Simple response for now
        return {
            "answer": f"This is a test response from the minimal worker. Your question was: '{body.question}'",
            "sources": [0],
            "chunks_used": 1
        }
    except Exception as e:
        print(f"Question error: {e}")
        raise HTTPException(500, f"Question failed: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting minimal worker on port 8001...")
    print("📝 This is a simplified version to test basic functionality")
    uvicorn.run(app, host="0.0.0.0", port=8001)
