"""
Document Collaboration API Routes
Provides endpoints for real-time document collaboration
"""

from flask import Blueprint, request, jsonify
from datetime import datetime
try:
    from database import get_db_session
except ImportError:
    from database import get_db_session
import logging
import uuid

logger = logging.getLogger(__name__)

bp = Blueprint('document_collaboration', __name__)

# In-memory storage for demo purposes - in production, use a database
documents = {}
document_collaborators = {}
document_versions = {}

@bp.route('/documents', methods=['POST'])
def create_document():
    """Create a new collaborative document"""
    try:
        data = request.get_json()
        
        if not data or 'title' not in data:
            return jsonify({
                'error': 'Missing required field: title',
                'success': False
            }), 400
        
        document_id = str(uuid.uuid4())
        document = {
            'id': document_id,
            'title': data['title'],
            'content': data.get('content', ''),
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat(),
            'created_by': data.get('user_id', 'anonymous'),
            'version': 1,
            'is_public': data.get('is_public', False),
            'permissions': data.get('permissions', {})
        }
        
        documents[document_id] = document
        document_collaborators[document_id] = []
        document_versions[document_id] = [{
            'version': 1,
            'content': document['content'],
            'timestamp': document['created_at'],
            'author': document['created_by']
        }]
        
        return jsonify({
            'success': True,
            'document': document
        }), 201
        
    except Exception as e:
        logger.error(f"Error creating document: {e}")
        return jsonify({
            'error': f'Failed to create document: {str(e)}',
            'success': False
        }), 500

@bp.route('/documents/<document_id>', methods=['GET'])
def get_document(document_id):
    """Get a document by ID"""
    try:
        if document_id not in documents:
            return jsonify({
                'error': 'Document not found',
                'success': False
            }), 404
        
        document = documents[document_id]
        collaborators = document_collaborators.get(document_id, [])
        
        return jsonify({
            'success': True,
            'document': document,
            'collaborators': collaborators
        })
        
    except Exception as e:
        logger.error(f"Error getting document: {e}")
        return jsonify({
            'error': f'Failed to get document: {str(e)}',
            'success': False
        }), 500

@bp.route('/documents/<document_id>', methods=['PUT'])
def update_document(document_id):
    """Update a document"""
    try:
        if document_id not in documents:
            return jsonify({
                'error': 'Document not found',
                'success': False
            }), 404
        
        data = request.get_json()
        
        if not data:
            return jsonify({
                'error': 'No data provided',
                'success': False
            }), 400
        
        document = documents[document_id]
        
        # Update document
        if 'content' in data:
            document['content'] = data['content']
            document['version'] += 1
            document['updated_at'] = datetime.now().isoformat()
            
            # Add to version history
            if document_id not in document_versions:
                document_versions[document_id] = []
            
            document_versions[document_id].append({
                'version': document['version'],
                'content': data['content'],
                'timestamp': document['updated_at'],
                'author': data.get('author', 'anonymous')
            })
        
        if 'title' in data:
            document['title'] = data['title']
        
        documents[document_id] = document
        
        return jsonify({
            'success': True,
            'document': document
        })
        
    except Exception as e:
        logger.error(f"Error updating document: {e}")
        return jsonify({
            'error': f'Failed to update document: {str(e)}',
            'success': False
        }), 500

@bp.route('/documents/<document_id>/share', methods=['POST'])
def share_document(document_id):
    """Share a document with collaborators"""
    try:
        if document_id not in documents:
            return jsonify({
                'error': 'Document not found',
                'success': False
            }), 404
        
        data = request.get_json()
        
        if not data or 'email' not in data:
            return jsonify({
                'error': 'Missing required field: email',
                'success': False
            }), 400
        
        email = data['email']
        permissions = data.get('permissions', 'view')
        
        # Add collaborator
        if document_id not in document_collaborators:
            document_collaborators[document_id] = []
        
        collaborator = {
            'id': str(uuid.uuid4()),
            'email': email,
            'permissions': permissions,
            'added_at': datetime.now().isoformat(),
            'added_by': data.get('added_by', 'anonymous')
        }
        
        document_collaborators[document_id].append(collaborator)
        
        return jsonify({
            'success': True,
            'collaborator': collaborator,
            'message': f'Document shared with {email}'
        })
        
    except Exception as e:
        logger.error(f"Error sharing document: {e}")
        return jsonify({
            'error': f'Failed to share document: {str(e)}',
            'success': False
        }), 500

@bp.route('/documents/<document_id>/collaborators', methods=['GET'])
def get_document_collaborators(document_id):
    """Get document collaborators"""
    try:
        if document_id not in documents:
            return jsonify({
                'error': 'Document not found',
                'success': False
            }), 404
        
        collaborators = document_collaborators.get(document_id, [])
        
        return jsonify({
            'success': True,
            'collaborators': collaborators
        })
        
    except Exception as e:
        logger.error(f"Error getting collaborators: {e}")
        return jsonify({
            'error': f'Failed to get collaborators: {str(e)}',
            'success': False
        }), 500

@bp.route('/documents/<document_id>/versions', methods=['GET'])
def get_document_versions(document_id):
    """Get document version history"""
    try:
        if document_id not in documents:
            return jsonify({
                'error': 'Document not found',
                'success': False
            }), 404
        
        versions = document_versions.get(document_id, [])
        
        return jsonify({
            'success': True,
            'versions': versions
        })
        
    except Exception as e:
        logger.error(f"Error getting document versions: {e}")
        return jsonify({
            'error': f'Failed to get document versions: {str(e)}',
            'success': False
        }), 500

@bp.route('/documents/<document_id>/versions/<int:version>', methods=['GET'])
def get_document_version(document_id, version):
    """Get a specific document version"""
    try:
        if document_id not in documents:
            return jsonify({
                'error': 'Document not found',
                'success': False
            }), 404
        
        versions = document_versions.get(document_id, [])
        version_data = next((v for v in versions if v['version'] == version), None)
        
        if not version_data:
            return jsonify({
                'error': 'Version not found',
                'success': False
            }), 404
        
        return jsonify({
            'success': True,
            'version': version_data
        })
        
    except Exception as e:
        logger.error(f"Error getting document version: {e}")
        return jsonify({
            'error': f'Failed to get document version: {str(e)}',
            'success': False
        }), 500

@bp.route('/documents/<document_id>/restore', methods=['POST'])
def restore_document_version(document_id):
    """Restore document to a specific version"""
    try:
        if document_id not in documents:
            return jsonify({
                'error': 'Document not found',
                'success': False
            }), 404
        
        data = request.get_json()
        
        if not data or 'version' not in data:
            return jsonify({
                'error': 'Missing required field: version',
                'success': False
            }), 400
        
        target_version = data['version']
        versions = document_versions.get(document_id, [])
        version_data = next((v for v in versions if v['version'] == target_version), None)
        
        if not version_data:
            return jsonify({
                'error': 'Version not found',
                'success': False
            }), 404
        
        # Restore document
        document = documents[document_id]
        document['content'] = version_data['content']
        document['version'] += 1
        document['updated_at'] = datetime.now().isoformat()
        
        # Add restoration to version history
        document_versions[document_id].append({
            'version': document['version'],
            'content': version_data['content'],
            'timestamp': document['updated_at'],
            'author': data.get('author', 'anonymous'),
            'restored_from': target_version
        })
        
        documents[document_id] = document
        
        return jsonify({
            'success': True,
            'document': document,
            'message': f'Document restored to version {target_version}'
        })
        
    except Exception as e:
        logger.error(f"Error restoring document version: {e}")
        return jsonify({
            'error': f'Failed to restore document version: {str(e)}',
            'success': False
        }), 500

@bp.route('/documents/<document_id>/comments', methods=['POST'])
def add_document_comment(document_id):
    """Add a comment to a document"""
    try:
        if document_id not in documents:
            return jsonify({
                'error': 'Document not found',
                'success': False
            }), 404
        
        data = request.get_json()
        
        if not data or 'comment' not in data:
            return jsonify({
                'error': 'Missing required field: comment',
                'success': False
            }), 400
        
        comment = {
            'id': str(uuid.uuid4()),
            'document_id': document_id,
            'comment': data['comment'],
            'author': data.get('author', 'anonymous'),
            'timestamp': datetime.now().isoformat(),
            'position': data.get('position', 0),
            'resolved': False
        }
        
        # In production, store comments in database
        # For now, we'll just return success
        
        return jsonify({
            'success': True,
            'comment': comment,
            'message': 'Comment added successfully'
        })
        
    except Exception as e:
        logger.error(f"Error adding comment: {e}")
        return jsonify({
            'error': f'Failed to add comment: {str(e)}',
            'success': False
        }), 500

@bp.route('/documents/<document_id>/export', methods=['GET'])
def export_document(document_id):
    """Export document in various formats"""
    try:
        if document_id not in documents:
            return jsonify({
                'error': 'Document not found',
                'success': False
            }), 404
        
        document = documents[document_id]
        format_type = request.args.get('format', 'txt')
        
        if format_type == 'txt':
            return jsonify({
                'success': True,
                'content': document['content'],
                'filename': f"{document['title']}.txt",
                'mime_type': 'text/plain'
            })
        elif format_type == 'json':
            return jsonify({
                'success': True,
                'document': document,
                'filename': f"{document['title']}.json",
                'mime_type': 'application/json'
            })
        else:
            return jsonify({
                'error': 'Unsupported format',
                'success': False
            }), 400
        
    except Exception as e:
        logger.error(f"Error exporting document: {e}")
        return jsonify({
            'error': f'Failed to export document: {str(e)}',
            'success': False
        }), 500

@bp.route('/documents', methods=['GET'])
def list_documents():
    """List all documents for a user"""
    try:
        user_id = request.args.get('user_id')
        
        if not user_id:
            return jsonify({
                'error': 'Missing required parameter: user_id',
                'success': False
            }), 400
        
        # Filter documents by user (created by or collaborated on)
        user_documents = []
        
        for doc_id, document in documents.items():
            if (document['created_by'] == user_id or 
                any(collab['email'] == user_id for collab in document_collaborators.get(doc_id, []))):
                user_documents.append(document)
        
        return jsonify({
            'success': True,
            'documents': user_documents,
            'total': len(user_documents)
        })
        
    except Exception as e:
        logger.error(f"Error listing documents: {e}")
        return jsonify({
            'error': f'Failed to list documents: {str(e)}',
            'success': False
        }), 500
