# WebSocket Integration Guide

This guide explains how to use the real-time notification system in SmartProBono, powered by Socket.IO.

## Overview

The WebSocket implementation enables real-time communication between the server and clients, allowing for instant notifications, status updates, and messaging. Key features include:

- Real-time notifications for users
- Persistent storage of notifications
- Automatic reconnection handling
- Support for offline delivery (notifications are stored and delivered when the user reconnects)
- Event-based architecture for extensibility

## Architecture

The WebSocket functionality is divided into two main parts:

1. **Backend**: A modular WebSocket implementation with Socket.IO
2. **Frontend**: A React service for connecting to the WebSocket server

### Backend Structure

```
backend/websocket/
├── __init__.py             # Main exports
├── core.py                 # Core WebSocket functionality
├── handlers/               # Event handlers
│   ├── notification_handler.py
│   └── registration_handler.py
├── services/               # Service layer
│   ├── connection_service.py
│   └── notification_service.py
└── utils/                  # Utility functions
    ├── backoff.py
    ├── metrics.py
    └── persistence.py
```

### Frontend Structure

```
frontend/src/
├── components/
│   ├── WebSocketClient.js  # WebSocket connection component
│   └── Notifications.js    # Notification display component
├── context/
│   └── AuthContext.js      # Handles socket initialization with user authentication
└── services/
    └── socket.js           # Socket.IO client service
```

## Backend Implementation

### Initialization

The WebSocket server is initialized in `backend/app.py`:

```python
from websocket import socketio, init_socketio, register_notification_handlers

# In create_app function
socketio_app = init_socketio(app, allowed_origins)
register_notification_handlers()

# At the end of the file
if __name__ == '__main__':
    app = create_app()
    socketio.run(app, host='0.0.0.0', port=port, debug=True)
```

### Sending Notifications

You can send notifications to users from anywhere in the backend code:

```python
from websocket import send_notification

# Send a notification to a specific user
send_notification(
    user_id='user123',
    notification_data={
        'message': 'Your form has been submitted successfully',
        'type': 'success',
        'category': 'immigration'
    }
)
```

For more complex notifications, you can include additional data:

```python
send_notification(
    user_id='user123',
    notification_data={
        'message': 'Your case status has changed to In Progress',
        'type': 'info',
        'case_id': 'case456',
        'status': 'in-progress',
        'category': 'immigration',
        'action_required': False
    }
)
```

### API Endpoints

The system includes API endpoints for sending notifications:

```
POST /api/immigration/notifications/case-status-update
POST /api/immigration/notifications/form-submission
POST /api/immigration/notifications/document-required
```

Example usage:

```python
# Send notification when a form is submitted
@immigration.route('/intake-form', methods=['POST'])
@handle_exceptions
def submit_intake_form():
    # ... process form data ...
    
    # Send notification to the user
    notification_service.send_user_notification(
        user_id=user_id,
        message='Your immigration form has been submitted successfully.',
        notification_type='success',
        additional_data={
            'formId': form_id,
            'category': 'immigration'
        }
    )
    
    # ... return response ...
```

## Frontend Implementation

### Socket Service

The `socket.js` service manages the Socket.IO connection:

```javascript
// frontend/src/services/socket.js
import { io } from 'socket.io-client';
import config from '../config';

export const initializeSocket = (userId) => {
  // Create socket connection
  socket = io(config.wsUrl, {
    transports: ['websocket'],
    reconnection: true
  });
  
  // Register the user
  socket.emit('register', { user_id: userId });
  
  // Set up event handlers
  socket.on('notification', (data) => {
    // Handle incoming notifications
  });
};
```

### WebSocket Client Component

The `WebSocketClient.js` component initializes the socket connection when a user is authenticated:

```jsx
// frontend/src/components/WebSocketClient.js
import React, { useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { initializeSocket, disconnectSocket } from '../services/socket';

const WebSocketClient = () => {
  const { currentUser, isAuthenticated } = useAuth();

  useEffect(() => {
    if (isAuthenticated && currentUser?.id) {
      initializeSocket(currentUser.id);
      
      return () => {
        disconnectSocket();
      };
    }
  }, [currentUser, isAuthenticated]);

  return null;
};
```

### Notification Display

The `Notifications.js` component displays notifications to the user:

```jsx
// frontend/src/components/Notifications.js
import React, { useState } from 'react';
import { Badge, IconButton, Menu, MenuItem } from '@mui/material';
import NotificationsIcon from '@mui/icons-material/Notifications';
import { useAuth } from '../context/AuthContext';

const Notifications = () => {
  const { notifications } = useAuth();
  const [anchorEl, setAnchorEl] = useState(null);
  
  // Component implementation...
};
```

## Authentication Integration

The WebSocket connection is initialized when a user logs in, via the `AuthContext`:

```jsx
// frontend/src/context/AuthContext.js
useEffect(() => {
  if (currentUser && currentUser.id) {
    initializeSocket(currentUser.id)
      .then(() => {
        addSocketEventHandler('notification', handleNotification);
      });
    
    return () => {
      removeSocketEventHandler('notification', handleNotification);
    };
  }
}, [currentUser, handleNotification]);
```

## Testing the Integration

You can test the notification system in several ways:

1. **Using the Test Button**: The Immigration Dashboard includes a "Send Test Notification" button.

2. **Using the API Endpoints**: You can send notifications via the API:

```bash
curl -X POST http://localhost:5003/api/immigration/notifications/form-submission \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "form_id": "test-123",
    "form_type": "immigration_intake",
    "user_id": "user123"
  }'
```

3. **Using the Python Test Suite**: Run the WebSocket tests:

```bash
python -m unittest backend/tests/test_websocket.py
```

## Troubleshooting

If you encounter issues with the WebSocket implementation:

1. **Check Browser Console**: Look for connection errors or warnings.

2. **Check Server Logs**: The backend logs WebSocket events with detailed information.

3. **Verify CORS Settings**: Ensure that the WebSocket server allows connections from your frontend origin.

4. **Test Connectivity**: Use the Socket.IO debugging tools to verify the connection.

## Security Considerations

- WebSocket connections are authenticated using the same JWT tokens as the REST API.
- Users can only receive notifications intended for them.
- Sensitive data should not be included in notifications.
- Rate limiting is implemented to prevent abuse.

## Performance Optimization

- Notifications are delivered through rooms to minimize unnecessary broadcasting.
- Batch updates are used when marking multiple notifications as read.
- Exponential backoff is used for reconnection attempts.
- Notifications are persisted to ensure delivery even if a user is offline.

## Extending the System

To add new notification types:

1. Create a new API endpoint or service function.
2. Use the `send_notification` function with appropriate parameters.
3. Update the frontend to handle the new notification type if needed.

For example, to add a new "payment received" notification:

```python
send_notification(
    user_id=user_id,
    notification_data={
        'message': 'Payment received for your application',
        'type': 'success',
        'category': 'payment',
        'amount': payment_amount,
        'payment_id': payment_id
    }
)
``` 