import React, { useState, useRef, useEffect } from 'react';
import {
  Box,
  TextField,
  Typography,
  Paper,
  List,
  ListItem,
  CircularProgress,
  Alert,
  Container,
  Chip,
  IconButton,
  Tooltip,
  Avatar,
  Divider
} from '@mui/material';
import SendIcon from '@mui/icons-material/Send';
import GavelIcon from '@mui/icons-material/Gavel';
import { useTranslation } from 'react-i18next';

const ImprovedLegalAIChat = () => {
  const { t } = useTranslation();
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const formatAIResponse = (data) => {
    // Just return the text directly - no verbose formatting
    if (data.text) {
      return data.text;
    }
    if (data.response) {
      return data.response;
    }
    if (data.analysis?.text) {
      return data.analysis.text;
    }
    // Fallback - return simple message
    return data.message || "I understand. How can I help you today?";
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const userMessage = {
      id: Date.now(),
      text: input,
      sender: 'user',
      timestamp: new Date().toLocaleTimeString()
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);
    setError(null);

    try {
      // Call the new unified legal AI backend
      const response = await fetch('http://localhost:3001/api/v1/legal/analyze', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          query: input,
          jurisdiction: 'ri' // Default to Rhode Island
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      
      if (data.success) {
        // Format the response for display
        const aiMessage = {
          id: Date.now() + 1,
          text: formatAIResponse(data),
          sender: 'assistant',
          timestamp: new Date().toLocaleTimeString(),
          analysis: data.analysis,
          disclaimers: data.disclaimers || [],
          warnings: data.warnings || [],
          recommendations: data.recommendations || []
        };

        setMessages(prev => [...prev, aiMessage]);
      } else {
        // Even if the main analysis fails, show the disclaimers and warnings
        const fallbackMessage = {
          id: Date.now() + 1,
          text: formatAIResponse(data),
          sender: 'assistant',
          timestamp: new Date().toLocaleTimeString(),
          analysis: data.analysis || {},
          disclaimers: data.disclaimers || [],
          warnings: data.warnings || [],
          recommendations: data.recommendations || []
        };
        setMessages(prev => [...prev, fallbackMessage]);
      }
    } catch (err) {
      console.error('Error calling legal AI backend:', err);
      setError(err.message);
      
      // Fallback to simple response
      const fallbackMessage = {
        id: Date.now() + 1,
        text: "I apologize, but I'm experiencing technical difficulties. Please try again or consult with a qualified attorney for immediate assistance.",
        sender: 'assistant',
        timestamp: new Date().toLocaleTimeString()
      };
      setMessages(prev => [...prev, fallbackMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  return (
    <Container maxWidth="md" sx={{ py: 4 }}>
      <Box sx={{ mb: 3, textAlign: 'center' }}>
        <Avatar sx={{ bgcolor: 'primary.main', mx: 'auto', mb: 2 }}>
          <GavelIcon />
        </Avatar>
        <Typography variant="h4" component="h1" gutterBottom>
          {t('legalAI.title')}
        </Typography>
        <Typography variant="body1" color="text.secondary">
          Get intelligent legal analysis powered by case law research and AI
        </Typography>
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }} onClose={() => setError(null)}>
          {error}
        </Alert>
      )}

      <Paper sx={{ 
        height: { xs: 'calc(100vh - 300px)', md: 'calc(100vh - 250px)' },
        minHeight: '600px',
        maxHeight: '90vh',
        display: 'flex', 
        flexDirection: 'column' 
      }}>
        <Box sx={{ flex: 1, overflow: 'auto', p: 2 }}>
          <List>
            {messages.map((message) => (
              <React.Fragment key={message.id}>
                <ListItem
                  sx={{
                    flexDirection: message.sender === 'user' ? 'row-reverse' : 'row',
                    alignItems: 'flex-start'
                  }}
                >
                  <Avatar
                    sx={{
                      bgcolor: message.sender === 'user' ? 'primary.main' : 'secondary.main',
                      mr: message.sender === 'user' ? 0 : 1,
                      ml: message.sender === 'user' ? 1 : 0
                    }}
                  >
                    {message.sender === 'user' ? 'U' : 'AI'}
                  </Avatar>
                  <Box sx={{ maxWidth: '70%' }}>
                    <Paper
                      sx={{
                        p: 2,
                        bgcolor: message.sender === 'user' ? 'primary.light' : 'grey.100',
                        color: message.sender === 'user' ? 'primary.contrastText' : 'text.primary'
                      }}
                    >
                      <Typography variant="body1" sx={{ whiteSpace: 'pre-wrap' }}>
                        {message.text}
                      </Typography>
                    </Paper>
                    
                    {/* Display disclaimers and warnings */}
                    {message.disclaimers && message.disclaimers.length > 0 && (
                      <Box sx={{ mt: 1 }}>
                        {message.disclaimers.map((disclaimer, index) => (
                          <Chip
                            key={index}
                            label={disclaimer}
                            size="small"
                            color="warning"
                            sx={{ mr: 0.5, mb: 0.5 }}
                          />
                        ))}
                      </Box>
                    )}
                    
                    {message.warnings && message.warnings.length > 0 && (
                      <Box sx={{ mt: 1 }}>
                        {message.warnings.map((warning, index) => (
                          <Chip
                            key={index}
                            label={warning}
                            size="small"
                            color="error"
                            sx={{ mr: 0.5, mb: 0.5 }}
                          />
                        ))}
                      </Box>
                    )}
                    
                    <Typography variant="caption" color="text.secondary" sx={{ mt: 1, display: 'block' }}>
                      {message.timestamp}
                    </Typography>
                  </Box>
                </ListItem>
                <Divider />
              </React.Fragment>
            ))}
            {isLoading && (
              <ListItem>
                <Avatar sx={{ bgcolor: 'secondary.main', mr: 1 }}>
                  <CircularProgress size={20} color="inherit" />
                </Avatar>
                <Typography variant="body2" color="text.secondary">
                  Analyzing your legal situation...
                </Typography>
              </ListItem>
            )}
          </List>
          <div ref={messagesEndRef} />
        </Box>

        <Box component="form" onSubmit={handleSubmit} sx={{ p: 2, borderTop: 1, borderColor: 'divider' }}>
          <Box sx={{ display: 'flex', gap: 1 }}>
            <TextField
              fullWidth
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Describe your legal situation..."
              variant="outlined"
              multiline
              maxRows={3}
              disabled={isLoading}
            />
            <Tooltip title="Send message">
              <IconButton
                type="submit"
                color="primary"
                disabled={!input.trim() || isLoading}
                sx={{ alignSelf: 'flex-end' }}
              >
                <SendIcon />
              </IconButton>
            </Tooltip>
          </Box>
        </Box>
      </Paper>
    </Container>
  );
};

export default ImprovedLegalAIChat;