"""
Enhanced AI Service for SmartProBono
Integrates our AI agent with existing AI services for comprehensive legal assistance
"""

import logging
from datetime import datetime
from backend.services.ai_service import AIService
from backend.services.smartprobono_agent_service import SmartProBonoAgentService
from backend.services.enhanced_ai_service import EnhancedAIService

logger = logging.getLogger(__name__)

class EnhancedAIService:
    """Enhanced AI service that combines existing AI with our SmartProBono agent"""
    
    def __init__(self):
        # Initialize existing AI service
        self.existing_ai = AIService()
        
        # Initialize SmartProBono agent
        self.smartprobono_agent = SmartProBonoAgentService()
        
        logger.info("Enhanced AI Service initialized with SmartProBono agent integration")
    
    def process_legal_request(self, message, user_context=None, user_role="client", task_type="chat"):
        """
        Process legal requests using the most appropriate AI service
        
        Args:
            message (str): User's message or request
            user_context (dict): User context information
            user_role (str): User's role (client, lawyer, admin, etc.)
            task_type (str): Type of task (chat, research, case_management, etc.)
            
        Returns:
            dict: Response from the appropriate AI service
        """
        try:
            # Determine which service to use based on the request
            if self._needs_agent_capabilities(message, task_type):
                logger.info(f"Using SmartProBono agent for request: {message[:50]}...")
                return self._process_with_agent(message, user_context, user_role)
            else:
                logger.info(f"Using existing AI service for request: {message[:50]}...")
                return self._process_with_existing_ai(message, user_context, task_type)
            
        except Exception as e:
            logger.error(f"Error processing legal request: {str(e)}")
            return {
                "error": "Failed to process request",
                "message": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
    
    def _needs_agent_capabilities(self, message, task_type):
        """Determine if the request needs agent capabilities"""
        
        # Always use agent for specific task types
        agent_task_types = [
            "case_management", "document_analysis", "legal_research", 
            "client_management", "notification", "meeting_scheduling"
        ]
        
        if task_type in agent_task_types:
            return True
        
        # Check for agent-specific keywords in the message
        agent_keywords = [
            "create a case", "new case", "case status", "update case",
            "analyze document", "document analysis", "contract review",
            "search case law", "legal precedent", "case law research",
            "add client", "client information", "client management",
            "send notification", "notify", "schedule meeting", "meeting",
            "generate document", "legal document", "compliance check",
            "search cases", "find cases", "case details", "case information"
        ]
        
        message_lower = message.lower()
        return any(keyword in message_lower for keyword in agent_keywords)
    
    def _process_with_agent(self, message, user_context, user_role):
        """Process request using SmartProBono agent"""
        try:
            response = self.smartprobono_agent.process_request(
                user_input=message,
                user_context=user_context,
                user_role=user_role,
                verbose=False
            )
            
            return {
                "response": response,
                "service": "smartprobono_agent",
                "timestamp": datetime.utcnow().isoformat(),
                "user_role": user_role
            }
            
        except Exception as e:
            logger.error(f"Error with SmartProBono agent: {str(e)}")
            # Fallback to existing AI service
            return self._process_with_existing_ai(message, user_context, "chat")
    
    def _process_with_existing_ai(self, message, user_context, task_type):
        """Process request using existing AI service"""
        try:
            # Use existing AI service
            response = self.existing_ai.generate_legal_response(
                message=message,
                task_type=task_type,
                history=user_context.get('history', []) if user_context else [],
                model=user_context.get('model', 'default') if user_context else 'default'
            )
            
            return {
                "response": response.get('content', response.get('message', str(response))),
                "service": "existing_ai",
                "timestamp": datetime.utcnow().isoformat(),
                "task_type": task_type
            }
            
        except Exception as e:
            logger.error(f"Error with existing AI service: {str(e)}")
            return {
                "error": "AI service unavailable",
                "message": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
    
    def generate_legal_response(self, message, task_type="chat", conversation_id=None, history=None, model="default", user_id=None, user_role="client"):
        """
        Main entry point for legal response generation
        Maintains compatibility with existing AI service interface
        """
        try:
            # Prepare user context
            user_context = {
                'conversation_id': conversation_id,
                'history': history or [],
                'model': model,
                'user_id': user_id,
                'timestamp': datetime.utcnow().isoformat()
            }
            
            # Process the request
            result = self.process_legal_request(
                message=message,
                user_context=user_context,
                user_role=user_role,
                task_type=task_type
            )
            
            # Format response to match existing AI service format
            if 'error' in result:
                return {
                    "id": f"resp_{int(datetime.utcnow().timestamp())}",
                    "created_at": datetime.utcnow().isoformat(),
                    "model": model,
                    "task_type": task_type,
                    "error": result['error'],
                    "message": result.get('message', 'Unknown error')
                }
            else:
                return {
                    "id": f"resp_{int(datetime.utcnow().timestamp())}",
                    "created_at": datetime.utcnow().isoformat(),
                    "model": model,
                    "task_type": task_type,
                    "content": result['response'],
                    "service_used": result['service'],
                    "usage_metadata": {
                        "prompt_token_count": len(message.split()),
                        "candidates_token_count": len(result['response'].split())
                    }
                }
                
        except Exception as e:
            logger.error(f"Error in generate_legal_response: {str(e)}")
            return {
                "id": f"resp_{int(datetime.utcnow().timestamp())}",
                "created_at": datetime.utcnow().isoformat(),
                "model": model,
                "task_type": task_type,
                "error": "Failed to generate response",
                "message": str(e)
            }
    
    def analyze_document(self, document_path, analysis_type="general", case_id=None, user_id=None):
        """
        Analyze document using appropriate AI service
        """
        try:
            if analysis_type in ["compliance", "contract", "legal_review", "case_law"]:
                # Use SmartProBono agent for specialized analysis
                response = self.smartprobono_agent.analyze_document(
                    working_directory=".",
                    document_path=document_path,
                    analysis_type=analysis_type,
                    case_id=case_id
                )
                
                return {
                    "analysis": response,
                    "service": "smartprobono_agent",
                    "analysis_type": analysis_type,
                    "timestamp": datetime.utcnow().isoformat()
                }
            else:
                # Use existing AI service for general analysis
                response = self.existing_ai.analyze_document(document_path, analysis_type)
                
                return {
                    "analysis": response,
                    "service": "existing_ai",
                    "analysis_type": analysis_type,
                    "timestamp": datetime.utcnow().isoformat()
                }
                
        except Exception as e:
            logger.error(f"Error analyzing document: {str(e)}")
            return {
                "error": "Failed to analyze document",
                "message": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
    
    def search_case_law(self, query, jurisdiction=None, case_type=None, user_id=None):
        """
        Search case law using SmartProBono agent
        """
        try:
            response = self.smartprobono_agent.search_case_law(
                working_directory=".",
                query=query,
                jurisdiction=jurisdiction,
                case_type=case_type
            )
            
            return {
                "results": response,
                "service": "smartprobono_agent",
                "query": query,
                "jurisdiction": jurisdiction,
                "case_type": case_type,
                "timestamp": datetime.utcnow().isoformat()
            }
                
        except Exception as e:
            logger.error(f"Error searching case law: {str(e)}")
            return {
                "error": "Failed to search case law",
                "message": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
    
    def create_case(self, case_data, user_id=None, user_role="client"):
        """
        Create a new case using SmartProBono agent
        """
        try:
            response = self.smartprobono_agent.create_case(
                working_directory=".",
                title=case_data.get('title', ''),
                description=case_data.get('description', ''),
                case_type=case_data.get('case_type', ''),
                client_id=case_data.get('client_id', ''),
                attorney_id=case_data.get('attorney_id'),
                priority=case_data.get('priority', 'medium'),
                practice_area=case_data.get('practice_area'),
                due_date=case_data.get('due_date')
            )
            
            return {
                "result": response,
                "service": "smartprobono_agent",
                "case_data": case_data,
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error creating case: {str(e)}")
            return {
                "error": "Failed to create case",
                "message": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
    
    def get_service_status(self):
        """Get status of all AI services"""
        try:
            return {
                "existing_ai": "available",
                "smartprobono_agent": "available" if not self.smartprobono_agent.mock_mode else "mock_mode",
                "enhanced_service": "available",
                "timestamp": datetime.utcnow().isoformat()
            }
        except Exception as e:
            return {
                "existing_ai": "unknown",
                "smartprobono_agent": "error",
                "enhanced_service": "error",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }