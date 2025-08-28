"""
Document model for the SmartProBono application.
"""
from datetime import datetime
from database import db
import json

class Document(db.Model):
    """Document model for storing legal documents."""
    __tablename__ = 'documents'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=True)
    file_url = db.Column(db.String(512), nullable=True)
    file_type = db.Column(db.String(50), nullable=True)
    document_type = db.Column(db.String(50), default='case_document')
    description = db.Column(db.Text, nullable=True)
    cloudinary_public_id = db.Column(db.String(255), nullable=True)
    uploaded_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    case_id = db.Column(db.Integer, db.ForeignKey('cases.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    _tags = db.Column('tags', db.Text, nullable=True)
    _history = db.Column('history', db.Text, nullable=True)
    
    @property
    def tags(self):
        """Get document tags as a list."""
        if not self._tags:
            return []
        return json.loads(self._tags)
        
    @tags.setter
    def tags(self, value):
        """Set document tags from a list."""
        if isinstance(value, list):
            self._tags = json.dumps(value)
        else:
            self._tags = None
            
    @property
    def history(self):
        """Get document version history as a list."""
        if not self._history:
            return []
        return json.loads(self._history)
        
    def add_version(self, content):
        """Add a version to the document history."""
        current_history = self.history
        new_version = {
            'content': content,
            'timestamp': datetime.utcnow().isoformat(),
            'version': len(current_history) + 1
        }
        current_history.append(new_version)
        self._history = json.dumps(current_history)
        
    def to_dict(self):
        """Convert document to a dictionary."""
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'file_url': self.file_url,
            'file_type': self.file_type,
            'document_type': self.document_type,
            'description': self.description,
            'cloudinary_public_id': self.cloudinary_public_id,
            'uploaded_by': self.uploaded_by,
            'case_id': self.case_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'tags': self.tags,
            'version_count': len(self.history)
        } 