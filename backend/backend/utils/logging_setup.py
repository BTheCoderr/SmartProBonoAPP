"""
Logging setup and utilities for the application
"""
import logging
import os
import sys
from logging.handlers import RotatingFileHandler
from flask import Flask, request, g, has_request_context
import traceback
import time
import json
from datetime import datetime

# Log levels
DEBUG = logging.DEBUG
INFO = logging.INFO
WARNING = logging.WARNING
ERROR = logging.ERROR
CRITICAL = logging.CRITICAL

# Loggers cache
_loggers = {}

def configure_logging(app: Flask, log_level=logging.INFO):
    """
    Configure application-wide logging
    
    Args:
        app: The Flask application
        log_level: The minimum log level to record (default: INFO)
    """
    # Create logs directory if it doesn't exist
    logs_dir = os.path.join(os.path.dirname(app.root_path), 'logs')
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)
    
    # Configure application logger
    app_log_file = os.path.join(logs_dir, 'app.log')
    file_handler = RotatingFileHandler(app_log_file, maxBytes=10485760, backupCount=10)
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s %(levelname)s [%(name)s] [%(module)s:%(lineno)d] [%(process)d]: %(message)s'
    )
    file_handler.setFormatter(formatter)
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    
    # Add handlers
    root_logger.addHandler(file_handler)
    
    # Configure separate error log
    error_log_file = os.path.join(logs_dir, 'error.log')
    error_file_handler = RotatingFileHandler(error_log_file, maxBytes=10485760, backupCount=10)
    error_file_handler.setFormatter(formatter)
    error_file_handler.setLevel(logging.ERROR)
    root_logger.addHandler(error_file_handler)
    
    # Add console handler in development
    if app.debug:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        root_logger.addHandler(console_handler)
    
    # Register request logging
    @app.before_request
    def before_request():
        g.start_time = time.time()
    
    @app.after_request
    def after_request(response):
        if request.path == '/favicon.ico':
            return response
            
        # Calculate request duration
        if hasattr(g, 'start_time'):
            duration = round((time.time() - g.start_time) * 1000, 2)
        else:
            duration = 0
            
        # Log request details
        log_data = {
            'method': request.method,
            'path': request.path,
            'status': response.status_code,
            'duration_ms': duration,
            'content_length': response.content_length,
            'remote_addr': request.remote_addr,
            'user_agent': request.user_agent.string
        }
        
        # Add user ID if authenticated
        if hasattr(g, 'user_id'):
            log_data['user_id'] = g.user_id
            
        # Log level based on status code
        if response.status_code >= 500:
            app.logger.error(f"Request: {json.dumps(log_data)}")
        elif response.status_code >= 400:
            app.logger.warning(f"Request: {json.dumps(log_data)}")
        else:
            app.logger.info(f"Request: {json.dumps(log_data)}")
            
        return response
    
    # Register exception logging
    @app.errorhandler(Exception)
    def handle_exception(e):
        app.logger.error(f"Unhandled exception: {str(e)}")
        app.logger.error(traceback.format_exc())
        return {"error": "Internal server error"}, 500
    
    app.logger.info("Logging configured")
    return app


def get_logger(name: str):
    """
    Get a logger with the given name
    
    Args:
        name: The logger name
        
    Returns:
        A configured logger
    """
    if name in _loggers:
        return _loggers[name]
        
    logger = logging.getLogger(name)
    _loggers[name] = logger
    return logger


def log_function_call(logger, level=logging.DEBUG):
    """
    Decorator to log function calls with parameters and return values
    
    Args:
        logger: The logger to use
        level: The log level
        
    Returns:
        Decorator function
    """
    def decorator(func):
        import functools
        
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            func_name = func.__name__
            module_name = func.__module__
            
            # Log function call
            log_message = f"CALL {module_name}.{func_name} - args: {args}, kwargs: {kwargs}"
            logger.log(level, log_message)
            
            start_time = time.time()
            
            try:
                result = func(*args, **kwargs)
                
                # Log successful return
                duration = round((time.time() - start_time) * 1000, 2)
                logger.log(level, f"RETURN {module_name}.{func_name} - duration: {duration}ms, result: {result}")
                
                return result
            except Exception as e:
                # Log exception
                duration = round((time.time() - start_time) * 1000, 2)
                logger.error(f"EXCEPTION {module_name}.{func_name} - duration: {duration}ms, error: {str(e)}")
                logger.error(traceback.format_exc())
                
                # Re-raise the exception
                raise
                
        return wrapper
    
    return decorator


def log_to_file(message: str, log_file: str, level: int = logging.INFO):
    """
    Log a message to a specific file
    
    Args:
        message: The message to log
        log_file: The log file path
        level: The log level
    """
    # Ensure directory exists
    log_dir = os.path.dirname(log_file)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # Create handler
    file_handler = logging.FileHandler(log_file)
    formatter = logging.Formatter('%(asctime)s [%(levelname)s]: %(message)s')
    file_handler.setFormatter(formatter)
    
    # Create logger
    logger = logging.getLogger(f"file_logger_{log_file}")
    logger.setLevel(level)
    
    # Remove existing handlers
    for handler in logger.handlers:
        logger.removeHandler(handler)
    
    # Add new handler
    logger.addHandler(file_handler)
    
    # Log message
    logger.log(level, message)
    
    # Remove handler
    logger.removeHandler(file_handler)
    file_handler.close()

# Configure logging for the application
def setup_logging(app):
    """
    Set up application logging
    
    Args:
        app: Flask application instance
    """
    # Create logs directory if it doesn't exist
    logs_dir = os.path.join(app.root_path, 'logs')
    os.makedirs(logs_dir, exist_ok=True)
    
    # Set log level based on environment
    log_level = logging.DEBUG if app.config.get('DEBUG', False) else logging.INFO
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    
    # Clear existing handlers
    for handler in root_logger.handlers:
        root_logger.removeHandler(handler)
    
    # Create formatters
    standard_formatter = logging.Formatter(
        '[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s',
        '%Y-%m-%d %H:%M:%S'
    )
    
    verbose_formatter = logging.Formatter(
        '[%(asctime)s] [%(levelname)s] [%(name)s:%(lineno)d] [%(funcName)s] %(message)s',
        '%Y-%m-%d %H:%M:%S'
    )
    
    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_handler.setFormatter(standard_formatter)
    root_logger.addHandler(console_handler)
    
    # Create file handler for all logs
    all_log_file = os.path.join(logs_dir, 'app.log')
    file_handler = RotatingFileHandler(all_log_file, maxBytes=1024*1024*10, backupCount=5)
    file_handler.setLevel(log_level)
    file_handler.setFormatter(verbose_formatter)
    root_logger.addHandler(file_handler)
    
    # Create file handler for error logs
    error_log_file = os.path.join(logs_dir, 'error.log')
    error_file_handler = RotatingFileHandler(error_log_file, maxBytes=1024*1024*10, backupCount=5)
    error_file_handler.setLevel(logging.ERROR)
    error_file_handler.setFormatter(verbose_formatter)
    root_logger.addHandler(error_file_handler)
    
    # Set up SQLAlchemy logging
    if app.config.get('SQLALCHEMY_ECHO', False):
        logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
    
    # Log application startup
    app.logger.info(f"Application logging initialized with level {logging.getLevelName(log_level)}")
    
    return app.logger

# Custom logger for modules - using a different name to avoid conflicts
def create_logger(name):
    """
    Get a logger for a specific module
    
    Args:
        name: Name of the logger
        
    Returns:
        Logger instance
    """
    return logging.getLogger(name)

# Request logging middleware
class RequestLogger:
    """Middleware to log HTTP requests"""
    
    def __init__(self, app):
        self.app = app
        self.logger = get_logger('requests')
    
    def __call__(self, environ, start_response):
        def custom_start_response(status, headers, exc_info=None):
            # Log request when response starts
            if has_request_context():
                method = request.method
                path = request.path
                status_code = int(status.split(' ')[0])
                
                log_message = f"Request: {method} {path} - Response: {status_code}"
                
                # Different log level based on status code
                if status_code >= 500:
                    self.logger.error(log_message)
                elif status_code >= 400:
                    self.logger.warning(log_message)
                else:
                    self.logger.info(log_message)
            
            return start_response(status, headers, exc_info)
        
        return self.app(environ, custom_start_response) 