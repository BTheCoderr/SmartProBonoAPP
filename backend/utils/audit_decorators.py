"""
Enhanced audit decorators for comprehensive system auditing.
"""
import time
import logging
from functools import wraps
from typing import Dict, Any, Optional, Callable
from flask import request, g, jsonify, current_app
from services.audit_service import audit_service
from models.audit import AuditEventType, AuditSeverity

logger = logging.getLogger(__name__)

def audit_route(
    event_type: AuditEventType = AuditEventType.USER_ACTIVITY,
    action: str = "ACCESS",
    severity: AuditSeverity = AuditSeverity.LOW,
    include_request_data: bool = True,
    include_response_data: bool = True,
    sensitive_fields: Optional[list] = None
):
    """
    Comprehensive audit decorator for routes.
    
    Args:
        event_type: Type of audit event
        action: Action being performed
        severity: Severity level
        include_request_data: Whether to include request data
        include_response_data: Whether to include response data
        sensitive_fields: List of sensitive field names to redact
    """
    def decorator(f: Callable) -> Callable:
        @wraps(f)
        def decorated_function(*args, **kwargs):
            start_time = time.time()
            request_data = None
            response_data = None
            error_message = None
            status_code = 200
            
            try:
                # Log request start
                if include_request_data:
                    request_data = _extract_request_data(sensitive_fields)
                
                audit_service.log_audit_event(
                    event_type=event_type,
                    action=f"{action}_START",
                    description=f"Starting {f.__name__}",
                    request_data=request_data,
                    severity=severity,
                    metadata={
                        "function_name": f.__name__,
                        "module": f.__module__,
                        "args_count": len(args),
                        "kwargs_keys": list(kwargs.keys())
                    }
                )
                
                # Execute the function
                result = f(*args, **kwargs)
                
                # Calculate processing time
                processing_time = (time.time() - start_time) * 1000
                
                # Extract response data
                if include_response_data and hasattr(result, 'get_json'):
                    try:
                        response_data = result.get_json()
                    except Exception:
                        response_data = {"status": "non-json-response"}
                
                # Log successful completion
                audit_service.log_audit_event(
                    event_type=event_type,
                    action=f"{action}_SUCCESS",
                    description=f"Successfully completed {f.__name__}",
                    response_data=response_data,
                    processing_time_ms=int(processing_time),
                    severity=AuditSeverity.LOW,
                    metadata={
                        "function_name": f.__name__,
                        "module": f.__module__,
                        "processing_time_ms": processing_time
                    }
                )
                
                return result
                
            except Exception as e:
                processing_time = (time.time() - start_time) * 1000
                error_message = str(e)
                
                # Log the error
                audit_service.log_audit_event(
                    event_type=event_type,
                    action=f"{action}_ERROR",
                    description=f"Error in {f.__name__}: {error_message}",
                    error_message=error_message,
                    processing_time_ms=int(processing_time),
                    severity=AuditSeverity.HIGH,
                    metadata={
                        "function_name": f.__name__,
                        "module": f.__module__,
                        "exception_type": type(e).__name__,
                        "processing_time_ms": processing_time
                    }
                )
                
                # Re-raise the exception
                raise
        
        return decorated_function
    return decorator

def security_audit(
    action: str = "ACCESS",
    check_permissions: bool = True,
    log_failed_attempts: bool = True
):
    """
    Security-focused audit decorator.
    
    Args:
        action: Security action being performed
        check_permissions: Whether to check user permissions
        log_failed_attempts: Whether to log failed access attempts
    """
    def decorator(f: Callable) -> Callable:
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user_id = getattr(g, 'user_id', None)
            ip_address = request.remote_addr
            user_agent = request.headers.get('User-Agent')
            
            try:
                # Log security event
                audit_service.log_security_event(
                    event_type=f"security_{action.lower()}",
                    severity=AuditSeverity.MEDIUM,
                    user_id=user_id,
                    reason=f"Accessing {f.__name__}",
                    metadata={
                        "function_name": f.__name__,
                        "module": f.__module__,
                        "endpoint": request.path,
                        "method": request.method
                    }
                )
                
                # Check permissions if required
                if check_permissions and not user_id:
                    if log_failed_attempts:
                        audit_service.log_security_event(
                            event_type="unauthorized_access_attempt",
                            severity=AuditSeverity.HIGH,
                            user_id=None,
                            reason=f"Unauthorized access attempt to {f.__name__}",
                            blocked=True,
                            response_action="deny_access",
                            metadata={
                                "function_name": f.__name__,
                                "module": f.__module__,
                                "ip_address": ip_address,
                                "user_agent": user_agent
                            }
                        )
                    return jsonify({"error": "Authentication required"}), 401
                
                # Execute the function
                result = f(*args, **kwargs)
                
                return result
                
            except Exception as e:
                # Log security error
                audit_service.log_security_event(
                    event_type="security_error",
                    severity=AuditSeverity.HIGH,
                    user_id=user_id,
                    reason=f"Security error in {f.__name__}: {str(e)}",
                    metadata={
                        "function_name": f.__name__,
                        "module": f.__module__,
                        "error": str(e),
                        "exception_type": type(e).__name__
                    }
                )
                raise
        
        return decorated_function
    return decorator

def performance_audit(
    threshold_ms: float = 1000,
    alert_on_exceed: bool = True
):
    """
    Performance monitoring decorator.
    
    Args:
        threshold_ms: Performance threshold in milliseconds
        alert_on_exceed: Whether to alert when threshold is exceeded
    """
    def decorator(f: Callable) -> Callable:
        @wraps(f)
        def decorated_function(*args, **kwargs):
            start_time = time.time()
            
            try:
                # Execute the function
                result = f(*args, **kwargs)
                
                # Calculate processing time
                processing_time = (time.time() - start_time) * 1000
                
                # Log performance metric
                audit_service.log_performance_metric(
                    metric_type="function_execution_time",
                    value=processing_time,
                    unit="ms",
                    threshold=threshold_ms,
                    endpoint=request.path,
                    user_id=getattr(g, 'user_id', None),
                    metadata={
                        "function_name": f.__name__,
                        "module": f.__module__,
                        "threshold_ms": threshold_ms
                    }
                )
                
                # Alert if threshold exceeded
                if alert_on_exceed and processing_time > threshold_ms:
                    logger.warning(f"Performance threshold exceeded: {f.__name__} took {processing_time:.2f}ms (threshold: {threshold_ms}ms)")
                
                return result
                
            except Exception as e:
                processing_time = (time.time() - start_time) * 1000
                
                # Log performance metric even for errors
                audit_service.log_performance_metric(
                    metric_type="function_execution_time_error",
                    value=processing_time,
                    unit="ms",
                    threshold=threshold_ms,
                    endpoint=request.path,
                    user_id=getattr(g, 'user_id', None),
                    metadata={
                        "function_name": f.__name__,
                        "module": f.__module__,
                        "error": str(e),
                        "exception_type": type(e).__name__
                    }
                )
                
                raise
        
        return decorated_function
    return decorator

def data_access_audit(
    resource_type: str = "data",
    action: str = "ACCESS"
):
    """
    Data access auditing decorator.
    
    Args:
        resource_type: Type of resource being accessed
        action: Action being performed on the data
    """
    def decorator(f: Callable) -> Callable:
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user_id = getattr(g, 'user_id', None)
            
            try:
                # Extract resource ID from arguments
                resource_id = _extract_resource_id(kwargs, args)
                
                # Log data access
                audit_service.log_audit_event(
                    event_type=AuditEventType.DATA_ACCESS,
                    action=action,
                    user_id=user_id,
                    resource_id=resource_id,
                    resource_type=resource_type,
                    description=f"Accessing {resource_type} {resource_id}",
                    metadata={
                        "function_name": f.__name__,
                        "module": f.__module__,
                        "endpoint": request.path,
                        "method": request.method
                    }
                )
                
                # Execute the function
                result = f(*args, **kwargs)
                
                return result
                
            except Exception as e:
                # Log data access error
                audit_service.log_audit_event(
                    event_type=AuditEventType.DATA_ACCESS,
                    action=f"{action}_ERROR",
                    user_id=user_id,
                    resource_id=_extract_resource_id(kwargs, args),
                    resource_type=resource_type,
                    description=f"Error accessing {resource_type}: {str(e)}",
                    severity=AuditSeverity.HIGH,
                    error_message=str(e),
                    metadata={
                        "function_name": f.__name__,
                        "module": f.__module__,
                        "error": str(e),
                        "exception_type": type(e).__name__
                    }
                )
                raise
        
        return decorated_function
    return decorator

def compliance_audit(
    record_type: str = "data_access",
    legal_basis: str = "legitimate_interest"
):
    """
    Compliance auditing decorator for regulatory requirements.
    
    Args:
        record_type: Type of compliance record
        legal_basis: Legal basis for data processing
    """
    def decorator(f: Callable) -> Callable:
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user_id = getattr(g, 'user_id', None)
            
            try:
                # Log compliance record
                audit_service.log_compliance_record(
                    record_type=record_type,
                    user_id=user_id,
                    status="processing",
                    description=f"Processing {f.__name__}",
                    legal_basis=legal_basis,
                    metadata={
                        "function_name": f.__name__,
                        "module": f.__module__,
                        "endpoint": request.path,
                        "method": request.method
                    }
                )
                
                # Execute the function
                result = f(*args, **kwargs)
                
                # Update compliance record
                audit_service.log_compliance_record(
                    record_type=record_type,
                    user_id=user_id,
                    status="completed",
                    description=f"Completed {f.__name__}",
                    legal_basis=legal_basis,
                    processed_by=user_id,
                    metadata={
                        "function_name": f.__name__,
                        "module": f.__module__,
                        "status": "success"
                    }
                )
                
                return result
                
            except Exception as e:
                # Log compliance error
                audit_service.log_compliance_record(
                    record_type=record_type,
                    user_id=user_id,
                    status="failed",
                    description=f"Failed {f.__name__}: {str(e)}",
                    legal_basis=legal_basis,
                    metadata={
                        "function_name": f.__name__,
                        "module": f.__module__,
                        "error": str(e),
                        "exception_type": type(e).__name__
                    }
                )
                raise
        
        return decorated_function
    return decorator

def api_usage_audit(
    endpoint_name: str = None,
    rate_limit_check: bool = True
):
    """
    API usage auditing decorator.
    
    Args:
        endpoint_name: Name of the API endpoint
        rate_limit_check: Whether to check rate limits
    """
    def decorator(f: Callable) -> Callable:
        @wraps(f)
        def decorated_function(*args, **kwargs):
            start_time = time.time()
            endpoint = endpoint_name or request.path
            
            try:
                # Execute the function
                result = f(*args, **kwargs)
                
                # Calculate processing time
                processing_time = (time.time() - start_time) * 1000
                
                # Log API usage
                audit_service.log_api_usage(
                    endpoint=endpoint,
                    method=request.method,
                    response_time_ms=int(processing_time),
                    status_code=200,
                    user_id=getattr(g, 'user_id', None),
                    request_size=request.content_length,
                    response_size=getattr(result, 'content_length', None),
                    rate_limit_hit=False,  # TODO: Implement rate limit checking
                    metadata={
                        "function_name": f.__name__,
                        "module": f.__module__,
                        "user_agent": request.headers.get('User-Agent')
                    }
                )
                
                return result
                
            except Exception as e:
                processing_time = (time.time() - start_time) * 1000
                
                # Log API error
                audit_service.log_api_usage(
                    endpoint=endpoint,
                    method=request.method,
                    response_time_ms=int(processing_time),
                    status_code=500,
                    user_id=getattr(g, 'user_id', None),
                    error_message=str(e),
                    metadata={
                        "function_name": f.__name__,
                        "module": f.__module__,
                        "error": str(e),
                        "exception_type": type(e).__name__
                    }
                )
                raise
        
        return decorated_function
    return decorator

def _extract_request_data(sensitive_fields: Optional[list] = None) -> Dict[str, Any]:
    """Extract and sanitize request data."""
    if sensitive_fields is None:
        sensitive_fields = ['password', 'token', 'secret', 'key', 'ssn', 'credit_card']
    
    data = {}
    
    # Add headers (excluding sensitive ones)
    sensitive_headers = {'authorization', 'cookie', 'x-api-key', 'x-auth-token'}
    for key, value in request.headers:
        if key.lower() not in sensitive_headers:
            data[f"header_{key.lower()}"] = value
    
    # Add form data
    if request.form:
        for key, value in request.form.items():
            if key.lower() not in sensitive_fields:
                data[f"form_{key}"] = value
    
    # Add JSON data
    if request.is_json:
        json_data = request.get_json() or {}
        data["json_data"] = _sanitize_dict(json_data, sensitive_fields)
    
    # Add query parameters
    if request.args:
        data["query_params"] = dict(request.args)
    
    return data

def _sanitize_dict(data: Dict[str, Any], sensitive_fields: list) -> Dict[str, Any]:
    """Recursively sanitize dictionary data."""
    if not isinstance(data, dict):
        return data
    
    sanitized = {}
    for key, value in data.items():
        if key.lower() in sensitive_fields:
            sanitized[key] = "[REDACTED]"
        elif isinstance(value, dict):
            sanitized[key] = _sanitize_dict(value, sensitive_fields)
        elif isinstance(value, list):
            sanitized[key] = [_sanitize_dict(item, sensitive_fields) if isinstance(item, dict) else item for item in value]
        else:
            sanitized[key] = value
    
    return sanitized

def _extract_resource_id(kwargs: Dict[str, Any], args: tuple) -> Optional[str]:
    """Extract resource ID from function arguments."""
    # Try common resource ID parameter names
    resource_id_keys = ['id', 'user_id', 'document_id', 'case_id', 'resource_id']
    
    for key in resource_id_keys:
        if key in kwargs:
            return str(kwargs[key])
    
    # Try to extract from args (assuming first arg might be ID)
    if args and len(args) > 0:
        return str(args[0])
    
    return None
