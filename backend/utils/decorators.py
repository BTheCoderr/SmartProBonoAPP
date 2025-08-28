"""
Decorators for route functions.
"""
from functools import wraps
from flask import request, jsonify, current_app
import logging
import time

logger = logging.getLogger(__name__)

def token_required(f):
    """
    Decorator for routes that require token authentication.
    Similar to login_required but allows for custom token formats.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        # Placeholder for when custom token validation is needed
        # For now, just pass to login_required
        from utils.auth import login_required
        return login_required(f)(*args, **kwargs)
    return decorated

def admin_role_required(f):
    """
    Decorator for routes that require admin role.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        from utils.auth import admin_required
        return admin_required(f)(*args, **kwargs)
    return decorated

def log_route_access(f):
    """
    Decorator to log access to routes.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        start_time = time.time()
        method = request.method
        path = request.path
        ip = request.remote_addr
        
        logger.info(f"Access: {method} {path} from {ip}")
        
        response = f(*args, **kwargs)
        
        duration = time.time() - start_time
        status_code = response.status_code if hasattr(response, 'status_code') else 200
        
        logger.info(f"Completed: {method} {path} - {status_code} in {duration:.4f}s")
        
        return response
    return decorated

def handle_exceptions(f):
    """
    Decorator to handle exceptions and return appropriate responses.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error in {f.__name__}: {str(e)}")
            return jsonify({"error": str(e)}), 500
    return decorated 