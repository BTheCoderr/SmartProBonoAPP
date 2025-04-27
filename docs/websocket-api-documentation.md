# WebSocket API Documentation

This document provides a comprehensive reference for the WebSocket API used in the SmartProBono application. The WebSocket API enables real-time communication between the server and clients for notifications, status updates, and messaging.

## Table of Contents

1. [Overview](#overview)
2. [Connection](#connection)
3. [Authentication](#authentication)
4. [Events](#events)
5. [Client to Server Events](#client-to-server-events)
6. [Server to Client Events](#server-to-client-events)
7. [Notification Types](#notification-types)
8. [Error Handling](#error-handling)
9. [Usage Examples](#usage-examples)
10. [Testing](#testing)

## Overview

The WebSocket API is built on [Socket.IO](https://socket.io/) and provides the following functionality:

- Real-time notifications for system events
- User-specific notifications for case updates, form submissions, etc.
- Persistence of notifications for offline delivery
- Connection tracking and analytics
- Direct messaging between users

## Connection

### WebSocket URL

```
ws://localhost:5003
```

In production:

```
wss://api.smartprobono.org
```

### Connection Options

```javascript
const socket = io(WS_URL, {
  transports: ['websocket'],
  reconnection: true,
  reconnectionDelay: 1000,
  reconnectionDelayMax: 5000,
  reconnectionAttempts: 5,
});
```

## Authentication

Authentication with the WebSocket server happens after establishing a connection by emitting a `register` event with the user's ID. The user ID should be obtained from your authentication system after the user logs in.

```javascript
// After user login and establishing socket connection
socket.emit('register', { user_id: '12345' }, (response) => {
  if (response.status === 'success') {
    console.log('Successfully registered with WebSocket server');
  } else {
    console.error('Failed to register:', response.message);
  }
});
```

## Events

### Client to Server Events

| Event       | Description                         | Payload                                  | Response                                    |
|-------------|-------------------------------------|------------------------------------------|---------------------------------------------|
| `register`  | Register user for notifications     | `{ user_id: string }`                   | `{ status: string, message: string }`       |
| `mark_read` | Mark notifications as read          | `{ notification_id: string \| notification_ids: string[] }` | `{ status: string, message: string }` |
| `get_notifications` | Get user's notifications    | `{ limit: number, unread_only: boolean }` | `{ status: string, message: string, notifications: Notification[] }` |

### Server to Client Events

| Event            | Description                       | Payload                                 |
|------------------|-----------------------------------|----------------------------------------|
| `notification`   | Notification for the user         | [Notification Object](#notification-object) |
| `direct_message` | Direct message to specific client | [Message Object](#message-object)       |
| `connect`        | Socket connection established     | None                                    |
| `disconnect`     | Socket disconnected               | Reason string                           |
| `connect_error`  | Connection error                  | Error object                            |

### Notification Object

```typescript
{
  id: string;              // Unique identifier for the notification
  title?: string;          // Optional title
  message: string;         // Notification message
  type: string;            // 'info', 'success', 'warning', 'error'
  category?: string;       // Optional category, e.g., 'immigration', 'documents'
  timestamp: string;       // ISO date string
  read: boolean;           // Whether notification has been read
  data?: any;              // Optional additional data
}
```

### Message Object

```typescript
{
  id: string;              // Unique identifier for the message
  message: string;         // Message content
  timestamp: string;       // ISO date string
  sender_id?: string;      // Optional sender ID
  data?: any;              // Optional additional data
}
```

## Notification Types

The WebSocket API supports different types of notifications:

| Type      | Description                                 |
|-----------|---------------------------------------------|
| `info`    | Informational notifications                 |
| `success` | Success notifications                       |
| `warning` | Warning notifications                       |
| `error`   | Error notifications                         |

## Error Handling

### Connection Errors

Socket.IO will automatically attempt to reconnect when the connection is lost. You can listen for connection errors and disconnect events to handle them appropriately:

```javascript
socket.on('connect_error', (error) => {
  console.error('Connection error:', error);
  // Show offline indicator
});

socket.on('disconnect', (reason) => {
  console.warn('Disconnected:', reason);
  // Show reconnecting indicator
});

socket.on('connect', () => {
  console.log('Connected');
  // Hide offline indicators
});
```

### Event Errors

Events that expect a response (like `register`, `mark_read`, etc.) return an object with a `status` field that can be either `'success'` or `'error'`. In case of an error, a `message` field provides details about what went wrong.

```javascript
socket.emit('register', { user_id: '12345' }, (response) => {
  if (response.status === 'error') {
    console.error('Registration failed:', response.message);
    // Handle the error
  }
});
```

## Usage Examples

### Registering a User

```javascript
// After successful login
function registerWithSocketServer(userId) {
  return new Promise((resolve, reject) => {
    socket.emit('register', { user_id: userId }, (response) => {
      if (response && response.status === 'success') {
        resolve(response);
      } else {
        reject(new Error(response?.message || 'Registration failed'));
      }
    });
  });
}

// Usage
registerWithSocketServer(currentUser.id)
  .then(response => console.log('Registered:', response))
  .catch(error => console.error('Failed to register:', error));
```

### Listening for Notifications

```javascript
// Set up notification handler
socket.on('notification', (notification) => {
  console.log('Received notification:', notification);
  
  // Add to notification list
  addNotificationToList(notification);
  
  // Show toast/alert if appropriate
  if (!notification.read) {
    showNotificationToast(notification);
  }
});
```

### Marking Notifications as Read

```javascript
function markNotificationAsRead(notificationId) {
  return new Promise((resolve, reject) => {
    socket.emit('mark_read', { notification_id: notificationId }, (response) => {
      if (response && response.status === 'success') {
        resolve(response);
      } else {
        reject(new Error(response?.message || 'Failed to mark as read'));
      }
    });
  });
}

// Usage
markNotificationAsRead('notif_123')
  .then(() => console.log('Marked as read'))
  .catch(error => console.error('Failed to mark as read:', error));
```

### Getting User Notifications

```javascript
function getUserNotifications(limit = 20, unreadOnly = false) {
  return new Promise((resolve, reject) => {
    socket.emit('get_notifications', { limit, unread_only: unreadOnly }, (response) => {
      if (response && response.status === 'success') {
        resolve(response.notifications);
      } else {
        reject(new Error(response?.message || 'Failed to get notifications'));
      }
    });
  });
}

// Usage
getUserNotifications(10, true)  // Get 10 unread notifications
  .then(notifications => displayNotifications(notifications))
  .catch(error => console.error('Failed to get notifications:', error));
```

## Testing

You can test the WebSocket API using the provided test endpoints:

### Send Test Notification

```
POST /api/test/notification/:userId
Content-Type: application/json

{
  "message": "Test notification message",
  "type": "info"
}
```

### Send Test Direct Message

```
POST /api/test/direct-message/:sessionId
Content-Type: application/json

{
  "message": "Test direct message"
}
```

### Get Connected Users

```
GET /api/test/connected-users
```

### Get WebSocket Stats

```
GET /api/test/websocket-stats
```

## Advanced Usage

### Handling Reconnection

For robust handling of reconnection scenarios:

```javascript
let reconnectAttempts = 0;
const MAX_RECONNECT_ATTEMPTS = 5;

socket.on('connect', () => {
  console.log('Connected to WebSocket server');
  reconnectAttempts = 0;
  
  // Re-register user after reconnection if we have user ID
  if (currentUser?.id) {
    registerWithSocketServer(currentUser.id)
      .then(() => console.log('Re-registered after reconnection'))
      .catch(error => console.error('Failed to re-register:', error));
  }
});

socket.on('disconnect', (reason) => {
  console.log(`Disconnected: ${reason}`);
  
  // If the server initiated the disconnect, don't reconnect automatically
  if (reason === 'io server disconnect') {
    console.log('Server initiated disconnect, not attempting to reconnect');
  }
});

socket.on('connect_error', (error) => {
  console.error('Connection error:', error);
  reconnectAttempts++;
  
  if (reconnectAttempts >= MAX_RECONNECT_ATTEMPTS) {
    console.error('Max reconnect attempts reached, stopping reconnection');
    socket.disconnect();
  }
});
```

### Offline Mode Detection

```javascript
// Check if the socket is connected
function isConnected() {
  return socket && socket.connected;
}

// Queue notifications to be marked as read when connection is restored
const pendingReadOperations = [];

function markAsReadWhenOnline(notificationId) {
  if (isConnected()) {
    return markNotificationAsRead(notificationId);
  } else {
    // Queue for later
    pendingReadOperations.push(notificationId);
    return Promise.resolve({ status: 'queued', message: 'Will be processed when online' });
  }
}

// Process queued operations when connected
socket.on('connect', () => {
  if (pendingReadOperations.length > 0) {
    console.log(`Processing ${pendingReadOperations.length} queued read operations`);
    
    socket.emit('mark_read', { notification_ids: pendingReadOperations }, (response) => {
      if (response && response.status === 'success') {
        console.log('Processed queued operations successfully');
        pendingReadOperations.length = 0; // Clear the queue
      }
    });
  }
});
```

## Security Considerations

- All WebSocket communication should be over secure WebSockets (wss://) in production
- User authentication should happen before subscribing to notifications
- Validate all incoming data on the server side
- Avoid sending sensitive information via WebSockets
- Use rate limiting to prevent abuse

This documentation is subject to updates as the WebSocket API evolves. Check for the latest version in the repository. 