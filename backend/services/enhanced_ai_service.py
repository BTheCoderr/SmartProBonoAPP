"""Enhanced AI service with Claude, OpenAI, and Ollama integration"""
import logging
import random
import requests
import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Union

logger = logging.getLogger(__name__)

class EnhancedAIService:
    """Enhanced AI service supporting multiple providers: Claude, OpenAI, and Ollama"""
    
    def __init__(self):
        self.anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        self.ollama_url = "http://localhost:11434/api/generate"
        
    def generate_legal_response(self, message: str, task_type: str = "chat", 
                              conversation_id: Optional[str] = None, 
                              history: Optional[List[Dict]] = None, 
                              model: str = "claude", 
                              user_id: Optional[str] = None) -> Dict:
        """
        Generate a response using the specified AI model
        
        Args:
            message: The user message
            task_type: The type of task (chat, research, draft)
            conversation_id: The conversation ID
            history: Previous conversation history
            model: The AI model to use (claude, openai, ollama)
            user_id: The user ID
            
        Returns:
            Dict: The generated response
        """
        try:
            response_id = f"resp_{random.randint(1000, 9999)}_{int(datetime.now().timestamp())}"
            
            response = {
                "id": response_id,
                "created_at": datetime.now().isoformat(),
                "model": model,
                "task_type": task_type
            }
            
            # Route to appropriate AI provider
            if model.lower() in ["claude", "anthropic"] and self.anthropic_api_key:
                ai_response = self._call_claude(message, task_type, history)
                provider_info = {
                    "name": "Claude-3.5-Sonnet",
                    "type": "cloud_llm",
                    "provider": "anthropic"
                }
            elif model.lower() in ["openai", "gpt"] and self.openai_api_key:
                ai_response = self._call_openai(message, task_type, history)
                provider_info = {
                    "name": "GPT-4",
                    "type": "cloud_llm", 
                    "provider": "openai"
                }
            else:
                # Fallback to Ollama
                ai_response = self._call_ollama(message, task_type, history)
                provider_info = {
                    "name": f"Ollama-{model}",
                    "type": "local_llm",
                    "provider": "ollama"
                }
            
            if ai_response:
                response["response"] = ai_response
                response["model_info"] = provider_info
            else:
                # Final fallback
                response["response"] = self._get_fallback_response(message, task_type)
                response["model_info"] = {
                    "name": "fallback",
                    "type": "static",
                    "provider": "fallback"
                }
            
            if conversation_id:
                response["conversation_id"] = conversation_id
                
            return response
            
        except Exception as e:
            logger.error(f"Error generating legal response: {str(e)}")
            return {
                "error": "An error occurred while generating a response",
                "created_at": datetime.now().isoformat()
            }
    
    def _call_claude(self, message: str, task_type: str, history: Optional[List[Dict]] = None) -> Optional[str]:
        """Call Claude API to generate response"""
        try:
            # Build conversation history
            messages = []
            
            # Add system message based on task type
            system_prompts = {
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

                "research": """You are a legal research assistant. Provide comprehensive, well-structured legal information.

RESEARCH FRAMEWORK:
1. Direct Answer: Clear response to the question
2. Legal Principles: Key legal concepts involved
3. Practical Application: How this applies in real situations
4. Jurisdiction Notes: State/federal law differences
5. Resources: Relevant forms, websites, or organizations
6. Next Steps: Recommended actions

Be thorough but accessible.""",

                "draft": """You are a legal document drafting assistant. Help create clear, professional legal documents.

DRAFTING GUIDELINES:
- Use clear, professional language
- Include all necessary legal elements
- Structure documents logically
- Provide placeholders for specific information
- Include standard legal disclaimers

Focus on creating practical, usable documents."""
            }
            
            system_prompt = system_prompts.get(task_type, system_prompts["chat"])
            messages.append({"role": "user", "content": system_prompt})
            
            # Add conversation history
            if history:
                for msg in history[-6:]:  # Last 6 messages for context
                    role = "user" if msg.get('sender') == 'user' else "assistant"
                    messages.append({"role": role, "content": msg.get('text', '')})
            
            # Add current message
            messages.append({"role": "user", "content": message})
            
            # Call Claude API
            headers = {
                "x-api-key": self.anthropic_api_key,
                "Content-Type": "application/json",
                "anthropic-version": "2023-06-01"
            }
            
            payload = {
                "model": "claude-3-5-sonnet-20241022",
                "max_tokens": 2000,
                "messages": messages
            }
            
            response = requests.post(
                "https://api.anthropic.com/v1/messages",
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get("content", [{}])[0].get("text", "").strip()
            else:
                logger.error(f"Claude API error: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            logger.error(f"Error calling Claude: {str(e)}")
            return None
    
    def _call_openai(self, message: str, task_type: str, history: Optional[List[Dict]] = None) -> Optional[str]:
        """Call OpenAI API to generate response"""
        try:
            # Build conversation history
            messages = []
            
            # Add system message
            system_prompts = {
                "chat": "You are SmartProBono's AI Legal Assistant. Provide helpful, conversational legal guidance. Be friendly, clear, and always remind users this is general information, not legal advice.",
                "research": "You are a legal research assistant. Provide comprehensive, well-structured legal information with clear frameworks and practical applications.",
                "draft": "You are a legal document drafting assistant. Help create clear, professional legal documents with proper structure and legal elements."
            }
            
            messages.append({"role": "system", "content": system_prompts.get(task_type, system_prompts["chat"])})
            
            # Add conversation history
            if history:
                for msg in history[-6:]:
                    role = "user" if msg.get('sender') == 'user' else "assistant"
                    messages.append({"role": role, "content": msg.get('text', '')})
            
            # Add current message
            messages.append({"role": "user", "content": message})
            
            # Call OpenAI API
            headers = {
                "Authorization": f"Bearer {self.openai_api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": "gpt-4",
                "messages": messages,
                "max_tokens": 2000,
                "temperature": 0.7
            }
            
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get("choices", [{}])[0].get("message", {}).get("content", "").strip()
            else:
                logger.error(f"OpenAI API error: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            logger.error(f"Error calling OpenAI: {str(e)}")
            return None
    
    def _call_ollama(self, message: str, task_type: str, history: Optional[List[Dict]] = None) -> Optional[str]:
        """Call Ollama API to generate response (fallback)"""
        try:
            # Build context from conversation history
            context = ""
            if history and len(history) > 0:
                recent_history = history[-4:] if len(history) > 4 else history
                for msg in recent_history:
                    role = "User" if msg.get('sender') == 'user' else "Assistant"
                    context += f"{role}: {msg.get('text', '')}\n"
            
            # Create system prompt based on task type
            system_prompts = {
                "chat": "You are SmartProBono's AI Legal Assistant. Provide helpful, conversational legal guidance. Be friendly and clear.",
                "research": "You are a legal research assistant. Provide comprehensive, well-structured legal information.",
                "draft": "You are a legal document drafting assistant. Help create clear, professional legal documents."
            }
            
            system_prompt = system_prompts.get(task_type, system_prompts["chat"])
            full_prompt = f"{system_prompt}\n\n{context}User: {message}\n\nAssistant:"
            
            # Call Ollama API
            payload = {
                "model": "llama3.2:3b",
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
                logger.error(f"Ollama API error: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            logger.error(f"Error calling Ollama: {str(e)}")
            return None
    
    def _get_fallback_response(self, message: str, task_type: str) -> str:
        """Fallback responses when all AI services are unavailable"""
        fallback_responses = {
            "chat": f"I understand you're asking about '{message}'. While I'd normally provide detailed guidance using our AI system, I'm currently experiencing technical difficulties. For immediate help, I recommend:\n\n1. Contacting your local legal aid organization\n2. Checking your state's legal resources website\n3. Consulting with a qualified attorney\n\nI apologize for the inconvenience and encourage you to try again in a few moments.",
            
            "research": f"For research on '{message}', I'd typically provide comprehensive legal analysis. Since our AI system is temporarily unavailable, I suggest:\n\n1. Checking your state's legal code online\n2. Reviewing recent court decisions in your jurisdiction\n3. Consulting legal databases like Justia or FindLaw\n4. Speaking with a legal professional\n\nPlease try again shortly for AI-powered research assistance.",
            
            "draft": f"I'd normally help draft documents related to '{message}', but our system is temporarily offline. For immediate document needs:\n\n1. Use standard legal templates from your state's court website\n2. Consult with a legal professional for complex documents\n3. Check legal aid organizations for free document assistance\n\nOur AI drafting service should be available again soon."
        }
        
        return fallback_responses.get(task_type, fallback_responses["chat"])
    
    def get_available_models(self) -> Dict[str, List[str]]:
        """Get list of available AI models by provider"""
        models = {
            "anthropic": [],
            "openai": [],
            "ollama": []
        }
        
        if self.anthropic_api_key:
            models["anthropic"] = ["claude-3-5-sonnet", "claude-3-haiku", "claude-3-opus"]
        
        if self.openai_api_key:
            models["openai"] = ["gpt-4", "gpt-4-turbo", "gpt-3.5-turbo"]
        
        # Ollama models (assuming they're available locally)
        models["ollama"] = ["llama3.2:3b", "mistral:7b", "qwen2.5:0.5b", "gemma2:2b", "phi3:mini"]
        
        return models

# Create singleton instance
enhanced_ai_service = EnhancedAIService()

# Convenience functions
def generate_legal_response(message: str, task_type: str = "chat", 
                          conversation_id: Optional[str] = None, 
                          history: Optional[List[Dict]] = None, 
                          model: str = "claude", 
                          user_id: Optional[str] = None) -> Dict:
    return enhanced_ai_service.generate_legal_response(message, task_type, conversation_id, history, model, user_id)

def get_available_models() -> Dict[str, List[str]]:
    return enhanced_ai_service.get_available_models()
