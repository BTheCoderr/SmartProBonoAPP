from database import db
from datetime import datetime

class Draft(db.Model):
    __tablename__ = 'drafts'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    form_type = db.Column(db.String(50), nullable=False)
    data = db.Column(db.JSON, nullable=False)
    timestamp = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, user_id, form_type, data, timestamp=None):
        self.user_id = user_id
        self.form_type = form_type
        self.data = data
        self.timestamp = timestamp or datetime.utcnow().timestamp()

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'form_type': self.form_type,
            'data': self.data,
            'timestamp': self.timestamp,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        } 