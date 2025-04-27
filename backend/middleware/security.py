"""Security middleware for the application."""
from functools import wraps
from flask import request, abort, current_app
import re
from datetime import datetime
from backend.config.security import (
    SECURITY_HEADERS,
    RATE_LIMIT_CONFIG,
    PASSWORD_POLICY,
    API_SECURITY,
    SENSITIVE_FIELDS
)
from backend.utils.encryption import encrypt_field, mask_field

class SecurityMiddleware:
    """Middleware for handling security concerns."""
    
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)
    
    def init_app(self, app):
        """Initialize the security middleware with the Flask app."""
        @app.before_request
        def before_request():
            """Handle security checks before each request."""
            if API_SECURITY['require_https'] and not request.is_secure:
                abort(403, description="HTTPS required")
            
            self._validate_content_type()
            self._check_rate_limit()
        
        @app.after_request
        def after_request(response):
            """Add security headers to response."""
            for header, value in SECURITY_HEADERS.items():
                response.headers[header] = value
            return response
    
    def _validate_content_type(self):
        """Validate the Content-Type header."""
        if request.method in ['POST', 'PUT'] and API_SECURITY['validate_content_type']:
            content_type = request.headers.get('Content-Type', '')
            if not content_type.startswith('application/json'):
                abort(415, description="Content-Type must be application/json")
    
    def _check_rate_limit(self):
        """Check rate limiting for the current request."""
        # Implementation would use Redis or similar for production
        pass

def validate_password(password):
    """Validate password against policy."""
    if len(password) < PASSWORD_POLICY['min_length']:
        return False, "Password too short"
    
    if len(password) > PASSWORD_POLICY['max_length']:
        return False, "Password too long"
    
    if PASSWORD_POLICY['require_uppercase'] and not re.search(r'[A-Z]', password):
        return False, "Password must contain uppercase letter"
    
    if PASSWORD_POLICY['require_lowercase'] and not re.search(r'[a-z]', password):
        return False, "Password must contain lowercase letter"
    
    if PASSWORD_POLICY['require_numbers'] and not re.search(r'\d', password):
        return False, "Password must contain number"
    
    if PASSWORD_POLICY['require_special'] and not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False, "Password must contain special character"
    
    return True, None

def sanitize_input(data):
    """Sanitize input data."""
    if isinstance(data, dict):
        return {k: sanitize_input(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [sanitize_input(x) for x in data]
    elif isinstance(data, str):
        # Basic XSS protection
        data = data.replace('<', '&lt;').replace('>', '&gt;')
        # SQL injection protection
        data = re.sub(r'(\b(SELECT|INSERT|UPDATE|DELETE|DROP|UNION|ALTER)\b)', '', data, flags=re.IGNORECASE)
        return data
    return data

def protect_sensitive_data(data):
    """Protect sensitive data according to configuration."""
    if not isinstance(data, dict):
        return data
    
    protected_data = data.copy()
    for field, protection in SENSITIVE_FIELDS.items():
        if field in protected_data:
            if protection == 'encrypt':
                protected_data[field] = encrypt_field(protected_data[field])
            elif protection == 'mask':
                protected_data[field] = mask_field(protected_data[field])
    
    return protected_data

def require_https(f):
    """Decorator to require HTTPS."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not request.is_secure and current_app.config['ENV'] == 'production':
            abort(403, description="HTTPS required")
        return f(*args, **kwargs)
    return decorated_function

def validate_schema(schema):
    """Decorator to validate request schema."""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not request.is_json:
                abort(400, description="Request must be JSON")
            
            data = request.get_json()
            errors = schema.validate(data)
            if errors:
                abort(400, description=str(errors))
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator 