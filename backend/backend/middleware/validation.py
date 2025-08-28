"""Request validation middleware"""
from functools import wraps
from flask import request, jsonify
from typing import List, Dict, Any, Callable, Optional
import logging

logger = logging.getLogger(__name__)

def validate_json_request(required_fields: Optional[List[str]] = None) -> Callable:
    """Decorator to validate JSON request data"""
    def decorator(f: Callable) -> Callable:
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not request.is_json:
                return jsonify({'error': 'Request must be JSON'}), 400

            data = request.get_json()
            if not data:
                return jsonify({'error': 'No data provided'}), 400

            if required_fields:
                missing_fields = [field for field in required_fields if field not in data]
                if missing_fields:
                    return jsonify({
                        'error': 'Missing required fields',
                        'fields': missing_fields
                    }), 400

            return f(*args, **kwargs)
        return decorated_function
    return decorator

def validate_query_params(required_params: Optional[List[str]] = None) -> Callable:
    """Decorator to validate query parameters"""
    def decorator(f: Callable) -> Callable:
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if required_params:
                missing_params = [param for param in required_params if param not in request.args]
                if missing_params:
                    return jsonify({
                        'error': 'Missing required query parameters',
                        'params': missing_params
                    }), 400

            return f(*args, **kwargs)
        return decorated_function
    return decorator

def validate_schema(schema: Dict[str, Any]) -> Callable:
    """Decorator to validate request data against a schema"""
    def decorator(f: Callable) -> Callable:
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not request.is_json:
                return jsonify({'error': 'Request must be JSON'}), 400

            data = request.get_json()
            if not data:
                return jsonify({'error': 'No data provided'}), 400

            validation_errors = []
            for field, field_schema in schema.items():
                if field_schema.get('required', False) and field not in data:
                    validation_errors.append(f"Missing required field: {field}")
                elif field in data:
                    field_type = field_schema.get('type')
                    if field_type and not isinstance(data[field], field_type):
                        validation_errors.append(
                            f"Invalid type for field {field}. "
                            f"Expected {field_type.__name__}, got {type(data[field]).__name__}"
                        )

            if validation_errors:
                return jsonify({
                    'error': 'Schema validation failed',
                    'details': validation_errors
                }), 400

            return f(*args, **kwargs)
        return decorated_function
    return decorator 