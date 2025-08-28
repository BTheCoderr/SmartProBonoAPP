"""
Case model for the SmartProBono application.
"""
from datetime import datetime
from database import db
import json

class Case(db.Model):
    """Case model for storing legal cases."""
    __tablename__ = 'cases'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    client_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    attorney_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    status = db.Column(db.String(50), default='open')
    case_type = db.Column(db.String(50), nullable=True)
    priority = db.Column(db.String(20), default='medium')
    practice_area = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    due_date = db.Column(db.DateTime, nullable=True)
    _notes = db.Column('notes', db.Text, nullable=True)
    _tags = db.Column('tags', db.Text, nullable=True)
    
    # Relationships
    documents = db.relationship('Document', backref='case', lazy=True)
    
    @property
    def tags(self):
        """Get case tags as a list."""
        if not self._tags:
            return []
        return json.loads(self._tags)
        
    @tags.setter
    def tags(self, value):
        """Set case tags from a list."""
        if isinstance(value, list):
            self._tags = json.dumps(value)
        else:
            self._tags = None
            
    @property
    def notes(self):
        """Get case notes as a list."""
        if not self._notes:
            return []
        return json.loads(self._notes)
        
    @notes.setter
    def notes(self, value):
        """Set case notes from a list."""
        if isinstance(value, list):
            self._notes = json.dumps(value)
        else:
            self._notes = None
    
    def add_note(self, note_text, user_id):
        """Add a note to the case."""
        current_notes = self.notes
        new_note = {
            'text': note_text,
            'user_id': user_id,
            'timestamp': datetime.utcnow().isoformat()
        }
        current_notes.append(new_note)
        self._notes = json.dumps(current_notes)
        
    def to_dict(self):
        """Convert case to a dictionary."""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'client_id': self.client_id,
            'attorney_id': self.attorney_id,
            'status': self.status,
            'case_type': self.case_type,
            'priority': self.priority,
            'practice_area': self.practice_area,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'notes': self.notes,
            'tags': self.tags,
            'document_count': len(self.documents) if self.documents else 0
        } 