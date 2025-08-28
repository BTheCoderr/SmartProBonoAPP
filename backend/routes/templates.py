from flask import Blueprint, request, jsonify, send_file, current_app
from werkzeug.exceptions import BadRequest
import json
import os
from datetime import datetime
import logging
from backend.services.auth_service import require_auth, get_current_user
from backend.services.document_service import generate_document, generate_pdf
import uuid
from utils.document_generator import list_templates

bp = Blueprint('templates', __name__)
logger = logging.getLogger(__name__)

@bp.route('/api/templates', methods=['GET'])
def get_templates():
    """Get list of available templates"""
    try:
        templates = list_templates()
        return jsonify({
            'success': True,
            'templates': templates
        }), 200
    except Exception as e:
        current_app.logger.error(f"Error listing templates: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to list templates'
        }), 500

@bp.route('/api/templates/<template_id>', methods=['GET'])
def get_template(template_id):
    """Get template details and fields"""
    try:
        templates = list_templates()
        template = next((t for t in templates if t['id'] == template_id), None)
        
        if not template:
            return jsonify({
                'success': False,
                'error': 'Template not found'
            }), 404
            
        # Mock template fields (in a real app, these would be stored in the template metadata)
        fields = [
            {'name': 'title', 'label': 'Document Title', 'type': 'text', 'required': True},
            {'name': 'client_name', 'label': 'Client Name', 'type': 'text', 'required': True},
            {'name': 'matter_description', 'label': 'Matter Description', 'type': 'text', 'required': True},
            {'name': 'content', 'label': 'Document Content', 'type': 'textarea', 'required': True},
            {'name': 'user_name', 'label': 'User Name', 'type': 'text', 'required': True}
        ]
        
        template['fields'] = fields
        return jsonify({
            'success': True,
            'template': template
        }), 200
    except Exception as e:
        current_app.logger.error(f"Error getting template: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to get template'
        }), 500

@bp.route('/api/templates/generate', methods=['POST'])
def generate_template():
    """Generate document from template with provided data"""
    try:
        data = request.json
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'No data provided'
            }), 400
            
        template_id = data.get('template_id')
        if not template_id:
            return jsonify({
                'success': False,
                'error': 'Template ID is required'
            }), 400
            
        # Generate document
        output_format = data.get('format', 'pdf').lower()
        
        # Create document in database (mock)
        document_id = str(uuid.uuid4())
        
        # Generate document
        output_path = generate_document(
            template_id,
            data.get('data', {}),
            output_format
        )
        
        # Save document path to user's documents (mock)
        document = {
            'id': document_id,
            'template_id': template_id,
            'name': data.get('data', {}).get('title', 'Untitled Document'),
            'created_at': datetime.now().isoformat(),
            'path': output_path,
            'format': output_format
        }
        
        # In a real app, save to database
        documents_dir = os.path.join(current_app.instance_path, 'documents')
        os.makedirs(documents_dir, exist_ok=True)
        
        with open(os.path.join(documents_dir, f"{document_id}.json"), 'w') as f:
            json.dump(document, f)
        
        return jsonify({
            'success': True,
            'document': {
                'id': document_id,
                'name': document['name'],
                'created_at': document['created_at'],
                'format': output_format
            }
        }), 200
    except Exception as e:
        current_app.logger.error(f"Error generating document: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Failed to generate document: {str(e)}'
        }), 500

@bp.route('/api/documents/<document_id>/download', methods=['GET'])
def download_document(document_id):
    """Download generated document"""
    try:
        documents_dir = os.path.join(current_app.instance_path, 'documents')
        document_path = os.path.join(documents_dir, f"{document_id}.json")
        
        if not os.path.exists(document_path):
            return jsonify({
                'success': False,
                'error': 'Document not found'
            }), 404
            
        with open(document_path, 'r') as f:
            document = json.load(f)
            
        if not os.path.exists(document['path']):
            return jsonify({
                'success': False,
                'error': 'Document file not found'
            }), 404
            
        return send_file(
            document['path'],
            as_attachment=True,
            download_name=f"{document['name']}.{document['format']}",
            mimetype='application/pdf' if document['format'] == 'pdf' else 'text/html'
        )
    except Exception as e:
        current_app.logger.error(f"Error downloading document: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Failed to download document: {str(e)}'
        }), 500

@bp.route('/categories', methods=['GET'])
def get_template_categories():
    """Get list of document template categories"""
    try:
        categories = [
            {"id": "court_documents", "name": "Court Documents", "description": "Official documents for filing with courts"},
            {"id": "letters", "name": "Letters", "description": "Formal letters for legal communications"},
            {"id": "contracts", "name": "Contracts", "description": "Legal agreements and contracts"},
            {"id": "forms", "name": "Forms", "description": "Standard forms for various legal needs"}
        ]
        
        return jsonify({"categories": categories})
    except Exception as e:
        logger.error(f"Error getting template categories: {str(e)}")
        return jsonify({"error": str(e)}), 500

@bp.route('/custom', methods=['POST'])
@require_auth
def create_custom_template():
    """Create a custom document template (admin only)"""
    try:
        current_user = get_current_user()
        
        # Check if user has admin privileges (in a real app)
        if not current_user.get('is_admin'):
            return jsonify({"error": "Unauthorized"}), 403
            
        data = request.json
        if not data or not data.get('name') or not data.get('fields'):
            raise BadRequest("Missing required template data")
            
        # Generate a template ID
        template_id = f"custom_{data['name'].lower().replace(' ', '_')}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        # In a real app, would save to database
        template = {
            "id": template_id,
            "name": data['name'],
            "description": data.get('description', ''),
            "category": data.get('category', 'custom'),
            "fields": data['fields'],
            "created_by": current_user['id'],
            "created_at": datetime.now().isoformat()
        }
        
        return jsonify({
            "success": True,
            "template": template
        })
    except BadRequest as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logger.error(f"Error creating custom template: {str(e)}")
        return jsonify({"error": str(e)}), 500 