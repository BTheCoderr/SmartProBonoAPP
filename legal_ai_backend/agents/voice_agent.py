"""
Voice Interface Agent
Handles speech-to-text, text-to-speech, and voice-based interactions
"""

import logging
import asyncio
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
import json
import base64
import io

logger = logging.getLogger(__name__)

@dataclass
class VoiceCommand:
    """Represents a voice command"""
    command_type: str  # 'question', 'request', 'command'
    text: str
    confidence: float
    intent: str
    entities: Dict[str, Any]

@dataclass
class VoiceResponse:
    """Represents a voice response"""
    text: str
    audio_data: Optional[bytes] = None
    should_speak: bool = True
    response_type: str = "answer"  # 'answer', 'question', 'confirmation'

class VoiceAgent:
    """Agent for handling voice interactions"""
    
    def __init__(self):
        self.supported_languages = ["en-US", "en-GB", "es-US"]
        self.voice_commands = self._initialize_voice_commands()
        self.speech_config = self._initialize_speech_config()
        
    def _initialize_voice_commands(self) -> Dict[str, Dict[str, Any]]:
        """Initialize supported voice commands"""
        return {
            "legal_question": {
                "patterns": [
                    "what should I do if",
                    "is it legal to",
                    "can I sue for",
                    "what are my rights",
                    "help me with my case"
                ],
                "intent": "legal_advice",
                "confidence_threshold": 0.7
            },
            "case_search": {
                "patterns": [
                    "find cases about",
                    "search for cases",
                    "show me similar cases",
                    "what cases are relevant"
                ],
                "intent": "case_search",
                "confidence_threshold": 0.8
            },
            "document_help": {
                "patterns": [
                    "help me fill out",
                    "generate a document",
                    "create a form",
                    "what documents do I need"
                ],
                "intent": "document_assistance",
                "confidence_threshold": 0.7
            },
            "status_check": {
                "patterns": [
                    "check my case status",
                    "what's the status",
                    "any updates on my case",
                    "how is my case going"
                ],
                "intent": "status_inquiry",
                "confidence_threshold": 0.8
            },
            "general_help": {
                "patterns": [
                    "help",
                    "what can you do",
                    "how does this work",
                    "explain the process"
                ],
                "intent": "general_help",
                "confidence_threshold": 0.6
            }
        }
    
    def _initialize_speech_config(self) -> Dict[str, Any]:
        """Initialize speech synthesis configuration"""
        return {
            "voice_settings": {
                "en-US": {
                    "voice_name": "en-US-AriaNeural",
                    "rate": "medium",
                    "pitch": "medium",
                    "volume": "medium"
                },
                "en-GB": {
                    "voice_name": "en-GB-SoniaNeural",
                    "rate": "medium",
                    "pitch": "medium",
                    "volume": "medium"
                },
                "es-US": {
                    "voice_name": "es-US-PalomaNeural",
                    "rate": "medium",
                    "pitch": "medium",
                    "volume": "medium"
                }
            },
            "response_templates": {
                "legal_advice": "I understand you're asking about {topic}. Let me analyze this for you.",
                "case_search": "I'll search for cases related to {query}.",
                "document_assistance": "I can help you with {document_type}. Let me guide you through this.",
                "status_inquiry": "Let me check the status of your case.",
                "general_help": "I'm here to help with legal questions, case research, and document assistance."
            }
        }
    
    async def process_voice_input(self, audio_data: bytes, language: str = "en-US") -> VoiceCommand:
        """Process voice input and return structured command"""
        try:
            # In a real implementation, this would use speech-to-text service
            # For now, we'll simulate the process
            text = await self._speech_to_text(audio_data, language)
            
            # Parse the command
            command = self._parse_voice_command(text)
            
            logger.info(f"Processed voice input: {command.text}")
            return command
            
        except Exception as e:
            logger.error(f"Error processing voice input: {e}")
            return VoiceCommand(
                command_type="error",
                text="I'm sorry, I couldn't understand that. Please try again.",
                confidence=0.0,
                intent="error",
                entities={}
            )
    
    async def _speech_to_text(self, audio_data: bytes, language: str) -> str:
        """Convert speech to text (simulated)"""
        # In production, integrate with Azure Speech Services, Google Speech-to-Text, or similar
        # For now, return a placeholder
        return "I need help with my legal case"
    
    def _parse_voice_command(self, text: str) -> VoiceCommand:
        """Parse voice command and extract intent"""
        text_lower = text.lower()
        
        # Find best matching command
        best_match = None
        best_confidence = 0.0
        
        for command_type, config in self.voice_commands.items():
            for pattern in config["patterns"]:
                if pattern in text_lower:
                    confidence = self._calculate_confidence(text_lower, pattern)
                    if confidence > best_confidence and confidence >= config["confidence_threshold"]:
                        best_confidence = confidence
                        best_match = {
                            "type": command_type,
                            "intent": config["intent"],
                            "confidence": confidence
                        }
        
        if best_match:
            return VoiceCommand(
                command_type=best_match["type"],
                text=text,
                confidence=best_match["confidence"],
                intent=best_match["intent"],
                entities=self._extract_entities(text)
            )
        else:
            return VoiceCommand(
                command_type="unknown",
                text=text,
                confidence=0.0,
                intent="unknown",
                entities={}
            )
    
    def _calculate_confidence(self, text: str, pattern: str) -> float:
        """Calculate confidence score for pattern matching"""
        # Simple word overlap calculation
        text_words = set(text.split())
        pattern_words = set(pattern.split())
        
        if not pattern_words:
            return 0.0
        
        overlap = len(text_words.intersection(pattern_words))
        return overlap / len(pattern_words)
    
    def _extract_entities(self, text: str) -> Dict[str, Any]:
        """Extract entities from voice command"""
        entities = {}
        
        # Simple entity extraction - in production, use NLP libraries
        if "case" in text.lower():
            entities["case_mentioned"] = True
        
        if "document" in text.lower() or "form" in text.lower():
            entities["document_mentioned"] = True
        
        if "urgent" in text.lower() or "emergency" in text.lower():
            entities["urgency"] = "high"
        
        return entities
    
    async def generate_voice_response(self, response_text: str, language: str = "en-US") -> VoiceResponse:
        """Generate voice response from text"""
        try:
            # In production, use text-to-speech service
            audio_data = await self._text_to_speech(response_text, language)
            
            return VoiceResponse(
                text=response_text,
                audio_data=audio_data,
                should_speak=True,
                response_type="answer"
            )
            
        except Exception as e:
            logger.error(f"Error generating voice response: {e}")
            return VoiceResponse(
                text=response_text,
                audio_data=None,
                should_speak=False,
                response_type="answer"
            )
    
    async def _text_to_speech(self, text: str, language: str) -> bytes:
        """Convert text to speech (simulated)"""
        # In production, integrate with Azure Speech Services, Google Text-to-Speech, or similar
        # For now, return empty bytes
        return b""
    
    def format_response_for_voice(self, analysis_result: Dict[str, Any]) -> str:
        """Format analysis result for voice output"""
        try:
            # Extract key information
            summary = analysis_result.get("analysis", {}).get("case_summary", "")
            key_facts = analysis_result.get("analysis", {}).get("key_facts", [])
            recommendations = analysis_result.get("recommendations", [])
            
            # Format for voice
            voice_text = "Here's what I found: "
            
            if summary:
                voice_text += f"{summary} "
            
            if key_facts:
                voice_text += "Key points to consider: "
                for i, fact in enumerate(key_facts[:3], 1):  # Limit to 3 facts
                    voice_text += f"{i}. {fact} "
            
            if recommendations:
                voice_text += "My recommendations: "
                for i, rec in enumerate(recommendations[:2], 1):  # Limit to 2 recommendations
                    voice_text += f"{i}. {rec} "
            
            # Add disclaimer
            voice_text += "Please remember, this is not legal advice. Consult with a qualified attorney for your specific situation."
            
            return voice_text
            
        except Exception as e:
            logger.error(f"Error formatting response for voice: {e}")
            return "I apologize, but I'm having trouble processing that information. Please try again or consult with a qualified attorney."
    
    def get_voice_help(self) -> str:
        """Get help text for voice commands"""
        help_text = "I can help you with: "
        help_text += "Legal questions and advice, "
        help_text += "Searching for relevant cases, "
        help_text += "Document assistance and form generation, "
        help_text += "Checking case status, "
        help_text += "And general legal guidance. "
        help_text += "Just speak naturally and I'll do my best to help you."
        
        return help_text
    
    def validate_voice_command(self, command: VoiceCommand) -> bool:
        """Validate if voice command is properly formed"""
        return (
            command.confidence > 0.5 and
            command.intent != "unknown" and
            len(command.text.strip()) > 0
        )

# Global instance
voice_agent = VoiceAgent()

async def process_voice_input(audio_data: bytes, language: str = "en-US") -> VoiceCommand:
    """Process voice input"""
    return await voice_agent.process_voice_input(audio_data, language)

async def generate_voice_response(response_text: str, language: str = "en-US") -> VoiceResponse:
    """Generate voice response"""
    return await voice_agent.generate_voice_response(response_text, language)

def format_response_for_voice(analysis_result: Dict[str, Any]) -> str:
    """Format analysis result for voice output"""
    return voice_agent.format_response_for_voice(analysis_result)
