"""
Validation utilities for checking input data
"""
import re
from typing import Dict, List, Any, Tuple, Optional, Union, Callable
import jsonschema
from jsonschema import validate, ValidationError
from functools import wraps
from flask import request, jsonify
import logging

logger = logging.getLogger(__name__)

# Common validation patterns
EMAIL_PATTERN = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
PHONE_PATTERN = r'^\+?[0-9]{10,15}$'
US_ZIP_PATTERN = r'^\d{5}(-\d{4})?$'

def validate_required_fields(data: Dict, required_fields: List[str]) -> Tuple[bool, List[str]]:
    """
    Validate that required fields are present and not empty
    
    Args:
        data: The data to validate
        required_fields: List of required field names
        
    Returns:
        Tuple of (is_valid, missing_fields)
    """
    missing = []
    
    for field in required_fields:
        # Check if field exists and is not empty
        if field not in data or (data[field] == '' or data[field] is None):
            missing.append(field)
            
    return len(missing) == 0, missing

def validate_email(email: str) -> bool:
    """
    Validate an email address format
    
    Args:
        email: The email address to validate
        
    Returns:
        True if valid, False otherwise
    """
    if not email:
        return False
    
    return bool(re.match(EMAIL_PATTERN, email))

def validate_phone(phone: str) -> bool:
    """
    Validate a phone number format
    
    Args:
        phone: The phone number to validate
        
    Returns:
        True if valid, False otherwise
    """
    if not phone:
        return False
    
    # Remove common separators
    clean_phone = re.sub(r'[\s\-\(\)\.]', '', phone)
    
    return bool(re.match(PHONE_PATTERN, clean_phone))

def validate_zip_code(zip_code: str) -> bool:
    """
    Validate a US ZIP code format
    
    Args:
        zip_code: The ZIP code to validate
        
    Returns:
        True if valid, False otherwise
    """
    if not zip_code:
        return False
    
    return bool(re.match(US_ZIP_PATTERN, zip_code))

def validate_enum(value: Any, allowed_values: List[Any]) -> bool:
    """
    Validate that a value is one of the allowed values
    
    Args:
        value: The value to validate
        allowed_values: List of allowed values
        
    Returns:
        True if valid, False otherwise
    """
    return value in allowed_values

def validate_min_length(value: str, min_length: int) -> bool:
    """
    Validate that a string has a minimum length
    
    Args:
        value: The string to validate
        min_length: The minimum required length
        
    Returns:
        True if valid, False otherwise
    """
    if not value or not isinstance(value, str):
        return False
    
    return len(value) >= min_length

def validate_max_length(value: str, max_length: int) -> bool:
    """
    Validate that a string doesn't exceed a maximum length
    
    Args:
        value: The string to validate
        max_length: The maximum allowed length
        
    Returns:
        True if valid, False otherwise
    """
    if not isinstance(value, str):
        return False
    
    return len(value) <= max_length

def validate_number_range(value: Union[int, float], min_value: Optional[Union[int, float]] = None, 
                          max_value: Optional[Union[int, float]] = None) -> bool:
    """
    Validate that a number is within a specified range
    
    Args:
        value: The number to validate
        min_value: The minimum allowed value (optional)
        max_value: The maximum allowed value (optional)
        
    Returns:
        True if valid, False otherwise
    """
    if not isinstance(value, (int, float)):
        return False
    
    if min_value is not None and value < min_value:
        return False
    
    if max_value is not None and value > max_value:
        return False
    
    return True

def validate_schema(schema: Dict[str, Any]) -> bool:
    """
    Validate that a form schema follows the required structure.
    
    Args:
        schema: Dictionary containing the form schema
               
    Returns:
        bool: True if schema is valid, False otherwise
    """
    try:
        # Meta-schema that defines what a valid form schema looks like
        form_meta_schema = {
            "type": "object",
            "required": ["fields"],
            "properties": {
                "fields": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "required": ["id", "type", "label"],
                        "properties": {
                            "id": {"type": "string"},
                            "type": {
                                "type": "string",
                                "enum": ["text", "textarea", "select", "radio", "checkbox", "date", "file"]
                            },
                            "label": {"type": "string"},
                            "required": {"type": "boolean"},
                            "placeholder": {"type": "string"},
                            "options": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "required": ["value", "label"],
                                    "properties": {
                                        "value": {"type": "string"},
                                        "label": {"type": "string"}
                                    }
                                }
                            },
                            "validation": {
                                "type": "object",
                                "properties": {
                                    "pattern": {"type": "string"},
                                    "min": {"type": "number"},
                                    "max": {"type": "number"},
                                    "minLength": {"type": "integer"},
                                    "maxLength": {"type": "integer"},
                                    "allowedTypes": {
                                        "type": "array",
                                        "items": {"type": "string"}
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
        
        validate(instance=schema, schema=form_meta_schema)
        return True
    except ValidationError:
        return False
    except Exception:
        return False

def validate_json(schema):
    """Validate request JSON against schema"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                if not request.is_json:
                    return jsonify({'error': 'Request must be JSON'}), 400
                
                validate(instance=request.json, schema=schema)
                return f(*args, **kwargs)
            except ValidationError as e:
                logger.warning(f'Validation error: {str(e)}')
                return jsonify({'error': str(e)}), 400
            except Exception as e:
                logger.error(f'Unexpected error during validation: {str(e)}')
                return jsonify({'error': 'Internal server error'}), 500
        return decorated_function
    return decorator

# Schema definitions
TEMPLATE_SCHEMA = {
    'type': 'object',
    'required': ['template_id', 'name', 'title', 'fields'],
    'properties': {
        'template_id': {'type': 'string', 'minLength': 1},
        'name': {'type': 'string', 'minLength': 1},
        'title': {'type': 'string', 'minLength': 1},
        'fields': {
            'type': 'object',
            'additionalProperties': {
                'type': 'string',
                'enum': ['string', 'number', 'date', 'boolean', 'array']
            }
        },
        'version': {'type': 'string', 'pattern': r'^\d+\.\d+$'},
        'is_active': {'type': 'boolean'}
    }
}

FORM_DATA_SCHEMA = {
    'type': 'object',
    'additionalProperties': {
        'anyOf': [
            {'type': 'string'},
            {'type': 'number'},
            {'type': 'boolean'},
            {'type': 'array', 'items': {'type': 'string'}}
        ]
    }
}

USER_SCHEMA = {
    'type': 'object',
    'required': ['email', 'password', 'role'],
    'properties': {
        'email': {'type': 'string', 'format': 'email'},
        'password': {'type': 'string', 'minLength': 8},
        'role': {'type': 'string', 'enum': ['admin', 'paralegal', 'client']},
        'first_name': {'type': 'string'},
        'last_name': {'type': 'string'},
        'phone': {'type': 'string'},
        'organization': {'type': 'string'}
    }
}

CASE_SCHEMA = {
    'type': 'object',
    'required': ['client_id', 'case_type', 'status'],
    'properties': {
        'client_id': {'type': 'string'},
        'case_type': {'type': 'string'},
        'status': {'type': 'string', 'enum': ['open', 'closed', 'pending']},
        'assigned_to': {'type': 'string'},
        'priority': {'type': 'string', 'enum': ['low', 'medium', 'high']},
        'notes': {'type': 'string'}
    }
}

NOTIFICATION_SCHEMA = {
    'type': 'object',
    'required': ['title', 'message', 'recipient_id'],
    'properties': {
        'title': {'type': 'string', 'minLength': 1},
        'message': {'type': 'string', 'minLength': 1},
        'recipient_id': {'type': 'string'},
        'priority': {'type': 'string', 'enum': ['low', 'medium', 'high']},
        'category': {'type': 'string'}
    }
} 