"""
Document Management API Routes
Handles document upload, download, and management operations.
"""
from flask import Blueprint, request, jsonify, send_file, current_app
from werkzeug.utils import secure_filename
import os
import logging
from backend.services.document_management_service import document_management_service
from backend.services.auth_service import require_auth, get_current_user

bp = Blueprint('document_management_api', __name__, url_prefix='/api/v1/documents')
logger = logging.getLogger(__name__)

@bp.route('/upload', methods=['POST'])
@require_auth
def upload_document():
    """Upload a new document."""
    try:
        current_user = get_current_user()
        
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'success': False, 'error': 'No file selected'}), 400
        
        # Get additional data from form
        case_id = request.form.get('case_id', type=int)
        document_type = request.form.get('document_type', 'case_document')
        description = request.form.get('description', '')
        
        # Upload document
        document = document_management_service.save_document(
            file=file,
            case_id=case_id,
            uploaded_by=current_user['id'],
            document_type=document_type
        )
        
        # Update description if provided
        if description:
            document_management_service.update_document(
                document['id'],
                {'description': description}
            )
            document['description'] = description
        
        return jsonify({
            'success': True,
            'document': document,
            'message': 'Document uploaded successfully'
        }), 201
        
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    except Exception as e:
        logger.error(f"Error uploading document: {e}")
        return jsonify({'success': False, 'error': 'Failed to upload document'}), 500

@bp.route('/case/<int:case_id>', methods=['GET'])
@require_auth
def get_case_documents(case_id):
    """Get all documents for a specific case."""
    try:
        current_user = get_current_user()
        
        # Check if user has access to this case
        # This would need to be implemented based on your access control logic
        
        documents = document_management_service.get_case_documents(case_id)
        
        return jsonify({
            'success': True,
            'documents': documents
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting case documents: {e}")
        return jsonify({'success': False, 'error': 'Failed to get documents'}), 500

@bp.route('/<int:document_id>', methods=['GET'])
@require_auth
def get_document(document_id):
    """Get a specific document."""
    try:
        current_user = get_current_user()
        
        document = document_management_service.get_document(document_id)
        if not document:
            return jsonify({'success': False, 'error': 'Document not found'}), 404
        
        return jsonify({
            'success': True,
            'document': document
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting document: {e}")
        return jsonify({'success': False, 'error': 'Failed to get document'}), 500

@bp.route('/<int:document_id>/download', methods=['GET'])
@require_auth
def download_document(document_id):
    """Download a document file."""
    try:
        current_user = get_current_user()
        
        document = document_management_service.get_document(document_id)
        if not document:
            return jsonify({'success': False, 'error': 'Document not found'}), 404
        
        file_path = document['file_url']
        if not os.path.exists(file_path):
            return jsonify({'success': False, 'error': 'File not found'}), 404
        
        return send_file(
            file_path,
            as_attachment=True,
            download_name=document['title']
        )
        
    except Exception as e:
        logger.error(f"Error downloading document: {e}")
        return jsonify({'success': False, 'error': 'Failed to download document'}), 500

@bp.route('/<int:document_id>', methods=['PUT'])
@require_auth
def update_document(document_id):
    """Update document metadata."""
    try:
        current_user = get_current_user()
        
        data = request.json
        if not data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400
        
        document = document_management_service.update_document(document_id, data)
        
        return jsonify({
            'success': True,
            'document': document,
            'message': 'Document updated successfully'
        }), 200
        
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    except Exception as e:
        logger.error(f"Error updating document: {e}")
        return jsonify({'success': False, 'error': 'Failed to update document'}), 500

@bp.route('/<int:document_id>', methods=['DELETE'])
@require_auth
def delete_document(document_id):
    """Delete a document."""
    try:
        current_user = get_current_user()
        
        success = document_management_service.delete_document(document_id)
        
        if success:
            return jsonify({
                'success': True,
                'message': 'Document deleted successfully'
            }), 200
        else:
            return jsonify({'success': False, 'error': 'Failed to delete document'}), 500
        
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    except Exception as e:
        logger.error(f"Error deleting document: {e}")
        return jsonify({'success': False, 'error': 'Failed to delete document'}), 500

@bp.route('/<int:document_id>/version', methods=['POST'])
@require_auth
def add_document_version(document_id):
    """Add a new version to an existing document."""
    try:
        current_user = get_current_user()
        
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'success': False, 'error': 'No file selected'}), 400
        
        document = document_management_service.add_document_version(document_id, file)
        
        return jsonify({
            'success': True,
            'document': document,
            'message': 'Document version added successfully'
        }), 200
        
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    except Exception as e:
        logger.error(f"Error adding document version: {e}")
        return jsonify({'success': False, 'error': 'Failed to add document version'}), 500

@bp.route('/search', methods=['GET'])
@require_auth
def search_documents():
    """Search documents."""
    try:
        current_user = get_current_user()
        
        query = request.args.get('q', '')
        case_id = request.args.get('case_id', type=int)
        document_type = request.args.get('document_type')
        
        if not query:
            return jsonify({'success': False, 'error': 'Search query required'}), 400
        
        documents = document_management_service.search_documents(
            query=query,
            case_id=case_id,
            document_type=document_type
        )
        
        return jsonify({
            'success': True,
            'documents': documents,
            'query': query
        }), 200
        
    except Exception as e:
        logger.error(f"Error searching documents: {e}")
        return jsonify({'success': False, 'error': 'Failed to search documents'}), 500

@bp.route('/statistics', methods=['GET'])
@require_auth
def get_document_statistics():
    """Get document statistics."""
    try:
        current_user = get_current_user()
        
        case_id = request.args.get('case_id', type=int)
        
        statistics = document_management_service.get_document_statistics(case_id=case_id)
        
        return jsonify({
            'success': True,
            'statistics': statistics
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting document statistics: {e}")
        return jsonify({'success': False, 'error': 'Failed to get statistics'}), 500
