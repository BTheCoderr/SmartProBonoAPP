from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.user import User
from models.database import db
from models.case import Case
from models.document import Document
from datetime import datetime
import os
from werkzeug.utils import secure_filename
import logging
from typing import Any, TYPE_CHECKING
from sqlalchemy.orm import scoped_session, Session

# Configure logging
logger = logging.getLogger(__name__)

# Type hint for SQLAlchemy session
if TYPE_CHECKING:
    db.session: Any  # Type as Any to avoid linter errors with dynamic attributes

immigration_bp = Blueprint('immigration', __name__, url_prefix='/api/immigration')

ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'txt'}
MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10MB

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@immigration_bp.route('/cases', methods=['GET'])
@jwt_required()
def get_cases():
    try:
        cases = Case.query.filter_by(case_type='IMMIGRATION').all()
        return jsonify([{
            'id': case.id,
            'title': case.title,
            'description': case.description,
            'status': case.status,
            'priority': case.priority,
            'client_id': case.client_id,
            'lawyer_id': case.lawyer_id,
            'created': case.created.isoformat(),
            'updated': case.updated.isoformat(),
            'documents': [doc.to_dict() for doc in case.documents]
        } for case in cases]), 200
    except Exception as e:
        logger.error(f"Error fetching immigration cases: {str(e)}")
        return jsonify({'error': 'Failed to fetch cases'}), 500

@immigration_bp.route('/cases', methods=['POST'])
@jwt_required()
def create_case():
    try:
        data = request.get_json()
        required_fields = ['title', 'description', 'status', 'priority']
        
        # Validate required fields
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({'error': f'Missing required fields: {", ".join(missing_fields)}'}), 400
        
        # Create new case
        case = Case(
            title=data['title'],
            description=data['description'],
            case_type='IMMIGRATION',
            status=data['status'],
            priority=data['priority'],
            client_id=get_jwt_identity(),
            created=datetime.utcnow(),
            updated=datetime.utcnow()
        )
        
        db.session.add(case)
        db.session.commit()
        
        return jsonify({
            'message': 'Case created successfully',
            'case': {
                'id': case.id,
                'title': case.title,
                'description': case.description,
                'status': case.status,
                'priority': case.priority,
                'client_id': case.client_id,
                'created': case.created.isoformat(),
                'updated': case.updated.isoformat()
            }
        }), 201
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error creating immigration case: {str(e)}")
        return jsonify({'error': 'Failed to create case'}), 500

@immigration_bp.route('/cases/<case_id>', methods=['PUT'])
@jwt_required()
def update_case(case_id):
    try:
        case = Case.query.get(case_id)
        if not case:
            return jsonify({'error': 'Case not found'}), 404
            
        # Verify user has permission to update this case
        current_user_id = get_jwt_identity()
        if case.client_id != current_user_id and case.lawyer_id != current_user_id:
            return jsonify({'error': 'Unauthorized to update this case'}), 403
        
        data = request.get_json()
        allowed_fields = ['title', 'description', 'status', 'priority']
        
        # Update allowed fields
        for field in allowed_fields:
            if field in data:
                setattr(case, field, data[field])
        
        case.updated = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'message': 'Case updated successfully',
            'case': {
                'id': case.id,
                'title': case.title,
                'description': case.description,
                'status': case.status,
                'priority': case.priority,
                'client_id': case.client_id,
                'lawyer_id': case.lawyer_id,
                'created': case.created.isoformat(),
                'updated': case.updated.isoformat()
            }
        })
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error updating immigration case: {str(e)}")
        return jsonify({'error': 'Failed to update case'}), 500

@immigration_bp.route('/cases/<case_id>', methods=['DELETE'])
@jwt_required()
def delete_case(case_id):
    try:
        case = Case.query.get(case_id)
        if not case:
            return jsonify({'error': 'Case not found'}), 404
            
        # Verify user has permission to delete this case
        current_user_id = get_jwt_identity()
        if case.client_id != current_user_id and case.lawyer_id != current_user_id:
            return jsonify({'error': 'Unauthorized to delete this case'}), 403
        
        db.session.delete(case)
        db.session.commit()
        
        return jsonify({'message': 'Case deleted successfully'})
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error deleting immigration case: {str(e)}")
        return jsonify({'error': 'Failed to delete case'}), 500

@immigration_bp.route('/cases/<case_id>/documents', methods=['POST'])
@jwt_required()
def upload_document(case_id):
    try:
        case = Case.query.get(case_id)
        if not case:
            return jsonify({'error': 'Case not found'}), 404
            
        # Verify user has permission to upload documents
        current_user_id = get_jwt_identity()
        if case.client_id != current_user_id and case.lawyer_id != current_user_id:
            return jsonify({'error': 'Unauthorized to upload documents'}), 403
        
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
            
        file = request.files['file']
        if not file or not file.filename:
            return jsonify({'error': 'No file selected'}), 400
            
        if not allowed_file(file.filename):
            return jsonify({
                'error': 'Invalid file type',
                'allowed_types': list(ALLOWED_EXTENSIONS)
            }), 400
            
        if file.content_length and file.content_length > MAX_CONTENT_LENGTH:
            return jsonify({
                'error': 'File too large',
                'max_size_mb': MAX_CONTENT_LENGTH / (1024 * 1024)
            }), 400
        
        # Create documents directory if it doesn't exist
        upload_dir = os.path.join(current_app.config['UPLOAD_FOLDER'], 'immigration', case_id)
        os.makedirs(upload_dir, exist_ok=True)
        
        # Save file
        filename = secure_filename(file.filename)
        file_path = os.path.join(upload_dir, filename)
        file.save(file_path)
        
        # Create document record
        document = Document(
            title=filename,
            description=request.form.get('description', ''),
            document_type='IMMIGRATION',
            status='UPLOADED',
            case_id=case_id,
            created_by=current_user_id,
            file_path=file_path,
            file_size=os.path.getsize(file_path),
            file_type=filename.rsplit('.', 1)[1].lower()
        )
        
        db.session.add(document)
        db.session.commit()
        
        return jsonify({
            'message': 'Document uploaded successfully',
            'document': document.to_dict()
        })
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error uploading document: {str(e)}")
        return jsonify({'error': 'Failed to upload document'}), 500

@immigration_bp.route('/cases/<case_id>/documents', methods=['GET'])
@jwt_required()
def get_documents(case_id):
    try:
        case = Case.query.get(case_id)
        if not case:
            return jsonify({'error': 'Case not found'}), 404
            
        # Verify user has permission to view documents
        current_user_id = get_jwt_identity()
        if case.client_id != current_user_id and case.lawyer_id != current_user_id:
            return jsonify({'error': 'Unauthorized to view documents'}), 403
        
        return jsonify([doc.to_dict() for doc in case.documents])
    except Exception as e:
        logger.error(f"Error fetching documents: {str(e)}")
        return jsonify({'error': 'Failed to fetch documents'}), 500 