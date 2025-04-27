# Socket.IO Testing Guide

This guide provides instructions for testing the Socket.IO real-time notification system in the SmartProBono application.

## Prerequisites

- Both the backend and frontend applications should be running
- You should have a user account to test with

## Testing Flow

### 1. Testing Connection Establishment

1. Log in to the application
2. Open the browser developer console (F12 or right-click > Inspect)
3. Look for the following log messages:
   - "Initializing socket for user: [user_id]"
   - "Socket connected!"
   - "User [user_id] registered with socket server"

If you see these messages, the Socket.IO connection has been established successfully.

### 2. Testing User Registration

1. While logged in, navigate to the browser console
2. Verify that the user ID has been registered with the socket server by checking the last log message
3. You can also check the connected users by making a GET request to the test endpoint:

```
GET /api/test/connected-users
```

This endpoint will return a list of all connected users and their session IDs.

### 3. Testing Notifications

#### Send a Test Notification

1. Use Postman or curl to send a notification to your user:

```
POST /api/test/notification/[your_user_id]
Content-Type: application/json

{
  "message": "This is a test notification",
  "type": "info"
}
```

2. The notification bell in the UI should update with a badge indicating a new notification
3. Click the notification bell to open the notifications dropdown
4. You should see the notification message you just sent

#### Notification Types

You can test different notification types by changing the "type" field in your request:

- "info" - Blue information icon
- "success" - Green checkmark icon
- "warning" - Yellow warning icon
- "error" - Red error icon

### 4. Testing Direct Messages

Direct messages are sent to a specific client session rather than a user ID. To test:

1. Get your session ID from the console logs or the `/api/test/connected-users` endpoint
2. Send a direct message using:

```
POST /api/test/direct-message/[your_session_id]
Content-Type: application/json

{
  "message": "This is a direct message to your session"
}
```

3. Check the console logs for the received message

## Testing Using the Notification Service

The notification service can be used from any part of the application. Here's how to test it:

### Through the Immigration Route

The immigration route has been set up to send a notification when a form is submitted. To test:

1. Navigate to the Immigration page
2. Fill out and submit an immigration form
3. After submission, you should receive a notification about the form submission

### Through the Test Route

You can test the notification service directly through the test route:

```
GET /api/test/notification/[your_user_id]
```

This will send a random notification to your user ID.

## Troubleshooting

### No Connection

If the Socket.IO connection is not being established:

1. Check if WebSockets are enabled in the config (`enableWebSocket: true` in `config.js`)
2. Verify that the `wsUrl` in the config is correct
3. Check for CORS issues in the browser console
4. Ensure the eventlet server is running correctly

### Notifications Not Showing

If notifications are not showing up:

1. Check the browser console for any errors
2. Verify that the user ID in the notification request matches your logged-in user
3. Check that the socket is properly connected
4. Inspect the network tab to see if the Socket.IO connection is active

## Creating Custom Notifications

You can send custom notifications from any part of the application by importing the `notification_service`:

```python
from services.notification_service import get_notification_service

notification_service = get_notification_service()
notification_service.send_user_notification(
    user_id="123",
    message="Your document has been processed",
    notification_type="success",
    additional_data={"document_id": "doc_123"}
)
```

For broadcasting to all users:

```python
notification_service.send_broadcast(
    message="System maintenance scheduled for tonight",
    notification_type="warning"
)
``` 