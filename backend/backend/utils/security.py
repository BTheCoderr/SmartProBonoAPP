"""
Security utilities for authentication and authorization
"""
import hashlib
import secrets
import string
from typing import Callable, Dict, List, Optional, Tuple, Union
from functools import wraps
from flask import request, current_app, g
from flask_jwt_extended import get_jwt, get_jwt_identity, verify_jwt_in_request

from .responses import error_response

# Constants
PASSWORD_MIN_LENGTH = 8
TOKEN_LENGTH = 32

def hash_password(password: str, salt: Optional[str] = None) -> Tuple[str, str]:
    """
    Hash a password with a salt using PBKDF2
    
    Args:
        password: The password to hash
        salt: Optional salt, generated if not provided
        
    Returns:
        Tuple of (hashed_password, salt)
    """
    if not salt:
        salt = secrets.token_hex(16)
        
    # Use PBKDF2 via hashlib
    key = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt.encode('utf-8'),
        100000  # Number of iterations
    ).hex()
    
    return key, salt

def verify_password(password: str, hashed_password: str, salt: str) -> bool:
    """
    Verify a password against a hashed password and salt
    
    Args:
        password: The password to verify
        hashed_password: The stored hashed password
        salt: The salt used for hashing
        
    Returns:
        True if password matches
    """
    calculated_hash, _ = hash_password(password, salt)
    return secrets.compare_digest(calculated_hash, hashed_password)

def generate_password(length: int = 12) -> str:
    """
    Generate a secure random password
    
    Args:
        length: Length of the password
        
    Returns:
        A random password
    """
    if length < PASSWORD_MIN_LENGTH:
        length = PASSWORD_MIN_LENGTH
        
    # Include at least one of each: uppercase, lowercase, digit, symbol
    chars = string.ascii_lowercase + string.ascii_uppercase + string.digits + string.punctuation
    
    # Ensure we have one of each type
    password = [
        secrets.choice(string.ascii_lowercase),
        secrets.choice(string.ascii_uppercase),
        secrets.choice(string.digits),
        secrets.choice(string.punctuation)
    ]
    
    # Fill the rest randomly
    password.extend(secrets.choice(chars) for _ in range(length - 4))
    
    # Shuffle the password
    password_list = list(password)
    secrets.SystemRandom().shuffle(password_list)
    
    return ''.join(password_list)

def generate_token(length: int = TOKEN_LENGTH) -> str:
    """
    Generate a secure random token
    
    Args:
        length: Length of the token
        
    Returns:
        A random token
    """
    return secrets.token_urlsafe(length)

def role_required(role: Union[str, List[str]]) -> Callable:
    """
    Decorator to check if a user has the required role(s)
    
    Args:
        role: Required role or list of roles (any match is sufficient)
        
    Returns:
        Decorator function
    """
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            # Verify JWT is present
            try:
                verify_jwt_in_request()
            except Exception:
                return error_response("Missing or invalid token", status_code=401)
            
            # Get claims from the JWT
            claims = get_jwt()
            user_roles = claims.get('roles', [])
            
            # Convert single role to list
            required_roles = [role] if isinstance(role, str) else role
            
            # Check if user has any of the required roles
            if not any(r in user_roles for r in required_roles):
                return error_response("Insufficient permissions", status_code=403)
            
            # Store user ID and roles in Flask's g object for convenience
            g.user_id = get_jwt_identity()
            g.roles = user_roles
            
            return fn(*args, **kwargs)
        return wrapper
    return decorator

def admin_required(fn):
    """
    Decorator to check if a user has admin role
    
    Args:
        fn: The function to decorate
        
    Returns:
        Decorated function
    """
    return role_required('admin')(fn)

def user_required(fn):
    """
    Decorator to check if a user has user role
    
    Args:
        fn: The function to decorate
        
    Returns:
        Decorated function
    """
    return role_required('user')(fn)

def lawyer_required(fn):
    """
    Decorator to check if a user has lawyer role
    
    Args:
        fn: The function to decorate
        
    Returns:
        Decorated function
    """
    return role_required('lawyer')(fn)

def get_current_user_id() -> Optional[str]:
    """
    Get the ID of the current user
    
    Returns:
        User ID or None if not authenticated
    """
    try:
        verify_jwt_in_request()
        return get_jwt_identity()
    except Exception:
        return None

def get_current_user_roles() -> List[str]:
    """
    Get the roles of the current user
    
    Returns:
        List of user roles or empty list if not authenticated
    """
    try:
        verify_jwt_in_request()
        claims = get_jwt()
        return claims.get('roles', [])
    except Exception:
        return []

def has_role(role: Union[str, List[str]]) -> bool:
    """
    Check if the current user has a specific role
    
    Args:
        role: Role or list of roles to check
        
    Returns:
        True if user has any of the specified roles
    """
    user_roles = get_current_user_roles()
    required_roles = [role] if isinstance(role, str) else role
    return any(r in user_roles for r in required_roles)

def is_admin() -> bool:
    """
    Check if the current user is an admin
    
    Returns:
        True if user is an admin
    """
    return has_role('admin')

def is_lawyer() -> bool:
    """
    Check if the current user is a lawyer
    
    Returns:
        True if user is a lawyer
    """
    return has_role('lawyer')

def sanitize_user_data(user_data: Dict) -> Dict:
    """
    Remove sensitive fields from user data
    
    Args:
        user_data: User data dictionary
        
    Returns:
        Sanitized user data
    """
    # Create a copy to avoid modifying the original
    sanitized = user_data.copy()
    
    # Remove sensitive fields
    sensitive_fields = ['password', 'password_hash', 'salt', 'security_question_answer', 
                       'reset_token', 'activation_token', 'auth_tokens']
                       
    for field in sensitive_fields:
        if field in sanitized:
            del sanitized[field]
            
    return sanitized 