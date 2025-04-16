from datetime import datetime
import uuid
from models.database import db
from sqlalchemy import Column, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship

class CaseDocument(db.Model):
    """Model for case documents."""
    __tablename__ = 'case_documents'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    case_id = Column(String(36), ForeignKey('cases.id', ondelete='CASCADE'), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    file_path = Column(String(512), nullable=False)  # Path to the stored document
    file_type = Column(String(50), nullable=False)   # e.g., 'pdf', 'docx', etc.
    file_size = Column(String(20))                   # Size in bytes
    created_by = Column(String(36), ForeignKey('users.id'), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    case = relationship('Case', backref=relationship('documents', lazy=True, cascade='all, delete-orphan'))
    creator = relationship('User', foreign_keys=[created_by], backref=relationship('uploaded_documents', lazy=True))

    def to_dict(self):
        """Convert document to dictionary."""
        return {
            'id': self.id,
            'case_id': self.case_id,
            'title': self.title,
            'description': self.description,
            'file_path': self.file_path,
            'file_type': self.file_type,
            'file_size': self.file_size,
            'created_by': self.created_by,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'creator_name': f"{self.creator.first_name} {self.creator.last_name}"
        } 