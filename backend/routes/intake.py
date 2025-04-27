"""
Routes for handling intake form submissions
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from backend.database.mongo import mongo
from backend.models.user import User
from bson import ObjectId
import logging
from typing import Tuple, Dict, Any
from pymongo.collection import Collection
import re
import phonenumbers
from email_validator import validate_email, EmailNotValidError
from werkzeug.utils import secure_filename
import os
from flask import current_app

logger = logging.getLogger(__name__)
bp = Blueprint('intake', __name__)

# Define valid immigration statuses
IMMIGRATION_STATUSES = [
    {'value': 'us_citizen', 'label': 'U.S. Citizen'},
    {'value': 'permanent_resident', 'label': 'Permanent Resident (Green Card)'},
    {'value': 'conditional_resident', 'label': 'Conditional Resident'},
    {'value': 'temporary_visa', 'label': 'Temporary Visa Holder'},
    {'value': 'refugee', 'label': 'Refugee'},
    {'value': 'asylee', 'label': 'Asylee'},
    {'value': 'daca', 'label': 'DACA Recipient'},
    {'value': 'tps', 'label': 'Temporary Protected Status (TPS)'},
    {'value': 'undocumented', 'label': 'Undocumented'},
    {'value': 'visa_overstay', 'label': 'Visa Overstay'},
    {'value': 'student_visa', 'label': 'Student Visa (F-1/M-1)'},
    {'value': 'work_visa', 'label': 'Work Visa (H-1B, L-1, etc.)'},
    {'value': 'visitor_visa', 'label': 'Visitor Visa (B-1/B-2)'},
    {'value': 'pending_asylum', 'label': 'Pending Asylum Application'},
    {'value': 'pending_adjustment', 'label': 'Pending Adjustment of Status'},
    {'value': 'other', 'label': 'Other'}
]

# Define valid visa types
VISA_TYPES = [
    {'value': 'family', 'label': 'Family-Based Immigration'},
    {'value': 'employment', 'label': 'Employment-Based Immigration'},
    {'value': 'student', 'label': 'Student Visa'},
    {'value': 'visitor', 'label': 'Visitor Visa'},
    {'value': 'refugee', 'label': 'Refugee/Asylum'},
    {'value': 'citizenship', 'label': 'Citizenship/Naturalization'},
    {'value': 'other', 'label': 'Other Immigration Matter'}
]

def validate_phone_number(phone: str) -> bool:
    """Validate phone number format"""
    try:
        parsed = phonenumbers.parse(phone, "US")
        return phonenumbers.is_valid_number(parsed)
    except phonenumbers.NumberParseException:
        return False

def validate_email_address(email: str) -> bool:
    """Validate email address format"""
    try:
        validate_email(email)
        return True
    except EmailNotValidError:
        return False

def validate_date(date_str: str) -> bool:
    """Validate date format and range"""
    try:
        date = datetime.strptime(date_str, '%Y-%m-%d')
        return date <= datetime.now() and date >= datetime(1900, 1, 1)
    except ValueError:
        return False

def validate_name(name: str) -> bool:
    """Validate name format"""
    return bool(re.match(r'^[a-zA-Z\s-\']{2,50}$', name))

def validate_intake_data(data: Dict[Any, Any]) -> Tuple[bool, str]:
    """Validate intake form data"""
    # Required fields with their validation functions
    required_validations = {
        'firstName': (validate_name, 'Invalid first name format'),
        'lastName': (validate_name, 'Invalid last name format'),
        'email': (validate_email_address, 'Invalid email format'),
        'phone': (validate_phone_number, 'Invalid phone number format'),
        'dateOfBirth': (validate_date, 'Invalid date of birth'),
        'immigrationStatus': (lambda x: x in [s['value'] for s in IMMIGRATION_STATUSES], 'Invalid immigration status'),
        'visaType': (lambda x: x in [v['value'] for v in VISA_TYPES], 'Invalid visa type'),
        'urgency': (lambda x: x in ['high', 'medium', 'low'], 'Invalid urgency level'),
    }

    # Check required fields presence
    for field in required_validations:
        if field not in data:
            return False, f'Missing required field: {field}'
        
        # Validate field format
        validator, error_msg = required_validations[field]
        if not validator(data[field]):
            return False, error_msg

    # Validate conditional fields
    if data.get('priorApplications'):
        if not data.get('priorApplicationDetails'):
            return False, 'Prior application details required when prior applications is true'
        if len(data['priorApplicationDetails']) < 20:
            return False, 'Prior application details too short'

    # Validate case description
    if not data.get('caseDescription'):
        return False, 'Case description is required'
    if len(data['caseDescription']) < 50:
        return False, 'Case description too short'
    if len(data['caseDescription']) > 2000:
        return False, 'Case description too long'

    return True, ''

def get_collections() -> Tuple[Collection, Collection]:
    """Get MongoDB collections for intakes and cases"""
    db = mongo.db
    if db is None:
        raise RuntimeError("MongoDB connection not available")
    return db.intakes, db.cases

@bp.route('/api/intake/immigration', methods=['POST'])
@jwt_required()
def submit_immigration_intake():
    """Submit an immigration intake form"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        if not user:
            return jsonify({'message': 'User not found'}), 404

        data = request.get_json()
        if not data:
            return jsonify({'message': 'No data provided'}), 400

        # Validate form data
        is_valid, error_message = validate_intake_data(data)
        if not is_valid:
            return jsonify({'message': error_message}), 400

        # Create intake document with metadata
        intake_data = {
            'user_id': str(current_user_id),
            'status': 'pending_review',
            'submission_date': datetime.utcnow(),
            'form_type': 'immigration',
            'personal_info': {
                'first_name': data['firstName'],
                'last_name': data['lastName'],
                'email': data['email'],
                'phone': data['phone'],
                'date_of_birth': data['dateOfBirth'],
                'nationality': data['nationality'],
                'current_residence': data['currentResidence']
            },
            'immigration_info': {
                'status': data['immigrationStatus'],
                'visa_type': data['visaType'],
                'prior_applications': data.get('priorApplications', False),
                'prior_application_details': data.get('priorApplicationDetails', ''),
                'desired_service': data['desiredService']
            },
            'case_info': {
                'description': data['caseDescription'],
                'urgency': data['urgency'],
                'has_legal_representation': data.get('hasLegalRepresentation', 'no'),
                'special_circumstances': data.get('specialCircumstances', '')
            },
            'documents': data.get('documents', []),
            'metadata': {
                'ip_address': request.remote_addr,
                'user_agent': request.user_agent.string,
                'submission_platform': data.get('metadata', {}).get('submissionPlatform', 'web'),
                'form_version': data.get('metadata', {}).get('formVersion', '1.0'),
                'browser': data.get('metadata', {}).get('browser', '')
            }
        }

        # Get collections
        intakes_collection, cases_collection = get_collections()

        # Save to MongoDB
        result = intakes_collection.insert_one(intake_data)
        if not result.inserted_id:
            logger.error('Failed to save intake form to database')
            return jsonify({'message': 'Failed to save intake form'}), 500

        # Create a case reference
        case_ref = {
            'intake_id': str(result.inserted_id),
            'user_id': str(current_user_id),
            'status': 'new',
            'created_at': datetime.utcnow(),
            'type': 'immigration',
            'priority': data['urgency'],
            'assigned_to': None
        }
        
        case_result = cases_collection.insert_one(case_ref)
        if not case_result.inserted_id:
            logger.warning('Failed to create case reference for intake')

        return jsonify({
            'message': 'Intake form submitted successfully',
            'id': str(result.inserted_id),
            'case_id': str(case_result.inserted_id) if case_result.inserted_id else None
        }), 201

    except Exception as e:
        logger.error(f'Error submitting intake form: {str(e)}')
        return jsonify({
            'message': 'An error occurred while processing your submission',
            'error': str(e)
        }), 500

@bp.route('/api/intake/<intake_id>', methods=['GET'])
@jwt_required()
def get_intake(intake_id):
    """Get an intake form by ID"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        if not user:
            return jsonify({'message': 'User not found'}), 404

        # Validate intake ID
        if not ObjectId.is_valid(intake_id):
            return jsonify({'message': 'Invalid intake ID'}), 400

        # Get collections
        intakes_collection, _ = get_collections()

        # Get intake document
        intake = intakes_collection.find_one({'_id': ObjectId(intake_id)})
        if not intake:
            return jsonify({'message': 'Intake form not found'}), 404

        # Check if user has permission to view this intake
        if str(intake['user_id']) != str(current_user_id) and user.role not in ['admin', 'lawyer']:
            return jsonify({'message': 'Unauthorized to view this intake form'}), 403

        # Convert ObjectId to string for JSON serialization
        intake['_id'] = str(intake['_id'])
        return jsonify(intake), 200

    except Exception as e:
        logger.error(f'Error retrieving intake form: {str(e)}')
        return jsonify({'message': 'An error occurred while retrieving the intake form'}), 500

@bp.route('/api/intake/<intake_id>/status', methods=['PUT'])
@jwt_required()
def update_intake_status(intake_id):
    """Update the status of an intake form"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        if not user or user.role not in ['admin', 'lawyer']:
            return jsonify({'message': 'Unauthorized to update intake status'}), 403

        data = request.get_json()
        if not data or 'status' not in data:
            return jsonify({'message': 'No status provided'}), 400

        # Validate intake ID
        if not ObjectId.is_valid(intake_id):
            return jsonify({'message': 'Invalid intake ID'}), 400

        # Get collections
        intakes_collection, _ = get_collections()

        # Update intake status
        result = intakes_collection.update_one(
            {'_id': ObjectId(intake_id)},
            {
                '$set': {
                    'status': data['status'],
                    'updated_at': datetime.utcnow(),
                    'updated_by': str(current_user_id)
                }
            }
        )

        if result.modified_count == 0:
            return jsonify({'message': 'Intake form not found or status not changed'}), 404

        return jsonify({'message': 'Intake status updated successfully'}), 200

    except Exception as e:
        logger.error(f'Error updating intake status: {str(e)}')
        return jsonify({'message': 'An error occurred while updating the intake status'}), 500

@bp.route('/api/intake/<intake_id>/documents', methods=['POST'])
@jwt_required()
def upload_intake_documents(intake_id):
    """Upload documents for an intake form"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        if not user:
            return jsonify({'message': 'User not found'}), 404

        # Validate intake ID
        if not ObjectId.is_valid(intake_id):
            return jsonify({'message': 'Invalid intake ID'}), 400

        # Get collections
        intakes_collection, _ = get_collections()

        # Check if intake exists and user has permission
        intake = intakes_collection.find_one({'_id': ObjectId(intake_id)})
        if not intake:
            return jsonify({'message': 'Intake form not found'}), 404
        if str(intake['user_id']) != str(current_user_id) and user.role not in ['admin', 'lawyer']:
            return jsonify({'message': 'Unauthorized to upload documents for this intake'}), 403

        # Handle file uploads
        if 'files' not in request.files:
            return jsonify({'message': 'No files provided'}), 400

        uploaded_files = request.files.getlist('files')
        if not uploaded_files:
            return jsonify({'message': 'No files selected'}), 400

        # Process each uploaded file
        saved_files = []
        for file in uploaded_files:
            if file and file.filename:
                # Generate secure filename
                filename = secure_filename(file.filename)
                
                # Create document metadata
                doc_data = {
                    'original_name': file.filename,
                    'stored_name': filename,
                    'upload_date': datetime.utcnow(),
                    'uploaded_by': str(current_user_id),
                    'document_type': request.form.get('document_type', 'other'),
                    'status': 'pending_review'
                }

                # Save file metadata to intake document
                result = intakes_collection.update_one(
                    {'_id': ObjectId(intake_id)},
                    {
                        '$push': {
                            'documents': doc_data
                        }
                    }
                )

                if result.modified_count > 0:
                    # Save file to storage
                    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                    file.save(file_path)
                    saved_files.append(doc_data)

        if not saved_files:
            return jsonify({'message': 'Failed to save any files'}), 500

        return jsonify({
            'message': 'Documents uploaded successfully',
            'uploaded_files': saved_files
        }), 201

    except Exception as e:
        logger.error(f'Error uploading documents: {str(e)}')
        return jsonify({'message': 'An error occurred while uploading documents'}), 500

@bp.route('/api/intake/<intake_id>/documents', methods=['GET'])
@jwt_required()
def get_intake_documents(intake_id):
    """Get documents associated with an intake form"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        if not user:
            return jsonify({'message': 'User not found'}), 404

        # Validate intake ID
        if not ObjectId.is_valid(intake_id):
            return jsonify({'message': 'Invalid intake ID'}), 400

        # Get collections
        intakes_collection, _ = get_collections()

        # Check if intake exists and user has permission
        intake = intakes_collection.find_one({'_id': ObjectId(intake_id)})
        if not intake:
            return jsonify({'message': 'Intake form not found'}), 404
        if str(intake['user_id']) != str(current_user_id) and user.role not in ['admin', 'lawyer']:
            return jsonify({'message': 'Unauthorized to view documents for this intake'}), 403

        # Get documents list
        documents = intake.get('documents', [])
        return jsonify({
            'intake_id': intake_id,
            'documents': documents
        }), 200

    except Exception as e:
        logger.error(f'Error retrieving documents: {str(e)}')
        return jsonify({'message': 'An error occurred while retrieving documents'}), 500 