"""
Simple Free AI Service - No database dependencies
Direct Ollama integration for all AI operations
"""

import requests
import json
from datetime import datetime
from typing import Dict, List, Optional, Any

class SimpleFreeAI:
    """Simple free AI service using Ollama models"""
    
    def __init__(self):
        self.ollama_url = "http://localhost:11434/api/generate"
        self.models = {
            "legal": "gemma2:2b",
            "chat": "tinyllama:1.1b", 
            "research": "qwen2.5:0.5b",
            "default": "gemma2:2b"
        }
    
    def generate_response(self, message: str, task_type: str = "chat", **kwargs) -> Dict[str, Any]:
        """Generate response using Ollama"""
        try:
            model = self.models.get(task_type, self.models["default"])
            
            # Build prompt
            system_prompt = self._get_system_prompt(task_type)
            full_prompt = f"{system_prompt}\n\nUser: {message}\n\nAssistant:"
            
            payload = {
                "model": model,
                "prompt": full_prompt,
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "num_predict": 200  # Faster responses - brief but helpful
                }
            }
            
            response = requests.post(self.ollama_url, json=payload, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                response_text = result.get("response", "").strip()
                
                return {
                    "id": f"resp_{hash(message) % 10000}_{int(datetime.now().timestamp())}",
                    "created_at": datetime.now().isoformat(),
                    "model": model,
                    "task_type": task_type,
                    "text": response_text,
                    "success": True,
                    "conversation_id": kwargs.get('conversation_id'),
                    "user_id": kwargs.get('user_id')
                }
            else:
                return self._get_fallback_response(message, task_type)
                
        except Exception as e:
            return self._get_fallback_response(message, task_type)
    
    def _get_system_prompt(self, task_type: str) -> str:
        """Get system prompt for task type"""
        prompts = {
            "legal": """You are a legal assistant for SmartProBono. Provide helpful legal guidance.

COMMUNICATION STYLE:
- Be professional but approachable
- Use clear, simple language
- Provide specific, actionable advice
- Always remind users this is general information, not legal advice

RESPONSE FORMAT:
- Start with a direct answer
- Provide relevant legal details
- Suggest next steps or resources
- End with disclaimer about consulting an attorney

Keep responses helpful and informative.""",

            "chat": """You are a legal assistant. Give brief, helpful answers. Note: This is general info, not legal advice.""",

            "research": """You are a legal research specialist. Provide comprehensive legal research.

RESEARCH FRAMEWORK:
1. Direct Answer: Clear response to the question
2. Legal Principles: Key legal concepts involved
3. Practical Application: How this applies in real situations
4. Resources: Relevant databases, websites, or organizations
5. Next Steps: Recommended research actions

Be thorough and well-organized in your research.""",

            "default": """You are a legal assistant. Provide helpful legal guidance in a professional manner."""
        }
        
        return prompts.get(task_type, prompts["default"])
    
    def _get_fallback_response(self, message: str, task_type: str) -> Dict[str, Any]:
        """Get fallback response"""
        fallback_text = f"I understand you're asking about '{message}'. While I'd normally provide detailed guidance using our AI system, I'm currently experiencing technical difficulties. For immediate help, I recommend:\n\n1. Contacting your local legal aid organization\n2. Checking your state's legal resources website\n3. Consulting with a qualified attorney\n\nI apologize for the inconvenience and encourage you to try again in a few moments."
        
        return {
            "id": f"resp_{hash(message) % 10000}_{int(datetime.now().timestamp())}",
            "created_at": datetime.now().isoformat(),
            "model": "fallback",
            "task_type": task_type,
            "text": fallback_text,
            "success": False,
            "conversation_id": None,
            "user_id": None
        }

# Global instance
simple_free_ai = SimpleFreeAI()
