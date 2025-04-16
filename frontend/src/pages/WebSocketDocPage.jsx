import React from 'react';
import { 
  Box, 
  Typography, 
  Paper, 
  Divider,
  Container,
  List,
  ListItem,
  ListItemText
} from '@mui/material';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { vscDarkPlus } from 'react-syntax-highlighter/dist/esm/styles/prism';

const WebSocketDocPage = () => {
  const contextExample = `
import { useWebSocket } from '../contexts/WebSocketContext';

const MyComponent = () => {
  const {
    isConnected,
    connectionError,
    connect,
    disconnect,
    sendMessage,
    on,
    off
  } = useWebSocket();

  // Use the WebSocket functionality here
  // ...
};
`;

  const connectionExample = `
// Connect to the default WebSocket server
connect();

// Or connect to a custom WebSocket server
connect('http://custom-server.com');

// Disconnect when done
disconnect();
`;

  const sendMessageExample = `
// Send a simple message
sendMessage({
  type: 'chat_message',
  data: {
    roomId: 'room-123',
    userId: 'user-456',
    message: 'Hello, world!'
  }
});

// Send a message to join a room
sendMessage({
  type: 'join_room',
  data: {
    roomId: 'room-123',
    userId: 'user-456',
    userName: 'John Doe'
  }
});
`;

  const eventListenerExample = `
// Listen for incoming messages
useEffect(() => {
  const handleMessage = (data) => {
    console.log('Message received:', data);
    // Update state or UI based on message
  };

  // Set up event listeners
  const cleanup1 = on('message_received', handleMessage);
  const cleanup2 = on('user_joined', handleUserJoined);
  
  // Clean up when component unmounts
  return () => {
    if (cleanup1) cleanup1();
    if (cleanup2) cleanup2();
  };
}, [on]);
`;

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Typography variant="h3" gutterBottom>
        WebSocket Documentation
      </Typography>
      
      <Paper elevation={2} sx={{ p: 3, mb: 4 }}>
        <Typography variant="h4" gutterBottom>
          Introduction
        </Typography>
        <Typography variant="body1" paragraph>
          This application uses WebSockets for real-time communication between clients and server.
          The WebSocket functionality is managed through a centralized context provider pattern,
          making it easy to use WebSockets in any component.
        </Typography>
        <Typography variant="body1" paragraph>
          Key features include:
        </Typography>
        <List>
          <ListItem>
            <ListItemText primary="Centralized connection management" secondary="A single WebSocket connection shared throughout the app" />
          </ListItem>
          <ListItem>
            <ListItemText primary="Connection state tracking" secondary="Easy access to connection status and errors" />
          </ListItem>
          <ListItem>
            <ListItemText primary="Event-based communication" secondary="Register listeners for specific event types" />
          </ListItem>
          <ListItem>
            <ListItemText primary="Automatic reconnection" secondary="Handles reconnection attempts when connection is lost" />
          </ListItem>
        </List>
      </Paper>

      <Paper elevation={2} sx={{ p: 3, mb: 4 }}>
        <Typography variant="h4" gutterBottom>
          Using the WebSocketContext
        </Typography>
        <Typography variant="body1" paragraph>
          Import and use the WebSocketContext in your components:
        </Typography>
        <SyntaxHighlighter language="jsx" style={vscDarkPlus}>
          {contextExample}
        </SyntaxHighlighter>
      </Paper>

      <Paper elevation={2} sx={{ p: 3, mb: 4 }}>
        <Typography variant="h4" gutterBottom>
          Managing Connections
        </Typography>
        <Typography variant="body1" paragraph>
          Connect to and disconnect from the WebSocket server:
        </Typography>
        <SyntaxHighlighter language="jsx" style={vscDarkPlus}>
          {connectionExample}
        </SyntaxHighlighter>
      </Paper>

      <Paper elevation={2} sx={{ p: 3, mb: 4 }}>
        <Typography variant="h4" gutterBottom>
          Sending Messages
        </Typography>
        <Typography variant="body1" paragraph>
          Send messages to the WebSocket server:
        </Typography>
        <SyntaxHighlighter language="jsx" style={vscDarkPlus}>
          {sendMessageExample}
        </SyntaxHighlighter>
      </Paper>

      <Paper elevation={2} sx={{ p: 3, mb: 4 }}>
        <Typography variant="h4" gutterBottom>
          Handling Events
        </Typography>
        <Typography variant="body1" paragraph>
          Listen for and respond to WebSocket events:
        </Typography>
        <SyntaxHighlighter language="jsx" style={vscDarkPlus}>
          {eventListenerExample}
        </SyntaxHighlighter>
      </Paper>

      <Paper elevation={2} sx={{ p: 3, mb: 4 }}>
        <Typography variant="h4" gutterBottom>
          Available Event Types
        </Typography>
        <Typography variant="body1" paragraph>
          Here are the common event types used in the application:
        </Typography>
        <List>
          <ListItem>
            <ListItemText 
              primary="connect" 
              secondary="Triggered when a connection is established" 
            />
          </ListItem>
          <ListItem>
            <ListItemText 
              primary="disconnect" 
              secondary="Triggered when the connection is closed" 
            />
          </ListItem>
          <ListItem>
            <ListItemText 
              primary="connect_error" 
              secondary="Triggered when there's an error establishing connection" 
            />
          </ListItem>
          <ListItem>
            <ListItemText 
              primary="message_received" 
              secondary="Triggered when a new message is received" 
            />
          </ListItem>
          <ListItem>
            <ListItemText 
              primary="user_joined" 
              secondary="Triggered when a user joins a chat room" 
            />
          </ListItem>
          <ListItem>
            <ListItemText 
              primary="user_left" 
              secondary="Triggered when a user leaves a chat room" 
            />
          </ListItem>
          <ListItem>
            <ListItemText 
              primary="chat_history" 
              secondary="Triggered when chat history is loaded" 
            />
          </ListItem>
        </List>
      </Paper>

      <Paper elevation={2} sx={{ p: 3 }}>
        <Typography variant="h4" gutterBottom>
          Testing WebSocket Functionality
        </Typography>
        <Typography variant="body1" paragraph>
          You can test WebSocket functionality using the WebSocketTestComponent located at <code>/ws-test</code> in the application.
          This component provides a UI for connecting to WebSocket servers, sending messages, and viewing responses.
        </Typography>
        <Typography variant="body1" paragraph>
          For server-side testing, you can use the <code>test_websocket_connection.py</code> script in the root directory.
        </Typography>
      </Paper>
    </Container>
  );
};

export default WebSocketDocPage; 