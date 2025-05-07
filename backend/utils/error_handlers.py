from flask import jsonify, current_app
from functools import wraps
import logging
from sqlalchemy.exc import SQLAlchemyError
from marshmallow import ValidationError
from werkzeug.exceptions import HTTPException

logger = logging.getLogger(__name__)

class APIError(Exception):
    """Base class for API errors"""
    
    def __init__(self, message, status_code=400, payload=None):
        super().__init__()
        self.message = message
        self.status_code = status_code
        self.payload = payload
    
    def to_dict(self):
        rv = dict(self.payload or {})
        rv['message'] = self.message
        rv['status_code'] = self.status_code
        return rv

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

def handle_api_error(f):
    """Decorator to handle API errors consistently."""
    @wraps(f)
    def wrapped(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except ValidationError as e:
            return jsonify({
                'error': 'Validation error',
                'details': e.messages
            }), 400
        except SQLAlchemyError as e:
            current_app.logger.error(f"Database error: {str(e)}")
            return jsonify({
                'error': 'Database error occurred',
                'message': 'An error occurred while processing your request'
            }), 500
        except HTTPException as e:
            return jsonify({
                'error': e.name,
                'message': e.description
            }), e.code
        except APIError as e:
            return jsonify(e.to_dict()), e.status_code
        except Exception as e:
            current_app.logger.error(f"Unexpected error: {str(e)}")
            return jsonify({
                'error': 'Internal server error',
                'message': 'An unexpected error occurred'
            }), 500
    return wrapped

def validation_error(message, errors=None):
    """Create a validation error response."""
    return APIError(
        message=message,
        status_code=400,
        payload={'errors': errors} if errors else None
    )

def not_found_error(message):
    """Create a not found error response."""
    return APIError(message=message, status_code=404)

def unauthorized_error(message="Unauthorized"):
    """Create an unauthorized error response."""
    return APIError(message=message, status_code=401)

def forbidden_error(message="Forbidden"):
    """Create a forbidden error response."""
    return APIError(message=message, status_code=403)

def server_error(message="Internal server error"):
    """Create a server error response."""
    return APIError(message=message, status_code=500)

def handle_validation_error(error):
    """Handle marshmallow validation errors."""
    return jsonify({
        'error': 'Validation error',
        'details': error.messages
    }), 400

def handle_sqlalchemy_error(error):
    """Handle SQLAlchemy errors."""
    current_app.logger.error(f"Database error: {str(error)}")
    return jsonify({
        'error': 'Database error',
        'message': 'An error occurred while processing your request'
    }), 500

def handle_http_error(error):
    """Handle HTTP errors."""
    return jsonify({
        'error': error.name,
        'message': error.description
    }), error.code

def handle_generic_error(error):
    """Handle generic errors."""
    current_app.logger.error(f"Unexpected error: {str(error)}")
    return jsonify({
        'error': 'Internal server error',
        'message': 'An unexpected error occurred'
    }), 500

def register_error_handlers(app):
    """Register error handlers with the Flask app."""
    app.register_error_handler(ValidationError, handle_validation_error)
    app.register_error_handler(SQLAlchemyError, handle_sqlalchemy_error)
    app.register_error_handler(HTTPException, handle_http_error)
    app.register_error_handler(Exception, handle_generic_error)

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