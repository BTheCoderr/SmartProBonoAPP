# Real-time Chat System Documentation

The Smart Pro Bono application includes a robust real-time chat system that enables secure communication between attorneys, clients, and administrators. This document outlines the architecture, implementation details, and usage guidelines for the chat system.

## Architecture Overview

The chat system is built on a WebSocket-based architecture with the following key components:

1. **Flask-SocketIO Backend**: Manages WebSocket connections, rooms, and message broadcasting.
2. **Frontend Socket.IO Client**: Establishes and maintains the WebSocket connection from the browser.
3. **Chat Rooms**: Virtual spaces where users can communicate in groups.
4. **Private Messaging**: One-to-one communication channels between users.
5. **User Presence System**: Real-time tracking of user online status and typing indicators.
6. **Rate Limiting**: Protection against message flooding and abuse.

## Backend Implementation

### Socket.IO Server

The Socket.IO server is integrated with Flask and handles all real-time communication:

```python
from flask import Flask
from flask_socketio import SocketIO, emit, join_room, leave_room

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")
```

### Connection Management

The server tracks user connections, manages rooms, and handles reconnection:

```python
# Dictionaries to track user connections and status
online_users = {}  # Maps user_id to connected status
typing_users = {}  # Maps room_id to a list of users currently typing
user_rooms = {}    # Maps user_id to a list of active rooms

@socketio.on('connect')
def handle_connect():
    sid = get_sid()
    user_id = session.get('user_id')
    if user_id:
        online_users[user_id] = True
        # Notify other users about this user coming online
        emit('user_online', {'user_id': user_id}, broadcast=True)
        
@socketio.on('disconnect')
def handle_disconnect():
    sid = get_sid()
    user_id = session.get('user_id')
    if user_id:
        online_users.pop(user_id, None)
        # Remove user from all typing lists
        for room_id in user_rooms.get(user_id, []):
            if room_id in typing_users and user_id in typing_users[room_id]:
                typing_users[room_id].remove(user_id)
                emit('typing_update', {'room_id': room_id, 'typing_users': typing_users[room_id]}, room=room_id)
        # Notify other users about this user going offline
        emit('user_offline', {'user_id': user_id}, broadcast=True)
```

### Room Management

Rooms allow for group conversations or dedicated channels:

```python
@socketio.on('join_room')
def handle_join_room(data):
    sid = get_sid()
    user_id = session.get('user_id')
    room_id = data.get('room_id')
    
    if not user_id or not room_id:
        return
        
    join_room(room_id)
    
    # Track that this user is in this room
    if user_id not in user_rooms:
        user_rooms[user_id] = []
    if room_id not in user_rooms[user_id]:
        user_rooms[user_id].append(room_id)
    
    # Notify room that user has joined
    emit('user_joined', {'user_id': user_id, 'username': get_username(user_id)}, room=room_id)

@socketio.on('leave_room')
def handle_leave_room(data):
    sid = get_sid()
    user_id = session.get('user_id')
    room_id = data.get('room_id')
    
    if not user_id or not room_id:
        return
        
    leave_room(room_id)
    
    # Remove room from user's list
    if user_id in user_rooms and room_id in user_rooms[user_id]:
        user_rooms[user_id].remove(room_id)
    
    # Remove user from typing list for this room
    if room_id in typing_users and user_id in typing_users[room_id]:
        typing_users[room_id].remove(user_id)
        emit('typing_update', {'room_id': room_id, 'typing_users': typing_users[room_id]}, room=room_id)
    
    # Notify room that user has left
    emit('user_left', {'user_id': user_id, 'username': get_username(user_id)}, room=room_id)
```

### Messaging

Message handling with rate limiting protection:

```python
@socketio.on('chat_message')
def handle_chat_message(data):
    sid = get_sid()
    user_id = session.get('user_id')
    room_id = data.get('room_id')
    message = data.get('message')
    
    if not user_id or not room_id or not message:
        return
        
    # Check rate limit
    if check_rate_limit(user_id):
        emit('error', {'message': 'Rate limit exceeded. Please wait before sending more messages.'}, room=sid)
        return
    
    # Create message data
    message_data = {
        'id': str(uuid.uuid4()),
        'room_id': room_id,
        'user_id': user_id,
        'username': get_username(user_id),
        'message': message,
        'timestamp': datetime.now().isoformat()
    }
    
    # Save message to database
    save_message_to_db(message_data)
    
    # Clear user from typing list
    if room_id in typing_users and user_id in typing_users[room_id]:
        typing_users[room_id].remove(user_id)
    
    # Send message to room
    emit('new_message', message_data, room=room_id)
    
    # Send notification to users in the room who are not connected
    send_message_notification(room_id, user_id, message)
```

### Typing Indicators

Real-time updates when users are typing:

```python
@socketio.on('typing')
def handle_typing(data):
    sid = get_sid()
    user_id = session.get('user_id')
    room_id = data.get('room_id')
    is_typing = data.get('is_typing', False)
    
    if not user_id or not room_id:
        return
    
    # Initialize typing users list for this room if it doesn't exist
    if room_id not in typing_users:
        typing_users[room_id] = []
    
    # Add or remove user from typing list
    if is_typing and user_id not in typing_users[room_id]:
        typing_users[room_id].append(user_id)
    elif not is_typing and user_id in typing_users[room_id]:
        typing_users[room_id].remove(user_id)
    
    # Send typing update to everyone in the room
    emit('typing_update', {
        'room_id': room_id,
        'typing_users': typing_users[room_id]
    }, room=room_id)
```

### Rate Limiting

Protection against message flooding:

```python
# Rate limiting configuration
RATE_LIMIT_MAX_MESSAGES = 20  # Maximum number of messages per minute
RATE_LIMIT_WINDOW = 60        # Time window in seconds

# Store user message timestamps
message_rate_limit = {}  # user_id -> list of timestamps

def check_rate_limit(user_id):
    """
    Check if a user has exceeded the message rate limit.
    Returns True if rate limit is exceeded, False otherwise.
    """
    current_time = time.time()
    
    # Initialize if user not in rate limit dict
    if user_id not in message_rate_limit:
        message_rate_limit[user_id] = []
    
    # Filter timestamps to only include those within the time window
    message_rate_limit[user_id] = [
        ts for ts in message_rate_limit[user_id] 
        if current_time - ts < RATE_LIMIT_WINDOW
    ]
    
    # Check if rate limit is exceeded
    if len(message_rate_limit[user_id]) >= RATE_LIMIT_MAX_MESSAGES:
        # Rate limit exceeded
        return True
    
    # Add current timestamp and return False (not exceeded)
    message_rate_limit[user_id].append(current_time)
    return False
```

## Frontend Implementation

### WebSocket Context

The `WebSocketContext` provides a centralized way to access the WebSocket connection:

```jsx
import React, { createContext, useState, useEffect, useContext, useCallback } from 'react';
import { io } from 'socket.io-client';
import { useAuth } from './AuthContext';

const WebSocketContext = createContext(null);

export const WebSocketProvider = ({ children }) => {
  const [socket, setSocket] = useState(null);
  const [isConnected, setIsConnected] = useState(false);
  const { isAuthenticated, token } = useAuth();
  
  // Connect to WebSocket when authenticated
  useEffect(() => {
    if (isAuthenticated && token) {
      const newSocket = io(process.env.REACT_APP_WS_URL, {
        auth: { token },
        transports: ['websocket'],
        reconnection: true,
        reconnectionAttempts: 5,
        reconnectionDelay: 1000,
      });
      
      newSocket.on('connect', () => {
        setIsConnected(true);
        console.log('WebSocket connected');
      });
      
      newSocket.on('disconnect', () => {
        setIsConnected(false);
        console.log('WebSocket disconnected');
      });
      
      setSocket(newSocket);
      
      return () => {
        newSocket.disconnect();
      };
    }
  }, [isAuthenticated, token]);
  
  // Emit wrapper function
  const emit = useCallback((event, data, callback) => {
    if (socket && isConnected) {
      socket.emit(event, data, callback);
    }
  }, [socket, isConnected]);
  
  // Listen wrapper function
  const on = useCallback((event, callback) => {
    if (socket) {
      socket.on(event, callback);
    }
    return () => {
      if (socket) {
        socket.off(event, callback);
      }
    };
  }, [socket]);
  
  // Remove listener wrapper function
  const off = useCallback((event, callback) => {
    if (socket) {
      socket.off(event, callback);
    }
  }, [socket]);
  
  return (
    <WebSocketContext.Provider value={{ socket, isConnected, emit, on, off }}>
      {children}
    </WebSocketContext.Provider>
  );
};

export const useWebSocket = () => useContext(WebSocketContext);
```

### ChatRoom Component

The main chat room component that handles messaging and user presence:

```jsx
import React, { useState, useEffect, useCallback, useRef } from 'react';
import { useWebSocket } from '../contexts/WebSocketContext';
import { useAuth } from '../contexts/AuthContext';
import { debounce } from 'lodash';

const ChatRoom = ({ roomId, roomName }) => {
  const { user } = useAuth();
  const { emit, on, off, isConnected } = useWebSocket();
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState('');
  const [participants, setParticipants] = useState([]);
  const [typingUsers, setTypingUsers] = useState([]);
  const [onlineUsers, setOnlineUsers] = useState({});
  const messagesEndRef = useRef(null);
  
  // Fetch messages when component mounts
  useEffect(() => {
    if (isConnected && roomId) {
      // Join the room
      emit('join_room', { room_id: roomId });
      
      // Fetch previous messages
      emit('get_messages', { room_id: roomId }, (response) => {
        if (response.success) {
          setMessages(response.messages);
        }
      });
      
      // Fetch room participants
      emit('get_room_participants', { room_id: roomId }, (response) => {
        if (response.success) {
          setParticipants(response.participants);
          // Initialize online status for all participants
          const initialOnlineStatus = {};
          response.participants.forEach(p => {
            initialOnlineStatus[p.id] = false;
          });
          setOnlineUsers(initialOnlineStatus);
        }
      });
      
      // Clean up when component unmounts
      return () => {
        emit('leave_room', { room_id: roomId });
      };
    }
  }, [isConnected, roomId, emit]);
  
  // Set up event listeners
  useEffect(() => {
    if (isConnected) {
      // Handle new messages
      const handleNewMessage = (messageData) => {
        if (messageData.room_id === roomId) {
          setMessages(prevMessages => [...prevMessages, messageData]);
        }
      };
      
      // Handle user joined
      const handleUserJoined = (userData) => {
        setParticipants(prev => {
          if (!prev.find(p => p.id === userData.user_id)) {
            return [...prev, { id: userData.user_id, username: userData.username }];
          }
          return prev;
        });
        
        setOnlineUsers(prev => ({
          ...prev,
          [userData.user_id]: true
        }));
      };
      
      // Handle user left
      const handleUserLeft = (userData) => {
        setOnlineUsers(prev => ({
          ...prev,
          [userData.user_id]: false
        }));
      };
      
      // Handle typing updates
      const handleTypingUpdate = (data) => {
        if (data.room_id === roomId) {
          setTypingUsers(data.typing_users);
        }
      };
      
      // Handle user online status
      const handleUserOnline = (data) => {
        setOnlineUsers(prev => ({
          ...prev,
          [data.user_id]: true
        }));
      };
      
      // Handle user offline status
      const handleUserOffline = (data) => {
        setOnlineUsers(prev => ({
          ...prev,
          [data.user_id]: false
        }));
      };
      
      // Register event listeners
      on('new_message', handleNewMessage);
      on('user_joined', handleUserJoined);
      on('user_left', handleUserLeft);
      on('typing_update', handleTypingUpdate);
      on('user_online', handleUserOnline);
      on('user_offline', handleUserOffline);
      
      // Clean up event listeners
      return () => {
        off('new_message', handleNewMessage);
        off('user_joined', handleUserJoined);
        off('user_left', handleUserLeft);
        off('typing_update', handleTypingUpdate);
        off('user_online', handleUserOnline);
        off('user_offline', handleUserOffline);
      };
    }
  }, [isConnected, roomId, on, off]);
  
  // Debounced typing indicator
  const debouncedTypingUpdate = useCallback(
    debounce((isTyping) => {
      emit('typing', { room_id: roomId, is_typing: isTyping });
    }, 300),
    [emit, roomId]
  );
  
  // Handle input change
  const handleInputChange = (e) => {
    setNewMessage(e.target.value);
    debouncedTypingUpdate(e.target.value.length > 0);
  };
  
  // Handle sending message
  const handleSendMessage = (e) => {
    e.preventDefault();
    if (newMessage.trim() === '') return;
    
    emit('chat_message', {
      room_id: roomId,
      message: newMessage.trim()
    });
    
    setNewMessage('');
    debouncedTypingUpdate(false);
  };
  
  // Scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);
  
  // Render typing indicators
  const renderTypingIndicator = () => {
    const typingUsernames = typingUsers
      .filter(userId => userId !== user.id)
      .map(userId => {
        const participant = participants.find(p => p.id === userId);
        return participant ? participant.username : 'Someone';
      });
    
    if (typingUsernames.length === 0) return null;
    if (typingUsernames.length === 1) return `${typingUsernames[0]} is typing...`;
    if (typingUsernames.length === 2) return `${typingUsernames[0]} and ${typingUsernames[1]} are typing...`;
    return 'Multiple people are typing...';
  };
  
  return (
    <div className="chat-room">
      <div className="chat-header">
        <h2>{roomName}</h2>
        <div className="participants">
          {participants.map(participant => (
            <div key={participant.id} className="participant">
              <span className={`status-indicator ${onlineUsers[participant.id] ? 'online' : 'offline'}`} />
              <span>{participant.username}</span>
            </div>
          ))}
        </div>
      </div>
      
      <div className="messages-container">
        {messages.map(message => (
          <div 
            key={message.id} 
            className={`message ${message.user_id === user.id ? 'sent' : 'received'}`}
          >
            <div className="message-header">
              <span className="message-username">{message.username}</span>
              <span className="message-time">
                {new Date(message.timestamp).toLocaleTimeString()}
              </span>
            </div>
            <div className="message-content">{message.message}</div>
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>
      
      <div className="typing-indicator">{renderTypingIndicator()}</div>
      
      <form onSubmit={handleSendMessage} className="message-form">
        <input
          type="text"
          value={newMessage}
          onChange={handleInputChange}
          placeholder="Type a message..."
          disabled={!isConnected}
        />
        <button type="submit" disabled={!isConnected || newMessage.trim() === ''}>
          Send
        </button>
      </form>
    </div>
  );
};

export default ChatRoom;
```

## Usage Guidelines

### Creating a New Chat Room

```javascript
import { useWebSocket } from '../contexts/WebSocketContext';

const CreateChatRoom = () => {
  const { emit } = useWebSocket();
  const [roomName, setRoomName] = useState('');
  
  const handleCreateRoom = () => {
    emit('create_room', { name: roomName }, (response) => {
      if (response.success) {
        // Navigate to the new room
        navigate(`/chat/${response.room_id}`);
      }
    });
  };
  
  // ...render form...
};
```

### Private Messaging

```javascript
const sendPrivateMessage = (recipientId, message) => {
  emit('private_message', {
    recipient_id: recipientId,
    message: message
  });
};
```

### Fetching User Conversations

```javascript
useEffect(() => {
  emit('get_user_conversations', {}, (response) => {
    if (response.success) {
      setConversations(response.conversations);
    }
  });
}, [emit]);
```

## Testing the Chat System

The chat system can be tested using the built-in chat page or through socket.io's debugging tools:

1. Open multiple browser windows/tabs to simulate different users
2. Use the browser's developer tools to monitor WebSocket traffic
3. Check the Flask-SocketIO server logs for connection and event information

## Future Enhancements

1. **End-to-End Encryption**: Implement secure messaging using client-side encryption
2. **Message Reactions**: Allow users to react to messages with emojis
3. **File Sharing**: Enable secure document sharing within chats
4. **Message Threading**: Support threaded replies to messages
5. **Read Receipts**: Show when messages have been read by recipients
6. **Message Editing**: Allow users to edit or delete their messages
7. **Chat History Search**: Full-text search across chat history
8. **Voice/Video Chat**: Integrate WebRTC for audio/video communication

## Troubleshooting

### Common Issues

1. **WebSocket Connection Issues**
   - Check network connectivity
   - Verify that the WebSocket server is running
   - Ensure that the authentication token is valid

2. **Messages Not Being Delivered**
   - Confirm that users are in the same room
   - Check for rate limiting blocks
   - Verify that the WebSocket connection is established

3. **User Presence Not Updating**
   - Ensure proper room joining/leaving events
   - Check for errors in the presence tracking system

## API Reference

### Server-Side Events

| Event | Description |
|-------|-------------|
| `connect` | Client connects to the WebSocket server |
| `disconnect` | Client disconnects from the server |
| `join_room` | Client joins a chat room |
| `leave_room` | Client leaves a chat room |
| `chat_message` | Client sends a message to a room |
| `typing` | Client indicates typing status |
| `get_messages` | Client requests chat history |
| `get_room_participants` | Client requests room participant list |
| `private_message` | Client sends a private message |

### Client-Side Events

| Event | Description |
|-------|-------------|
| `new_message` | Server sends a new message |
| `user_joined` | User joins a chat room |
| `user_left` | User leaves a chat room |
| `typing_update` | Users typing status changes |
| `user_online` | User comes online |
| `user_offline` | User goes offline |
| `error` | Server sends an error message | 