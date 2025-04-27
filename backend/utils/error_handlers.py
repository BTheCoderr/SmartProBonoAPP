from flask import jsonify
from functools import wraps
import logging

logger = logging.getLogger(__name__)

class APIError(Exception):
    """Base class for API errors"""
    
    def __init__(self, message, status_code=400, payload=None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.payload = payload
    
    def to_dict(self):
        result = {
            'success': False,
            'error': self.message
        }
        if self.payload:
            result.update(self.payload)
        return result

class ValidationError(APIError):
    """Validation error for invalid input data"""
    
    def __init__(self, message, errors=None, status_code=400):
        super().__init__(message, status_code)
        self.errors = errors
    
    def to_dict(self):
        result = super().to_dict()
        if self.errors:
            result['errors'] = self.errors
        return result

class AuthError(APIError):
    """Authentication error for unauthorized access"""
    
    def __init__(self, message, status_code=401):
        super().__init__(message, status_code)

class NotFoundError(APIError):
    """Not found error for missing resources"""
    
    def __init__(self, message='Resource not found', status_code=404):
        super().__init__(message, status_code)

def handle_exceptions(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error in {f.__name__}: {str(e)}")
            return jsonify({
                'error': 'Internal server error',
                'message': str(e)
            }), 500
    return decorated_function

def register_error_handlers(app):
    """Register error handlers for the Flask app"""
    
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'error': 'Bad request',
            'message': str(error)
        }), 400
    
    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({
            'error': 'Unauthorized',
            'message': str(error)
        }), 401
    
    @app.errorhandler(403)
    def forbidden(error):
        return jsonify({
            'error': 'Forbidden',
            'message': str(error)
        }), 403
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'error': 'Not found',
            'message': str(error)
        }), 404
    
    @app.errorhandler(500)
    def server_error(error):
        logger.error(f"Server error: {str(error)}")
        return jsonify({
            'error': 'Internal server error',
            'message': str(error)
        }), 500 