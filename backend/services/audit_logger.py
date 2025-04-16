import logging
from datetime import datetime
import json
from typing import Dict, Any, Optional
import os
from logging.handlers import RotatingFileHandler
import threading

class AuditLogger:
    def __init__(self, log_dir: str = 'logs/audit'):
        self.log_dir = log_dir
        self._setup_logger()
        self._local = threading.local()
        
    def _setup_logger(self):
        """Set up the audit logger"""
        # Create logs directory if it doesn't exist
        os.makedirs(self.log_dir, exist_ok=True)
        
        # Create logger
        self.logger = logging.getLogger('audit')
        self.logger.setLevel(logging.INFO)
        
        # Create handlers
        # File handler for all logs
        file_handler = RotatingFileHandler(
            os.path.join(self.log_dir, 'audit.log'),
            maxBytes=10_000_000,  # 10MB
            backupCount=10
        )
        
        # File handler for security events
        security_handler = RotatingFileHandler(
            os.path.join(self.log_dir, 'security.log'),
            maxBytes=10_000_000,  # 10MB
            backupCount=10
        )
        
        # Create formatters
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s'
        )
        
        # Set formatters
        file_handler.setFormatter(formatter)
        security_handler.setFormatter(formatter)
        
        # Add handlers
        self.logger.addHandler(file_handler)
        self.logger.addHandler(security_handler)
    
    def set_request_context(self, request_id: str, user_id: Optional[str] = None):
        """Set context for the current request"""
        self._local.request_id = request_id
        self._local.user_id = user_id
    
    def _format_log_entry(self, 
                         event_type: str, 
                         details: Dict[str, Any], 
                         severity: str = 'INFO') -> str:
        """Format a log entry as JSON"""
        entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'event_type': event_type,
            'severity': severity,
            'request_id': getattr(self._local, 'request_id', None),
            'user_id': getattr(self._local, 'user_id', None),
            'details': details
        }
        return json.dumps(entry)
    
    def log_auth_event(self, event_type: str, details: Dict[str, Any]):
        """Log authentication events"""
        entry = self._format_log_entry(
            f"AUTH_{event_type}",
            details,
            'WARNING' if event_type in ['FAILED_LOGIN', 'INVALID_2FA'] else 'INFO'
        )
        self.logger.warning(entry) if 'FAILED' in event_type else self.logger.info(entry)
    
    def log_access_event(self, resource: str, action: str, details: Dict[str, Any]):
        """Log resource access events"""
        entry = self._format_log_entry(
            'ACCESS',
            {
                'resource': resource,
                'action': action,
                **details
            }
        )
        self.logger.info(entry)
    
    def log_data_event(self, event_type: str, details: Dict[str, Any]):
        """Log data modification events"""
        entry = self._format_log_entry(
            f"DATA_{event_type}",
            details
        )
        self.logger.info(entry)
    
    def log_security_event(self, event_type: str, details: Dict[str, Any]):
        """Log security-related events"""
        entry = self._format_log_entry(
            f"SECURITY_{event_type}",
            details,
            'WARNING'
        )
        self.logger.warning(entry)
    
    def log_error(self, error_type: str, details: Dict[str, Any]):
        """Log error events"""
        entry = self._format_log_entry(
            f"ERROR_{error_type}",
            details,
            'ERROR'
        )
        self.logger.error(entry)
    
    def log_api_request(self, 
                       method: str, 
                       path: str, 
                       status_code: int, 
                       duration_ms: float):
        """Log API requests"""
        entry = self._format_log_entry(
            'API_REQUEST',
            {
                'method': method,
                'path': path,
                'status_code': status_code,
                'duration_ms': duration_ms
            }
        )
        self.logger.info(entry)
    
    def log_file_event(self, event_type: str, details: Dict[str, Any]):
        """Log file-related events"""
        entry = self._format_log_entry(
            f"FILE_{event_type}",
            details
        )
        self.logger.info(entry)
    
    def export_logs(self, 
                   start_date: datetime, 
                   end_date: datetime, 
                   event_types: Optional[list] = None) -> list:
        """Export logs within a date range"""
        logs = []
        log_file = os.path.join(self.log_dir, 'audit.log')
        
        with open(log_file, 'r') as f:
            for line in f:
                try:
                    log_entry = json.loads(line.split(' - ')[-1])
                    log_timestamp = datetime.fromisoformat(log_entry['timestamp'])
                    
                    if start_date <= log_timestamp <= end_date:
                        if not event_types or log_entry['event_type'] in event_types:
                            logs.append(log_entry)
                except:
                    continue
        
        return logs

# Create a global instance
audit_logger = AuditLogger() 