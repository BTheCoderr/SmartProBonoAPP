"""
Audit middleware for comprehensive request/response auditing.
"""
import time
import json
import logging
from functools import wraps
from typing import Dict, Any, Optional
from flask import request, g, current_app, jsonify
from services.audit_service import audit_service
from models.audit import AuditEventType, AuditSeverity

logger = logging.getLogger(__name__)

class AuditMiddleware:
    """Middleware for automatic request/response auditing."""
    
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)
    
    def init_app(self, app):
        """Initialize the middleware with Flask app."""
        app.before_request(self.before_request)
        app.after_request(self.after_request)
        app.teardown_appcontext(self.teardown_request)
    
    def before_request(self):
        """Called before each request."""
        # Start timing
        g.start_time = time.time()
        
        # Generate session ID if not exists
        if not hasattr(g, 'session_id'):
            g.session_id = self._generate_session_id()
        
        # Log request start
        self._log_request_start()
    
    def after_request(self, response):
        """Called after each request."""
        try:
            # Calculate processing time
            processing_time = (time.time() - g.start_time) * 1000  # Convert to milliseconds
            
            # Log the request/response
            self._log_request_complete(response, processing_time)
            
            # Log performance metrics
            self._log_performance_metrics(processing_time, response)
            
            # Log API usage
            self._log_api_usage(processing_time, response)
            
        except Exception as e:
            logger.error(f"Error in audit middleware after_request: {str(e)}")
        
        return response
    
    def teardown_request(self, exception):
        """Called when request context is torn down."""
        if exception:
            self._log_exception(exception)
    
    def _log_request_start(self):
        """Log the start of a request."""
        try:
            # Get request data (excluding sensitive fields)
            request_data = self._sanitize_request_data()
            
            audit_service.log_audit_event(
                event_type=AuditEventType.SYSTEM,
                action="REQUEST_START",
                description=f"Request started: {request.method} {request.path}",
                request_data=request_data,
                metadata={
                    "content_type": request.content_type,
                    "content_length": request.content_length,
                    "query_string": request.query_string.decode() if request.query_string else None
                }
            )
        except Exception as e:
            logger.error(f"Failed to log request start: {str(e)}")
    
    def _log_request_complete(self, response, processing_time_ms):
        """Log the completion of a request."""
        try:
            # Get response data (excluding sensitive fields)
            response_data = self._sanitize_response_data(response)
            
            # Determine event type based on endpoint
            event_type = self._get_event_type_for_endpoint(request.path)
            
            # Determine severity based on status code
            severity = self._get_severity_for_status_code(response.status_code)
            
            audit_service.log_audit_event(
                event_type=event_type,
                action="REQUEST_COMPLETE",
                description=f"Request completed: {request.method} {request.path} - {response.status_code}",
                status_code=response.status_code,
                processing_time_ms=int(processing_time_ms),
                response_data=response_data,
                severity=severity,
                metadata={
                    "content_type": response.content_type,
                    "content_length": response.content_length,
                    "processing_time_ms": processing_time_ms
                }
            )
        except Exception as e:
            logger.error(f"Failed to log request complete: {str(e)}")
    
    def _log_performance_metrics(self, processing_time_ms, response):
        """Log performance metrics."""
        try:
            # Log response time
            audit_service.log_performance_metric(
                metric_type="response_time",
                value=processing_time_ms,
                unit="ms",
                threshold=1000,  # 1 second threshold
                endpoint=request.path,
                user_id=getattr(g, 'user_id', None)
            )
            
            # Log response size if available
            if response.content_length:
                audit_service.log_performance_metric(
                    metric_type="response_size",
                    value=response.content_length,
                    unit="bytes",
                    threshold=1024 * 1024,  # 1MB threshold
                    endpoint=request.path,
                    user_id=getattr(g, 'user_id', None)
                )
            
        except Exception as e:
            logger.error(f"Failed to log performance metrics: {str(e)}")
    
    def _log_api_usage(self, processing_time_ms, response):
        """Log API usage statistics."""
        try:
            # Only log for API endpoints
            if not request.path.startswith('/api/'):
                return
            
            # Get request size
            request_size = request.content_length if request.content_length else 0
            
            # Get response size
            response_size = response.content_length if response.content_length else 0
            
            audit_service.log_api_usage(
                endpoint=request.path,
                method=request.method,
                response_time_ms=int(processing_time_ms),
                status_code=response.status_code,
                user_id=getattr(g, 'user_id', None),
                request_size=request_size,
                response_size=response_size,
                rate_limit_hit=False,  # TODO: Check rate limiting
                metadata={
                    "user_agent": request.headers.get('User-Agent'),
                    "referer": request.headers.get('Referer')
                }
            )
        except Exception as e:
            logger.error(f"Failed to log API usage: {str(e)}")
    
    def _log_exception(self, exception):
        """Log exceptions that occur during request processing."""
        try:
            audit_service.log_audit_event(
                event_type=AuditEventType.SYSTEM,
                action="EXCEPTION",
                description=f"Exception occurred: {str(exception)}",
                severity=AuditSeverity.HIGH,
                error_message=str(exception),
                metadata={
                    "exception_type": type(exception).__name__,
                    "traceback": str(exception)
                }
            )
        except Exception as e:
            logger.error(f"Failed to log exception: {str(e)}")
    
    def _sanitize_request_data(self) -> Dict[str, Any]:
        """Sanitize request data to remove sensitive information."""
        try:
            data = {}
            
            # Add headers (excluding sensitive ones)
            sensitive_headers = {'authorization', 'cookie', 'x-api-key', 'x-auth-token'}
            for key, value in request.headers:
                if key.lower() not in sensitive_headers:
                    data[f"header_{key.lower()}"] = value
            
            # Add form data (excluding sensitive fields)
            if request.form:
                sensitive_fields = {'password', 'token', 'secret', 'key', 'ssn', 'credit_card'}
                for key, value in request.form.items():
                    if key.lower() not in sensitive_fields:
                        data[f"form_{key}"] = value
            
            # Add JSON data (excluding sensitive fields)
            if request.is_json:
                json_data = request.get_json() or {}
                data["json_data"] = self._sanitize_dict(json_data)
            
            # Add query parameters
            if request.args:
                data["query_params"] = dict(request.args)
            
            return data
        except Exception as e:
            logger.error(f"Failed to sanitize request data: {str(e)}")
            return {}
    
    def _sanitize_response_data(self, response) -> Dict[str, Any]:
        """Sanitize response data to remove sensitive information."""
        try:
            data = {
                "status_code": response.status_code,
                "content_type": response.content_type,
                "content_length": response.content_length
            }
            
            # Only log response data for non-sensitive endpoints
            sensitive_endpoints = {'/api/auth/', '/api/login', '/api/register'}
            if not any(endpoint in request.path for endpoint in sensitive_endpoints):
                try:
                    if response.is_json:
                        json_data = response.get_json()
                        if json_data:
                            data["json_data"] = self._sanitize_dict(json_data)
                except Exception:
                    pass  # Skip if response is not JSON
            
            return data
        except Exception as e:
            logger.error(f"Failed to sanitize response data: {str(e)}")
            return {}
    
    def _sanitize_dict(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Recursively sanitize dictionary data."""
        if not isinstance(data, dict):
            return data
        
        sanitized = {}
        sensitive_keys = {'password', 'token', 'secret', 'key', 'ssn', 'credit_card', 'api_key'}
        
        for key, value in data.items():
            if key.lower() in sensitive_keys:
                sanitized[key] = "[REDACTED]"
            elif isinstance(value, dict):
                sanitized[key] = self._sanitize_dict(value)
            elif isinstance(value, list):
                sanitized[key] = [self._sanitize_dict(item) if isinstance(item, dict) else item for item in value]
            else:
                sanitized[key] = value
        
        return sanitized
    
    def _get_event_type_for_endpoint(self, path: str) -> AuditEventType:
        """Determine audit event type based on endpoint."""
        if '/api/auth/' in path or '/login' in path or '/register' in path:
            return AuditEventType.SECURITY
        elif '/api/documents/' in path:
            return AuditEventType.DOCUMENT_ACCESS
        elif '/api/users/' in path:
            return AuditEventType.USER_ACTIVITY
        elif '/api/' in path:
            return AuditEventType.API_USAGE
        else:
            return AuditEventType.SYSTEM
    
    def _get_severity_for_status_code(self, status_code: int) -> AuditSeverity:
        """Determine severity based on HTTP status code."""
        if status_code >= 500:
            return AuditSeverity.HIGH
        elif status_code >= 400:
            return AuditSeverity.MEDIUM
        else:
            return AuditSeverity.LOW
    
    def _generate_session_id(self) -> str:
        """Generate a unique session ID."""
        import uuid
        return str(uuid.uuid4())

def audit_required(event_type: AuditEventType = AuditEventType.USER_ACTIVITY, action: str = "ACCESS"):
    """Decorator to require audit logging for a route."""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                # Log the access attempt
                audit_service.log_audit_event(
                    event_type=event_type,
                    action=action,
                    description=f"Accessing {f.__name__}",
                    metadata={
                        "function_name": f.__name__,
                        "module": f.__module__
                    }
                )
                
                # Execute the original function
                result = f(*args, **kwargs)
                
                # Log successful completion
                audit_service.log_audit_event(
                    event_type=event_type,
                    action=f"{action}_SUCCESS",
                    description=f"Successfully completed {f.__name__}",
                    metadata={
                        "function_name": f.__name__,
                        "module": f.__module__
                    }
                )
                
                return result
                
            except Exception as e:
                # Log the error
                audit_service.log_audit_event(
                    event_type=event_type,
                    action=f"{action}_ERROR",
                    description=f"Error in {f.__name__}: {str(e)}",
                    severity=AuditSeverity.HIGH,
                    error_message=str(e),
                    metadata={
                        "function_name": f.__name__,
                        "module": f.__module__,
                        "exception_type": type(e).__name__
                    }
                )
                raise
        
        return decorated_function
    return decorator

def log_user_activity(activity_type: str, **kwargs):
    """Decorator to log user activity."""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                # Get user ID from context
                user_id = getattr(g, 'user_id', None)
                
                if user_id:
                    audit_service.log_user_activity(
                        user_id=user_id,
                        activity_type=activity_type,
                        page_url=request.path,
                        action=f.__name__,
                        metadata={
                            "function_name": f.__name__,
                            "module": f.__module__,
                            **kwargs
                        }
                    )
                
                return f(*args, **kwargs)
                
            except Exception as e:
                logger.error(f"Failed to log user activity: {str(e)}")
                return f(*args, **kwargs)
        
        return decorated_function
    return decorator

def log_document_access(action: str):
    """Decorator to log document access."""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                # Get document ID from arguments or request
                document_id = kwargs.get('document_id') or request.view_args.get('document_id')
                user_id = getattr(g, 'user_id', None)
                
                if document_id and user_id:
                    audit_service.log_document_access(
                        document_id=document_id,
                        user_id=user_id,
                        action=action,
                        metadata={
                            "function_name": f.__name__,
                            "module": f.__module__
                        }
                    )
                
                return f(*args, **kwargs)
                
            except Exception as e:
                logger.error(f"Failed to log document access: {str(e)}")
                return f(*args, **kwargs)
        
        return decorated_function
    return decorator
