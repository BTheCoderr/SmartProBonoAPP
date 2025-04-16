import React, { useState, useEffect, useRef } from 'react';
import {
  Box,
  Container,
  Typography,
  TextField,
  Button,
  Paper,
  List,
  ListItem,
  ListItemText,
  CircularProgress,
  IconButton,
  Tooltip,
  Divider,
  Alert,
  Chip,
} from '@mui/material';
import { useTranslation } from 'react-i18next';
import AttachFileIcon from '@mui/icons-material/AttachFile';
import DownloadIcon from '@mui/icons-material/Download';
import SendIcon from '@mui/icons-material/Send';
import config from '../config';
import { logInfo, logError } from '../utils/logger';
import { useWebSocket } from '../contexts/WebSocketContext';
import { useAuth } from '../contexts/AuthContext';
import { v4 as uuidv4 } from 'uuid';

const LegalAIChat = () => {
  const { t } = useTranslation();
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState('');
  const [files, setFiles] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const messagesEndRef = useRef(null);
  const fileInputRef = useRef(null);
  
  // Use WebSocket context and auth context
  const { 
    isConnected, 
    connectionError,
    connect,
    sendMessage,
    on,
    off
  } = useWebSocket();
  
  const { isAuthenticated, user } = useAuth();
  
  // Set up event listeners for WebSocket messages
  useEffect(() => {
    // Handle AI responses through WebSocket
    const handleAiResponse = (data) => {
      setMessages(prev => [...prev, {
        sender: 'ai',
        content: data.content,
        timestamp: data.timestamp || new Date().toISOString(),
        files: data.files || [],
        queryId: data.query_id
      }]);
      setIsLoading(false);
    };
    
    // Handle errors
    const handleError = (data) => {
      setError(data.message || 'An error occurred');
      setIsLoading(false);
    };
    
    // Register event listeners
    const cleanupFns = [
      on('ai_response', handleAiResponse),
      on('error', handleError)
    ];
    
    // Cleanup when unmounting
    return () => {
      cleanupFns.forEach(cleanup => cleanup && cleanup());
    };
  }, [on, off]);
  
  // Connect to WebSocket if not connected
  useEffect(() => {
    if (!isConnected && config.features.enableWebSocket) {
      connect();
    }
  }, [isConnected, connect]);
  
  // Update error state when connection error changes
  useEffect(() => {
    if (connectionError) {
      setError(`WebSocket: ${connectionError}. Falling back to HTTP requests.`);
    }
  }, [connectionError]);

  // Scroll to bottom on new messages
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Load chat history
  useEffect(() => {
    const loadChatHistory = async () => {
      try {
        const response = await fetch('/api/legal/chat/history');
        if (!response.ok) throw new Error('Failed to load chat history');
        const data = await response.json();
        setMessages(data);
      } catch (err) {
        setError('Failed to load chat history');
      }
    };
    loadChatHistory();
  }, []);

  const handleSend = async () => {
    if (!newMessage.trim() && files.length === 0) return;
    
    setIsLoading(true);
    setError(null);
    
    // Generate query ID to track this conversation
    const queryId = uuidv4();
    
    // Add user message to the list
    const userMessage = {
      sender: 'user',
      content: newMessage.trim(),
      timestamp: new Date().toISOString(),
      files: files.map(file => ({ name: file.name })),
      queryId
    };
    
    setMessages(prev => [...prev, userMessage]);
    
    try {
      // Try WebSocket first if connected
      if (isConnected) {
        const success = sendMessage({
          type: 'legal_query',
          data: {
            query: newMessage.trim(),
            timestamp: new Date().toISOString(),
            query_id: queryId
          }
        });
        
        if (!success) {
          throw new Error('Failed to send message through WebSocket');
        }
      } else {
        // Fallback to HTTP
        const formData = new FormData();
        formData.append('message', newMessage);
        formData.append('query_id', queryId);
        files.forEach(file => formData.append('files', file));
        
        const response = await fetch('/api/legal/chat', {
          method: 'POST',
          body: formData,
        });
        
        if (!response.ok) {
          throw new Error('Failed to send message');
        }
        
        const data = await response.json();
        setMessages(prev => [...prev, {
          sender: 'ai',
          content: data.response,
          timestamp: data.timestamp || new Date().toISOString(),
          files: data.files || [],
          queryId: data.query_id || queryId
        }]);
        
        setIsLoading(false);
      }
      
      setNewMessage('');
      setFiles([]);
    } catch (err) {
      logError('Error sending message:', err);
      setError('Failed to send message: ' + (err.message || 'Unknown error'));
      setIsLoading(false);
    }
  };

  const handleFileSelect = (event) => {
    setFiles(Array.from(event.target.files));
  };

  const handleKeyPress = (event) => {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      handleSend();
    }
  };

  const exportChat = () => {
    const chatHistory = messages.map(msg => 
      `${new Date(msg.timestamp).toLocaleString()}\n${msg.sender}: ${msg.content}`
    ).join('\n\n');
    
    const blob = new Blob([chatHistory], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `chat-history-${new Date().toISOString()}.txt`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  return (
    <Container maxWidth="md" sx={{ py: 4 }}>
      <Paper elevation={3} sx={{ p: 3, mb: 3 }}>
        <Typography variant="h4" gutterBottom align="center">
          {t('Legal AI Assistant')}
        </Typography>
        {error && (
          <Alert severity="error" sx={{ mb: 2 }}>
            {error}
          </Alert>
        )}
        <Box sx={{ mb: 2, display: 'flex', justifyContent: 'flex-end' }}>
          <Tooltip title={t('Export Chat')}>
            <IconButton onClick={exportChat}>
              <DownloadIcon />
            </IconButton>
          </Tooltip>
        </Box>
        <Paper
          variant="outlined"
          sx={{
            height: '60vh',
            overflow: 'auto',
            mb: 2,
            p: 2,
            backgroundColor: '#f9f9f9',
          }}
        >
          <List>
            {messages.length === 0 ? (
              <Box
                sx={{
                  display: 'flex',
                  height: '100%',
                  alignItems: 'center',
                  justifyContent: 'center',
                }}
              >
                <Typography color="text.secondary">
                  {t('Start a conversation to get legal assistance')}
                </Typography>
              </Box>
            ) : (
              messages.map((msg, index) => (
                <ListItem
                  key={index}
                  alignItems="flex-start"
                  sx={{
                    flexDirection: msg.sender === 'user' ? 'row-reverse' : 'row',
                    mb: 1,
                  }}
                >
                  <Paper
                    elevation={1}
                    sx={{
                      p: 2,
                      maxWidth: '80%',
                      backgroundColor:
                        msg.sender === 'user' ? '#e3f2fd' : '#ffffff',
                      borderRadius: 2,
                    }}
                  >
                    <Typography variant="subtitle2" color="text.secondary">
                      {msg.sender === 'user' ? t('You') : t('AI Assistant')} •{' '}
                      {new Date(msg.timestamp).toLocaleString()}
                    </Typography>
                    <Typography variant="body1" sx={{ mt: 1, whiteSpace: 'pre-wrap' }}>
                      {msg.content}
                    </Typography>
                    {msg.files && msg.files.length > 0 && (
                      <Box sx={{ mt: 1 }}>
                        <Typography variant="subtitle2">
                          {t('Attached Files')}:
                        </Typography>
                        {msg.files.map((file, fileIndex) => (
                          <Chip
                            key={fileIndex}
                            label={file.name}
                            size="small"
                            sx={{ m: 0.5 }}
                          />
                        ))}
                      </Box>
                    )}
                  </Paper>
                </ListItem>
              ))
            )}
            <div ref={messagesEndRef} />
          </List>
          {isLoading && (
            <Box sx={{ display: 'flex', justifyContent: 'center', my: 2 }}>
              <CircularProgress size={24} />
            </Box>
          )}
        </Paper>
        <Box sx={{ display: 'flex', alignItems: 'flex-start' }}>
          <Box sx={{ flexGrow: 1 }}>
            <TextField
              fullWidth
              multiline
              rows={2}
              placeholder={t('Type your legal question here...')}
              value={newMessage}
              onChange={(e) => setNewMessage(e.target.value)}
              onKeyPress={handleKeyPress}
              disabled={isLoading}
              InputProps={{
                endAdornment: (
                  <Tooltip title={t('Attach Files')}>
                    <IconButton
                      onClick={() => fileInputRef.current.click()}
                      disabled={isLoading}
                    >
                      <AttachFileIcon />
                    </IconButton>
                  </Tooltip>
                ),
              }}
              sx={{ mr: 1 }}
            />
            <input
              type="file"
              multiple
              ref={fileInputRef}
              onChange={handleFileSelect}
              style={{ display: 'none' }}
            />
            {files.length > 0 && (
              <Box sx={{ mt: 1 }}>
                {files.map((file, index) => (
                  <Chip
                    key={index}
                    label={file.name}
                    size="small"
                    onDelete={() => setFiles(files.filter((_, i) => i !== index))}
                    sx={{ m: 0.5 }}
                  />
                ))}
              </Box>
            )}
          </Box>
          <Button
            variant="contained"
            color="primary"
            endIcon={<SendIcon />}
            onClick={handleSend}
            disabled={isLoading || (!newMessage.trim() && files.length === 0)}
            sx={{ mt: 1, height: 40 }}
          >
            {t('Send')}
          </Button>
        </Box>
      </Paper>
    </Container>
  );
};

export default LegalAIChat; 