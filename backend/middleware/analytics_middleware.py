import os
from functools import wraps
from flask import request, g
import time
from typing import Callable

# Only import analytics services if enabled
ANALYTICS_ENABLED = os.getenv('ENABLE_ANALYTICS', 'false').lower() == 'true'

if ANALYTICS_ENABLED:
    try:
        from services.analytics_service import analytics_service
        from services.performance_monitor import performance_monitor
    except ImportError:
        print("Warning: Analytics services not available")
        ANALYTICS_ENABLED = False

class AnalyticsMiddleware:
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """Initialize the middleware with a Flask app."""
        init_analytics_middleware(app)

def track_analytics(f: Callable) -> Callable:
    """Middleware decorator to track request analytics.
    
    This decorator:
    1. Tracks request timing
    2. Records errors
    3. Sends data to both GA4 and custom monitoring
    4. Tracks concurrent users
    """
    @wraps(f)
    async def decorated(*args, **kwargs):
        if not ANALYTICS_ENABLED:
            return await f(*args, **kwargs)
            
        start_time = time.time()
        
        try:
            # Track request start
            g.request_id = str(time.time())  # Simple request ID
            
            # Track concurrent users (active requests)
            performance_monitor.track_concurrent_users(
                performance_monitor.get_peak_concurrent_users() + 1
            )
            
            # Execute the request
            response = await f(*args, **kwargs)
            
            # Calculate execution time
            execution_time = (time.time() - start_time) * 1000  # Convert to ms
            
            # Track successful request
            performance_monitor.track_request_time(
                request.path,
                execution_time
            )
            
            # Track in Google Analytics
            await analytics_service.track_event(
                'api_request',
                {
                    'path': request.path,
                    'method': request.method,
                    'status': response.status_code,
                    'execution_time': execution_time,
                    'user_id': g.get('user_id'),  # If user is authenticated
                }
            )
            
            return response
            
        except Exception as e:
            # Track error in both systems
            error_type = type(e).__name__
            performance_monitor.track_error(error_type, request.path)
            
            await analytics_service.track_event(
                'api_error',
                {
                    'error_type': error_type,
                    'path': request.path,
                    'message': str(e)
                }
            )
            
            raise  # Re-raise the exception
            
        finally:
            # Update concurrent users count
            performance_monitor.track_concurrent_users(
                max(0, performance_monitor.get_peak_concurrent_users() - 1)
            )
    
    return decorated

def init_analytics_middleware(app):
    """Initialize analytics middleware for the Flask app."""
    if not ANALYTICS_ENABLED:
        return
    
    @app.before_request
    def before_request():
        g.start_time = time.time()
        
        # Track page view in GA4 for non-API routes
        if not request.path.startswith('/api/'):
            analytics_service.track_event(
                'page_view',
                {
                    'page_path': request.path,
                    'referrer': request.referrer,
                    'user_agent': request.user_agent.string
                }
            )
    
    @app.after_request
    def after_request(response):
        # Add performance monitoring headers
        if hasattr(g, 'start_time'):
            execution_time = (time.time() - g.start_time) * 1000
            response.headers['X-Response-Time'] = f"{execution_time:.2f}ms"
        
        return response
    
    @app.teardown_request
    def teardown_request(exception=None):
        # Cleanup any resources
        if exception:
            performance_monitor.track_error(
                type(exception).__name__ if exception else 'Unknown',
                request.path
            ) 