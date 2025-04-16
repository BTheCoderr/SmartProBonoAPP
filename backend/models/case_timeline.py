from datetime import datetime
import uuid
from models.database import db
from sqlalchemy import Column, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship

class CaseTimelineEvent(db.Model):
    """Model for case timeline events."""
    __tablename__ = 'case_timeline_events'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    case_id = Column(String(36), ForeignKey('cases.id', ondelete='CASCADE'), nullable=False)
    event_type = Column(String(50), nullable=False)  # e.g., 'document_added', 'status_changed', 'note_added'
    title = Column(String(255), nullable=False)
    description = Column(Text)
    event_metadata = Column(Text)  # JSON string for additional event-specific data
    created_by = Column(String(36), ForeignKey('users.id'), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    event_date = Column(DateTime, nullable=False)  # When the event actually occurred

    # Relationships
    case = relationship('Case', backref=db.backref('timeline_events', lazy=True, cascade='all, delete-orphan'))
    creator = relationship('User', foreign_keys=[created_by], backref=db.backref('created_events', lazy=True))

    def to_dict(self):
        """Convert timeline event to dictionary."""
        return {
            'id': self.id,
            'case_id': self.case_id,
            'event_type': self.event_type,
            'title': self.title,
            'description': self.description,
            'event_metadata': self.event_metadata,
            'created_by': self.created_by,
            'created_at': self.created_at.isoformat(),
            'event_date': self.event_date.isoformat(),
            'creator_name': f"{self.creator.first_name} {self.creator.last_name}"
        } 