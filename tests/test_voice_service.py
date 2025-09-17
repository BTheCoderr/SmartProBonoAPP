"""
Voice Service Tests
Tests for voice processing functionality
"""

import pytest
import io
import base64
from unittest.mock import Mock, patch, MagicMock
import sys
import os

# Add the backend directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from services.voice_service import VoiceService, VoiceProcessingResult, VoiceSynthesisResult

class TestVoiceService:
    """Test Voice Service functionality"""
    
    @pytest.fixture
    def voice_service(self):
        """Create a voice service instance for testing"""
        with patch('services.voice_service.VOICE_AVAILABLE', True):
            with patch('services.voice_service.VOICE_AI_AVAILABLE', True):
                service = VoiceService()
                service.recognizer = Mock()
                service.tts_engine = Mock()
                service.voice_agent = Mock()
                return service
    
    def test_voice_service_initialization(self, voice_service):
        """Test voice service initialization"""
        assert voice_service.recognizer is not None
        assert voice_service.tts_engine is not None
        assert voice_service.voice_agent is not None
    
    def test_is_available(self, voice_service):
        """Test voice service availability check"""
        assert voice_service.is_available() == True
        
        voice_service.recognizer = None
        assert voice_service.is_available() == False
    
    def test_get_supported_languages(self, voice_service):
        """Test getting supported languages"""
        languages = voice_service.get_supported_languages()
        assert isinstance(languages, dict)
        assert 'en-US' in languages
        assert 'es-ES' in languages
        assert len(languages) > 0
    
    @patch('services.voice_service.AudioSegment')
    @patch('services.voice_service.sr.AudioData')
    def test_process_audio_file_success(self, mock_audio_data, mock_audio_segment, voice_service):
        """Test successful audio processing"""
        # Mock audio data
        mock_audio_bytes = b'fake_audio_data'
        mock_segment = Mock()
        mock_segment.frame_rate = 16000
        mock_segment.channels = 1
        mock_segment.raw_data = b'fake_raw_data'
        mock_audio_segment.from_file.return_value = mock_segment
        
        # Mock recognition result
        mock_result = {
            'alternative': [
                {'transcript': 'Hello world', 'confidence': 0.95}
            ]
        }
        voice_service.recognizer.recognize_google.return_value = mock_result
        
        # Test processing
        result = voice_service.process_audio_file(mock_audio_bytes, 'en-US')
        
        assert result.success == True
        assert result.text == 'Hello world'
        assert result.confidence == 0.95
        assert result.language == 'en-US'
        assert result.processing_time > 0
    
    def test_process_audio_file_unavailable_service(self):
        """Test audio processing when service is unavailable"""
        with patch('services.voice_service.VOICE_AVAILABLE', False):
            service = VoiceService()
            result = service.process_audio_file(b'fake_audio', 'en-US')
            
            assert result.success == False
            assert result.error == "Voice processing not available"
    
    @patch('services.voice_service.AudioSegment')
    def test_process_audio_file_recognition_error(self, mock_audio_segment, voice_service):
        """Test audio processing with recognition error"""
        # Mock audio data
        mock_audio_bytes = b'fake_audio_data'
        mock_segment = Mock()
        mock_segment.frame_rate = 16000
        mock_segment.channels = 1
        mock_segment.raw_data = b'fake_raw_data'
        mock_audio_segment.from_file.return_value = mock_segment
        
        # Mock recognition error
        voice_service.recognizer.recognize_google.side_effect = Exception('Recognition failed')
        
        result = voice_service.process_audio_file(mock_audio_bytes, 'en-US')
        
        assert result.success == False
        assert 'error' in result.error
    
    @patch('services.voice_service.pyttsx3.init')
    def test_synthesize_speech_success(self, mock_tts_init, voice_service):
        """Test successful speech synthesis"""
        # Mock TTS engine
        mock_engine = Mock()
        mock_engine.save_to_file = Mock()
        mock_engine.runAndWait = Mock()
        mock_tts_init.return_value = mock_engine
        voice_service.tts_engine = mock_engine
        
        # Mock audio buffer
        with patch('io.BytesIO') as mock_bytes_io:
            mock_buffer = Mock()
            mock_buffer.read.return_value = b'fake_audio_data'
            mock_bytes_io.return_value = mock_buffer
            
            result = voice_service.synthesize_speech('Hello world', 'en-US')
            
            assert result.success == True
            assert result.audio_data == b'fake_audio_data'
            assert result.format == 'wav'
            assert result.duration > 0
    
    def test_synthesize_speech_unavailable_service(self):
        """Test speech synthesis when service is unavailable"""
        with patch('services.voice_service.VOICE_AVAILABLE', False):
            service = VoiceService()
            result = service.synthesize_speech('Hello world')
            
            assert result.success == False
            assert result.error == "Voice synthesis not available"
    
    def test_process_voice_command_success(self, voice_service):
        """Test successful voice command processing"""
        # Mock voice agent
        mock_command = Mock()
        mock_command.command_type = "legal_question"
        mock_command.intent = "get_legal_advice"
        mock_command.entities = {"topic": "immigration"}
        mock_command.confidence = 0.9
        
        voice_service.voice_agent._parse_voice_command.return_value = mock_command
        voice_service.voice_agent.validate_voice_command.return_value = True
        
        result = voice_service.process_voice_command("I need help with immigration", "user123")
        
        assert result['success'] == True
        assert result['command_type'] == "legal_question"
        assert result['intent'] == "get_legal_advice"
        assert result['entities'] == {"topic": "immigration"}
        assert result['confidence'] == 0.9
    
    def test_process_voice_command_no_agent(self):
        """Test voice command processing without AI agent"""
        with patch('services.voice_service.VOICE_AI_AVAILABLE', False):
            service = VoiceService()
            service.voice_agent = None
            
            result = service.process_voice_command("test command", "user123")
            
            assert result['success'] == False
            assert result['error'] == "Voice AI agent not available"
    
    def test_process_voice_command_invalid_command(self, voice_service):
        """Test voice command processing with invalid command"""
        voice_service.voice_agent._parse_voice_command.return_value = None
        
        result = voice_service.process_voice_command("invalid command", "user123")
        
        assert result['success'] == False
        assert result['error'] == "Could not parse voice command"
    
    def test_get_voice_analysis_success(self, voice_service):
        """Test successful voice analysis"""
        # Mock analysis result
        mock_analysis = {
            'case_summary': 'Test case summary',
            'key_facts': ['Fact 1', 'Fact 2'],
            'practical_advice': ['Advice 1', 'Advice 2']
        }
        
        with patch('services.voice_service.analyze_legal_issue') as mock_analyze:
            mock_analyze.return_value = mock_analysis
            
            result = voice_service.get_voice_analysis("I need legal help", {"user_type": "client"})
            
            assert result['success'] == True
            assert result['analysis'] == mock_analysis
            assert result['text'] == "I need legal help"
            assert 'timestamp' in result
    
    def test_get_voice_analysis_no_ai(self):
        """Test voice analysis without AI support"""
        with patch('services.voice_service.VOICE_AI_AVAILABLE', False):
            service = VoiceService()
            
            result = service.get_voice_analysis("test text")
            
            assert result['success'] == False
            assert result['error'] == "AI analysis not available"
    
    def test_get_available_voices(self, voice_service):
        """Test getting available voices"""
        # Mock voices
        mock_voices = [
            Mock(id='voice1', name='English Voice', gender='female'),
            Mock(id='voice2', name='Spanish Voice', gender='male')
        ]
        voice_service.tts_engine.getProperty.return_value = mock_voices
        
        voices = voice_service.get_available_voices('en-US')
        
        assert len(voices) == 2
        assert voices[0]['id'] == 'voice1'
        assert voices[0]['name'] == 'English Voice'
    
    def test_get_voice_statistics(self, voice_service):
        """Test getting voice statistics"""
        stats = voice_service.get_voice_statistics()
        
        assert stats['voice_available'] == True
        assert stats['supported_languages'] > 0
        assert 'languages' in stats
        assert stats['voice_ai_available'] == True
        assert stats['tts_engine_available'] == True
        assert stats['recognition_available'] == True

class TestVoiceProcessingResult:
    """Test VoiceProcessingResult dataclass"""
    
    def test_voice_processing_result_creation(self):
        """Test creating a voice processing result"""
        result = VoiceProcessingResult(
            success=True,
            text="Hello world",
            confidence=0.95,
            language="en-US",
            processing_time=1.5
        )
        
        assert result.success == True
        assert result.text == "Hello world"
        assert result.confidence == 0.95
        assert result.language == "en-US"
        assert result.processing_time == 1.5
        assert result.error is None
        assert result.audio_data is None
    
    def test_voice_processing_result_failure(self):
        """Test creating a failed voice processing result"""
        result = VoiceProcessingResult(
            success=False,
            error="Recognition failed",
            processing_time=2.0
        )
        
        assert result.success == False
        assert result.error == "Recognition failed"
        assert result.processing_time == 2.0
        assert result.text is None
        assert result.confidence == 0.0

class TestVoiceSynthesisResult:
    """Test VoiceSynthesisResult dataclass"""
    
    def test_voice_synthesis_result_creation(self):
        """Test creating a voice synthesis result"""
        result = VoiceSynthesisResult(
            success=True,
            audio_data=b'fake_audio_data',
            duration=3.5,
            format="wav"
        )
        
        assert result.success == True
        assert result.audio_data == b'fake_audio_data'
        assert result.duration == 3.5
        assert result.format == "wav"
        assert result.error is None
    
    def test_voice_synthesis_result_failure(self):
        """Test creating a failed voice synthesis result"""
        result = VoiceSynthesisResult(
            success=False,
            error="Synthesis failed",
            duration=1.0
        )
        
        assert result.success == False
        assert result.error == "Synthesis failed"
        assert result.duration == 1.0
        assert result.audio_data is None

class TestVoiceServiceIntegration:
    """Integration tests for voice service"""
    
    @pytest.fixture
    def mock_voice_service(self):
        """Create a mocked voice service for integration tests"""
        with patch('services.voice_service.VOICE_AVAILABLE', True):
            with patch('services.voice_service.VOICE_AI_AVAILABLE', True):
                service = VoiceService()
                
                # Mock all dependencies
                service.recognizer = Mock()
                service.tts_engine = Mock()
                service.voice_agent = Mock()
                
                return service
    
    def test_complete_voice_workflow(self, mock_voice_service):
        """Test complete voice processing workflow"""
        # 1. Process audio input
        mock_audio_data = b'fake_audio_data'
        mock_result = {
            'alternative': [
                {'transcript': 'What are my legal options?', 'confidence': 0.9}
            ]
        }
        mock_voice_service.recognizer.recognize_google.return_value = mock_result
        
        with patch('services.voice_service.AudioSegment'):
            processing_result = mock_voice_service.process_audio_file(mock_audio_data, 'en-US')
            assert processing_result.success == True
            assert processing_result.text == 'What are my legal options?'
        
        # 2. Process voice command
        mock_command = Mock()
        mock_command.command_type = "legal_question"
        mock_command.intent = "get_legal_advice"
        mock_command.entities = {"topic": "legal_options"}
        mock_command.confidence = 0.9
        
        mock_voice_service.voice_agent._parse_voice_command.return_value = mock_command
        mock_voice_service.voice_agent.validate_voice_command.return_value = True
        
        command_result = mock_voice_service.process_voice_command("What are my legal options?", "user123")
        assert command_result['success'] == True
        assert command_result['command_type'] == "legal_question"
        
        # 3. Analyze with AI
        mock_analysis = {
            'case_summary': 'User seeking legal options',
            'key_facts': ['User has legal questions'],
            'practical_advice': ['Consult with attorney', 'Research relevant laws']
        }
        
        with patch('services.voice_service.analyze_legal_issue') as mock_analyze:
            mock_analyze.return_value = mock_analysis
            
            analysis_result = mock_voice_service.get_voice_analysis("What are my legal options?")
            assert analysis_result['success'] == True
            assert analysis_result['analysis'] == mock_analysis
        
        # 4. Synthesize response
        mock_voice_service.tts_engine.save_to_file = Mock()
        mock_voice_service.tts_engine.runAndWait = Mock()
        
        with patch('io.BytesIO') as mock_bytes_io:
            mock_buffer = Mock()
            mock_buffer.read.return_value = b'synthesized_audio'
            mock_bytes_io.return_value = mock_buffer
            
            synthesis_result = mock_voice_service.synthesize_speech("Here are your legal options...")
            assert synthesis_result.success == True
            assert synthesis_result.audio_data == b'synthesized_audio'
    
    def test_error_handling_workflow(self, mock_voice_service):
        """Test error handling in voice workflow"""
        # Test recognition error
        mock_voice_service.recognizer.recognize_google.side_effect = Exception('Recognition failed')
        
        with patch('services.voice_service.AudioSegment'):
            result = mock_voice_service.process_audio_file(b'fake_audio', 'en-US')
            assert result.success == False
            assert 'error' in result.error
        
        # Test command processing error
        mock_voice_service.voice_agent._parse_voice_command.side_effect = Exception('Command parsing failed')
        
        result = mock_voice_service.process_voice_command("test", "user")
        assert result['success'] == False
        assert 'error' in result['error']
        
        # Test synthesis error
        mock_voice_service.tts_engine.save_to_file.side_effect = Exception('Synthesis failed')
        
        result = mock_voice_service.synthesize_speech("test")
        assert result.success == False
        assert 'error' in result.error

if __name__ == '__main__':
    pytest.main([__file__, '-v'])
