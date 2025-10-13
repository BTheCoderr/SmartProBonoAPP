"""
Model Management Routes
Endpoints for managing AI models, training custom models, and model configuration
"""

from flask import Blueprint, request, jsonify
from werkzeug.exceptions import BadRequest
import logging
from datetime import datetime

from services.custom_legal_model_trainer import custom_legal_trainer
from services.saul_legal_ai_service import saul_legal_ai
from services.saul_enhanced_ai_service import saul_enhanced_ai
from services.model_config_service import model_config_service
from services.auth_service import get_current_user

bp = Blueprint('model_management', __name__, url_prefix='/api/v1/models')
logger = logging.getLogger(__name__)

# ============================================================================
# MODEL INFORMATION ENDPOINTS
# ============================================================================

@bp.route('/available', methods=['GET'])
def list_available_models():
    """
    List all available AI models (both pre-trained and custom)
    
    Returns:
        List of available models with their status and capabilities
    """
    try:
        # Get Saul model info
        saul_models = saul_enhanced_ai.get_available_models()
        
        # Get custom models
        custom_models = custom_legal_trainer.list_custom_models()
        
        return jsonify({
            "success": True,
            "pretrained_models": saul_models,
            "custom_models": custom_models,
            "total_models": len(saul_models) + len(custom_models),
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error listing models: {e}")
        return jsonify({"error": str(e)}), 500

@bp.route('/status', methods=['GET'])
def model_status():
    """
    Get current status of all AI models
    
    Returns:
        Health status and availability of each model
    """
    try:
        health = saul_enhanced_ai.health_check()
        
        return jsonify({
            "success": True,
            "health": health,
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error checking model status: {e}")
        return jsonify({"error": str(e)}), 500

# ============================================================================
# CUSTOM MODEL TRAINING ENDPOINTS
# ============================================================================

@bp.route('/train/prepare-data', methods=['POST'])
def prepare_training_data():
    """
    Prepare training data from conversations
    
    Expected payload:
    {
        "conversations": [
            {"question": "...", "answer": "..."},
            ...
        ],
        "output_file": "optional_filename.json"
    }
    
    Returns:
        Path to prepared training data file
    """
    try:
        data = request.json
        if not data or not data.get('conversations'):
            raise BadRequest("Conversations data is required")
        
        conversations = data['conversations']
        output_file = data.get('output_file')
        
        # Prepare training data
        training_file = custom_legal_trainer.prepare_training_data(
            conversations=conversations,
            output_file=output_file
        )
        
        return jsonify({
            "success": True,
            "training_file": training_file,
            "num_examples": len(conversations),
            "timestamp": datetime.now().isoformat()
        })
        
    except BadRequest as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logger.error(f"Error preparing training data: {e}")
        return jsonify({"error": str(e)}), 500

@bp.route('/train/start', methods=['POST'])
def start_training():
    """
    Start training a custom legal model
    
    Expected payload:
    {
        "training_data_path": "path/to/training_data.json",
        "model_name": "my-custom-legal-model",
        "epochs": 3,
        "batch_size": 4,
        "learning_rate": 0.00002
    }
    
    Returns:
        Training results and model information
    """
    try:
        data = request.json
        if not data or not data.get('training_data_path'):
            raise BadRequest("Training data path is required")
        
        if not data.get('model_name'):
            raise BadRequest("Model name is required")
        
        # Start training (this will take a while!)
        result = custom_legal_trainer.train_custom_model(
            training_data_path=data['training_data_path'],
            model_name=data['model_name'],
            epochs=data.get('epochs', 3),
            batch_size=data.get('batch_size', 4),
            learning_rate=data.get('learning_rate', 2e-5)
        )
        
        if result.get('success'):
            return jsonify(result)
        else:
            return jsonify(result), 500
        
    except BadRequest as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logger.error(f"Error starting training: {e}")
        return jsonify({"error": str(e)}), 500

@bp.route('/train/export-conversations', methods=['POST'])
def export_conversations():
    """
    Export existing conversations for training
    
    Expected payload:
    {
        "db_path": "optional/path/to/database"
    }
    
    Returns:
        Path to exported training data
    """
    try:
        data = request.json or {}
        db_path = data.get('db_path')
        
        # Export conversations
        training_file = custom_legal_trainer.export_conversations_for_training(
            db_path=db_path
        )
        
        return jsonify({
            "success": True,
            "training_file": training_file,
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error exporting conversations: {e}")
        return jsonify({"error": str(e)}), 500

# ============================================================================
# MODEL CONFIGURATION ENDPOINTS
# ============================================================================

@bp.route('/config', methods=['GET'])
def get_model_config():
    """
    Get current model configuration
    
    Returns:
        Current model settings and parameters
    """
    try:
        saul_info = saul_legal_ai.get_model_info()
        full_config = model_config_service.get_full_config()
        
        config = {
            "current_model": saul_info.get('model_name'),
            "device": saul_info.get('device'),
            "model_type": saul_info.get('model_type'),
            "is_loaded": saul_info.get('is_loaded'),
            **full_config
        }
        
        return jsonify({
            "success": True,
            "config": config,
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error getting model config: {e}")
        return jsonify({"error": str(e)}), 500

@bp.route('/config', methods=['POST'])
def update_model_config():
    """
    Update model configuration
    
    Expected payload:
    {
        "generation_params": {
            "max_tokens": 200,
            "temperature": 0.8,
            "top_p": 0.95
        }
    }
    
    Returns:
        Updated configuration
    """
    try:
        data = request.json
        if not data:
            raise BadRequest("Configuration data is required")
        
        result = {}
        
        # Update generation params if provided
        if "generation_params" in data:
            result["generation_params"] = model_config_service.update_generation_params(
                data["generation_params"]
            )
        
        # Update quality settings if provided
        if "quality_settings" in data:
            result["quality_settings"] = model_config_service.update_quality_settings(
                data["quality_settings"]
            )
        
        return jsonify({
            "success": True,
            "message": "Configuration updated successfully",
            "updates": result,
            "timestamp": datetime.now().isoformat()
        })
        
    except BadRequest as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logger.error(f"Error updating model config: {e}")
        return jsonify({"error": str(e)}), 500

@bp.route('/config/presets', methods=['GET'])
def get_config_presets():
    """
    Get available configuration presets
    
    Returns:
        List of available presets
    """
    try:
        presets = model_config_service.get_presets()
        
        return jsonify({
            "success": True,
            "presets": presets,
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error getting presets: {e}")
        return jsonify({"error": str(e)}), 500

@bp.route('/config/presets/<preset_name>', methods=['POST'])
def apply_config_preset(preset_name):
    """
    Apply a configuration preset
    
    Args:
        preset_name: Name of preset to apply (fast, balanced, quality, creative, precise)
    
    Returns:
        Updated configuration
    """
    try:
        result = model_config_service.apply_preset(preset_name)
        
        if result.get("success"):
            return jsonify(result)
        else:
            return jsonify(result), 404
        
    except Exception as e:
        logger.error(f"Error applying preset: {e}")
        return jsonify({"error": str(e)}), 500

@bp.route('/config/reset', methods=['POST'])
def reset_config():
    """
    Reset configuration to defaults
    
    Returns:
        Status of reset operation
    """
    try:
        result = model_config_service.reset_to_defaults()
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error resetting config: {e}")
        return jsonify({"error": str(e)}), 500

# ============================================================================
# MODEL TESTING ENDPOINTS
# ============================================================================

@bp.route('/test/<model_name>', methods=['POST'])
def test_model(model_name):
    """
    Test a specific model with a sample prompt
    
    Expected payload:
    {
        "message": "Test question",
        "max_tokens": 100
    }
    
    Returns:
        Model response for testing
    """
    try:
        data = request.json
        if not data or not data.get('message'):
            raise BadRequest("Message is required")
        
        message = data['message']
        max_tokens = data.get('max_tokens', 100)
        
        # Generate response
        if model_name == "saul":
            response = saul_legal_ai.generate_response(
                message=message,
                task_type="legal",
                max_tokens=max_tokens
            )
        else:
            return jsonify({"error": f"Model '{model_name}' not found"}), 404
        
        return jsonify({
            "success": True,
            "model": model_name,
            "response": response,
            "timestamp": datetime.now().isoformat()
        })
        
    except BadRequest as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logger.error(f"Error testing model: {e}")
        return jsonify({"error": str(e)}), 500

