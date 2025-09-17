"""
Voice Processing Service
Handles voice input processing, speech-to-text, and text-to-speech functionality
"""

import os
import io
import base64
import logging
import asyncio
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
import json

# Voice processing imports
try:
    import speech_recognition as sr
    import pyttsx3
    import pydub
    from pydub import AudioSegment
    VOICE_AVAILABLE = True
except ImportError:
    VOICE_AVAILABLE = False
    logging.warning("Voice processing libraries not available. Install with: pip install SpeechRecognition pyttsx3 pydub")

# AI integration
try:
    from legal_ai_backend.agents.voice_agent import VoiceAgent, VoiceCommand
    from legal_ai_backend.agents.advanced_reasoning_agent import analyze_legal_issue
    VOICE_AI_AVAILABLE = True
except ImportError:
    VOICE_AI_AVAILABLE = False
    logging.warning("Voice AI agents not available")

logger = logging.getLogger(__name__)

@dataclass
class VoiceProcessingResult:
    """Result of voice processing operation"""
    success: bool
    text: Optional[str] = None
    audio_data: Optional[bytes] = None
    error: Optional[str] = None
    confidence: float = 0.0
    language: str = "en-US"
    processing_time: float = 0.0

@dataclass
class VoiceSynthesisResult:
    """Result of text-to-speech synthesis"""
    success: bool
    audio_data: Optional[bytes] = None
    error: Optional[str] = None
    duration: float = 0.0
    format: str = "wav"

class VoiceService:
    """Service for handling voice processing operations"""
    
    def __init__(self):
        self.recognizer = None
        self.tts_engine = None
        self.voice_agent = None
        self.supported_languages = {
            'en-US': 'English (US)',
            'en-GB': 'English (UK)',
            'es-ES': 'Spanish',
            'fr-FR': 'French',
            'de-DE': 'German',
            'it-IT': 'Italian',
            'pt-BR': 'Portuguese (Brazil)',
            'ru-RU': 'Russian',
            'ja-JP': 'Japanese',
            'ko-KR': 'Korean',
            'zh-CN': 'Chinese (Simplified)',
            'zh-TW': 'Chinese (Traditional)'
        }
        
        self._initialize_voice_components()
    
    def _initialize_voice_components(self):
        """Initialize voice recognition and synthesis components"""
        if not VOICE_AVAILABLE:
            logger.warning("Voice processing not available - install required libraries")
            return
        
        try:
            # Initialize speech recognition
            self.recognizer = sr.Recognizer()
            self.recognizer.energy_threshold = 300
            self.recognizer.dynamic_energy_threshold = True
            self.recognizer.pause_threshold = 0.8
            self.recognizer.phrase_threshold = 0.3
            self.recognizer.non_speaking_duration = 0.8
            
            # Initialize text-to-speech
            self.tts_engine = pyttsx3.init()
            self._configure_tts_engine()
            
            # Initialize voice AI agent
            if VOICE_AI_AVAILABLE:
                self.voice_agent = VoiceAgent()
            
            logger.info("Voice service initialized successfully")
            
        except Exception as e:
            logger.error(f"Error initializing voice service: {e}")
            self.recognizer = None
            self.tts_engine = None
    
    def _configure_tts_engine(self):
        """Configure text-to-speech engine settings"""
        if not self.tts_engine:
            return
        
        try:
            # Get available voices
            voices = self.tts_engine.getProperty('voices')
            if voices:
                # Try to find a good quality voice
                for voice in voices:
                    if 'english' in voice.name.lower() or 'us' in voice.id.lower():
                        self.tts_engine.setProperty('voice', voice.id)
                        break
            
            # Set default properties
            self.tts_engine.setProperty('rate', 150)  # Speed
            self.tts_engine.setProperty('volume', 0.8)  # Volume
            
        except Exception as e:
            logger.warning(f"Error configuring TTS engine: {e}")
    
    def is_available(self) -> bool:
        """Check if voice processing is available"""
        return VOICE_AVAILABLE and self.recognizer is not None and self.tts_engine is not None
    
    def get_supported_languages(self) -> Dict[str, str]:
        """Get list of supported languages"""
        return self.supported_languages
    
    def process_audio_file(self, audio_data: bytes, language: str = "en-US") -> VoiceProcessingResult:
        """Process audio file and convert to text"""
        start_time = datetime.now()
        
        if not self.is_available():
            return VoiceProcessingResult(
                success=False,
                error="Voice processing not available"
            )
        
        try:
            # Convert bytes to audio segment
            audio_segment = AudioSegment.from_file(io.BytesIO(audio_data))
            
            # Convert to WAV format if needed
            if audio_segment.frame_rate != 16000:
                audio_segment = audio_segment.set_frame_rate(16000)
            
            if audio_segment.channels > 1:
                audio_segment = audio_segment.set_channels(1)
            
            # Convert to AudioData for speech recognition
            wav_data = audio_segment.raw_data
            audio_data_sr = sr.AudioData(wav_data, 16000, 2)
            
            # Perform speech recognition
            with sr.Microphone() as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            
            result = self.recognizer.recognize_google(
                audio_data_sr,
                language=language,
                show_all=True
            )
            
            processing_time = (datetime.now() - start_time).total_seconds()
            
            if isinstance(result, dict) and 'alternative' in result:
                # Get the best result
                alternatives = result['alternative']
                if alternatives:
                    best_result = alternatives[0]
                    text = best_result.get('transcript', '')
                    confidence = best_result.get('confidence', 0.0)
                    
                    return VoiceProcessingResult(
                        success=True,
                        text=text,
                        confidence=confidence,
                        language=language,
                        processing_time=processing_time
                    )
            
            return VoiceProcessingResult(
                success=False,
                error="No speech detected",
                processing_time=processing_time
            )
            
        except sr.UnknownValueError:
            return VoiceProcessingResult(
                success=False,
                error="Could not understand audio",
                processing_time=(datetime.now() - start_time).total_seconds()
            )
        except sr.RequestError as e:
            return VoiceProcessingResult(
                success=False,
                error=f"Speech recognition service error: {e}",
                processing_time=(datetime.now() - start_time).total_seconds()
            )
        except Exception as e:
            logger.error(f"Error processing audio: {e}")
            return VoiceProcessingResult(
                success=False,
                error=f"Processing error: {str(e)}",
                processing_time=(datetime.now() - start_time).total_seconds()
            )
    
    def synthesize_speech(self, text: str, language: str = "en-US", 
                         voice: str = "default", speed: float = 1.0, 
                         pitch: float = 1.0, volume: float = 0.8) -> VoiceSynthesisResult:
        """Convert text to speech audio"""
        start_time = datetime.now()
        
        if not self.is_available():
            return VoiceSynthesisResult(
                success=False,
                error="Voice synthesis not available"
            )
        
        try:
            # Configure TTS engine
            self.tts_engine.setProperty('rate', int(150 * speed))
            self.tts_engine.setProperty('volume', volume)
            
            # Set voice if specified
            if voice != "default":
                voices = self.tts_engine.getProperty('voices')
                for v in voices:
                    if voice.lower() in v.name.lower() or voice in v.id:
                        self.tts_engine.setProperty('voice', v.id)
                        break
            
            # Generate audio
            audio_buffer = io.BytesIO()
            self.tts_engine.save_to_file(text, audio_buffer)
            self.tts_engine.runAndWait()
            
            # Get audio data
            audio_buffer.seek(0)
            audio_data = audio_buffer.read()
            
            processing_time = (datetime.now() - start_time).total_seconds()
            
            return VoiceSynthesisResult(
                success=True,
                audio_data=audio_data,
                duration=processing_time,
                format="wav"
            )
            
        except Exception as e:
            logger.error(f"Error synthesizing speech: {e}")
            return VoiceSynthesisResult(
                success=False,
                error=f"Synthesis error: {str(e)}",
                duration=(datetime.now() - start_time).total_seconds()
            )
    
    def process_voice_command(self, text: str, user_id: str = None) -> Dict:
        """Process voice command using AI agent"""
        if not VOICE_AI_AVAILABLE or not self.voice_agent:
            return {
                "success": False,
                "error": "Voice AI agent not available"
            }
        
        try:
            # Parse voice command
            command = self.voice_agent._parse_voice_command(text)
            
            if not command:
                return {
                    "success": False,
                    "error": "Could not parse voice command"
                }
            
            # Validate command
            if not self.voice_agent.validate_voice_command(command):
                return {
                    "success": False,
                    "error": "Invalid voice command"
                }
            
            # Process command based on type
            result = {
                "success": True,
                "command_type": command.command_type,
                "intent": command.intent,
                "entities": command.entities,
                "confidence": command.confidence
            }
            
            # Add specific processing based on command type
            if command.command_type == "legal_question":
                result["response"] = "I understand you have a legal question. Let me help you with that."
            elif command.command_type == "case_search":
                result["response"] = "I'll help you search for relevant cases."
            elif command.command_type == "document_request":
                result["response"] = "I'll help you with document requests."
            elif command.command_type == "appointment":
                result["response"] = "I'll help you schedule an appointment."
            else:
                result["response"] = "I understand your request. How can I assist you?"
            
            return result
            
        except Exception as e:
            logger.error(f"Error processing voice command: {e}")
            return {
                "success": False,
                "error": f"Command processing error: {str(e)}"
            }
    
    def get_voice_analysis(self, text: str, context: Dict = None) -> Dict:
        """Get AI analysis of voice input"""
        try:
            # Use advanced reasoning agent for legal analysis
            if VOICE_AI_AVAILABLE:
                analysis_result = analyze_legal_issue(
                    issue_description=text,
                    jurisdiction="ri",
                    context=context or {}
                )
                
                return {
                    "success": True,
                    "analysis": analysis_result,
                    "text": text,
                    "timestamp": datetime.now().isoformat()
                }
            else:
                return {
                    "success": False,
                    "error": "AI analysis not available"
                }
                
        except Exception as e:
            logger.error(f"Error in voice analysis: {e}")
            return {
                "success": False,
                "error": f"Analysis error: {str(e)}"
            }
    
    def get_available_voices(self, language: str = "en-US") -> List[Dict]:
        """Get available voices for a language"""
        if not self.is_available():
            return []
        
        try:
            voices = self.tts_engine.getProperty('voices')
            available_voices = []
            
            for voice in voices:
                if language.lower() in voice.id.lower() or language.split('-')[0].lower() in voice.id.lower():
                    available_voices.append({
                        "id": voice.id,
                        "name": voice.name,
                        "language": voice.id,
                        "gender": getattr(voice, 'gender', 'unknown'),
                        "age": getattr(voice, 'age', 'unknown')
                    })
            
            return available_voices
            
        except Exception as e:
            logger.error(f"Error getting available voices: {e}")
            return []
    
    def get_voice_statistics(self) -> Dict:
        """Get voice processing statistics"""
        return {
            "voice_available": self.is_available(),
            "supported_languages": len(self.supported_languages),
            "languages": list(self.supported_languages.keys()),
            "voice_ai_available": VOICE_AI_AVAILABLE,
            "tts_engine_available": self.tts_engine is not None,
            "recognition_available": self.recognizer is not None
        }

# Global voice service instance
voice_service = VoiceService()
