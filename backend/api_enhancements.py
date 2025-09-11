"""
Flask API Enhancements inspired by Django REST Framework
Adds serialization, pagination, and better API structure to Flask
"""

from flask import Flask, jsonify, request, url_for
from functools import wraps
import json
from typing import Dict, List, Any, Optional
from datetime import datetime
import math

class APIResponse:
    """Standardized API response format"""
    
    @staticmethod
    def success(data: Any = None, message: str = "Success", status_code: int = 200, **kwargs):
        """Create a successful API response"""
        response = {
            "success": True,
            "message": message,
            "timestamp": datetime.now().isoformat(),
            **kwargs
        }
        if data is not None:
            response["data"] = data
        return jsonify(response), status_code
    
    @staticmethod
    def error(message: str = "Error", status_code: int = 400, errors: List = None, **kwargs):
        """Create an error API response"""
        response = {
            "success": False,
            "message": message,
            "timestamp": datetime.now().isoformat(),
            **kwargs
        }
        if errors:
            response["errors"] = errors
        return jsonify(response), status_code
    
    @staticmethod
    def paginated(data: List, page: int, per_page: int, total: int, **kwargs):
        """Create a paginated API response"""
        total_pages = math.ceil(total / per_page) if per_page > 0 else 1
        
        response = {
            "success": True,
            "data": data,
            "pagination": {
                "page": page,
                "per_page": per_page,
                "total": total,
                "total_pages": total_pages,
                "has_next": page < total_pages,
                "has_prev": page > 1,
                "next_page": page + 1 if page < total_pages else None,
                "prev_page": page - 1 if page > 1 else None
            },
            "timestamp": datetime.now().isoformat(),
            **kwargs
        }
        return jsonify(response), 200

class Serializer:
    """Base serializer class for data transformation"""
    
    def __init__(self, instance=None, many=False):
        self.instance = instance
        self.many = many
    
    def to_representation(self, obj):
        """Convert object to dictionary representation"""
        raise NotImplementedError("Subclasses must implement to_representation")
    
    def data(self):
        """Get serialized data"""
        if self.many:
            return [self.to_representation(item) for item in self.instance]
        return self.to_representation(self.instance)
    
    @classmethod
    def serialize(cls, data, many=False):
        """Class method to serialize data"""
        serializer = cls(data, many=many)
        return serializer.data()

class Paginator:
    """Pagination helper for API responses"""
    
    def __init__(self, queryset, page=1, per_page=20, max_per_page=100):
        self.queryset = queryset
        self.page = max(1, int(page))
        self.per_page = min(max(1, int(per_page)), max_per_page)
        self.total = len(queryset) if hasattr(queryset, '__len__') else 0
    
    def get_page(self):
        """Get the current page of data"""
        start = (self.page - 1) * self.per_page
        end = start + self.per_page
        
        if hasattr(self.queryset, '__getitem__'):
            return self.queryset[start:end]
        else:
            # Convert to list if not sliceable
            items = list(self.queryset)
            return items[start:end]
    
    def get_paginated_response(self, serializer_class=None):
        """Get paginated response with metadata"""
        page_data = self.get_page()
        
        if serializer_class:
            page_data = serializer_class.serialize(page_data, many=True)
        
        return APIResponse.paginated(
            data=page_data,
            page=self.page,
            per_page=self.per_page,
            total=self.total
        )

class APIView:
    """Base API view class with common functionality"""
    
    def __init__(self):
        self.serializer_class = None
        self.permission_classes = []
    
    def get_serializer(self, data=None, many=False):
        """Get serializer instance"""
        if self.serializer_class:
            return self.serializer_class(data, many=many)
        return None
    
    def check_permissions(self):
        """Check if user has required permissions"""
        for permission_class in self.permission_classes:
            if not permission_class.has_permission():
                return False
        return True
    
    def dispatch_request(self, *args, **kwargs):
        """Dispatch request to appropriate method"""
        if not self.check_permissions():
            return APIResponse.error("Permission denied", 403)
        
        method = request.method.lower()
        if hasattr(self, method):
            return getattr(self, method)(*args, **kwargs)
        else:
            return APIResponse.error(f"Method {method.upper()} not allowed", 405)

def api_view(methods=None):
    """Decorator for API views"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if methods and request.method not in methods:
                return APIResponse.error(f"Method {request.method} not allowed", 405)
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def require_auth(f):
    """Decorator to require authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check if user is authenticated
        # This is a simple implementation - you can enhance it
        if not hasattr(request, 'user') or not request.user:
            return APIResponse.error("Authentication required", 401)
        return f(*args, **kwargs)
    return decorated_function

class Permission:
    """Base permission class"""
    
    @staticmethod
    def has_permission():
        """Check if permission is granted"""
        return True

class IsAuthenticated(Permission):
    """Require authentication"""
    
    @staticmethod
    def has_permission():
        return hasattr(request, 'user') and request.user is not None

class IsAdminUser(Permission):
    """Require admin user"""
    
    @staticmethod
    def has_permission():
        return (hasattr(request, 'user') and 
                request.user is not None and 
                getattr(request.user, 'is_admin', False))

# Example serializers for your existing models
class CaseSerializer(Serializer):
    """Serializer for case data"""
    
    def to_representation(self, obj):
        return {
            'id': getattr(obj, 'id', None),
            'title': getattr(obj, 'title', ''),
            'type': getattr(obj, 'type', ''),
            'client_name': getattr(obj, 'client_name', ''),
            'status': getattr(obj, 'status', ''),
            'date_created': getattr(obj, 'date_created', None),
            'url': url_for('api.case_detail', id=getattr(obj, 'id', None)) if hasattr(obj, 'id') else None
        }

class UserSerializer(Serializer):
    """Serializer for user data"""
    
    def to_representation(self, obj):
        return {
            'id': getattr(obj, 'id', None),
            'username': getattr(obj, 'username', ''),
            'email': getattr(obj, 'email', ''),
            'is_active': getattr(obj, 'is_active', True),
            'date_joined': getattr(obj, 'date_joined', None),
            'url': url_for('api.user_detail', id=getattr(obj, 'id', None)) if hasattr(obj, 'id') else None
        }

class DocumentSerializer(Serializer):
    """Serializer for document data"""
    
    def to_representation(self, obj):
        return {
            'id': getattr(obj, 'id', None),
            'title': getattr(obj, 'title', ''),
            'type': getattr(obj, 'type', ''),
            'content': getattr(obj, 'content', ''),
            'date_created': getattr(obj, 'date_created', None),
            'url': url_for('api.document_detail', id=getattr(obj, 'id', None)) if hasattr(obj, 'id') else None
        }

# API View classes
class CaseViewSet(APIView):
    """ViewSet for case operations"""
    
    def __init__(self):
        super().__init__()
        self.serializer_class = CaseSerializer
        self.permission_classes = [IsAuthenticated]
    
    def list(self):
        """List all cases"""
        # This would typically query your database
        cases = []  # Replace with actual database query
        paginator = Paginator(cases, page=request.args.get('page', 1), per_page=request.args.get('per_page', 20))
        return paginator.get_paginated_response(CaseSerializer)
    
    def retrieve(self, case_id):
        """Get specific case"""
        # This would typically query your database
        case = None  # Replace with actual database query
        if not case:
            return APIResponse.error("Case not found", 404)
        
        serializer = CaseSerializer(case)
        return APIResponse.success(data=serializer.data)
    
    def create(self):
        """Create new case"""
        data = request.get_json()
        # Validate and create case
        # This would typically save to database
        return APIResponse.success(message="Case created successfully", status_code=201)
    
    def update(self, case_id):
        """Update case"""
        data = request.get_json()
        # Validate and update case
        # This would typically update in database
        return APIResponse.success(message="Case updated successfully")
    
    def destroy(self, case_id):
        """Delete case"""
        # This would typically delete from database
        return APIResponse.success(message="Case deleted successfully")

# Utility functions
def create_api_blueprint(app):
    """Create API blueprint with enhanced features"""
    from flask import Blueprint
    
    api_bp = Blueprint('api', __name__, url_prefix='/api/v2')
    
    # Add enhanced API routes
    case_viewset = CaseViewSet()
    
    @api_bp.route('/cases/', methods=['GET', 'POST'])
    @api_view(['GET', 'POST'])
    def cases():
        if request.method == 'GET':
            return case_viewset.list()
        else:
            return case_viewset.create()
    
    @api_bp.route('/cases/<int:case_id>/', methods=['GET', 'PUT', 'DELETE'])
    @api_view(['GET', 'PUT', 'DELETE'])
    def case_detail(case_id):
        if request.method == 'GET':
            return case_viewset.retrieve(case_id)
        elif request.method == 'PUT':
            return case_viewset.update(case_id)
        else:
            return case_viewset.destroy(case_id)
    
    # Add API documentation endpoint
    @api_bp.route('/', methods=['GET'])
    def api_root():
        """API root with available endpoints"""
        return APIResponse.success(data={
            "name": "SmartProBono API",
            "version": "2.0",
            "description": "Enhanced API with DRF-like features",
            "endpoints": {
                "cases": "/api/v2/cases/",
                "users": "/api/v2/users/",
                "documents": "/api/v2/documents/",
                "ai_paralegal": "/api/v1/ai-virtual-paralegal/"
            },
            "features": [
                "Pagination",
                "Serialization", 
                "Authentication",
                "Standardized responses",
                "Error handling"
            ]
        })
    
    return api_bp
