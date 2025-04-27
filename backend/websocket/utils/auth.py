"""
Authentication utilities for WebSocket connections.

This module provides functions for verifying JWT tokens,
validating user identity, and authorizing WebSocket connections.
"""

import logging
import jwt
from datetime import datetime
from flask import current_app

# Configure logging
logger = logging.getLogger('websocket.utils.auth')

def validate_jwt(token, required_user_id=None, required_role=None):
    """
    Validate a JWT token and optionally check user identity and role.
    
    Args:
        token (str): The JWT token to validate
        required_user_id (str, optional): If provided, check that token belongs to this user
        required_role (str, optional): If provided, check that user has this role
        
    Returns:
        dict: Validation result with keys:
            - valid (bool): Whether token is valid
            - user_id (str, optional): User ID from token if valid
            - error (str, optional): Error message if invalid
    """
    if not token:
        return {
            'valid': False,
            'error': 'No token provided'
        }
    
    # Remove 'Bearer ' prefix if present
    if token.startswith('Bearer '):
        token = token[7:]
    
    try:
        # Get secret key from app config
        secret_key = current_app.config.get('JWT_SECRET_KEY', 'dev-secret-key')
        
        # Decode and verify the token
        payload = jwt.decode(token, secret_key, algorithms=['HS256'])
        
        # Check if token is expired
        exp = payload.get('exp')
        if exp and datetime.utcnow().timestamp() > exp:
            logger.warning("JWT token has expired")
            return {
                'valid': False,
                'error': 'Token expired'
            }
        
        # Get user ID from token
        user_id = payload.get('sub')
        if not user_id:
            logger.warning("JWT token missing subject (user ID)")
            return {
                'valid': False,
                'error': 'Invalid token: missing user ID'
            }
        
        # Check required user ID if specified
        if required_user_id and str(user_id) != str(required_user_id):
            logger.warning(f"JWT user_id {user_id} does not match required {required_user_id}")
            return {
                'valid': False,
                'error': 'Unauthorized: token belongs to different user'
            }
        
        # Check required role if specified
        if required_role:
            roles = payload.get('roles', [])
            if not roles or required_role not in roles:
                logger.warning(f"User {user_id} missing required role: {required_role}")
                return {
                    'valid': False,
                    'error': f'Unauthorized: missing required role {required_role}'
                }
        
        # Token is valid and passes all checks
        return {
            'valid': True,
            'user_id': user_id,
            'roles': payload.get('roles', [])
        }
        
    except jwt.ExpiredSignatureError:
        logger.warning("JWT signature has expired")
        return {
            'valid': False,
            'error': 'Token expired'
        }
    except jwt.InvalidTokenError as e:
        logger.warning(f"Invalid JWT token: {str(e)}")
        return {
            'valid': False,
            'error': f'Invalid token: {str(e)}'
        }
    except Exception as e:
        logger.error(f"Error validating JWT token: {str(e)}")
        return {
            'valid': False,
            'error': f'Error validating token: {str(e)}'
        }

def authenticate_connection(auth_data):
    """
    Authenticate a WebSocket connection using provided credentials.
    
    Args:
        auth_data (dict): Authentication data containing token or credentials
        
    Returns:
        dict: Authentication result with keys:
            - authenticated (bool): Whether connection is authenticated
            - user_id (str, optional): User ID if authenticated
            - error (str, optional): Error message if not authenticated
    """
    if not auth_data or not isinstance(auth_data, dict):
        return {
            'authenticated': False,
            'error': 'Invalid authentication data'
        }
    
    # Check for JWT token
    token = auth_data.get('token')
    if token:
        # Validate JWT
        validation = validate_jwt(token)
        if validation['valid']:
            logger.info(f"Successfully authenticated user {validation['user_id']} via JWT")
            return {
                'authenticated': True,
                'user_id': validation['user_id'],
                'roles': validation.get('roles', [])
            }
        else:
            return {
                'authenticated': False,
                'error': validation['error']
            }
    
    # Alternative: API key authentication (for services)
    api_key = auth_data.get('api_key')
    if api_key:
        # In production, validate API key against secure storage
        valid_api_keys = current_app.config.get('API_KEYS', {})
        if api_key in valid_api_keys:
            service_id = valid_api_keys[api_key]
            logger.info(f"Successfully authenticated service {service_id} via API key")
            return {
                'authenticated': True,
                'service_id': service_id,
                'is_service': True
            }
        else:
            logger.warning("Invalid API key provided")
            return {
                'authenticated': False,
                'error': 'Invalid API key'
            }
    
    # No recognized authentication method found
    return {
        'authenticated': False,
        'error': 'No valid authentication credentials provided'
    }

def check_authorization(user_id, resource, action):
    """
    Check if a user is authorized to perform an action on a resource.
    
    Args:
        user_id (str): User ID
        resource (str): Resource identifier (e.g., 'notification', 'case')
        action (str): Action to perform (e.g., 'read', 'write', 'delete')
        
    Returns:
        bool: True if user is authorized, False otherwise
    """
    # In a real implementation, this would check against a permissions system
    # For now, implementing a simple check
    
    # Admin users can do anything
    admin_users = current_app.config.get('ADMIN_USERS', [])
    if user_id in admin_users:
        return True
    
    # Example of resource-specific checks
    if resource == 'notification':
        # All authenticated users can read notifications
        if action == 'read':
            return True
        # Only admins can create broadcast notifications
        if action == 'broadcast':
            return False
    
    elif resource == 'user_data':
        # Users can only access their own data
        if action == 'read' and resource.startswith(f'user_{user_id}'):
            return True
    
    # Default to denying access if no explicit rule allows it
    logger.warning(f"Authorization denied for user {user_id} to {action} on {resource}")
    return False 