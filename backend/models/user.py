from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from models.database import db

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='client')  # 'client' or 'attorney'
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    phone = db.Column(db.String(20))
    address = db.Column(db.String(200))
    city = db.Column(db.String(100))
    state = db.Column(db.String(50))
    zip_code = db.Column(db.String(20))
    is_verified = db.Column(db.Boolean, default=False)
    verification_token = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    # Attorney-specific fields
    bar_number = db.Column(db.String(50))
    practice_areas = db.Column(db.String(500))  # Comma-separated list
    years_of_experience = db.Column(db.Integer)
    languages = db.Column(db.String(200))  # Comma-separated list
    availability = db.Column(db.String(500))  # JSON string of availability
    pro_bono_hours = db.Column(db.Integer, default=0)
    
    # Client-specific fields
    income_level = db.Column(db.String(50))
    legal_issue_type = db.Column(db.String(100))
    case_description = db.Column(db.Text)
    
    def __init__(self, email, password, role='client', **kwargs):
        self.email = email.lower()
        self.set_password(password)
        self.role = role
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    def set_password(self, password):
        """Set password hash using SHA256"""
        self.password_hash = generate_password_hash(password, method='pbkdf2:sha256')
    
    def check_password(self, password):
        """Check password against hash"""
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        """Convert user object to dictionary"""
        base_dict = {
            'id': self.id,
            'email': self.email,
            'role': self.role,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'phone': self.phone,
            'address': self.address,
            'city': self.city,
            'state': self.state,
            'zip_code': self.zip_code,
            'is_verified': self.is_verified,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None
        }
        
        # Add role-specific fields
        if self.role == 'attorney':
            base_dict.update({
                'bar_number': self.bar_number,
                'practice_areas': self.practice_areas.split(',') if self.practice_areas else [],
                'years_of_experience': self.years_of_experience,
                'languages': self.languages.split(',') if self.languages else [],
                'availability': self.availability,  # Frontend will parse JSON
                'pro_bono_hours': self.pro_bono_hours
            })
        else:  # client
            base_dict.update({
                'income_level': self.income_level,
                'legal_issue_type': self.legal_issue_type,
                'case_description': self.case_description
            })
        
        return base_dict
    
    @staticmethod
    def get_by_email(email):
        """Get user by email"""
        return User.query.filter_by(email=email.lower()).first()
    
    @staticmethod
    def get_by_verification_token(token):
        """Get user by verification token"""
        return User.query.filter_by(verification_token=token).first()
    
    @staticmethod
    def get_attorneys_by_practice_area(practice_area):
        """Get attorneys by practice area"""
        return User.query.filter(
            User.role == 'attorney',
            User.practice_areas.like(f'%{practice_area}%')
        ).all()
    
    def update_last_login(self):
        """Update last login timestamp"""
        self.last_login = datetime.utcnow()
        db.session.commit() 