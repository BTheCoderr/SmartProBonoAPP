"""Beta signup model"""
from datetime import datetime
from app import db  # Import db directly from app
from sqlalchemy.dialects.postgresql import JSONB

class BetaSignup(db.Model):
    """Model for beta signup emails"""
    __tablename__ = "beta_signups"
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    source = db.Column(db.String(255), nullable=True)
    utm_source = db.Column(db.String(255), nullable=True)
    utm_medium = db.Column(db.String(255), nullable=True)
    utm_campaign = db.Column(db.String(255), nullable=True)
    is_confirmed = db.Column(db.Boolean, default=False)
    confirmation_token = db.Column(db.String(255), unique=True, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    confirmed_at = db.Column(db.DateTime, nullable=True)
    
    # Subscription fields
    subscription_preferences = db.Column(JSONB, nullable=True)
    subscribed_at = db.Column(db.DateTime, nullable=True)
    is_subscribed = db.Column(db.Boolean, default=False)
    
    def __repr__(self):
        return f"<BetaSignup {self.email}>" 