"""
Authentication utilities for JWT token management and route protection
"""
from functools import wraps
from flask import request, jsonify, current_app, g
from flask_jwt_extended import (
    verify_jwt_in_request, get_jwt_identity, get_jwt,
    create_access_token, create_refresh_token
)
import logging
from datetime import datetime, timedelta
from bson import ObjectId
from typing import Optional, Dict, Any, List, Union, Callable

# Set up logger
logger = logging.getLogger(__name__)

def generate_tokens(user_id: str, additional_claims: Optional[Dict[str, Any]] = None) -> Dict[str, str]:
    """
    Generate JWT access and refresh tokens
    
    Args:
        user_id: The user ID to encode in the token
        additional_claims: Additional claims to include in the token
        
    Returns:
        Dict containing access_token and refresh_token
    """
    try:
        if additional_claims is None:
            additional_claims = {}
            
        access_token = create_access_token(
            identity=str(user_id),
            additional_claims=additional_claims
        )
        
        refresh_token = create_refresh_token(
            identity=str(user_id),
            additional_claims=additional_claims
        )
        
        return {
            'access_token': access_token,
            'refresh_token': refresh_token
        }
        
    except Exception as e:
        logger.error(f"Error generating tokens: {str(e)}")
        raise

def login_required(fn: Callable) -> Callable:
    """
    Decorator to require JWT authentication for a route
    
    Args:
        fn: The function to decorate
        
    Returns:
        The decorated function
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request()
            # Store user ID in Flask's g object for convenience
            g.user_id = get_jwt_identity()
            g.jwt_claims = get_jwt()
            return fn(*args, **kwargs)
        except Exception as e:
            logger.error(f"Authentication error: {str(e)}")
            return jsonify({"error": "Authentication required"}), 401
    return wrapper

def role_required(required_roles: Union[str, List[str]]) -> Callable:
    """
    Decorator to require specific role(s) for a route
    
    Args:
        required_roles: Role or list of roles (any match is sufficient)
        
    Returns:
        The decorator function
    """
    if isinstance(required_roles, str):
        required_roles = [required_roles]
        
    def decorator(fn: Callable) -> Callable:
        @wraps(fn)
        @login_required
        def wrapper(*args, **kwargs):
            jwt_data = get_jwt()
            user_roles = jwt_data.get('roles', [])
            
            if isinstance(user_roles, str):
                user_roles = [user_roles]
                
            # Check if user has any of the required roles
            if not any(role in user_roles for role in required_roles):
                logger.warning(f"User {get_jwt_identity()} lacks required role(s): {required_roles}")
                return jsonify({"error": "Insufficient permissions"}), 403
                
            return fn(*args, **kwargs)
        return wrapper
    return decorator

def admin_required(fn: Callable) -> Callable:
    """
    Decorator to require admin role for a route
    
    Args:
        fn: The function to decorate
        
    Returns:
        The decorated function
    """
    return role_required('admin')(fn)
    
def get_current_user_id() -> Optional[str]:
    """
    Get the current authenticated user ID
    
    Returns:
        User ID or None if not authenticated
    """
    try:
        verify_jwt_in_request(optional=True)
        return get_jwt_identity()
    except Exception:
        return None

def is_token_revoked(jwt_payload: Dict[str, Any]) -> bool:
    """
    Check if a token has been revoked
    
    Args:
        jwt_payload: The JWT payload to check
        
    Returns:
        True if token is revoked, False otherwise
    """
    jti = jwt_payload.get('jti')
    
    if not jti:
        return True
        
    # Check if token is in blocklist
    if 'jwt_blocklist' in current_app.extensions:
        return jti in current_app.extensions['jwt_blocklist']
        
    return False 