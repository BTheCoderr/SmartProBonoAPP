from datetime import datetime
from typing import Dict, List, Optional, Any
from models.database import db
from models.case import Case
from models.document import Document
from models.case_timeline import CaseTimelineEvent
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import SQLAlchemyError
from .case_document_service import CaseDocumentService
from .case_timeline_service import CaseTimelineService

class CaseStatus:
    """Enum-like class for case statuses."""
    NEW = 'new'
    IN_PROGRESS = 'in_progress'
    PENDING_REVIEW = 'pending_review'
    COMPLETED = 'completed'
    CLOSED = 'closed'
    
    @classmethod
    def get_valid_statuses(cls) -> List[str]:
        return [cls.NEW, cls.IN_PROGRESS, cls.PENDING_REVIEW, cls.COMPLETED, cls.CLOSED]

class CaseService:
    """Service for managing legal cases."""
    
    def __init__(self, session: Optional[Session] = None):
        """Initialize the service with optional session override."""
        self._session = session or db.session  # type: ignore
        self.document_service = CaseDocumentService()
        self.timeline_service = CaseTimelineService()
    
    @property
    def session(self) -> Session:
        return self._session
    
    def create_case(self, case_data: Dict[str, Any], user_id: str) -> Case:
        """Create a new case."""
        try:
            case = Case(
                title=case_data['title'],
                description=case_data.get('description'),
                case_type=case_data['case_type'],
                status=CaseStatus.NEW,
                priority=case_data.get('priority', 'medium'),
                client_id=case_data.get('client_id'),
                lawyer_id=case_data.get('lawyer_id'),
                created_by=user_id
            )
            self.session.add(case)  # type: ignore
            self.session.commit()  # type: ignore
            
            # Add initial timeline event
            self.timeline_service.add_timeline_event(
                case_id=str(case.id),
                user_id=user_id,
                event_type='case_created',
                title='Case Created',
                description=f"Case '{case.title}' was created"
            )
            
            return case
            
        except SQLAlchemyError as e:
            self.session.rollback()  # type: ignore
            raise ValueError(f"Failed to create case: {str(e)}")
    
    def update_case(self, case_id: str, update_data: Dict[str, Any], user_id: str) -> Case:
        """Update a case."""
        try:
            case = Case.query.get(case_id)
            if not case:
                raise ValueError("Case not found")
            
            # Track changes for timeline
            changes = []
            
            # Update allowed fields
            for field in ['title', 'description', 'case_type', 'priority', 'lawyer_id']:
                if field in update_data:
                    old_value = getattr(case, field)
                    new_value = update_data[field]
                    if old_value != new_value:
                        setattr(case, field, new_value)
                        changes.append(f"{field}: {old_value} -> {new_value}")
            
            # Handle status change separately
            if 'status' in update_data:
                new_status = update_data['status']
                if new_status in CaseStatus.get_valid_statuses():
                    old_status = case.status
                    case.status = new_status
                    changes.append(f"status: {old_status} -> {new_status}")
                else:
                    raise ValueError(f"Invalid status: {new_status}")
            
            if changes:
                self.session.commit()  # type: ignore
                
                # Add timeline event for the update
                self.timeline_service.add_timeline_event(
                    case_id=case_id,
                    user_id=user_id,
                    event_type='case_updated',
                    title='Case Updated',
                    description="The following changes were made:\n" + "\n".join(changes)
                )
            
            return case
            
        except SQLAlchemyError as e:
            self.session.rollback()  # type: ignore
            raise ValueError(f"Failed to update case: {str(e)}")
    
    def get_case(self, case_id: str) -> Case:
        """Get a case by ID."""
        case = Case.query.get(case_id)
        if not case:
            raise ValueError("Case not found")
        return case

    def get_cases(self, filters: Optional[Dict[str, Any]] = None) -> List[Case]:
        """Get cases with optional filters."""
        query = Case.query
        
        if filters:
            if 'status' in filters:
                query = query.filter(Case.status == filters['status'])
            if 'priority' in filters:
                query = query.filter(Case.priority == filters['priority'])
            if 'lawyer_id' in filters:
                query = query.filter(Case.lawyer_id == filters['lawyer_id'])
            if 'client_id' in filters:
                query = query.filter(Case.client_id == filters['client_id'])
        
        return query.order_by(Case.created_at.desc()).all()
    
    def add_document(self, case_id: str, user_id: str, document_data: Dict[str, Any]) -> Document:
        """Add a document to a case."""
        return self.document_service.add_document(case_id, user_id, document_data)
    
    def get_case_documents(self, case_id: str) -> List[Document]:
        """Get all documents for a case."""
        return self.document_service.get_case_documents(case_id)
    
    def add_timeline_event(self, case_id: str, user_id: str, event_data: Dict[str, Any]) -> CaseTimelineEvent:
        """Add a timeline event to a case."""
        return self.timeline_service.add_timeline_event(
            case_id=case_id,
            user_id=user_id,
            event_type=event_data['event_type'],
            title=event_data['title'],
            description=event_data.get('description'),
            metadata=event_data.get('metadata')
        )
    
    def get_case_timeline(self, case_id: str) -> List[CaseTimelineEvent]:
        """Get all timeline events for a case."""
        return self.timeline_service.get_case_timeline(case_id)
    
    def delete_case(self, case_id: str) -> bool:
        """Delete a case by ID.
        
        Args:
            case_id: The ID of the case to delete
            
        Returns:
            bool: True if the case was deleted, False if not found
        """
        try:
            case = Case.query.get(case_id)
            if not case:
                return False
                
            self.session.delete(case)
            self.session.commit()
            return True
            
        except SQLAlchemyError as e:
            self.session.rollback()
            raise ValueError(f"Failed to delete case: {str(e)}")