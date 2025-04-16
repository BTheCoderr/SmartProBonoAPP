from flask import Blueprint, request, jsonify, session, current_app
from werkzeug.security import generate_password_hash, check_password_hash
import os
import json
from datetime import datetime, timedelta
import uuid
# Import PyJWT for token handling
import jwt
from functools import wraps
from models.user import User
from models.database import db
import secrets
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
from flask_limiter import Limiter  # type: ignore
from flask_limiter.util import get_remote_address  # type: ignore
from typing import Dict, Any, Optional, Union, cast, TypeVar, Type
from sqlalchemy.orm import scoped_session, Session  # type: ignore
from sqlalchemy.orm.session import Session as SQLAlchemySession  # type: ignore

load_dotenv()

# Create the auth blueprint with a URL prefix
auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth', cli_group=None)

# Initialize rate limiter
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://"
)

# Rate limit decorators
login_limit = limiter.limit("5 per minute, 20 per hour")
signup_limit = limiter.limit("3 per minute, 10 per hour")
verify_limit = limiter.limit("3 per minute, 10 per hour")

# Create users directory if it doesn't exist
if not os.path.exists('data/users'):
    os.makedirs('data/users')

# Secret key for JWT
SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'dev_secret_key')

# User database file
USERS_FILE = 'data/users/users.json'

# Initialize users file if it doesn't exist
if not os.path.exists(USERS_FILE):
    with open(USERS_FILE, 'w') as f:
        json.dump([], f)

def get_users():
    try:
        with open(USERS_FILE, 'r') as f:
            return json.load(f)
    except:
        return []

def save_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=2)

def generate_safe_password_hash(password):
    """Generate a password hash using pbkdf2:sha256 method"""
    return generate_password_hash(password, method='pbkdf2:sha256')

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]
            except IndexError:
                return jsonify({'error': 'Token is missing'}), 401
        
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
            
        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = User.query.get(data['user_id'])
            if not current_user:
                return jsonify({'error': 'Invalid token'}), 401
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token'}), 401
            
        return f(current_user, *args, **kwargs)
    
    return decorated

def send_verification_email(user_email, token):
    """Send verification email to user"""
    try:
        smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        smtp_port = int(os.getenv('SMTP_PORT', '587'))
        smtp_username = os.getenv('SMTP_USERNAME')
        smtp_password = os.getenv('SMTP_PASSWORD')
        
        msg = MIMEMultipart()
        msg['From'] = smtp_username
        msg['To'] = user_email
        msg['Subject'] = 'Verify your SmartProBono account'
        
        verification_url = f"{os.getenv('FRONTEND_URL')}/verify-email?token={token}"
        body = f"""
        Welcome to SmartProBono!
        
        Please click the link below to verify your email address:
        {verification_url}
        
        This link will expire in 24 hours.
        
        If you did not create an account, please ignore this email.
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.send_message(msg)
        server.quit()
        
        return True
    except Exception as e:
        current_app.logger.error(f"Error sending verification email: {str(e)}")
        return False

T = TypeVar('T')

def get_value(data: Dict[str, Any], key: str) -> str:
    """Safely get a value from a dictionary with proper type casting."""
    value = data.get(key)
    if value is None or not isinstance(value, str):
        raise ValueError(f"Missing or invalid required field: {key}")
    return value

@auth_bp.route('/signup', methods=['POST'])
@limiter.limit("5 per minute")
def signup() -> tuple[Dict[str, Any], int]:
    try:
        data = request.get_json()
        if not data:
            return {"error": "No data provided"}, 400
            
        try:
            # Get and validate required fields
            email = get_value(data, 'email')
            password = get_value(data, 'password')
            first_name = get_value(data, 'first_name')
            last_name = get_value(data, 'last_name')
            user_type = get_value(data, 'user_type')
        except ValueError as e:
            return {"error": str(e)}, 400
                
        # Check if user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return {"error": "Email already registered"}, 409
            
        # Create new user
        new_user = User(
            email=email,
            password=generate_password_hash(password),
            first_name=first_name,
            last_name=last_name,
            user_type=user_type
        )
        
        db.session.add(new_user)  # type: ignore
        db.session.commit()  # type: ignore
        
        return {"message": "User created successfully"}, 201
        
    except Exception as e:
        if hasattr(db, 'session'):
            db.session.rollback()  # type: ignore
        current_app.logger.error(f"Error in signup: {str(e)}")
        return {"error": "Internal server error"}, 500

@auth_bp.route('/login', methods=['POST'])
@limiter.limit("10 per minute")
def login() -> tuple[Dict[str, Any], int]:
    try:
        data = request.get_json()
        if not data:
            return {"error": "No data provided"}, 400
            
        try:
            email = get_value(data, 'email')
            password = get_value(data, 'password')
        except ValueError as e:
            return {"error": str(e)}, 400
            
        user = User.query.filter_by(email=email).first()
        if not user or not check_password_hash(cast(str, user.password), password):
            return {"error": "Invalid email or password"}, 401
            
        # Generate access token here
        
        return {
            "message": "Login successful",
            "user": {
                "id": user.id,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "user_type": user.user_type
            }
        }, 200
        
    except Exception as e:
        current_app.logger.error(f"Error in login: {str(e)}")
        return {"error": "Internal server error"}, 500

@auth_bp.route('/verify-email/<token>', methods=['GET'])
@verify_limit
def verify_email(token):
    """Verify user's email"""
    user = User.get_by_verification_token(token)
    
    if not user:
        return jsonify({'error': 'Invalid verification token'}), 400
    
    if user.is_verified:
        return jsonify({'message': 'Email already verified'}), 200
    
    user.is_verified = True
    user.verification_token = None
    db.session.commit()
    
    return jsonify({'message': 'Email verified successfully'})

@auth_bp.route('/me', methods=['GET'])
@token_required
def get_current_user(current_user):
    """Get current user's profile"""
    return jsonify(current_user.to_dict())

@auth_bp.route('/me', methods=['PUT'])
@token_required
def update_profile(current_user):
    """Update user's profile"""
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    # Don't allow updating email or role through this endpoint
    forbidden_fields = ['email', 'role', 'password_hash', 'is_verified', 'verification_token']
    for field in forbidden_fields:
        data.pop(field, None)
    
    try:
        for key, value in data.items():
            setattr(current_user, key, value)
        
        db.session.commit()
        return jsonify({
            'message': 'Profile updated successfully',
            'user': current_user.to_dict()
        })
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error updating profile: {str(e)}")
        return jsonify({'error': 'Could not update profile'}), 500

@auth_bp.route('/change-password', methods=['POST'])
@token_required
def change_password(current_user):
    """Change user's password"""
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    if 'current_password' not in data or 'new_password' not in data:
        return jsonify({'error': 'Current and new passwords are required'}), 400
    
    if not current_user.check_password(data['current_password']):
        return jsonify({'error': 'Current password is incorrect'}), 401
    
    try:
        current_user.set_password(data['new_password'])
        db.session.commit()
        return jsonify({'message': 'Password changed successfully'})
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error changing password: {str(e)}")
        return jsonify({'error': 'Could not change password'}), 500