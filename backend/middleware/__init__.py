"""
Middleware package for the backend API.
"""

def init_middleware(app):
    """Initialize middleware for the Flask app"""
    try:
        from .audit_middleware import init_audit_middleware
        init_audit_middleware(app)
        print("✅ Audit middleware initialized")
    except ImportError as e:
        print(f"⚠️ Audit middleware not available: {e}")
    
    try:
        from .rate_limiting import init_rate_limiting
        init_rate_limiting(app)
        print("✅ Rate limiting middleware initialized")
    except ImportError as e:
        print(f"⚠️ Rate limiting middleware not available: {e}")
    
    try:
        from .validation import init_validation_middleware
        init_validation_middleware(app)
        print("✅ Validation middleware initialized")
    except ImportError as e:
        print(f"⚠️ Validation middleware not available: {e}")

__all__ = ['init_middleware'] 