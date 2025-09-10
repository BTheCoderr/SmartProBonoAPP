"""
UNIFIED AI SERVICE - Single source of truth for all AI operations
Consolidates all AI chat, analysis, and response generation functionality
"""

import os
import logging
import requests
import json
from datetime import datetime
from typing import Dict, List, Optional, Any, Union
import random

logger = logging.getLogger(__name__)

class UnifiedAIService:
    """
    Single service for all AI operations:
    - Legal chat responses
    - Document analysis
    - Case law research
    - Response generation
    """
    
    def __init__(self):
        self.anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        self.ollama_url = "http://localhost:11434/api/generate"
        
        # Check which services are available
        self.claude_available = bool(self.anthropic_api_key)
        self.openai_available = bool(self.openai_api_key)
        self.ollama_available = self._check_ollama_availability()
    
    def _check_ollama_availability(self) -> bool:
        """Check if Ollama is running and available."""
        try:
            response = requests.get("http://localhost:11434/api/tags", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def generate_legal_response(self, message: str, task_type: str = "chat", 
                              conversation_id: Optional[str] = None, 
                              history: Optional[List[Dict]] = None, 
                              model: str = "auto", 
                              user_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Generate a legal response using the best available AI service.
        
        Args:
            message: User message
            task_type: Type of task (chat, research, draft)
            conversation_id: Conversation ID
            history: Previous conversation history
            model: AI model to use (auto, claude, openai, ollama)
            user_id: User ID
            
        Returns:
            Generated response
        """
        try:
            response_id = f"resp_{random.randint(1000, 9999)}_{int(datetime.now().timestamp())}"
            
            # Auto-select best available model
            if model == "auto":
                if self.claude_available:
                    model = "claude"
                elif self.openai_available:
                    model = "openai"
                elif self.ollama_available:
                    model = "ollama"
                else:
                    model = "fallback"
            
            # Generate response based on selected model
            if model == "claude" and self.claude_available:
                response_text = self._call_claude(message, task_type, history)
            elif model == "openai" and self.openai_available:
                response_text = self._call_openai(message, task_type, history)
            elif model == "ollama" and self.ollama_available:
                response_text = self._call_ollama(message, task_type, history)
            else:
                response_text = self._get_fallback_response(message, task_type)
            
            return {
                "id": response_id,
                "created_at": datetime.now().isoformat(),
                "model": model,
                "task_type": task_type,
                "text": response_text,
                "conversation_id": conversation_id,
                "user_id": user_id,
                "success": True
            }
            
        except Exception as e:
            logger.error(f"Error generating legal response: {e}")
            return {
                "id": f"error_{int(datetime.now().timestamp())}",
                "created_at": datetime.now().isoformat(),
                "model": "error",
                "task_type": task_type,
                "text": "I apologize, but I'm experiencing technical difficulties. Please try again later.",
                "conversation_id": conversation_id,
                "user_id": user_id,
                "success": False,
                "error": str(e)
            }
    
    def _call_claude(self, message: str, task_type: str, history: Optional[List[Dict]] = None) -> str:
        """Call Claude API for response generation."""
        try:
            import anthropic
            
            client = anthropic.Anthropic(api_key=self.anthropic_api_key)
            
            # Build conversation context
            messages = []
            if history:
                for msg in history[-5:]:  # Last 5 messages
                    role = "user" if msg.get('sender') == 'user' else "assistant"
                    messages.append({
                        "role": role,
                        "content": msg.get('text', '')
                    })
            
            messages.append({"role": "user", "content": message})
            
            # Get system prompt
            system_prompt = self._get_system_prompt(task_type)
            
            response = client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=1000,
                temperature=0.3,
                system=system_prompt,
                messages=messages
            )
            
            return response.content[0].text
            
        except Exception as e:
            logger.error(f"Claude API error: {e}")
            return self._get_fallback_response(message, task_type)
    
    def _call_openai(self, message: str, task_type: str, history: Optional[List[Dict]] = None) -> str:
        """Call OpenAI API for response generation."""
        try:
            import openai
            
            client = openai.OpenAI(api_key=self.openai_api_key)
            
            # Build conversation context
            messages = [{"role": "system", "content": self._get_system_prompt(task_type)}]
            
            if history:
                for msg in history[-5:]:  # Last 5 messages
                    role = "user" if msg.get('sender') == 'user' else "assistant"
                    messages.append({
                        "role": role,
                        "content": msg.get('text', '')
                    })
            
            messages.append({"role": "user", "content": message})
            
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                max_tokens=1000,
                temperature=0.3
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            return self._get_fallback_response(message, task_type)
    
    def _call_ollama(self, message: str, task_type: str, history: Optional[List[Dict]] = None) -> str:
        """Call Ollama API for response generation."""
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
                logger.error(f"Ollama API error: {response.status_code}")
                return self._get_fallback_response(message, task_type)
                
        except Exception as e:
            logger.error(f"Ollama API error: {e}")
            return self._get_fallback_response(message, task_type)
    
    def _get_system_prompt(self, task_type: str) -> str:
        """Get system prompt based on task type."""
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

Focus on creating practical, usable documents.""",

            "analysis": """You are a legal document analysis assistant. Analyze documents and provide insights.

ANALYSIS FRAMEWORK:
1. Document Type: Identify the type of legal document
2. Key Terms: Highlight important legal terms and clauses
3. Potential Issues: Identify areas of concern
4. Recommendations: Suggest improvements or next steps
5. Risk Assessment: Evaluate potential risks

Be thorough and professional in your analysis."""
        }
        
        return prompts.get(task_type, prompts["chat"])
    
    def _get_fallback_response(self, message: str, task_type: str) -> str:
        """Fallback responses when all AI services are unavailable."""
        fallback_responses = {
            "chat": f"I understand you're asking about: {message}\n\nI'm currently experiencing technical difficulties with my AI services. For immediate legal assistance, please:\n\n1. Contact a qualified attorney\n2. Visit your local legal aid office\n3. Check online legal resources\n\nI apologize for the inconvenience and will be back online soon.",
            
            "research": f"Research request: {message}\n\nI'm currently unable to access my research databases. For legal research assistance, please:\n\n1. Consult with a legal professional\n2. Visit your local law library\n3. Use online legal databases\n4. Contact legal aid organizations\n\nI'll be back online shortly to help with your research needs.",
            
            "draft": f"Document drafting request: {message}\n\nI'm currently unable to access my document generation tools. For document assistance, please:\n\n1. Use standard legal document templates\n2. Consult with a legal professional\n3. Visit legal aid document resources\n4. Check online legal form libraries\n\nI'll be back online soon to help with your document needs.",
            
            "analysis": f"Document analysis request: {message}\n\nI'm currently unable to access my analysis tools. For document analysis, please:\n\n1. Have a legal professional review the document\n2. Use online legal analysis tools\n3. Consult legal aid services\n4. Check document review services\n\nI'll be back online shortly to help with your analysis needs."
        }
        
        return fallback_responses.get(task_type, fallback_responses["chat"])
    
    def analyze_document_content(self, text: str, document_type: str = "generic") -> Dict[str, Any]:
        """
        Analyze document content for legal information.
        
        Args:
            text: Document text content
            document_type: Type of document
            
        Returns:
            Analysis results
        """
        try:
            # Basic text analysis
            word_count = len(text.split())
            char_count = len(text)
            
            # Extract basic information
            analysis = {
                "success": True,
                "document_type": document_type,
                "word_count": word_count,
                "char_count": char_count,
                "analysis_timestamp": datetime.now().isoformat(),
                "confidence": 0.8,
                "summary": self._generate_summary(text),
                "key_terms": self._extract_key_terms(text),
                "potential_issues": self._identify_issues(text),
                "recommendations": self._generate_recommendations(text, document_type)
            }
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing document content: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def _generate_summary(self, text: str) -> str:
        """Generate a summary of the document."""
        # Simple extractive summary - take first few sentences
        sentences = text.split('. ')
        if len(sentences) > 3:
            return '. '.join(sentences[:3]) + '.'
        return text[:200] + "..." if len(text) > 200 else text
    
    def _extract_key_terms(self, text: str) -> List[str]:
        """Extract key legal terms from the text."""
        legal_terms = [
            'contract', 'agreement', 'lease', 'liability', 'damages',
            'breach', 'warranty', 'indemnification', 'jurisdiction',
            'arbitration', 'mediation', 'force majeure', 'termination',
            'payment', 'obligation', 'right', 'duty', 'clause'
        ]
        
        found_terms = []
        text_lower = text.lower()
        for term in legal_terms:
            if term in text_lower:
                found_terms.append(term)
        
        return found_terms[:10]  # Limit to 10 terms
    
    def _identify_issues(self, text: str) -> List[str]:
        """Identify potential legal issues in the text."""
        issues = []
        text_lower = text.lower()
        
        if 'liability' in text_lower and 'limit' in text_lower:
            issues.append("Limited liability clause present")
        if 'termination' in text_lower and 'notice' in text_lower:
            issues.append("Termination clause requires notice")
        if 'payment' in text_lower and 'late' in text_lower:
            issues.append("Late payment penalties may apply")
        if 'arbitration' in text_lower:
            issues.append("Arbitration clause may limit court access")
        
        return issues
    
    def _generate_recommendations(self, text: str, document_type: str) -> List[str]:
        """Generate recommendations based on document analysis."""
        recommendations = [
            "Review all terms and conditions carefully",
            "Consider consulting with a legal professional",
            "Ensure all parties understand their obligations"
        ]
        
        if document_type.lower() in ['contract', 'agreement']:
            recommendations.append("Verify all parties have signed the document")
            recommendations.append("Check for any missing essential terms")
        
        return recommendations

# Create singleton instance
unified_ai_service = UnifiedAIService()
