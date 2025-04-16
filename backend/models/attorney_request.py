from datetime import datetime
from typing import Optional
from config.database import db, BaseModel
import uuid

class AttorneyRequest(BaseModel):
    """Model for attorney connection requests."""
    __tablename__ = 'attorney_requests'

    id: str = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    client_id: str = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    attorney_id: str = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    status: str = db.Column(db.String(20), nullable=False)  # pending, accepted, rejected
    message: Optional[str] = db.Column(db.Text)
    legal_issue_type: Optional[str] = db.Column(db.String(50))
    case_description: Optional[str] = db.Column(db.Text)
    created_at: datetime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at: datetime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    client = db.relationship('User', foreign_keys=[client_id], backref=db.backref('sent_requests', lazy=True))
    attorney = db.relationship('User', foreign_keys=[attorney_id], backref=db.backref('received_requests', lazy=True))

    def __repr__(self) -> str:
        return f'<AttorneyRequest {self.id}: {self.client_id} -> {self.attorney_id}>'

    def to_dict(self) -> dict:
        """Convert request to dictionary."""
        return {
            'id': self.id,
            'client_id': self.client_id,
            'attorney_id': self.attorney_id,
            'status': self.status,
            'message': self.message,
            'legal_issue_type': self.legal_issue_type,
            'case_description': self.case_description,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'client': {
                'id': self.client.id,
                'name': f"{self.client.first_name} {self.client.last_name}",
                'email': self.client.email
            },
            'attorney': {
                'id': self.attorney.id,
                'name': f"{self.attorney.first_name} {self.attorney.last_name}",
                'email': self.attorney.email
            }
        } 