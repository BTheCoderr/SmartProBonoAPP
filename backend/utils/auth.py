from functools import wraps
from flask import request, jsonify, abort, g, current_app
import jwt
from datetime import datetime, timedelta
import os
from typing import List, Union, Callable

# Define user roles and their hierarchy
ROLES = {
    'client': 0,
    'lawyer': 10,
    'admin': 20,
    'superadmin': 30
}

# Define permissions for each endpoint
PERMISSIONS = {
    'view_queue': ['client', 'lawyer', 'admin', 'superadmin'],
    'manage_queue': ['lawyer', 'admin', 'superadmin'],
    'admin_actions': ['admin', 'superadmin'],
    'system_config': ['superadmin']
}

def require_auth(f: Callable) -> Callable:
    """Decorator to require authentication for a route."""
    @wraps(f)
    def decorated(*args, **kwargs):
        if not g.user:
            return jsonify({'error': 'Authentication required'}), 401
        return f(*args, **kwargs)
    return decorated

def require_role(*roles: str) -> Callable:
    """Decorator to require specific role(s) for a route."""
    def decorator(f: Callable) -> Callable:
        @wraps(f)
        def decorated(*args, **kwargs):
            if not g.user:
                return jsonify({'error': 'Authentication required'}), 401
            if g.user.get('role') not in roles:
                return jsonify({'error': 'Insufficient permissions'}), 403
            return f(*args, **kwargs)
        return decorated
    return decorator

def require_permission(permission: str) -> Callable:
    """Decorator to require specific permission for a route."""
    def decorator(f: Callable) -> Callable:
        @wraps(f)
        def decorated(*args, **kwargs):
            if not g.user:
                return jsonify({'error': 'Authentication required'}), 401
            user_permissions = g.user.get('permissions', [])
            if permission not in user_permissions:
                return jsonify({'error': 'Insufficient permissions'}), 403
            return f(*args, **kwargs)
        return decorated
    return decorator

def create_token(user_data):
    """Create a new JWT token"""
    token = jwt.encode({
        'user_id': user_data.get('id'),
        'email': user_data.get('email'),
        'role': user_data.get('role', 'client'),
        'exp': datetime.utcnow() + timedelta(hours=24)
    }, current_app.config['JWT_SECRET_KEY'], algorithm="HS256")
    
    return token 