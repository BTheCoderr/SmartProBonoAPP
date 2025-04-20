"""
API routes for managing document templates and generating documents.

This module provides endpoints for:
- Listing, creating, and updating document templates
- Retrieving template fields
- Generating documents from templates
- Retrieving and downloading generated documents
- Getting available template categories
"""

from flask import Blueprint, jsonify, request, send_file
from http import HTTPStatus
import uuid
from typing import Dict, Any, List, Optional, Union
import logging
import io

from backend.auth.jwt_auth import jwt_required, get_jwt_identity
from backend.models.user import User
from backend.models.document_template import DocumentTemplate, DocumentTemplateVersion
from backend.models.document import GeneratedDocument
from backend.services.document_service import (
    get_template_by_id,
    create_template,
    update_template,
    get_templates,
    generate_document,
    get_document_by_id,
    get_template_categories
)
from backend.utils.roles import has_role, RoleType

# Set up logging
logger = logging.getLogger(__name__)

# Create blueprint
document_template_bp = Blueprint('document_templates', __name__, url_prefix='/api')

@document_template_bp.route('/templates', methods=['GET'])
@jwt_required
def get_all_templates():
    """Get all document templates with optional filtering."""
    try:
        # Get query parameters
        category = request.args.get('category')
        search_term = request.args.get('search')
        show_unpublished = request.args.get('show_unpublished', 'false').lower() == 'true'
        
        # Check permissions for unpublished templates
        if show_unpublished:
            current_user_id = get_jwt_identity()
            current_user = User.get_by_id(current_user_id)
            if not current_user or not has_role(current_user, [RoleType.ADMIN, RoleType.ATTORNEY]):
                return jsonify({"error": "Unauthorized to view unpublished templates"}), HTTPStatus.FORBIDDEN
        
        # Get templates with filtering
        templates = get_templates(
            category=category,
            search_term=search_term,
            include_unpublished=show_unpublished
        )
        
        # Format response
        response = [{
            "id": str(template.id),
            "title": template.title,
            "description": template.description,
            "category": template.category,
            "created_at": template.created_at.isoformat(),
            "updated_at": template.updated_at.isoformat() if template.updated_at else None,
            "created_by": str(template.created_by),
            "current_version": str(template.current_version_id) if template.current_version_id else None,
            "is_published": template.is_published
        } for template in templates]
        
        return jsonify(response), HTTPStatus.OK
    
    except Exception as e:
        logger.error(f"Error retrieving templates: {str(e)}")
        return jsonify({"error": "Failed to retrieve templates"}), HTTPStatus.INTERNAL_SERVER_ERROR

@document_template_bp.route('/templates/<uuid:template_id>', methods=['GET'])
@jwt_required
def get_template(template_id):
    """Get a specific document template by ID."""
    try:
        # Get current user for permission check
        current_user_id = get_jwt_identity()
        current_user = User.get_by_id(current_user_id)
        
        # Get template
        template = get_template_by_id(template_id)
        if not template:
            return jsonify({"error": "Template not found"}), HTTPStatus.NOT_FOUND
        
        # Check permissions for unpublished templates
        if not template.is_published and not has_role(current_user, [RoleType.ADMIN, RoleType.ATTORNEY]):
            return jsonify({"error": "Unauthorized to view this template"}), HTTPStatus.FORBIDDEN
        
        # Get current version
        current_version = None
        if template.current_version_id:
            current_version = DocumentTemplateVersion.get_by_id(template.current_version_id)
        
        # Format response
        response = {
            "id": str(template.id),
            "title": template.title,
            "description": template.description,
            "category": template.category,
            "created_at": template.created_at.isoformat(),
            "updated_at": template.updated_at.isoformat() if template.updated_at else None,
            "created_by": str(template.created_by),
            "is_published": template.is_published,
            "current_version": {
                "id": str(current_version.id),
                "content": current_version.content,
                "field_schema": current_version.field_schema,
                "version_number": current_version.version_number,
                "created_at": current_version.created_at.isoformat()
            } if current_version else None
        }
        
        return jsonify(response), HTTPStatus.OK
    
    except Exception as e:
        logger.error(f"Error retrieving template {template_id}: {str(e)}")
        return jsonify({"error": "Failed to retrieve template"}), HTTPStatus.INTERNAL_SERVER_ERROR

@document_template_bp.route('/templates', methods=['POST'])
@jwt_required
def create_new_template():
    """Create a new document template."""
    try:
        # Get current user for permission check
        current_user_id = get_jwt_identity()
        current_user = User.get_by_id(current_user_id)
        
        # Check permissions
        if not has_role(current_user, [RoleType.ADMIN, RoleType.ATTORNEY]):
            return jsonify({"error": "Unauthorized to create templates"}), HTTPStatus.FORBIDDEN
        
        # Get request data
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), HTTPStatus.BAD_REQUEST
        
        # Validate required fields
        required_fields = ['title', 'content', 'field_schema', 'category']
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({
                "error": f"Missing required fields: {', '.join(missing_fields)}"
            }), HTTPStatus.BAD_REQUEST
        
        # Extract template data
        title = data.get('title')
        description = data.get('description', '')
        content = data.get('content')
        field_schema = data.get('field_schema')
        category = data.get('category')
        is_published = data.get('is_published', False)
        
        # Create template
        template = create_template(
            title=title,
            description=description,
            content=content,
            field_schema=field_schema,
            category=category,
            created_by=current_user_id,
            is_published=is_published
        )
        
        # Format response
        response = {
            "id": str(template.id),
            "title": template.title,
            "description": template.description,
            "category": template.category,
            "created_at": template.created_at.isoformat(),
            "created_by": str(template.created_by),
            "is_published": template.is_published,
            "current_version_id": str(template.current_version_id)
        }
        
        return jsonify(response), HTTPStatus.CREATED
    
    except Exception as e:
        logger.error(f"Error creating template: {str(e)}")
        return jsonify({"error": "Failed to create template"}), HTTPStatus.INTERNAL_SERVER_ERROR

@document_template_bp.route('/templates/<uuid:template_id>', methods=['PUT'])
@jwt_required
def update_existing_template(template_id):
    """Update an existing document template."""
    try:
        # Get current user for permission check
        current_user_id = get_jwt_identity()
        current_user = User.get_by_id(current_user_id)
        
        # Check permissions
        if not has_role(current_user, [RoleType.ADMIN, RoleType.ATTORNEY]):
            return jsonify({"error": "Unauthorized to update templates"}), HTTPStatus.FORBIDDEN
        
        # Get template
        template = get_template_by_id(template_id)
        if not template:
            return jsonify({"error": "Template not found"}), HTTPStatus.NOT_FOUND
        
        # Get request data
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), HTTPStatus.BAD_REQUEST
        
        # Extract template data
        title = data.get('title', template.title)
        description = data.get('description', template.description)
        content = data.get('content')
        field_schema = data.get('field_schema')
        category = data.get('category', template.category)
        is_published = data.get('is_published', template.is_published)
        
        # Validate content and field_schema when updating version
        if (content is None or field_schema is None) and (content is not None or field_schema is not None):
            return jsonify({
                "error": "Both content and field_schema must be provided together when updating version"
            }), HTTPStatus.BAD_REQUEST
        
        # Update template
        updated_template = update_template(
            template_id=template_id,
            title=title,
            description=description,
            content=content,
            field_schema=field_schema,
            category=category,
            updated_by=current_user_id,
            is_published=is_published
        )
        
        # Format response
        response = {
            "id": str(updated_template.id),
            "title": updated_template.title,
            "description": updated_template.description,
            "category": updated_template.category,
            "created_at": updated_template.created_at.isoformat(),
            "updated_at": updated_template.updated_at.isoformat() if updated_template.updated_at else None,
            "created_by": str(updated_template.created_by),
            "is_published": updated_template.is_published,
            "current_version_id": str(updated_template.current_version_id) if updated_template.current_version_id else None
        }
        
        return jsonify(response), HTTPStatus.OK
    
    except Exception as e:
        logger.error(f"Error updating template {template_id}: {str(e)}")
        return jsonify({"error": f"Failed to update template: {str(e)}"}), HTTPStatus.INTERNAL_SERVER_ERROR

@document_template_bp.route('/templates/<uuid:template_id>/fields', methods=['GET'])
@jwt_required
def get_template_fields(template_id):
    """Get the field schema for a specific template."""
    try:
        # Get template
        template = get_template_by_id(template_id)
        if not template:
            return jsonify({"error": "Template not found"}), HTTPStatus.NOT_FOUND
        
        # Get current version
        if not template.current_version_id:
            return jsonify({"error": "Template has no current version"}), HTTPStatus.NOT_FOUND
        
        current_version = DocumentTemplateVersion.get_by_id(template.current_version_id)
        if not current_version:
            return jsonify({"error": "Template version not found"}), HTTPStatus.NOT_FOUND
        
        # Return field schema
        return jsonify(current_version.field_schema), HTTPStatus.OK
    
    except Exception as e:
        logger.error(f"Error retrieving field schema for template {template_id}: {str(e)}")
        return jsonify({"error": "Failed to retrieve field schema"}), HTTPStatus.INTERNAL_SERVER_ERROR

@document_template_bp.route('/templates/<uuid:template_id>/generate', methods=['POST'])
@jwt_required
def generate_document_from_template(template_id):
    """Generate a document from a template."""
    try:
        # Get current user
        current_user_id = get_jwt_identity()
        
        # Get template
        template = get_template_by_id(template_id)
        if not template:
            return jsonify({"error": "Template not found"}), HTTPStatus.NOT_FOUND
        
        # Get request data
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), HTTPStatus.BAD_REQUEST
        
        field_values = data.get('field_values', {})
        output_format = data.get('format', 'html').lower()
        document_name = data.get('document_name')
        
        # Validate format
        if output_format not in ['html', 'pdf']:
            return jsonify({"error": "Invalid format. Must be 'html' or 'pdf'"}), HTTPStatus.BAD_REQUEST
        
        # Generate document
        document = generate_document(
            template_id=template_id,
            field_values=field_values,
            created_by=current_user_id,
            output_format=output_format,
            document_name=document_name
        )
        
        # Format response
        response = {
            "document_id": str(document.id),
            "template_id": str(document.template_id),
            "created_at": document.created_at.isoformat(),
            "created_by": str(document.created_by),
            "name": document.name
        }
        
        return jsonify(response), HTTPStatus.CREATED
    
    except ValueError as e:
        logger.error(f"Validation error when generating document: {str(e)}")
        return jsonify({"error": str(e)}), HTTPStatus.BAD_REQUEST
    
    except Exception as e:
        logger.error(f"Error generating document from template {template_id}: {str(e)}")
        return jsonify({"error": "Failed to generate document"}), HTTPStatus.INTERNAL_SERVER_ERROR

@document_template_bp.route('/documents/<uuid:document_id>', methods=['GET'])
@jwt_required
def get_generated_document(document_id):
    """Get a generated document by ID."""
    try:
        # Get current user for permission check
        current_user_id = get_jwt_identity()
        current_user = User.get_by_id(current_user_id)
        
        # Get document
        document = get_document_by_id(document_id)
        if not document:
            return jsonify({"error": "Document not found"}), HTTPStatus.NOT_FOUND
        
        # Check permissions (only creator or admin/attorney can view)
        is_creator = str(document.created_by) == str(current_user_id)
        has_permission = has_role(current_user, [RoleType.ADMIN, RoleType.ATTORNEY])
        
        if not (is_creator or has_permission):
            return jsonify({"error": "Unauthorized to view this document"}), HTTPStatus.FORBIDDEN
        
        # Format response
        response = {
            "id": str(document.id),
            "name": document.name,
            "template_id": str(document.template_id),
            "created_at": document.created_at.isoformat(),
            "created_by": str(document.created_by),
            "content": document.content if document.format == 'html' else None,
            "format": document.format
        }
        
        return jsonify(response), HTTPStatus.OK
    
    except Exception as e:
        logger.error(f"Error retrieving document {document_id}: {str(e)}")
        return jsonify({"error": "Failed to retrieve document"}), HTTPStatus.INTERNAL_SERVER_ERROR

@document_template_bp.route('/documents/<uuid:document_id>/download', methods=['GET'])
@jwt_required
def download_document(document_id):
    """Download a generated document as a PDF."""
    try:
        # Get current user for permission check
        current_user_id = get_jwt_identity()
        current_user = User.get_by_id(current_user_id)
        
        # Get document
        document = get_document_by_id(document_id)
        if not document:
            return jsonify({"error": "Document not found"}), HTTPStatus.NOT_FOUND
        
        # Check permissions (only creator or admin/attorney can download)
        is_creator = str(document.created_by) == str(current_user_id)
        has_permission = has_role(current_user, [RoleType.ADMIN, RoleType.ATTORNEY])
        
        if not (is_creator or has_permission):
            return jsonify({"error": "Unauthorized to download this document"}), HTTPStatus.FORBIDDEN
        
        # If format is HTML, convert to PDF
        if document.format == 'html':
            # This would typically use a service like WeasyPrint to convert HTML to PDF
            # For now, we'll just return the HTML content as a placeholder
            return jsonify({"error": "PDF conversion not implemented yet"}), HTTPStatus.NOT_IMPLEMENTED
        
        # Return PDF file
        filename = f"{document.name or 'document'}.pdf"
        return send_file(
            io.BytesIO(document.content),
            mimetype='application/pdf',
            as_attachment=True,
            download_name=filename
        )
    
    except Exception as e:
        logger.error(f"Error downloading document {document_id}: {str(e)}")
        return jsonify({"error": "Failed to download document"}), HTTPStatus.INTERNAL_SERVER_ERROR

@document_template_bp.route('/templates/categories', methods=['GET'])
@jwt_required
def get_available_categories():
    """Get all available template categories."""
    try:
        categories = get_template_categories()
        return jsonify(categories), HTTPStatus.OK
    
    except Exception as e:
        logger.error(f"Error retrieving template categories: {str(e)}")
        return jsonify({"error": "Failed to retrieve template categories"}), HTTPStatus.INTERNAL_SERVER_ERROR 