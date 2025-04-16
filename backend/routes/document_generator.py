"""
Document Generator API routes
Provides endpoints for generating legal documents
"""
from flask import Blueprint, request, jsonify, send_file, current_app, Response
import os
import json
from datetime import datetime
from typing import Dict, Any, List, Optional, Union, Tuple, cast
from werkzeug.exceptions import NotFound, BadRequest
from sqlalchemy.orm import Session
from pathlib import Path

from config.database import DatabaseConfig
from models.document import Document
from services.document_template_engine import DocumentTemplateEngine, DocumentValidationError
from utils.auth import require_auth
from flask_login import current_user, login_required

# Create the document generator blueprint
document_generator_bp = Blueprint('document_generator', __name__)

# Document templates directory
TEMPLATES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../templates')
if not os.path.exists(TEMPLATES_DIR):
    os.makedirs(TEMPLATES_DIR)

# Initialize template engine
template_engine = DocumentTemplateEngine(TEMPLATES_DIR)

@document_generator_bp.route('/templates', methods=['GET'])
@login_required
def get_templates() -> Union[Dict[str, List[Dict[str, Any]]], Tuple[Dict[str, str], int]]:
    """Get list of available document templates."""
    try:
        templates = template_engine.get_templates()
        return {'templates': templates}
    except Exception as e:
        return {'error': str(e)}, 500

@document_generator_bp.route('/generate', methods=['POST'])
@login_required
def generate_document() -> Union[Dict[str, Any], Tuple[Dict[str, str], int]]:
    """Generate a document from a template."""
    data = request.get_json()
    if not data or 'template_id' not in data:
        raise BadRequest('Missing template_id in request')

    template_id = data['template_id']
    field_values = data.get('field_values', {})
    session = DatabaseConfig.get_session()

    try:
        # Create output directory if it doesn't exist
        output_dir = os.path.join(current_app.root_path, 'generated_documents')
        os.makedirs(output_dir, exist_ok=True)

        # Generate unique filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{template_id}_{timestamp}.pdf"
        output_path = os.path.join(output_dir, filename)

        # Generate document
        template_engine.generate_document(template_id, field_values, output_path)

        # Save document to database
        document = Document.create(
            title=f"{template_id} - {timestamp}",
            file_path=output_path,
            user_id=str(current_user.id)  # Ensure ID is string
        )

        return {
            'document_id': document.id,
            'message': 'Document generated successfully'
        }

    except DocumentValidationError as e:
        if session:
            session.rollback()
        return {'error': str(e)}, 400
    except Exception as e:
        if session:
            session.rollback()
        current_app.logger.error(f"Error generating document: {str(e)}")
        return {'error': str(e)}, 500
    finally:
        if session:
            session.close()

@document_generator_bp.route('/download/<document_id>', methods=['GET'])
@login_required
def download_document(document_id: str) -> Union[Any, Tuple[Dict[str, str], int]]:
    """Download a generated document."""
    try:
        document = Document.get_by_id(document_id)
        if not document:
            raise NotFound('Document not found')

        file_path = cast(str, document.file_path)
        if not os.path.exists(file_path):
            raise NotFound('Document file not found')

        return send_file(
            file_path,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=os.path.basename(file_path)
        )

    except NotFound as e:
        return {'error': str(e)}, 404
    except Exception as e:
        current_app.logger.error(f"Error downloading document: {str(e)}")
        return {'error': str(e)}, 500

@document_generator_bp.route('/api/documents/templates', methods=['GET'])
@require_auth
def get_template_details() -> Union[Response, Tuple[Response, int]]:
    """Get detailed information about a specific template"""
    template_id = request.args.get('template_id')
    if not template_id:
        return jsonify({'error': 'Template ID is required'}), 400
        
    try:
        template_info = template_engine.get_template_fields(template_id)
        if not template_info:
            return jsonify({'error': 'Template not found'}), 404
        return jsonify(template_info)
    except Exception as e:
        current_app.logger.error(f"Error getting template details: {str(e)}")
        return jsonify({'error': 'Could not fetch template details'}), 500

@document_generator_bp.route('/api/documents/<document_id>/versions', methods=['GET'])
@require_auth
def get_document_versions(document_id: str) -> Union[Response, Tuple[Response, int]]:
    """Get all versions of a document"""
    try:
        document = Document.get_by_id(document_id)
        if not document:
            return jsonify({'error': 'Document not found'}), 404

        file_path = cast(str, document.file_path)
        versions = template_engine.get_document_versions(file_path)
        return jsonify({
            'document_id': document_id,
            'current_version': versions[-1] if versions else None,
            'versions': versions
        })
    except Exception as e:
        current_app.logger.error(f"Error getting document versions: {str(e)}")
        return jsonify({'error': 'Could not fetch document versions'}), 500

@document_generator_bp.route('/api/documents/<document_id>/versions/<int:version>', methods=['GET'])
@require_auth
def download_document_version(document_id: str, version: int) -> Union[Response, Tuple[Response, int]]:
    """Download a specific version of a document"""
    try:
        document = Document.get_by_id(document_id)
        if not document:
            return jsonify({'error': 'Document not found'}), 404

        file_path = cast(str, document.file_path)
        versions = template_engine.get_document_versions(file_path)
        version_info = next((v for v in versions if v['version'] == version), None)
        
        if not version_info:
            return jsonify({'error': 'Version not found'}), 404

        return send_file(
            version_info['path'],
            as_attachment=True,
            download_name=version_info['filename'],
            mimetype='application/pdf'
        )
    except Exception as e:
        current_app.logger.error(f"Error downloading document version: {str(e)}")
        return jsonify({'error': 'Could not download document version'}), 500

@document_generator_bp.route('/api/documents/download/<document_id>', methods=['GET'])
@require_auth
def download_document_latest(document_id: str) -> Union[Response, Tuple[Response, int]]:
    """Download the latest version of a document"""
    try:
        document = Document.get_by_id(document_id)
        if not document:
            return jsonify({'error': 'Document not found'}), 404

        file_path = cast(str, document.file_path)
        versions = template_engine.get_document_versions(file_path)
        if not versions:
            return jsonify({'error': 'No versions found'}), 404

        latest_version = versions[-1]
        return send_file(
            latest_version['path'],
            as_attachment=True,
            download_name=latest_version['filename'],
            mimetype='application/pdf'
        )
    except Exception as e:
        current_app.logger.error(f"Error downloading document: {str(e)}")
        return jsonify({'error': 'Could not download document'}), 500
