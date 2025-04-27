"""Authentication decorators"""
from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt, verify_jwt_in_request

def admin_required():
    """Decorator to require admin role"""
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if claims.get('roles') != 'admin':
                return jsonify({'error': 'Admin access required'}), 403
            return fn(*args, **kwargs)
        return decorator
    return wrapper

def paralegal_required():
    """Decorator to require paralegal role"""
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if claims.get('roles') not in ['admin', 'paralegal']:
                return jsonify({'error': 'Paralegal access required'}), 403
            return fn(*args, **kwargs)
        return decorator
    return wrapper

def client_required():
    """Decorator to require client role"""
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if not claims.get('roles'):
                return jsonify({'error': 'Client access required'}), 403
            return fn(*args, **kwargs)
        return decorator
    return wrapper 