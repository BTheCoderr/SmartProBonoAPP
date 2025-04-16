from datetime import datetime
from typing import Optional
from config.database import db, BaseModel
import uuid

class Document(BaseModel):
    """Document model representing legal documents in the system."""
    __tablename__ = 'documents'

    id: str = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title: str = db.Column(db.String(255), nullable=False)
    description: Optional[str] = db.Column(db.Text)
    document_type: str = db.Column(db.String(50), nullable=False)  # LEGAL_FORM, EVIDENCE, etc.
    status: str = db.Column(db.String(50), nullable=False)  # DRAFT, IN_REVIEW, FINAL, etc.
    
    # Foreign keys
    case_id: str = db.Column(db.String(36), db.ForeignKey('cases.id'), nullable=False)
    created_by: str = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    
    # File storage fields
    file_path: Optional[str] = db.Column(db.String(255))
    file_size: Optional[int] = db.Column(db.Integer)
    file_type: Optional[str] = db.Column(db.String(50))
    
    # Timestamps
    created: datetime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated: datetime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    creator = db.relationship('User', backref=db.backref('created_documents', lazy=True))

    def __repr__(self) -> str:
        return f'<Document {self.id}: {self.title}>'

    def to_dict(self) -> dict:
        """Convert document to dictionary."""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'document_type': self.document_type,
            'status': self.status,
            'case_id': self.case_id,
            'created_by': self.created_by,
            'file_path': self.file_path,
            'file_size': self.file_size,
            'file_type': self.file_type,
            'created': self.created.isoformat(),
            'updated': self.updated.isoformat(),
            'creator': {
                'id': self.creator.id,
                'name': f"{self.creator.first_name} {self.creator.last_name}"
            }
        } 