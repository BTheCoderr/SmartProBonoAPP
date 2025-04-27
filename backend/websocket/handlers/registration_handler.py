"""
Registration handler for WebSocket clients
"""
from flask import request
from flask_socketio import join_room
from ..core import socketio
from ..services.connection_service import register_connection
from ..services.notification_service import get_user_notifications
from ...utils.logging_setup import get_logger

# Set up logging
logger = get_logger('websocket.handlers.registration')

def register_handler(data):
    """
    Handle client registration for receiving notifications
    
    Args:
        data: Registration data containing user_id
        
    Returns:
        Response with status and message
    """
    try:
        if 'user_id' not in data:
            logger.warning("Registration attempt without user_id")
            return {'status': 'error', 'message': 'user_id is required'}
        
        user_id = str(data['user_id'])
        session_id = request.sid  # type: ignore  # Flask-SocketIO adds this attribute
        
        if not user_id or not session_id:
            logger.warning(f"Invalid registration data: user_id={user_id}, session_id={session_id}")
            return {'status': 'error', 'message': 'Invalid user_id or session'}
        
        # Add user to a room with their user_id
        join_room(user_id)
        
        # Register the session
        success = register_connection(user_id, session_id)
        
        if success:
            logger.info(f"User {user_id} registered from session {session_id}")
            
            # Send any unread notifications
            try:
                unread_notifications = get_user_notifications(user_id, include_read=False)
                if unread_notifications:
                    logger.info(f"Sending {len(unread_notifications)} unread notifications to user {user_id}")
                    for notification in unread_notifications:
                        socketio.emit('notification', notification, to=session_id)
            except Exception as e:
                logger.error(f"Error sending unread notifications: {str(e)}")
            
            return {
                'status': 'success', 
                'message': f'User {user_id} registered for notifications',
                'session_id': session_id
            }
        else:
            logger.error(f"Failed to register user {user_id}")
            return {'status': 'error', 'message': 'Failed to register user'}
            
    except Exception as e:
        logger.error(f"Error in register handler: {str(e)}")
        return {'status': 'error', 'message': str(e)} 