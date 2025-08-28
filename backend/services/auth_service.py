"""Authentication service for user management and route protection"""
import jwt
import logging
from functools import wraps
from flask import request, jsonify, current_app, g
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

def generate_token(user_id, role="user", expiration=24):
    """
    Generate a JWT token for authentication
    
    Args:
        user_id (str): The user ID
        role (str): The user role
        expiration (int): Token expiration time in hours
        
    Returns:
        str: The generated JWT token
    """
    try:
        payload = {
            'exp': datetime.utcnow() + timedelta(hours=expiration),
            'iat': datetime.utcnow(),
            'sub': str(user_id),
            'role': role
        }
        return jwt.encode(
            payload,
            current_app.config.get('SECRET_KEY', 'dev-key'),
            algorithm='HS256'
        )
    except Exception as e:
        logger.error(f"Error generating token: {str(e)}")
        return None

def decode_token(token):
    """
    Decode a JWT token
    
    Args:
        token (str): The JWT token to decode
        
    Returns:
        dict: The decoded token payload
    """
    try:
        return jwt.decode(
            token,
            current_app.config.get('SECRET_KEY', 'dev-key'),
            algorithms=['HS256']
        )
    except jwt.ExpiredSignatureError:
        logger.warning("Token expired")
        return None
    except jwt.InvalidTokenError as e:
        logger.warning(f"Invalid token: {str(e)}")
        return None
    except Exception as e:
        logger.error(f"Error decoding token: {str(e)}")
        return None

def require_auth(f):
    """
    Decorator to protect routes requiring authentication
    
    Args:
        f (function): The function to decorate
        
    Returns:
        function: The decorated function
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Check if token is in headers
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]
            except IndexError:
                token = auth_header
        
        # Check if token is in cookies
        if not token and request.cookies.get('token'):
            token = request.cookies.get('token')
            
        # Check if token is in query params (for WebSocket connections)
        if not token and request.args.get('token'):
            token = request.args.get('token')
            
        if not token:
            logger.warning("No token provided")
            return jsonify({'message': 'Authentication required'}), 401
            
        try:
            payload = decode_token(token)
            if not payload:
                logger.warning("Invalid token payload")
                return jsonify({'message': 'Invalid token'}), 401
                
            # Store user info in g for access in the request
            g.user_id = payload['sub']
            g.user_role = payload.get('role', 'user')
        except Exception as e:
            logger.error(f"Authentication error: {str(e)}")
            return jsonify({'message': 'Invalid token'}), 401
            
        return f(*args, **kwargs)
        
    return decorated

def require_admin(f):
    """
    Decorator to protect routes requiring admin privileges
    
    Args:
        f (function): The function to decorate
        
    Returns:
        function: The decorated function
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Check if token is in headers
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]
            except IndexError:
                token = auth_header
        
        # Check if token is in cookies
        if not token and request.cookies.get('token'):
            token = request.cookies.get('token')
            
        if not token:
            logger.warning("No token provided")
            return jsonify({'message': 'Authentication required'}), 401
            
        try:
            payload = decode_token(token)
            if not payload:
                logger.warning("Invalid token payload")
                return jsonify({'message': 'Invalid token'}), 401
                
            # Check for admin role
            if payload.get('role') != 'admin':
                logger.warning(f"User {payload['sub']} attempted to access admin route")
                return jsonify({'message': 'Admin privileges required'}), 403
                
            # Store user info in g for access in the request
            g.user_id = payload['sub']
            g.user_role = payload['role']
        except Exception as e:
            logger.error(f"Authentication error: {str(e)}")
            return jsonify({'message': 'Invalid token'}), 401
            
        return f(*args, **kwargs)
        
    return decorated

def get_current_user():
    """
    Get the current authenticated user
    
    Returns:
        dict: User info with id and role
    """
    if hasattr(g, 'user_id'):
        return {
            'id': g.user_id,
            'role': getattr(g, 'user_role', 'user')
        }
    return None

# Mock user database for development/testing
# In a real application, this would be replaced with database queries
MOCK_USERS = {
    'user1': {
        'id': 'user1',
        'email': 'user@example.com',
        'password': 'hashed_password_here',
        'name': 'Test User',
        'role': 'user'
    },
    'admin1': {
        'id': 'admin1',
        'email': 'admin@example.com',
        'password': 'admin_hashed_password',
        'name': 'Admin User',
        'role': 'admin'
    }
}

def authenticate_user(email, password):
    """
    Authenticate a user with email and password
    
    Args:
        email (str): User email
        password (str): User password
        
    Returns:
        tuple: (user_id, user_role) or (None, None) if authentication fails
    """
    # In a real app, you would verify credentials against a database
    # and use proper password hashing (bcrypt, etc.)
    
    # This is a simplified mock implementation
    for user_id, user_data in MOCK_USERS.items():
        if user_data['email'] == email:
            # In a real app: if bcrypt.checkpw(password.encode(), user_data['password_hash'].encode()):
            if user_data['password'] == password:  # NEVER do this in production!
                return user_id, user_data['role']
                
    return None, None 