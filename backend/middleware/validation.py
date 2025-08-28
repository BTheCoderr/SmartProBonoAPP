"""
Request validation middleware.
"""
from functools import wraps
from flask import request, jsonify
import logging

logger = logging.getLogger(__name__)

def validate_json_request(required_fields=None):
    """
    Decorator to validate JSON request body.
    
    Args:
        required_fields: List of required fields in the request body
        
    Returns:
        Decorated function
    """
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            # Check if request has JSON body
            if not request.is_json:
                return jsonify({"error": "Request must be JSON"}), 400
                
            data = request.get_json()
            
            # Check required fields
            if required_fields:
                missing_fields = [field for field in required_fields if field not in data]
                if missing_fields:
                    return jsonify({
                        "error": "Missing required fields",
                        "missing_fields": missing_fields
                    }), 400
                    
            return f(*args, **kwargs)
        return decorated
    return decorator

def validate_query_params(required_params=None):
    """
    Decorator to validate query parameters.
    
    Args:
        required_params: List of required query parameters
        
    Returns:
        Decorated function
    """
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            # Check required query parameters
            if required_params:
                missing_params = [param for param in required_params if param not in request.args]
                if missing_params:
                    return jsonify({
                        "error": "Missing required query parameters",
                        "missing_params": missing_params
                    }), 400
                    
            return f(*args, **kwargs)
        return decorated
    return decorator 