# WebSocket Implementation Guide

This document provides an overview of the WebSocket implementation in the SmartProBono application, including architecture, usage patterns, and troubleshooting tips.

## Architecture

The WebSocket functionality in this application follows a provider pattern with these key components:

1. **Backend Socket.IO Server**: Implemented in the Flask application using Flask-SocketIO.
2. **WebSocketContext**: React context that provides a centralized API for WebSocket functionality.
3. **socketService**: Service module that handles the low-level Socket.IO client interactions.
4. **Component Integration**: Components like ChatRoom and WebSocketTestComponent that utilize the WebSocket context.

### Data Flow

```
┌───────────────┐     ┌───────────────┐     ┌───────────────┐     ┌───────────────┐
│    React      │     │  WebSocket    │     │   Socket      │     │   Flask       │
│  Components   │◄───►│   Context     │◄───►│   Service     │◄───►│  Socket.IO    │
└───────────────┘     └───────────────┘     └───────────────┘     └───────────────┘
```

## Setup Instructions

### Backend Setup

1. Ensure Flask-SocketIO is installed:
   ```
   pip install flask-socketio
   ```

2. The Flask app.py already includes Socket.IO setup:
   ```python
   socketio = SocketIO(
       app, 
       cors_allowed_origins="*", 
       logger=True, 
       engineio_logger=True,
       async_mode='threading',
       ping_timeout=60,
       ping_interval=25
   )
   ```

3. Start the backend server:
   ```
   cd backend
   python app.py
   ```

### Frontend Setup

1. Ensure Socket.IO client is installed:
   ```
   npm install socket.io-client
   ```

2. The WebSocketContext is already set up in the app. To use it in a component:
   ```jsx
   import { useWebSocket } from '../contexts/WebSocketContext';
   
   function MyComponent() {
     const { isConnected, connect, sendMessage } = useWebSocket();
     // Use WebSocket functionality
   }
   ```

## Event Types

The following event types are used in the WebSocket communication:

| Event Type | Direction | Description |
|------------|-----------|-------------|
| `connect` | Client ← Server | When connection is established |
| `disconnect` | Client ← Server | When connection is closed |
| `message` | Client → Server | General message from client |
| `message_response` | Client ← Server | Response to a general message |
| `chat_message` | Client → Server | Send a chat message |
| `chat_update` | Client ← Server | Receive a chat update/message |
| `join_room` | Client → Server | Request to join a chat room |
| `leave_room` | Client → Server | Request to leave a chat room |
| `user_joined` | Client ← Server | Notification of user joining |
| `user_left` | Client ← Server | Notification of user leaving |
| `message_received` | Client ← Server | A new message is received in a room |
| `chat_history` | Client ← Server | History of chat messages |
| `participants_list` | Client ← Server | List of participants in a room |

## Message Format

Messages sent with `sendMessage` should follow this format:

```javascript
{
  type: 'event_type', // e.g., 'chat_message', 'join_room'
  data: {
    // Event-specific payload
    roomId: 'room-123',
    userId: 'user-456',
    message: 'Hello, world!'
  }
}
```

## Testing

### Using the Test Component

Navigate to `/ws-test` in the application to access the WebSocket test component. This provides a UI for:
- Connecting/disconnecting from the WebSocket server
- Sending messages
- Viewing received messages

### Using the Python Test Script

The `test_websocket_connection.py` script in the root directory can be used to test the Socket.IO server:

```bash
python test_websocket_connection.py [server_url]
```

If no server URL is provided, it defaults to `http://localhost:5002`.

### Using the HTML Test Page

The `websocket_test.html` file in the root directory can be opened in a browser for testing.

## Troubleshooting

### Common Issues

1. **Connection Failures**
   - Ensure the backend server is running
   - Check CORS settings in both frontend and backend
   - Verify the WebSocket URL is correct
   - Check browser console for errors

2. **Message Not Received**
   - Ensure the message format is correct
   - Verify the event type is registered on both client and server
   - Check server logs for any processing errors

3. **Disconnect Issues**
   - Check network connectivity
   - Increase ping timeout and interval if needed
   - Verify the server isn't overloaded

## Future Improvements

1. **Authentication**: Add JWT authentication for WebSocket connections
2. **Reconnection Strategy**: Implement exponential backoff for reconnection attempts
3. **Presence Indicators**: Add user online/offline status indicators
4. **Typing Indicators**: Show when users are typing in chat rooms
5. **Message Delivery Status**: Add seen/delivered indicators for messages
6. **Rate Limiting**: Implement rate limiting to prevent abuse

## Resources

- [Socket.IO Documentation](https://socket.io/docs/v4/)
- [Flask-SocketIO Documentation](https://flask-socketio.readthedocs.io/)
- [WebSocket API (MDN)](https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API) 