from flask import Blueprint, jsonify, request, send_file
from services.digital_signature import digital_signature_service
from services.audit_trail import audit_trail_service
from services.secure_storage import SecureStorageService
from utils.auth import require_auth
import os
import json
from datetime import datetime

security_routes = Blueprint('security_routes', __name__)
secure_storage = SecureStorageService()

# Digital Signature Endpoints
@security_routes.route('/api/signatures/generate-keys', methods=['POST'])
@require_auth
def generate_keys():
    """Generate a new key pair for a user"""
    try:
        user_id = request.json.get('user_id')
        if not user_id:
            return jsonify({'error': 'User ID is required'}), 400
            
        public_key_path, private_key_path = digital_signature_service.generate_key_pair(user_id)
        
        # Log key generation event
        audit_trail_service.log_event(
            entity_id=user_id,
            event_type='key_generation',
            user_id=user_id,
            details={'timestamp': datetime.now().isoformat()}
        )
        
        return jsonify({
            'message': 'Key pair generated successfully',
            'public_key_path': public_key_path
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@security_routes.route('/api/signatures/sign', methods=['POST'])
@require_auth
def sign_document():
    """Sign a document"""
    try:
        data = request.json
        required_fields = ['user_id', 'document_id', 'document_hash']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400
            
        signature_id = digital_signature_service.sign_document(
            user_id=data['user_id'],
            document_id=data['document_id'],
            document_hash=data['document_hash']
        )
        
        return jsonify({
            'signature_id': signature_id,
            'message': 'Document signed successfully'
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@security_routes.route('/api/signatures/verify', methods=['POST'])
@require_auth
def verify_signature():
    """Verify a document signature"""
    try:
        data = request.json
        required_fields = ['signature_id', 'document_hash']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400
            
        is_valid = digital_signature_service.verify_signature(
            signature_id=data['signature_id'],
            document_hash=data['document_hash']
        )
        
        return jsonify({
            'is_valid': is_valid,
            'message': 'Signature verified successfully'
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@security_routes.route('/api/signatures/<signature_id>/metadata', methods=['GET'])
@require_auth
def get_signature_metadata(signature_id):
    """Get metadata for a signature"""
    try:
        metadata = digital_signature_service.get_signature_metadata(signature_id)
        if not metadata:
            return jsonify({'error': 'Signature not found'}), 404
            
        return jsonify(metadata), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Audit Trail Endpoints
@security_routes.route('/api/audit-trail/<entity_id>', methods=['GET'])
@require_auth
def get_audit_trail(entity_id):
    """Get audit trail for an entity"""
    try:
        filters = request.args.to_dict()
        trail = audit_trail_service.get_audit_trail(entity_id, filters)
        return jsonify(trail), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@security_routes.route('/api/audit-trail/user/<user_id>', methods=['GET'])
@require_auth
def get_user_audit_trail(user_id):
    """Get audit trail for a user"""
    try:
        events = audit_trail_service.get_user_events(user_id)
        return jsonify(events), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@security_routes.route('/api/audit-trail/recent', methods=['GET'])
@require_auth
def get_recent_events():
    """Get recent audit trail events"""
    try:
        limit = request.args.get('limit', 100, type=int)
        events = audit_trail_service.get_recent_events(limit)
        return jsonify(events), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Secure Storage Endpoints
@security_routes.route('/api/documents/store', methods=['POST'])
@require_auth
def store_document():
    """Store a document securely"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
            
        file = request.files['file']
        metadata = request.form.get('metadata', '{}')
        
        # Save file temporarily
        temp_path = os.path.join('/tmp', file.filename)
        file.save(temp_path)
        
        # Store file securely
        file_id = secure_storage.store_file(temp_path, json.loads(metadata))
        
        # Clean up temp file
        os.remove(temp_path)
        
        return jsonify({
            'file_id': file_id,
            'message': 'Document stored successfully'
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@security_routes.route('/api/documents/<file_id>', methods=['GET'])
@require_auth
def get_document(file_id):
    """Retrieve a stored document"""
    try:
        output_path = os.path.join('/tmp', f'download_{file_id}')
        file_path = secure_storage.retrieve_file(file_id, output_path)
        
        return send_file(
            file_path,
            as_attachment=True,
            download_name=os.path.basename(file_path)
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if os.path.exists(output_path):
            os.remove(output_path)

@security_routes.route('/api/documents/<file_id>/metadata', methods=['PUT'])
@require_auth
def update_document_metadata(file_id):
    """Update document metadata"""
    try:
        metadata = request.json
        if not metadata:
            return jsonify({'error': 'No metadata provided'}), 400
            
        success = secure_storage.update_metadata(file_id, metadata)
        if not success:
            return jsonify({'error': 'Document not found'}), 404
            
        return jsonify({
            'message': 'Metadata updated successfully'
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500 