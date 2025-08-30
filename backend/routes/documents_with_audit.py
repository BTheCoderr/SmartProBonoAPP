from flask import Blueprint, request, jsonify, Response, current_app, send_file
from datetime import datetime
import re
from bson import ObjectId
from ..database import db, mongo
from ..models.document import Document
from ..models.user import User
from ..services.email_service import send_document_share_email
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..services.document_service import DocumentService
from werkzeug.utils import secure_filename
import os
import logging
from ..utils.auth import login_required
from ..services.notification_service import NotificationService

# Import OCR services
from ..services.ocr_service import ocr_service
from ..services.ocr_storage_service import ocr_storage_service

from ..middleware.validation import validate_json_request, validate_query_params
from ..middleware.rate_limiting import rate_limiter
from ..services.document_management_service import document_management_service
from ..services.validation_service import validation_service
from ..services.error_logging_service import error_logging_service
from ..utils.decorators import token_required
from typing import Dict, Any, List, Optional

# Import audit services
from ..services.audit_service import audit_service
from ..services.user_activity_service import user_activity_service
from ..services.data_access_service import data_access_service
from ..services.document_audit_service import document_audit_service
from ..services.performance_service import performance_service
from ..utils.audit_decorators import audit_route, security_audit, performance_audit, data_access_audit
from ..models.audit import AuditEventType, AuditSeverity

bp = Blueprint('documents', __name__, url_prefix='/api/documents')
logger = logging.getLogger(__name__)

@bp.route('/<document_id>', methods=['GET'])
@jwt_required()
@audit_route(event_type=AuditEventType.DOCUMENT_ACCESS, action="VIEW_DOCUMENT")
@security_audit(action="DOCUMENT_ACCESS")
@performance_audit(threshold_ms=1000)
@data_access_audit(resource_type="document", action="READ")
def get_document(document_id):
    """Get a document with comprehensive auditing."""
    try:
        user_id = get_jwt_identity()
        
        # Track user activity
        user_activity_service.track_page_view(
            user_id=user_id,
            page_url=f"/api/documents/{document_id}",
            page_title="Document View",
            audit_metadata={"document_id": document_id}
        )
        
        # Log data access
        data_access_service.log_data_access(
            user_id=user_id,
            resource_type="document",
            resource_id=document_id,
            action="READ",
            data_fields=["title", "content", "metadata"],
            result_count=1
        )
        
        # Get document (your existing logic)
        document = Document.query.get(document_id)
        if not document:
            return jsonify({"error": "Document not found"}), 404
        
        # Log document access
        document_audit_service.log_document_access(
            document_id=document_id,
            user_id=user_id,
            action="view",
            file_size=document.file_size if hasattr(document, 'file_size') else None,
            version=document.version if hasattr(document, 'version') else None
        )
        
        return jsonify(document.to_dict())
        
    except Exception as e:
        logger.error(f"Error getting document {document_id}: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@bp.route('/', methods=['POST'])
@jwt_required()
@audit_route(event_type=AuditEventType.DOCUMENT_ACCESS, action="CREATE_DOCUMENT")
@security_audit(action="DOCUMENT_CREATE")
@performance_audit(threshold_ms=2000)
@data_access_audit(resource_type="document", action="CREATE")
def create_document():
    """Create a document with comprehensive auditing."""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        # Track user activity
        user_activity_service.track_form_submission(
            user_id=user_id,
            form_type="document_creation",
            success=True,
            audit_metadata={"document_type": data.get('type', 'unknown')}
        )
        
        # Log data modification
        data_access_service.log_data_modification(
            user_id=user_id,
            resource_type="document",
            resource_id="new",
            action="CREATE",
            new_data=data,
            audit_metadata={"form_type": "document_creation"}
        )
        
        # Create document (your existing logic)
        document = Document(
            title=data.get('title'),
            content=data.get('content'),
            user_id=user_id,
            # ... other fields
        )
        
        db.session.add(document)
        db.session.commit()
        
        # Log document creation
        document_audit_service.log_document_access(
            document_id=document.id,
            user_id=user_id,
            action="create",
            file_size=len(data.get('content', '')) if data.get('content') else None
        )
        
        return jsonify({
            "message": "Document created successfully",
            "document": document.to_dict()
        }), 201
        
    except Exception as e:
        logger.error(f"Error creating document: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@bp.route('/<document_id>/download', methods=['GET'])
@jwt_required()
@audit_route(event_type=AuditEventType.DOCUMENT_ACCESS, action="DOWNLOAD_DOCUMENT")
@security_audit(action="DOCUMENT_DOWNLOAD")
@performance_audit(threshold_ms=1500)
@data_access_audit(resource_type="document", action="DOWNLOAD")
def download_document(document_id):
    """Download document with security auditing."""
    try:
        user_id = get_jwt_identity()
        
        # Check permissions (your existing logic)
        document = Document.query.get(document_id)
        if not document:
            # Log unauthorized access attempt
            audit_service.log_security_event(
                event_type="unauthorized_document_access",
                severity=AuditSeverity.HIGH,
                user_id=user_id,
                reason=f"Unauthorized access attempt to document {document_id}",
                blocked=True,
                response_action="deny_access"
            )
            return jsonify({"error": "Document not found"}), 404
        
        # Track user activity
        user_activity_service.track_file_download(
            user_id=user_id,
            file_name=f"document_{document_id}.pdf",
            file_type="pdf",
            page_url=f"/documents/{document_id}/download"
        )
        
        # Log document access
        document_audit_service.log_document_download(
            document_id=document_id,
            user_id=user_id,
            download_format="pdf",
            file_size=document.file_size if hasattr(document, 'file_size') else None,
            processing_time_ms=0
        )
        
        # Log data access
        data_access_service.log_data_access(
            user_id=user_id,
            resource_type="document",
            resource_id=document_id,
            action="DOWNLOAD",
            data_fields=["content", "metadata"],
            result_count=1
        )
        
        # Serve file (your existing logic)
        return send_file(document.file_path)
        
    except Exception as e:
        logger.error(f"Error downloading document {document_id}: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@bp.route('/<document_id>', methods=['PUT'])
@jwt_required()
@audit_route(event_type=AuditEventType.DOCUMENT_ACCESS, action="UPDATE_DOCUMENT")
@security_audit(action="DOCUMENT_UPDATE")
@performance_audit(threshold_ms=1500)
@data_access_audit(resource_type="document", action="UPDATE")
def update_document(document_id):
    """Update a document with comprehensive auditing."""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        # Get existing document
        document = Document.query.get(document_id)
        if not document:
            return jsonify({"error": "Document not found"}), 404
        
        # Store old data for comparison
        old_data = {
            "title": document.title,
            "content": document.content,
            # ... other fields
        }
        
        # Update document (your existing logic)
        document.title = data.get('title', document.title)
        document.content = data.get('content', document.content)
        # ... other updates
        
        db.session.commit()
        
        # Log data modification
        data_access_service.log_data_modification(
            user_id=user_id,
            resource_type="document",
            resource_id=document_id,
            action="UPDATE",
            old_data=old_data,
            new_data=data,
            changed_fields=list(data.keys())
        )
        
        # Log document modification
        document_audit_service.log_document_modification(
            document_id=document_id,
            user_id=user_id,
            modification_type="update",
            changes_made=data,
            file_size=len(data.get('content', '')) if data.get('content') else None
        )
        
        return jsonify({
            "message": "Document updated successfully",
            "document": document.to_dict()
        })
        
    except Exception as e:
        logger.error(f"Error updating document {document_id}: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@bp.route('/<document_id>', methods=['DELETE'])
@jwt_required()
@audit_route(event_type=AuditEventType.DOCUMENT_ACCESS, action="DELETE_DOCUMENT")
@security_audit(action="DOCUMENT_DELETE")
@performance_audit(threshold_ms=1000)
@data_access_audit(resource_type="document", action="DELETE")
def delete_document(document_id):
    """Delete a document with comprehensive auditing."""
    try:
        user_id = get_jwt_identity()
        
        # Get document
        document = Document.query.get(document_id)
        if not document:
            return jsonify({"error": "Document not found"}), 404
        
        # Log data deletion
        data_access_service.log_data_deletion(
            user_id=user_id,
            resource_type="document",
            resource_id=document_id,
            deletion_reason="User requested deletion",
            soft_delete=True
        )
        
        # Log document deletion
        document_audit_service.log_document_deletion(
            document_id=document_id,
            user_id=user_id,
            deletion_reason="User requested deletion",
            soft_delete=True
        )
        
        # Delete document (your existing logic)
        db.session.delete(document)
        db.session.commit()
        
        return jsonify({"message": "Document deleted successfully"})
        
    except Exception as e:
        logger.error(f"Error deleting document {document_id}: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500
