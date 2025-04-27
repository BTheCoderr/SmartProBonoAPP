from flask import Blueprint, request, jsonify
from backend.utils.error_handlers import handle_exceptions
from backend.utils.decorators import token_required
from backend.websocket.services.notification_service import (
    get_user_notifications,
    mark_notification_read,
    delete_notification,
    get_notification_stats
)
from backend.websocket.services.application_notifications import (
    send_user_notification,
    send_case_status_update,
    send_document_request,
    send_document_uploaded_notification,
    send_appointment_reminder,
    send_message_notification,
    send_immigration_form_notification
)

bp = Blueprint('notifications', __name__)

@bp.route('/notifications', methods=['GET'])
@token_required
@handle_exceptions
def get_notifications(current_user):
    """Get notifications for the current user."""
    include_read = request.args.get('include_read', 'false').lower() == 'true'
    limit = int(request.args.get('limit', 50))
    
    notifications = get_user_notifications(
        user_id=current_user['_id'],
        include_read=include_read,
        limit=limit
    )
    return jsonify(notifications)

@bp.route('/notifications/<notification_id>/read', methods=['POST'])
@token_required
@handle_exceptions
def mark_read(current_user, notification_id):
    """Mark a notification as read."""
    success = mark_notification_read(
        notification_id=notification_id,
        user_id=current_user['_id']
    )
    if success:
        return jsonify({'message': 'Notification marked as read'}), 200
    return jsonify({'error': 'Notification not found'}), 404

@bp.route('/notifications/<notification_id>', methods=['DELETE'])
@token_required
@handle_exceptions
def delete_user_notification(current_user, notification_id):
    """Delete a notification."""
    result = delete_notification(
        notification_id=notification_id,
        user_id=current_user['_id']
    )
    return jsonify(result)

@bp.route('/notifications/stats', methods=['GET'])
@token_required
@handle_exceptions
def notification_stats(current_user):
    """Get notification statistics."""
    stats = get_notification_stats()
    return jsonify(stats)

@bp.route('/notifications/send', methods=['POST'])
@token_required
@handle_exceptions
def send_notification_endpoint(current_user):
    """Send a notification to a user."""
    data = request.get_json()
    
    notification_type = data.get('type', 'info')
    if notification_type not in ['info', 'success', 'warning', 'error']:
        return jsonify({'error': 'Invalid notification type'}), 400
    
    result = send_user_notification(
        user_id=data['user_id'],
        title=data['title'],
        message=data['message'],
        notification_type=notification_type,
        data=data.get('data')
    )
    return jsonify(result)

@bp.route('/notifications/case-status', methods=['POST'])
@token_required
@handle_exceptions
def send_case_status_notification(current_user):
    """Send a case status update notification."""
    data = request.get_json()
    
    result = send_case_status_update(
        user_id=data['user_id'],
        case_id=data['case_id'],
        status=data['status'],
        details=data.get('details')
    )
    return jsonify(result)

@bp.route('/notifications/document-request', methods=['POST'])
@token_required
@handle_exceptions
def send_document_request_notification(current_user):
    """Send a document request notification."""
    data = request.get_json()
    
    result = send_document_request(
        user_id=data['user_id'],
        document_type=data['document_type'],
        due_date=data.get('due_date'),
        case_id=data.get('case_id')
    )
    return jsonify(result)

@bp.route('/notifications/document-uploaded', methods=['POST'])
@token_required
@handle_exceptions
def send_document_uploaded(current_user):
    """Send a document uploaded notification."""
    data = request.get_json()
    
    result = send_document_uploaded_notification(
        attorney_id=data['attorney_id'],
        client_id=data['client_id'],
        document_type=data['document_type'],
        case_id=data.get('case_id')
    )
    return jsonify(result)

@bp.route('/notifications/appointment-reminder', methods=['POST'])
@token_required
@handle_exceptions
def send_appointment_reminder_notification(current_user):
    """Send an appointment reminder notification."""
    data = request.get_json()
    
    result = send_appointment_reminder(
        user_id=data['user_id'],
        appointment_type=data['appointment_type'],
        date_time=data['date_time'],
        location=data.get('location'),
        zoom_link=data.get('zoom_link')
    )
    return jsonify(result)

@bp.route('/notifications/message', methods=['POST'])
@token_required
@handle_exceptions
def send_message_notification_endpoint(current_user):
    """Send a message notification."""
    data = request.get_json()
    
    result = send_message_notification(
        user_id=data['user_id'],
        sender_name=data['sender_name'],
        message_preview=data['message_preview'],
        conversation_id=data['conversation_id']
    )
    return jsonify(result)

@bp.route('/notifications/immigration-form', methods=['POST'])
@token_required
@handle_exceptions
def send_immigration_form_notification_endpoint(current_user):
    """Send an immigration form notification."""
    data = request.get_json()
    
    result = send_immigration_form_notification(
        user_id=data['user_id'],
        form_type=data['form_type'],
        status=data['status'],
        case_id=data.get('case_id')
    )
    return jsonify(result) 