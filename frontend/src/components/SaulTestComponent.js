import React, { useState } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  TextField,
  Button,
  Chip,
  LinearProgress,
  Alert,
  Divider
} from '@mui/material';
import { SmartToy as SaulIcon, Send as SendIcon } from '@mui/icons-material';

const SaulTestComponent = () => {
  const [message, setMessage] = useState('');
  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [modelInfo, setModelInfo] = useState(null);

  const testSaulInfo = async () => {
    try {
      const res = await fetch('http://localhost:3001/api/v1/ai/saul/info');
      const data = await res.json();
      setModelInfo(data);
    } catch (err) {
      setError('Failed to get Saul model info');
    }
  };

  const sendMessage = async () => {
    if (!message.trim()) return;
    
    setLoading(true);
    setError(null);
    setResponse(null);

    try {
      const res = await fetch('http://localhost:3001/api/v1/ai/saul/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: message,
          task_type: 'legal',
          max_tokens: 200
        })
      });

      const data = await res.json();
      
      if (res.ok) {
        setResponse(data);
      } else {
        setError(data.error || 'Failed to get response');
      }
    } catch (err) {
      setError('Network error: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  const testEnhancedChat = async () => {
    setLoading(true);
    setError(null);
    setResponse(null);

    try {
      const res = await fetch('http://localhost:3001/api/v1/ai/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: 'What are my rights as a tenant?',
          task_type: 'legal',
          model: 'auto'
        })
      });

      const data = await res.json();
      
      if (res.ok) {
        setResponse(data);
      } else {
        setError(data.error || 'Failed to get response');
      }
    } catch (err) {
      setError('Network error: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box sx={{ maxWidth: 800, margin: '0 auto', p: 2 }}>
      <Card>
        <CardContent>
          <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
            <SaulIcon sx={{ mr: 1, color: 'primary.main' }} />
            <Typography variant="h5" component="h2">
              Saul Legal AI Test
            </Typography>
          </Box>

          <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
            Test the Saul-7B-Instruct-v1 legal language model integration
          </Typography>

          {/* Model Info Section */}
          <Box sx={{ mb: 3 }}>
            <Button 
              variant="outlined" 
              onClick={testSaulInfo}
              sx={{ mb: 2 }}
            >
              Get Saul Model Info
            </Button>
            
            {modelInfo && (
              <Card variant="outlined" sx={{ p: 2, bgcolor: 'grey.50' }}>
                <Typography variant="h6" gutterBottom>
                  Model Information
                </Typography>
                <Typography variant="body2">
                  <strong>Model:</strong> {modelInfo.model_info?.model_name}
                </Typography>
                <Typography variant="body2">
                  <strong>Device:</strong> {modelInfo.model_info?.device}
                </Typography>
                <Typography variant="body2">
                  <strong>Status:</strong> 
                  <Chip 
                    label={modelInfo.health_status?.status} 
                    color={modelInfo.health_status?.status === 'healthy' ? 'success' : 'warning'}
                    size="small"
                    sx={{ ml: 1 }}
                  />
                </Typography>
                <Typography variant="body2">
                  <strong>Company:</strong> {modelInfo.model_info?.company}
                </Typography>
              </Card>
            )}
          </Box>

          <Divider sx={{ my: 3 }} />

          {/* Direct Saul Chat */}
          <Box sx={{ mb: 3 }}>
            <Typography variant="h6" gutterBottom>
              Direct Saul Chat
            </Typography>
            
            <Box sx={{ display: 'flex', gap: 1, mb: 2 }}>
              <TextField
                fullWidth
                label="Ask Saul a legal question..."
                value={message}
                onChange={(e) => setMessage(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
                disabled={loading}
                placeholder="e.g., What is contract law?"
              />
              <Button
                variant="contained"
                onClick={sendMessage}
                disabled={loading || !message.trim()}
                startIcon={<SendIcon />}
              >
                Send
              </Button>
            </Box>
          </Box>

          {/* Enhanced Chat Test */}
          <Box sx={{ mb: 3 }}>
            <Typography variant="h6" gutterBottom>
              Enhanced AI Chat (Saul + Fallbacks)
            </Typography>
            <Button
              variant="contained"
              color="secondary"
              onClick={testEnhancedChat}
              disabled={loading}
              sx={{ mb: 2 }}
            >
              Test Enhanced Chat
            </Button>
          </Box>

          {/* Loading */}
          {loading && (
            <Box sx={{ mb: 2 }}>
              <LinearProgress />
              <Typography variant="body2" sx={{ mt: 1 }}>
                Processing with Saul Legal AI...
              </Typography>
            </Box>
          )}

          {/* Error */}
          {error && (
            <Alert severity="error" sx={{ mb: 2 }}>
              {error}
            </Alert>
          )}

          {/* Response */}
          {response && (
            <Card variant="outlined" sx={{ p: 2, bgcolor: 'primary.50' }}>
              <Typography variant="h6" gutterBottom>
                Saul Response
              </Typography>
              
              <Box sx={{ mb: 2 }}>
                <Chip 
                  label={`Model: ${response.model || 'Unknown'}`} 
                  size="small" 
                  sx={{ mr: 1 }}
                />
                {response.model_used && (
                  <Chip 
                    label={`Used: ${response.model_used}`} 
                    size="small" 
                    color="secondary"
                    sx={{ mr: 1 }}
                  />
                )}
                {response.fallback_used && (
                  <Chip 
                    label="Fallback Used" 
                    size="small" 
                    color="warning"
                  />
                )}
              </Box>

              <Typography variant="body1" sx={{ whiteSpace: 'pre-wrap' }}>
                {response.text || response.content || 'No response text'}
              </Typography>

              <Typography variant="caption" color="text.secondary" sx={{ mt: 2, display: 'block' }}>
                Response ID: {response.id} | Created: {response.created_at}
              </Typography>
            </Card>
          )}
        </CardContent>
      </Card>
    </Box>
  );
};

export default SaulTestComponent;
