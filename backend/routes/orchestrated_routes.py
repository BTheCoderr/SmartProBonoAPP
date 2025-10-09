"""
Orchestrated AI Routes - Multiple Models Working Together
Each response uses 4-5 different AI models for the BEST answer
"""

from flask import Blueprint, request, jsonify
import logging
import sys
import os

# Load environment variables
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

logger = logging.getLogger(__name__)

# Create blueprint
bp = Blueprint('orchestrated', __name__, url_prefix='/api/orchestrated')

# Import orchestrated AI service
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'services'))
from orchestrated_ai import orchestrated_ai

@bp.route('/chat', methods=['POST'])
def orchestrated_chat():
    """
    Chat endpoint using ORCHESTRATED multi-model approach
    
    Each response uses 4-5 models:
    1. Tinyllama - Query analysis
    2. Gemini/Gemma2 - Deep research
    3. Gemma2 - Legal verification
    4. Qwen - Compliance check
    5. Gemini/Gemma2 - Final synthesis
    
    Body:
    - message: User message (required)
    - task_type: Type of task (optional, default: "legal")
    """
    try:
        data = request.json
        if not data or not data.get('message'):
            return jsonify({"error": "Message is required", "success": False}), 400
        
        message = data['message']
        task_type = data.get('task_type', 'legal')
        
        # Generate orchestrated response
        response = orchestrated_ai.generate_best_response(message, task_type)
        
        return jsonify(response)
        
    except Exception as e:
        logger.error(f"Error in orchestrated chat: {e}")
        return jsonify({"error": str(e), "success": False}), 500

@bp.route('/status', methods=['GET'])
def orchestration_status():
    """Get orchestration system status"""
    try:
        status = orchestrated_ai.get_status()
        return jsonify({
            "success": True,
            **status,
            "description": "Multi-model orchestration: 4-5 models collaborate on each response",
            "benefits": [
                "More accurate (multiple models verify)",
                "More comprehensive (different perspectives)",
                "More reliable (cross-validation)",
                "Still 100% FREE ($0/month)"
            ]
        })
    except Exception as e:
        logger.error(f"Error getting orchestration status: {e}")
        return jsonify({"error": str(e), "success": False}), 500

@bp.route('/compare', methods=['POST'])
def compare_responses():
    """
    Compare single-model vs orchestrated responses
    
    Body:
    - message: User message (required)
    """
    try:
        data = request.json
        if not data or not data.get('message'):
            return jsonify({"error": "Message is required", "success": False}), 400
        
        message = data['message']
        
        # Get orchestrated response
        orchestrated_response = orchestrated_ai.generate_best_response(message, "legal")
        
        # Get single-model response for comparison
        from simple_free_ai import simple_free_ai
        single_response = simple_free_ai.generate_response(message, "legal")
        
        return jsonify({
            "success": True,
            "comparison": {
                "orchestrated": {
                    "text": orchestrated_response.get("text"),
                    "models_used": orchestrated_response.get("orchestration", {}).get("models_consulted", []),
                    "steps": orchestrated_response.get("orchestration", {}).get("steps", []),
                    "length": len(orchestrated_response.get("text", ""))
                },
                "single_model": {
                    "text": single_response.get("text"),
                    "model": single_response.get("model"),
                    "length": len(single_response.get("text", ""))
                },
                "analysis": {
                    "orchestrated_length": len(orchestrated_response.get("text", "")),
                    "single_length": len(single_response.get("text", "")),
                    "difference": len(orchestrated_response.get("text", "")) - len(single_response.get("text", "")),
                    "models_consulted": len(orchestrated_response.get("orchestration", {}).get("models_consulted", []))
                }
            }
        })
        
    except Exception as e:
        logger.error(f"Error comparing responses: {e}")
        return jsonify({"error": str(e), "success": False}), 500

