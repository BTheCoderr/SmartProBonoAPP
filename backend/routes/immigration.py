from flask import Blueprint, request, jsonify, Response, current_app
from datetime import datetime, timedelta
from bson import ObjectId
from database import db
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from functools import wraps
from models.user import User
import uuid  # Add this for generating mock IDs
import os
import werkzeug
from werkzeug.utils import secure_filename
from services.notification_service import get_notification_service
from database.mongo import mongo
import logging
from typing import Dict, List, Optional, Any, TypeVar, cast, Union, NoReturn, Callable, TYPE_CHECKING
from datetime import date
import json
from jsonschema import validate, ValidationError
import boto3
from botocore.exceptions import ClientError
import magic  # for file type detection
import hashlib
from enum import Enum
from copy import deepcopy
from pymongo.collection import Collection
from pymongo.database import Database
from flask_pymongo import PyMongo
from database.mongo_utils import (
    safe_insert_one,
    safe_find_one,
    safe_find,
    safe_update_one,
    safe_count_documents,
    MongoDBError
)

if TYPE_CHECKING:
    from flask import Flask
    class FlaskWithMongo(Flask):
        mongo: PyMongo

bp = Blueprint('immigration', __name__, url_prefix='/api/immigration')
logger = logging.getLogger(__name__)

# Add configuration for S3
S3_BUCKET = os.getenv('S3_BUCKET', 'smart-pro-bono-documents')
S3_REGION = os.getenv('S3_REGION', 'us-east-1')
ALLOWED_EXTENSIONS = {
    'pdf': 'application/pdf',
    'jpg': 'image/jpeg',
    'jpeg': 'image/jpeg',
    'png': 'image/png',
    'doc': 'application/msword',
    'docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

class FormStatus(Enum):
    DRAFT = 'draft'
    SUBMITTED = 'submitted'
    UNDER_REVIEW = 'under_review'
    NEEDS_INFO = 'needs_info'
    APPROVED = 'approved'
    REJECTED = 'rejected'

class TemplateStatus(Enum):
    DRAFT = 'draft'
    PUBLISHED = 'published'
    ARCHIVED = 'archived'

VALID_STATUS_TRANSITIONS = {
    FormStatus.DRAFT: [FormStatus.SUBMITTED],
    FormStatus.SUBMITTED: [FormStatus.UNDER_REVIEW, FormStatus.REJECTED],
    FormStatus.UNDER_REVIEW: [FormStatus.NEEDS_INFO, FormStatus.APPROVED, FormStatus.REJECTED],
    FormStatus.NEEDS_INFO: [FormStatus.UNDER_REVIEW, FormStatus.REJECTED],
    FormStatus.APPROVED: [],  # Terminal state
    FormStatus.REJECTED: [FormStatus.SUBMITTED]  # Can resubmit
}

T = TypeVar('T')

class DatabaseError(Exception):
    """Base class for database-related errors."""
    pass

class CollectionNotFoundError(DatabaseError):
    """Raised when a MongoDB collection is not found or invalid."""
    pass

def get_mongo_db() -> Optional[Database]:
    """Get MongoDB database instance."""
    app = cast('FlaskWithMongo', current_app)
    if not hasattr(app, 'mongo') or not hasattr(app.mongo, 'db'):
        logger.error("MongoDB connection not initialized")
        return None
    return cast(Database, app.mongo.db)

def get_mongo_collection(collection_name: str) -> Optional[Collection]:
    """Get a MongoDB collection."""
    db = get_mongo_db()
    if db is None:
        return None
    
    try:
        collection = db[collection_name]
        # type: ignore[truthy-bool] # PyMongo Collections don't implement __bool__ properly
        if not isinstance(collection, Collection):
            logger.error(f"Invalid collection type for {collection_name}")
            return None
        return collection
    except Exception as e:
        logger.error(f"Error getting collection {collection_name}: {str(e)}")
        return None

def is_valid_collection(collection: Optional[Collection]) -> bool:
    """Check if a collection is valid and available."""
    return collection is not None

def handle_db_operation(collection: Optional[Collection], operation: Callable[[Collection], T]) -> Union[T, tuple[Response, int]]:
    """Handle database operations with proper error checking."""
    # type: ignore[truthy-bool] # PyMongo Collections don't implement __bool__ properly
    if collection is None:
        return jsonify({"error": "Database service unavailable"}), 503
    
    try:
        return operation(collection)
    except Exception as e:
        logger.error(f"Database operation failed: {str(e)}")
        return jsonify({"error": "Database operation failed"}), 500

def with_collection(collection_name: str) -> Callable:
    """Decorator to handle MongoDB collection access and error handling."""
    def decorator(f: Callable) -> Callable:
        @wraps(f)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            collection = get_mongo_collection(collection_name)
            if collection is None:
                return jsonify({"error": "Database service unavailable"}), 503
            return f(collection, *args, **kwargs)
        return wrapper
    return decorator

def check_collection(collection: Optional[Collection]) -> bool:
    """Check if a MongoDB collection is available."""
    return collection is not None

def get_s3_client():
    """Get configured S3 client."""
    return boto3.client(
        's3',
        region_name=S3_REGION,
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
    )

def validate_file(file) -> tuple[bool, str]:
    """Validate file type and size."""
    try:
        # Check file size
        file.seek(0, 2)  # Seek to end
        size = file.tell()
        file.seek(0)  # Reset to beginning
        
        if size > MAX_FILE_SIZE:
            return False, f"File too large. Maximum size is {MAX_FILE_SIZE/1024/1024}MB"
            
        # Read first 2048 bytes for mime detection
        header = file.read(2048)
        file.seek(0)
        
        # Detect mime type
        mime = magic.from_buffer(header, mime=True)
        
        if mime not in ALLOWED_EXTENSIONS.values():
            return False, f"File type {mime} not allowed"
            
        return True, ""
    except Exception as e:
        return False, str(e)

def upload_file_to_s3(file, user_id: str, form_id: str) -> Optional[Dict[str, Any]]:
    """Upload file to S3 and return file metadata."""
    try:
        filename = secure_filename(file.filename)
        file_hash = hashlib.md5(file.read()).hexdigest()
        file.seek(0)
        
        # Generate S3 path: user_id/form_id/file_hash_filename
        s3_path = f"{user_id}/{form_id}/{file_hash}_{filename}"
        
        s3 = get_s3_client()
        s3.upload_fileobj(
            file,
            S3_BUCKET,
            s3_path,
            ExtraArgs={
                'ContentType': magic.from_buffer(file.read(2048), mime=True),
                'Metadata': {
                    'user_id': user_id,
                    'form_id': form_id,
                    'original_filename': filename
                }
            }
        )
        
        # Generate presigned URL for temporary access
        url = s3.generate_presigned_url(
            'get_object',
            Params={'Bucket': S3_BUCKET, 'Key': s3_path},
            ExpiresIn=3600  # URL valid for 1 hour
        )
        
        return {
            'filename': filename,
            'hash': file_hash,
            's3_path': s3_path,
            'url': url,
            'size': file.tell(),
            'mime_type': magic.from_buffer(file.read(2048), mime=True)
        }
    except Exception as e:
        logger.error(f"S3 upload error: {str(e)}")
        return None

# Role-based access control decorator
def lawyer_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        # Get JWT claims
        claims = get_jwt()
        role = claims.get('role', '')
        
        # Check if user has lawyer or admin role
        if role not in ['lawyer', 'admin']:
            return jsonify({'error': 'Access denied. Lawyer or admin rights required.'}), 403
        
        return fn(*args, **kwargs)
    
    return wrapper

# Mock data storage for testing purposes
mock_immigration_intake = []
mock_cases = []
mock_documents = {}  # Case ID -> list of documents
mock_notifications = []
mock_events = []

# Populate some initial mock data
def populate_mock_data():
    # Add sample cases if none exist
    if not mock_cases:
        # Get current time
        now = datetime.utcnow()
        
        mock_cases.extend([
            {
                '_id': str(uuid.uuid4()),
                'title': 'Family Visa Application',
                'status': 'in-progress',
                'type': 'family',
                'clientName': 'Maria Rodriguez',
                'createdAt': (now - timedelta(days=10)).isoformat(),
                'updatedAt': (now - timedelta(days=2)).isoformat(),
                'notes': 'Waiting for additional documentation from client'
            },
            {
                '_id': str(uuid.uuid4()),
                'title': 'Student Visa Renewal',
                'status': 'new',
                'type': 'student',
                'clientName': 'John Smith',
                'createdAt': (now - timedelta(days=5)).isoformat(),
                'updatedAt': (now - timedelta(days=5)).isoformat()
            },
            {
                '_id': str(uuid.uuid4()),
                'title': 'Work Visa Application',
                'status': 'completed',
                'type': 'employment',
                'clientName': 'David Chen',
                'createdAt': (now - timedelta(days=30)).isoformat(),
                'updatedAt': (now - timedelta(days=1)).isoformat(),
                'notes': 'Application approved'
            }
        ])
    
    # Add sample events if none exist
    if not mock_events:
        # Get current time
        now = datetime.utcnow()
        
        mock_events.extend([
            {
                '_id': str(uuid.uuid4()),
                'title': 'Document Submission Deadline',
                'date': (now + timedelta(days=7)).isoformat(),
                'type': 'deadline',
                'caseId': mock_cases[0]['_id'] if mock_cases else None,
                'description': 'Submit all required documents before this date'
            },
            {
                '_id': str(uuid.uuid4()),
                'title': 'Consultation with Immigration Lawyer',
                'date': (now + timedelta(days=3)).isoformat(),
                'type': 'appointment',
                'caseId': mock_cases[0]['_id'] if mock_cases else None,
                'description': 'Video call with Atty. Johnson to discuss case details'
            },
            {
                '_id': str(uuid.uuid4()),
                'title': 'USCIS Interview Preparation',
                'date': (now + timedelta(days=14)).isoformat(),
                'type': 'preparation',
                'caseId': mock_cases[1]['_id'] if len(mock_cases) > 1 else None,
                'description': 'Preparation session for upcoming USCIS interview'
            }
        ])
    
    # Add sample notifications if none exist
    if not mock_notifications:
        # Get current time
        now = datetime.utcnow()
        
        mock_notifications.extend([
            {
                '_id': str(uuid.uuid4()),
                'title': 'New Document Required',
                'message': 'Please upload your updated passport information',
                'type': 'document_request',
                'createdAt': now.isoformat(),
                'isRead': False,
                'caseId': mock_cases[0]['_id'] if mock_cases else None
            },
            {
                '_id': str(uuid.uuid4()),
                'title': 'Case Status Update',
                'message': 'Your case has been assigned to Attorney Sarah Johnson',
                'type': 'status_update',
                'createdAt': (now - timedelta(days=1)).isoformat(),
                'isRead': True,
                'caseId': mock_cases[0]['_id'] if mock_cases else None
            },
            {
                '_id': str(uuid.uuid4()),
                'title': 'Upcoming Deadline',
                'message': 'Document submission deadline in 7 days',
                'type': 'deadline',
                'createdAt': now.isoformat(),
                'isRead': False,
                'caseId': mock_cases[0]['_id'] if mock_cases else None
            }
        ])

# Call this to populate mock data
populate_mock_data()

# Form templates with JSON schema validation
FORM_TEMPLATES = {
    'family_visa': {
        'name': 'Family Visa Application',
        'description': 'Application for family-based immigration visas',
        'schema': {
            'type': 'object',
            'required': [
                'applicantInfo',
                'familyInfo',
                'sponsorInfo',
                'residenceInfo'
            ],
            'properties': {
                'applicantInfo': {
                    'type': 'object',
                    'required': ['firstName', 'lastName', 'dateOfBirth', 'nationality', 'passportNumber'],
                    'properties': {
                        'firstName': {'type': 'string', 'minLength': 1},
                        'lastName': {'type': 'string', 'minLength': 1},
                        'dateOfBirth': {'type': 'string', 'format': 'date'},
                        'nationality': {'type': 'string'},
                        'passportNumber': {'type': 'string'},
                        'email': {'type': 'string', 'format': 'email'},
                        'phone': {'type': 'string'}
                    }
                },
                'familyInfo': {
                    'type': 'object',
                    'required': ['relationshipType', 'familyMembers'],
                    'properties': {
                        'relationshipType': {
                            'type': 'string',
                            'enum': ['spouse', 'parent', 'child', 'sibling']
                        },
                        'familyMembers': {
                            'type': 'array',
                            'items': {
                                'type': 'object',
                                'required': ['name', 'relationship'],
                                'properties': {
                                    'name': {'type': 'string'},
                                    'relationship': {'type': 'string'},
                                    'dateOfBirth': {'type': 'string', 'format': 'date'}
                                }
                            }
                        }
                    }
                },
                'sponsorInfo': {
                    'type': 'object',
                    'required': ['name', 'residencyStatus', 'address'],
                    'properties': {
                        'name': {'type': 'string'},
                        'residencyStatus': {
                            'type': 'string',
                            'enum': ['citizen', 'permanent_resident']
                        },
                        'address': {'type': 'string'},
                        'income': {'type': 'number'},
                        'employmentInfo': {'type': 'string'}
                    }
                },
                'residenceInfo': {
                    'type': 'object',
                    'required': ['currentAddress', 'intendedResidence'],
                    'properties': {
                        'currentAddress': {'type': 'string'},
                        'intendedResidence': {'type': 'string'},
                        'previousResidences': {
                            'type': 'array',
                            'items': {
                                'type': 'object',
                                'properties': {
                                    'address': {'type': 'string'},
                                    'fromDate': {'type': 'string', 'format': 'date'},
                                    'toDate': {'type': 'string', 'format': 'date'}
                                }
                            }
                        }
                    }
                }
            }
        }
    },
    'employment_visa': {
        'name': 'Employment Visa Application',
        'description': 'Application for employment-based immigration visas',
        'schema': {
            'type': 'object',
            'required': [
                'applicantInfo',
                'employmentInfo',
                'educationInfo',
                'sponsorInfo'
            ],
            'properties': {
                'applicantInfo': {
                    'type': 'object',
                    'required': ['firstName', 'lastName', 'dateOfBirth', 'nationality', 'passportNumber'],
                    'properties': {
                        'firstName': {'type': 'string', 'minLength': 1},
                        'lastName': {'type': 'string', 'minLength': 1},
                        'dateOfBirth': {'type': 'string', 'format': 'date'},
                        'nationality': {'type': 'string'},
                        'passportNumber': {'type': 'string'},
                        'email': {'type': 'string', 'format': 'email'},
                        'phone': {'type': 'string'}
                    }
                },
                'employmentInfo': {
                    'type': 'object',
                    'required': ['jobTitle', 'employer', 'salary', 'startDate'],
                    'properties': {
                        'jobTitle': {'type': 'string'},
                        'employer': {'type': 'string'},
                        'salary': {'type': 'number'},
                        'startDate': {'type': 'string', 'format': 'date'},
                        'employmentType': {
                            'type': 'string',
                            'enum': ['full_time', 'part_time', 'contract']
                        },
                        'jobDescription': {'type': 'string'}
                    }
                },
                'educationInfo': {
                    'type': 'object',
                    'required': ['highestDegree'],
                    'properties': {
                        'highestDegree': {'type': 'string'},
                        'institution': {'type': 'string'},
                        'graduationDate': {'type': 'string', 'format': 'date'},
                        'fieldOfStudy': {'type': 'string'}
                    }
                },
                'sponsorInfo': {
                    'type': 'object',
                    'required': ['companyName', 'address', 'contactPerson'],
                    'properties': {
                        'companyName': {'type': 'string'},
                        'address': {'type': 'string'},
                        'contactPerson': {'type': 'string'},
                        'contactEmail': {'type': 'string', 'format': 'email'},
                        'contactPhone': {'type': 'string'}
                    }
                }
            }
        }
    }
}

@bp.route('/cases', methods=['GET'])
@jwt_required()
def get_cases():
    collection = get_mongo_collection('cases')
    if collection is None:
        return jsonify({'error': 'Database error'}), 500
    
    try:
        current_user_id = get_jwt_identity()
        cases = list(collection.find({'user_id': current_user_id}))
        for case in cases:
            case['_id'] = str(case['_id'])  # Convert ObjectId to string for JSON serialization
        return jsonify({'cases': cases}), 200
    except Exception as e:
        logger.error(f"Error fetching cases: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@bp.route('/cases', methods=['POST'])
@jwt_required()
def create_case():
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['title', 'description', 'case_type']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Create new case
        new_case = {
            'title': data['title'],
            'description': data['description'],
            'case_type': data['case_type'],
            'status': 'pending',
            'client_id': ObjectId(current_user_id),
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow(),
            'documents': [],
            'notes': [],
            'assigned_attorney': None,
            'priority': data.get('priority', 'normal'),
            'deadline': data.get('deadline'),
            'tags': data.get('tags', [])
        }
        
        # Get cases collection
        cases_collection = get_mongo_collection('cases')
        if cases_collection is None:
            return jsonify({'error': 'Database error'}), 500
        
        # Insert into database
        result = cases_collection.insert_one(new_case)
        
        # Return created case
        return jsonify({
            'message': 'Case created successfully',
            'case_id': str(result.inserted_id)
        }), 201
        
    except Exception as e:
        logger.error(f"Create case error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@bp.route('/cases/<case_id>', methods=['GET'])
@jwt_required()
def get_case(case_id):
    try:
        current_user_id = get_jwt_identity()
        users_collection = get_mongo_collection('cases')
        
        if users_collection is None:
            return jsonify({'error': 'Database error'}), 500
            
        user = users_collection.find_one({'_id': ObjectId(current_user_id)})
        if not user:
            return jsonify({'error': 'User not found'}), 404
            
        # Get case
        case = users_collection.find_one({'_id': ObjectId(case_id)})
        if not case:
            return jsonify({'error': 'Case not found'}), 404
        
        # Check permission
        role = user.get('role', 'client')
        client_id = str(case.get('client_id', ''))
        assigned_attorney = case.get('assigned_attorney')
        assigned_attorney_str = str(assigned_attorney) if assigned_attorney else None
        
        if (role == 'client' and client_id != current_user_id) or \
           (role == 'attorney' and assigned_attorney_str != current_user_id):
            return jsonify({'error': 'Access denied'}), 403
        
        # Convert ObjectId to string
        case['_id'] = str(case['_id'])
        case['client_id'] = client_id
        if assigned_attorney:
            case['assigned_attorney'] = assigned_attorney_str
        
        return jsonify({'case': case}), 200
        
    except Exception as e:
        logger.error(f"Get case error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@bp.route('/cases/<case_id>', methods=['PUT'])
@jwt_required()
def update_case(case_id):
    try:
        current_user_id = get_jwt_identity()
        users_collection = get_mongo_collection('cases')
        
        if users_collection is None:
            return jsonify({'error': 'Database error'}), 500
            
        user = users_collection.find_one({'_id': ObjectId(current_user_id)})
        if not user:
            return jsonify({'error': 'User not found'}), 404
            
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No update data provided'}), 400
        
        # Get case
        case = users_collection.find_one({'_id': ObjectId(case_id)})
        if not case:
            return jsonify({'error': 'Case not found'}), 404
        
        # Check permission
        role = user.get('role', 'client')
        if role not in ['admin', 'attorney']:
            return jsonify({'error': 'Access denied'}), 403
        
        # Update case
        update_data = {
            'updated_at': datetime.utcnow(),
            **{k: v for k, v in data.items() if k not in ['_id', 'client_id', 'created_at']}
        }
        
        result = users_collection.update_one(
            {'_id': ObjectId(case_id)},
            {'$set': update_data}
        )
        
        if result.modified_count == 0:
            return jsonify({'error': 'No changes made'}), 400
        
        return jsonify({'message': 'Case updated successfully'}), 200
        
    except Exception as e:
        logger.error(f"Update case error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@bp.route('/cases/<case_id>/notes', methods=['POST'])
@jwt_required()
def add_case_note(case_id):
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        if not data or not data.get('content'):
            return jsonify({'error': 'Note content is required'}), 400
        
        note = {
            'content': data['content'],
            'created_by': ObjectId(current_user_id),
            'created_at': datetime.utcnow()
        }
        
        # Get cases collection
        cases_collection = get_mongo_collection('cases')
        if cases_collection is None:
            return jsonify({'error': 'Database error'}), 500
        
        result = cases_collection.update_one(
            {'_id': ObjectId(case_id)},
            {
                '$push': {'notes': note},
                '$set': {'updated_at': datetime.utcnow()}
            }
        )
        
        if result.modified_count == 0:
            return jsonify({'error': 'Case not found'}), 404
        
        return jsonify({'message': 'Note added successfully'}), 200
        
    except Exception as e:
        logger.error(f"Add note error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@bp.route('/cases/<case_id>/status', methods=['PUT'])
@jwt_required()
def update_case_status(case_id):
    try:
        data = request.get_json()
        
        if 'status' not in data:
            return jsonify({'error': 'Status is required'}), 400
        
        valid_statuses = ['new', 'in-progress', 'completed', 'delayed']
        if data['status'] not in valid_statuses:
            return jsonify({'error': f'Status must be one of: {", ".join(valid_statuses)}'}), 400
            
        # Find and update case status
        for case in mock_cases:
            if case['_id'] == case_id:
                old_status = case['status']
                case['status'] = data['status']
                case['updatedAt'] = datetime.utcnow().isoformat()
                
                # Create a notification for status change
                notification = {
                    '_id': str(uuid.uuid4()),
                    'title': 'Case Status Changed',
                    'message': f'Case status changed from {old_status} to {data["status"]}',
                    'type': 'status_change',
                    'createdAt': datetime.utcnow().isoformat(),
                    'isRead': False,
                    'caseId': case_id
                }
                mock_notifications.append(notification)
                
                return jsonify({
                    'success': True,
                    'message': 'Case status updated successfully',
                    'case': case
                })
                
        return jsonify({'error': 'Case not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/cases/<case_id>', methods=['DELETE'])
@jwt_required()
@lawyer_required
def delete_case(case_id):
    try:
        # Find and delete case from mock data
        for i, case in enumerate(mock_cases):
            if case['_id'] == case_id:
                deleted_case = mock_cases.pop(i)
                
                # Delete associated documents
                if case_id in mock_documents:
                    del mock_documents[case_id]
                
                # Delete associated notifications
                mock_notifications[:] = [n for n in mock_notifications if n.get('caseId') != case_id]
                
                # Delete associated events
                mock_events[:] = [e for e in mock_events if e.get('caseId') != case_id]
                
                return jsonify({
                    'message': 'Case deleted successfully',
                    'deletedCase': deleted_case
                })
                
            return jsonify({'error': 'Case not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/cases/<case_id>/documents', methods=['POST'])
@jwt_required()
def upload_document(case_id):
    try:
        # Check if case exists
        case_exists = False
        for case in mock_cases:
            if case['_id'] == case_id:
                case_exists = True
                break
                
        if not case_exists:
            return jsonify({'error': 'Case not found'}), 404
            
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
            
        file = request.files['file']
        document_type = request.form.get('documentType', 'other')
        
        if not file.filename:
            return jsonify({'error': 'No file selected'}), 400
            
        # In a real app, we'd save the file to a storage system
        # For mock data, just store the metadata
        filename = secure_filename(file.filename)
        
        document = {
            '_id': str(uuid.uuid4()),
            'filename': filename,
            'originalName': file.filename,
            'documentType': document_type,
            'mimeType': file.content_type,
            'size': 0,  # In a real app, this would be file.content_length
            'uploadedAt': datetime.utcnow().isoformat(),
            'uploadedBy': get_jwt_identity()
        }
        
        # Initialize document list for case if it doesn't exist
        if case_id not in mock_documents:
            mock_documents[case_id] = []
            
        mock_documents[case_id].append(document)
        
        # Create a notification for document upload
        notification = {
            '_id': str(uuid.uuid4()),
            'title': 'New Document Uploaded',
            'message': f'Document {filename} has been uploaded',
            'type': 'document_upload',
            'createdAt': datetime.utcnow().isoformat(),
            'isRead': False,
            'caseId': case_id
        }
        mock_notifications.append(notification)
        
        return jsonify({
            'message': 'Document uploaded successfully',
            'document': document
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/cases/<case_id>/documents', methods=['GET'])
@jwt_required()
def get_documents(case_id):
    try:
        # Check if case exists
        case_exists = False
        for case in mock_cases:
            if case['_id'] == case_id:
                case_exists = True
                break
                
        if not case_exists:
            return jsonify({'error': 'Case not found'}), 404
            
        # Return documents for case (or empty list)
        documents = mock_documents.get(case_id, [])
        return jsonify({
            'documents': documents,
            'count': len(documents)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/intake', methods=['POST'])
def submit_immigration_intake() -> Union[Response, tuple[Response, int]]:
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        try:
            doc_id = safe_insert_one('intakes', {
                **data,
                'created_at': datetime.utcnow(),
                'status': 'submitted'
            })
            return jsonify({
                'success': True,
                'intake_id': str(doc_id)
            }), 201
        except MongoDBError as e:
            logger.error(f"Failed to store intake: {str(e)}")
            return jsonify({'error': 'Database error'}), 500

    except Exception as e:
        logger.error(f"Error submitting intake: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@bp.route('/intake/<intake_id>', methods=['GET'])
def get_intake(intake_id: str) -> Union[Response, tuple[Response, int]]:
    try:
        intake = safe_find_one('intakes', {'_id': ObjectId(intake_id)})
        if intake is None:
            return jsonify({'error': 'Intake not found'}), 404
            
        # Convert ObjectId to string for JSON serialization
        intake['_id'] = str(intake['_id'])
        return jsonify({'intake': intake}), 200
            
    except MongoDBError as e:
        logger.error(f"Database error getting intake: {str(e)}")
        return jsonify({'error': 'Database error'}), 500
    except Exception as e:
        logger.error(f"Error getting intake: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@bp.route('/intake/<intake_id>/status', methods=['PUT'])
def update_intake_status(intake_id: str) -> Union[Response, tuple[Response, int]]:
    try:
        data = request.get_json()
        new_status = data.get('status')
        if not new_status:
            return jsonify({'error': 'Status is required'}), 400
            
        try:
            updated = safe_update_one(
                'intakes',
                {'_id': ObjectId(intake_id)},
                {'$set': {'status': new_status}}
            )
            
            if not updated:
                return jsonify({'error': 'Intake not found'}), 404
                
            return jsonify({'message': 'Status updated successfully'}), 200
            
        except MongoDBError as e:
            logger.error(f"Database error updating intake status: {str(e)}")
            return jsonify({'error': 'Database error'}), 500
        
    except Exception as e:
        logger.error(f"Error updating intake status: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@bp.route('/visa-requirements', methods=['GET'])
def get_visa_requirements():
    try:
        visa_type = request.args.get('type', 'general')
        
        # Return mock visa requirements
        requirements = {
            '_id': str(uuid.uuid4()),
            'type': visa_type,
            'documents': [
                'Passport',
                'Birth Certificate',
                'Financial Documents',
                'Application Forms'
            ],
            'timeline': '3-6 months',
            'fees': '$500-1000'
        }
        
        return jsonify(requirements)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/intake-forms', methods=['GET'])
@jwt_required()
def get_intake_forms():
    try:
        # In a real app, filter by user or permissions
        # For now, return all mock data
        return jsonify(mock_immigration_intake)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/intake-forms/<form_id>', methods=['GET'])
@jwt_required()
def get_intake_form(form_id):
    try:
        # Get form from mock data
        for form in mock_immigration_intake:
            if form['_id'] == form_id:
                return jsonify(form)
                
        return jsonify({'error': 'Form not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/intake-forms/<form_id>/status', methods=['PUT'])
@jwt_required()
def update_intake_form_status(form_id):
    try:
        data = request.get_json()
        
        if 'status' not in data:
            return jsonify({'error': 'Status is required'}), 400
            
        valid_statuses = ['new', 'in-progress', 'completed', 'archived']
        if data['status'] not in valid_statuses:
            return jsonify({'error': f'Status must be one of: {", ".join(valid_statuses)}'}), 400
        
        # Update form in mock data
        for form in mock_immigration_intake:
            if form['_id'] == form_id:
                old_status = form.get('status', 'new')
                form['status'] = data['status']
                form['updatedAt'] = datetime.utcnow().isoformat()
                form['updatedBy'] = get_jwt_identity()
                
                # Create a notification for status change
                notification = {
                    '_id': str(uuid.uuid4()),
                    'title': 'Form Status Changed',
                    'message': f'Form status changed from {old_status} to {data["status"]}',
                    'type': 'status_change',
                    'createdAt': datetime.utcnow().isoformat(),
                    'isRead': False,
                    'formId': form_id
                }
                mock_notifications.append(notification)
                
                return jsonify({'success': True, 'message': 'Form status updated successfully'})
                
        return jsonify({'error': 'Form not found or status not changed'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/notifications', methods=['GET'])
@jwt_required()
def get_notifications():
    try:
        # In a real app, filter by user
        # For mock data, just return all
        return jsonify({
            'notifications': mock_notifications,
            'count': len(mock_notifications),
            'unreadCount': sum(1 for n in mock_notifications if not n.get('isRead', False))
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/notifications/<notification_id>/read', methods=['PUT'])
@jwt_required()
def mark_notification_read(notification_id):
    try:
        for notification in mock_notifications:
            if notification['_id'] == notification_id:
                notification['isRead'] = True
                notification['readAt'] = datetime.utcnow().isoformat()
                return jsonify({
                    'success': True,
                    'message': 'Notification marked as read'
                })
                
        return jsonify({'error': 'Notification not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/events', methods=['GET'])
@jwt_required()
def get_events():
    try:
        # In a real app, filter by user and permissions
        # For mock data, just return all
        return jsonify({
            'events': mock_events,
            'count': len(mock_events)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/events', methods=['POST'])
@jwt_required()
def create_event():
    try:
        event_data = request.get_json()
        
        # Validate required fields
        required_fields = ['title', 'date', 'type']
        for field in required_fields:
            if field not in event_data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
                
        # Valid event types
        valid_types = ['deadline', 'appointment', 'preparation', 'other']
        if event_data['type'] not in valid_types:
            return jsonify({'error': f'Event type must be one of: {", ".join(valid_types)}'}), 400
            
        # If caseId is provided, check if case exists
        if 'caseId' in event_data:
            case_exists = False
            for case in mock_cases:
                if case['_id'] == event_data['caseId']:
                    case_exists = True
                    break
                    
            if not case_exists:
                return jsonify({'error': 'Case not found'}), 404
                
        # Generate ID and add timestamps
        event_data['_id'] = str(uuid.uuid4())
        event_data['createdAt'] = datetime.utcnow().isoformat()
        event_data['createdBy'] = get_jwt_identity()
        
        # Add to mock data
        mock_events.append(event_data)
        
        # Create a notification for new event
        notification = {
            '_id': str(uuid.uuid4()),
            'title': 'New Event Created',
            'message': f'Event "{event_data["title"]}" scheduled for {event_data["date"]}',
            'type': 'new_event',
            'createdAt': datetime.utcnow().isoformat(),
            'isRead': False,
            'eventId': event_data['_id'],
            'caseId': event_data.get('caseId')
        }
        mock_notifications.append(notification)
        
        return jsonify({
            'message': 'Event created successfully',
            'event': event_data
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500 

@bp.route('/form-templates', methods=['GET'])
def get_form_templates():
    """Get available form templates."""
    try:
        templates = [{
            'id': template_id,
            'name': template['name'],
            'description': template['description']
        } for template_id, template in FORM_TEMPLATES.items()]
        
        return jsonify({
            'templates': templates
        })
    except Exception as e:
        logger.error(f"Error getting form templates: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@bp.route('/form-templates/<template_id>', methods=['GET'])
def get_form_template(template_id):
    """Get a specific form template with its schema."""
    try:
        if template_id not in FORM_TEMPLATES:
            return jsonify({'error': 'Template not found'}), 404
            
        return jsonify(FORM_TEMPLATES[template_id])
    except Exception as e:
        logger.error(f"Error getting form template: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@bp.route('/submit-form/<template_id>', methods=['POST'])
@jwt_required()
def submit_form(template_id):
    """Submit a form based on a specific template."""
    try:
        if template_id not in FORM_TEMPLATES:
            return jsonify({'error': 'Template not found'}), 404
            
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No form data provided'}), 400
            
        # Validate form data against schema
        try:
            validate(instance=data, schema=FORM_TEMPLATES[template_id]['schema'])
        except ValidationError as e:
            return jsonify({
                'error': 'Form validation failed',
                'details': str(e)
            }), 400
            
        # Get current user
        current_user_id = get_jwt_identity()
        
        # Create form submission record
        form_submission = {
            'template_id': template_id,
            'user_id': ObjectId(current_user_id),
            'data': data,
            'status': 'submitted',
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        
        # Save to database
        forms_collection = get_mongo_collection('form_submissions')
        # type: ignore[truthy-bool] # PyMongo Collections don't implement __bool__ properly
        if not forms_collection:
            return jsonify({'error': 'Database error'}), 500
            
        result = forms_collection.insert_one(form_submission)
        
        # Create notification for form submission
        notifications_collection = get_mongo_collection('notifications')
        # type: ignore[truthy-bool] # PyMongo Collections don't implement __bool__ properly
        if notifications_collection:
            notification = {
                'user_id': ObjectId(current_user_id),
                'title': f'{FORM_TEMPLATES[template_id]["name"]} Submitted',
                'message': 'Your form has been submitted successfully and is under review.',
                'type': 'form_submission',
                'status': 'unread',
                'created_at': datetime.utcnow()
            }
            notifications_collection.insert_one(notification)
        
        return jsonify({
            'message': 'Form submitted successfully',
            'form_id': str(result.inserted_id)
        }), 201
        
    except Exception as e:
        logger.error(f"Error submitting form: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@bp.route('/forms/<form_id>', methods=['GET'])
@jwt_required()
def get_form_submission(form_id):
    """Get a specific form submission."""
    try:
        current_user_id = get_jwt_identity()
        
        forms_collection = get_mongo_collection('form_submissions')
        if forms_collection is None:
            return jsonify({'error': 'Database error'}), 500
            
        form = forms_collection.find_one({
            '_id': ObjectId(form_id),
            'user_id': ObjectId(current_user_id)
        })
        
        if form is None:
            return jsonify({'error': 'Form not found'}), 404
            
        # Convert ObjectId to string for JSON serialization
        form['_id'] = str(form['_id'])
        form['user_id'] = str(form['user_id'])
        
        return jsonify(form)
    except Exception as e:
        logger.error(f"Error getting form submission: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@bp.route('/submit-form/<template_id>/attachment', methods=['POST'])
@jwt_required()
def upload_form_attachment(template_id):
    """Upload a file attachment for a form submission."""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
            
        file = request.files['file']
        if not file.filename:
            return jsonify({'error': 'No file selected'}), 400
            
        # Validate file
        is_valid, error = validate_file(file)
        if not is_valid:
            return jsonify({'error': error}), 400
            
        current_user_id = get_jwt_identity()
        form_id = request.form.get('form_id')
        
        if not form_id:
            return jsonify({'error': 'Form ID required'}), 400
            
        # Upload to S3
        result = upload_file_to_s3(file, current_user_id, form_id)
        if not result:
            return jsonify({'error': 'File upload failed'}), 500
            
        # Save attachment metadata to database
        attachments_collection = get_mongo_collection('form_attachments')
        # type: ignore[truthy-bool] # PyMongo Collections don't implement __bool__ properly
        if not attachments_collection:
            return jsonify({'error': 'Database error'}), 500
            
        attachment = {
            'form_id': ObjectId(form_id),
            'user_id': ObjectId(current_user_id),
            'file_metadata': result,
            'upload_date': datetime.utcnow(),
            'status': 'pending_review'
        }
        
        attachment_id = attachments_collection.insert_one(attachment).inserted_id
        
        # Update form submission with attachment reference
        forms_collection = get_mongo_collection('form_submissions')
        # type: ignore[truthy-bool] # PyMongo Collections don't implement __bool__ properly
        if forms_collection:
            forms_collection.update_one(
                {'_id': ObjectId(form_id)},
                {
                    '$push': {'attachments': attachment_id},
                    '$set': {'updated_at': datetime.utcnow()}
                }
            )
        
        return jsonify({
            'message': 'File uploaded successfully',
            'attachment': {
                'id': str(attachment_id),
                'filename': result['filename'],
                'url': result['url'],
                'size': result['size'],
                'mime_type': result['mime_type']
            }
        }), 201
        
    except Exception as e:
        logger.error(f"Form attachment upload error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@bp.route('/forms/<form_id>/attachments', methods=['GET'])
@jwt_required()
def get_form_attachments(form_id):
    """Get all attachments for a form submission."""
    try:
        current_user_id = get_jwt_identity()
        
        # Get attachments
        attachments_collection = get_mongo_collection('form_attachments')
        # type: ignore[truthy-bool] # PyMongo Collections don't implement __bool__ properly
        if not attachments_collection:
            return jsonify({'error': 'Database error'}), 500
            
        attachments = list(attachments_collection.find({
            'form_id': ObjectId(form_id),
            'user_id': ObjectId(current_user_id)
        }))
        
        # Generate fresh presigned URLs for each attachment
        s3 = get_s3_client()
        for attachment in attachments:
            s3_path = attachment['file_metadata']['s3_path']
            attachment['file_metadata']['url'] = s3.generate_presigned_url(
                'get_object',
                Params={'Bucket': S3_BUCKET, 'Key': s3_path},
                ExpiresIn=3600
            )
            attachment['_id'] = str(attachment['_id'])
            attachment['form_id'] = str(attachment['form_id'])
            attachment['user_id'] = str(attachment['user_id'])
        
        return jsonify({'attachments': attachments})
    except Exception as e:
        logger.error(f"Get form attachments error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@bp.route('/forms/<form_id>/comments', methods=['POST'])
@jwt_required()
def add_form_comment(form_id: str) -> Union[Response, tuple[Response, int]]:
    """Add a comment to a form submission."""
    collection = get_mongo_collection('form_submissions')
    if collection is None:
        return jsonify({"error": "Database service unavailable"}), 503

    try:
        comment_data = request.get_json()
        if not comment_data or 'text' not in comment_data:
            return jsonify({"error": "Comment text is required"}), 400

        user_id = get_jwt_identity()
        comment = {
            'id': str(uuid.uuid4()),
            'text': comment_data['text'],
            'user_id': user_id,
            'created_at': datetime.utcnow()
        }

        result = collection.update_one(
            {'_id': ObjectId(form_id)},
            {'$push': {'comments': comment}}
        )

        if result.modified_count == 0:
            return jsonify({"error": "Form submission not found"}), 404

        return jsonify({"message": "Comment added successfully", "comment": comment})
    except Exception as e:
        logger.error(f"Error adding comment: {str(e)}")
        return jsonify({"error": "Failed to add comment"}), 500

@bp.route('/forms/<form_id>/comments', methods=['GET'])
@jwt_required()
def get_form_comments(form_id):
    """Get all comments for a form submission."""
    try:
        current_user_id = get_jwt_identity()
        
        # Get user role
        users_collection = get_mongo_collection('users')
        # type: ignore[truthy-bool] # PyMongo Collections don't implement __bool__ properly
        if not users_collection:
            return jsonify({'error': 'Database error'}), 500
            
        user = users_collection.find_one({'_id': ObjectId(current_user_id)})
        if user is None:
            return jsonify({'error': 'User not found'}), 404
            
        is_staff = user.get('role') in ['lawyer', 'admin']
        
        # Build query based on user role
        query = {'form_id': ObjectId(form_id)}
        if not is_staff:
            # type: ignore[assignment] # MongoDB query operators are not properly typed
            query['$or'] = [
                {'visibility': 'all'},
                {'visibility': 'client', 'user_id': ObjectId(current_user_id)}
            ]
        
        # Get comments
        comments_collection = get_mongo_collection('form_comments')
        # type: ignore[truthy-bool] # PyMongo Collections don't implement __bool__ properly
        if not comments_collection:
            return jsonify({'error': 'Database error'}), 500
            
        comments = list(comments_collection.find(query).sort('created_at', 1))
        
        # Convert ObjectIds to strings for JSON serialization
        for comment in comments:
            comment['_id'] = str(comment['_id'])
            comment['user_id'] = str(comment['user_id'])
            comment['form_id'] = str(comment['form_id'])
        
        return jsonify({'comments': comments})
        
    except Exception as e:
        logger.error(f"Get form comments error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@bp.route('/forms/search', methods=['GET'])
@jwt_required()
def search_forms() -> Union[Response, tuple[Response, int]]:
    try:
        current_user_id = get_jwt_identity()
        
        try:
            # Get user role
            user = safe_find_one('users', {'_id': ObjectId(current_user_id)})
            if user is None:
                return jsonify({'error': 'User not found'}), 404
                
            is_staff = user.get('role') in ['lawyer', 'admin']
            
            # Build search query
            query: Dict[str, Any] = {} if is_staff else {'user_id': ObjectId(current_user_id)}
            
            # Apply filters
            status = request.args.get('status')
            if status:
                query['status'] = status
                
            template_id = request.args.get('template_id')
            if template_id:
                query['template_id'] = template_id
                
            # Get pagination parameters
            page = max(1, int(request.args.get('page', 1)))
            per_page = min(50, max(1, int(request.args.get('per_page', 10))))
            skip = (page - 1) * per_page
            
            # Get forms with pagination
            forms = safe_find(
                'form_submissions',
                query,
                skip=skip,
                limit=per_page,
                sort=[('created_at', -1)]
            )
            
            # Get total count for pagination
            total_forms = safe_count_documents('form_submissions', query)
            
            # Process forms
            for form in forms:
                form['_id'] = str(form['_id'])
                form['user_id'] = str(form['user_id'])
                if 'assigned_reviewer' in form:
                    form['assigned_reviewer'] = str(form['assigned_reviewer'])
                if 'comments' in form:
                    form['comments'] = [str(c) for c in form['comments']]
                if 'attachments' in form:
                    form['attachments'] = [str(a) for a in form['attachments']]
            
            return jsonify({
                'forms': forms,
                'total': total_forms,
                'page': page,
                'per_page': per_page,
                'total_pages': (total_forms + per_page - 1) // per_page
            })
            
        except MongoDBError as e:
            logger.error(f"Database error searching forms: {str(e)}")
            return jsonify({'error': 'Database error'}), 500
            
    except Exception as e:
        logger.error(f"Error searching forms: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@bp.route('/forms/stats', methods=['GET'])
@jwt_required()
def get_form_stats():
    """Get statistics about form submissions."""
    try:
        current_user_id = get_jwt_identity()
        
        # Get user role
        users_collection = get_mongo_collection('users')
        # type: ignore[truthy-bool] # PyMongo Collections don't implement __bool__ properly
        if not users_collection:
            return jsonify({'error': 'Database error'}), 500
            
        user = users_collection.find_one({'_id': ObjectId(current_user_id)})
        if user is None:
            return jsonify({'error': 'User not found'}), 404
            
        is_staff = user.get('role') in ['lawyer', 'admin']
        
        # Build base query
        query = {} if is_staff else {'user_id': ObjectId(current_user_id)}
        
        forms_collection = get_mongo_collection('form_submissions')
        # type: ignore[truthy-bool] # PyMongo Collections don't implement __bool__ properly
        if not forms_collection:
            return jsonify({'error': 'Database error'}), 500
            
        # Get status counts
        status_counts = {}
        for status in FormStatus:
            count = forms_collection.count_documents({**query, 'status': status.value})
            status_counts[status.value] = count
            
        # Get template counts
        template_counts = {}
        for template_id in FORM_TEMPLATES:
            count = forms_collection.count_documents({**query, 'template_id': template_id})
            template_counts[template_id] = count
            
        # Get timeline data (forms per day for last 30 days)
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        timeline_query = {
            **query,
            'created_at': {'$gte': thirty_days_ago}
        }
        
        timeline_data = list(forms_collection.aggregate([
            {'$match': timeline_query},
            {
                '$group': {
                    '_id': {
                        '$dateToString': {
                            'format': '%Y-%m-%d',
                            'date': '$created_at'
                        }
                    },
                    'count': {'$sum': 1}
                }
            },
            {'$sort': {'_id': 1}}
        ]))
        
        # Fill in missing dates with zero counts
        timeline = {}
        current_date = thirty_days_ago
        while current_date <= datetime.utcnow():
            date_str = current_date.strftime('%Y-%m-%d')
            timeline[date_str] = 0
            current_date += timedelta(days=1)
            
        for data in timeline_data:
            timeline[data['_id']] = data['count']
        
        return jsonify({
            'total_forms': forms_collection.count_documents(query),
            'status_counts': status_counts,
            'template_counts': template_counts,
            'timeline': timeline
        })
        
    except Exception as e:
        logger.error(f"Get form stats error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@bp.route('/form-templates', methods=['POST'])
@jwt_required()
@lawyer_required
def create_form_template():
    """Create a new form template."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No template data provided'}), 400
            
        required_fields = ['name', 'description', 'schema']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400
            
        current_user_id = get_jwt_identity()
        
        # Create template document
        template = {
            'name': data['name'],
            'description': data['description'],
            'schema': data['schema'],
            'created_by': ObjectId(current_user_id),
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow(),
            'status': TemplateStatus.DRAFT.value,
            'version': 1,
            'category': data.get('category', 'general'),
            'tags': data.get('tags', []),
            'is_active': True
        }
        
        # Validate schema structure
        try:
            validate(instance={'test': True}, schema=template['schema'])
        except ValidationError as e:
            return jsonify({
                'error': 'Invalid JSON schema',
                'details': str(e)
            }), 400
            
        # Save template
        templates_collection = get_mongo_collection('form_templates')
        # type: ignore[truthy-bool] # PyMongo Collections don't implement __bool__ properly
        if not templates_collection:
            return jsonify({'error': 'Database error'}), 500
            
        result = templates_collection.insert_one(template)
        
        return jsonify({
            'message': 'Template created successfully',
            'template_id': str(result.inserted_id)
        }), 201
        
    except Exception as e:
        logger.error(f"Create template error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@bp.route('/form-templates/<template_id>', methods=['PUT'])
@jwt_required()
@lawyer_required
def update_form_template(template_id):
    """Update an existing form template, creating a new version."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No template data provided'}), 400
            
        current_user_id = get_jwt_identity()
        
        # Get current template
        templates_collection = get_mongo_collection('form_templates')
        if not templates_collection:
            return jsonify({'error': 'Database error'}), 500
            
        current_template = templates_collection.find_one({
            '_id': ObjectId(template_id),
            'is_active': True
        })
        
        if not current_template:
            return jsonify({'error': 'Template not found'}), 404
            
        # Create new version
        new_version = current_template['version'] + 1
        
        # Archive current version
        templates_collection.update_one(
            {'_id': ObjectId(template_id)},
            {'$set': {'is_active': False}}
        )
        
        # Create new version document
        new_template = {
            'name': data.get('name', current_template['name']),
            'description': data.get('description', current_template['description']),
            'schema': data.get('schema', current_template['schema']),
            'created_by': ObjectId(current_user_id),
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow(),
            'status': TemplateStatus.DRAFT.value,
            'version': new_version,
            'category': data.get('category', current_template['category']),
            'tags': data.get('tags', current_template['tags']),
            'previous_version': ObjectId(template_id),
            'is_active': True
        }
        
        # Validate schema if changed
        if 'schema' in data:
            try:
                validate(instance={'test': True}, schema=new_template['schema'])
            except ValidationError as e:
                return jsonify({
                    'error': 'Invalid JSON schema',
                    'details': str(e)
                }), 400
                
        # Save new version
        result = templates_collection.insert_one(new_template)
        
        return jsonify({
            'message': 'Template updated successfully',
            'template_id': str(result.inserted_id),
            'version': new_version
        })
        
    except Exception as e:
        logger.error(f"Update template error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@bp.route('/form-templates/<template_id>/status', methods=['PUT'])
@jwt_required()
@lawyer_required
def update_template_status(template_id):
    """Update the status of a form template."""
    try:
        data = request.get_json()
        if not data or 'status' not in data:
            return jsonify({'error': 'New status is required'}), 400
            
        new_status = data['status']
        try:
            new_status = TemplateStatus(new_status)
        except ValueError:
            return jsonify({'error': f'Invalid status. Must be one of: {[s.value for s in TemplateStatus]}'}), 400
            
        templates_collection = get_mongo_collection('form_templates')
        if not templates_collection:
            return jsonify({'error': 'Database error'}), 500
            
        result = templates_collection.update_one(
            {'_id': ObjectId(template_id), 'is_active': True},
            {
                '$set': {
                    'status': new_status.value,
                    'updated_at': datetime.utcnow(),
                    'updated_by': ObjectId(get_jwt_identity())
                }
            }
        )
        
        if result.modified_count == 0:
            return jsonify({'error': 'Template not found or not modified'}), 404
            
        return jsonify({
            'message': 'Template status updated successfully',
            'new_status': new_status.value
        })
        
    except Exception as e:
        logger.error(f"Update template status error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@bp.route('/form-templates/categories', methods=['GET'])
def get_template_categories():
    """Get all template categories with counts."""
    try:
        templates_collection = get_mongo_collection('form_templates')
        # type: ignore[truthy-bool] # PyMongo Collections don't implement __bool__ properly
        if not templates_collection:
            return jsonify({'error': 'Database error'}), 500
            
        # Get category counts
        categories = list(templates_collection.aggregate([
            {'$match': {'is_active': True}},
            {
                '$group': {
                    '_id': '$category',
                    'count': {'$sum': 1},
                    'templates': {'$push': {
                        'id': '$_id',
                        'name': '$name',
                        'description': '$description',
                        'status': '$status'
                    }}
                }
            },
            {'$sort': {'_id': 1}}
        ]))
        
        # Process results
        for category in categories:
            category['category'] = category.pop('_id')
            # Convert ObjectIds in templates list
            for template in category['templates']:
                template['id'] = str(template['id'])
        
        return jsonify({'categories': categories})
        
    except Exception as e:
        logger.error(f"Get template categories error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@bp.route('/form-templates/<template_id>/versions', methods=['GET'])
@jwt_required()
def get_template_versions(template_id):
    """Get all versions of a template."""
    try:
        templates_collection = get_mongo_collection('form_templates')
        if not templates_collection:
            return jsonify({'error': 'Database error'}), 500
            
        # Get current version
        current = templates_collection.find_one({
            '_id': ObjectId(template_id)
        })
        
        if not current:
            return jsonify({'error': 'Template not found'}), 404
            
        # Get all versions
        versions = []
        template = current
        
        while template:
            version_data = {
                'id': str(template['_id']),
                'version': template['version'],
                'status': template['status'],
                'created_at': template['created_at'].isoformat(),
                'created_by': str(template['created_by']),
                'is_active': template.get('is_active', False)
            }
            versions.append(version_data)
            
            # Get previous version if exists
            if 'previous_version' in template:
                template = templates_collection.find_one({
                    '_id': template['previous_version']
                })
            else:
                template = None
        
        return jsonify({
            'versions': sorted(versions, key=lambda x: x['version'], reverse=True)
        })
        
    except Exception as e:
        logger.error(f"Get template versions error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500 