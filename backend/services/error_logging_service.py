"""
Error logging service for application-wide error tracking and monitoring.
"""
import os
import json
import logging
import traceback
from datetime import datetime
from typing import Dict, Any, Optional, List, Union
from flask import request, current_app, g
import uuid

class ErrorLoggingService:
    """Service for logging and tracking application errors."""
    
    def __init__(self, app=None):
        """Initialize the error logging service."""
        self.app = app
        self.logger = logging.getLogger('error_service')
        
        # Configure logger if not already configured
        if not self.logger.handlers:
            self._configure_logger()
            
        if app is not None:
            self.init_app(app)
    
    def _configure_logger(self):
        """Configure the logger handlers and formatters."""
        # Set up console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.ERROR)
        
        # Set up file handler if log directory exists
        log_dir = 'logs'
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        file_handler = logging.FileHandler(os.path.join(log_dir, 'errors.log'))
        file_handler.setLevel(logging.ERROR)
        
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        console_handler.setFormatter(formatter)
        file_handler.setFormatter(formatter)
        
        # Add handlers to logger
        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)
        self.logger.setLevel(logging.ERROR)
    
    def init_app(self, app):
        """Initialize the service with a Flask application."""
        self.app = app
        
        # Set up error handlers
        @app.errorhandler(Exception)
        def handle_exception(e):
            """Handle uncaught exceptions."""
            error_id = self.log_exception(e)
            
            # Get appropriate response based on exception
            return self._get_error_response(e, error_id)
    
    def _get_error_response(self, exception: Exception, error_id: str) -> Dict[str, Any]:
        """Generate an appropriate error response based on the exception."""
        if hasattr(exception, 'code') and exception.code:
            status_code = exception.code
        else:
            status_code = 500
            
        if hasattr(exception, 'description'):
            error_message = exception.description
        else:
            error_message = str(exception) or "Internal Server Error"
            
        # In production, don't expose detailed error messages for 500 errors
        if status_code == 500 and current_app.config.get('ENV') == 'production':
            error_message = "Internal Server Error"
            
        response = {
            'error': {
                'message': error_message,
                'status_code': status_code,
                'error_id': error_id
            }
        }
        
        return response, status_code
    
    def log_exception(self, exception: Exception) -> str:
        """Log an exception with context information."""
        error_id = str(uuid.uuid4())
        
        # Get request information if available
        request_info = self._get_request_info()
        
        # Get user information if available
        user_info = self._get_user_info()
        
        # Format traceback
        tb = traceback.format_exc()
        
        # Create structured error log
        error_log = {
            'error_id': error_id,
            'timestamp': datetime.utcnow().isoformat(),
            'exception_type': exception.__class__.__name__,
            'exception_message': str(exception),
            'traceback': tb,
            'request': request_info,
            'user': user_info
        }
        
        # Log the error
        self.logger.error(
            f"Error {error_id}: {exception.__class__.__name__} - {str(exception)}\n"
            f"Request: {json.dumps(request_info)}\n"
            f"User: {json.dumps(user_info)}\n"
            f"Traceback: {tb}"
        )
        
        # Store in database if available
        self._store_error_in_db(error_log)
        
        return error_id
    
    def _get_request_info(self) -> Dict[str, Any]:
        """Get information about the current request."""
        if not request:
            return {'available': False}
            
        try:
            # Get basic request info
            request_info = {
                'method': request.method,
                'url': request.url,
                'path': request.path,
                'ip': request.remote_addr,
                'user_agent': request.user_agent.string if request.user_agent else None,
                'headers': dict(request.headers)
            }
            
            # Sanitize sensitive headers
            sensitive_headers = ['Authorization', 'Cookie', 'X-API-Key']
            for header in sensitive_headers:
                if header in request_info['headers']:
                    request_info['headers'][header] = '[REDACTED]'
                    
            # Add query parameters and form data
            request_info['query_params'] = dict(request.args)
            
            # Add JSON body if present
            if request.is_json:
                # Deep copy and sanitize the JSON body
                json_body = dict(request.get_json())
                self._sanitize_data(json_body)
                request_info['json_body'] = json_body
            
            return request_info
        except Exception as e:
            # If we can't get request info, don't fail the error logging
            return {
                'available': False,
                'error': str(e)
            }
    
    def _get_user_info(self) -> Dict[str, Any]:
        """Get information about the current user."""
        try:
            if hasattr(g, 'user') and g.user:
                return {
                    'user_id': getattr(g.user, 'id', None),
                    'email': getattr(g.user, 'email', '[REDACTED]'),
                    'role': getattr(g.user, 'role', None)
                }
        except Exception:
            pass
            
        return {'available': False}
    
    def _sanitize_data(self, data: Dict[str, Any], sensitive_fields: List[str] = None) -> None:
        """Sanitize sensitive data to avoid logging it."""
        if sensitive_fields is None:
            sensitive_fields = [
                'password', 'password_confirmation', 'token', 'secret',
                'credit_card', 'ssn', 'social_security', 'birth_date'
            ]
            
        for key, value in data.items():
            if isinstance(value, dict):
                self._sanitize_data(value, sensitive_fields)
            elif key.lower() in [field.lower() for field in sensitive_fields]:
                data[key] = '[REDACTED]'
    
    def _store_error_in_db(self, error_log: Dict[str, Any]) -> None:
        """Store error in the database for later analysis."""
        if not self.app:
            return
            
        try:
            # Check if MongoDB is available
            if hasattr(current_app, 'mongo') and current_app.mongo.db:
                # Store error in MongoDB
                current_app.mongo.db.errors.insert_one(error_log)
        except Exception as e:
            # If we can't store in DB, just log the issue
            self.logger.warning(f"Could not store error in database: {str(e)}")
    
    def log_error(self, 
                 message: str, 
                 level: str = 'error', 
                 context: Optional[Dict[str, Any]] = None) -> str:
        """Log an error message with context."""
        error_id = str(uuid.uuid4())
        
        log_levels = {
            'debug': logging.DEBUG,
            'info': logging.INFO,
            'warning': logging.WARNING,
            'error': logging.ERROR,
            'critical': logging.CRITICAL
        }
        
        log_level = log_levels.get(level.lower(), logging.ERROR)
        
        # Get request and user info
        request_info = self._get_request_info()
        user_info = self._get_user_info()
        
        # Combine all context
        full_context = {
            'request': request_info,
            'user': user_info
        }
        
        if context:
            # Sanitize any provided context
            context_copy = context.copy()
            self._sanitize_data(context_copy)
            full_context['additional'] = context_copy
        
        # Log the error
        self.logger.log(
            log_level,
            f"Error {error_id}: {message}\n"
            f"Context: {json.dumps(full_context)}"
        )
        
        # Store in database
        error_log = {
            'error_id': error_id,
            'timestamp': datetime.utcnow().isoformat(),
            'message': message,
            'level': level,
            'context': full_context
        }
        self._store_error_in_db(error_log)
        
        return error_id

# Create a singleton instance
error_logging_service = ErrorLoggingService() 