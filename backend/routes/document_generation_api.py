"""
Document Generation API Routes
Handles document generation endpoints
"""

from flask import Blueprint, request, jsonify, send_file
import os
from services.document_generation_service import DocumentGenerationService

bp = Blueprint('document_generation_api', __name__)

# Initialize document generation service
doc_service = DocumentGenerationService()

@bp.route('/api/v1/documents/templates', methods=['GET'])
def get_templates():
    """Get available document templates"""
    try:
        templates = doc_service.get_available_templates()
        return jsonify({
            "success": True,
            "templates": templates
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@bp.route('/api/v1/documents/generate', methods=['POST'])
def generate_document():
    """Generate a document from template and form data"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                "success": False,
                "error": "No data provided"
            }), 400
        
        template_id = data.get('template_id')
        form_data = data.get('form_data', {})
        
        if not template_id:
            return jsonify({
                "success": False,
                "error": "Template ID is required"
            }), 400
        
        result = doc_service.generate_document(template_id, form_data)
        
        if result["success"]:
            return jsonify(result)
        else:
            return jsonify(result), 400
            
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@bp.route('/api/v1/documents/preview/<document_id>', methods=['GET'])
def preview_document(document_id):
    """Get document preview"""
    try:
        content = doc_service.get_document_preview(document_id)
        
        if content:
            return content, 200, {'Content-Type': 'text/html'}
        else:
            return jsonify({
                "success": False,
                "error": "Document not found"
            }), 404
            
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@bp.route('/api/v1/documents/download/<document_id>', methods=['GET'])
def download_document(document_id):
    """Download generated document"""
    try:
        filename = f"{document_id}.html"
        filepath = os.path.join(doc_service.output_dir, filename)
        
        if os.path.exists(filepath):
            return send_file(
                filepath,
                as_attachment=True,
                download_name=filename,
                mimetype='text/html'
            )
        else:
            return jsonify({
                "success": False,
                "error": "Document not found"
            }), 404
            
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@bp.route('/api/v1/documents/categories', methods=['GET'])
def get_categories():
    """Get document categories"""
    try:
        templates = doc_service.get_available_templates()
        categories = list(set(template["category"] for template in templates))
        
        return jsonify({
            "success": True,
            "categories": categories
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500
