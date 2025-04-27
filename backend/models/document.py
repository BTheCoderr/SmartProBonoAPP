from backend.database import db
from datetime import datetime
import json

class Document(db.Model):
    __table_args__ = {'extend_existing': True}
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    file_url = db.Column(db.String(500), nullable=False)  # Cloudinary URL
    file_type = db.Column(db.String(50), nullable=False)
    cloudinary_public_id = db.Column(db.String(200), nullable=True)
    document_type = db.Column(db.String(50), default='case_document')  # 'case_document', 'template', 'contract'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    content = db.Column(db.Text, nullable=True)  # Document content or HTML
    
    # Foreign keys
    uploaded_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    case_id = db.Column(db.Integer, db.ForeignKey('case.id'), nullable=True)
    
    # Tags (stored as JSON string)
    _tags = db.Column('tags', db.Text, default='[]')
    
    # Version history (stored as JSON string)
    _history = db.Column('history', db.Text, default='[]')
    
    # Email shares (stored as JSON string)
    _email_shares = db.Column('email_shares', db.Text, default='[]')
    
    # Relationships
    uploader = db.relationship('User', foreign_keys=[uploaded_by], backref='uploaded_documents')
    case = db.relationship('Case', backref='documents')
    
    @property
    def tags(self):
        """Get the document tags"""
        try:
            return json.loads(self._tags)
        except (TypeError, json.JSONDecodeError):
            return []
            
    @tags.setter
    def tags(self, value):
        """Set the document tags"""
        if isinstance(value, list):
            self._tags = json.dumps(value)
        else:
            self._tags = '[]'
            
    @property
    def history(self):
        """Get the document version history"""
        try:
            return json.loads(self._history)
        except (TypeError, json.JSONDecodeError):
            return []
            
    @history.setter
    def history(self, value):
        """Set the document version history"""
        if isinstance(value, list):
            self._history = json.dumps(value)
        else:
            self._history = '[]'
            
    @property
    def email_shares(self):
        """Get the document email shares"""
        try:
            return json.loads(self._email_shares)
        except (TypeError, json.JSONDecodeError):
            return []
            
    @email_shares.setter
    def email_shares(self, value):
        """Set the document email shares"""
        if isinstance(value, list):
            self._email_shares = json.dumps(value)
        else:
            self._email_shares = '[]'
            
    def add_version(self, content, modified_by=None):
        """Add a new version to the history"""
        current_history = self.history
        new_version = {
            'content': content,
            'timestamp': datetime.utcnow().isoformat(),
            'version': len(current_history) + 1
        }
        
        if modified_by is not None:
            new_version['modified_by'] = modified_by
            
        current_history.append(new_version)
        self.history = current_history
        
    def add_email_share(self, email):
        """Record an email share"""
        current_shares = self.email_shares
        new_share = {
            'email': email,
            'timestamp': datetime.utcnow().isoformat()
        }
        current_shares.append(new_share)
        self.email_shares = current_shares
        
    def to_dict(self):
        """Convert document to dictionary"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'file_url': self.file_url,
            'file_type': self.file_type,
            'cloudinary_public_id': self.cloudinary_public_id,
            'document_type': self.document_type,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'content': self.content,
            'uploaded_by': self.uploaded_by,
            'case_id': self.case_id,
            'tags': self.tags,
            'history': self.history,
            'email_shares': self.email_shares
        } 