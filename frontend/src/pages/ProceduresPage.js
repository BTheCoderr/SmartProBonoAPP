import React, { useState } from 'react';
import {
  TextField,
  Button,
  Paper,
  Box,
  Typography,
  CircularProgress,
  Alert,
  Grid,
} from '@mui/material';

function ProceduresPage() {
  const [prompt, setPrompt] = useState('');
  const [loading, setLoading] = useState(false);
  const [messages, setMessages] = useState([]);
  const [error, setError] = useState(null);

  const handleSubmit = async e => {
    e.preventDefault();
    setLoading(true);

    try {
      const response = await fetch('http://localhost:5000/api/legal/procedures', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt: prompt.trim() }),
      });

      const data = await response.json();
      setMessages(prev => [
        ...prev,
        { type: 'user', text: prompt },
        { type: 'assistant', text: data.response },
      ]);
      setPrompt('');
    } catch (error) {
      setError('Failed to get response');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Legal Procedures Information
      </Typography>

      <Grid container spacing={2}>
        <Grid item xs={12}>
          <Paper sx={{ p: 2, mb: 2 }}>
            <Typography variant="body1" gutterBottom>
              Ask questions about legal procedures and processes:
            </Typography>
            <ul>
              <li>Court procedures</li>
              <li>Filing documents</li>
              <li>Legal timelines</li>
              <li>Administrative processes</li>
            </ul>
          </Paper>
        </Grid>
      </Grid>

      <Box sx={{ mb: 3, maxHeight: '60vh', overflow: 'auto' }}>
        {messages.map((msg, index) => (
          <Paper
            key={index}
            sx={{ p: 2, mb: 2, bgcolor: msg.type === 'user' ? '#e3f2fd' : '#fff' }}
          >
            <Typography>{msg.text}</Typography>
          </Paper>
        ))}
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}

      <form onSubmit={handleSubmit}>
        <TextField
          fullWidth
          multiline
          rows={4}
          value={prompt}
          onChange={e => setPrompt(e.target.value)}
          placeholder="Ask about legal procedures..."
          sx={{ mb: 2 }}
        />
        <Button fullWidth variant="contained" type="submit" disabled={loading}>
          {loading ? <CircularProgress size={24} /> : 'Ask Question'}
        </Button>
      </form>
    </Box>
  );
}

export default ProceduresPage;
