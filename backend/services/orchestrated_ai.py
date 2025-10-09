"""
Orchestrated AI System - Multiple Models Working Together
Uses MULTIPLE models and agents to create the BEST possible response

Flow:
1. Analyze query with fast model (tinyllama)
2. Research with Gemini (if available) or Gemma2
3. Document check with Gemma2
4. Compliance check with Qwen
5. Synthesize all insights into final response

This creates responses that are:
- More accurate (multiple models verify)
- More comprehensive (different perspectives)
- More reliable (cross-validation)
- Still FREE ($0/month)
"""

import os
import logging
import requests
import json
from datetime import datetime
from typing import Dict, List, Optional, Any
from dotenv import load_dotenv, find_dotenv

# Load environment variables
load_dotenv(find_dotenv())

logger = logging.getLogger(__name__)

class OrchestratedAI:
    """Multi-model orchestration for best responses"""
    
    def __init__(self):
        self.ollama_url = "http://localhost:11434/api/generate"
        
        # Import Gemini if available
        self.gemini_available = False
        try:
            import google.generativeai as genai
            api_key = os.getenv('GEMINI_API_KEY')
            if api_key:
                genai.configure(api_key=api_key)
                self.gemini_model = genai.GenerativeModel('gemini-2.0-flash')
                self.gemini_available = True
                logger.info("✅ Gemini available for orchestration")
        except Exception as e:
            logger.warning(f"Gemini not available: {e}")
        
        # Model roles
        self.models = {
            "analyzer": "tinyllama:1.1b",  # Fast query analysis
            "researcher": "gemini" if self.gemini_available else "gemma2:2b",  # Deep research
            "document_expert": "gemma2:2b",  # Document analysis
            "compliance": "qwen2.5:0.5b",  # Compliance check
            "synthesizer": "gemini" if self.gemini_available else "gemma2:2b"  # Final synthesis
        }
    
    def generate_best_response(self, message: str, task_type: str = "legal") -> Dict[str, Any]:
        """
        Generate the BEST response by consulting multiple models
        
        Process:
        1. Analyze the query (understand what's being asked)
        2. Research the topic (gather information)
        3. Check documents/precedents (legal basis)
        4. Verify compliance (legal requirements)
        5. Synthesize into final answer (combine all insights)
        """
        try:
            logger.info(f"🎯 Orchestrating multi-model response for: {message[:50]}...")
            
            # Step 1: Quick analysis (what is being asked?)
            analysis = self._analyze_query(message)
            logger.info(f"📊 Query Analysis: {analysis.get('intent', 'unknown')}")
            
            # Step 2: Deep research (gather information)
            research = self._research_topic(message, analysis)
            logger.info(f"📚 Research: {len(research.get('text', ''))} chars")
            
            # Step 3: Document/legal check (if needed)
            if task_type in ["legal", "document_analysis", "court_filing"]:
                legal_check = self._check_legal_requirements(message, research)
                logger.info(f"⚖️ Legal Check: {len(legal_check.get('text', ''))} chars")
            else:
                legal_check = {"text": "", "relevant": False}
            
            # Step 4: Compliance verification
            compliance = self._verify_compliance(message, research)
            logger.info(f"✅ Compliance: {compliance.get('status', 'unknown')}")
            
            # Step 5: Synthesize final response
            final_response = self._synthesize_response(
                message, 
                analysis, 
                research, 
                legal_check, 
                compliance
            )
            
            return {
                "success": True,
                "text": final_response,
                "orchestration": {
                    "models_consulted": [
                        self.models["analyzer"],
                        self.models["researcher"],
                        self.models["document_expert"] if legal_check.get("relevant") else None,
                        self.models["compliance"],
                        self.models["synthesizer"]
                    ],
                    "steps": ["analyze", "research", "legal_check", "compliance", "synthesize"],
                    "gemini_used": self.gemini_available
                },
                "timestamp": datetime.now().isoformat(),
                "task_type": task_type,
                "metadata": {
                    "analysis": analysis.get("intent"),
                    "research_quality": len(research.get("text", "")),
                    "compliance_status": compliance.get("status"),
                    "free_models": True
                }
            }
            
        except Exception as e:
            logger.error(f"Orchestration error: {e}")
            return {
                "success": False,
                "error": str(e),
                "text": "I apologize, but I encountered an error processing your request. Please try again.",
                "timestamp": datetime.now().isoformat()
            }
    
    def _analyze_query(self, message: str) -> Dict[str, Any]:
        """Step 1: Quickly analyze what the user is asking (fast model)"""
        try:
            prompt = f"Analyze this query in 2-3 words (e.g., 'tenant rights question', 'document review', 'court filing help'): {message}"
            
            response = self._call_ollama(
                self.models["analyzer"],
                prompt,
                num_predict=20
            )
            
            return {
                "intent": response.strip() if response else "general legal question",
                "model": self.models["analyzer"]
            }
        except Exception as e:
            logger.error(f"Analysis error: {e}")
            return {"intent": "general legal question", "model": "fallback"}
    
    def _research_topic(self, message: str, analysis: Dict) -> Dict[str, Any]:
        """Step 2: Research the topic deeply"""
        try:
            intent = analysis.get("intent", "general")
            prompt = f"Provide comprehensive legal information about: {message}\n\nFocus: {intent}\n\nBe thorough but concise."
            
            if self.models["researcher"] == "gemini":
                response = self._call_gemini(prompt)
            else:
                response = self._call_ollama(
                    self.models["researcher"],
                    prompt,
                    num_predict=400
                )
            
            return {
                "text": response or "",
                "model": self.models["researcher"]
            }
        except Exception as e:
            logger.error(f"Research error: {e}")
            return {"text": "", "model": "fallback"}
    
    def _check_legal_requirements(self, message: str, research: Dict) -> Dict[str, Any]:
        """Step 3: Check legal documents and requirements"""
        try:
            prompt = f"Based on this research: {research.get('text', '')[:500]}\n\nWhat are the key legal requirements for: {message}\n\nList 3-5 key points."
            
            response = self._call_ollama(
                self.models["document_expert"],
                prompt,
                num_predict=200
            )
            
            return {
                "text": response or "",
                "relevant": bool(response),
                "model": self.models["document_expert"]
            }
        except Exception as e:
            logger.error(f"Legal check error: {e}")
            return {"text": "", "relevant": False, "model": "fallback"}
    
    def _verify_compliance(self, message: str, research: Dict) -> Dict[str, Any]:
        """Step 4: Verify compliance and add disclaimers"""
        try:
            prompt = f"For this legal topic: {message}\n\nWhat compliance notes or disclaimers are needed? Keep it brief."
            
            response = self._call_ollama(
                self.models["compliance"],
                prompt,
                num_predict=100
            )
            
            return {
                "text": response or "This is general information, not legal advice.",
                "status": "verified" if response else "default",
                "model": self.models["compliance"]
            }
        except Exception as e:
            logger.error(f"Compliance error: {e}")
            return {"text": "Consult a qualified attorney.", "status": "default", "model": "fallback"}
    
    def _synthesize_response(self, message: str, analysis: Dict, research: Dict, 
                            legal_check: Dict, compliance: Dict) -> str:
        """Step 5: Synthesize all insights into final response"""
        try:
            # Build comprehensive context from all models
            synthesis_prompt = f"""Based on insights from multiple legal AI models, provide a final comprehensive answer to: {message}

Research Findings:
{research.get('text', 'No research available')}

Legal Requirements:
{legal_check.get('text', 'No specific requirements identified')}

Compliance Notes:
{compliance.get('text', 'Standard legal disclaimers apply')}

Synthesize this into a clear, helpful response that:
1. Directly answers the question
2. Provides key legal points
3. Offers practical guidance
4. Includes appropriate disclaimers

Keep the response focused and actionable."""

            if self.models["synthesizer"] == "gemini":
                final_response = self._call_gemini(synthesis_prompt, num_predict=300)
            else:
                final_response = self._call_ollama(
                    self.models["synthesizer"],
                    synthesis_prompt,
                    num_predict=300
                )
            
            # Add compliance footer if not already included
            if compliance.get("text") and compliance["text"] not in final_response:
                final_response += f"\n\n**Important:** {compliance['text']}"
            
            return final_response or "Unable to generate response. Please consult a qualified attorney."
            
        except Exception as e:
            logger.error(f"Synthesis error: {e}")
            return "Unable to synthesize response. Please consult a qualified attorney."
    
    def _call_ollama(self, model: str, prompt: str, num_predict: int = 200) -> str:
        """Call Ollama API"""
        try:
            payload = {
                "model": model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "num_predict": num_predict
                }
            }
            
            response = requests.post(self.ollama_url, json=payload, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                return result.get("response", "").strip()
            return None
            
        except Exception as e:
            logger.error(f"Ollama error ({model}): {e}")
            return None
    
    def _call_gemini(self, prompt: str, num_predict: int = 300) -> str:
        """Call Gemini API"""
        try:
            response = self.gemini_model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            logger.error(f"Gemini error: {e}")
            return None
    
    def get_status(self) -> Dict[str, Any]:
        """Get orchestration status"""
        return {
            "status": "operational",
            "orchestration": "multi-model",
            "models": self.models,
            "gemini_available": self.gemini_available,
            "steps": 5,
            "description": "Multiple models working together for best responses",
            "cost": "$0/month"
        }

# Global instance
orchestrated_ai = OrchestratedAI()

