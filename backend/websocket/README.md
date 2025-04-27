# WebSocket Module

This module provides a comprehensive WebSocket implementation for real-time communication in the SmartProBono application. It enables features such as real-time notifications, case status updates, and direct messaging.

## Directory Structure

```
websocket/
├── __init__.py             # Main exports and package initialization
├── core.py                 # Core WebSocket functionality
├── handlers/               # Event handlers for WebSocket events
│   ├── __init__.py         # Handler exports
│   ├── registration_handler.py   # User registration handlers
│   └── notification_handler.py   # Notification operation handlers
├── services/               # Service layer for WebSocket functionality
│   ├── __init__.py         # Service exports
│   ├── connection_service.py     # User connection management
│   └── notification_service.py   # Notification delivery
└── utils/                  # Utility functions
    ├── __init__.py         # Utility exports
    ├── backoff.py          # Retry strategies with backoff
    ├── metrics.py          # Connection and performance metrics
    └── persistence.py      # Notification persistence
```

## Key Components

### Core (`core.py`)

The core module initializes and configures the SocketIO server, manages event handler registration, and handles basic connection/disconnection logic.

```python
from websocket import socketio, init_socketio

# Initialize WebSocket with Flask app
socketio_app = init_socketio(app, allowed_origins)
```

### Connection Service (`services/connection_service.py`)

Manages user connections and sessions, with thread-safe operations for tracking connected users.

```python
from websocket.services.connection_service import register_user_session, get_user_sessions

# Register a user session
register_user_session(user_id, session_id)

# Get all sessions for a user
sessions = get_user_sessions(user_id)
```

### Notification Service (`services/notification_service.py`)

Handles sending notifications and messages to users and specific client sessions.

```python
from websocket import send_notification, send_direct_message, send_broadcast_notification

# Send notification to a specific user
send_notification(user_id, {
    'message': 'Your case status has been updated',
    'type': 'info'
})

# Send direct message to a specific client session
send_direct_message(session_id, {
    'message': 'Server is restarting in 5 minutes'
})

# Broadcast to all connected users
send_broadcast_notification({
    'message': 'System maintenance scheduled for tomorrow',
    'type': 'warning'
})
```

### Event Handlers (`handlers/`)

Handle WebSocket events like user registration and notification operations.

```python
# Registration handler (called when 'register' event is received)
def register_handler(data):
    # Handle user registration
    pass

# Mark read handler (called when 'mark_read' event is received)
def mark_read_handler(data):
    # Mark notifications as read
    pass
```

### Persistence (`utils/persistence.py`)

Stores notifications in a database for offline delivery and history.

```python
from websocket.utils.persistence import save_notification, get_notifications_for_user

# Save a notification
save_notification(user_id, notification_data)

# Get notifications for a user
notifications = get_notifications_for_user(user_id, unread_only=True)
```

### Metrics (`utils/metrics.py`)

Tracks connection statistics and performance metrics.

```python
from websocket.utils.metrics import get_connection_metrics

# Get metrics about connections
metrics = get_connection_metrics()
```

## Usage

### Initialization

The WebSocket module is initialized in the Flask application's `create_app()` function:

```python
from websocket import socketio, init_socketio, register_notification_handlers

def create_app():
    # ... app setup ...
    
    # Initialize SocketIO
    socketio_app = init_socketio(app, allowed_origins)
    
    # Register notification handlers
    register_notification_handlers()
    
    # ... other app setup ...
    
    return app
```

### Sending Notifications

Notifications can be sent from any part of the application:

```python
from websocket import send_notification

def process_immigration_form(form_data, user_id):
    # ... process form ...
    
    # Send confirmation notification
    send_notification(user_id, {
        'message': 'Your immigration form has been submitted successfully',
        'type': 'success',
        'form_id': form_id,
        'category': 'immigration'
    })
```

### Frontend Integration

The frontend connects to the WebSocket server and registers the user:

```javascript
import { initializeSocket, addSocketEventHandler } from '../services/socket';

// Initialize socket connection
await initializeSocket(userId);

// Listen for notifications
addSocketEventHandler('notification', (notification) => {
  console.log('Received notification:', notification);
  showNotification(notification);
});
```

## Testing

The WebSocket functionality can be tested using the test suite in `backend/tests/test_websocket.py`:

```bash
python -m unittest backend/tests/test_websocket.py
```

You can also use the test API endpoints in `backend/routes/test.py` to send test notifications:

```bash
curl -X POST http://localhost:5003/api/test/notification/user123 \
  -H "Content-Type: application/json" \
  -d '{"message": "Test notification", "type": "info"}'
```

## Security Considerations

1. All WebSocket communications are subject to the same CORS restrictions as the REST API
2. User authentication is required for accessing user-specific notifications
3. Admin-only routes are protected with proper authorization
4. Input validation is performed on all notification data
5. Rate limiting helps prevent abuse

## Performance

The WebSocket implementation includes several optimizations:

1. Thread-safe connection tracking with minimal locking
2. Efficient notification delivery to specific users or sessions
3. Database persistence with indexes for quick retrieval
4. Automatic cleanup of old notifications
5. Connection metrics for monitoring and troubleshooting 