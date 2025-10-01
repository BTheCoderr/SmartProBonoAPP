"""
Voice-Enhanced AI Service for SmartProBono
Integrates voice capabilities with existing multi-model AI system
"""

import logging
import asyncio
import os
from datetime import datetime
from services.ai_service import AIService
from services.simple_smartprobono_agent_service import SimpleSmartProBonoAgentService

logger = logging.getLogger(__name__)

class VoiceEnhancedAIService:
    """Enhanced AI service that combines existing AI with voice capabilities"""
    
    def __init__(self):
        # Initialize existing AI service
        self.existing_ai = AIService()
        
        # Initialize SmartProBono agent
        self.smartprobono_agent = SimpleSmartProBonoAgentService()
        
        # Initialize voice capabilities
        self.voice_enabled = self._initialize_voice_components()
        
        logger.info("Voice-Enhanced AI Service initialized with multi-model and voice capabilities")
    
    def _initialize_voice_components(self):
        """Initialize voice components if available"""
        try:
            # Check if we have the required voice packages
            import livekit
            from cerebras.cloud.sdk import Cerebras
            
            # Check for API keys
            cerebras_key = os.getenv("CEREBRAS_API_KEY")
            livekit_key = os.getenv("LIVEKIT_API_KEY")
            
            if cerebras_key and livekit_key:
                self.voice_components = {
                    "cerebras_client": Cerebras(api_key=cerebras_key),
                    "livekit_available": True
                }
                logger.info("Voice components initialized successfully")
                return True
            else:
                logger.warning("Voice API keys not found - voice features disabled")
                return False
                
        except ImportError as e:
            logger.warning(f"Voice packages not available: {e}")
            return False
        except Exception as e:
            logger.warning(f"Voice initialization failed: {e}")
            return False
    
    async def process_request(self, message, user_context=None, user_role="client", task_type="chat", voice_enabled=False):
        """
        Process requests using the most appropriate AI service
        
        Args:
            message (str): User's message or request
            user_context (dict): User context information
            user_role (str): User's role (client, lawyer, admin, etc.)
            task_type (str): Type of task (chat, research, case_management, sales, etc.)
            voice_enabled (bool): Whether voice capabilities should be used
            
        Returns:
            dict: Response from the appropriate AI service
        """
        try:
            # Determine which service to use based on the request
            if voice_enabled and self.voice_enabled and self._is_voice_request(message, task_type):
                logger.info(f"Using voice AI for request: {message[:50]}...")
                return await self._process_with_voice(message, user_context, user_role, task_type)
            elif self._needs_agent_capabilities(message, task_type):
                logger.info(f"Using SmartProBono agent for request: {message[:50]}...")
                return self._process_with_agent(message, user_context, user_role)
            else:
                logger.info(f"Using existing AI service for request: {message[:50]}...")
                return self._process_with_existing_ai(message, user_context, task_type)
            
        except Exception as e:
            logger.error(f"Error processing request: {str(e)}")
            return {
                "error": f"Failed to process request: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }
    
    def _is_voice_request(self, message, task_type):
        """Determine if this should be handled by voice AI"""
        voice_keywords = [
            "sales", "pricing", "demo", "technical support", 
            "switch to", "transfer", "speak", "call", "voice"
        ]
        
        message_lower = message.lower()
        task_lower = task_type.lower()
        
        return any(keyword in message_lower or keyword in task_lower for keyword in voice_keywords)
    
    def _needs_agent_capabilities(self, message, task_type):
        """Determine if this needs SmartProBono agent capabilities"""
        agent_keywords = [
            "create case", "search cases", "analyze document", "case law",
            "schedule meeting", "add client", "generate document", "legal research"
        ]
        
        message_lower = message.lower()
        task_lower = task_type.lower()
        
        return any(keyword in message_lower or keyword in task_lower for keyword in agent_keywords)
    
    async def _process_with_voice(self, message, user_context, user_role, task_type):
        """Process request using voice AI (Cerebras)"""
        try:
            # Load SmartProBono context
            context = self._load_smartprobono_context()
            
            # Create system prompt for voice AI
            system_prompt = f"""
You are a professional AI assistant for SmartProBono, an AI-powered legal platform.
You communicate by voice, so avoid bullets, slashes, or non-pronounceable punctuation.

You have access to the following company information:

{context}

CRITICAL RULES:
- ONLY use information from the context above
- If asked about something not in the context, say "I don't have that information available"
- DO NOT make up prices, features, or any other details
- Quote directly from the context when possible
- Be professional, helpful, and solution-focused
- Focus on the value proposition and ROI

You can transfer to specialists:
- Use switch_to_tech_support() for technical questions
- Use switch_to_pricing() for detailed pricing discussions
"""
            
            # Generate response using Cerebras
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message}
            ]
            
            stream = self.voice_components["cerebras_client"].chat.completions.create(
                messages=messages,
                model="qwen-3-235b-a22b-instruct-2507",
                stream=True,
                max_completion_tokens=1000,
                temperature=0.7,
                top_p=0.8
            )
            
            # Collect response from stream
            response_content = ""
            for chunk in stream:
                if hasattr(chunk, 'choices') and chunk.choices:
                    delta_content = chunk.choices[0].delta.content
                    if delta_content:
                        response_content += delta_content
            
            return {
                "response": response_content.strip(),
                "model": "cerebras-voice",
                "task_type": task_type,
                "voice_enabled": True,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Voice AI processing failed: {str(e)}")
            return {
                "error": f"Voice AI processing failed: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }
    
    def _process_with_agent(self, message, user_context, user_role):
        """Process request using SmartProBono agent"""
        try:
            # Use the existing SmartProBono agent
            response = self.smartprobono_agent.generate_legal_response(
                message=message,
                task_type="chat",
                user_id=user_context.get("user_id") if user_context else None,
                user_role=user_role
            )
            
            return {
                "response": response,
                "model": "smartprobono-agent",
                "task_type": "legal",
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"SmartProBono agent processing failed: {str(e)}")
            return {
                "error": f"SmartProBono agent processing failed: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }
    
    def _process_with_existing_ai(self, message, user_context, task_type):
        """Process request using existing AI service"""
        try:
            # Use the existing AI service
            response = self.existing_ai.generate_legal_response(
                message=message,
                task_type=task_type,
                history=user_context.get("history") if user_context else None
            )
            
            return {
                "response": response,
                "model": "ollama-legal",
                "task_type": task_type,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Existing AI processing failed: {str(e)}")
            return {
                "error": f"Existing AI processing failed: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }
    
    def _load_smartprobono_context(self):
        """Load SmartProBono context for voice AI"""
        try:
            import json
            from pathlib import Path
            
            # Try to load from context directory
            context_dir = Path("context")
            if context_dir.exists():
                all_content = ""
                for file_path in context_dir.glob("*"):
                    if file_path.is_file():
                        try:
                            content = file_path.read_text(encoding='utf-8')
                            all_content += f"\n=== {file_path.name} ===\n{content}\n"
                        except:
                            pass
                return all_content.strip() if all_content else "SmartProBono Legal Platform context not available"
            
            # Fallback to basic context
            return """
SmartProBono is an AI-powered legal assistance platform that connects pro bono lawyers with clients.
Key features include AI-powered case management, document analysis, legal research, and client communication.
Pricing ranges from $199-999/month with Starter, Professional, and Enterprise plans.
The platform increases efficiency by 60% and reduces legal costs by 70%.
"""
            
        except Exception as e:
            logger.warning(f"Could not load SmartProBono context: {e}")
            return "SmartProBono Legal Platform context not available"
    
    def get_available_models(self):
        """Get list of available AI models"""
        models = {
            "ollama": ["llama3.2:3b", "mistral:7b", "qwen2.5:0.5b", "gemma2:2b", "phi3:mini"],
            "smartprobono_agent": ["gemini"],
            "voice_ai": ["cerebras"] if self.voice_enabled else []
        }
        return models
    
    def get_capabilities(self):
        """Get available capabilities"""
        capabilities = {
            "legal_analysis": True,
            "case_management": True,
            "document_processing": True,
            "voice_conversations": self.voice_enabled,
            "multi_agent_transfers": self.voice_enabled,
            "real_time_communication": self.voice_enabled
        }
        return capabilities
