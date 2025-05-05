from datetime import datetime
from ..database import db
from sqlalchemy.dialects.postgresql import JSONB

class Form(db.Model):
    """Form model for storing submitted forms."""
    __tablename__ = 'forms'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    form_type = db.Column(db.String(50), nullable=False)
    data = db.Column(JSONB, nullable=False)
    status = db.Column(db.String(20), default='draft')  # draft, submitted, approved, rejected
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    submitted_at = db.Column(db.DateTime)
    
    # Relationships
    user = db.relationship('User', backref=db.backref('forms', lazy=True))
    documents = db.relationship('Document', backref='form', lazy=True)

    def __init__(self, user_id, form_type, data, status='draft', submitted_at=None):
        self.user_id = user_id
        self.form_type = form_type
        self.data = data
        self.status = status
        self.submitted_at = submitted_at

    def to_dict(self):
        """Convert form to dictionary."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'form_type': self.form_type,
            'data': self.data,
            'status': self.status,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'submitted_at': self.submitted_at.isoformat() if self.submitted_at else None
        }

class FormDraft(db.Model):
    """Model for storing form drafts."""
    __tablename__ = 'form_drafts'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    form_type = db.Column(db.String(50), nullable=False)
    data = db.Column(JSONB, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref=db.backref('form_drafts', lazy=True))

    def __init__(self, user_id, form_type, data):
        self.user_id = user_id
        self.form_type = form_type
        self.data = data

    def to_dict(self):
        """Convert draft to dictionary."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'form_type': self.form_type,
            'data': self.data,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        } 