# Notification System Documentation

The Smart Pro Bono application includes a comprehensive notification system to keep users informed about important events, updates, and messages. This document outlines the architecture, implementation details, and usage guidelines for the notification system.

## Architecture Overview

The notification system is built on a real-time event-driven architecture with the following key components:

1. **Backend Notification Service**: Centralized service for creating, storing, and delivering notifications.
2. **WebSocket Integration**: Real-time delivery of notifications to connected clients.
3. **Frontend Notification Context**: Context provider that manages notification state and provides methods for interaction.
4. **UI Components**: Visual components for displaying and interacting with notifications.
5. **Notification Preferences**: User-configurable settings for notification delivery methods.

## Backend Implementation

### Notification Service

The notification service (`NotificationService`) is a singleton that manages all notification-related operations:

- Creating notifications
- Storing notifications (in-memory with file backup)
- Sending notifications via WebSocket
- Retrieving user notifications
- Marking notifications as read
- Deleting notifications

```python
# Key methods in the NotificationService
create_notification(user_id, notification_data)
send_notification(user_id, notification_data, online_users)
send_bulk_notification(user_ids, notification_template, online_users)
get_user_notifications(user_id, limit=50, include_read=True)
mark_notification_read(user_id, notification_id)
mark_all_notifications_read(user_id)
delete_notification(user_id, notification_id)
delete_all_notifications(user_id)
```

### Notification Types

The backend supports various notification types, each with its own template and purpose:

- **Case Status Notifications**: Updates about case status changes
- **Document Notifications**: Information about document uploads, processing, or approvals
- **Appointment Notifications**: Reminders and updates about upcoming appointments
- **Message Notifications**: Alerts about new messages in chat rooms
- **Legal AI Notifications**: Notifications when legal AI has processed a query
- **System Notifications**: General system announcements and updates

```python
# Examples of notification creation
create_case_status_notification(user_id, case_id, case_title, old_status, new_status)
create_document_notification(user_id, document_id, document_title, event_type)
create_appointment_notification(user_id, appointment_id, attorney_name, appointment_time, event_type)
create_message_notification(user_id, sender_name, room_id, room_name, preview_text)
create_legal_response_notification(user_id, query_id, preview_text)
create_system_notification(user_id, title, message, action_url, notification_type)
```

### WebSocket Handlers

Socket.IO event handlers are implemented for notification-related operations:

- `handle_test_notification`: For testing notification delivery
- `handle_get_notifications`: Retrieve user notifications
- `handle_mark_notification_read`: Mark a notification as read
- `handle_mark_all_notifications_read`: Mark all notifications as read
- `handle_delete_notification`: Delete a notification

## Frontend Implementation

### Notification Context

The `NotificationContext` provides a central store for notifications and methods to interact with them:

```javascript
// Key features of the NotificationContext
const { 
  notifications,      // All user notifications
  unreadCount,        // Count of unread notifications
  markAsRead,         // Function to mark a notification as read
  markAllAsRead,      // Function to mark all notifications as read
  removeNotification  // Function to delete a notification
} = useNotification();
```

### WebSocket Integration

The `WebSocketContext` handles the WebSocket connection and event listeners, including notification events:

```javascript
// Setting up notification event listeners
useEffect(() => {
  if (isConnected && isAuthenticated) {
    // Handler for receiving new notifications
    const handleNewNotification = (notification) => {
      // Add notification to state
      // Update unread count
      // Show browser notification if supported
    };
    
    // Register event listener
    on('notification', handleNewNotification);
    
    // Clean up listeners when unmounting
    return () => {
      off('notification', handleNewNotification);
    };
  }
}, [isConnected, isAuthenticated, on, off]);
```

### UI Components

1. **NotificationCenter**: The main component that displays a notification bell icon with counter and a dropdown of notifications.
2. **NotificationBell**: A simple component that displays just the notification icon with a badge.
3. **NotificationPreferences**: Component for managing notification preferences.

### Browser Notifications

The system supports native browser notifications when the application is running in the background:

```javascript
// Function to show browser notification
const showBrowserNotification = (notification) => {
  if ('Notification' in window && Notification.permission === 'granted') {
    new Notification(notification.title, {
      body: notification.message,
      icon: '/logo192.png'
    });
  }
};
```

## Usage Guidelines

### Triggering Notifications from Backend Code

To trigger a notification from backend code:

```python
from services.notification_service import get_notification_service
from utils.notification_utils import create_system_notification

# Get notification service instance
notification_service = get_notification_service()

# Create notification data
notification_data = create_system_notification(
    user_id="user123",
    title="Action Required",
    message="Please complete your profile information",
    action_url="/profile"
)

# Send notification
notification_service.send_notification(user_id="user123", notification_data=notification_data)
```

### Displaying Notifications in React Components

To access and display notifications in a React component:

```jsx
import React from 'react';
import { useNotification } from '../contexts/NotificationContext';

const MyComponent = () => {
  const { notifications, unreadCount, markAsRead } = useNotification();
  
  return (
    <div>
      <h2>You have {unreadCount} unread notifications</h2>
      <ul>
        {notifications.map(notification => (
          <li key={notification.id} onClick={() => markAsRead(notification.id)}>
            {notification.title} - {notification.message}
          </li>
        ))}
      </ul>
    </div>
  );
};
```

## Testing Notifications

The application includes a dedicated notification testing page at `/notification-test` that allows:

1. Sending test notifications of different types
2. Testing browser notification permissions
3. Viewing notification delivery in real-time

## Future Enhancements

1. **Persistent Storage**: Replace in-memory storage with a database solution for scalability.
2. **Push Notifications**: Implement web push notifications for delivery when the browser is closed.
3. **Mobile Notifications**: Add mobile push notifications via Firebase Cloud Messaging.
4. **Notification Templates**: Create a template system for consistent notification formatting.
5. **Notification Analytics**: Track notification delivery, open rates, and interactions.
6. **Advanced Filtering**: Allow users to filter notifications by type, date, etc.
7. **Notification Scheduling**: Support for scheduling notifications to be sent at a specific time.
8. **Notification Batching**: Group similar notifications to reduce noise.

## Troubleshooting

### Common Issues

1. **Notifications not appearing in real-time**
   - Ensure WebSocket connection is established
   - Check if user is authenticated
   - Verify that notification preferences allow the notification type

2. **Browser notifications not working**
   - Verify that notification permissions are granted
   - Check if browser supports the Notification API
   - Ensure the application is properly requesting permissions

3. **Missing notifications**
   - Validate that notification events are correctly processed
   - Check if the user has an active WebSocket connection
   - Ensure the notification service is properly initialized

## API Reference

### Notification Object Structure

```javascript
{
  id: "unique-notification-id",
  type: "message",  // message, case, document, appointment, legal_ai, system
  title: "New Message",
  message: "You have received a new message from John Doe",
  timestamp: "2023-06-15T14:30:00Z",
  read: false,
  actionUrl: "/chat/room123",
  sender: "John Doe",
  relatedEntityId: "room123",
  relatedEntityType: "chat_room"
}
```

### Backend API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/notifications` | GET | Get user notifications |
| `/api/notifications/:id/read` | PUT | Mark notification as read |
| `/api/notifications/read-all` | PUT | Mark all notifications as read |
| `/api/notifications/:id` | DELETE | Delete a notification |
| `/api/notifications/settings` | GET | Get notification preferences |
| `/api/notifications/settings` | PUT | Update notification preferences |

### WebSocket Events

| Event | Direction | Description |
|-------|-----------|-------------|
| `notification` | Server → Client | Sent when a new notification is created |
| `get_notifications` | Client → Server | Request to get all notifications |
| `mark_notification_read` | Client → Server | Request to mark a notification as read |
| `mark_all_notifications_read` | Client → Server | Request to mark all notifications as read |
| `delete_notification` | Client → Server | Request to delete a notification |
| `test_notification` | Client → Server | Send a test notification | 