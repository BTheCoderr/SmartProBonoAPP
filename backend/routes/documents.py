from flask import Blueprint, request, jsonify, Response
from datetime import datetime
from models.database import db
from models.document import Document
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from typing import Dict, Any, List, Optional, Union, Tuple

documents_bp = Blueprint('documents', __name__, url_prefix='/api/documents')

@documents_bp.route('/<document_id>', methods=['GET'])
def get_document(document_id: str) -> Union[Response, Tuple[Response, int]]:
    try:
        document = Document.query.get(document_id)
        if not document:
            return jsonify({'error': 'Document not found'}), 404
            
        return jsonify(document.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@documents_bp.route('/<document_id>', methods=['PUT'])
def update_document(document_id: str) -> Union[Response, Tuple[Response, int]]:
    try:
        data = request.get_json()
        document = Document.query.get(document_id)
        if not document:
            return jsonify({'error': 'Document not found'}), 404
            
        # Add current version to history if content changed
        if 'content' in data and data['content'] != document.content:
            history_entry = {
                'content': document.content,
                'timestamp': datetime.utcnow(),
                'version': len(document.history) + 1 if document.history else 1
            }
            document.history.append(history_entry)
            
        # Update document fields
        for key, value in data.items():
            if hasattr(document, key) and key != 'history':
                setattr(document, key, value)
        
        document.updated = datetime.utcnow()
        
        session: Session = db.session  # type: ignore
        try:
            session.commit()
        except SQLAlchemyError:
            session.rollback()
            return jsonify({'error': 'Failed to update document'}), 500
            
        return jsonify(document.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@documents_bp.route('/', methods=['POST'])
def create_document() -> Union[Response, Tuple[Response, int]]:
    try:
        data = request.get_json()
        required_fields = ['title', 'content', 'type']
        
        # Validate required fields
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
                
        # Create new document
        document = Document(
            title=data['title'],
            content=data['content'],
            document_type=data['type'],
            created=datetime.utcnow(),
            updated=datetime.utcnow(),
            history=[]
        )
        
        session: Session = db.session  # type: ignore
        try:
            session.add(document)
            session.commit()
        except SQLAlchemyError:
            session.rollback()
            return jsonify({'error': 'Failed to create document'}), 500
        
        return jsonify(document.to_dict()), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@documents_bp.route('/<document_id>/versions', methods=['GET'])
def get_document_versions(document_id: str) -> Union[Response, Tuple[Response, int]]:
    try:
        document = Document.query.get(document_id)
        if not document:
            return jsonify({'error': 'Document not found'}), 404
            
        versions = document.history or []
        # Add current version
        versions.append({
            'content': document.content,
            'timestamp': document.updated,
            'version': len(versions) + 1,
            'isCurrent': True
        })
        
        return jsonify(versions)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@documents_bp.route('/<document_id>/versions/<int:version>', methods=['POST'])
def revert_to_version(document_id: str, version: int) -> Union[Response, Tuple[Response, int]]:
    try:
        document = Document.query.get(document_id)
        if not document:
            return jsonify({'error': 'Document not found'}), 404
            
        history = document.history or []
        if version < 1 or version > len(history):
            return jsonify({'error': 'Invalid version number'}), 400
            
        # Get the content from the specified version
        target_version = history[version - 1]
        
        # Add current version to history
        history_entry = {
            'content': document.content,
            'timestamp': datetime.utcnow(),
            'version': len(history) + 1
        }
        document.history.append(history_entry)
        
        # Update document with old version's content
        document.content = target_version['content']
        document.updated = datetime.utcnow()
        
        session: Session = db.session  # type: ignore
        try:
            session.commit()
        except SQLAlchemyError:
            session.rollback()
            return jsonify({'error': 'Failed to revert document'}), 500
            
        return jsonify({'message': 'Document reverted successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@documents_bp.route('/<document_id>/share', methods=['POST'])
def share_document(document_id: str) -> Union[Response, Tuple[Response, int]]:
    try:
        data = request.get_json()
        if 'users' not in data:
            return jsonify({'error': 'Missing users to share with'}), 400
            
        document = Document.query.get(document_id)
        if not document:
            return jsonify({'error': 'Document not found'}), 404
            
        # Update shared users
        document.shared_with = list(set(document.shared_with + data['users']))
        
        session: Session = db.session  # type: ignore
        try:
            session.commit()
        except SQLAlchemyError:
            session.rollback()
            return jsonify({'error': 'Failed to share document'}), 500
            
        return jsonify({'message': 'Document shared successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500 