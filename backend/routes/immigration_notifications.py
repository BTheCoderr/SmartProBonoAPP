"""
Integration of notifications with the immigration process
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils.responses import success_response, error_response
from utils.logging_setup import get_logger
from notifications.services import send_user_notification

# Set up logging
logger = get_logger('immigration_notifications')

# Create a blueprint
immigration_notifications_bp = Blueprint('immigration_notifications', __name__, url_prefix='/api/notifications/immigration')

@immigration_notifications_bp.route('/test', methods=['POST'])
def test_notification():
    """
    Send a test notification to the user
    
    Returns:
        Success message
    """
    try:
        data = request.get_json() or {}
        user_id = data.get('user_id', 'test_user')
        
        notification = send_user_notification(
            user_id=user_id,
            title="Test Notification",
            message="This is a test notification from the server.",
            notification_type="info",
            category="test"
        )
        
        return success_response(
            message="Test notification sent successfully",
            data={"notification": notification}
        )
    except Exception as e:
        logger.error(f"Error sending test notification: {str(e)}")
        return error_response(message=f"Failed to send notification: {str(e)}")

@immigration_notifications_bp.route('/form-submitted', methods=['POST'])
@jwt_required()
def form_submission_notification():
    """
    Send a notification for a form submission
    
    Returns:
        Success message
    """
    try:
        data = request.get_json()
        if not data:
            return error_response(message="No data provided")
        
        # Get form details
        form_id = data.get('form_id')
        form_type = data.get('form_type', 'immigration')
        
        if not form_id:
            return error_response(message="Missing required field: form_id")
        
        # Get the current user from the JWT token
        user_id = get_jwt_identity()
        
        # Send notification
        notification = send_user_notification(
            user_id=user_id,
            title="Form Submitted Successfully",
            message=f"Your {form_type} form has been submitted successfully.",
            notification_type="success",
            category="immigration",
            additional_data={
                "formId": form_id,
                "formType": form_type
            }
        )
        
        # Notify admin (if applicable)
        # This would be implemented separately with admin user IDs
        
        return success_response(
            message="Form submission notification sent",
            data={"notification": notification}
        )
    except Exception as e:
        logger.error(f"Error sending form submission notification: {str(e)}")
        return error_response(message=f"Failed to send notification: {str(e)}")

@immigration_notifications_bp.route('/status-update', methods=['POST'])
@jwt_required()
def status_update_notification():
    """
    Send a notification for a status update
    
    Returns:
        Success message
    """
    try:
        data = request.get_json()
        if not data:
            return error_response(message="No data provided")
        
        # Get required fields
        case_id = data.get('case_id')
        old_status = data.get('old_status')
        new_status = data.get('new_status')
        
        if not all([case_id, new_status]):
            return error_response(message="Missing required fields: case_id, new_status")
        
        # Get the current user from the JWT token
        user_id = get_jwt_identity()
        
        # Determine notification type based on status
        if new_status.lower() in ['approved', 'completed', 'accepted']:
            notification_type = 'success'
            message = f"Your case status has been updated to {new_status}."
        elif new_status.lower() in ['rejected', 'denied', 'cancelled']:
            notification_type = 'error'
            message = f"Your case status has been updated to {new_status}."
        elif new_status.lower() in ['pending', 'in review', 'processing']:
            notification_type = 'info'
            message = f"Your case is now {new_status}."
        else:
            notification_type = 'info'
            message = f"Your case status has been updated to {new_status}."
        
        # Send notification
        notification = send_user_notification(
            user_id=user_id,
            title="Case Status Updated",
            message=message,
            notification_type=notification_type,
            category="immigration",
            additional_data={
                "caseId": case_id,
                "oldStatus": old_status,
                "newStatus": new_status
            }
        )
        
        return success_response(
            message="Status update notification sent",
            data={"notification": notification}
        )
    except Exception as e:
        logger.error(f"Error sending status update notification: {str(e)}")
        return error_response(message=f"Failed to send notification: {str(e)}") 