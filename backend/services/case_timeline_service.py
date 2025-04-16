from datetime import datetime
from typing import Dict, List, Optional, Any, cast
from models.database import db
from models.case import Case
from models.case_timeline import CaseTimelineEvent
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import SQLAlchemyError
import json

class CaseTimelineService:
    """Service for managing case timeline events."""
    
    @staticmethod
    def add_timeline_event(
        case_id: str,
        user_id: str,
        event_type: str,
        title: str,
        description: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> CaseTimelineEvent:
        """Add a timeline event to a case."""
        session = cast(Session, db.session)
        try:
            # Convert metadata to JSON string if present
            metadata_json = json.dumps(metadata) if metadata else None
            
            event = CaseTimelineEvent(
                case_id=case_id,
                event_type=event_type,
                title=title,
                description=description,
                created_by=user_id,
                event_date=datetime.utcnow(),
                metadata=metadata_json
            )
            session.add(event)
            session.commit()
            return event
            
        except SQLAlchemyError as e:
            session.rollback()
            raise ValueError(f"Failed to add timeline event: {str(e)}")
    
    @staticmethod
    def get_case_timeline(case_id: str) -> List[CaseTimelineEvent]:
        """Get all timeline events for a case, ordered by event date."""
        return CaseTimelineEvent.query.filter_by(case_id=case_id)\
            .order_by(CaseTimelineEvent.event_date.desc())\
            .all()
    
    @staticmethod
    def update_timeline_event(
        event_id: str,
        user_id: str,
        update_data: Dict[str, Any]
    ) -> CaseTimelineEvent:
        """Update a timeline event."""
        session = cast(Session, db.session)
        try:
            event = CaseTimelineEvent.query.get(event_id)
            if not event:
                raise ValueError("Timeline event not found")
            
            # Update allowed fields
            for field in ['title', 'description']:
                if field in update_data:
                    setattr(event, field, update_data[field])
            
            # Handle metadata separately to ensure proper JSON serialization
            if 'metadata' in update_data:
                current_metadata = json.loads(event.metadata) if event.metadata else {}
                current_metadata.update(update_data['metadata'])
                event.metadata = json.dumps(current_metadata)
            
            # Add update tracking
            update_metadata = {
                'last_updated': {
                    'timestamp': datetime.utcnow().isoformat(),
                    'updated_by': user_id
                }
            }
            current_metadata = json.loads(event.metadata) if event.metadata else {}
            current_metadata.update(update_metadata)
            event.metadata = json.dumps(current_metadata)
            
            session.commit()
            return event
            
        except SQLAlchemyError as e:
            session.rollback()
            raise ValueError(f"Failed to update timeline event: {str(e)}")
    
    @staticmethod
    def delete_timeline_event(event_id: str) -> None:
        """Delete a timeline event."""
        session = cast(Session, db.session)
        try:
            event = CaseTimelineEvent.query.get(event_id)
            if not event:
                raise ValueError("Timeline event not found")
            
            session.delete(event)
            session.commit()
            
        except SQLAlchemyError as e:
            session.rollback()
            raise ValueError(f"Failed to delete timeline event: {str(e)}")
    
    @staticmethod
    def get_timeline_events_by_type(
        case_id: str,
        event_type: str
    ) -> List[CaseTimelineEvent]:
        """Get timeline events of a specific type for a case."""
        return CaseTimelineEvent.query.filter_by(
            case_id=case_id,
            event_type=event_type
        ).order_by(CaseTimelineEvent.event_date.desc()).all() 