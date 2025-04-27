"""Template model module"""
from datetime import datetime
from backend.extensions import db

class Template(db.Model):
    """Template model for form templates"""
    __tablename__ = 'templates'

    id = db.Column(db.Integer, primary_key=True)
    template_id = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    fields = db.Column(db.JSON, nullable=False)
    version = db.Column(db.String(20), nullable=False, default='1.0')
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, template_id, name, title, fields, version='1.0', is_active=True):
        """Initialize template"""
        self.template_id = template_id
        self.name = name
        self.title = title
        self.fields = fields
        self.version = version
        self.is_active = is_active

    def to_dict(self):
        """Convert template to dictionary"""
        return {
            'id': self.id,
            'template_id': self.template_id,
            'name': self.name,
            'title': self.title,
            'fields': self.fields,
            'version': self.version,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

    @staticmethod
    def from_dict(data):
        """Create template from dictionary"""
        return Template(
            template_id=data['template_id'],
            name=data['name'],
            title=data['title'],
            fields=data['fields'],
            version=data.get('version', '1.0'),
            is_active=data.get('is_active', True)
        ) 