"""
Saul Enhanced AI Service - Integration of Saul Legal AI with existing SmartProBono AI services
Provides a unified interface that can use Saul model as the primary legal AI option
"""

import logging
import sys
import os
from datetime import datetime
from typing import Dict, List, Optional, Any

# Add backend directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from services.saul_legal_ai_service import saul_legal_ai
from services.simple_free_ai import simple_free_ai

logger = logging.getLogger(__name__)

class SaulEnhancedAIService:
    """Enhanced AI service that prioritizes Saul legal model with fallbacks"""
    
    def __init__(self):
        self.saul_service = saul_legal_ai
        self.fallback_service = simple_free_ai
        
        # Model priority order
        self.model_priority = {
            "saul": 1,           # Highest priority - Saul legal model
            "legal": 2,          # Fallback to legal-optimized models
            "default": 3,        # General fallback
            "ollama": 4          # Local Ollama fallback
        }
        
        logger.info("Saul Enhanced AI Service initialized")
    
    def generate_legal_response(self, message: str, task_type: str = "chat", 
                              conversation_id: Optional[str] = None, 
                              history: Optional[List] = None, 
                              model: str = "auto", 
                              user_id: Optional[str] = None, 
                              user_role: str = "client") -> Dict[str, Any]:
        """
        Generate legal response using Saul model with intelligent fallbacks
        
        Args:
            message: User's message
            task_type: Type of task (chat, research, analysis, etc.)
            conversation_id: Conversation ID for context
            history: Previous conversation history
            model: Preferred model ("auto", "saul", "legal", "default")
            user_id: User ID for personalization
            user_role: User role (client, lawyer, admin, etc.)
        
        Returns:
            Dict containing the AI response
        """
        try:
            # Handle simple greetings with conversational responses (don't use AI models)
            greeting_response = self._handle_greeting(message)
            if greeting_response:
                return greeting_response
            
            # Determine which model to use
            selected_model = self._select_model(model, task_type, user_role)
            
            logger.info(f"Using {selected_model} model for {task_type} request")
            
            # Prepare context for the selected service
            context = {
                "conversation_id": conversation_id,
                "user_id": user_id,
                "task_type": task_type,
                "user_role": user_role,
                "history": history or [],
                "max_tokens": self._get_max_tokens(task_type),
                "temperature": self._get_temperature(task_type)
            }
            
            # For conversational legal questions, use a guided approach like SmartProBono Lite
            conversational_response = self._handle_conversational_legal(message, task_type, history)
            if conversational_response:
                return conversational_response
            
            # Saul commented out - requires too much CPU/GPU power
            # if selected_model == "saul":
            #     try:
            #         response = self.saul_service.generate_response(message, **context)
            #         if response.get("success", False):
            #             response["model_used"] = "saul"
            #             response["model_info"] = self.saul_service.get_model_info()
            #             return response
            #         else:
            #             logger.warning("Saul model failed, falling back to Ollama")
            #             # Fall through to fallback
            #     except Exception as e:
            #         logger.error(f"Saul model error: {str(e)}")
            #         # Fall through to fallback
            
            # Use fallback service
            response = self.fallback_service.generate_response(message, **context)
            response["model_used"] = selected_model
            response["fallback_used"] = True
            
            return response
            
        except Exception as e:
            logger.error(f"Error in Saul Enhanced AI Service: {str(e)}")
            return self._get_error_response(message, task_type, str(e))
    
    def _handle_greeting(self, message: str) -> Optional[Dict[str, Any]]:
        """Detect and handle simple greetings with conversational responses"""
        greetings = ['hi', 'hello', 'hey', 'greetings', 'good morning', 'good afternoon', 'good evening', 'howdy', 'sup', 'yo']
        message_lower = message.lower().strip()
        
        # Check if this is a simple greeting (3 words or less, contains greeting word)
        if len(message.split()) <= 3 and any(greeting in message_lower for greeting in greetings):
            return {
                "id": f"greeting_{int(datetime.now().timestamp())}",
                "created_at": datetime.now().isoformat(),
                "success": True,
                "text": "Hi! I'm your AI legal assistant. I can help you with:\n\n• Answering legal questions\n• Analyzing documents\n• Drafting legal letters\n• Understanding your rights\n• Court filing procedures\n\nYou can upload a document, ask me a question, or tell me what legal issue you're working on. What can I help you with today?",
                "model_used": "greeting_handler",
                "task_type": "greeting",
                "conversation_id": None,
                "user_id": None,
                "model_info": {
                    "model_name": "Conversational Handler",
                    "description": "Simple greeting response system"
                }
            }
        return None
    
    def _handle_conversational_legal(self, message: str, task_type: str, history: Optional[List]) -> Optional[Dict[str, Any]]:
        """Handle legal questions with conversational, guided responses like SmartProBono Lite"""
        message_lower = message.lower()
        
        # Detect custody-related questions
        if any(word in message_lower for word in ['custody', 'child custody', 'visitation', 'parenting time']):
            return {
                "id": f"conv_{int(datetime.now().timestamp())}",
                "created_at": datetime.now().isoformat(),
                "success": True,
                "text": "I can help you with child custody matters. To better assist you, I'll need some information:\n\n1. What is your current relationship with the other parent (married, divorced, separated, never married)?\n\n2. What is the current custody arrangement for your child, if any?\n\n3. What changes are you hoping to make to the custody arrangement?\n\nThis information will help me guide you through the process and assist with drafting a Custody Modification Letter if needed.",
                "model_used": "conversational_handler",
                "task_type": "custody_inquiry",
                "conversation_id": None,
                "user_id": None,
                "model_info": {
                    "model_name": "Conversational Legal Assistant",
                    "description": "Guided legal assistance system"
                }
            }
        
        # Detect eviction/housing questions
        if any(word in message_lower for word in ['evict', 'eviction', 'tenant', 'landlord', 'rent', 'lease']):
            return {
                "id": f"conv_{int(datetime.now().timestamp())}",
                "created_at": datetime.now().isoformat(),
                "success": True,
                "text": "I can help with housing and tenant rights issues. To provide the best guidance, please tell me:\n\n1. Are you facing eviction, or do you have another landlord/tenant issue?\n\n2. What state are you in? (Tenant rights vary by state)\n\n3. Do you have a written lease agreement?\n\n4. What's the main issue you're dealing with?\n\nOnce I have this information, I can provide specific guidance and help draft any necessary documents.",
                "model_used": "conversational_handler",
                "task_type": "housing_inquiry",
                "conversation_id": None,
                "user_id": None,
                "model_info": {
                    "model_name": "Conversational Legal Assistant",
                    "description": "Guided legal assistance system"
                }
            }
        
        # Detect employment/workplace questions
        if any(word in message_lower for word in ['work', 'job', 'employ', 'fired', 'discrimination', 'harassment', 'grievance']):
            return {
                "id": f"conv_{int(datetime.now().timestamp())}",
                "created_at": datetime.now().isoformat(),
                "success": True,
                "text": "I can assist with employment-related legal matters. To help you effectively, please share:\n\n1. What is the nature of your workplace issue (termination, discrimination, harassment, wage dispute, etc.)?\n\n2. Are you currently employed or were you recently terminated?\n\n3. Have you reported this issue to your employer or HR?\n\n4. What outcome are you seeking?\n\nWith this information, I can guide you on your rights and help draft appropriate letters or complaints.",
                "model_used": "conversational_handler",
                "task_type": "employment_inquiry",
                "conversation_id": None,
                "user_id": None,
                "model_info": {
                    "model_name": "Conversational Legal Assistant",
                    "description": "Guided legal assistance system"
                }
            }
        
        # If no specific pattern matches but it's a question, give general guidance
        if '?' in message or any(word in message_lower for word in ['how', 'what', 'when', 'where', 'who', 'can i', 'should i', 'help', 'need']):
            return {
                "id": f"conv_{int(datetime.now().timestamp())}",
                "created_at": datetime.now().isoformat(),
                "success": True,
                "text": f"I understand you're asking about: \"{message}\"\n\nTo provide you with the most helpful guidance, could you tell me a bit more about:\n\n• What type of legal issue is this (family law, housing, employment, etc.)?\n• What state are you in?\n• What's your main goal or concern?\n• Do you have any documents related to this matter?\n\nThe more details you provide, the better I can assist you with specific advice and document preparation.",
                "model_used": "conversational_handler",
                "task_type": "general_inquiry",
                "conversation_id": None,
                "user_id": None,
                "model_info": {
                    "model_name": "Conversational Legal Assistant",
                    "description": "Guided legal assistance system"
                }
            }
        
        return None
    
    def _select_model(self, requested_model: str, task_type: str, user_role: str) -> str:
        """Intelligently select the best model for the request"""
        
        # Saul commented out - use Groq/Gemini/Ollama instead
        # if user_role in ["lawyer", "attorney", "paralegal"] and requested_model in ["auto", "saul"]:
        #     return "saul"
        
        # Respect explicit model requests (except saul)
        if requested_model in ["legal", "default", "ollama", "groq"]:
            return requested_model
        
        # Default to legal-optimized models for legal tasks
        legal_tasks = ["legal", "research", "analysis", "document_review", "case_law", "legal_advice", "draft", "document_drafting"]
        if task_type in legal_tasks:
            return "legal"  # Will use Groq/Gemini/Ollama
        else:
            return "legal"  # Use legal-optimized models for general chat too
    
    def _get_max_tokens(self, task_type: str) -> int:
        """Get appropriate max tokens for task type"""
        token_limits = {
            "research": 300,
            "analysis": 250,
            "document_review": 400,
            "case_law": 350,
            "legal_advice": 200,
            "chat": 150,
            "default": 200
        }
        return token_limits.get(task_type, 200)
    
    def _get_temperature(self, task_type: str) -> float:
        """Get appropriate temperature for task type"""
        temperatures = {
            "research": 0.3,      # More focused for research
            "analysis": 0.4,      # Balanced for analysis
            "document_review": 0.2,  # Conservative for document review
            "case_law": 0.3,      # Focused for case law
            "legal_advice": 0.5,  # Slightly more creative for advice
            "chat": 0.7,          # More conversational
            "default": 0.6
        }
        return temperatures.get(task_type, 0.6)
    
    def _get_error_response(self, message: str, task_type: str, error: str) -> Dict[str, Any]:
        """Get error response when all services fail"""
        return {
            "id": f"error_{hash(message) % 10000}_{int(datetime.now().timestamp())}",
            "created_at": datetime.now().isoformat(),
            "model": "error_fallback",
            "task_type": task_type,
            "text": f"""I apologize, but I'm currently experiencing technical difficulties and cannot process your request: "{message}".

For immediate assistance with your legal question, I recommend:

1. **Contact a qualified attorney** - This is always the best option for specific legal matters
2. **Reach out to your local legal aid organization** - They provide free or low-cost legal assistance
3. **Check your state's legal resources website** - Many states offer self-help legal resources
4. **Visit your local law library** - Public law libraries often have helpful resources

*Important: This is general information only, not legal advice. For specific legal matters, please consult with a licensed attorney.*

Technical Details: {error}

Please try again in a few moments, or contact our support team if the issue persists.""",
            "success": False,
            "error": error,
            "conversation_id": None,
            "user_id": None
        }
    
    def get_available_models(self) -> Dict[str, Any]:
        """Get information about available models"""
        saul_info = self.saul_service.get_model_info()
        saul_health = self.saul_service.health_check()
        
        return {
            "saul": {
                "name": "Saul Legal AI",
                "model": saul_info["model_name"],
                "description": "Specialized legal language model trained on legal text",
                "status": saul_health["status"],
                "available": saul_health["status"] == "healthy",
                "device": saul_info["device"],
                "paper": saul_info["paper"],
                "website": saul_info["website"]
            },
            "ollama_legal": {
                "name": "Ollama Legal",
                "model": "gemma2:2b (legal optimized)",
                "description": "Local legal-optimized model via Ollama",
                "status": "available",
                "available": True,
                "device": "local"
            },
            "ollama_general": {
                "name": "Ollama General",
                "model": "tinyllama:1.1b",
                "description": "General purpose local model via Ollama",
                "status": "available",
                "available": True,
                "device": "local"
            }
        }
    
    def health_check(self) -> Dict[str, Any]:
        """Check health of all AI services"""
        saul_health = self.saul_service.health_check()
        
        return {
            "saul_enhanced_service": "healthy",
            "saul_model": saul_health,
            "fallback_service": "available",
            "timestamp": datetime.now().isoformat(),
            "recommended_model": "saul" if saul_health["status"] == "healthy" else "ollama_legal"
        }

# Global instance
saul_enhanced_ai = SaulEnhancedAIService()
