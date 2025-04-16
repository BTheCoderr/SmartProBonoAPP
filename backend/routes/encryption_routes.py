from flask import Blueprint, jsonify, request
from services.encryption_service import encryption_service
from utils.auth import require_auth

encryption_routes = Blueprint('encryption_routes', __name__)

@encryption_routes.route('/api/encryption/conversation', methods=['POST'])
@require_auth
def create_conversation():
    """Create a new encrypted conversation"""
    try:
        data = request.get_json()
        conversation_id = data.get('conversation_id')
        password = data.get('password')
        
        if not conversation_id or not password:
            return jsonify({'error': 'Conversation ID and password are required'}), 400
            
        result = encryption_service.create_conversation(conversation_id, password)
        return jsonify(result), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@encryption_routes.route('/api/encryption/message', methods=['POST'])
@require_auth
def encrypt_message():
    """Encrypt a message"""
    try:
        data = request.get_json()
        conversation_id = data.get('conversation_id')
        password = data.get('password')
        message = data.get('message')
        
        if not conversation_id or not password or not message:
            return jsonify({'error': 'Conversation ID, password, and message are required'}), 400
            
        encrypted = encryption_service.encrypt_message(conversation_id, password, message)
        return jsonify({'encrypted_message': encrypted}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@encryption_routes.route('/api/encryption/message', methods=['PUT'])
@require_auth
def decrypt_message():
    """Decrypt a message"""
    try:
        data = request.get_json()
        conversation_id = data.get('conversation_id')
        password = data.get('password')
        encrypted_message = data.get('encrypted_message')
        
        if not conversation_id or not password or not encrypted_message:
            return jsonify({'error': 'Conversation ID, password, and encrypted message are required'}), 400
            
        decrypted = encryption_service.decrypt_message(conversation_id, password, encrypted_message)
        return jsonify({'decrypted_message': decrypted}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@encryption_routes.route('/api/encryption/key', methods=['PUT'])
@require_auth
def rotate_key():
    """Rotate encryption key for a conversation"""
    try:
        data = request.get_json()
        conversation_id = data.get('conversation_id')
        old_password = data.get('old_password')
        new_password = data.get('new_password')
        
        if not conversation_id or not old_password or not new_password:
            return jsonify({'error': 'Conversation ID, old password, and new password are required'}), 400
            
        result = encryption_service.rotate_key(conversation_id, old_password, new_password)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500 