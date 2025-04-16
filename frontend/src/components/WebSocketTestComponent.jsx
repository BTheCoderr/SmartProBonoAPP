import React, { useState, useEffect, useRef } from 'react';
import PropTypes from 'prop-types';
import {
  Box, Typography, TextField, Button, Paper, Grid, Alert, List, ListItem, 
  ListItemText, Divider, CircularProgress, Switch, FormControlLabel,
  Chip, IconButton, Card, CardContent, Accordion, AccordionSummary, 
  AccordionDetails
} from '@mui/material';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import SendIcon from '@mui/icons-material/Send';
import RefreshIcon from '@mui/icons-material/Refresh';
import CloseIcon from '@mui/icons-material/Close';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import ErrorIcon from '@mui/icons-material/Error';
import { useWebSocket } from '../contexts/WebSocketContext';
import { useAuth } from '../contexts/AuthContext';

const WebSocketTestComponent = ({ url, autoConnect = true }) => {
  const [serverUrl, setServerUrl] = useState(url || '');
  const [message, setMessage] = useState('');
  const [chatMessage, setChatMessage] = useState('');
  const [chatUser, setChatUser] = useState('WebSocketTester');
  const [receivedMessages, setReceivedMessages] = useState([]);
  const [showError, setShowError] = useState(false);
  const messagesEndRef = useRef(null);
  
  const { 
    isConnected, 
    isConnecting,
    connectionError, 
    connect, 
    disconnect,
    sendMessage,
    on,
    off,
    autoConnect: isAutoConnectEnabled,
    toggleAutoConnect,
    reconnect
  } = useWebSocket();
  
  const { isAuthenticated, user } = useAuth();

  // Scroll to bottom when new messages are received
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [receivedMessages]);

  // Set up event listeners for incoming messages
  useEffect(() => {
    const handleMessage = (data) => {
      addReceivedMessage('message_response', data);
    };

    const handleConnectionResponse = (data) => {
      addReceivedMessage('connection_response', data);
    };

    const handleChatUpdate = (data) => {
      addReceivedMessage('chat_update', data);
    };

    const handleConnectionError = (data) => {
      addReceivedMessage('connection_error', data);
      setShowError(true);
    };

    // Register event listeners
    const cleanupFns = [
      on('message_response', handleMessage),
      on('connection_response', handleConnectionResponse),
      on('chat_update', handleChatUpdate),
      on('connect_error', handleConnectionError)
    ];

    // Clean up event listeners on unmount
    return () => {
      cleanupFns.forEach(fn => fn && fn());
    };
  }, [on]);

  const addReceivedMessage = (type, data) => {
    const timestamp = new Date().toISOString();
    setReceivedMessages(prev => [
      ...prev,
      { type, data, timestamp }
    ]);
  };

  const handleConnect = () => {
    // Use custom URL if provided, otherwise default
    const success = connect(serverUrl || undefined);
    if (!success) {
      setShowError(true);
    }
  };

  const handleDisconnect = () => {
    disconnect();
  };

  const handleSendMessage = () => {
    if (!message.trim()) return;
    
    const success = sendMessage({
      type: 'message',
      data: message
    });
    
    if (success) {
      addReceivedMessage('sent', message);
      setMessage('');
    }
  };

  const handleSendChatMessage = () => {
    if (!chatMessage.trim() || !chatUser.trim()) return;
    
    const success = sendMessage({
      type: 'chat_message',
      data: {
        message: chatMessage,
        user: chatUser,
        timestamp: new Date().toISOString()
      }
    });
    
    if (success) {
      addReceivedMessage('sent_chat', {
        message: chatMessage,
        user: chatUser,
        timestamp: new Date().toISOString()
      });
      setChatMessage('');
    }
  };

  const handleCloseError = () => {
    setShowError(false);
  };

  const clearMessages = () => {
    setReceivedMessages([]);
  };

  const formatTimestamp = (timestamp) => {
    const date = new Date(timestamp);
    return date.toLocaleTimeString();
  };

  return (
    <Paper elevation={3} sx={{ p: 3, maxWidth: 800, mx: 'auto', my: 4 }}>
      <Typography variant="h5" component="h1" gutterBottom>
        WebSocket Test Console
      </Typography>
      
      {/* Connection Status */}
      <Box sx={{ mb: 3 }}>
        <Grid container spacing={2} alignItems="center">
          <Grid item>
            <Chip
              icon={isConnected ? <CheckCircleIcon /> : <ErrorIcon />}
              label={isConnected ? 'Connected' : 'Disconnected'}
              color={isConnected ? 'success' : 'error'}
              variant="outlined"
            />
          </Grid>
          {isAuthenticated && (
            <Grid item>
              <Chip
                label={`Authenticated as ${user?.email || 'User'}`}
                color="primary"
                variant="outlined"
              />
            </Grid>
          )}
          <Grid item>
            <FormControlLabel
              control={
                <Switch
                  checked={isAutoConnectEnabled}
                  onChange={toggleAutoConnect}
                  name="autoConnect"
                  color="primary"
                />
              }
              label="Auto Connect"
            />
          </Grid>
        </Grid>

        {showError && connectionError && (
          <Alert 
            severity="error" 
            sx={{ mt: 2 }}
            action={
              <IconButton size="small" onClick={handleCloseError}>
                <CloseIcon fontSize="small" />
              </IconButton>
            }
          >
            {connectionError}
          </Alert>
        )}
      </Box>

      {/* Connection Controls */}
      <Box sx={{ mb: 3 }}>
        <Grid container spacing={2} alignItems="flex-start">
          <Grid item xs={12} sm={7}>
            <TextField
              fullWidth
              label="WebSocket Server URL"
              variant="outlined"
              value={serverUrl}
              onChange={(e) => setServerUrl(e.target.value)}
              placeholder="ws://localhost:5002"
              disabled={isConnected}
              helperText="Leave empty to use default server URL"
            />
          </Grid>
          <Grid item xs={12} sm={5}>
            <Box sx={{ display: 'flex', gap: 1 }}>
              <Button
                variant="contained"
                color={isConnected ? 'error' : 'primary'}
                onClick={isConnected ? handleDisconnect : handleConnect}
                disabled={isConnecting}
                sx={{ flex: 1 }}
                startIcon={isConnecting ? <CircularProgress size={20} /> : null}
              >
                {isConnecting ? 'Connecting...' : isConnected ? 'Disconnect' : 'Connect'}
              </Button>
              {isConnected && (
                <IconButton onClick={reconnect} color="primary" title="Reconnect">
                  <RefreshIcon />
                </IconButton>
              )}
            </Box>
          </Grid>
        </Grid>
      </Box>

      {/* Send Simple Message */}
      <Accordion defaultExpanded>
        <AccordionSummary expandIcon={<ExpandMoreIcon />}>
          <Typography variant="subtitle1">Send Simple Message</Typography>
        </AccordionSummary>
        <AccordionDetails>
          <Grid container spacing={2} alignItems="flex-start">
            <Grid item xs={12} sm={9}>
              <TextField
                fullWidth
                label="Message"
                variant="outlined"
                value={message}
                onChange={(e) => setMessage(e.target.value)}
                disabled={!isConnected}
                multiline
                rows={2}
              />
            </Grid>
            <Grid item xs={12} sm={3}>
              <Button
                variant="outlined"
                onClick={handleSendMessage}
                disabled={!isConnected || !message.trim()}
                endIcon={<SendIcon />}
                sx={{ height: '56px' }}
              >
                Send
              </Button>
            </Grid>
          </Grid>
        </AccordionDetails>
      </Accordion>

      {/* Send Chat Message */}
      <Accordion sx={{ mt: 2 }}>
        <AccordionSummary expandIcon={<ExpandMoreIcon />}>
          <Typography variant="subtitle1">Send Chat Message</Typography>
        </AccordionSummary>
        <AccordionDetails>
          <Grid container spacing={2}>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="Username"
                variant="outlined"
                value={chatUser}
                onChange={(e) => setChatUser(e.target.value)}
                disabled={!isConnected}
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Chat Message"
                variant="outlined"
                value={chatMessage}
                onChange={(e) => setChatMessage(e.target.value)}
                disabled={!isConnected}
                multiline
                rows={2}
              />
            </Grid>
            <Grid item xs={12}>
              <Button
                variant="outlined"
                onClick={handleSendChatMessage}
                disabled={!isConnected || !chatMessage.trim() || !chatUser.trim()}
                endIcon={<SendIcon />}
              >
                Send Chat Message
              </Button>
            </Grid>
          </Grid>
        </AccordionDetails>
      </Accordion>

      {/* Messages Log */}
      <Card variant="outlined" sx={{ mt: 3 }}>
        <CardContent>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
            <Typography variant="h6">Message Log</Typography>
            <Button
              variant="text"
              size="small"
              onClick={clearMessages}
              disabled={receivedMessages.length === 0}
            >
              Clear
            </Button>
          </Box>
          
          <Box 
            sx={{
              maxHeight: 300,
              overflowY: 'auto',
              bgcolor: 'grey.50',
              borderRadius: 1,
              p: 1
            }}
          >
            {receivedMessages.length === 0 ? (
              <Typography variant="body2" sx={{ py: 2, textAlign: 'center', color: 'text.secondary' }}>
                No messages yet. Connect to the server and send a message.
              </Typography>
            ) : (
              <List dense>
                {receivedMessages.map((msg, index) => (
                  <React.Fragment key={index}>
                    <ListItem alignItems="flex-start">
                      <ListItemText
                        primary={
                          <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                            <Typography variant="subtitle2" component="span" color="primary">
                              {msg.type}
                            </Typography>
                            <Typography variant="caption" component="span" color="text.secondary">
                              {formatTimestamp(msg.timestamp)}
                            </Typography>
                          </Box>
                        }
                        secondary={
                          <Box sx={{ mt: 1 }}>
                            <Typography 
                              variant="body2" 
                              component="pre"
                              sx={{ 
                                whiteSpace: 'pre-wrap',
                                wordBreak: 'break-word',
                                bgcolor: 'grey.100',
                                p: 1,
                                borderRadius: 1,
                                fontSize: '0.8rem'
                              }}
                            >
                              {typeof msg.data === 'object' 
                                ? JSON.stringify(msg.data, null, 2) 
                                : msg.data}
                            </Typography>
                          </Box>
                        }
                      />
                    </ListItem>
                    {index < receivedMessages.length - 1 && <Divider />}
                  </React.Fragment>
                ))}
                <div ref={messagesEndRef} />
              </List>
            )}
          </Box>
        </CardContent>
      </Card>
    </Paper>
  );
};

WebSocketTestComponent.propTypes = {
  url: PropTypes.string,
  autoConnect: PropTypes.bool
};

export default WebSocketTestComponent; 