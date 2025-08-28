"""
Routes for immigration services
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from datetime import datetime
from functools import wraps
import os
from werkzeug.utils import secure_filename

# Import our new utilities
from utils.decorators import handle_exceptions, validate_json_request
from utils.responses import success_response, error_response, not_found_response
from utils.mock_data import (
    mock_immigration_intake, mock_cases, mock_documents, mock_notifications, mock_events,
    create_notification, add_timestamps, add_id, validate_required_fields, populate_mock_data
)
from services.notification_service import get_notification_service

# Create blueprint
immigration = Blueprint('immigration', __name__, url_prefix='/api/immigration')

# Role-based access control decorator
def lawyer_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        # Get JWT claims
        claims = get_jwt()
        role = claims.get('role', '')
        
        # Check if user has lawyer or admin role
        if role not in ['lawyer', 'admin']:
            return error_response('Access denied. Lawyer or admin rights required.', status_code=403)
        
        return fn(*args, **kwargs)
    
    return wrapper

# Populate mock data
populate_mock_data()

@immigration.route('/cases', methods=['GET'])
@jwt_required()
@handle_exceptions
def get_cases():
    """Get all cases for the current user"""
    # Get user identity
    user_id = get_jwt_identity()
    
    # In a real app, we'd filter cases by user_id
    # For mock data, just return all
    return success_response(message="Cases retrieved successfully", data={"cases": mock_cases})

@immigration.route('/cases', methods=['POST'])
@jwt_required()
@validate_json_request(['clientName', 'caseType', 'status'])
@handle_exceptions
def create_case():
    """Create a new case"""
    case_data = request.get_json()
    
    # Add timestamps and ID
    add_timestamps(case_data)
    add_id(case_data)
    
    # Add to mock data
    mock_cases.append(case_data)
    
    # Create a notification for new case
    notification = create_notification(
        title='New Case Created',
        message=f'Case {case_data.get("title", "New Case")} has been created',
        notification_type='new_case',
        entity_id=case_data['_id'],
        entity_type='case'
    )
    mock_notifications.append(notification)
    
    return success_response(message='Case created successfully', data=case_data, status_code=201)

@immigration.route('/cases/<case_id>', methods=['GET'])
@jwt_required()
@handle_exceptions
def get_case(case_id):
    """Get a specific case by ID"""
    for case in mock_cases:
        if case['_id'] == case_id:
            return success_response(message="Case retrieved successfully", data=case)
    
    return not_found_response('case', case_id)

@immigration.route('/cases/<case_id>', methods=['PUT'])
@jwt_required()
@handle_exceptions
def update_case(case_id):
    """Update a case"""
    case_data = request.get_json()
    case_data['updatedAt'] = datetime.utcnow().isoformat()
    
    # Find and update case in mock data
    for i, case in enumerate(mock_cases):
        if case['_id'] == case_id:
            # Keep the original ID
            original_id = case['_id']
            # Update with new data but preserve the ID
            mock_cases[i].update(case_data)
            mock_cases[i]['_id'] = original_id
            
            # Create a notification for case update
            notification = create_notification(
                title='Case Updated',
                message=f'Case {mock_cases[i].get("title", "Unnamed Case")} has been updated',
                notification_type='case_update',
                entity_id=case_id,
                entity_type='case'
            )
            mock_notifications.append(notification)
            
            return success_response(message='Case updated successfully', data=mock_cases[i])
            
    return not_found_response('case', case_id)

@immigration.route('/cases/<case_id>/status', methods=['PUT'])
@jwt_required()
@validate_json_request(['status'])
@handle_exceptions
def update_case_status(case_id):
    """Update a case's status"""
    data = request.get_json()
    status = data['status']
    
    valid_statuses = ['new', 'in-progress', 'completed', 'delayed']
    if status not in valid_statuses:
        return error_response(f'Status must be one of: {", ".join(valid_statuses)}')
        
    # Find and update case status
    for case in mock_cases:
        if case['_id'] == case_id:
            old_status = case['status']
            case['status'] = status
            case['updatedAt'] = datetime.utcnow().isoformat()
            
            # Create a notification for status change
            notification = create_notification(
                title='Case Status Changed',
                message=f'Case status changed from {old_status} to {status}',
                notification_type='status_change',
                entity_id=case_id,
                entity_type='case'
            )
            mock_notifications.append(notification)
            
            return success_response(
                message='Case status updated successfully', 
                data={'case': case}
            )
            
    return not_found_response('case', case_id)

@immigration.route('/cases/<case_id>', methods=['DELETE'])
@jwt_required()
@lawyer_required
@handle_exceptions
def delete_case(case_id):
    """Delete a case and all associated data"""
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
            
            return success_response(
                message='Case deleted successfully',
                data={'deletedCase': deleted_case}
            )
            
    return not_found_response('case', case_id)

@immigration.route('/intake-form', methods=['POST'])
@validate_json_request(['firstName', 'lastName', 'email', 'phone', 'dateOfBirth'])
@handle_exceptions
def submit_intake_form():
    """Submit a new immigration intake form"""
    form_data = request.get_json()
    notification_service = get_notification_service()
    
    # Get user ID from token if authenticated, or use anonymous
    user_id = None
    try:
        user_id = get_jwt_identity()
    except:
        pass  # User might not be authenticated
    
    # Add timestamps
    add_timestamps(form_data, include_updated=False)
    
    # Add status for tracking
    form_data['status'] = 'new'
    
    # Generate mock ID
    add_id(form_data)
    
    # Add user ID if authenticated
    if user_id:
        form_data['userId'] = user_id
    
    # Add to mock data storage
    mock_immigration_intake.append(form_data)
    
    # Create a notification for new intake form
    notification = create_notification(
        title='New Intake Form Submitted',
        message=f'A new intake form has been submitted by {form_data["firstName"]} {form_data["lastName"]}',
        notification_type='new_form',
        entity_id=form_data['_id'],
        entity_type='form'
    )
    mock_notifications.append(notification)
    
    # Send notification to the user who submitted the form (if authenticated)
    if user_id:
        notification_service.send_user_notification(
            user_id=user_id,
            message=f'Your immigration form has been submitted successfully.',
            notification_type='success',
            additional_data={
                'formId': form_data['_id'],
                'title': 'Form Submitted',
                'category': 'immigration'
            }
        )
    
    # Send notification to admin users about the new form
    # In a real application, you would query for admin users and send to each
    # For now, we'll simulate sending to a fake admin
    admin_user_id = "admin_user_id"  # Replace with actual admin user ID in production
    notification_service.send_user_notification(
        user_id=admin_user_id,
        message=f'New immigration form submitted by {form_data["firstName"]} {form_data["lastName"]}',
        notification_type='info',
        additional_data={
            'formId': form_data['_id'],
            'title': 'New Form Submission',
            'category': 'immigration_admin'
        }
    )
    
    return success_response(
        message='Immigration intake form submitted successfully',
        data={'id': form_data['_id']},
        status_code=201
    ) 