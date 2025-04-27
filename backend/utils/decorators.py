"""
Utility decorators for route handlers
"""
import functools
from flask import jsonify, current_app
import logging
from functools import wraps
from flask import request
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity

logger = logging.getLogger(__name__)

def handle_exceptions(f):
    """
    Decorator to standardize exception handling in route handlers
    
    Args:
        f: The route handler function to wrap
        
    Returns:
        The wrapped function
    """
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            # Log the error
            logger.error(f"Error in {f.__name__}: {str(e)}", exc_info=True)
            
            # Return standardized error response
            return jsonify({
                'error': str(e),
                'endpoint': f.__name__
            }), 500
    
    return wrapper

def validate_json_request(required_fields=None):
    """
    Decorator to validate that a request has a JSON body with required fields
    
    Args:
        required_fields (list, optional): List of required field names
        
    Returns:
        The decorator function
    """
    def decorator(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            from flask import request
            
            # Check for JSON body
            if not request.is_json:
                return jsonify({
                    'error': 'Request must be JSON',
                    'endpoint': f.__name__
                }), 400
            
            # Get JSON data
            data = request.get_json()
            
            # Check required fields if any
            if required_fields:
                missing_fields = [field for field in required_fields if field not in data]
                if missing_fields:
                    return jsonify({
                        'error': f'Missing required fields: {", ".join(missing_fields)}',
                        'endpoint': f.__name__
                    }), 400
            
            # Continue to the handler
            return f(*args, **kwargs)
        
        return wrapper
    
    return decorator 

def token_required(f):
    """Decorator to check valid JWT token."""
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            verify_jwt_in_request()
            return f(*args, **kwargs)
        except Exception as e:
            return jsonify({'error': 'Token is invalid or missing'}), 401
    return decorated 