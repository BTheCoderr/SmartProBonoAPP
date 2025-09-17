/**
 * Real-Time Chat Component
 * Provides live chat functionality with WebSocket integration
 */

import React, { useState, useEffect, useRef } from 'react';
import {
  Box,
  Paper,
  TextField,
  Button,
  List,
  ListItem,
  ListItemText,
  Typography,
  Avatar,
  Chip,
  IconButton,
  Divider,
  CircularProgress,
  Alert
} from '@mui/material';
import SendIcon from '@mui/icons-material/Send';
import PersonIcon from '@mui/icons-material/Person';
import { useChat } from '../hooks/useWebSocket';

const RealtimeChat = ({ 
  roomId, 
  currentUser = 'Anonymous',
  showUserAvatars = true,
  maxMessages = 100,
  placeholder = 'Type your message...'
}) => {
  const [message, setMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);
  
  const {
    isConnected,
    isJoined,
    messages,
    sendMessage,
    loadHistory
  } = useChat(roomId);

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Load message history when component mounts
  useEffect(() => {
    if (roomId && isConnected) {
      loadHistory(maxMessages);
    }
  }, [roomId, isConnected, loadHistory, maxMessages]);

  const handleSendMessage = async () => {
    if (!message.trim() || !isConnected || !isJoined) return;

    setIsLoading(true);
    try {
      sendMessage(message.trim(), currentUser);
      setMessage('');
    } catch (error) {
      console.error('Error sending message:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (event) => {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      handleSendMessage();
    }
  };

  const formatTimestamp = (timestamp) => {
    const date = new Date(timestamp);
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  const getMessageAlignment = (sender) => {
    return sender === currentUser ? 'flex-end' : 'flex-start';
  };

  const getMessageColor = (sender) => {
    return sender === currentUser ? 'primary' : 'default';
  };

  return (
    <Box sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
      {/* Connection Status */}
      <Box sx={{ mb: 1 }}>
        {!isConnected && (
          <Alert severity="warning" sx={{ mb: 1 }}>
            Disconnected from chat server
          </Alert>
        )}
        {isConnected && !isJoined && roomId && (
          <Alert severity="info" sx={{ mb: 1 }}>
            Joining chat room...
          </Alert>
        )}
        {isConnected && isJoined && (
          <Chip 
            label="Connected" 
            color="success" 
            size="small" 
            sx={{ mb: 1 }}
          />
        )}
      </Box>

      {/* Messages List */}
      <Paper 
        variant="outlined" 
        sx={{ 
          flex: 1, 
          overflow: 'auto', 
          p: 1,
          mb: 1,
          minHeight: 300,
          maxHeight: 500
        }}
      >
        {messages.length === 0 ? (
          <Box sx={{ 
            display: 'flex', 
            justifyContent: 'center', 
            alignItems: 'center', 
            height: '100%',
            color: 'text.secondary'
          }}>
            <Typography variant="body2">
              {isConnected ? 'No messages yet. Start the conversation!' : 'Connecting...'}
            </Typography>
          </Box>
        ) : (
          <List sx={{ p: 0 }}>
            {messages.map((msg, index) => (
              <React.Fragment key={msg.id || index}>
                <ListItem 
                  sx={{ 
                    display: 'flex', 
                    justifyContent: getMessageAlignment(msg.sender),
                    alignItems: 'flex-start',
                    py: 0.5
                  }}
                >
                  <Box sx={{ 
                    maxWidth: '70%',
                    display: 'flex',
                    flexDirection: getMessageAlignment(msg.sender) === 'flex-end' ? 'row-reverse' : 'row',
                    alignItems: 'flex-start',
                    gap: 1
                  }}>
                    {/* Avatar */}
                    {showUserAvatars && (
                      <Avatar 
                        sx={{ 
                          width: 32, 
                          height: 32,
                          bgcolor: getMessageColor(msg.sender) === 'primary' ? 'primary.main' : 'grey.500'
                        }}
                      >
                        <PersonIcon fontSize="small" />
                      </Avatar>
                    )}
                    
                    {/* Message Content */}
                    <Box sx={{ 
                      bgcolor: getMessageColor(msg.sender) === 'primary' ? 'primary.main' : 'grey.100',
                      color: getMessageColor(msg.sender) === 'primary' ? 'primary.contrastText' : 'text.primary',
                      borderRadius: 2,
                      px: 2,
                      py: 1,
                      maxWidth: '100%'
                    }}>
                      <Typography variant="body2" sx={{ wordBreak: 'break-word' }}>
                        {msg.message}
                      </Typography>
                      <Typography 
                        variant="caption" 
                        sx={{ 
                          display: 'block', 
                          mt: 0.5,
                          opacity: 0.7,
                          fontSize: '0.7rem'
                        }}
                      >
                        {msg.sender} • {formatTimestamp(msg.timestamp)}
                      </Typography>
                    </Box>
                  </Box>
                </ListItem>
                {index < messages.length - 1 && <Divider sx={{ my: 0.5 }} />}
              </React.Fragment>
            ))}
            <div ref={messagesEndRef} />
          </List>
        )}
      </Paper>

      {/* Message Input */}
      <Box sx={{ display: 'flex', gap: 1, alignItems: 'flex-end' }}>
        <TextField
          fullWidth
          multiline
          maxRows={4}
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder={placeholder}
          disabled={!isConnected || !isJoined}
          variant="outlined"
          size="small"
        />
        <IconButton
          onClick={handleSendMessage}
          disabled={!message.trim() || !isConnected || !isJoined || isLoading}
          color="primary"
          sx={{ 
            bgcolor: 'primary.main',
            color: 'white',
            '&:hover': {
              bgcolor: 'primary.dark'
            },
            '&:disabled': {
              bgcolor: 'grey.300',
              color: 'grey.500'
            }
          }}
        >
          {isLoading ? (
            <CircularProgress size={20} color="inherit" />
          ) : (
            <SendIcon />
          )}
        </IconButton>
      </Box>

      {/* Room Info */}
      {roomId && (
        <Typography variant="caption" color="text.secondary" sx={{ mt: 1, textAlign: 'center' }}>
          Room: {roomId} • {messages.length} messages
        </Typography>
      )}
    </Box>
  );
};

export default RealtimeChat;
