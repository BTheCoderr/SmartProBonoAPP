# Notifications System Implementation

This document provides a detailed technical overview of the real-time notification system implemented in SmartProBono.

## Architecture Overview

The notification system uses a WebSocket-based architecture with the following components:

1. **Backend Services**:
   - Notification Service: Core service for generating and managing notifications
   - Connection Service: Manages WebSocket connections and user sessions
   - Application Notification Services: Domain-specific notification generators

2. **Frontend Components**:
   - WebSocket connection manager
   - Notification listener and state management
   - UI components for displaying notifications

3. **Transport Layer**:
   - Socket.IO for WebSocket communication
   - Redis for pub/sub messaging between server instances

```
┌─────────────┐     ┌────────────────┐     ┌───────────────┐
│  Frontend   │◄────┤   WebSockets   │◄────┤ Notification  │
│ Components  │     │  (Socket.IO)   │     │   Services    │
└─────────────┘     └────────────────┘     └───────────────┘
                            ▲                      ▲
                            │                      │
                            ▼                      │
                    ┌────────────────┐             │
                    │     Redis      │◄────────────┘
                    │    Pub/Sub     │
                    └────────────────┘
```

## Backend Implementation

### Connection Management (`connection_service.py`)

The connection service tracks active WebSocket connections and manages user sessions. Key functions:

```python
def register_connection(sid, user_id, metadata=None)
def unregister_connection(sid)
def get_user_sessions(user_id)
def get_connection_stats()
```

User sessions are stored in an in-memory dictionary with Redis backup for persistence across server instances.

### Notification Service (`notification_service.py`)

The notification service generates and delivers notifications to users. Core functions:

```python
def send_notification(user_id, title, message, notification_type='info', category=None, data=None, persist=True)
def send_broadcast_notification(title, message, notification_type='info', category=None, data=None, exclude_users=None, persist=True)
def mark_notification_read(notification_id, user_id)
def get_user_notifications(user_id, limit=50, skip=0, include_read=False)
```

Notifications are persisted in MongoDB and tracked for delivery statistics.

### Application Notifications (`application_notifications.py`)

Domain-specific notification generators for different application features:

```python
def send_immigration_form_notification(user_id, form_id, status, form_type=None)
def send_case_status_update(user_id, case_id, status, case_type)
def send_document_request(user_id, document_type, deadline=None)
def send_appointment_reminder(user_id, appointment_id, appointment_type, date_time)
def send_message_notification(user_id, sender_id, sender_name, message_preview)
```

### WebSocket Core (`core.py`)

Initializes the WebSocket server and registers event handlers:

```python
def init_websocket(app)
def register_event_handlers()
```

Event handlers for connection, disconnection, and client-to-server events are registered here.

## API Routes (`notifications.py`)

RESTful endpoints for notification management:

- `GET /api/notifications`: Retrieve user notifications
- `PUT /api/notifications/:id/read`: Mark notification as read
- `DELETE /api/notifications`: Clear all notifications
- `POST /api/notifications/form`: Send form notification
- `POST /api/notifications/case`: Send case update
- `POST /api/notifications/document`: Send document request
- `POST /api/notifications/appointment`: Send appointment reminder
- `POST /api/notifications/message`: Send message notification

## Frontend Implementation

### WebSocket Service (`socket.js`)

Manages the WebSocket connection and provides event listeners:

```javascript
// Initialize connection
const socket = io(WEBSOCKET_URL, {
  transports: ['websocket'],
  autoConnect: false,
  reconnection: true
});

// Register user after connection
export const registerUser = (token) => {
  socket.emit('register', { token });
};

// Listen for notifications
export const onNotification = (callback) => {
  socket.on('notification', callback);
};
```

### Notification Context (`NotificationContext.js`)

React context for managing notification state:

```javascript
const NotificationContext = createContext();

export const NotificationProvider = ({ children }) => {
  const [notifications, setNotifications] = useState([]);
  const [unreadCount, setUnreadCount] = useState(0);
  
  // Methods for handling notifications
  const addNotification = (notification) => {...}
  const markAsRead = (notificationId) => {...}
  const clearAllNotifications = () => {...}
  
  return (
    <NotificationContext.Provider 
      value={{ 
        notifications, 
        unreadCount,
        addNotification,
        markAsRead,
        clearAllNotifications
      }}
    >
      {children}
    </NotificationContext.Provider>
  );
};
```

### UI Components

- `NotificationsList.js`: Displays a list of notifications
- `NotificationBadge.js`: Shows unread notification count
- `NotificationSnackbar.js`: Displays toast notifications
- `NotificationDrawer.js`: Expandable drawer for viewing all notifications

## Notification Types and Categories

### Types

- `info`: General information
- `success`: Successful actions
- `warning`: Important alerts that need attention
- `error`: Critical errors or failures

### Categories

- `system`: System-level notifications
- `case`: Updates about legal cases
- `document`: Document-related notifications
- `appointment`: Appointment reminders
- `message`: Communication notifications

## Security Considerations

1. **Authentication**: All WebSocket connections require valid JWT authentication
2. **Authorization**: Notifications are only delivered to authorized users
3. **Rate Limiting**: Prevention of notification flooding
4. **Data Validation**: Strict validation of notification content

## Testing

The notification system can be tested using:

1. **Admin Dashboard**: Send test notifications to users
2. **WebSocket Testing Tools**: Monitor connections and events
3. **Automated Tests**: Unit and integration tests for notification services

## Best Practices

1. Keep notifications concise and relevant
2. Use appropriate notification types based on urgency
3. Implement proper error handling for failed deliveries
4. Monitor delivery statistics and optimize accordingly
5. Consider user time zones for scheduled notifications 