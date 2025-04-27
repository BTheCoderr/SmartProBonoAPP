"""User model"""
from backend.database import db
from datetime import datetime
from typing import Optional, Dict, Any
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    """User model for authentication and profile information"""
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256))
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    role = db.Column(db.String(20), default='user')
    active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = db.Column(db.DateTime)

    # Profile fields
    phone = db.Column(db.String(20))
    address = db.Column(db.String(200))
    city = db.Column(db.String(100))
    state = db.Column(db.String(50))
    zip_code = db.Column(db.String(20))
    preferred_language = db.Column(db.String(20), default='en')
    notification_preferences = db.Column(db.JSON)

    def __init__(self, email: str, password: Optional[str] = None, 
                 first_name: Optional[str] = None, last_name: Optional[str] = None,
                 role: str = 'user', active: bool = True) -> None:
        self.email = email
        if password:
            self.set_password(password)
        self.first_name = first_name
        self.last_name = last_name
        self.role = role
        self.active = active
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def __repr__(self) -> str:
        return f'<User {self.email}>'
    
    def set_password(self, password: str) -> None:
        """Set the password hash"""
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password: str) -> bool:
        """Check if the password matches"""
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert user object to dictionary"""
        return {
            'id': self.id,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'role': self.role,
            'active': self.active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'phone': self.phone,
            'address': self.address,
            'city': self.city,
            'state': self.state,
            'zip_code': self.zip_code,
            'preferred_language': self.preferred_language,
            'notification_preferences': self.notification_preferences
        } 