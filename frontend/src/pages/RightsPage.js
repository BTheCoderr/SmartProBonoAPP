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
  Card,
  CardContent,
  Chip,
  Divider,
} from '@mui/material';
import PageLayout from '../components/PageLayout';
import GavelIcon from '@mui/icons-material/Gavel';
import SecurityIcon from '@mui/icons-material/Security';
import BusinessCenterIcon from '@mui/icons-material/BusinessCenter';
import HomeIcon from '@mui/icons-material/Home';
import HealthAndSafetyIcon from '@mui/icons-material/HealthAndSafety';
import AccountBalanceIcon from '@mui/icons-material/AccountBalance';
import config from '../config';

function RightsPage() {
  const [prompt, setPrompt] = useState('');
  const [loading, setLoading] = useState(false);
  const [messages, setMessages] = useState([]);
  const [error, setError] = useState(null);

  const rightCategories = [
    {
      title: 'Civil Rights',
      icon: <GavelIcon sx={{ fontSize: 40, color: '#1976d2' }} />,
      description: 'Fundamental rights and freedoms protected by law',
      examples: ['Freedom of speech', 'Equal protection', 'Due process'],
    },
    {
      title: 'Consumer Rights',
      icon: <SecurityIcon sx={{ fontSize: 40, color: '#2e7d32' }} />,
      description: 'Rights related to purchases and services',
      examples: ['Product safety', 'Fair pricing', 'Warranty claims'],
    },
    {
      title: 'Employment Rights',
      icon: <BusinessCenterIcon sx={{ fontSize: 40, color: '#ed6c02' }} />,
      description: 'Workplace protections and employee rights',
      examples: ['Fair wages', 'Safe workplace', 'Non-discrimination'],
    },
    {
      title: 'Housing Rights',
      icon: <HomeIcon sx={{ fontSize: 40, color: '#9c27b0' }} />,
      description: 'Tenant and property owner protections',
      examples: ['Fair housing', 'Tenant rights', 'Property rights'],
    },
    {
      title: 'Healthcare Rights',
      icon: <HealthAndSafetyIcon sx={{ fontSize: 40, color: '#d32f2f' }} />,
      description: 'Medical and healthcare related rights',
      examples: ['Patient privacy', 'Treatment access', 'Insurance coverage'],
    },
    {
      title: 'Constitutional Rights',
      icon: <AccountBalanceIcon sx={{ fontSize: 40, color: '#0288d1' }} />,
      description: 'Rights guaranteed by the Constitution',
      examples: ['Voting rights', 'Privacy rights', 'Religious freedom'],
    },
  ];

  const handleSubmit = async e => {
    e.preventDefault();
    setLoading(true);

    try {
      const response = await fetch(`${config.apiUrl}${config.endpoints.rights}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt: prompt.trim() }),
      });

      const data = await response.json();
      setMessages(prev => [
        ...prev,
        { type: 'user', text: prompt },
        { type: 'assistant', text: data.response, timing: data.timing },
      ]);
      setPrompt('');
    } catch (error) {
      setError('Failed to get response');
    } finally {
      setLoading(false);
    }
  };

  return (
    <PageLayout
      title="Know Your Rights"
      description="Learn about your legal rights and protections in various aspects of life"
    >
      {/* Categories Grid */}
      <Grid container spacing={4} sx={{ mb: 6 }}>
        {rightCategories.map((category, index) => (
          <Grid item xs={12} sm={6} md={4} key={index}>
            <Card
              sx={{
                height: '100%',
                transition: 'transform 0.2s',
                '&:hover': {
                  transform: 'translateY(-4px)',
                  boxShadow: 4,
                },
              }}
            >
              <CardContent sx={{ p: 3 }}>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                  {category.icon}
                  <Typography variant="h6" sx={{ ml: 1 }}>
                    {category.title}
                  </Typography>
                </Box>
                <Typography color="text.secondary" paragraph>
                  {category.description}
                </Typography>
                <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                  {category.examples.map((example, i) => (
                    <Chip key={i} label={example} size="small" variant="outlined" />
                  ))}
                </Box>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      {/* Chat Interface */}
      <Paper
        elevation={2}
        sx={{
          p: 3,
          bgcolor: 'rgba(255, 255, 255, 0.9)',
          backdropFilter: 'blur(8px)',
        }}
      >
        <Typography variant="h5" gutterBottom>
          Ask About Your Rights
        </Typography>

        <Box sx={{ mb: 3, maxHeight: '50vh', overflow: 'auto' }}>
          {messages.map((msg, index) => (
            <Paper
              key={index}
              sx={{
                p: 2,
                mb: 2,
                bgcolor: msg.type === 'user' ? '#e3f2fd' : '#fff',
                maxWidth: '80%',
                ml: msg.type === 'user' ? 'auto' : 0,
              }}
            >
              <Typography>{msg.text}</Typography>
              {msg.timing && (
                <Typography variant="caption" color="text.secondary">
                  Response time: {msg.timing.model_time}
                </Typography>
              )}
            </Paper>
          ))}
        </Box>

        {error && (
          <Alert severity="error" sx={{ mb: 2 }}>
            {error}
          </Alert>
        )}

        <Divider sx={{ my: 3 }} />

        <form onSubmit={handleSubmit}>
          <TextField
            fullWidth
            multiline
            rows={3}
            value={prompt}
            onChange={e => setPrompt(e.target.value)}
            placeholder="Ask about your legal rights..."
            sx={{
              mb: 2,
              '& .MuiOutlinedInput-root': {
                backgroundColor: 'white',
              },
            }}
          />
          <Button
            fullWidth
            variant="contained"
            type="submit"
            disabled={loading || !prompt.trim()}
            sx={{ py: 1.5 }}
          >
            {loading ? <CircularProgress size={24} /> : 'Ask Question'}
          </Button>
        </form>
      </Paper>

      <Alert severity="info" sx={{ mt: 4 }}>
        This information is for general guidance only. For specific legal advice, please consult
        with a qualified legal professional.
      </Alert>
    </PageLayout>
  );
}

export default RightsPage;
