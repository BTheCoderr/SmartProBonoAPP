from functools import wraps
from flask import request, jsonify
from pydantic import BaseModel, ValidationError, EmailStr, constr, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
import re

class ValidationMiddleware:
    def __init__(self):
        self.models = {}
        self._register_models()
    
    def _register_models(self):
        """Register all validation models"""
        
        class UserRegistration(BaseModel):
            email: EmailStr
            password: constr(min_length=8, max_length=100)
            full_name: constr(min_length=2, max_length=100)
            phone: Optional[constr(regex=r'^\+?1?\d{9,15}$')] = None
        
        class UserLogin(BaseModel):
            email: EmailStr
            password: str
            totp_token: Optional[str] = None
        
        class LegalCase(BaseModel):
            title: constr(min_length=5, max_length=200)
            description: constr(min_length=20, max_length=2000)
            priority: constr(regex='^(urgent|high|medium|low)$')
            category: constr(min_length=2, max_length=50)
            attachments: Optional[List[str]] = []
            client_info: Dict[str, Any]
        
        class Message(BaseModel):
            content: constr(min_length=1, max_length=5000)
            attachment_ids: Optional[List[str]] = []
            metadata: Optional[Dict[str, Any]] = {}
        
        class FileUpload(BaseModel):
            file_type: constr(regex='^(document|image|audio)$')
            content_type: str
            size: int = Field(..., gt=0, lt=20_000_000)  # Max 20MB
            metadata: Optional[Dict[str, Any]] = {}
        
        # Register models
        self.models = {
            'user_registration': UserRegistration,
            'user_login': UserLogin,
            'legal_case': LegalCase,
            'message': Message,
            'file_upload': FileUpload
        }
    
    def validate_request(self, model_name: str):
        """Decorator to validate request data against a model"""
        def decorator(f):
            @wraps(f)
            def wrapped(*args, **kwargs):
                model = self.models.get(model_name)
                if not model:
                    return jsonify({
                        'error': f'Validation model {model_name} not found'
                    }), 500
                
                try:
                    # Get request data based on content type
                    if request.is_json:
                        data = request.get_json()
                    elif request.form:
                        data = request.form.to_dict()
                    else:
                        data = request.args.to_dict()
                    
                    # Validate data against model
                    validated_data = model(**data)
                    
                    # Add validated data to request
                    request.validated_data = validated_data.dict()
                    
                    return f(*args, **kwargs)
                except ValidationError as e:
                    return jsonify({
                        'error': 'Validation error',
                        'details': e.errors()
                    }), 400
                except Exception as e:
                    return jsonify({
                        'error': 'Internal server error',
                        'message': str(e)
                    }), 500
            return wrapped
        return decorator
    
    def sanitize_input(self, text: str) -> str:
        """Sanitize input text"""
        # Remove any HTML tags
        text = re.sub(r'<[^>]+>', '', text)
        
        # Remove any script tags and their contents
        text = re.sub(r'<script[\s\S]*?</script>', '', text)
        
        # Remove any potentially dangerous attributes
        text = re.sub(r'on\w+="[^"]*"', '', text)
        
        # Remove any javascript: protocols
        text = re.sub(r'javascript:', '', text)
        
        # Remove any data: URIs
        text = re.sub(r'data:', '', text)
        
        return text.strip()
    
    def validate_file(self, file) -> Dict[str, Any]:
        """Validate file upload"""
        try:
            # Validate file size
            content_length = request.content_length
            if content_length and content_length > 20_000_000:  # 20MB limit
                raise ValueError('File too large')
            
            # Validate file type
            allowed_types = {
                'application/pdf': 'document',
                'application/msword': 'document',
                'application/vnd.openxmlformats-officedocument.wordprocessingml.document': 'document',
                'image/jpeg': 'image',
                'image/png': 'image',
                'image/gif': 'image',
                'audio/mpeg': 'audio',
                'audio/wav': 'audio'
            }
            
            content_type = file.content_type
            if content_type not in allowed_types:
                raise ValueError('Invalid file type')
            
            return {
                'file_type': allowed_types[content_type],
                'content_type': content_type,
                'size': content_length or 0,
                'filename': file.filename,
                'timestamp': datetime.utcnow().isoformat()
            }
        except Exception as e:
            raise ValueError(f'File validation failed: {str(e)}')

# Create a global instance
validation_middleware = ValidationMiddleware() 