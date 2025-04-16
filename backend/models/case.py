from datetime import datetime
from typing import Optional, List
from config.database import db, BaseModel
import uuid

class Case(BaseModel):
    """Case model representing legal cases in the system."""
    __tablename__ = 'cases'

    id: str = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title: str = db.Column(db.String(255), nullable=False)
    description: Optional[str] = db.Column(db.Text)
    case_type: str = db.Column(db.String(50), nullable=False)  # IMMIGRATION, FAMILY, etc.
    status: str = db.Column(db.String(50), nullable=False)  # NEW, IN_PROGRESS, etc.
    priority: str = db.Column(db.String(50), nullable=False)  # LOW, MEDIUM, HIGH, URGENT
    
    # Foreign keys
    client_id: str = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    lawyer_id: Optional[str] = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=True)
    
    # Timestamps
    created: datetime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated: datetime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    client = db.relationship('User', foreign_keys=[client_id], backref=db.backref('client_cases', lazy=True))
    lawyer = db.relationship('User', foreign_keys=[lawyer_id], backref=db.backref('lawyer_cases', lazy=True))
    documents = db.relationship('Document', backref='case', lazy=True)

    def __repr__(self) -> str:
        return f'<Case {self.id}: {self.title}>'
        
    def to_dict(self) -> dict:
        """Convert case to dictionary."""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'case_type': self.case_type,
            'status': self.status,
            'priority': self.priority,
            'client_id': self.client_id,
            'lawyer_id': self.lawyer_id,
            'created': self.created.isoformat(),
            'updated': self.updated.isoformat(),
            'client': {
                'id': self.client.id,
                'name': f"{self.client.first_name} {self.client.last_name}"
            },
            'lawyer': {
                'id': self.lawyer.id,
                'name': f"{self.lawyer.first_name} {self.lawyer.last_name}"
            } if self.lawyer else None
        } 