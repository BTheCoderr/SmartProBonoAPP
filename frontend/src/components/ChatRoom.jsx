import React, { useState, useRef, useEffect } from 'react';
import {
  Box,
  TextField,
  Button,
  List,
  ListItem,
  Typography,
  Paper,
  Divider,
  CircularProgress,
  IconButton,
  Badge,
  Alert,
  Snackbar,
  Avatar,
  Chip
} from '@mui/material';
import SendIcon from '@mui/icons-material/Send';
import PersonIcon from '@mui/icons-material/Person';
import { useWebSocket } from '../utils/webSocketIntegration';
import { useTranslation } from 'react-i18next';
import PropTypes from 'prop-types';
import { useAuth } from '../contexts/AuthContext';
import debounce from 'lodash/debounce';
/**
 * ChatRoom component that handles real-time messaging using WebSockets
 * 
 * @param {Object} props
 * @param {string} props.roomId - The ID of the chat room
 * @param {string} props.userId - The ID of the current user
 * @param {string} props.userName - The name of the current user
 * @param {Function} props.onLeave - Callback when user leaves the chat
 */
const ChatRoom = ({ roomId, userId, userName, onLeave }) => {
  const { t } = useTranslation();
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [participants, setParticipants] = useState([]);
  const [snackbar, setSnackbar] = useState({ open: false, message: '', severity: 'info' });
  const [typingUsers, setTypingUsers] = useState([]);
  const [onlineUsers, setOnlineUsers] = useState([]);
  const messagesEndRef = useRef(null);
  const { isAuthenticated, user } = useAuth();
  
  // Get WebSocket context
  const {
    isConnected,
    connectionError,
    connect,
    disconnect,
    sendMessage,
    on,
    off
  } = useWebSocket();
  
  // Create a derived state for connection status display
  const [isConnecting, setIsConnecting] = useState(false);
  const wsError = connectionError;
  
  // Set up WebSocket event handlers
  useEffect(() => {
    // Initial connection - join the room when connected
    if (isConnected) {
      // Join room when connected
      sendMessage({
        type: 'join_room',
        data: { roomId, userId, userName }
      });
      
      setSnackbar({
        open: true,
        message: t('Connected to chat room'),
        severity: 'success'
      });
      
      setIsConnecting(false);
    }
    
    // Event handlers
    const handleMessageReceived = (data) => {
      setMessages(prev => [...prev, {
        id: data.messageId,
        sender: data.userId,
        senderName: data.userName,
        text: data.message,
        timestamp: data.timestamp || new Date().toISOString(),
        isSystemMessage: data.isSystemMessage
      }]);
    };
    
    const handleUserJoined = (data) => {
      setParticipants(prev => [...prev, { id: data.userId, name: data.userName }]);
      setMessages(prev => [...prev, {
        id: `system-${Date.now()}`,
        sender: 'system',
        text: t('{{userName}} joined the chat', { userName: data.userName }),
        timestamp: new Date().toISOString(),
        isSystemMessage: true
      }]);
      
      // Add to online users
      setOnlineUsers(prev => {
        if (!prev.includes(data.userId)) {
          return [...prev, data.userId];
        }
        return prev;
      });
    };
    
    const handleUserLeft = (data) => {
      setParticipants(prev => prev.filter(p => p.id !== data.userId));
      setMessages(prev => [...prev, {
        id: `system-${Date.now()}`,
        sender: 'system',
        text: t('{{userName}} left the chat', { userName: data.userName }),
        timestamp: new Date().toISOString(),
        isSystemMessage: true
      }]);
      
      // Remove from online users
      setOnlineUsers(prev => prev.filter(id => id !== data.userId));
    };
    
    const handleChatHistory = (data) => {
      setMessages(data.messages);
    };
    
    const handleParticipantsList = (data) => {
      setParticipants(data.participants);
      // Add all participants to online users
      setOnlineUsers(data.participants.map(p => p.id));
    };
    
    const handleUserOnline = (data) => {
      if (data.user_id) {
        setOnlineUsers(prev => {
          if (!prev.includes(data.user_id)) {
            return [...prev, data.user_id];
          }
          return prev;
        });
      }
    };
    
    const handleUserOffline = (data) => {
      if (data.user_id) {
        setOnlineUsers(prev => prev.filter(id => id !== data.user_id));
        // Also remove from typing users
        setTypingUsers(prev => prev.filter(id => id !== data.user_id));
      }
    };
    
    const handleTypingUpdate = (data) => {
      if (data.user_id && data.room_id === roomId) {
        if (data.is_typing) {
          setTypingUsers(prev => {
            if (!prev.includes(data.user_id)) {
              return [...prev, data.user_id];
            }
            return prev;
          });
        } else {
          setTypingUsers(prev => prev.filter(id => id !== data.user_id));
        }
      }
    };
    
    // Register all event listeners
    const cleanupFns = [
      on('message_received', handleMessageReceived),
      on('user_joined', handleUserJoined),
      on('user_left', handleUserLeft),
      on('chat_history', handleChatHistory),
      on('participants_list', handleParticipantsList),
      on('user_online', handleUserOnline),
      on('user_offline', handleUserOffline),
      on('typing_update', handleTypingUpdate),
      on('disconnect', (reason) => {
        setSnackbar({
          open: true,
          message: t('Disconnected from chat: {{reason}}', { reason }),
          severity: 'warning'
        });
      })
    ];
    
    // Error handler
    if (connectionError) {
      setSnackbar({
        open: true,
        message: t('Connection error: {{message}}', { message: connectionError }),
        severity: 'error'
      });
      setIsConnecting(false);
    }
    
    // Clean up all event handlers
    return () => {
      cleanupFns.forEach(cleanup => cleanup && cleanup());
    };
  }, [isConnected, connectionError, on, sendMessage, roomId, userId, userName, t]);
  
  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);
  
  // Create debounced function for typing indicators
  const debouncedTypingUpdate = useRef(
    debounce((isTyping) => {
      if (isConnected) {
        sendMessage({
          type: 'typing',
          data: {
            room_id: roomId,
            is_typing: isTyping
          }
        });
      }
    }, 300)
  ).current;
  
  // Handle typing notification when input changes
  useEffect(() => {
    if (inputMessage.length > 0) {
      debouncedTypingUpdate(true);
    } else {
      debouncedTypingUpdate(false);
    }
    
    // Cleanup typing indicator when component unmounts
    return () => {
      debouncedTypingUpdate.cancel();
      if (isConnected) {
        sendMessage({
          type: 'typing',
          data: {
            room_id: roomId,
            is_typing: false
          }
        });
      }
    };
  }, [inputMessage, debouncedTypingUpdate, isConnected, roomId, sendMessage]);
  
  // Handle sending a new message
  const handleSendMessage = () => {
    if (!inputMessage.trim() || !isConnected) return;
    
    const success = sendMessage({
      type: 'send_message',
      data: {
        roomId,
        userId,
        userName,
        message: inputMessage.trim()
      }
    });
    
    if (success) {
      setInputMessage('');
    } else {
      setSnackbar({
        open: true,
        message: t('Failed to send message. Please try again.'),
        severity: 'error'
      });
    }
  };
  
  // Handle pressing Enter to send a message
  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };
  
  // Handle leaving the chat room
  const handleLeaveChat = () => {
    if (isConnected) {
      sendMessage({
        type: 'leave_room', 
        data: { roomId, userId }
      });
    }
    if (onLeave) onLeave();
  };
  
  // Handle reconnecting to the WebSocket
  const handleReconnect = () => {
    connect();
  };
  
  // Close the snackbar
  const handleCloseSnackbar = () => {
    setSnackbar(prev => ({ ...prev, open: false }));
  };
  
  // Format a message timestamp for display
  const formatTimestamp = (timestamp) => {
    try {
      return new Date(timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    } catch (error) {
      return '';
    }
  };
  
  // Get a participant's name by their ID
  const getParticipantName = (id) => {
    const participant = participants.find(p => p.id === id);
    return participant ? participant.name : t('Someone');
  };
  
  // Check if a user is online
  const isUserOnline = (userId) => {
    return onlineUsers.includes(userId);
  };
  
  // Render typing indicator
  const renderTypingIndicator = () => {
    if (typingUsers.length === 0) return null;
    
    const typingNames = typingUsers
      .filter(id => id !== userId) // Don't show for current user
      .map(id => getParticipantName(id));
    
    if (typingNames.length === 0) return null;
    
    let message;
    if (typingNames.length === 1) {
      message = t('{{name}} is typing...', { name: typingNames[0] });
    } else if (typingNames.length === 2) {
      message = t('{{name1}} and {{name2}} are typing...', { 
        name1: typingNames[0], 
        name2: typingNames[1] 
      });
    } else {
      message = t('Several people are typing...');
    }
    
    return (
      <Box sx={{ 
        p: 1, 
        mb: 1, 
        fontStyle: 'italic', 
        color: 'text.secondary',
        fontSize: '0.85rem',
        animation: 'pulse 1.5s infinite'
      }}>
        {message}
      </Box>
    );
  };

  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', height: '100%', maxHeight: '80vh' }}>
      {/* Connection status */}
      {(!isConnected || wsError) && (
        <Alert 
          severity={isConnecting ? 'info' : 'error'} 
          action={
            <Button color="inherit" size="small" onClick={handleReconnect}>
              {t('Reconnect')}
            </Button>
          }
        >
          {isConnecting 
            ? t('Connecting to chat...') 
            : t('Disconnected from chat. Please reconnect.')}
        </Alert>
      )}
      
      {/* Header with room info and participants */}
      <Paper elevation={1} sx={{ p: 2, mb: 2, display: 'flex', justifyContent: 'space-between' }}>
        <Box>
          <Typography variant="h6">{t('Chat Room: {{roomId}}', { roomId })}</Typography>
          <Typography variant="body2" color="textSecondary">
            {t('Connected as {{userName}}', { userName })}
          </Typography>
        </Box>
        <Box>
          <Badge 
            badgeContent={participants.length} 
            color="primary" 
            sx={{ mr: 2 }}
          >
            <PersonIcon />
          </Badge>
          <Button variant="outlined" color="secondary" onClick={handleLeaveChat}>
            {t('Leave Chat')}
          </Button>
        </Box>
      </Paper>
      
      {/* Participants list */}
      <Box sx={{ mb: 2, display: 'flex', flexWrap: 'wrap', gap: 1 }}>
        {participants.map(participant => (
          <Chip 
            key={participant.id}
            label={participant.name}
            variant={participant.id === userId ? "filled" : "outlined"}
            color={isUserOnline(participant.id) ? "success" : "default"}
            avatar={
              <Avatar
                sx={{ 
                  bgcolor: isUserOnline(participant.id) ? 'success.main' : 'grey.400'
                }}
              >
                {participant.name.charAt(0).toUpperCase()}
              </Avatar>
            }
          />
        ))}
      </Box>
      
      {/* Messages list */}
      <Paper 
        elevation={3} 
        sx={{ 
          p: 2, 
          flex: 1, 
          overflowY: 'auto',
          display: 'flex',
          flexDirection: 'column'
        }}
      >
        <List sx={{ flex: 1 }}>
          {messages.length === 0 ? (
            <Box sx={{ textAlign: 'center', my: 4 }}>
              <Typography color="textSecondary">
                {t('No messages yet. Start the conversation!')}
              </Typography>
            </Box>
          ) : (
            messages.map((message) => (
              <ListItem 
                key={message.id || `${message.sender}-${message.timestamp}`}
                sx={{ 
                  flexDirection: 'column',
                  alignItems: message.sender === userId ? 'flex-end' : 'flex-start',
                  mb: 1
                }}
              >
                {/* System messages are centered */}
                {message.isSystemMessage ? (
                  <Paper 
                    elevation={0} 
                    sx={{ 
                      p: 1, 
                      bgcolor: 'grey.100', 
                      width: '100%', 
                      textAlign: 'center' 
                    }}
                  >
                    <Typography variant="body2" color="textSecondary">
                      {message.text}
                    </Typography>
                  </Paper>
                ) : (
                  <Box sx={{ maxWidth: '70%', width: 'auto' }}>
                    <Typography variant="caption" color="textSecondary" sx={{ ml: 1 }}>
                      {message.sender === userId 
                        ? t('You') 
                        : message.senderName || t('Unknown')}
                      {' • '}{formatTimestamp(message.timestamp)}
                    </Typography>
                    <Paper 
                      elevation={1} 
                      sx={{ 
                        p: 2, 
                        bgcolor: message.sender === userId 
                          ? 'primary.light' 
                          : 'grey.100',
                        color: message.sender === userId 
                          ? 'primary.contrastText' 
                          : 'text.primary',
                        borderRadius: 2
                      }}
                    >
                      <Typography variant="body1">{message.text}</Typography>
                    </Paper>
                  </Box>
                )}
              </ListItem>
            ))
          )}
          <div ref={messagesEndRef} />
        </List>
      </Paper>
      
      {/* Message input */}
      <Box sx={{ mt: 2, display: 'flex' }}>
        <TextField
          fullWidth
          variant="outlined"
          placeholder={t('Type a message...')}
          value={inputMessage}
          onChange={(e) => setInputMessage(e.target.value)}
          onKeyPress={handleKeyPress}
          disabled={!isConnected}
          multiline
          maxRows={3}
          sx={{ mr: 1 }}
        />
        <Button
          variant="contained"
          color="primary"
          disabled={!isConnected || !inputMessage.trim()}
          onClick={handleSendMessage}
          endIcon={<SendIcon />}
        >
          {t('Send')}
        </Button>
      </Box>
      
      {/* Status snackbar */}
      <Snackbar
        open={snackbar.open}
        autoHideDuration={6000}
        onClose={handleCloseSnackbar}
        anchorOrigin={{ vertical: 'bottom', horizontal: 'center' }}
      >
        <Alert onClose={handleCloseSnackbar} severity={snackbar.severity}>
          {snackbar.message}
        </Alert>
      </Snackbar>
    </Box>
  );
};

// Define PropTypes
ChatRoom.propTypes = {
  /** Unique identifier for the chat room */
  roomId: PropTypes.string.isRequired,
  /** Current user identifier */
  userId: PropTypes.string.isRequired,
  /** Display name of the current user */
  userName: PropTypes.string,
};

export default ChatRoom; 