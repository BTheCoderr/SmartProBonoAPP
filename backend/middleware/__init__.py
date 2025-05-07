"""Middleware package initialization"""
import logging
from middleware.security import SecurityMiddleware
from middleware.rate_limiting import RateLimitingMiddleware
from middleware.analytics_middleware import AnalyticsMiddleware

logger = logging.getLogger(__name__)

def init_middleware(app):
    """Initialize all middleware for the application"""
    try:
        # Initialize security middleware
        SecurityMiddleware(app)
        logger.info("Security middleware initialized successfully")
        
        # Initialize rate limiting middleware
        RateLimitingMiddleware(app)
        logger.info("Rate limiting middleware initialized successfully")
        
        # Initialize analytics middleware
        AnalyticsMiddleware(app)
        logger.info("Analytics middleware initialized successfully")
        
    except Exception as e:
        logger.error(f"Error initializing middleware: {str(e)}")
        raise 