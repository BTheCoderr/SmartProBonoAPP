"""
Authentication utilities
"""
from functools import wraps
from flask import request, jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity, get_jwt
import secrets
import string
import logging
import time
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

def login_required(fn):
    """
    Decorator to require JWT authentication for a route
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request()
            return fn(*args, **kwargs)
        except Exception as e:
            logger.error(f"Authentication error: {str(e)}")
            return jsonify({"error": "Authentication required"}), 401
    return wrapper

def admin_required(fn):
    """
    Decorator to require admin role for a route
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request()
            claims = get_jwt()
            if claims.get("role") != "admin":
                return jsonify({"error": "Admin privileges required"}), 403
            return fn(*args, **kwargs)
        except Exception as e:
            logger.error(f"Authentication error: {str(e)}")
            return jsonify({"error": "Authentication required"}), 401
    return wrapper

def generate_verification_token(length=32):
    """
    Generate a random verification token
    """
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def verify_token(token, token_type="verification", expiration_hours=24):
    """
    Verify a token from the database
    
    Args:
        token: The token to verify
        token_type: The type of token ('verification', 'reset', etc.)
        expiration_hours: How long the token is valid for
        
    Returns:
        User ID if valid, None otherwise
    """
    from database import db
    from models.user import User
    
    try:
        # Mock implementation - replace with actual database lookup
        user = User.query.filter_by(verification_token=token).first()
        
        if not user:
            return None
            
        # Check if token is expired
        token_created = user.token_created_at
        if token_created:
            expiration = token_created + timedelta(hours=expiration_hours)
            if datetime.utcnow() > expiration:
                return None
                
        return user.id
    except Exception as e:
        logger.error(f"Error verifying token: {str(e)}")
        return None 