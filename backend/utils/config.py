"""
Configuration utilities for the application
"""
import os
import json
from typing import Any, Dict, Optional, Union
from dotenv import load_dotenv

# Default configuration
DEFAULT_CONFIG = {
    'APP_NAME': 'SmartProBono',
    'ENV': 'development',
    'DEBUG': True,
    'TESTING': False,
    'SECRET_KEY': 'dev-key',
    'DATABASE_URL': 'sqlite:///smartprobono.db',
    'JWT_SECRET_KEY': 'dev-jwt-key',
    'JWT_ACCESS_TOKEN_EXPIRES': 86400,  # 24 hours
    'JWT_REFRESH_TOKEN_EXPIRES': 2592000,  # 30 days
    'MAIL_SERVER': 'smtp.gmail.com',
    'MAIL_PORT': 587,
    'MAIL_USE_TLS': True,
    'MAIL_USERNAME': '',
    'MAIL_PASSWORD': '',
    'MAIL_DEFAULT_SENDER': 'noreply@smartprobono.org',
    'ALLOWED_ORIGINS': 'http://localhost:3000,http://localhost:3100,https://smartprobono.netlify.app',
    'UPLOAD_FOLDER': 'uploads',
    'MAX_CONTENT_LENGTH': 16 * 1024 * 1024,  # 16 MB
    'RATE_LIMIT_DEFAULT': '100/hour',
    'ENABLE_WEBSOCKET': True,
    'LOG_LEVEL': 'INFO'
}

# Configuration instance
_config = {}

def load_config(env_file: Optional[str] = None) -> Dict[str, Any]:
    """
    Load configuration from environment variables and .env file
    
    Args:
        env_file: Path to the .env file (default: None, uses .env in current directory)
        
    Returns:
        The loaded configuration
    """
    global _config
    
    # Load environment variables from .env file
    load_dotenv(env_file)
    
    # Start with default configuration
    config = DEFAULT_CONFIG.copy()
    
    # Override with environment variables
    for key in config.keys():
        env_value = os.environ.get(key)
        if env_value is not None:
            # Convert boolean strings
            if env_value.lower() in ('true', 'yes', '1'):
                config[key] = True
            elif env_value.lower() in ('false', 'no', '0'):
                config[key] = False
            # Convert integer strings
            elif env_value.isdigit():
                config[key] = int(env_value)
            # Convert float strings
            elif env_value.replace('.', '', 1).isdigit() and env_value.count('.') < 2:
                config[key] = float(env_value)
            # Use string value
            else:
                config[key] = env_value
    
    # Load from config file if specified
    config_file = os.environ.get('CONFIG_FILE')
    if config_file and os.path.exists(config_file):
        with open(config_file, 'r') as f:
            file_config = json.load(f)
            config.update(file_config)
    
    # Cache config
    _config = config
    
    return config

def get_config() -> Dict[str, Any]:
    """
    Get the current configuration
    
    Returns:
        The current configuration
    """
    global _config
    
    # Load config if not loaded
    if not _config:
        return load_config()
        
    return _config

def get_config_value(key: str, default: Any = None) -> Any:
    """
    Get a configuration value
    
    Args:
        key: The configuration key
        default: The default value if key is not found
        
    Returns:
        The configuration value or default
    """
    config = get_config()
    return config.get(key, default)

def set_config_value(key: str, value: Any) -> None:
    """
    Set a configuration value (runtime only)
    
    Args:
        key: The configuration key
        value: The configuration value
    """
    global _config
    
    # Ensure config is loaded
    if not _config:
        load_config()
        
    _config[key] = value

def get_env() -> str:
    """
    Get the current environment
    
    Returns:
        The current environment (development, testing, production)
    """
    return get_config_value('ENV', 'development')

def is_development() -> bool:
    """
    Check if the application is running in development mode
    
    Returns:
        True if in development mode
    """
    return get_env() == 'development'

def is_production() -> bool:
    """
    Check if the application is running in production mode
    
    Returns:
        True if in production mode
    """
    return get_env() == 'production'

def is_testing() -> bool:
    """
    Check if the application is running in testing mode
    
    Returns:
        True if in testing mode
    """
    return get_env() == 'testing' or get_config_value('TESTING', False)

def configure_app(app) -> None:
    """
    Configure a Flask application with the loaded configuration
    
    Args:
        app: The Flask application
    """
    config = get_config()
    
    # Set Flask configuration
    for key, value in config.items():
        if key.isupper():  # Flask config keys are uppercase
            app.config[key] = value 