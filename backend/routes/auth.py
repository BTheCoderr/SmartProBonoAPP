from flask import Blueprint, request, jsonify, current_app
from werkzeug.security import check_password_hash, generate_password_hash
from backend.models.user import User
from backend.extensions import mongo, db
from backend.utils.decorators import token_required
from backend.middleware.rate_limiting import rate_limiter
import os
import secrets
import uuid
from datetime import datetime, timedelta
from functools import wraps
from services.email_service import EmailService
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    create_refresh_token, get_jwt_identity, get_jwt
)
from bson import ObjectId
import logging
from typing import Optional
from pymongo.collection import Collection
from pymongo.database import Database

bp = Blueprint('auth', __name__, url_prefix='/api/auth')
logger = logging.getLogger(__name__)

def get_users_collection() -> Optional[Collection]:
    """Get the users collection from MongoDB."""
    try:
        db: Optional[Database] = getattr(mongo, 'db', None)
        if db is None:
            logger.error("MongoDB connection not available")
            return None
        return db.users
    except Exception as e:
        logger.error(f"Error accessing MongoDB collection: {str(e)}")
        return None

# Store reset tokens and email verification tokens temporarily - in production, these should be in a database
password_reset_tokens = {}
email_verification_tokens = {}
# For tracking active sessions (user_id -> {token -> expiry})
active_sessions = {}

# Token blacklist
jwt_blocklist = set()

def token_required(f):
    @wraps(f)
    @jwt_required()
    def decorated(*args, **kwargs):
        # Get current user identity from JWT
        current_user_id = get_jwt_identity()
        current_user = User.query.filter_by(id=current_user_id).first()
        
        if not current_user:
            return jsonify({'message': 'User not found'}), 401
            
        # Pass the current user to the wrapped function
        return f(current_user, *args, **kwargs)
        
    return decorated

@bp.route('/register', methods=['POST'])
@rate_limiter.limit('register')
def register():
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['email', 'password', 'firstName', 'lastName', 'role']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400
        
        users = get_users_collection()
        if users is None:
            return jsonify({'error': 'Database connection error'}), 500
            
        # Check if user already exists
        if users.find_one({'email': data['email']}) is not None:
            return jsonify({'error': 'Email already registered'}), 409
        
        # Create new user document
        new_user = {
            'email': data['email'],
            'password': generate_password_hash(data['password']),
            'firstName': data['firstName'],
            'lastName': data['lastName'],
            'role': data['role'],
            'active': True,
            'created_at': datetime.utcnow()
        }
        
        # Insert into database
        result = users.insert_one(new_user)
        
        # Create tokens
        access_token = create_access_token(identity=str(result.inserted_id))
        refresh_token = create_refresh_token(identity=str(result.inserted_id))
        
        return jsonify({
            'message': 'User registered successfully',
            'access_token': access_token,
            'refresh_token': refresh_token,
            'user': {
                'id': str(result.inserted_id),
                'email': data['email'],
                'firstName': data['firstName'],
                'lastName': data['lastName'],
                'role': data['role']
            }
        }), 201
        
    except Exception as e:
        logger.error(f"Registration error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@bp.route('/verify-email/<token>', methods=['GET'])
def verify_email(token):
    # Check if token exists and is valid
    if token not in email_verification_tokens:
        return jsonify({'message': 'Invalid or expired verification token'}), 400
    
    token_data = email_verification_tokens[token]
    
    # Check if token is expired
    if datetime.utcnow() > token_data['expiration']:
        # Remove expired token
        del email_verification_tokens[token]
        return jsonify({'message': 'Verification token has expired'}), 400
        
    # Find user and activate account
    user = User.query.filter_by(id=token_data['user_id']).first()
    
    if not user:
        return jsonify({'message': 'User not found'}), 404
        
    user.active = True
    user.email_verified = True
    db.session.commit()
    
    # Remove the used token
    del email_verification_tokens[token]
    
    return jsonify({'message': 'Email verified successfully. Your account is now active.'}), 200

@bp.route('/login', methods=['POST'])
@rate_limiter.limit('login')
def login():
    try:
        data = request.get_json()
        
        # Validate input
        if not data or not data.get('email') or not data.get('password'):
            return jsonify({'error': 'Missing email or password'}), 400
        
        users = get_users_collection()
        if users is None:
            return jsonify({'error': 'Database connection error'}), 500
            
        # Find user
        user = users.find_one({'email': data['email']})
        if user is None or not check_password_hash(user['password'], data['password']):
            return jsonify({'error': 'Invalid email or password'}), 401
        
        # Create tokens
        access_token = create_access_token(identity=str(user['_id']))
        refresh_token = create_refresh_token(identity=str(user['_id']))
        
        return jsonify({
            'access_token': access_token,
            'refresh_token': refresh_token,
            'user': {
                'id': str(user['_id']),
                'email': user['email'],
                'firstName': user['firstName'],
                'lastName': user['lastName'],
                'role': user['role']
            }
        }), 200
        
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@bp.route('/refresh', methods=['POST'])
@rate_limiter.limit('default')
@jwt_required(refresh=True)
def refresh():
    try:
        current_user = get_jwt_identity()
        new_access_token = create_access_token(identity=current_user)
        
        return jsonify({
            'access_token': new_access_token
        }), 200
        
    except Exception as e:
        logger.error(f"Token refresh error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@bp.route('/logout', methods=['POST'])
@rate_limiter.limit('default')
@jwt_required()
def logout():
    jti = get_jwt()['jti']
    jwt_blocklist.add(jti)
    return jsonify({'message': 'Logged out successfully'}), 200

@bp.route('/me', methods=['GET'])
@token_required
def get_user_profile(current_user):
    try:
        current_user_id = get_jwt_identity()
        users = get_users_collection()
        if users is None:
            return jsonify({'error': 'Database connection error'}), 500
            
        user = users.find_one({'_id': ObjectId(current_user_id)})
        if user is None:
            return jsonify({'error': 'User not found'}), 404
            
        return jsonify({
            'user': {
                'id': str(user['_id']),
                'email': user['email'],
                'firstName': user['firstName'],
                'lastName': user['lastName'],
                'role': user['role']
            }
        }), 200
        
    except Exception as e:
        logger.error(f"Get profile error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@bp.route('/forgot-password', methods=['POST'])
@rate_limiter.limit('forgot_password')
def forgot_password():
    data = request.json
    
    if not data or not data.get('email'):
        return jsonify({'message': 'Email is required'}), 400
        
    user = User.query.filter_by(email=data['email']).first()
    
    # Always return success even if user not found (security best practice)
    if not user:
        return jsonify({
            'message': 'If a user with that email exists, a password reset link has been sent.'
        }), 200
    
    # Generate a secure random token
    token = secrets.token_urlsafe(32)
    expiration = datetime.utcnow() + timedelta(hours=1)
    
    # Store token with user ID and expiration
    password_reset_tokens[token] = {
        'user_id': user.id,
        'expiration': expiration
    }
    
    # Generate reset link
    reset_link = f"{request.host_url}reset-password/{token}"
    
    # Send password reset email
    EmailService.send_password_reset_email(
        user.email,
        user.username,
        reset_link
    )
    
    return jsonify({
        'message': 'If a user with that email exists, a password reset link has been sent.',
        'reset_link': reset_link  # Remove this in production
    }), 200

@bp.route('/reset-password', methods=['POST'])
@rate_limiter.limit('forgot_password')
def reset_password():
    data = request.json
    
    if not data or not data.get('token') or not data.get('password'):
        return jsonify({'message': 'Token and new password are required'}), 400
        
    token = data['token']
    new_password = data['password']
    
    # Check if token exists and is valid
    if token not in password_reset_tokens:
        return jsonify({'message': 'Invalid or expired token'}), 400
    
    token_data = password_reset_tokens[token]
    
    # Check if token is expired
    if datetime.utcnow() > token_data['expiration']:
        # Remove expired token
        del password_reset_tokens[token]
        return jsonify({'message': 'Token has expired'}), 400
        
    # Find user and update password
    user = User.query.filter_by(id=token_data['user_id']).first()
    
    if not user:
        return jsonify({'message': 'User not found'}), 404
        
    user.set_password(new_password)
    db.session.commit()
    
    # Remove the used token
    del password_reset_tokens[token]
    
    # Logout from all devices when password is reset
    if str(user.id) in active_sessions:
        active_sessions[str(user.id)] = {}
    
    return jsonify({'message': 'Password has been reset successfully'}), 200

# Initialize limiter with the app
def init_app(app):
    """Initialize the auth module with the Flask app."""
    return app 