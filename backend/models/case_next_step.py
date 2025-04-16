from datetime import datetime
import uuid
from models.database import db
from sqlalchemy import Column, String, DateTime, Boolean, Text, ForeignKey
from sqlalchemy.orm import relationship

class CaseNextStep(db.Model):
    """Model for case next steps/tasks."""
    __tablename__ = 'case_next_steps'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    case_id = Column(String(36), ForeignKey('cases.id', ondelete='CASCADE'), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    due_date = Column(DateTime)
    completed = Column(Boolean, default=False)
    completed_at = Column(DateTime)
    completed_by = Column(String(36), ForeignKey('users.id'))
    created_by = Column(String(36), ForeignKey('users.id'), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    case = relationship('Case', backref=relationship('next_steps', lazy=True, cascade='all, delete-orphan'))
    creator = relationship('User', foreign_keys=[created_by], backref=relationship('created_steps', lazy=True))
    completer = relationship('User', foreign_keys=[completed_by], backref=relationship('completed_steps', lazy=True))

    def to_dict(self):
        """Convert next step to dictionary."""
        return {
            'id': self.id,
            'case_id': self.case_id,
            'title': self.title,
            'description': self.description,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'completed': self.completed,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'completed_by': self.completed_by,
            'created_by': self.created_by,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'creator_name': f"{self.creator.first_name} {self.creator.last_name}",
            'completer_name': f"{self.completer.first_name} {self.completer.last_name}" if self.completer else None
        } 