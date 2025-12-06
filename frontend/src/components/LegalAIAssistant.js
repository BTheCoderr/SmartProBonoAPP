import React, { useState, useRef, useEffect } from 'react';
import {
  Box,
  Grid,
  Paper,
  Typography,
  TextField,
  Button,
  IconButton,
  CircularProgress,
  Alert,
  Chip,
  Avatar,
  Divider,
  List,
  ListItem,
  ListItemText,
  Card,
  CardContent,
} from '@mui/material';
import {
  CloudUpload as UploadIcon,
  Send as SendIcon,
  ChatBubble as ChatIcon,
  Description as DocumentIcon,
  CheckCircle as CheckIcon,
  Error as ErrorIcon,
} from '@mui/icons-material';
import { API_URL } from '../config';

const LegalAIAssistant = () => {
  const [messages, setMessages] = useState([
    {
      id: 1,
      text: "Hi! I'm your AI legal assistant. I help organize client intakes and prepare draft documents for attorney review.",
      sender: 'assistant',
      timestamp: new Date().toLocaleTimeString(),
    },
    {
      id: 2,
      text: "You can upload an intake form, paste client information, or just tell me what you're working on. What can I help you with today?",
      sender: 'assistant',
      timestamp: new Date().toLocaleTimeString(),
    },
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [selectedFile, setSelectedFile] = useState(null);
  const [uploadStatus, setUploadStatus] = useState(null);
  const [uploadedDocument, setUploadedDocument] = useState(null);
  const [generatedOutput, setGeneratedOutput] = useState(null);
  const messagesEndRef = useRef(null);
  const fileInputRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleFileSelect = (event) => {
    const file = event.target.files?.[0];
    if (file) {
      // Validate file type
      const allowedTypes = ['.txt', '.pdf', '.doc', '.docx'];
      const fileExtension = '.' + file.name.split('.').pop().toLowerCase();
      
      if (!allowedTypes.includes(fileExtension)) {
        setError('Please upload a TXT, PDF, DOC, or DOCX file');
        return;
      }

      // Validate file size (max 10MB)
      if (file.size > 10 * 1024 * 1024) {
        setError('File size must be less than 10MB');
        return;
      }

      setSelectedFile(file);
      setError(null);
      setUploadStatus(null);
    }
  };

  const handleFileUpload = async () => {
    if (!selectedFile) return;

    setUploadStatus('uploading');
    setError(null);

    try {
      const formData = new FormData();
      formData.append('file', selectedFile);

      const response = await fetch(`${API_URL}/api/scanner/analyze`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`Upload failed: ${response.status}`);
      }

      const result = await response.json();
      setUploadStatus('success');
      setUploadedDocument(result);
      
      // Add message about uploaded document
      const uploadMessage = {
        id: Date.now(),
        text: `I've uploaded and analyzed your ${selectedFile.name}. ${result.extracted_text ? 'I can help you review it or generate documents based on it.' : 'How can I help you with this document?'}`,
        sender: 'assistant',
        timestamp: new Date().toLocaleTimeString(),
        document: result,
      };
      setMessages(prev => [...prev, uploadMessage]);

      // Clear file selection after 3 seconds
      setTimeout(() => {
        setSelectedFile(null);
        setUploadStatus(null);
        if (fileInputRef.current) {
          fileInputRef.current.value = '';
        }
      }, 3000);
    } catch (err) {
      console.error('Upload error:', err);
      setError(err.message || 'Failed to upload file');
      setUploadStatus('error');
    }
  };

  const handleSendMessage = async (e) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const userMessage = {
      id: Date.now(),
      text: input,
      sender: 'user',
      timestamp: new Date().toLocaleTimeString(),
    };

    setMessages(prev => [...prev, userMessage]);
    const currentInput = input;
    setInput('');
    setIsLoading(true);
    setError(null);

    try {
      // Check if we should generate a document or just chat
      const isDocumentRequest = currentInput.toLowerCase().includes('generate') || 
                                currentInput.toLowerCase().includes('create') ||
                                currentInput.toLowerCase().includes('draft') ||
                                currentInput.toLowerCase().includes('letter') ||
                                currentInput.toLowerCase().includes('form');

      let response;
      const requestBody = {
        message: currentInput,
        task_type: isDocumentRequest ? 'document_generation' : 'legal_assistance',
      };

      // Add context if document is uploaded
      if (uploadedDocument) {
        requestBody.context = uploadedDocument.extracted_text || uploadedDocument.text || uploadedDocument.analysis?.text;
      }

      // Try /api/v1/legal/chat first, fallback to /api/v1/ai/chat
      try {
        response = await fetch(`${API_URL}/api/v1/legal/chat`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(requestBody),
        });
      } catch (err) {
        // Fallback to unified AI endpoint
        response = await fetch(`${API_URL}/api/v1/ai/chat`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(requestBody),
        });
      }

      if (!response.ok) {
        throw new Error(`Request failed: ${response.status}`);
      }

      const data = await response.json();
      
      const aiMessage = {
        id: Date.now() + 1,
        text: data.response || data.text || data.message || "I understand. How can I help you further?",
        sender: 'assistant',
        timestamp: new Date().toLocaleTimeString(),
      };

      setMessages(prev => [...prev, aiMessage]);

      // If document was generated, show it in output panel
      if (data.document || data.generated_document) {
        setGeneratedOutput({
          title: data.document_title || 'Generated Document',
          content: data.document || data.generated_document || data.response,
          type: data.document_type || 'legal_document',
        });
      }
    } catch (err) {
      console.error('Chat error:', err);
      setError(err.message || 'Failed to send message');
      
      const errorMessage = {
        id: Date.now() + 1,
        text: "I apologize, but I'm experiencing technical difficulties. Please try again or consult with a qualified attorney for immediate assistance.",
        sender: 'assistant',
        timestamp: new Date().toLocaleTimeString(),
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage(e);
    }
  };

  const getFileTypeLabel = (filename) => {
    const ext = filename.split('.').pop().toLowerCase();
    if (ext === 'txt') return 'Plain Text';
    if (ext === 'pdf') return 'Documents';
    if (ext === 'doc' || ext === 'docx') return 'Word Files';
    return 'File';
  };

  const getFileTypeColor = (filename) => {
    const ext = filename.split('.').pop().toLowerCase();
    if (ext === 'txt') return 'primary';
    if (ext === 'pdf') return 'error';
    if (ext === 'doc' || ext === 'docx') return 'info';
    return 'default';
  };

  return (
    <Box sx={{ height: 'calc(100vh - 120px)', p: 2 }}>
      <Grid container spacing={2} sx={{ height: '100%' }}>
        {/* Left Panel - Upload & Chat */}
        <Grid item xs={12} md={6} sx={{ display: 'flex', flexDirection: 'column', gap: 2, height: '100%' }}>
          {/* Upload Section */}
          <Card sx={{ bgcolor: '#1e3a5f', color: 'white' }}>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 2 }}>
                <UploadIcon />
                <Typography variant="h6" sx={{ fontWeight: 600 }}>
                  Upload Intake Form
                </Typography>
              </Box>
              
              <Box
                sx={{
                  border: '2px dashed',
                  borderColor: selectedFile ? 'primary.light' : 'rgba(255,255,255,0.3)',
                  borderRadius: 2,
                  p: 4,
                  textAlign: 'center',
                  bgcolor: 'rgba(255,255,255,0.05)',
                  cursor: 'pointer',
                  transition: 'all 0.3s',
                  '&:hover': {
                    borderColor: 'primary.light',
                    bgcolor: 'rgba(255,255,255,0.1)',
                  },
                }}
                onClick={() => fileInputRef.current?.click()}
              >
                <input
                  ref={fileInputRef}
                  type="file"
                  hidden
                  accept=".txt,.pdf,.doc,.docx"
                  onChange={handleFileSelect}
                />
                <UploadIcon sx={{ fontSize: 48, mb: 2, opacity: 0.7 }} />
                <Typography variant="body1" sx={{ mb: 1 }}>
                  Drop file here or click to upload
                </Typography>
                <Typography variant="caption" sx={{ opacity: 0.8 }}>
                  Supports TXT, PDF, DOCX (max 10MB)
                </Typography>
              </Box>

              {selectedFile && (
                <Box sx={{ mt: 2, display: 'flex', gap: 1, flexWrap: 'wrap' }}>
                  <Chip
                    label={selectedFile.name}
                    color={getFileTypeColor(selectedFile.name)}
                    icon={<DocumentIcon />}
                    sx={{ mb: 1 }}
                  />
                  <Chip
                    label={getFileTypeLabel(selectedFile.name)}
                    color={getFileTypeColor(selectedFile.name)}
                    variant="outlined"
                    size="small"
                  />
                  <Button
                    variant="contained"
                    size="small"
                    onClick={handleFileUpload}
                    disabled={uploadStatus === 'uploading'}
                    startIcon={uploadStatus === 'uploading' ? <CircularProgress size={16} /> : <UploadIcon />}
                    sx={{ ml: 'auto' }}
                  >
                    {uploadStatus === 'uploading' ? 'Uploading...' : 'Upload'}
                  </Button>
                </Box>
              )}

              {uploadStatus === 'success' && (
                <Alert severity="success" sx={{ mt: 2 }}>
                  File uploaded successfully!
                </Alert>
              )}

              {uploadStatus === 'error' && (
                <Alert severity="error" sx={{ mt: 2 }}>
                  Upload failed. Please try again.
                </Alert>
              )}
            </CardContent>
          </Card>

          {/* Chat Section */}
          <Card sx={{ flex: 1, display: 'flex', flexDirection: 'column', bgcolor: '#1e3a5f', color: 'white' }}>
            <CardContent sx={{ flex: 1, display: 'flex', flexDirection: 'column', p: 0 }}>
              {/* Header */}
              <Box sx={{ p: 2, borderBottom: '1px solid rgba(255,255,255,0.1)' }}>
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                  <ChatIcon />
                  <Typography variant="h6" sx={{ fontWeight: 600 }}>
                    AI Legal Assistant
                  </Typography>
                </Box>
              </Box>

              {/* Messages */}
              <Box sx={{ flex: 1, overflow: 'auto', p: 2 }}>
                <List>
                  {messages.map((message) => (
                    <ListItem
                      key={message.id}
                      sx={{
                        flexDirection: message.sender === 'user' ? 'row-reverse' : 'row',
                        alignItems: 'flex-start',
                        mb: 1,
                      }}
                    >
                      <Avatar
                        sx={{
                          bgcolor: message.sender === 'user' ? 'primary.main' : 'secondary.main',
                          mr: message.sender === 'user' ? 0 : 1,
                          ml: message.sender === 'user' ? 1 : 0,
                          width: 32,
                          height: 32,
                        }}
                      >
                        {message.sender === 'user' ? 'U' : 'AI'}
                      </Avatar>
                      <Box sx={{ maxWidth: '75%' }}>
                        <Paper
                          sx={{
                            p: 1.5,
                            bgcolor: message.sender === 'user' ? 'primary.light' : 'rgba(255,255,255,0.1)',
                            color: 'white',
                          }}
                        >
                          <Typography variant="body2" sx={{ whiteSpace: 'pre-wrap' }}>
                            {message.text}
                          </Typography>
                        </Paper>
                        <Typography variant="caption" sx={{ color: 'rgba(255,255,255,0.6)', mt: 0.5, display: 'block' }}>
                          {message.timestamp}
                        </Typography>
                      </Box>
                    </ListItem>
                  ))}
                  {isLoading && (
                    <ListItem>
                      <Avatar sx={{ bgcolor: 'secondary.main', mr: 1, width: 32, height: 32 }}>
                        <CircularProgress size={16} color="inherit" />
                      </Avatar>
                      <Typography variant="body2" sx={{ color: 'rgba(255,255,255,0.7)' }}>
                        Thinking...
                      </Typography>
                    </ListItem>
                  )}
                  <div ref={messagesEndRef} />
                </List>
              </Box>

              {/* Input */}
              <Box
                component="form"
                onSubmit={handleSendMessage}
                sx={{
                  p: 2,
                  borderTop: '1px solid rgba(255,255,255,0.1)',
                }}
              >
                {error && (
                  <Alert severity="error" sx={{ mb: 1 }} onClose={() => setError(null)}>
                    {error}
                  </Alert>
                )}
                <Box sx={{ display: 'flex', gap: 1 }}>
                  <TextField
                    fullWidth
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    onKeyPress={handleKeyPress}
                    placeholder="Type your message... (Shift+Enter for new line)"
                    variant="outlined"
                    multiline
                    maxRows={3}
                    disabled={isLoading}
                    sx={{
                      '& .MuiOutlinedInput-root': {
                        bgcolor: 'rgba(255,255,255,0.1)',
                        color: 'white',
                        '& fieldset': {
                          borderColor: 'rgba(255,255,255,0.3)',
                        },
                        '&:hover fieldset': {
                          borderColor: 'rgba(255,255,255,0.5)',
                        },
                        '&.Mui-focused fieldset': {
                          borderColor: 'primary.light',
                        },
                      },
                      '& .MuiInputBase-input': {
                        color: 'white',
                        '&::placeholder': {
                          color: 'rgba(255,255,255,0.6)',
                        },
                      },
                    }}
                  />
                  <IconButton
                    type="submit"
                    color="primary"
                    disabled={!input.trim() || isLoading}
                    sx={{
                      bgcolor: 'primary.main',
                      color: 'white',
                      '&:hover': {
                        bgcolor: 'primary.dark',
                      },
                      '&:disabled': {
                        bgcolor: 'rgba(255,255,255,0.1)',
                      },
                    }}
                  >
                    <SendIcon />
                  </IconButton>
                </Box>
                <Typography variant="caption" sx={{ color: 'rgba(255,255,255,0.6)', mt: 1, display: 'block' }}>
                  Try: "Can you review this intake?" or "Generate a client engagement letter"
                </Typography>
              </Box>
            </CardContent>
          </Card>

          {/* Footer */}
          <Box sx={{ textAlign: 'center', py: 1 }}>
            <Typography variant="caption" sx={{ color: 'text.secondary' }}>
              SmartProBono © 2025 | Powered by AI
            </Typography>
            <Typography variant="caption" sx={{ color: 'text.secondary', display: 'block', mt: 0.5 }}>
              AI does not provide legal advice — all outputs require attorney review.
            </Typography>
          </Box>
        </Grid>

        {/* Right Panel - Generated Output */}
        <Grid item xs={12} md={6} sx={{ height: '100%' }}>
          <Card sx={{ height: '100%', bgcolor: '#1e3a5f', color: 'white', display: 'flex', flexDirection: 'column' }}>
            <CardContent sx={{ flex: 1, display: 'flex', flexDirection: 'column', p: 0 }}>
              {/* Header */}
              <Box sx={{ p: 2, borderBottom: '1px solid rgba(255,255,255,0.1)' }}>
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                  <DocumentIcon />
                  <Typography variant="h6" sx={{ fontWeight: 600 }}>
                    Generated Output
                  </Typography>
                </Box>
              </Box>

              {/* Content */}
              <Box sx={{ flex: 1, overflow: 'auto', p: 3 }}>
                {generatedOutput ? (
                  <Box>
                    <Typography variant="h6" gutterBottom sx={{ mb: 2 }}>
                      {generatedOutput.title}
                    </Typography>
                    <Paper
                      sx={{
                        p: 3,
                        bgcolor: 'rgba(255,255,255,0.05)',
                        border: '1px solid rgba(255,255,255,0.1)',
                        borderRadius: 2,
                      }}
                    >
                      <Typography
                        variant="body1"
                        sx={{
                          whiteSpace: 'pre-wrap',
                          color: 'white',
                          lineHeight: 1.8,
                        }}
                      >
                        {generatedOutput.content}
                      </Typography>
                    </Paper>
                    <Box sx={{ mt: 2, display: 'flex', gap: 1 }}>
                      <Button
                        variant="contained"
                        startIcon={<DocumentIcon />}
                        onClick={() => {
                          // Download as text file
                          const blob = new Blob([generatedOutput.content], { type: 'text/plain' });
                          const url = URL.createObjectURL(blob);
                          const a = document.createElement('a');
                          a.href = url;
                          a.download = `${generatedOutput.title.replace(/\s+/g, '_')}.txt`;
                          a.click();
                          URL.revokeObjectURL(url);
                        }}
                      >
                        Download
                      </Button>
                      <Button
                        variant="outlined"
                        onClick={() => setGeneratedOutput(null)}
                      >
                        Clear
                      </Button>
                    </Box>
                  </Box>
                ) : (
                  <Box
                    sx={{
                      display: 'flex',
                      flexDirection: 'column',
                      alignItems: 'center',
                      justifyContent: 'center',
                      height: '100%',
                      color: 'rgba(255,255,255,0.5)',
                    }}
                  >
                    <DocumentIcon sx={{ fontSize: 64, mb: 2, opacity: 0.3 }} />
                    <Typography variant="h6" gutterBottom>
                      No Output Yet
                    </Typography>
                    <Typography variant="body2" sx={{ textAlign: 'center', maxWidth: 300 }}>
                      Generated documents and summaries will appear here. Start by uploading a file or chatting with the AI assistant.
                    </Typography>
                  </Box>
                )}
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};

export default LegalAIAssistant;

