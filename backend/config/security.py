"""Security configuration for the application."""
from datetime import timedelta

# CORS settings
ALLOWED_ORIGINS = [
    'http://localhost:3000',
    'http://localhost:3100',
    'https://smartprobono.org',
    'https://www.smartprobono.org'
]

ALLOWED_METHODS = ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS']

ALLOWED_HEADERS = [
    'Content-Type',
    'Authorization',
    'X-API-Key',
    'X-Requested-With',
    'Accept'
]

# Request size limits
MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10MB

# Rate limiting rules
RATE_LIMIT_RULES = [
    {'path': '/api/forms', 'limit': 100, 'window': 3600},  # 100 requests per hour
    {'path': '/api/documents', 'limit': 50, 'window': 3600},  # 50 requests per hour
    {'path': '/api/auth', 'limit': 20, 'window': 3600}  # 20 requests per hour
]

# Authentication settings
AUTH_REQUIRED_ROUTES = [
    '/api/forms',
    '/api/documents',
    '/api/analytics'
]

EXEMPT_ROUTES = [
    '/health',
    '/api/auth/login',
    '/api/auth/register'
]

API_KEY_HEADER = 'X-API-Key'
JWT_SECRET_KEY = 'your-secret-key'  # Change in production

# Security headers
SECURITY_HEADERS = {
    'X-Frame-Options': 'SAMEORIGIN',
    'X-XSS-Protection': '1; mode=block',
    'X-Content-Type-Options': 'nosniff',
    'Strict-Transport-Security': 'max-age=31536000; includeSubDomains',
    'Content-Security-Policy': "default-src 'self'"
}

# Rate limiting configuration
RATE_LIMIT_CONFIG = {
    'default': '100 per hour',
    'auth': '20 per hour'
}

# Password policy
PASSWORD_POLICY = {
    'min_length': 8,
    'require_uppercase': True,
    'require_lowercase': True,
    'require_numbers': True,
    'require_special': True
}

# API security settings
API_SECURITY = {
    'require_https': True,
    'validate_content_type': True,
    'max_token_age': 3600
}

# Fields to be treated as sensitive
SENSITIVE_FIELDS = [
    'password',
    'ssn',
    'credit_card',
    'bank_account'
]

# JWT Configuration
JWT_CONFIG = {
    'access_token_expires': timedelta(minutes=15),
    'refresh_token_expires': timedelta(days=30),
    'blacklist_enabled': True,
    'blacklist_token_checks': ['access', 'refresh'],
    'csrf_protect': True,
    'cookie_secure': True,
    'cookie_samesite': 'Lax'
}

# Session Configuration
SESSION_CONFIG = {
    'permanent': True,
    'permanent_session_lifetime': timedelta(days=1),
    'secure': True,
    'httponly': True,
    'samesite': 'Lax'
}

# CORS Configuration
CORS_CONFIG = {
    'resources': r'/api/*',
    'origins': ['https://smartprobono.org', 'https://app.smartprobono.org'],
    'methods': ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
    'allow_headers': ['Content-Type', 'Authorization'],
    'expose_headers': ['Content-Range', 'X-Total-Count'],
    'supports_credentials': True,
    'max_age': 600
}

# File Upload Configuration
UPLOAD_CONFIG = {
    'max_content_length': 16 * 1024 * 1024,  # 16MB
    'allowed_extensions': {'pdf', 'png', 'jpg', 'jpeg', 'doc', 'docx'},
    'upload_folder': 'uploads',
    'scan_uploads': True,
    'sanitize_filenames': True
} 