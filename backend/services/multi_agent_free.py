"""
Multi-Agent System with FREE Models
Uses: Ollama (free) + Google Gemini (free tier: 1500 requests/day)

Agents:
1. Legal Research Agent - Gemini (best for complex research)
2. Document Analysis Agent - Gemma2:2b (best for legal docs)
3. Case Manager Agent - Tinyllama (fast for case management)
4. Client Support Agent - Gemini (best for conversations)
5. Court Filing Agent - Gemma2:2b (legal document generation)
6. Compliance Agent - Qwen (good for checking compliance)
"""

import os
import logging
import requests
import json
from datetime import datetime
from typing import Dict, List, Optional, Any
import google.generativeai as genai
from dotenv import load_dotenv, find_dotenv

# Load environment variables (find .env in project root)
load_dotenv(find_dotenv())

logger = logging.getLogger(__name__)

class MultiAgentFree:
    """Multi-agent system using free models"""
    
    def __init__(self):
        # Ollama setup
        self.ollama_url = "http://localhost:11434/api/generate"
        
        # Gemini setup (FREE tier!)
        self.gemini_api_key = os.getenv('GEMINI_API_KEY')
        if self.gemini_api_key:
            try:
                genai.configure(api_key=self.gemini_api_key)
                self.gemini_model = genai.GenerativeModel('gemini-2.0-flash')  # Free, fast model
                self.gemini_available = True
                logger.info("✅ Gemini 2.0 Flash available (FREE tier: 1500 requests/day)")
            except Exception as e:
                logger.error(f"Failed to initialize Gemini: {e}")
                self.gemini_available = False
        else:
            self.gemini_available = False
            logger.warning("⚠️ GEMINI_API_KEY not set - using Ollama fallback")
        
        # Agent definitions
        self.agents = {
            "legal_research": {
                "name": "Legal Research Agent",
                "model": "gemini" if self.gemini_available else "gemma2:2b",
                "description": "Researches legal precedents, case law, and statutes",
                "expertise": ["case_law", "statutes", "legal_research", "precedents"]
            },
            "document_analysis": {
                "name": "Document Analysis Agent",
                "model": "gemma2:2b",
                "description": "Analyzes legal documents, contracts, and agreements",
                "expertise": ["contracts", "agreements", "document_review", "legal_documents"]
            },
            "case_manager": {
                "name": "Case Manager Agent", 
                "model": "tinyllama:1.1b",
                "description": "Manages cases, tracks deadlines, and coordinates tasks",
                "expertise": ["case_management", "deadlines", "task_tracking", "coordination"]
            },
            "client_support": {
                "name": "Client Support Agent",
                "model": "gemini" if self.gemini_available else "tinyllama:1.1b",
                "description": "Provides client support and answers questions",
                "expertise": ["client_questions", "support", "guidance", "information"]
            },
            "court_filing": {
                "name": "Court Filing Agent",
                "model": "gemma2:2b",
                "description": "Assists with court filings and legal forms",
                "expertise": ["court_filings", "legal_forms", "court_procedures", "filing_deadlines"]
            },
            "compliance": {
                "name": "Compliance Agent",
                "model": "qwen2.5:0.5b",
                "description": "Checks legal compliance and regulatory requirements",
                "expertise": ["compliance", "regulations", "legal_requirements", "ethical_guidelines"]
            }
        }
        
        logger.info(f"✅ Multi-Agent System initialized with {len(self.agents)} agents")
    
    def route_to_agent(self, message: str, task_type: Optional[str] = None) -> str:
        """Route message to the best agent"""
        
        # If task type is specified, use direct routing
        if task_type:
            agent_mapping = {
                "legal_research": "legal_research",
                "research": "legal_research",
                "case_law": "legal_research",
                
                "document_analysis": "document_analysis",
                "contract": "document_analysis",
                "document": "document_analysis",
                
                "case_management": "case_manager",
                "deadline": "case_manager",
                "task": "case_manager",
                
                "client_support": "client_support",
                "chat": "client_support",
                "question": "client_support",
                
                "court_filing": "court_filing",
                "filing": "court_filing",
                "form": "court_filing",
                
                "compliance": "compliance",
                "regulation": "compliance",
                "ethical": "compliance"
            }
            
            agent_id = agent_mapping.get(task_type, "client_support")
        else:
            # Intelligent routing based on message content
            message_lower = message.lower()
            
            # Legal research keywords
            if any(word in message_lower for word in ["case law", "precedent", "statute", "research", "court decision"]):
                agent_id = "legal_research"
            
            # Document analysis keywords
            elif any(word in message_lower for word in ["contract", "agreement", "document", "review", "analyze"]):
                agent_id = "document_analysis"
            
            # Court filing keywords
            elif any(word in message_lower for word in ["file", "filing", "court", "form", "motion"]):
                agent_id = "court_filing"
            
            # Case management keywords
            elif any(word in message_lower for word in ["deadline", "case status", "track", "manage", "schedule"]):
                agent_id = "case_manager"
            
            # Compliance keywords
            elif any(word in message_lower for word in ["compliance", "regulation", "ethical", "rule"]):
                agent_id = "compliance"
            
            # Default to client support
            else:
                agent_id = "client_support"
        
        return agent_id
    
    def process_with_agent(self, message: str, agent_id: Optional[str] = None, 
                          task_type: Optional[str] = None, 
                          context: Optional[Dict] = None) -> Dict[str, Any]:
        """Process message with specific agent"""
        
        try:
            # Route to best agent if not specified
            if not agent_id:
                agent_id = self.route_to_agent(message, task_type)
            
            agent = self.agents.get(agent_id)
            if not agent:
                return {"error": f"Agent {agent_id} not found", "success": False}
            
            logger.info(f"🤖 Routing to: {agent['name']} ({agent['model']})")
            
            # Get system prompt for the agent
            system_prompt = self._get_agent_prompt(agent_id, agent)
            
            # Generate response using the agent's model
            if agent["model"] == "gemini" and self.gemini_available:
                response_text = self._call_gemini(message, system_prompt, context)
            else:
                response_text = self._call_ollama(message, system_prompt, agent["model"], context)
            
            if response_text:
                return {
                    "success": True,
                    "text": response_text,
                    "agent": agent["name"],
                    "agent_id": agent_id,
                    "model": agent["model"],
                    "timestamp": datetime.now().isoformat(),
                    "context": context,
                    "metadata": {
                        "response_length": len(response_text),
                        "free_model": True,
                        "agent_expertise": agent["expertise"]
                    }
                }
            else:
                return self._get_fallback_response(message, agent_id)
                
        except Exception as e:
            logger.error(f"Error in process_with_agent: {e}")
            return {
                "success": False,
                "error": str(e),
                "text": f"I apologize, but I encountered an error: {str(e)}. Please try again.",
                "agent": "error",
                "timestamp": datetime.now().isoformat()
            }
    
    def _call_gemini(self, message: str, system_prompt: str, context: Optional[Dict] = None) -> str:
        """Call free Gemini API"""
        try:
            # Build full prompt
            context_info = ""
            if context:
                context_info = f"\n\nAdditional Context: {json.dumps(context, indent=2)}"
            
            full_prompt = f"{system_prompt}\n\n{context_info}\n\nUser Question: {message}\n\nYour Response:"
            
            # Generate response
            response = self.gemini_model.generate_content(full_prompt)
            return response.text.strip()
            
        except Exception as e:
            logger.error(f"Gemini API error: {e}")
            return None
    
    def _call_ollama(self, message: str, system_prompt: str, model: str, context: Optional[Dict] = None) -> str:
        """Call Ollama API"""
        try:
            # Build context information
            context_info = ""
            if context:
                context_info = f"\n\nAdditional Context: {json.dumps(context, indent=2)}"
            
            full_prompt = f"{system_prompt}\n\n{context_info}\n\nUser Question: {message}\n\nYour Response:"
            
            payload = {
                "model": model,
                "prompt": full_prompt,
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "top_p": 0.9,
                    "num_predict": 200  # Faster responses - 200 tokens ~= 150 words
                }
            }
            
            response = requests.post(self.ollama_url, json=payload, timeout=45)
            
            if response.status_code == 200:
                result = response.json()
                return result.get("response", "").strip()
            else:
                logger.error(f"Ollama API error: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"Ollama API error: {e}")
            return None
    
    def _get_agent_prompt(self, agent_id: str, agent: Dict) -> str:
        """Get system prompt for specific agent"""
        
        prompts = {
            "legal_research": f"""You are the {agent['name']} for SmartProBono. You specialize in legal research and case law analysis.

YOUR EXPERTISE:
- Researching legal precedents and case law
- Finding relevant statutes and regulations
- Analyzing court decisions and their implications
- Providing comprehensive legal research

RESEARCH FRAMEWORK:
1. Direct Answer: Clear response to the research question
2. Legal Principles: Key legal concepts and precedents
3. Case Law: Relevant court decisions and their holdings
4. Statutes: Applicable laws and regulations
5. Analysis: How these apply to the specific situation
6. Resources: Where to find more detailed information
7. Disclaimer: This is research information, not legal advice

Provide thorough, well-researched legal analysis.""",

            "document_analysis": f"""You are the {agent['name']} for SmartProBono. You specialize in analyzing legal documents.

YOUR EXPERTISE:
- Reviewing contracts and agreements
- Analyzing legal documents for issues
- Identifying missing or problematic clauses
- Providing document improvement suggestions

ANALYSIS FRAMEWORK:
1. Document Overview: Type and purpose of document
2. Key Provisions: Important terms and conditions
3. Strengths: Well-drafted sections
4. Concerns: Potential issues or missing elements
5. Recommendations: Suggested improvements
6. Next Steps: What to do with this analysis
7. Disclaimer: This is document analysis, not legal advice

Provide detailed, professional document analysis.""",

            "case_manager": f"""You are the {agent['name']} for SmartProBono. You specialize in case management and coordination.

YOUR EXPERTISE:
- Managing case timelines and deadlines
- Tracking case progress and status
- Coordinating tasks and activities
- Providing case organization guidance

MANAGEMENT FRAMEWORK:
1. Current Status: Where things stand now
2. Key Deadlines: Important dates and timeframes
3. Required Actions: What needs to be done
4. Priorities: What's most important
5. Coordination: Who needs to do what
6. Next Steps: Immediate actions needed
7. Reminders: Important things to remember

Provide clear, organized case management guidance.""",

            "client_support": f"""You are a legal assistant. Give brief, helpful answers. Note: This is general info, not legal advice.""",

            "court_filing": f"""You are the {agent['name']} for SmartProBono. You specialize in court filings and procedures.

YOUR EXPERTISE:
- Court filing procedures and requirements
- Legal forms and document preparation
- Filing deadlines and timeframes
- Court-specific rules and procedures

FILING FRAMEWORK:
1. Filing Requirements: What documents are needed
2. Procedures: Step-by-step filing process
3. Deadlines: Important timeframes
4. Fees: Applicable costs and payment
5. Court Rules: Specific requirements
6. Forms: Required forms and where to get them
7. Next Steps: What to do next
8. Disclaimer: Verify requirements with court

Provide practical, actionable court filing guidance.""",

            "compliance": f"""You are the {agent['name']} for SmartProBono. You specialize in legal compliance and regulations.

YOUR EXPERTISE:
- Checking legal compliance requirements
- Understanding regulations and rules
- Identifying potential compliance issues
- Providing ethical guidance

COMPLIANCE FRAMEWORK:
1. Requirements: What's legally required
2. Regulations: Applicable rules and standards
3. Compliance Check: Are requirements being met
4. Issues: Potential compliance concerns
5. Recommendations: How to ensure compliance
6. Resources: Where to learn more
7. Next Steps: Actions to take
8. Disclaimer: Consult legal/compliance professionals

Provide thorough compliance guidance."""
        }
        
        return prompts.get(agent_id, f"You are the {agent['name']}. Provide helpful assistance.")
    
    def _get_fallback_response(self, message: str, agent_id: str) -> Dict[str, Any]:
        """Get fallback response when agent fails"""
        agent = self.agents.get(agent_id, {})
        agent_name = agent.get('name', 'AI Assistant')
        
        return {
            "success": False,
            "text": f"I'm the {agent_name}, but I'm currently experiencing technical difficulties. For immediate assistance, please:\n\n1. Try again in a moment\n2. Consult with a legal professional\n3. Check online legal resources\n\nI apologize for the inconvenience.",
            "agent": agent_name,
            "agent_id": agent_id,
            "model": "fallback",
            "timestamp": datetime.now().isoformat()
        }
    
    def get_available_agents(self) -> Dict[str, Any]:
        """Get list of available agents"""
        return {
            "agents": self.agents,
            "gemini_available": self.gemini_available,
            "gemini_free_tier": "1500 requests/day" if self.gemini_available else "Not configured",
            "ollama_models": ["gemma2:2b", "tinyllama:1.1b", "qwen2.5:0.5b"],
            "total_agents": len(self.agents)
        }
    
    def multi_agent_collaboration(self, message: str, agents: List[str]) -> Dict[str, Any]:
        """Have multiple agents collaborate on a task"""
        
        results = []
        for agent_id in agents:
            if agent_id in self.agents:
                response = self.process_with_agent(message, agent_id=agent_id)
                results.append({
                    "agent": agent_id,
                    "agent_name": self.agents[agent_id]["name"],
                    "response": response.get("text", ""),
                    "success": response.get("success", False)
                })
        
        # Combine insights from all agents
        combined_text = "**Multi-Agent Analysis:**\n\n"
        for i, result in enumerate(results, 1):
            combined_text += f"**{result['agent_name']}:**\n{result['response']}\n\n"
        
        return {
            "success": True,
            "text": combined_text,
            "agents_consulted": len(results),
            "individual_responses": results,
            "collaboration": True,
            "timestamp": datetime.now().isoformat()
        }

# Global instance
multi_agent_free = MultiAgentFree()
