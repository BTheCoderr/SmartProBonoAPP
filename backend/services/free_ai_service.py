"""
Free AI Service - Connects ALL systems to your free Ollama models
Replaces all paid API calls with free Ollama models
"""

import os
import logging
import requests
import json
from datetime import datetime
from typing import Dict, List, Optional, Any
import random

logger = logging.getLogger(__name__)

class FreeAIService:
    """
    Universal AI Service that uses your free Ollama models for ALL operations:
    - Chat and conversation
    - Legal research and analysis
    - Document generation and drafting
    - Multi-agent coordination
    - Voice AI processing
    - Court filing assistance
    - CRM integration
    """
    
    def __init__(self):
        self.ollama_url = "http://localhost:11434/api/generate"
        
        # Model mapping for different tasks
        self.model_mapping = {
            # Chat and general conversation
            "chat": "tinyllama:1.1b",
            "conversation": "tinyllama:1.1b",
            "general": "tinyllama:1.1b",
            
            # Legal tasks (use best model)
            "legal": "gemma2:2b",
            "legal_analysis": "gemma2:2b",
            "legal_research": "gemma2:2b",
            "case_analysis": "gemma2:2b",
            "document_analysis": "gemma2:2b",
            "court_filing": "gemma2:2b",
            "legal_advice": "gemma2:2b",
            
            # Document generation
            "document_drafting": "gemma2:2b",
            "contract_generation": "gemma2:2b",
            "legal_documents": "gemma2:2b",
            "forms": "gemma2:2b",
            
            # Research and analysis
            "research": "qwen2.5:0.5b",
            "analysis": "qwen2.5:0.5b",
            "summarization": "qwen2.5:0.5b",
            "data_analysis": "qwen2.5:0.5b",
            
            # Default fallback
            "default": "gemma2:2b",
            "auto": "gemma2:2b"
        }
        
        # Test model availability
        self.available_models = self._test_models()
        logger.info(f"Free AI Service initialized with models: {self.available_models}")
    
    def _test_models(self) -> Dict[str, bool]:
        """Test which models are available"""
        available = {}
        unique_models = list(set(self.model_mapping.values()))
        
        for model in unique_models:
            try:
                response = requests.post(
                    self.ollama_url,
                    json={
                        "model": model,
                        "prompt": "test",
                        "stream": False,
                        "options": {"max_tokens": 10}
                    },
                    timeout=5
                )
                available[model] = response.status_code == 200
                logger.info(f"Model {model}: {'✅ Available' if available[model] else '❌ Not available'}")
            except Exception as e:
                available[model] = False
                logger.warning(f"Model {model}: Error - {e}")
        
        return available
    
    def generate_response(self, message: str, task_type: str = "chat", 
                         context: Optional[Dict] = None, 
                         history: Optional[List[Dict]] = None,
                         model: Optional[str] = None,
                         **kwargs) -> Dict[str, Any]:
        """
        Universal response generator for ALL AI operations
        
        Args:
            message: Input message or query
            task_type: Type of task (chat, legal, research, etc.)
            context: Additional context information
            history: Conversation history
            model: Specific model to use (optional)
            **kwargs: Additional parameters
            
        Returns:
            Generated response with metadata
        """
        try:
            # Select the best model for the task
            if model and model in self.available_models and self.available_models[model]:
                selected_model = model
            else:
                selected_model = self._select_best_model(task_type)
            
            # Generate response
            response_text = self._call_ollama(message, task_type, selected_model, context, history)
            
            if response_text:
                return {
                    "success": True,
                    "text": response_text,
                    "model": selected_model,
                    "task_type": task_type,
                    "timestamp": datetime.now().isoformat(),
                    "context": context,
                    "metadata": {
                        "response_length": len(response_text),
                        "model_available": self.available_models.get(selected_model, False),
                        "free_model": True
                    }
                }
            else:
                return self._get_fallback_response(message, task_type)
                
        except Exception as e:
            logger.error(f"Error in generate_response: {e}")
            return {
                "success": False,
                "error": str(e),
                "text": f"I apologize, but I encountered an error: {str(e)}. Please try again.",
                "model": "error",
                "task_type": task_type,
                "timestamp": datetime.now().isoformat()
            }
    
    def _select_best_model(self, task_type: str) -> str:
        """Select the best available model for the task"""
        # Get the preferred model for this task
        preferred_model = self.model_mapping.get(task_type, "gemma2:2b")
        
        # Check if preferred model is available
        if self.available_models.get(preferred_model, False):
            return preferred_model
        
        # Fallback to any available model
        for model, available in self.available_models.items():
            if available:
                logger.info(f"Using fallback model {model} for task {task_type}")
                return model
        
        # Last resort
        return "gemma2:2b"
    
    def _call_ollama(self, message: str, task_type: str, model: str, 
                    context: Optional[Dict] = None, 
                    history: Optional[List[Dict]] = None) -> str:
        """Call Ollama API with optimized prompts"""
        try:
            # Build conversation context
            conversation_context = ""
            if history:
                recent_history = history[-4:] if len(history) > 4 else history
                for msg in recent_history:
                    role = "User" if msg.get('sender', msg.get('role', '')) == 'user' else "Assistant"
                    text = msg.get('text', msg.get('content', ''))
                    conversation_context += f"{role}: {text}\n"
            
            # Build context information
            context_info = ""
            if context:
                context_info = f"\nAdditional Context: {json.dumps(context, indent=2)}\n"
            
            # Get system prompt for the task
            system_prompt = self._get_system_prompt(task_type, context)
            full_prompt = f"{system_prompt}\n\n{conversation_context}{context_info}User: {message}\n\nAssistant:"
            
            payload = {
                "model": model,
                "prompt": full_prompt,
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "top_p": 0.9,
                    "max_tokens": 1500  # Increased for better responses
                }
            }
            
            response = requests.post(self.ollama_url, json=payload, timeout=45)
            
            if response.status_code == 200:
                result = response.json()
                return result.get("response", "").strip()
            else:
                logger.error(f"Ollama API error: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            logger.error(f"Ollama API error: {e}")
            return None
    
    def _get_system_prompt(self, task_type: str, context: Optional[Dict] = None) -> str:
        """Get optimized system prompt for the task type"""
        prompts = {
            "chat": """You are SmartProBono's AI Legal Assistant. Provide helpful, conversational legal guidance.

COMMUNICATION STYLE:
- Be friendly and approachable
- Use simple, clear language
- Provide specific, actionable advice when possible
- Always remind users this is general information, not legal advice

RESPONSE FORMAT:
- Start with a direct answer to their question
- Provide relevant details and context
- Suggest next steps or resources
- End with a disclaimer about consulting an attorney

Keep responses conversational and helpful.""",

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

            "legal_research": """You are a legal research specialist. Provide comprehensive, well-structured legal research.

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

Focus on creating practical, usable documents.""",

            "court_filing": """You are a court filing assistant for SmartProBono. Help with court document preparation and filing procedures.

COURT FILING GUIDANCE:
1. Document Requirements: What documents are needed
2. Filing Procedures: Step-by-step filing process
3. Deadlines: Important timeframes and deadlines
4. Fees: Applicable filing fees and payment methods
5. Jurisdiction: Court-specific requirements
6. Forms: Required forms and where to get them
7. Next Steps: Recommended actions

Provide practical, actionable guidance for court filings.""",

            "case_analysis": """You are a case analysis specialist. Analyze legal cases and provide comprehensive insights.

ANALYSIS FRAMEWORK:
1. Case Summary: Brief overview of the case
2. Key Issues: Main legal issues involved
3. Legal Analysis: Relevant laws and precedents
4. Strengths/Weaknesses: Case assessment
5. Recommendations: Suggested strategies
6. Research Needs: Additional research required
7. Timeline: Important dates and deadlines

Provide thorough, professional case analysis.""",

            "crm": """You are a CRM assistant for SmartProBono. Help manage client relationships and case information.

CRM ASSISTANCE:
- Client communication guidance
- Case status updates
- Document organization
- Appointment scheduling
- Follow-up reminders
- Data entry assistance

Be professional and organized in your responses.""",

            "voice": """You are a voice AI assistant for SmartProBono. Provide concise, clear responses optimized for speech.

VOICE OPTIMIZATION:
- Use conversational language
- Avoid complex punctuation
- Speak naturally and clearly
- Provide concise, focused answers
- Use transitions between topics
- End with clear next steps

Optimize for natural speech patterns.""",

            "research": """You are a research assistant. Provide comprehensive research and analysis.

RESEARCH FRAMEWORK:
1. Direct Answer: Clear response to the question
2. Key Findings: Important information discovered
3. Sources: Where information was found
4. Analysis: What the information means
5. Gaps: What additional research is needed
6. Recommendations: Suggested next steps

Be thorough and well-organized in your research.""",

            "analysis": """You are an analysis specialist. Provide detailed analysis and insights.

ANALYSIS FRAMEWORK:
1. Overview: Brief summary of what you're analyzing
2. Key Points: Main findings or issues
3. Detailed Analysis: In-depth examination
4. Implications: What this means
5. Recommendations: Suggested actions
6. Next Steps: What to do next

Provide comprehensive, actionable analysis.""",

            "document_analysis": """You are a document analysis specialist. Analyze legal documents and provide insights.

DOCUMENT ANALYSIS FRAMEWORK:
1. Document Type: What kind of document this is
2. Key Information: Important details extracted
3. Legal Issues: Any legal concerns or issues
4. Missing Elements: What might be missing
5. Recommendations: Suggested improvements
6. Next Steps: Recommended actions

Provide thorough document analysis."""
        }
        
        return prompts.get(task_type, prompts["chat"])
    
    def _get_fallback_response(self, message: str, task_type: str) -> Dict[str, Any]:
        """Get fallback response when Ollama is unavailable"""
        fallback_responses = {
            "chat": f"I understand you're asking about '{message}'. While I'd normally provide detailed guidance using our AI system, I'm currently experiencing technical difficulties. For immediate help, I recommend:\n\n1. Contacting your local legal aid organization\n2. Checking your state's legal resources website\n3. Consulting with a qualified attorney\n\nI apologize for the inconvenience and encourage you to try again in a few moments.",
            
            "legal": f"For legal analysis on '{message}', I'd typically provide comprehensive guidance. Since our AI system is temporarily unavailable, I suggest:\n\n1. Checking your state's legal code online\n2. Reviewing recent court decisions in your jurisdiction\n3. Consulting legal databases like Justia or FindLaw\n4. Speaking with a legal professional\n\nPlease try again shortly for AI-powered legal assistance.",
            
            "research": f"For research on '{message}', I'd normally provide comprehensive legal analysis. Since our AI system is temporarily unavailable, I suggest:\n\n1. Checking your state's legal code online\n2. Reviewing recent court decisions in your jurisdiction\n3. Consulting legal databases like Justia or FindLaw\n4. Speaking with a legal professional\n\nPlease try again shortly for AI-powered research assistance.",
            
            "document_drafting": f"I'd normally help draft documents related to '{message}', but our system is temporarily offline. For immediate document needs:\n\n1. Use standard legal templates from your state's court website\n2. Consult with a legal professional for complex documents\n3. Check legal aid organizations for free document assistance\n\nOur AI drafting service should be available again soon."
        }
        
        return {
            "success": False,
            "text": fallback_responses.get(task_type, fallback_responses["chat"]),
            "model": "fallback",
            "task_type": task_type,
            "timestamp": datetime.now().isoformat(),
            "metadata": {
                "fallback": True,
                "free_model": False
            }
        }
    
    # Convenience methods for different systems
    def chat_response(self, message: str, history: Optional[List[Dict]] = None) -> Dict[str, Any]:
        """Chat response for conversation systems"""
        return self.generate_response(message, "chat", history=history)
    
    def legal_analysis(self, query: str, jurisdiction: str = "state", context: Optional[Dict] = None) -> Dict[str, Any]:
        """Legal analysis for research systems"""
        analysis_context = {"jurisdiction": jurisdiction, **(context or {})}
        return self.generate_response(query, "legal", context=analysis_context)
    
    def document_analysis(self, document_text: str, document_type: str = "legal") -> Dict[str, Any]:
        """Document analysis for document processing systems"""
        context = {"document_type": document_type, "document_text": document_text}
        return self.generate_response(f"Analyze this {document_type} document", "document_analysis", context=context)
    
    def court_filing_help(self, filing_type: str, jurisdiction: str = "state") -> Dict[str, Any]:
        """Court filing assistance"""
        context = {"filing_type": filing_type, "jurisdiction": jurisdiction}
        return self.generate_response(f"Help with {filing_type} court filing", "court_filing", context=context)
    
    def crm_assistance(self, task: str, client_info: Optional[Dict] = None) -> Dict[str, Any]:
        """CRM system assistance"""
        context = {"client_info": client_info}
        return self.generate_response(task, "crm", context=context)
    
    def voice_response(self, message: str) -> Dict[str, Any]:
        """Voice-optimized response"""
        return self.generate_response(message, "voice")
    
    def research_response(self, query: str, research_type: str = "legal") -> Dict[str, Any]:
        """Research response for research systems"""
        context = {"research_type": research_type}
        return self.generate_response(query, "research", context=context)
    
    def get_status(self) -> Dict[str, Any]:
        """Get service status"""
        return {
            "status": "healthy" if any(self.available_models.values()) else "unhealthy",
            "available_models": self.available_models,
            "model_mapping": self.model_mapping,
            "ollama_url": self.ollama_url,
            "free_service": True,
            "timestamp": datetime.now().isoformat()
        }

# Global instance for easy import
free_ai_service = FreeAIService()
