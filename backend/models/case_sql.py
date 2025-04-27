from datetime import datetime
from backend.database import db
from backend.models.user import User

class SQLCase(db.Model):
    __tablename__ = 'cases'
    __table_args__ = {'extend_existing': True}
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    client_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    lawyer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    category = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(50), default='open')  # 'open', 'assigned', 'closed'
    priority = db.Column(db.String(20), default='medium')  # 'low', 'medium', 'high'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    closed_at = db.Column(db.DateTime, nullable=True)
    
    # Define relationships
    client = db.relationship('User', foreign_keys=[client_id], backref=db.backref('client_cases', lazy=True))
    lawyer = db.relationship('User', foreign_keys=[lawyer_id], backref=db.backref('lawyer_cases', lazy=True))
    
    def __repr__(self):
        return f'<Case {self.id}: {self.title}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'client_id': self.client_id,
            'lawyer_id': self.lawyer_id,
            'category': self.category,
            'status': self.status,
            'priority': self.priority,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'closed_at': self.closed_at.isoformat() if self.closed_at else None
        } 