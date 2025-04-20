"""
API routes for document template management and document generation.

Routes:
- GET /api/document/templates - List all document templates
- GET /api/document/templates/<template_id> - Get a specific template
- POST /api/document/templates - Create a new template
- PUT /api/document/templates/<template_id> - Update a template
- DELETE /api/document/templates/<template_id> - Delete a template
- POST /api/document/templates/<template_id>/versions - Create a new version
- GET /api/document/templates/<template_id>/versions - List all versions
- GET /api/document/versions/<version_id> - Get a specific version
- POST /api/document/generate - Generate a document from a template
- GET /api/document/generated - List all generated documents
- GET /api/document/generated/<document_id> - Get a specific generated document
- DELETE /api/document/generated/<document_id> - Delete a generated document
- GET /api/document/templates/categories - Get all template categories
"""

import uuid
from typing import Dict, Any, List

from flask import Blueprint, jsonify, request, current_app, g, send_file
from sqlalchemy.exc import SQLAlchemyError
import io

from backend.models.document_template import DocumentTemplate, DocumentTemplateVersion, GeneratedDocument
from backend.services.document_service import DocumentService
from backend.auth.auth_middleware import authenticate_user, authorize_role
from backend.schemas.document_schemas import (
    template_schema, template_list_schema, version_schema, 
    version_list_schema, document_schema, document_list_schema
)
from backend.auth.auth_utils import login_required, role_required
from backend.utils.pagination import paginate_results
from backend.utils.validation import validate_request_json

# Blueprint for document-related routes
document_bp = Blueprint('document', __name__, url_prefix='/api/document')

# Helper function to validate document template data
def validate_template_data():
    """Validate template data from request."""
    data = request.json
    if not data:
        return None, "No data provided"
    
    # Required fields
    if not data.get('title'):
        return None, "Title is required"
    if not data.get('category'):
        return None, "Category is required"
    if not data.get('content'):
        return None, "Content is required"
    if not data.get('field_schema') or not isinstance(data.get('field_schema'), dict):
        return None, "Field schema is required and must be a JSON object"
    
    return data, None

# Routes for document templates
@document_bp.route('/templates', methods=['GET'])
@authenticate_user
def get_templates():
    """Get all document templates with optional filtering.
    
    Query parameters:
        - category: Filter by category
        - page: Page number for pagination
        - per_page: Number of items per page
    """
    category = request.args.get('category')
    
    templates = DocumentService.get_templates(
        category=category
    )
    
    return paginate_results(templates, request)

@document_bp.route('/templates/<template_id>', methods=['GET'])
@authenticate_user
def get_template(template_id):
    """Get a specific document template."""
    try:
        template_uuid = uuid.UUID(template_id)
    except ValueError:
        return jsonify({
            "success": False,
            "error": "Invalid template ID format"
        }), 400
    
    template = DocumentService.get_template_by_id(template_uuid)
    if not template:
        return jsonify({
            "success": False,
            "error": "Template not found"
        }), 404
    
    # Check if user can access this template
    if template.created_by != g.user.id and not g.user.is_admin:
        if template.is_published is not True:  # Use proper comparison for SQLAlchemy Column
            return jsonify({
                "success": False,
                "error": "Access denied"
            }), 403
    
    # Get all versions of this template
    versions = DocumentTemplateVersion.query.filter_by(template_id=template_uuid).all()
    
    template_data = template.to_dict()
    template_data["versions"] = [v.to_dict() for v in versions]
    
    return jsonify(template_data)

@document_bp.route('/templates', methods=['POST'])
@authenticate_user
@authorize_role(['admin', 'attorney'])
def create_template():
    """Create a new document template."""
    schema = {
        "type": "object",
        "required": ["title", "category", "description", "content", "field_schema"],
        "properties": {
            "title": {"type": "string"},
            "category": {"type": "string"},
            "description": {"type": "string"},
            "content": {"type": "string"},
            "field_schema": {"type": "object"}
        }
    }
    
    data = validate_request_json(schema)
    user_id = g.user.id
    
    try:
        template = DocumentService.create_template(
            title=data["title"],
            category=data["category"],
            description=data["description"],
            content=data["content"],
            field_schema=data["field_schema"],
            created_by=user_id
        )
        
        return jsonify(template.to_dict()), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@document_bp.route('/templates/<template_id>', methods=['PUT'])
@authenticate_user
def update_template(template_id):
    """Update a document template's metadata."""
    schema = {
        "type": "object",
        "properties": {
            "title": {"type": "string"},
            "category": {"type": "string"},
            "description": {"type": "string"}
        }
    }
    
    data = validate_request_json(schema)
    
    try:
        template = DocumentService.update_template(
            template_id=uuid.UUID(template_id),
            title=data.get("title"),
            category=data.get("category"),
            description=data.get("description")
        )
        
        return jsonify(template.to_dict())
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@document_bp.route('/templates/<template_id>', methods=['DELETE'])
@authenticate_user
def delete_template(template_id):
    """Delete a document template."""
    try:
        template_uuid = uuid.UUID(template_id)
    except ValueError:
        return jsonify({
            "success": False,
            "error": "Invalid template ID format"
        }), 400
    
    # Check if template exists
    template = DocumentService.get_template_by_id(template_uuid)
    if not template:
        return jsonify({
            "success": False,
            "error": "Template not found"
        }), 404
    
    # Check if user can delete this template
    if template.created_by != g.user.id and g.user.role != 'admin':
        return jsonify({
            "success": False,
            "error": "Access denied"
        }), 403
    
    success, error = DocumentService.delete_template(template_uuid)
    if not success:
        return jsonify({
            "success": False,
            "error": error
        }), 400
    
    return jsonify({
        "success": True,
        "message": "Template deleted successfully"
    }), 200

# Routes for template versions
@document_bp.route('/templates/<template_id>/versions', methods=['POST'])
@authenticate_user
def create_template_version(template_id):
    """Create a new version for an existing document template."""
    schema = {
        "type": "object",
        "required": ["content", "field_schema"],
        "properties": {
            "content": {"type": "string"},
            "field_schema": {"type": "object"}
        }
    }
    
    data = validate_request_json(schema)
    
    try:
        version = DocumentService.create_template_version(
            template_id=uuid.UUID(template_id),
            content=data["content"],
            field_schema=data["field_schema"],
            created_by=g.user.id
        )
        
        return jsonify(version.to_dict()), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@document_bp.route('/templates/<template_id>/versions', methods=['GET'])
@authenticate_user
def get_versions(template_id):
    """Get all versions for a template."""
    try:
        template_uuid = uuid.UUID(template_id)
    except ValueError:
        return jsonify({
            "success": False,
            "error": "Invalid template ID format"
        }), 400
    
    # Check if template exists
    template = DocumentService.get_template_by_id(template_uuid)
    if not template:
        return jsonify({
            "success": False,
            "error": "Template not found"
        }), 404
    
    # Check if user can view versions for this template
    if template.created_by != g.user.id and not g.user.is_admin:
        if template.is_published is not True:  # Use proper comparison for SQLAlchemy Column
            return jsonify({
                "success": False,
                "error": "Access denied"
            }), 403
    
    return jsonify({
        "success": True,
        "versions": version_list_schema.dump(template.versions)
    }), 200

@document_bp.route('/versions/<version_id>', methods=['GET'])
@authenticate_user
def get_version(version_id):
    """Get a specific template version."""
    try:
        version_uuid = uuid.UUID(version_id)
    except ValueError:
        return jsonify({
            "success": False,
            "error": "Invalid version ID format"
        }), 400
    
    version = DocumentService.get_template_version_by_id(version_uuid)
    if not version:
        return jsonify({
            "success": False,
            "error": "Version not found"
        }), 404
    
    # Check if user can view this version
    template = version.template
    if template.created_by != g.user.id and not template.is_published and g.user.role != 'admin':
        return jsonify({
            "success": False,
            "error": "Access denied"
        }), 403
    
    return jsonify({
        "success": True,
        "version": version_schema.dump(version)
    }), 200

# Routes for document generation and management
@document_bp.route('/generate', methods=['POST'])
@authenticate_user
def generate_document():
    """Generate a document from a template version."""
    schema = {
        "type": "object",
        "required": ["template_version_id", "case_id", "field_values"],
        "properties": {
            "template_version_id": {"type": "string", "format": "uuid"},
            "case_id": {"type": "string", "format": "uuid"},
            "field_values": {"type": "object"},
            "title": {"type": "string"}
        }
    }
    
    data = validate_request_json(schema)
    
    try:
        document, error = DocumentService.generate_document(
            template_version_id=uuid.UUID(data["template_version_id"]),
            case_id=uuid.UUID(data["case_id"]),
            field_values=data["field_values"],
            title=data.get("title", "Generated Document"),
            created_by=g.user.id
        )
        
        if error or document is None:
            return jsonify({"error": error or "Failed to generate document"}), 400
            
        return jsonify(document.to_dict()), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@document_bp.route('/generated', methods=['GET'])
@authenticate_user
def get_generated_documents():
    """Get all generated documents for the authenticated user."""
    case_id = request.args.get('case_id')
    
    # If case_id provided, get documents for that case
    if case_id:
        try:
            case_uuid = uuid.UUID(case_id)
        except ValueError:
            return jsonify({
                "success": False,
                "error": "Invalid case ID format"
            }), 400
        
        documents = DocumentService.get_documents_for_case(case_uuid)
    else:
        # TODO: Implement getting all documents for current user
        documents = []
    
    return jsonify({
        "success": True,
        "documents": document_list_schema.dump(documents)
    }), 200

@document_bp.route('/generated/<document_id>', methods=['GET'])
@authenticate_user
def get_generated_document(document_id):
    """Get a specific generated document."""
    try:
        document_uuid = uuid.UUID(document_id)
    except ValueError:
        return jsonify({
            "success": False,
            "error": "Invalid document ID format"
        }), 400
    
    document = DocumentService.get_document_by_id(document_uuid)
    if not document:
        return jsonify({
            "success": False,
            "error": "Document not found"
        }), 404
    
    # Check if user can view this document
    if document.created_by != g.user.id and g.user.role != 'admin':
        # If document is part of a case, check if user has access to the case
        if document.case_id is not None:  # Use proper comparison for SQLAlchemy Column
            # TODO: Check case access permission
            pass
        else:
            return jsonify({
                "success": False,
                "error": "Access denied"
            }), 403
    
    return jsonify({
        "success": True,
        "document": document_schema.dump(document)
    }), 200

@document_bp.route('/generated/<document_id>', methods=['DELETE'])
@authenticate_user
def delete_generated_document(document_id):
    """Delete a generated document."""
    try:
        document_uuid = uuid.UUID(document_id)
    except ValueError:
        return jsonify({
            "success": False,
            "error": "Invalid document ID format"
        }), 400
    
    document = DocumentService.get_document_by_id(document_uuid)
    if not document:
        return jsonify({
            "success": False,
            "error": "Document not found"
        }), 404
    
    # Check if user can delete this document
    if document.created_by != g.user.id and g.user.role != 'admin':
        return jsonify({
            "success": False,
            "error": "Access denied"
        }), 403
    
    success, error = DocumentService.delete_document(document_uuid)
    if not success:
        return jsonify({
            "success": False,
            "error": error
        }), 400
    
    return jsonify({
        "success": True,
        "message": "Document deleted successfully"
    }), 200

@document_bp.route('/templates/categories', methods=['GET'])
@authenticate_user
def get_template_categories():
    """Get all template categories."""
    # This would typically come from a database query
    # For now, return a static list
    categories = [
        "Pleadings",
        "Motions",
        "Contracts",
        "Letters",
        "Forms",
        "Other"
    ]
    
    return jsonify({
        "success": True,
        "categories": categories
    }), 200

@document_bp.route("/documents/<uuid:document_id>/download", methods=["GET"])
@login_required
def download_document(document_id: uuid.UUID):
    """Download a generated document."""
    document = GeneratedDocument.query.get_or_404(document_id)
    
    try:
        file_data = DocumentService.get_document_file(document_id)
        
        # Create an in-memory file-like object
        file_obj = io.BytesIO(file_data)
        
        # Determine file extension and MIME type based on document format
        file_extension = "pdf"  # Default
        mime_type = "application/pdf"  # Default
        
        if document.format == "docx":
            file_extension = "docx"
            mime_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        
        filename = f"{document.title.replace(' ', '_')}.{file_extension}"
        
        return send_file(
            file_obj,
            mimetype=mime_type,
            as_attachment=True,
            download_name=filename
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@document_bp.route("/case/<uuid:case_id>/documents", methods=["GET"])
@login_required
def get_case_documents(case_id: uuid.UUID):
    """Get all documents for a specific case."""
    documents = GeneratedDocument.query.filter_by(case_id=case_id).all()
    
    return paginate_results([doc.to_dict() for doc in documents], request) 