"""Security middleware for the application."""
import logging
from functools import wraps
from flask import request, jsonify, current_app
import re
from datetime import datetime
from werkzeug.security import check_password_hash
from config.security import (
    SECURITY_HEADERS,
    RATE_LIMIT_CONFIG,
    PASSWORD_POLICY,
    API_SECURITY,
    SENSITIVE_FIELDS,
    ALLOWED_ORIGINS,
    ALLOWED_METHODS,
    ALLOWED_HEADERS,
    MAX_CONTENT_LENGTH,
    RATE_LIMIT_RULES,
    AUTH_REQUIRED_ROUTES,
    EXEMPT_ROUTES,
    API_KEY_HEADER,
    JWT_SECRET_KEY
)
from utils.encryption import encrypt_field, mask_field

logger = logging.getLogger(__name__)

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
            # Skip security checks for exempt routes
            if request.path in EXEMPT_ROUTES:
                return None

            # CORS check
            origin = request.headers.get('Origin')
            if origin and origin not in ALLOWED_ORIGINS:
                return jsonify({'error': 'Invalid origin'}), 403

            # Method check
            if request.method not in ALLOWED_METHODS:
                return jsonify({'error': 'Method not allowed'}), 405

            # Content length check
            content_length = request.content_length
            if content_length and content_length > MAX_CONTENT_LENGTH:
                return jsonify({'error': 'Request too large'}), 413

            # API key check for protected routes
            if request.path in AUTH_REQUIRED_ROUTES:
                api_key = request.headers.get(API_KEY_HEADER)
                if not api_key or not self._validate_api_key(api_key):
                    return jsonify({'error': 'Invalid API key'}), 401

            # Rate limiting
            if not self._check_rate_limit(request):
                return jsonify({'error': 'Rate limit exceeded'}), 429

            return None

        @app.after_request
        def after_request(response):
            """Add security headers to response."""
            for header, value in SECURITY_HEADERS.items():
                response.headers[header] = value
            return response
    
    def _validate_api_key(self, api_key):
        """Validate the API key"""
        return check_password_hash(current_app.config['API_KEY_HASH'], api_key)

    def _check_rate_limit(self, request):
        """Check if the request exceeds rate limits"""
        client_ip = request.remote_addr
        path = request.path

        # Get applicable rate limit rule
        rule = next((r for r in RATE_LIMIT_RULES if r['path'] == path), None)
        if not rule:
            return True

        # Check rate limit using Redis
        key = f"rate_limit:{client_ip}:{path}"
        try:
            current = current_app.redis.get(key)
            if current and int(current) >= rule['limit']:
                return False
            
            # Update counter
            if current:
                current_app.redis.incr(key)
            else:
                current_app.redis.setex(key, rule['window'], 1)
            
            return True
        except Exception as e:
            current_app.logger.error(f"Rate limit check failed: {str(e)}")
            return True  # Allow request if rate limiting fails

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

def requires_encryption(f):
    """Decorator to ensure sensitive data is encrypted"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            if request.is_json:
                sensitive_fields = current_app.config.get('SENSITIVE_FIELDS', [])
                data = request.json
                for field in sensitive_fields:
                    if field in data:
                        data[field] = encrypt_field(data[field])
            return f(*args, **kwargs)
        except Exception as e:
            logger.error(f"Encryption error: {str(e)}")
            return jsonify({"error": "Failed to process sensitive data"}), 500
    return decorated_function

def mask_sensitive_data(data, fields_to_mask=None):
    """Mask sensitive data in the response"""
    if not data or not fields_to_mask:
        return data

    if isinstance(data, dict):
        for field in fields_to_mask:
            if field in data:
                data[field] = mask_field(data[field])
    elif isinstance(data, list):
        for item in data:
            mask_sensitive_data(item, fields_to_mask)

    return data 