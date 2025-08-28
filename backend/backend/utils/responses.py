"""
Common response utilities for API endpoints
"""
from typing import Any, Dict, List, Optional, Union, Tuple
from flask import jsonify, make_response, Response

def success_response(
    message: str = "Success", 
    data: Optional[Union[Dict, List, Any]] = None, 
    status_code: int = 200
) -> Response:
    """
    Create a standard success response
    
    Args:
        message: Success message
        data: Response data
        status_code: HTTP status code
        
    Returns:
        JSON response
    """
    response = {
        "success": True,
        "message": message
    }
    
    if data is not None:
        response["data"] = data
        
    return make_response(jsonify(response), status_code)

def error_response(
    message: str = "An error occurred", 
    errors: Optional[Union[Dict, List, str]] = None, 
    status_code: int = 400
) -> Response:
    """
    Create a standard error response
    
    Args:
        message: Error message
        errors: Detailed errors (optional)
        status_code: HTTP status code
        
    Returns:
        JSON response
    """
    response = {
        "success": False,
        "message": message
    }
    
    if errors is not None:
        response["errors"] = errors
        
    return make_response(jsonify(response), status_code)

def pagination_response(
    data: List, 
    total: int, 
    page: int, 
    per_page: int,
    message: str = "Data retrieved successfully"
) -> Response:
    """
    Create a standardized paginated response
    
    Args:
        data: List of items for the current page
        total: Total number of items across all pages
        page: Current page number (1-indexed)
        per_page: Number of items per page
        message: Success message
        
    Returns:
        Flask Response object
    """
    total_pages = (total + per_page - 1) // per_page if per_page > 0 else 0
    
    response = {
        'success': True,
        'message': message,
        'data': data,
        'pagination': {
            'total': total,
            'per_page': per_page,
            'current_page': page,
            'total_pages': total_pages,
            'has_next': page < total_pages,
            'has_prev': page > 1
        }
    }
    
    return make_response(jsonify(response), 200)

def file_response(
    file_path: str, 
    filename: Optional[str] = None, 
    mimetype: Optional[str] = None
) -> Any:
    """
    Create a file download response
    
    Args:
        file_path: Path to the file
        filename: Optional filename to use for the download
        mimetype: Optional mimetype
        
    Returns:
        Response for file download
    """
    from flask import send_file
    return send_file(
        file_path,
        download_name=filename,
        mimetype=mimetype,
        as_attachment=True if filename else False
    )

def validation_error_response(errors: Dict[str, List[str]]) -> Response:
    """
    Create a standardized validation error response
    
    Args:
        errors: Dictionary of field errors with field names as keys and lists of error messages as values
        
    Returns:
        Flask Response object
    """
    return error_response(
        message="Validation failed",
        errors=errors,
        status_code=422  # Unprocessable Entity
    )

def not_found_response(resource_type: str, resource_id: Optional[Union[str, int]] = None) -> Response:
    """
    Create a standardized not found response
    
    Args:
        resource_type: The type of resource that was not found
        resource_id: Optional ID of the resource
        
    Returns:
        Flask Response object
    """
    if resource_id:
        message = f"{resource_type} with ID {resource_id} not found"
    else:
        message = f"{resource_type} not found"
        
    return error_response(message=message, status_code=404) 