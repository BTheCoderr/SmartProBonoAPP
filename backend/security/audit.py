import logging
from datetime import datetime
from typing import Dict, Any, Optional
from flask import request, g
import json
import hashlib
import os
from functools import wraps
from dataclasses import dataclass
from enum import Enum

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SecurityEventType(Enum):
    AUTH_SUCCESS = "authentication_success"
    AUTH_FAILURE = "authentication_failure"
    ACCESS_DENIED = "access_denied"
    RATE_LIMIT_EXCEEDED = "rate_limit_exceeded"
    SUSPICIOUS_ACTIVITY = "suspicious_activity"
    DATA_ACCESS = "data_access"
    DATA_MODIFICATION = "data_modification"
    CONFIGURATION_CHANGE = "configuration_change"
    SYSTEM_ERROR = "system_error"

@dataclass
class SecurityEvent:
    event_type: SecurityEventType
    timestamp: datetime
    user_id: Optional[str]
    ip_address: str
    user_agent: str
    request_method: str
    request_path: str
    request_data: Dict[str, Any]
    response_status: int
    additional_info: Dict[str, Any]

class SecurityAuditor:
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """Initialize the security auditor with the Flask app."""
        self.audit_log_path = app.config.get('SECURITY_AUDIT_LOG', 'security_audit.log')
        self.enable_file_logging = app.config.get('ENABLE_AUDIT_FILE_LOGGING', True)
        self.enable_db_logging = app.config.get('ENABLE_AUDIT_DB_LOGGING', True)
        
        # Setup audit log file
        if self.enable_file_logging:
            handler = logging.FileHandler(self.audit_log_path)
            handler.setFormatter(logging.Formatter(
                '%(asctime)s - %(levelname)s - %(message)s'
            ))
            logger.addHandler(handler)

    def log_event(self, event: SecurityEvent):
        """Log a security event."""
        event_data = {
            'event_type': event.event_type.value,
            'timestamp': event.timestamp.isoformat(),
            'user_id': event.user_id,
            'ip_address': event.ip_address,
            'user_agent': event.user_agent,
            'request_method': event.request_method,
            'request_path': event.request_path,
            'request_data': self._sanitize_sensitive_data(event.request_data),
            'response_status': event.response_status,
            'additional_info': event.additional_info
        }

        # Log to file
        if self.enable_file_logging:
            logger.info(json.dumps(event_data))

        # Log to database
        if self.enable_db_logging:
            self._log_to_database(event_data)

        # Check for suspicious activity
        self._check_suspicious_activity(event_data)

    def _sanitize_sensitive_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Remove sensitive information from request data."""
        sensitive_fields = ['password', 'token', 'secret', 'credit_card', 'ssn']
        sanitized = {}

        def sanitize_dict(d):
            result = {}
            for k, v in d.items():
                if any(field in k.lower() for field in sensitive_fields):
                    result[k] = '[REDACTED]'
                elif isinstance(v, dict):
                    result[k] = sanitize_dict(v)
                elif isinstance(v, list):
                    result[k] = [sanitize_dict(i) if isinstance(i, dict) else i for i in v]
                else:
                    result[k] = v
            return result

        return sanitize_dict(data)

    def _log_to_database(self, event_data: Dict[str, Any]):
        """Log security event to database."""
        try:
            from models import SecurityAuditLog
            from extensions import db

            log_entry = SecurityAuditLog(
                event_type=event_data['event_type'],
                timestamp=datetime.fromisoformat(event_data['timestamp']),
                user_id=event_data['user_id'],
                ip_address=event_data['ip_address'],
                user_agent=event_data['user_agent'],
                request_method=event_data['request_method'],
                request_path=event_data['request_path'],
                request_data=json.dumps(event_data['request_data']),
                response_status=event_data['response_status'],
                additional_info=json.dumps(event_data['additional_info'])
            )
            
            db.session.add(log_entry)
            db.session.commit()
        except Exception as e:
            logger.error(f"Failed to log security event to database: {str(e)}")

    def _check_suspicious_activity(self, event_data: Dict[str, Any]):
        """Check for suspicious activity patterns."""
        suspicious_patterns = [
            self._check_rapid_requests,
            self._check_multiple_failures,
            self._check_unusual_access_patterns,
            self._check_sensitive_data_access
        ]

        for check in suspicious_patterns:
            if check(event_data):
                self._handle_suspicious_activity(event_data)

    def _check_rapid_requests(self, event_data: Dict[str, Any]) -> bool:
        """Check for rapid successive requests."""
        # Implementation would track request frequency per IP/user
        return False

    def _check_multiple_failures(self, event_data: Dict[str, Any]) -> bool:
        """Check for multiple authentication failures."""
        # Implementation would track auth failures per IP/user
        return False

    def _check_unusual_access_patterns(self, event_data: Dict[str, Any]) -> bool:
        """Check for unusual access patterns."""
        # Implementation would analyze access patterns
        return False

    def _check_sensitive_data_access(self, event_data: Dict[str, Any]) -> bool:
        """Check for suspicious sensitive data access."""
        # Implementation would monitor sensitive data access
        return False

    def _handle_suspicious_activity(self, event_data: Dict[str, Any]):
        """Handle detected suspicious activity."""
        logger.warning(f"Suspicious activity detected: {json.dumps(event_data)}")
        # Implementation would trigger alerts, notifications, or automated responses

def audit_trail(event_type: SecurityEventType):
    """Decorator to add security audit trail to routes."""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            start_time = datetime.utcnow()
            
            try:
                response = f(*args, **kwargs)
                status_code = response.status_code
            except Exception as e:
                status_code = 500
                raise e
            finally:
                # Create security event
                event = SecurityEvent(
                    event_type=event_type,
                    timestamp=start_time,
                    user_id=getattr(g, 'user_id', None),
                    ip_address=request.remote_addr,
                    user_agent=request.user_agent.string,
                    request_method=request.method,
                    request_path=request.path,
                    request_data=request.get_json(silent=True) or {},
                    response_status=status_code,
                    additional_info={
                        'duration_ms': (datetime.utcnow() - start_time).total_seconds() * 1000,
                        'endpoint': f.__name__
                    }
                )
                
                # Log the event
                security_auditor.log_event(event)
                
            return response
        return decorated_function
    return decorator

# Initialize security auditor
security_auditor = SecurityAuditor() 