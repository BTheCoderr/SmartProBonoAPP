"""
Voice AI Routes for SmartProBono
Provides voice-enabled AI endpoints
"""

import logging
import asyncio
from flask import Blueprint, request, jsonify
from werkzeug.exceptions import BadRequest
from services.voice_enhanced_ai_service import VoiceEnhancedAIService

logger = logging.getLogger(__name__)

# Create blueprint
bp = Blueprint('voice_ai', __name__)

# Initialize voice-enhanced AI service
voice_ai_service = VoiceEnhancedAIService()

@bp.route('/voice-chat', methods=['POST'])
def voice_chat():
    """Voice-enabled AI chat endpoint"""
    try:
        data = request.json
        if not data or not data.get('message'):
            raise BadRequest("Missing message")
        
        message = data['message']
        task_type = data.get('task_type', 'chat')
        conversation_id = data.get('conversation_id')
        history = data.get('history', [])
        user_role = data.get('user_role', 'client')
        voice_enabled = data.get('voice_enabled', False)
        
        logger.info(f"Received voice chat message: {message}, task_type: {task_type}, voice_enabled: {voice_enabled}")
        
        # Get user context
        user_id = None
        try:
            from backend.utils.auth import get_current_user
            user = get_current_user()
            if user:
                user_id = user.get('id')
                user_role = user.get('role', user_role)
        except:
            # User not authenticated - still allow chat as guest
            pass
        
        user_context = {
            "user_id": user_id,
            "role": user_role,
            "history": history
        }
        
        # Process with voice-enhanced AI service
        response = asyncio.run(voice_ai_service.process_request(
            message=message,
            user_context=user_context,
            user_role=user_role,
            task_type=task_type,
            voice_enabled=voice_enabled
        ))
        
        return jsonify(response)
        
    except BadRequest as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logger.error(f"Error in voice chat: {e}")
        return jsonify({"error": "Failed to generate response"}), 500

@bp.route('/voice-transfer', methods=['POST'])
def voice_transfer():
    """Transfer to different AI specialist"""
    try:
        data = request.json
        if not data or not data.get('message'):
            raise BadRequest("Missing message")
        
        message = data['message']
        specialist = data.get('specialist', 'sales')  # sales, technical, pricing
        user_role = data.get('user_role', 'client')
        
        logger.info(f"Voice transfer request: {message}, specialist: {specialist}")
        
        # Get user context
        user_id = None
        try:
            from backend.utils.auth import get_current_user
            user = get_current_user()
            if user:
                user_id = user.get('id')
                user_role = user.get('role', user_role)
        except:
            pass
        
        user_context = {
            "user_id": user_id,
            "role": user_role
        }
        
        # Process transfer with voice AI
        transfer_message = f"Transfer to {specialist} specialist: {message}"
        response = asyncio.run(voice_ai_service.process_request(
            message=transfer_message,
            user_context=user_context,
            user_role=user_role,
            task_type="transfer",
            voice_enabled=True
        ))
        
        return jsonify(response)
        
    except BadRequest as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logger.error(f"Error in voice transfer: {e}")
        return jsonify({"error": "Failed to process transfer"}), 500

@bp.route('/voice-capabilities', methods=['GET'])
def voice_capabilities():
    """Get voice AI capabilities and available models"""
    try:
        capabilities = voice_ai_service.get_capabilities()
        models = voice_ai_service.get_available_models()
        
        return jsonify({
            "capabilities": capabilities,
            "models": models,
            "voice_enabled": voice_ai_service.voice_enabled
        })
        
    except Exception as e:
        logger.error(f"Error getting voice capabilities: {e}")
        return jsonify({"error": "Failed to get capabilities"}), 500

@bp.route('/voice-status', methods=['GET'])
def voice_status():
    """Get voice AI service status"""
    try:
        return jsonify({
            "status": "active",
            "voice_enabled": voice_ai_service.voice_enabled,
            "timestamp": voice_ai_service._load_smartprobono_context()[:100] + "..." if voice_ai_service.voice_enabled else "Voice not available"
        })
        
    except Exception as e:
        logger.error(f"Error getting voice status: {e}")
        return jsonify({"error": "Failed to get status"}), 500
