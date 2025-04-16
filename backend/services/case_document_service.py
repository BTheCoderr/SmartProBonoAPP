from datetime import datetime
from typing import Dict, List, Optional, Any, cast
from models.database import db, DatabaseConfig
from models.case import Case
from models.document import Document
from models.case_timeline import CaseTimelineEvent
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import SQLAlchemyError
import json

class CaseDocumentService:
    """Service for managing case documents and timeline events."""
    
    @staticmethod
    def add_document(case_id: str, user_id: str, document_data: Dict[str, Any]) -> Document:
        """Add a document to a case."""
        session = cast(Session, db.session)
        try:
            # Convert metadata to JSON string if present
            metadata = json.dumps(document_data.get('metadata', {})) if document_data.get('metadata') else None
            
            document = Document(
                case_id=case_id,
                title=document_data['title'],
                document_type=document_data['document_type'],
                file_path=document_data['file_path'],
                created_by=user_id,
                metadata=metadata
            )
            session.add(document)
            
            # Create timeline event for document addition
            timeline_event = CaseTimelineEvent(
                case_id=case_id,
                event_type='document_added',
                title=f"Document added: {document_data['title']}",
                description=f"Document of type {document_data['document_type']} was added to the case",
                created_by=user_id,
                event_date=datetime.utcnow()
            )
            session.add(timeline_event)
            
            session.commit()
            return document
            
        except SQLAlchemyError as e:
            session.rollback()
            raise ValueError(f"Failed to add document: {str(e)}")
    
    @staticmethod
    def get_case_documents(case_id: str) -> List[Document]:
        """Get all documents for a case."""
        return Document.query.filter_by(case_id=case_id).all()
    
    @staticmethod
    def update_document(document_id: str, user_id: str, update_data: Dict[str, Any]) -> Document:
        """Update a document's metadata."""
        session = cast(Session, db.session)
        try:
            document = Document.query.get(document_id)
            if not document:
                raise ValueError("Document not found")
            
            # Update allowed fields
            for field in ['title', 'document_type']:
                if field in update_data:
                    setattr(document, field, update_data[field])
            
            # Handle metadata separately to ensure proper JSON serialization
            if 'metadata' in update_data:
                document.metadata = json.dumps(update_data['metadata'])
            
            # Create timeline event for document update
            timeline_event = CaseTimelineEvent(
                case_id=document.case_id,
                event_type='document_updated',
                title=f"Document updated: {document.title}",
                description="Document metadata was updated",
                created_by=user_id,
                event_date=datetime.utcnow()
            )
            session.add(timeline_event)
            
            session.commit()
            return document
            
        except SQLAlchemyError as e:
            session.rollback()
            raise ValueError(f"Failed to update document: {str(e)}")
    
    @staticmethod
    def delete_document(document_id: str, user_id: str) -> None:
        """Delete a document from a case."""
        session = cast(Session, db.session)
        try:
            document = Document.query.get(document_id)
            if not document:
                raise ValueError("Document not found")
            
            case_id = document.case_id
            title = document.title
            
            session.delete(document)
            
            # Create timeline event for document deletion
            timeline_event = CaseTimelineEvent(
                case_id=case_id,
                event_type='document_deleted',
                title=f"Document deleted: {title}",
                description="Document was removed from the case",
                created_by=user_id,
                event_date=datetime.utcnow()
            )
            session.add(timeline_event)
            
            session.commit()
            
        except SQLAlchemyError as e:
            session.rollback()
            raise ValueError(f"Failed to delete document: {str(e)}") 