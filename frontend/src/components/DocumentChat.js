import React, { useState } from 'react';
import {
  Box,
  Paper,
  Typography,
  TextField,
  Button,
  CircularProgress,
  Avatar,
  Chip,
  useTheme,
  Fade,
  Zoom,
  Divider,
  Alert
} from '@mui/material';
import {
  Send as SendIcon,
  SmartToy as AIIcon,
  Person as PersonIcon,
  Source as SourceIcon
} from '@mui/icons-material';
import { motion, AnimatePresence } from 'framer-motion';

const DocumentChat = ({ documentId, documentTitle }) => {
  const [question, setQuestion] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [chatHistory, setChatHistory] = useState([]);
  const [error, setError] = useState(null);
  const theme = useTheme();

  const handleAskQuestion = async () => {
    if (!question.trim() || isLoading) return;

    const userQuestion = question.trim();
    setQuestion('');
    setIsLoading(true);
    setError(null);

    // Add user question to chat
    const userMessage = {
      id: Date.now(),
      type: 'user',
      content: userQuestion,
      timestamp: new Date(),
    };

    setChatHistory(prev => [...prev, userMessage]);

    try {
      // Import the service dynamically to avoid issues during build
      const { default: documentAIService } = await import('../services/documentAI');
      
      const result = await documentAIService.askQuestion(documentId, userQuestion);

      // Add AI response to chat
      const aiMessage = {
        id: Date.now() + 1,
        type: 'ai',
        content: result.answer,
        sources: result.sources || [],
        timestamp: new Date(),
      };

      setChatHistory(prev => [...prev, aiMessage]);

    } catch (error) {
      console.error('Chat error:', error);
      setError('Failed to get answer. Please try again.');
      
      // Add error message to chat
      const errorMessage = {
        id: Date.now() + 1,
        type: 'error',
        content: 'Sorry, I encountered an error while processing your question. Please try again.',
        timestamp: new Date(),
      };

      setChatHistory(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (event) => {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      handleAskQuestion();
    }
  };

  const formatTimestamp = (timestamp) => {
    return timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  const getMessageVariant = (type) => {
    switch (type) {
      case 'user': return 'contained';
      case 'ai': return 'outlined';
      case 'error': return 'outlined';
      default: return 'outlined';
    }
  };

  const getMessageColor = (type) => {
    switch (type) {
      case 'user': return 'primary';
      case 'ai': return 'success';
      case 'error': return 'error';
      default: return 'default';
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <Box
        sx={{
          borderRadius: 3,
          overflow: 'hidden',
          backgroundColor: '#ffffff',
          boxShadow: '0 4px 20px rgba(0,0,0,0.08)',
        }}
      >
        {/* Chat Header */}
        <Box
          sx={{
            p: 3,
            background: 'linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%)',
            color: 'white',
          }}
        >
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
            <Avatar
              sx={{
                backgroundColor: 'rgba(255,255,255,0.2)',
                color: 'white',
              }}
            >
              <AIIcon />
            </Avatar>
            <Box>
              <Typography variant="h6" sx={{ fontWeight: 600 }}>
                Document AI Assistant
              </Typography>
              <Typography variant="body2" sx={{ opacity: 0.9 }}>
                Ask questions about: {documentTitle || 'your document'}
              </Typography>
            </Box>
          </Box>
        </Box>

        {/* Chat Messages */}
        <Box
          sx={{
            height: 400,
            overflowY: 'auto',
            p: 2,
            backgroundColor: '#fafafa',
          }}
        >
          <AnimatePresence>
            {chatHistory.length === 0 ? (
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
              >
                <Box
                  sx={{
                    textAlign: 'center',
                    py: 8,
                    color: theme.palette.text.secondary,
                  }}
                >
                  <AIIcon sx={{ fontSize: 48, mb: 2, opacity: 0.5 }} />
                  <Typography variant="h6" gutterBottom sx={{ color: '#1e293b' }}>
                    Start a Conversation
                  </Typography>
                  <Typography variant="body2" sx={{ color: '#475569' }}>
                    Ask me anything about your uploaded document. I'll analyze the content and provide detailed answers.
                  </Typography>
                </Box>
              </motion.div>
            ) : (
              chatHistory.map((message, index) => (
                <motion.div
                  key={message.id}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -20 }}
                  transition={{ duration: 0.3 }}
                >
                  <Box
                    sx={{
                      display: 'flex',
                      gap: 2,
                      mb: 2,
                      justifyContent: message.type === 'user' ? 'flex-end' : 'flex-start',
                    }}
                  >
                    {message.type !== 'user' && (
                      <Avatar
                        sx={{
                          backgroundColor: '#2563eb',
                          color: 'white',
                          width: 32,
                          height: 32,
                        }}
                      >
                        <AIIcon fontSize="small" />
                      </Avatar>
                    )}

                    <Box
                      sx={{
                        maxWidth: '70%',
                        minWidth: 200,
                      }}
                    >
                      <Box
                        sx={{
                          p: 2,
                          borderRadius: 12,
                          backgroundColor: message.type === 'user' 
                            ? '#2563eb' 
                            : '#ffffff',
                          color: message.type === 'user' 
                            ? 'white' 
                            : '#1e293b',
                          boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
                          border: message.type === 'user' 
                            ? 'none' 
                            : '1px solid #e2e8f0',
                        }}
                      >
                        <Typography variant="body2" sx={{ whiteSpace: 'pre-wrap' }}>
                          {message.content}
                        </Typography>

                        {message.sources && message.sources.length > 0 && (
                          <Box sx={{ mt: 2, pt: 1, borderTop: '1px solid rgba(0,0,0,0.1)' }}>
                            <Typography variant="caption" sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
                              <SourceIcon fontSize="small" />
                              Sources: {message.sources.join(', ')}
                            </Typography>
                          </Box>
                        )}
                                              </Box>

                                              <Typography
                          variant="caption"
                          sx={{
                            display: 'block',
                            mt: 0.5,
                            textAlign: message.type === 'user' ? 'right' : 'left',
                            color: '#64748b',
                          }}
                        >
                        {formatTimestamp(message.timestamp)}
                      </Typography>
                    </Box>

                    {message.type === 'user' && (
                      <Avatar
                        sx={{
                          backgroundColor: '#7c3aed',
                          color: 'white',
                          width: 32,
                          height: 32,
                        }}
                      >
                        <PersonIcon fontSize="small" />
                      </Avatar>
                    )}
                  </Box>
                </motion.div>
              ))
            )}
          </AnimatePresence>

          {isLoading && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
            >
              <Box sx={{ display: 'flex', gap: 2, mb: 2 }}>
                <Avatar
                  sx={{
                    backgroundColor: '#2563eb',
                    color: 'white',
                    width: 32,
                    height: 32,
                  }}
                >
                  <AIIcon fontSize="small" />
                </Avatar>
                <Paper
                  variant="outlined"
                  sx={{
                    p: 2,
                    borderRadius: 2,
                    backgroundColor: 'white',
                    minWidth: 200,
                  }}
                >
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                    <CircularProgress size={16} />
                    <Typography variant="body2" color="text.secondary">
                      Thinking...
                    </Typography>
                  </Box>
                </Paper>
              </Box>
            </motion.div>
          )}
        </Box>

        <Divider />

        {/* Input Area */}
        <Box sx={{ p: 2 }}>
          {error && (
            <Zoom in={true}>
              <Alert severity="error" sx={{ mb: 2 }}>
                {error}
              </Alert>
            </Zoom>
          )}

          <Box sx={{ display: 'flex', gap: 2 }}>
            <TextField
              fullWidth
              multiline
              rows={2}
              placeholder="Ask a question about your document..."
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              onKeyPress={handleKeyPress}
              disabled={isLoading}
              variant="outlined"
              sx={{
                '& .MuiOutlinedInput-root': {
                  borderRadius: 2,
                  '&:hover': {
                    '& .MuiOutlinedInput-notchedOutline': {
                      borderColor: theme.palette.primary.main,
                    },
                  },
                },
              }}
            />
            <Button
              variant="contained"
              onClick={handleAskQuestion}
              disabled={!question.trim() || isLoading}
              sx={{
                borderRadius: 2,
                px: 3,
                minWidth: 100,
                height: 56,
                fontWeight: 600,
                textTransform: 'none',
                boxShadow: theme.shadows[4],
                '&:hover': {
                  boxShadow: theme.shadows[8],
                  transform: 'translateY(-1px)',
                },
                transition: 'all 0.3s ease',
              }}
            >
              {isLoading ? (
                <CircularProgress size={20} color="inherit" />
              ) : (
                <SendIcon />
              )}
            </Button>
          </Box>

          <Typography
            variant="caption"
            sx={{
              display: 'block',
              mt: 1,
              textAlign: 'center',
              color: theme.palette.text.secondary,
            }}
          >
            Press Enter to send, Shift+Enter for new line
          </Typography>
        </Box>
      </Box>
    </motion.div>
  );
};

export default DocumentChat;
