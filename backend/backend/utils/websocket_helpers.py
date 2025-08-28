"""
Utility functions for WebSocket operations
"""
from datetime import datetime
import uuid
from flask import current_app
from websocket_service import send_notification, send_broadcast_notification

def send_user_event(user_id, event_type, data, event_name='notification'):
    """
    Send an event to a specific user
    
    Args:
        user_id (str): The ID of the user to send the event to
        event_type (str): The type of event (info, success, warning, error)
        data (dict): The data to include in the event
        event_name (str, optional): The name of the event to emit
        
    Returns:
        bool: Whether the event was sent successfully
    """
    try:
        # Create event data
        event_data = {
            'type': event_type,
            'timestamp': datetime.utcnow().isoformat(),
            'id': str(uuid.uuid4())
        }
        
        # Add the data
        if isinstance(data, dict):
            event_data.update(data)
        else:
            event_data['message'] = str(data)
            
        # Send notification
        return send_notification(user_id, event_data)
    except Exception as e:
        current_app.logger.error(f"Error sending user event: {str(e)}")
        return False

def send_entity_update(user_id, entity_type, entity_id, action, data=None):
    """
    Send an entity update notification to a user
    
    Args:
        user_id (str): The ID of the user to notify
        entity_type (str): The type of entity (case, form, document, etc.)
        entity_id (str): The ID of the entity
        action (str): The action performed (created, updated, deleted)
        data (dict, optional): Additional data to include
        
    Returns:
        bool: Whether the notification was sent successfully
    """
    notification_data = {
        'entity': {
            'type': entity_type,
            'id': entity_id,
            'action': action
        },
        'message': f"{entity_type.capitalize()} {action}"
    }
    
    if data:
        notification_data['data'] = data
        
    return send_user_event(user_id, 'info', notification_data)

def broadcast_system_notification(message, notification_type='info', additional_data=None):
    """
    Broadcast a system notification to all connected users
    
    Args:
        message (str): The notification message
        notification_type (str): The type of notification
        additional_data (dict, optional): Additional data to include
        
    Returns:
        bool: Whether the broadcast was sent successfully
    """
    try:
        # Create notification data
        notification_data = {
            'message': message,
            'type': notification_type,
            'timestamp': datetime.utcnow().isoformat(),
            'id': str(uuid.uuid4()),
            'broadcast': True,
            'system': True
        }
        
        # Add additional data
        if additional_data and isinstance(additional_data, dict):
            notification_data.update(additional_data)
            
        # Send broadcast
        return send_broadcast_notification(notification_data)
    except Exception as e:
        current_app.logger.error(f"Error broadcasting system notification: {str(e)}")
        return False 