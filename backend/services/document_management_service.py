"""
Document Management Service for SmartProBono
Handles document upload, storage, versioning, and case association.
"""
import os
import uuid
from datetime import datetime
from werkzeug.utils import secure_filename
from flask import current_app
from backend.database import db
from backend.models import Document, Case, User
import logging

logger = logging.getLogger(__name__)

class DocumentManagementService:
    """Service for managing legal documents."""
    
    def __init__(self):
        self.allowed_extensions = {
            'pdf', 'doc', 'docx', 'txt', 'rtf', 'jpg', 'jpeg', 'png', 'gif',
            'mp4', 'mp3', 'wav', 'avi', 'mov', 'zip', 'rar'
        }
        self.max_file_size = 50 * 1024 * 1024  # 50MB
    
    def allowed_file(self, filename):
        """Check if file extension is allowed."""
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in self.allowed_extensions
    
    def generate_unique_filename(self, original_filename):
        """Generate a unique filename to prevent conflicts."""
        ext = original_filename.rsplit('.', 1)[1].lower()
        unique_id = str(uuid.uuid4())
        return f"{unique_id}.{ext}"
    
    def save_document(self, file, case_id=None, uploaded_by=None, document_type='case_document'):
        """Save uploaded document to filesystem and database."""
        try:
            if not file or not self.allowed_file(file.filename):
                raise ValueError("Invalid file type or no file provided")
            
            if len(file.read()) > self.max_file_size:
                raise ValueError("File too large")
            
            file.seek(0)  # Reset file pointer
            
            # Generate secure filename
            original_filename = secure_filename(file.filename)
            unique_filename = self.generate_unique_filename(original_filename)
            
            # Create upload directory if it doesn't exist
            upload_dir = os.path.join(current_app.config.get('UPLOAD_FOLDER', 'uploads'), str(case_id) if case_id else 'general')
            os.makedirs(upload_dir, exist_ok=True)
            
            # Save file
            file_path = os.path.join(upload_dir, unique_filename)
            file.save(file_path)
            
            # Create database record
            document = Document(
                title=original_filename,
                file_url=file_path,
                file_type=original_filename.rsplit('.', 1)[1].lower(),
                document_type=document_type,
                uploaded_by=uploaded_by,
                case_id=case_id,
                description=f"Uploaded document: {original_filename}"
            )
            
            db.session.add(document)
            db.session.commit()
            
            return document.to_dict()
            
        except Exception as e:
            logger.error(f"Error saving document: {e}")
            db.session.rollback()
            raise e
    
    def get_case_documents(self, case_id):
        """Get all documents for a specific case."""
        try:
            documents = Document.query.filter_by(case_id=case_id).all()
            return [doc.to_dict() for doc in documents]
        except Exception as e:
            logger.error(f"Error getting case documents: {e}")
            raise e
    
    def get_document(self, document_id):
        """Get a specific document by ID."""
        try:
            document = Document.query.get(document_id)
            if not document:
                return None
            return document.to_dict()
        except Exception as e:
            logger.error(f"Error getting document: {e}")
            raise e
    
    def update_document(self, document_id, update_data):
        """Update document metadata."""
        try:
            document = Document.query.get(document_id)
            if not document:
                raise ValueError("Document not found")
            
            # Update allowed fields
            allowed_fields = ['title', 'description', 'document_type']
            for field in allowed_fields:
                if field in update_data:
                    setattr(document, field, update_data[field])
            
            document.updated_at = datetime.utcnow()
            db.session.commit()
            
            return document.to_dict()
        except Exception as e:
            logger.error(f"Error updating document: {e}")
            db.session.rollback()
            raise e
    
    def delete_document(self, document_id):
        """Delete document from database and filesystem."""
        try:
            document = Document.query.get(document_id)
            if not document:
                raise ValueError("Document not found")
            
            # Delete file from filesystem
            if document.file_url and os.path.exists(document.file_url):
                os.remove(document.file_url)
            
            # Delete from database
            db.session.delete(document)
            db.session.commit()
            
            return True
        except Exception as e:
            logger.error(f"Error deleting document: {e}")
            db.session.rollback()
            raise e
    
    def add_document_version(self, document_id, new_file):
        """Add a new version to an existing document."""
        try:
            document = Document.query.get(document_id)
            if not document:
                raise ValueError("Document not found")
            
            if not self.allowed_file(new_file.filename):
                raise ValueError("Invalid file type")
            
            # Generate new filename for version
            original_filename = secure_filename(new_file.filename)
            unique_filename = self.generate_unique_filename(original_filename)
            
            # Save new version
            upload_dir = os.path.dirname(document.file_url)
            new_file_path = os.path.join(upload_dir, unique_filename)
            new_file.save(new_file_path)
            
            # Update document record
            old_file_path = document.file_url
            document.file_url = new_file_path
            document.updated_at = datetime.utcnow()
            
            # Add to version history
            version_history = document.history or []
            version_history.append({
                'version': len(version_history) + 1,
                'file_path': old_file_path,
                'uploaded_at': datetime.utcnow().isoformat(),
                'uploaded_by': document.uploaded_by
            })
            document.history = version_history
            
            db.session.commit()
            
            # Delete old file
            if os.path.exists(old_file_path):
                os.remove(old_file_path)
            
            return document.to_dict()
        except Exception as e:
            logger.error(f"Error adding document version: {e}")
            db.session.rollback()
            raise e
    
    def search_documents(self, query, case_id=None, document_type=None):
        """Search documents by title, description, or content."""
        try:
            search_query = Document.query
            
            if case_id:
                search_query = search_query.filter_by(case_id=case_id)
            
            if document_type:
                search_query = search_query.filter_by(document_type=document_type)
            
            # Search in title and description
            search_query = search_query.filter(
                db.or_(
                    Document.title.ilike(f'%{query}%'),
                    Document.description.ilike(f'%{query}%')
                )
            )
            
            documents = search_query.all()
            return [doc.to_dict() for doc in documents]
        except Exception as e:
            logger.error(f"Error searching documents: {e}")
            raise e
    
    def get_document_statistics(self, case_id=None):
        """Get document statistics for a case or overall."""
        try:
            query = Document.query
            if case_id:
                query = query.filter_by(case_id=case_id)
            
            total_documents = query.count()
            
            # Count by document type
            type_counts = {}
            for doc_type in ['case_document', 'contract', 'evidence', 'correspondence', 'other']:
                count = query.filter_by(document_type=doc_type).count()
                if count > 0:
                    type_counts[doc_type] = count
            
            # Get recent uploads
            recent_uploads = query.order_by(desc(Document.created_at)).limit(5).all()
            
            return {
                'total_documents': total_documents,
                'type_counts': type_counts,
                'recent_uploads': [doc.to_dict() for doc in recent_uploads]
            }
        except Exception as e:
            logger.error(f"Error getting document statistics: {e}")
            raise e

# Create singleton instance
document_management_service = DocumentManagementService()
