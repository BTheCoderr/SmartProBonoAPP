"""
Rate limiting middleware.
"""
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Initialize rate limiter - will be configured with the app in extensions.py
rate_limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

# Define rate limit by endpoint
document_upload_limit = "10 per minute"
api_call_limit = "60 per minute"
login_attempt_limit = "5 per minute"

# Define custom rate limit function
def get_user_limit(endpoint_name):
    """
    Get rate limit for a specific endpoint.
    
    Args:
        endpoint_name: Name of the endpoint
        
    Returns:
        Rate limit string
    """
    limits = {
        "document_upload": document_upload_limit,
        "api_call": api_call_limit,
        "login_attempt": login_attempt_limit
    }
    
    return limits.get(endpoint_name, "30 per minute")

# Shorthand function for rate limiting a route
def rate_limit(endpoint_name):
    """
    Decorator for rate limiting a route.
    
    Args:
        endpoint_name: Name of the endpoint
        
    Returns:
        Rate limiter decorator
    """
    return rate_limiter.limit(get_user_limit(endpoint_name)) 