"""Rate limiting middleware for the API"""
import time
from functools import wraps
from flask import request, jsonify, current_app, g
from typing import Dict, Any, Optional, Callable
import logging

logger = logging.getLogger(__name__)

class RateLimiter:
    """Rate limiting implementation using Redis"""
    
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)
    
    def init_app(self, app):
        """Initialize with Flask app"""
        self.app = app
        
        # Initialize with default rate limits if not set
        if not hasattr(app.config, 'RATE_LIMITS'):
            app.config['RATE_LIMITS'] = {
                'default': '100/minute',
                'login': '5/minute',
                'register': '3/minute',
                'forgot_password': '3/minute',
                'api': '200/minute'
            }
    
    def _get_rate_limit_data(self, key: str) -> Dict[str, Any]:
        """Get rate limit data from Redis"""
        redis_client = current_app.redis
        data = redis_client.hgetall(f"rate_limit:{key}")
        
        if not data:
            return {'count': 0, 'reset_at': int(time.time()) + 60}
        
        return {
            'count': int(data.get(b'count', 0)),
            'reset_at': int(data.get(b'reset_at', int(time.time()) + 60))
        }
    
    def _update_rate_limit(self, key: str, limit: int) -> Dict[str, Any]:
        """Update rate limit in Redis"""
        redis_client = current_app.redis
        pipe = redis_client.pipeline()
        
        now = int(time.time())
        rate_limit_key = f"rate_limit:{key}"
        
        # Get current data
        data = self._get_rate_limit_data(key)
        
        # Reset if expired
        if data['reset_at'] <= now:
            data['count'] = 1
            data['reset_at'] = now + 60  # Reset every minute
        else:
            data['count'] += 1
        
        # Update in Redis
        pipe.hset(rate_limit_key, 'count', data['count'])
        pipe.hset(rate_limit_key, 'reset_at', data['reset_at'])
        pipe.expireat(rate_limit_key, data['reset_at'])
        pipe.execute()
        
        # Calculate remaining
        data['limit'] = limit
        data['remaining'] = max(0, limit - data['count'])
        data['exceeded'] = data['count'] > limit
        
        return data

    def limit(self, limit_name: str = 'default') -> Callable:
        """Rate limiting decorator"""
        def decorator(f: Callable) -> Callable:
            @wraps(f)
            def decorated_function(*args, **kwargs):
                # Skip rate limiting in test mode
                if current_app.config.get('TESTING', False):
                    return f(*args, **kwargs)
                
                # Parse rate limit string
                limit_string = current_app.config['RATE_LIMITS'].get(
                    limit_name, 
                    current_app.config['RATE_LIMITS']['default']
                )
                limit_value, period = limit_string.split('/')
                limit = int(limit_value)
                
                # Get identifier based on IP or user
                if hasattr(g, 'user') and g.user:
                    identifier = f"{limit_name}:{g.user.id}"
                else:
                    identifier = f"{limit_name}:{request.remote_addr}"
                
                try:
                    rate_data = self._update_rate_limit(identifier, limit)
                    
                    # Set headers
                    response = f(*args, **kwargs)
                    if isinstance(response, tuple):
                        response_obj, status_code = response
                    else:
                        response_obj, status_code = response, 200
                    
                    # Add rate limit headers
                    headers = {
                        'X-RateLimit-Limit': str(rate_data['limit']),
                        'X-RateLimit-Remaining': str(rate_data['remaining']),
                        'X-RateLimit-Reset': str(rate_data['reset_at'])
                    }
                    
                    # Handle custom response objects
                    if hasattr(response_obj, 'headers'):
                        for key, value in headers.items():
                            response_obj.headers[key] = value
                    
                    # Check if rate limit exceeded
                    if rate_data['exceeded']:
                        logger.warning(f"Rate limit exceeded for {identifier}")
                        error_response = jsonify({
                            'error': 'Rate limit exceeded',
                            'retry_after': rate_data['reset_at'] - int(time.time())
                        })
                        error_response.status_code = 429
                        for key, value in headers.items():
                            error_response.headers[key] = value
                        error_response.headers['Retry-After'] = str(rate_data['reset_at'] - int(time.time()))
                        return error_response
                    
                    return response
                    
                except Exception as e:
                    logger.exception(f"Error in rate limiting: {str(e)}")
                    # If rate limiting fails, allow the request to pass through
                    return f(*args, **kwargs)
                    
            return decorated_function
        return decorator

# Create a singleton instance
rate_limiter = RateLimiter() 