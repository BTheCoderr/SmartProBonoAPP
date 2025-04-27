"""
Module for managing mock data for development and testing
"""
import uuid
from datetime import datetime, timedelta

# Mock data storage for testing purposes
mock_immigration_intake = []
mock_cases = []
mock_documents = {}  # Case ID -> list of documents
mock_notifications = []
mock_events = []

def create_notification(title, message, notification_type, entity_id=None, entity_type=None, is_read=False):
    """
    Create a notification with standard fields
    
    Args:
        title (str): The notification title
        message (str): The notification message
        notification_type (str): The type of notification (e.g., 'new_case', 'status_change')
        entity_id (str, optional): ID of the related entity (case, form, etc.)
        entity_type (str, optional): Type of the related entity ('case', 'form', 'event', etc.)
        is_read (bool, optional): Whether the notification has been read
        
    Returns:
        dict: The created notification
    """
    notification = {
        '_id': str(uuid.uuid4()),
        'title': title,
        'message': message,
        'type': notification_type,
        'createdAt': datetime.utcnow().isoformat(),
        'isRead': is_read
    }
    
    # Add entity reference if provided
    if entity_id and entity_type:
        if entity_type == 'case':
            notification['caseId'] = entity_id
        elif entity_type == 'form':
            notification['formId'] = entity_id
        elif entity_type == 'event':
            notification['eventId'] = entity_id
            
    return notification

def add_timestamps(data_object, include_updated=True):
    """
    Add standard timestamps to a data object
    
    Args:
        data_object (dict): The data object to add timestamps to
        include_updated (bool, optional): Whether to include updatedAt
        
    Returns:
        dict: The updated data object
    """
    now = datetime.utcnow()
    data_object['createdAt'] = now.isoformat()
    
    if include_updated:
        data_object['updatedAt'] = now.isoformat()
        
    return data_object

def add_id(data_object):
    """
    Add a unique ID to a data object
    
    Args:
        data_object (dict): The data object to add an ID to
        
    Returns:
        dict: The updated data object
    """
    data_object['_id'] = str(uuid.uuid4())
    return data_object

def validate_required_fields(data, required_fields):
    """
    Validate that required fields are present
    
    Args:
        data (dict): The data to validate
        required_fields (list): List of required field names
        
    Returns:
        tuple: (is_valid, missing_fields)
    """
    missing = [field for field in required_fields if field not in data]
    return len(missing) == 0, missing

def populate_mock_data():
    """
    Populate mock data for testing if they don't exist already
    """
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