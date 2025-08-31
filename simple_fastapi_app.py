#!/usr/bin/env python3
"""
SmartProBono - Simple FastAPI App for Deployment
A minimal FastAPI application that works with Python 3.13
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import os
import requests
import json
from datetime import datetime

# Create FastAPI app
app = FastAPI(
    title="SmartProBono API",
    description="AI-powered legal assistance platform",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class ChatRequest(BaseModel):
    message: str
    user_id: Optional[str] = None
    history: Optional[List[dict]] = None

class ChatResponse(BaseModel):
    response: str
    agent: str
    timestamp: str
    status: str

class BetaSignupRequest(BaseModel):
    email: str
    name: Optional[str] = None
    company: Optional[str] = None

class BetaSignupResponse(BaseModel):
    message: str
    status: str
    timestamp: str

# Supabase configuration
SUPABASE_URL = os.getenv("SUPABASE_URL", "https://ewtcvsohdgkthuyajyyk.supabase.co")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY", "")

def call_ollama(message: str, task_type: str = "chat") -> str:
    """Call Ollama API for AI responses"""
    try:
        # Simple AI response simulation for now
        if "contract" in message.lower():
            return "I can help you with contract-related legal questions. What specific aspect of contracts would you like to know about?"
        elif "employment" in message.lower():
            return "I can assist with employment law matters. Please describe your specific employment issue."
        elif "business" in message.lower():
            return "I can help with business law questions. What business legal matter do you need assistance with?"
        else:
            return f"I understand you're asking about: {message}. I'm here to help with your legal questions. Could you provide more specific details about your legal matter?"
    except Exception as e:
        return f"I apologize, but I'm having trouble processing your request right now. Please try again later. Error: {str(e)}"

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "SmartProBono API is running",
        "version": "1.0.0",
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "ok",
        "message": "SmartProBono API is healthy",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat(),
        "supabase_configured": bool(SUPABASE_URL and SUPABASE_SERVICE_KEY)
    }

@app.post("/api/legal/chat", response_model=ChatResponse)
async def legal_chat(request: ChatRequest):
    """Legal chat endpoint"""
    try:
        # Generate AI response
        response = call_ollama(request.message, "chat")
        
        return ChatResponse(
            response=response,
            agent="legal_assistant",
            timestamp=datetime.now().isoformat(),
            status="success"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing chat request: {str(e)}")

@app.post("/api/beta/signup", response_model=BetaSignupResponse)
async def beta_signup(request: BetaSignupRequest):
    """Beta signup endpoint"""
    try:
        # Store in Supabase if configured
        if SUPABASE_URL and SUPABASE_SERVICE_KEY:
            headers = {
                "apikey": SUPABASE_SERVICE_KEY,
                "Authorization": f"Bearer {SUPABASE_SERVICE_KEY}",
                "Content-Type": "application/json"
            }
            
            data = {
                "email": request.email,
                "name": request.name or "",
                "company": request.company or "",
                "created_at": datetime.now().isoformat()
            }
            
            response = requests.post(
                f"{SUPABASE_URL}/rest/v1/beta_signups",
                headers=headers,
                json=data
            )
            
            if response.status_code not in [200, 201]:
                print(f"Supabase error: {response.status_code} - {response.text}")
        
        return BetaSignupResponse(
            message="Thank you for signing up for our beta! We'll be in touch soon.",
            status="success",
            timestamp=datetime.now().isoformat()
        )
    except Exception as e:
        return BetaSignupResponse(
            message="Thank you for your interest! We'll be in touch soon.",
            status="success",
            timestamp=datetime.now().isoformat()
        )

@app.get("/api/legal/agents")
async def list_agents():
    """List available legal agents"""
    return {
        "agents": [
            {
                "name": "General Legal Assistant",
                "description": "General legal questions and guidance",
                "specialties": ["general", "contracts", "employment", "business"]
            },
            {
                "name": "Contract Specialist",
                "description": "Contract review and drafting assistance",
                "specialties": ["contracts", "agreements", "terms"]
            },
            {
                "name": "Employment Law Expert",
                "description": "Employment law and HR matters",
                "specialties": ["employment", "hr", "workplace"]
            },
            {
                "name": "Business Law Advisor",
                "description": "Business formation and legal structure",
                "specialties": ["business", "incorporation", "compliance"]
            }
        ]
    }

@app.get("/api/legal/services")
async def list_services():
    """List available legal services"""
    return {
        "services": [
            {
                "name": "Legal Chat",
                "description": "AI-powered legal assistance and guidance",
                "endpoint": "/api/legal/chat"
            },
            {
                "name": "Contract Review",
                "description": "Contract analysis and review services",
                "endpoint": "/api/legal/contracts"
            },
            {
                "name": "Legal Representation",
                "description": "Connect with qualified legal professionals",
                "endpoint": "/api/legal/representation"
            },
            {
                "name": "Document Templates",
                "description": "Access to legal document templates",
                "endpoint": "/api/legal/templates"
            }
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
