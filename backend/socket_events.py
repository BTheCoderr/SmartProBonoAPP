import datetime
import uuid
import random
import time
import logging
from flask import request
from flask_socketio import emit, join_room, leave_room, rooms
from utils.notification_utils import create_message_notification, create_legal_response_notification

logger = logging.getLogger(__name__)

# Track online users and their rooms
online_users = {}  # sid -> { user_id, rooms }
typing_users = {}  # room_id -> {user_id: timestamp}

# Message rate limiting
message_rate_limit = {}  # user_id -> list of timestamps
RATE_LIMIT_MAX_MESSAGES = 20  # max messages per minute
RATE_LIMIT_WINDOW = 60  # seconds

# Helper function to extract user ID from the session
def extract_user_id(sid):
    """
    Retrieve the user ID from session or authentication
    Returns an anonymous ID if not found
    """
    user_data = online_users.get(sid, {})
    return user_data.get('user_id', f"anonymous-{sid[:8]}")

# Helper function to get the Socket.IO session ID safely
def get_sid():
    """
    Safely get the Socket.IO session ID from the request context.
    Returns a random UUID if SID is not available (for testing).
    """
    try:
        return getattr(request, 'sid', str(uuid.uuid4()))
    except Exception:
        return str(uuid.uuid4())  # Fallback for testing

# Check if user has exceeded message rate limit
def check_rate_limit(user_id):
    """Check if a user has exceeded the message rate limit"""
    if user_id not in message_rate_limit:
        message_rate_limit[user_id] = []
        return True
        
    # Get current time
    now = datetime.datetime.now().timestamp()
    
    # Filter timestamps to keep only those within the window
    message_rate_limit[user_id] = [
        ts for ts in message_rate_limit[user_id] 
        if now - ts < RATE_LIMIT_WINDOW
    ]
    
    # Check if user has exceeded limit
    if len(message_rate_limit[user_id]) >= RATE_LIMIT_MAX_MESSAGES:
        return False
        
    # Add current timestamp
    message_rate_limit[user_id].append(now)
    return True

# Mock function to process legal queries
def process_legal_query(query):
    """
    Process a legal query and return a mock response.
    In a production environment, this would call an AI service.
    """
    # List of mock legal responses
    responses = [
        "Based on my analysis, your situation appears to be covered under Section 213 of the Civil Code. I would recommend consulting with an attorney who specializes in this area.",
        "The terms of the contract you described might be unenforceable due to the lack of consideration. This is a basic principle of contract law.",
        "For landlord-tenant disputes of this nature, mediation is often a cost-effective first step before pursuing litigation.",
        "The statute of limitations for this type of claim is typically 3 years from the date of the incident, but may vary by jurisdiction.",
        "In employment law cases similar to yours, documentation of all incidents and communications is crucial to building a strong case."
    ]
    
    # Add some random delay to simulate processing time (1-3 seconds)
    time.sleep(random.uniform(1, 3))
    
    return random.choice(responses)

def register_socket_events(socketio, app):
    """Register all Socket.IO event handlers"""
    from services.notification_service import get_notification_service
    notification_service = get_notification_service()
    
    @socketio.on('join_room')
    def handle_join_room(data):
        """Handle a user joining a chat room"""
        try:
            room_id = data.get('room_id')
            user_name = data.get('user_name', 'Anonymous')
            
            if not room_id:
                emit('error', {'message': 'Room ID is required'})
                return
                
            # Add user to room
            sid = get_sid()
            user_id = online_users[sid]['user_id'] if sid in online_users else None
            
            if not user_id:
                emit('error', {'message': 'Not authenticated'})
                return
                
            join_room(room_id)
            
            # Update user's room list
            if sid in online_users:
                if 'rooms' not in online_users[sid]:
                    online_users[sid]['rooms'] = []
                if room_id not in online_users[sid]['rooms']:
                    online_users[sid]['rooms'].append(room_id)
            
            # Notify room that user has joined
            emit('user_joined', {
                'user_id': user_id,
                'user_name': user_name,
                'room': room_id,
                'timestamp': datetime.datetime.utcnow().isoformat()
            }, to=room_id)
            
            logger.info(f"User {user_id} ({user_name}) joined room {room_id}")
            
            # Send success response to the user
            emit('room_joined', {
                'room_id': room_id,
                'status': 'success'
            })
            
        except Exception as e:
            logger.error(f"Error joining room: {str(e)}")
            emit('error', {'message': f'Error joining room: {str(e)}'})

    @socketio.on('leave_room')
    def handle_leave_room(data):
        """Handle a user leaving a chat room"""
        try:
            room_id = data.get('room_id')
            
            if not room_id:
                emit('error', {'message': 'Room ID is required'})
                return
                
            # Remove user from room
            sid = get_sid()
            user_id = online_users[sid]['user_id'] if sid in online_users else None
            
            if not user_id:
                emit('error', {'message': 'Not authenticated'})
                return
                
            leave_room(room_id)
            
            # Update user's room list
            if sid in online_users and 'rooms' in online_users[sid] and room_id in online_users[sid]['rooms']:
                online_users[sid]['rooms'].remove(room_id)
            
            # Notify room that user has left
            emit('user_left', {
                'user_id': user_id,
                'room': room_id,
                'timestamp': datetime.datetime.utcnow().isoformat()
            }, to=room_id)
            
            logger.info(f"User {user_id} left room {room_id}")
            
        except Exception as e:
            logger.error(f"Error leaving room: {str(e)}")
            emit('error', {'message': f'Error leaving room: {str(e)}'})

    @socketio.on('typing')
    def handle_typing(data):
        """Handle typing indicators"""
        try:
            room_id = data.get('room_id')
            is_typing = data.get('is_typing', True)
            
            if not room_id:
                return
                
            # Get user info
            sid = get_sid()
            if sid not in online_users or 'user_id' not in online_users[sid]:
                return
            
            user_id = online_users[sid]['user_id']
            
            if not user_id or 'rooms' not in online_users[sid] or room_id not in online_users[sid]['rooms']:
                return
                
            # Track typing status
            if room_id not in typing_users:
                typing_users[room_id] = set()
                
            if is_typing:
                typing_users[room_id].add(user_id)
            elif user_id in typing_users[room_id]:
                typing_users[room_id].remove(user_id)
                
            # Notify room of typing status
            emit('typing_update', {
                'room_id': room_id,
                'user_id': user_id,
                'is_typing': is_typing
            }, to=room_id)
            
        except Exception as e:
            logger.error(f"Error handling typing indicator: {str(e)}")

    @socketio.on('get_online_users')
    def handle_get_online_users():
        """Return list of online users"""
        try:
            # Extract unique user IDs from online_users
            unique_users = set()
            for user_data in online_users.values():
                if 'user_id' in user_data:
                    unique_users.add(user_data['user_id'])
                
            emit('online_users', {'users': list(unique_users)})
            
        except Exception as e:
            logger.error(f"Error getting online users: {str(e)}")
            emit('error', {'message': f'Error getting online users: {str(e)}'})

    @socketio.on('message')
    def handle_message(message):
        sid = get_sid()
        logging.info(f"Received message: {message}")
        try:
            user_id = extract_user_id(sid)
            # Check rate limit
            if not check_rate_limit(user_id):
                logging.warning(f"User {user_id} exceeded message rate limit")
                emit('error', {'message': 'Rate limit exceeded. Please try again later.'})
                return
            
            emit('message_response', {
                'status': 'received',
                'message': message,
                'timestamp': datetime.datetime.now().isoformat()
            })
        except Exception as e:
            logging.error(f"Error processing message: {str(e)}")
            emit('error', {'message': f'Error processing message: {str(e)}'})

    @socketio.on('legal_query')
    def handle_legal_query(data):
        sid = get_sid()
        logging.info(f"Received legal query: {data}")
        try:
            user_id = extract_user_id(sid)
            # Check rate limit
            if not check_rate_limit(user_id):
                logging.warning(f"User {user_id} exceeded message rate limit")
                emit('error', {'message': 'Rate limit exceeded. Please try again later.'})
                return
            
            # Process the legal query
            query = data.get('query', '')
            if not query:
                emit('error', {'message': 'Empty query not allowed'})
                return
                
            # Generate a unique ID for this query
            query_id = str(uuid.uuid4())
                
            # Here you would integrate with your actual AI service
            # For now, we'll mock a response
            response = process_legal_query(query)
            
            # Emit the AI response back to the client
            emit('ai_response', {
                'content': response,
                'timestamp': datetime.datetime.now().isoformat(),
                'files': [],  # Add files if needed
                'query_id': query_id
            })
            
            # Send notification after a short delay to simulate processing time
            # This would typically happen asynchronously when the AI response is ready
            notification_data = create_legal_response_notification(
                user_id,
                query_id,
                response[:50]  # Use first 50 chars as preview
            )
            if notification_service:
                notification_service.send_notification(user_id, notification_data, online_users)
            
        except Exception as e:
            logging.error(f"Error processing legal query: {str(e)}")
            emit('error', {'message': f'Error processing legal query: {str(e)}'})

    @socketio.on('chat_message')
    def handle_chat_message(data):
        logger.info(f"Received chat message: {data}")
        
        # Get user ID
        sid = get_sid()
        user_id = online_users.get(sid, {}).get('user_id')
        
        # Apply rate limiting if authenticated
        if user_id:
            if not check_rate_limit(user_id):
                logger.warning(f"Rate limit exceeded for user {user_id}")
                emit('error', {'message': 'Rate limit exceeded. Please wait before sending more messages.'})
                return
        
        # Send message to room
        room_id = data.get('room_id')
        message = data.get('message', '')
        sender_name = data.get('sender_name', 'Anonymous')
        
        if room_id:
            # Broadcast the message to all in the room
            emit('message_received', data, to=room_id)
            logger.info(f"Message sent to room {room_id}")
            
            # Send notification to all users in the room except sender
            for sid, user_data in online_users.items():
                recipient_id = user_data.get('user_id')
                
                # Skip the sender
                if recipient_id and recipient_id != user_id and 'rooms' in user_data and room_id in user_data.get('rooms', []):
                    # Create and send notification
                    notification_data = create_message_notification(
                        recipient_id,
                        sender_name,
                        room_id,
                        data.get('room_name', 'Chat Room'),
                        message
                    )
                    if notification_service:
                        notification_service.send_notification(recipient_id, notification_data, online_users)
        else:
            # Broadcast to all clients if no room specified
            emit('chat_update', data, broadcast=True)

    @socketio.on_error()
    def error_handler(e):
        logger.error(f"Socket.IO error: {str(e)}") 