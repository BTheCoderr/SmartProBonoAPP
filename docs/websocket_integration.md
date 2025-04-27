# WebSocket Integration Guide

This document provides a comprehensive guide to the WebSocket implementation in the SmartProBono application. It explains the architecture, usage patterns, and examples for leveraging real-time notifications and messaging capabilities.

## Overview

The WebSocket module enables real-time communication between the server and clients, facilitating instant notifications, status updates, and message delivery. This is particularly useful for features like form submission confirmations, case status updates, and alerts about required documents.

## Architecture

The WebSocket implementation follows a modular design pattern with clear separation of concerns:

1. **backend/websocket/core.py**
   - Core initialization and management of the Socket.IO server
   - Event handler registration
   - Connection/disconnection handling

2. **backend/websocket/services/**
   - Connection service: Manages user sessions and connections
   - Notification service: Handles sending notifications and messages

3. **backend/websocket/handlers/**
   - Registration handler: Handles user registration for notifications
   - Notification handler: Handles notification operations like marking as read

4. **backend/websocket/utils/**
   - Metrics: Tracks connection statistics and performance
   - Persistence: Stores notifications in a database for reliability
   - Backoff: Implements retry strategies with exponential/linear backoff

## Key Features

- **User Registration**: Associates user IDs with WebSocket sessions
- **Notification Persistence**: Notifications are stored in a database and delivered even if the user was offline
- **Delivery Confirmation**: Ensures notifications are delivered with retry logic
- **Read Status Tracking**: Tracks which notifications have been read by users
- **Broadcast Capabilities**: Send notifications to all users or specific groups
- **Direct Messaging**: Send messages to specific client sessions
- **Reconnection Logic**: Automatic reconnection with exponential backoff
- **Metrics and Monitoring**: Track connection statistics and performance

## Usage Examples

### Backend: Sending Notifications

```python
from backend.websocket import send_notification

# Send a basic notification
send_notification(user_id, {
    'message': 'Your immigration form has been submitted successfully',
    'type': 'success'
})

# Send a notification with additional data
send_notification(user_id, {
    'message': 'Your case status has been updated',
    'type': 'info',
    'case_id': '12345',
    'status': 'in_review',
    'priority': 'high',
    'category': 'immigration'
})
```

### Frontend: Receiving Notifications

```javascript
import { initializeSocket, addSocketEventHandler } from '../services/socket';

// Initialize socket and register user
const initSocket = async (userId) => {
  try {
    await initializeSocket(userId);
    
    // Listen for notifications
    addSocketEventHandler('notification', handleNotification);
  } catch (error) {
    console.error('Failed to initialize socket:', error);
  }
};

// Handle incoming notifications
const handleNotification = (notification) => {
  // Display notification to user
  console.log('New notification:', notification);
  
  // Add to notification store
  addNotificationToStore(notification);
  
  // Show toast or other UI element
  showToast(notification.message, notification.type);
};
```

## API Routes

The WebSocket integration provides several API routes for notification management:

### Immigration Notifications

- `POST /api/immigration/notifications/case-status-update`
  - Updates a case status and sends a notification to the user
  - Requires: `case_id`, `status`, `message`

- `POST /api/immigration/notifications/form-submission`
  - Notifies a user that their form was submitted successfully
  - Optionally notifies administrators of new submissions
  - Requires: `form_id`, `form_type`

- `POST /api/immigration/notifications/document-required`
  - Notifies a user that additional documents are required
  - Requires: `user_id`, `case_id`, `document_type`, `message`

## WebSocket Events

The WebSocket server handles these events:

- `connect`: Initial connection
- `disconnect`: Client disconnection
- `register`: Register a user for notifications
- `mark_read`: Mark one or more notifications as read
- `get_notifications`: Get a user's notifications

## Testing

The WebSocket functionality can be tested using:

1. The provided test suite in `backend/tests/test_websocket.py`
2. The test API endpoints in `backend/routes/test.py`
3. A WebSocket client like Socket.IO Client or Postman

### Running WebSocket Tests

```bash
# Run the WebSocket test suite
python -m unittest backend/tests/test_websocket.py

# Test specific endpoints
curl -X POST http://localhost:5003/api/test/notification/user123 \
  -H "Content-Type: application/json" \
  -d '{"message": "Test notification", "type": "info"}'
```

## Error Handling and Reconnection

The WebSocket implementation includes robust error handling and automatic reconnection:

- Client reconnection with exponential backoff
- Failed message retry with configurable attempts
- Session cleanup on disconnection
- Connection monitoring and statistics

## Integration with Frontend Components

The frontend includes components for handling WebSocket connections:

- `WebSocketClient`: Manages WebSocket connection in the app
- `NotificationCenter`: Displays and manages notifications
- `NotificationBadge`: Shows unread notification count
- `NotificationList`: Displays a list of notifications with read/unread status

## Performance Considerations

To ensure optimal performance:

1. Notifications are stored in a SQLite database with indexes for efficient querying
2. Connection state is maintained in memory with thread-safe access
3. Long polling fallback when WebSockets are not available
4. Batch operations for marking multiple notifications as read
5. Automatic cleanup of old notifications

## Security

Security measures in the WebSocket implementation:

1. Authentication required for sending notifications
2. Users can only access their own notifications
3. Admin-only routes for certain notification types
4. Rate limiting to prevent abuse
5. Validation of notification data

## Troubleshooting

Common issues and solutions:

1. **Connection Issues**: Ensure CORS is properly configured and the WebSocket server is running
2. **Missing Notifications**: Check that the user is properly registered and the notification was sent
3. **Performance Problems**: Monitor connection metrics and adjust batch sizes or cleanup frequency
4. **Database Errors**: Check database connectivity and schema 