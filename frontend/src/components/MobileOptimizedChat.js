/**
 * Mobile-Optimized Chat Component
 * Responsive chat interface optimized for mobile devices
 */

import React, { useState, useEffect, useRef } from 'react';
import {
  Box,
  Paper,
  TextField,
  Typography,
  IconButton,
  Button,
  Chip,
  CircularProgress,
  Alert,
  Tooltip,
  Fab,
  Drawer,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  Divider,
  Card,
  CardContent,
  useMediaQuery,
  useTheme,
  SwipeableDrawer,
  Badge
} from '@mui/material';
import {
  Mic as MicIcon,
  MicOff as MicOffIcon,
  VolumeUp as VolumeUpIcon,
  VolumeOff as VolumeOffIcon,
  Send as SendIcon,
  Menu as MenuIcon,
  Close as CloseIcon,
  Chat as ChatIcon,
  Notifications as NotificationsIcon,
  Settings as SettingsIcon,
  History as HistoryIcon,
  Star as StarIcon,
  Share as ShareIcon,
  Download as DownloadIcon
} from '@mui/icons-material';
import { useTranslation } from 'react-i18next';
import { useWebSocket } from '../hooks/useWebSocket';

const MobileOptimizedChat = () => {
  const { t } = useTranslation();
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('md'));
  const isTablet = useMediaQuery(theme.breakpoints.down('lg'));
  
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isListening, setIsListening] = useState(false);
  const [isSpeaking, setIsSpeaking] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const [error, setError] = useState(null);
  const [drawerOpen, setDrawerOpen] = useState(false);
  const [showVoiceControls, setShowVoiceControls] = useState(false);
  const [unreadCount, setUnreadCount] = useState(0);
  
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  // WebSocket connection for real-time features
  const { sendMessage, lastMessage, connectionStatus } = useWebSocket('ws://localhost:8765');

  // Auto-scroll to bottom
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Handle incoming WebSocket messages
  useEffect(() => {
    if (lastMessage) {
      try {
        const data = JSON.parse(lastMessage.data);
        if (data.type === 'chat_message') {
          const newMessage = {
            id: Date.now(),
            text: data.message,
            sender: 'assistant',
            timestamp: new Date().toLocaleTimeString(),
            type: 'text'
          };
          setMessages(prev => [...prev, newMessage]);
          setUnreadCount(prev => prev + 1);
        }
      } catch (error) {
        console.error('Error parsing WebSocket message:', error);
      }
    }
  }, [lastMessage]);

  const handleSubmit = async (text = input) => {
    if (!text.trim() || isProcessing) return;

    const userMessage = {
      id: Date.now(),
      text: text,
      sender: 'user',
      timestamp: new Date().toLocaleTimeString(),
      type: 'text'
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsProcessing(true);
    setError(null);

    try {
      // Send via WebSocket for real-time response
      sendMessage(JSON.stringify({
        type: 'chat_message',
        message: text,
        user_id: 'mobile_user'
      }));

      // Also send to API for processing
      const response = await fetch('http://localhost:3001/api/legal-analysis', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          query: text,
          jurisdiction: 'ri'
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      
      if (data.success) {
        const aiMessage = {
          id: Date.now() + 1,
          text: formatAIResponse(data),
          sender: 'assistant',
          timestamp: new Date().toLocaleTimeString(),
          type: 'text',
          analysis: data.analysis
        };

        setMessages(prev => [...prev, aiMessage]);
        setUnreadCount(prev => prev + 1);
      } else {
        throw new Error(data.error || 'Analysis failed');
      }
    } catch (err) {
      console.error('Error calling AI backend:', err);
      setError(err.message);
      
      const errorMessage = {
        id: Date.now() + 1,
        text: "I apologize, but I'm experiencing technical difficulties. Please try again or consult with a qualified attorney for immediate assistance.",
        sender: 'assistant',
        timestamp: new Date().toLocaleTimeString(),
        type: 'error'
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsProcessing(false);
    }
  };

  const formatAIResponse = (data) => {
    const analysis = data.analysis || {};
    let response = '';

    if (analysis.case_summary) {
      response += `Analysis: ${analysis.case_summary}\n\n`;
    }

    if (analysis.key_facts && analysis.key_facts.length > 0) {
      response += `Key Facts:\n${analysis.key_facts.map(fact => `• ${fact}`).join('\n')}\n\n`;
    }

    if (analysis.practical_advice && analysis.practical_advice.length > 0) {
      response += `Advice:\n${analysis.practical_advice.map(advice => `• ${advice}`).join('\n')}\n\n`;
    }

    if (data.disclaimers && data.disclaimers.length > 0) {
      response += `Important: ${data.disclaimers.join(' ')}`;
    }

    return response || 'I understand your question. How can I help you?';
  };

  const startVoiceInput = () => {
    if ('webkitSpeechRecognition' in window) {
      const recognition = new window.webkitSpeechRecognition();
      recognition.continuous = false;
      recognition.interimResults = true;
      recognition.lang = 'en-US';

      recognition.onstart = () => {
        setIsListening(true);
        setError(null);
      };

      recognition.onresult = (event) => {
        let finalTranscript = '';
        let interimTranscript = '';
        
        for (let i = event.resultIndex; i < event.results.length; i++) {
          const transcript = event.results[i][0].transcript;
          if (event.results[i].isFinal) {
            finalTranscript += transcript;
          } else {
            interimTranscript += transcript;
          }
        }
        
        if (finalTranscript) {
          setInput(finalTranscript);
          handleSubmit(finalTranscript);
        } else {
          setInput(interimTranscript);
        }
      };

      recognition.onerror = (event) => {
        console.error('Speech recognition error:', event.error);
        setError(`Speech recognition error: ${event.error}`);
        setIsListening(false);
      };

      recognition.onend = () => {
        setIsListening(false);
      };

      recognition.start();
    } else {
      setError('Speech recognition not supported in this browser');
    }
  };

  const stopVoiceInput = () => {
    setIsListening(false);
  };

  const speakText = (text) => {
    if ('speechSynthesis' in window) {
      const utterance = new SpeechSynthesisUtterance(text);
      utterance.rate = 0.8;
      utterance.pitch = 1.0;
      utterance.volume = 0.8;

      utterance.onstart = () => {
        setIsSpeaking(true);
      };

      utterance.onend = () => {
        setIsSpeaking(false);
      };

      utterance.onerror = (event) => {
        console.error('Speech synthesis error:', event.error);
        setError(`Speech synthesis error: ${event.error}`);
        setIsSpeaking(false);
      };

      window.speechSynthesis.speak(utterance);
    } else {
      setError('Speech synthesis not supported in this browser');
    }
  };

  const stopSpeaking = () => {
    if ('speechSynthesis' in window) {
      window.speechSynthesis.cancel();
      setIsSpeaking(false);
    }
  };

  const clearChat = () => {
    setMessages([]);
    setError(null);
    setUnreadCount(0);
  };

  const exportChat = () => {
    const chatData = {
      messages: messages,
      timestamp: new Date().toISOString(),
      export_version: '1.0'
    };
    
    const blob = new Blob([JSON.stringify(chatData, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `smartprobono-chat-${new Date().toISOString().split('T')[0]}.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  const shareChat = () => {
    if (navigator.share) {
      const chatText = messages.map(msg => 
        `${msg.sender}: ${msg.text}`
      ).join('\n\n');
      
      navigator.share({
        title: 'SmartProBono Chat',
        text: chatText,
        url: window.location.href
      });
    } else {
      // Fallback to clipboard
      const chatText = messages.map(msg => 
        `${msg.sender}: ${msg.text}`
      ).join('\n\n');
      
      navigator.clipboard.writeText(chatText).then(() => {
        setError('Chat copied to clipboard');
        setTimeout(() => setError(null), 3000);
      });
    }
  };

  const drawerContent = (
    <Box sx={{ width: 280, p: 2 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
        <Typography variant="h6">Chat Options</Typography>
        <IconButton onClick={() => setDrawerOpen(false)}>
          <CloseIcon />
        </IconButton>
      </Box>
      
      <List>
        <ListItem button onClick={clearChat}>
          <ListItemIcon>
            <HistoryIcon />
          </ListItemIcon>
          <ListItemText primary="Clear Chat" />
        </ListItem>
        
        <ListItem button onClick={exportChat}>
          <ListItemIcon>
            <DownloadIcon />
          </ListItemIcon>
          <ListItemText primary="Export Chat" />
        </ListItem>
        
        <ListItem button onClick={shareChat}>
          <ListItemIcon>
            <ShareIcon />
          </ListItemIcon>
          <ListItemText primary="Share Chat" />
        </ListItem>
        
        <Divider sx={{ my: 1 }} />
        
        <ListItem>
          <ListItemText 
            primary="Connection Status" 
            secondary={connectionStatus === 'Open' ? 'Connected' : 'Disconnected'}
          />
        </ListItem>
        
        <ListItem>
          <ListItemText 
            primary="Messages" 
            secondary={`${messages.length} messages`}
          />
        </ListItem>
      </List>
    </Box>
  );

  return (
    <Box sx={{ 
      height: '100vh', 
      display: 'flex', 
      flexDirection: 'column',
      bgcolor: 'background.default'
    }}>
      {/* Mobile Header */}
      <Paper elevation={2} sx={{ 
        p: 2, 
        borderRadius: 0,
        position: 'sticky',
        top: 0,
        zIndex: 1000
      }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            <IconButton onClick={() => setDrawerOpen(true)}>
              <MenuIcon />
            </IconButton>
            <Typography variant="h6">AI Legal Assistant</Typography>
            <Badge badgeContent={unreadCount} color="primary">
              <ChatIcon />
            </Badge>
          </Box>
          
          <Box sx={{ display: 'flex', gap: 1 }}>
            <Chip 
              label={isListening ? "Listening" : isSpeaking ? "Speaking" : "Ready"} 
              color={isListening ? "primary" : isSpeaking ? "secondary" : "default"}
              size="small"
            />
            <IconButton onClick={() => setShowVoiceControls(!showVoiceControls)}>
              <SettingsIcon />
            </IconButton>
          </Box>
        </Box>
      </Paper>

      {/* Voice Controls */}
      {showVoiceControls && (
        <Paper elevation={1} sx={{ p: 2, m: 1 }}>
          <Typography variant="subtitle2" gutterBottom>Voice Controls</Typography>
          <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
            <Button
              variant={isListening ? "contained" : "outlined"}
              startIcon={isListening ? <MicOffIcon /> : <MicIcon />}
              onClick={isListening ? stopVoiceInput : startVoiceInput}
              disabled={isProcessing}
            >
              {isListening ? "Stop" : "Voice Input"}
            </Button>
            
            {isSpeaking && (
              <Button
                variant="outlined"
                startIcon={<VolumeOffIcon />}
                onClick={stopSpeaking}
              >
                Stop Speaking
              </Button>
            )}
          </Box>
        </Paper>
      )}

      {/* Messages */}
      <Box sx={{ 
        flex: 1, 
        overflow: 'auto', 
        p: 1,
        display: 'flex',
        flexDirection: 'column'
      }}>
        {messages.length === 0 ? (
          <Box sx={{ 
            display: 'flex', 
            justifyContent: 'center', 
            alignItems: 'center', 
            height: '100%',
            flexDirection: 'column',
            gap: 2,
            p: 3
          }}>
            <ChatIcon sx={{ fontSize: 64, color: 'primary.main', opacity: 0.7 }} />
            <Typography variant="h6" color="text.secondary" align="center">
              Start a conversation
            </Typography>
            <Typography variant="body2" color="text.secondary" align="center">
              Ask me about legal matters, immigration cases, or any legal questions you have.
            </Typography>
            {isMobile && (
              <Button
                variant="contained"
                startIcon={<MicIcon />}
                onClick={startVoiceInput}
                sx={{ mt: 2 }}
              >
                Start Voice Chat
              </Button>
            )}
          </Box>
        ) : (
          <Box>
            {messages.map((message) => (
              <Box
                key={message.id}
                sx={{
                  display: 'flex',
                  justifyContent: message.sender === 'user' ? 'flex-end' : 'flex-start',
                  mb: 2
                }}
              >
                <Card sx={{ 
                  maxWidth: isMobile ? '85%' : '70%',
                  bgcolor: message.sender === 'user' ? 'primary.main' : 'grey.100',
                  color: message.sender === 'user' ? 'primary.contrastText' : 'text.primary'
                }}>
                  <CardContent sx={{ p: 2 }}>
                    <Typography variant="body2" sx={{ wordBreak: 'break-word' }}>
                      {message.text}
                    </Typography>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mt: 1 }}>
                      <Typography variant="caption" sx={{ opacity: 0.7 }}>
                        {message.timestamp}
                      </Typography>
                      {message.sender === 'assistant' && message.type !== 'error' && (
                        <IconButton 
                          size="small" 
                          onClick={() => speakText(message.text)}
                          disabled={isSpeaking}
                          sx={{ color: 'inherit' }}
                        >
                          <VolumeUpIcon fontSize="small" />
                        </IconButton>
                      )}
                    </Box>
                  </CardContent>
                </Card>
              </Box>
            ))}
            <div ref={messagesEndRef} />
          </Box>
        )}
      </Box>

      {/* Error Display */}
      {error && (
        <Alert severity="error" sx={{ m: 1 }}>
          {error}
        </Alert>
      )}

      {/* Input Area */}
      <Paper elevation={4} sx={{ p: 2, borderRadius: 0 }}>
        <Box sx={{ display: 'flex', gap: 1, alignItems: 'flex-end' }}>
          <TextField
            ref={inputRef}
            fullWidth
            multiline
            maxRows={isMobile ? 3 : 4}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Type your message or use voice input..."
            variant="outlined"
            size="small"
            disabled={isProcessing}
            onKeyPress={(e) => {
              if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                handleSubmit();
              }
            }}
          />
          
          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1 }}>
            {isMobile && (
              <IconButton
                color={isListening ? "error" : "primary"}
                onClick={isListening ? stopVoiceInput : startVoiceInput}
                disabled={isProcessing}
                sx={{ 
                  bgcolor: isListening ? 'error.main' : 'primary.main',
                  color: 'white',
                  '&:hover': {
                    bgcolor: isListening ? 'error.dark' : 'primary.dark',
                  }
                }}
              >
                {isListening ? <MicOffIcon /> : <MicIcon />}
              </IconButton>
            )}
            
            <Button
              variant="contained"
              onClick={() => handleSubmit()}
              disabled={!input.trim() || isProcessing}
              startIcon={isProcessing ? <CircularProgress size={20} /> : <SendIcon />}
              sx={{ minWidth: 'auto' }}
            >
              {isProcessing ? '' : 'Send'}
            </Button>
          </Box>
        </Box>
      </Paper>

      {/* Mobile FAB for voice input */}
      {isMobile && !isListening && (
        <Fab
          color="primary"
          aria-label="voice input"
          onClick={startVoiceInput}
          sx={{
            position: 'fixed',
            bottom: 100,
            right: 16,
            zIndex: 1000
          }}
        >
          <MicIcon />
        </Fab>
      )}

      {/* Drawer */}
      <SwipeableDrawer
        anchor="left"
        open={drawerOpen}
        onClose={() => setDrawerOpen(false)}
        onOpen={() => setDrawerOpen(true)}
      >
        {drawerContent}
      </SwipeableDrawer>
    </Box>
  );
};

export default MobileOptimizedChat;
