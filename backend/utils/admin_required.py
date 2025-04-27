"""
Admin authorization middleware
"""
from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from utils.logging_setup import get_logger

# Set up logging
logger = get_logger('utils.admin_required')

# List of admin users (in a real app, this would be stored in a database)
ADMIN_USERS = ['admin1', 'admin2', 'super_admin']

def admin_required(fn):
    """
    Decorator to check if the current user has admin privileges.
    
    Args:
        fn: The function to decorate
        
    Returns:
        The decorated function
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        # Verify JWT is valid
        verify_jwt_in_request()
        
        # Get current user ID
        current_user = get_jwt_identity()
        
        # Check if user is in admin list
        if current_user not in ADMIN_USERS:
            logger.warning(f"Unauthorized admin access attempt by user {current_user}")
            return jsonify({"success": False, "message": "Admin privileges required"}), 403
            
        logger.debug(f"Admin access granted to user {current_user}")
        return fn(*args, **kwargs)
        
    return wrapper 