"""
Ollama AI Service - Free Model Integration
Uses your local Ollama models for all AI operations
"""

import os
import logging
import requests
import json
from datetime import datetime
from typing import Dict, List, Optional, Any
import random

logger = logging.getLogger(__name__)

class OllamaAIService:
    """
    AI Service that uses your free Ollama models:
    - gemma2:2b (best for legal tasks)
    - tinyllama:1.1b (fastest for chat)
    - qwen2.5:0.5b (good for research)
    """
    
    def __init__(self):
        self.ollama_url = "http://localhost:11434/api/generate"
        self.available_models = {
            "chat": "tinyllama:1.1b",
            "legal": "gemma2:2b", 
            "research": "qwen2.5:0.5b",
            "default": "gemma2:2b"
        }
        
        # Test which models are actually available
        self.working_models = self._test_available_models()
        logger.info(f"Ollama models available: {self.working_models}")
    
    def _test_available_models(self) -> Dict[str, bool]:
        """Test which models are actually working"""
        working = {}
        for task, model in self.available_models.items():
            try:
                response = requests.post(
                    self.ollama_url,
                    json={
                        "model": model,
                        "prompt": "test",
                        "stream": False,
                        "options": {"max_tokens": 10}
                    },
                    timeout=10
                )
                working[task] = response.status_code == 200
                logger.info(f"Model {model} ({task}): {'Working' if working[task] else 'Failed'}")
            except Exception as e:
                working[task] = False
                logger.warning(f"Model {model} ({task}) error: {e}")
        return working
    
    def generate_legal_response(self, message: str, task_type: str = "chat", 
                              conversation_id: Optional[str] = None, 
                              history: Optional[List[Dict]] = None, 
                              model: str = "auto", 
                              user_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Generate a legal response using Ollama models
        
        Args:
            message: User message
            task_type: Type of task (chat, legal, research, etc.)
            conversation_id: Conversation ID
            history: Previous conversation history
            model: Model to use (auto, chat, legal, research)
            user_id: User ID
            
        Returns:
            Generated response
        """
        try:
            response_id = f"resp_{random.randint(1000, 9999)}_{int(datetime.now().timestamp())}"
            
            # Select the best model for the task
            if model == "auto":
                if task_type in ["legal", "document_drafting", "contract_generation"]:
                    model = "legal"
                elif task_type in ["research", "case_analysis", "legal_research"]:
                    model = "research"
                else:
                    model = "chat"
            
            # Get the actual model name
            ollama_model = self.available_models.get(model, "gemma2:2b")
            
            # Check if model is working - be more lenient
            if not self.working_models.get(model, False):
                logger.warning(f"Model {ollama_model} not detected as working, but trying anyway...")
                # Don't return fallback immediately, try to call the model
            
            # Generate response
            response_text = self._call_ollama(message, task_type, ollama_model, history)
            
            if response_text:
                return {
                    "id": response_id,
                    "created_at": datetime.now().isoformat(),
                    "model": ollama_model,
                    "task_type": task_type,
                    "text": response_text,
                    "conversation_id": conversation_id,
                    "user_id": user_id,
                    "success": True
                }
            else:
                return self._get_fallback_response(message, task_type, response_id)
                
        except Exception as e:
            logger.error(f"Error generating legal response: {e}")
            return self._get_error_response(message, task_type, str(e))
    
    def _call_ollama(self, message: str, task_type: str, model: str, history: Optional[List[Dict]] = None) -> str:
        """Call Ollama API for response generation"""
        try:
            # Build context from conversation history
            context = ""
            if history:
                recent_history = history[-4:] if len(history) > 4 else history
                for msg in recent_history:
                    role = "User" if msg.get('sender') == 'user' else "Assistant"
                    context += f"{role}: {msg.get('text', '')}\n"
            
            # Get system prompt
            system_prompt = self._get_system_prompt(task_type)
            full_prompt = f"{system_prompt}\n\n{context}User: {message}\n\nAssistant:"
            
            payload = {
                "model": model,
                "prompt": full_prompt,
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "top_p": 0.9,
                    "max_tokens": 1000
                }
            }
            
            response = requests.post(self.ollama_url, json=payload, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                return result.get("response", "").strip()
            else:
                logger.error(f"Ollama API error: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"Ollama API error: {e}")
            return None
    
    def _get_system_prompt(self, task_type: str) -> str:
        """Get system prompt based on task type"""
        prompts = {
            "chat": """You are SmartProBono's AI Legal Assistant. Provide helpful, conversational legal guidance.

COMMUNICATION STYLE:
- Be friendly and approachable
- Use simple, clear language
- Ask follow-up questions to understand the user's situation better
- Provide specific, actionable advice when possible
- Always remind users this is general information, not legal advice

RESPONSE FORMAT:
- Start with a direct answer to their question
- Provide relevant details and context
- Ask clarifying questions if needed
- Suggest next steps or resources
- End with a disclaimer about consulting an attorney

Keep responses conversational and helpful. Avoid repetitive responses.""",

            "legal": """You are a specialized legal assistant for SmartProBono. Provide comprehensive legal analysis and guidance.

LEGAL ANALYSIS FRAMEWORK:
1. Direct Answer: Clear response to the legal question
2. Legal Principles: Key legal concepts and relevant laws
3. Practical Application: How this applies in real situations
4. Jurisdiction Notes: State/federal law differences if relevant
5. Resources: Relevant forms, websites, or organizations
6. Next Steps: Recommended actions
7. Disclaimer: Always remind users to consult an attorney

Be thorough but accessible. Focus on practical legal guidance.""",

            "research": """You are a legal research specialist. Provide comprehensive, well-structured legal research.

RESEARCH FRAMEWORK:
1. Direct Answer: Clear response to the question
2. Legal Principles: Key legal concepts involved
3. Case Law: Relevant precedents and decisions
4. Statutes: Applicable laws and regulations
5. Practical Application: How this applies in real situations
6. Resources: Relevant databases, websites, or organizations
7. Next Steps: Recommended research actions

Be thorough and cite sources when possible.""",

            "document_drafting": """You are a legal document drafting assistant. Help create clear, professional legal documents.

DRAFTING GUIDELINES:
- Use clear, professional language
- Include all necessary legal elements
- Structure documents logically
- Provide placeholders for specific information
- Include standard legal disclaimers
- Follow proper legal formatting

Focus on creating practical, usable documents."""
        }
        
        return prompts.get(task_type, prompts["chat"])
    
    def _get_fallback_response(self, message: str, task_type: str, response_id: str) -> Dict[str, Any]:
        """Get fallback response when Ollama is unavailable"""
        fallback_responses = {
            "chat": f"I understand you're asking about '{message}'. While I'd normally provide detailed guidance using our AI system, I'm currently experiencing technical difficulties. For immediate help, I recommend:\n\n1. Contacting your local legal aid organization\n2. Checking your state's legal resources website\n3. Consulting with a qualified attorney\n\nI apologize for the inconvenience and encourage you to try again in a few moments.",
            
            "legal": f"For legal analysis on '{message}', I'd typically provide comprehensive guidance. Since our AI system is temporarily unavailable, I suggest:\n\n1. Checking your state's legal code online\n2. Reviewing recent court decisions in your jurisdiction\n3. Consulting legal databases like Justia or FindLaw\n4. Speaking with a legal professional\n\nPlease try again shortly for AI-powered legal assistance.",
            
            "research": f"For research on '{message}', I'd normally provide comprehensive legal analysis. Since our AI system is temporarily unavailable, I suggest:\n\n1. Checking your state's legal code online\n2. Reviewing recent court decisions in your jurisdiction\n3. Consulting legal databases like Justia or FindLaw\n4. Speaking with a legal professional\n\nPlease try again shortly for AI-powered research assistance.",
            
            "document_drafting": f"I'd normally help draft documents related to '{message}', but our system is temporarily offline. For immediate document needs:\n\n1. Use standard legal templates from your state's court website\n2. Consult with a legal professional for complex documents\n3. Check legal aid organizations for free document assistance\n\nOur AI drafting service should be available again soon."
        }
        
        return {
            "id": response_id,
            "created_at": datetime.now().isoformat(),
            "model": "fallback",
            "task_type": task_type,
            "text": fallback_responses.get(task_type, fallback_responses["chat"]),
            "success": False
        }
    
    def _get_error_response(self, message: str, task_type: str, error: str) -> Dict[str, Any]:
        """Get error response"""
        return {
            "id": f"resp_{random.randint(1000, 9999)}_{int(datetime.now().timestamp())}",
            "created_at": datetime.now().isoformat(),
            "model": "error",
            "task_type": task_type,
            "text": f"I apologize, but I encountered an error while processing your request: {error}. Please try again or consult with a qualified attorney for immediate assistance.",
            "success": False,
            "error": error
        }
    
    def get_available_models(self) -> Dict[str, str]:
        """Get available models"""
        return {task: model for task, model in self.available_models.items() 
                if self.working_models.get(task, False)}
    
    def test_models(self) -> Dict[str, Any]:
        """Test all models and return status"""
        return {
            "models": self.available_models,
            "working": self.working_models,
            "ollama_url": self.ollama_url,
            "status": "healthy" if any(self.working_models.values()) else "unhealthy"
        }
