import logging
import json
from datetime import datetime
from functools import wraps
from flask import request, current_app, g
from typing import Optional, Dict, Any

class AuditLogger:
    def __init__(self):
        self.logger = logging.getLogger('audit')
        self.logger.setLevel(logging.INFO)
        
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        # Create handlers
        file_handler = logging.FileHandler('audit.log')
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
        
        if current_app.debug:
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)

    def log_event(
        self,
        event_type: str,
        user_id: Optional[str] = None,
        resource_type: Optional[str] = None,
        resource_id: Optional[str] = None,
        action: Optional[str] = None,
        status: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
        ip_address: Optional[str] = None
    ):
        """Log an audit event with the specified parameters"""
        event_data = {
            'timestamp': datetime.utcnow().isoformat(),
            'event_type': event_type,
            'user_id': user_id or getattr(g, 'user_id', None),
            'resource_type': resource_type,
            'resource_id': resource_id,
            'action': action,
            'status': status,
            'details': details or {},
            'ip_address': ip_address or request.remote_addr
        }
        
        self.logger.info(json.dumps(event_data))
        return event_data

def audit_trail(
    event_type: str,
    resource_type: Optional[str] = None,
    action: Optional[str] = None
):
    """Decorator to automatically log audit events for route handlers"""
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            start_time = datetime.utcnow()
            
            try:
                result = f(*args, **kwargs)
                status = 'success'
            except Exception as e:
                status = 'error'
                details = {'error': str(e)}
                audit_logger.log_event(
                    event_type=event_type,
                    resource_type=resource_type,
                    action=action,
                    status=status,
                    details=details
                )
                raise
            
            end_time = datetime.utcnow()
            duration = (end_time - start_time).total_seconds()
            
            # Log successful execution
            details = {
                'duration': duration,
                'resource_id': kwargs.get('id'),
                'method': request.method,
                'path': request.path
            }
            
            audit_logger.log_event(
                event_type=event_type,
                resource_type=resource_type,
                action=action,
                status=status,
                details=details
            )
            
            return result
        return wrapped
    return decorator

# Create singleton instance
audit_logger = AuditLogger()

# Example usage:
# @audit_trail('document', resource_type='legal_document', action='create')
# def create_document():
#     pass 