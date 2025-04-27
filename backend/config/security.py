"""Security configuration for the application."""
from datetime import timedelta

# Security Headers
SECURITY_HEADERS = {
    'Strict-Transport-Security': 'max-age=31536000; includeSubDomains',
    'X-Content-Type-Options': 'nosniff',
    'X-Frame-Options': 'SAMEORIGIN',
    'X-XSS-Protection': '1; mode=block',
    'Content-Security-Policy': "default-src 'self'; script-src 'self' 'unsafe-inline' 'unsafe-eval'; style-src 'self' 'unsafe-inline';",
    'Referrer-Policy': 'strict-origin-when-cross-origin'
}

# Rate Limiting
RATE_LIMIT_CONFIG = {
    'default': '100 per minute',
    'login': '5 per minute',
    'register': '3 per minute',
    'forgot_password': '3 per minute',
    'api': '1000 per hour'
}

# Password Policy
PASSWORD_POLICY = {
    'min_length': 12,
    'require_uppercase': True,
    'require_lowercase': True,
    'require_numbers': True,
    'require_special': True,
    'max_length': 128
}

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

# API Security
API_SECURITY = {
    'require_https': True,
    'validate_content_type': True,
    'validate_schemas': True,
    'sanitize_inputs': True,
    'encrypt_sensitive_data': True
}

# Sensitive Data Fields (for encryption/masking)
SENSITIVE_FIELDS = {
    'ssn': 'encrypt',
    'dob': 'encrypt',
    'phone': 'mask',
    'email': 'mask',
    'address': 'mask',
    'case_details': 'encrypt'
} 