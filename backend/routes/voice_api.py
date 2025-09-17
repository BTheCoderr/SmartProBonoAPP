"""
Voice Processing API Routes
Handles voice input/output, speech-to-text, and text-to-speech functionality
"""

from flask import Blueprint, request, jsonify, send_file
from werkzeug.utils import secure_filename
import base64
import io
import logging
from datetime import datetime
from services.voice_service import voice_service

logger = logging.getLogger(__name__)

# Create blueprint
voice_bp = Blueprint('voice_api', __name__, url_prefix='/api/voice')

@voice_bp.route('/status', methods=['GET'])
def get_voice_status():
    """Get voice processing service status"""
    try:
        stats = voice_service.get_voice_statistics()
        return jsonify({
            "success": True,
            "status": "available" if voice_service.is_available() else "unavailable",
            "statistics": stats,
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        logger.error(f"Error getting voice status: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@voice_bp.route('/languages', methods=['GET'])
def get_supported_languages():
    """Get supported languages for voice processing"""
    try:
        languages = voice_service.get_supported_languages()
        return jsonify({
            "success": True,
            "languages": languages,
            "count": len(languages)
        })
    except Exception as e:
        logger.error(f"Error getting supported languages: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@voice_bp.route('/voices', methods=['GET'])
def get_available_voices():
    """Get available voices for text-to-speech"""
    try:
        language = request.args.get('language', 'en-US')
        voices = voice_service.get_available_voices(language)
        
        return jsonify({
            "success": True,
            "voices": voices,
            "language": language,
            "count": len(voices)
        })
    except Exception as e:
        logger.error(f"Error getting available voices: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@voice_bp.route('/speech-to-text', methods=['POST'])
def speech_to_text():
    """Convert speech audio to text"""
    try:
        # Check if voice service is available
        if not voice_service.is_available():
            return jsonify({
                "success": False,
                "error": "Voice processing not available"
            }), 503
        
        # Get request data
        data = request.get_json()
        if not data:
            return jsonify({
                "success": False,
                "error": "No data provided"
            }), 400
        
        # Get audio data
        audio_data_b64 = data.get('audio_data')
        if not audio_data_b64:
            return jsonify({
                "success": False,
                "error": "No audio data provided"
            }), 400
        
        # Decode base64 audio data
        try:
            audio_data = base64.b64decode(audio_data_b64)
        except Exception as e:
            return jsonify({
                "success": False,
                "error": f"Invalid audio data format: {str(e)}"
            }), 400
        
        # Get language parameter
        language = data.get('language', 'en-US')
        
        # Process audio
        result = voice_service.process_audio_file(audio_data, language)
        
        if result.success:
            return jsonify({
                "success": True,
                "text": result.text,
                "confidence": result.confidence,
                "language": result.language,
                "processing_time": result.processing_time
            })
        else:
            return jsonify({
                "success": False,
                "error": result.error,
                "processing_time": result.processing_time
            }), 400
            
    except Exception as e:
        logger.error(f"Error in speech-to-text: {e}")
        return jsonify({
            "success": False,
            "error": f"Internal server error: {str(e)}"
        }), 500

@voice_bp.route('/text-to-speech', methods=['POST'])
def text_to_speech():
    """Convert text to speech audio"""
    try:
        # Check if voice service is available
        if not voice_service.is_available():
            return jsonify({
                "success": False,
                "error": "Voice processing not available"
            }), 503
        
        # Get request data
        data = request.get_json()
        if not data:
            return jsonify({
                "success": False,
                "error": "No data provided"
            }), 400
        
        # Get text
        text = data.get('text')
        if not text:
            return jsonify({
                "success": False,
                "error": "No text provided"
            }), 400
        
        # Get voice parameters
        language = data.get('language', 'en-US')
        voice = data.get('voice', 'default')
        speed = float(data.get('speed', 1.0))
        pitch = float(data.get('pitch', 1.0))
        volume = float(data.get('volume', 0.8))
        
        # Synthesize speech
        result = voice_service.synthesize_speech(
            text=text,
            language=language,
            voice=voice,
            speed=speed,
            pitch=pitch,
            volume=volume
        )
        
        if result.success:
            # Encode audio data as base64
            audio_b64 = base64.b64encode(result.audio_data).decode('utf-8')
            
            return jsonify({
                "success": True,
                "audio_data": audio_b64,
                "format": result.format,
                "duration": result.duration,
                "language": language,
                "voice": voice
            })
        else:
            return jsonify({
                "success": False,
                "error": result.error,
                "duration": result.duration
            }), 400
            
    except Exception as e:
        logger.error(f"Error in text-to-speech: {e}")
        return jsonify({
            "success": False,
            "error": f"Internal server error: {str(e)}"
        }), 500

@voice_bp.route('/command', methods=['POST'])
def process_voice_command():
    """Process voice command using AI agent"""
    try:
        # Get request data
        data = request.get_json()
        if not data:
            return jsonify({
                "success": False,
                "error": "No data provided"
            }), 400
        
        # Get text and user ID
        text = data.get('text')
        user_id = data.get('user_id')
        
        if not text:
            return jsonify({
                "success": False,
                "error": "No text provided"
            }), 400
        
        # Process voice command
        result = voice_service.process_voice_command(text, user_id)
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error processing voice command: {e}")
        return jsonify({
            "success": False,
            "error": f"Internal server error: {str(e)}"
        }), 500

@voice_bp.route('/analyze', methods=['POST'])
def analyze_voice_input():
    """Analyze voice input using AI"""
    try:
        # Get request data
        data = request.get_json()
        if not data:
            return jsonify({
                "success": False,
                "error": "No data provided"
            }), 400
        
        # Get text and context
        text = data.get('text')
        context = data.get('context', {})
        
        if not text:
            return jsonify({
                "success": False,
                "error": "No text provided"
            }), 400
        
        # Analyze voice input
        result = voice_service.get_voice_analysis(text, context)
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error analyzing voice input: {e}")
        return jsonify({
            "success": False,
            "error": f"Internal server error: {str(e)}"
        }), 500

@voice_bp.route('/upload-audio', methods=['POST'])
def upload_audio_file():
    """Upload and process audio file"""
    try:
        # Check if voice service is available
        if not voice_service.is_available():
            return jsonify({
                "success": False,
                "error": "Voice processing not available"
            }), 503
        
        # Check if file is present
        if 'audio' not in request.files:
            return jsonify({
                "success": False,
                "error": "No audio file provided"
            }), 400
        
        file = request.files['audio']
        if file.filename == '':
            return jsonify({
                "success": False,
                "error": "No file selected"
            }), 400
        
        # Get language parameter
        language = request.form.get('language', 'en-US')
        
        # Read file data
        audio_data = file.read()
        
        # Process audio
        result = voice_service.process_audio_file(audio_data, language)
        
        if result.success:
            return jsonify({
                "success": True,
                "text": result.text,
                "confidence": result.confidence,
                "language": result.language,
                "processing_time": result.processing_time,
                "filename": secure_filename(file.filename)
            })
        else:
            return jsonify({
                "success": False,
                "error": result.error,
                "processing_time": result.processing_time
            }), 400
            
    except Exception as e:
        logger.error(f"Error uploading audio file: {e}")
        return jsonify({
            "success": False,
            "error": f"Internal server error: {str(e)}"
        }), 500

@voice_bp.route('/download-audio', methods=['POST'])
def download_audio():
    """Generate and download audio file from text"""
    try:
        # Check if voice service is available
        if not voice_service.is_available():
            return jsonify({
                "success": False,
                "error": "Voice processing not available"
            }), 503
        
        # Get request data
        data = request.get_json()
        if not data:
            return jsonify({
                "success": False,
                "error": "No data provided"
            }), 400
        
        # Get text and parameters
        text = data.get('text')
        if not text:
            return jsonify({
                "success": False,
                "error": "No text provided"
            }), 400
        
        language = data.get('language', 'en-US')
        voice = data.get('voice', 'default')
        speed = float(data.get('speed', 1.0))
        pitch = float(data.get('pitch', 1.0))
        volume = float(data.get('volume', 0.8))
        
        # Synthesize speech
        result = voice_service.synthesize_speech(
            text=text,
            language=language,
            voice=voice,
            speed=speed,
            pitch=pitch,
            volume=volume
        )
        
        if result.success:
            # Create audio file response
            audio_io = io.BytesIO(result.audio_data)
            audio_io.seek(0)
            
            return send_file(
                audio_io,
                mimetype='audio/wav',
                as_attachment=True,
                download_name=f'voice_output_{datetime.now().strftime("%Y%m%d_%H%M%S")}.wav'
            )
        else:
            return jsonify({
                "success": False,
                "error": result.error
            }), 400
            
    except Exception as e:
        logger.error(f"Error downloading audio: {e}")
        return jsonify({
            "success": False,
            "error": f"Internal server error: {str(e)}"
        }), 500

@voice_bp.route('/test', methods=['GET'])
def test_voice_service():
    """Test voice service functionality"""
    try:
        # Test text
        test_text = "Hello, this is a test of the voice synthesis system."
        
        # Test synthesis
        result = voice_service.synthesize_speech(test_text)
        
        if result.success:
            # Encode audio data as base64
            audio_b64 = base64.b64encode(result.audio_data).decode('utf-8')
            
            return jsonify({
                "success": True,
                "message": "Voice service test successful",
                "test_text": test_text,
                "audio_data": audio_b64,
                "duration": result.duration,
                "format": result.format
            })
        else:
            return jsonify({
                "success": False,
                "error": result.error
            }), 400
            
    except Exception as e:
        logger.error(f"Error testing voice service: {e}")
        return jsonify({
            "success": False,
            "error": f"Test error: {str(e)}"
        }), 500
