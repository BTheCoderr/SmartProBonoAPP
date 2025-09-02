import React, { useState } from 'react';
import { 
  TextField, 
  Paper, 
  Box, 
  Typography, 
  CircularProgress, 
  Alert,
  Grid,
  Chip,
  Divider
} from '@mui/material';
import { PageLayout, Section, Button, Card, CardContent, designTokens } from '../design-system';
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
      icon: <GavelIcon sx={{ fontSize: 40, color: '#1565C0' }} />,
      description: 'Fundamental rights and freedoms protected by law',
      examples: ['Freedom of speech', 'Equal protection', 'Due process'],
      color: '#1565C0'
    },
    {
      title: 'Consumer Rights',
      icon: <SecurityIcon sx={{ fontSize: 40, color: '#14B8A6' }} />,
      description: 'Rights related to purchases and services',
      examples: ['Product safety', 'Fair pricing', 'Warranty claims'],
      color: '#14B8A6'
    },
    {
      title: 'Employment Rights',
      icon: <BusinessCenterIcon sx={{ fontSize: 40, color: '#1565C0' }} />,
      description: 'Workplace protections and employee rights',
      examples: ['Fair wages', 'Safe workplace', 'Non-discrimination'],
      color: '#1565C0'
    },
    {
      title: 'Housing Rights',
      icon: <HomeIcon sx={{ fontSize: 40, color: '#14B8A6' }} />,
      description: 'Tenant and property owner protections',
      examples: ['Fair housing', 'Tenant rights', 'Property rights'],
      color: '#14B8A6'
    },
    {
      title: 'Healthcare Rights',
      icon: <HealthAndSafetyIcon sx={{ fontSize: 40, color: '#1565C0' }} />,
      description: 'Medical and healthcare related rights',
      examples: ['Patient privacy', 'Treatment access', 'Insurance coverage'],
      color: '#1565C0'
    },
    {
      title: 'Constitutional Rights',
      icon: <AccountBalanceIcon sx={{ fontSize: 40, color: '#14B8A6' }} />,
      description: 'Rights guaranteed by the Constitution',
      examples: ['Voting rights', 'Privacy rights', 'Religious freedom'],
      color: '#14B8A6'
    }
  ];

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    
    try {
      const response = await fetch(`${config.apiUrl}${config.endpoints.rights}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt: prompt.trim() })
      });
      
      const data = await response.json();
      setMessages(prev => [...prev, 
        { type: 'user', text: prompt },
        { type: 'assistant', text: data.response, timing: data.timing }
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
      <Section>
        {/* Categories Grid */}
        <Grid container spacing={4} sx={{ mb: 6 }}>
          {rightCategories.map((category, index) => (
            <Grid item xs={12} sm={6} md={4} key={index}>
              <Card 
                sx={{ 
                  height: '100%',
                  transition: 'all 0.3s ease',
                  border: `2px solid transparent`,
                  '&:hover': {
                    transform: 'translateY(-8px)',
                    boxShadow: '0 12px 24px rgba(21, 101, 192, 0.15)',
                    border: `2px solid ${category.color}`,
                  }
                }}
              >
                <CardContent sx={{ p: designTokens.spacing[4] }}>
                  <Box sx={{ display: 'flex', alignItems: 'center', mb: designTokens.spacing[3] }}>
                    {category.icon}
                    <Typography 
                      variant="h6" 
                      sx={{ 
                        ml: designTokens.spacing[2],
                        fontWeight: designTokens.typography.fontWeight.semibold,
                        color: designTokens.colors.neutral[800]
                      }}
                    >
                      {category.title}
                    </Typography>
                  </Box>
                  <Typography 
                    color="text.secondary" 
                    paragraph
                    sx={{ 
                      mb: designTokens.spacing[3],
                      lineHeight: 1.6
                    }}
                  >
                    {category.description}
                  </Typography>
                  <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                    {category.examples.map((example, i) => (
                      <Chip 
                        key={i} 
                        label={example} 
                        size="small" 
                        variant="outlined"
                        sx={{
                          borderColor: category.color,
                          color: category.color,
                          '&:hover': {
                            backgroundColor: `${category.color}15`,
                            borderColor: category.color,
                          }
                        }}
                      />
                    ))}
                  </Box>
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>
      </Section>

      <Section>
        {/* Chat Interface */}
        <Card 
          elevation={2}
          sx={{ 
            p: designTokens.spacing[4],
            bgcolor: 'rgba(255, 255, 255, 0.95)',
            backdropFilter: 'blur(8px)',
            border: '1px solid rgba(21, 101, 192, 0.1)'
          }}
        >
          <Typography 
            variant="h5" 
            gutterBottom
            sx={{
              fontWeight: designTokens.typography.fontWeight.bold,
              color: designTokens.colors.neutral[800],
              mb: designTokens.spacing[4]
            }}
          >
            Ask About Your Rights
          </Typography>
          
          <Box sx={{ mb: designTokens.spacing[4], maxHeight: '50vh', overflow: 'auto' }}>
            {messages.map((msg, index) => (
              <Paper 
                key={index} 
                sx={{ 
                  p: designTokens.spacing[3], 
                  mb: designTokens.spacing[2], 
                  bgcolor: msg.type === 'user' ? 'rgba(21, 101, 192, 0.08)' : '#fff',
                  border: msg.type === 'user' ? '1px solid rgba(21, 101, 192, 0.2)' : '1px solid rgba(0, 0, 0, 0.1)',
                  maxWidth: '80%',
                  ml: msg.type === 'user' ? 'auto' : 0,
                  borderRadius: designTokens.borderRadius.lg
                }}
              >
                <Typography sx={{ lineHeight: 1.6 }}>{msg.text}</Typography>
                {msg.timing && (
                  <Typography 
                    variant="caption" 
                    color="text.secondary"
                    sx={{ display: 'block', mt: 1 }}
                  >
                    Response time: {msg.timing.model_time}
                  </Typography>
                )}
              </Paper>
            ))}
          </Box>

          {error && (
            <Alert 
              severity="error" 
              sx={{ 
                mb: designTokens.spacing[3],
                borderRadius: designTokens.borderRadius.md
              }}
            >
              {error}
            </Alert>
          )}

          <Divider sx={{ my: designTokens.spacing[4] }} />

          <form onSubmit={handleSubmit}>
            <TextField
              fullWidth
              multiline
              rows={3}
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              placeholder="Ask about your legal rights..."
              sx={{ 
                mb: designTokens.spacing[3],
                '& .MuiOutlinedInput-root': {
                  backgroundColor: 'white',
                  borderRadius: designTokens.borderRadius.md,
                  '&:hover .MuiOutlinedInput-notchedOutline': {
                    borderColor: '#1565C0',
                  },
                  '&.Mui-focused .MuiOutlinedInput-notchedOutline': {
                    borderColor: '#1565C0',
                    borderWidth: 2,
                  }
                }
              }}
            />
            <Button 
              fullWidth 
              variant="contained" 
              type="submit"
              disabled={loading || !prompt.trim()}
              sx={{ 
                py: designTokens.spacing[2],
                backgroundColor: '#1565C0',
                '&:hover': {
                  backgroundColor: '#0D47A1',
                },
                '&:disabled': {
                  backgroundColor: 'rgba(21, 101, 192, 0.3)',
                },
                borderRadius: designTokens.borderRadius.md,
                fontWeight: designTokens.typography.fontWeight.semibold
              }}
            >
              {loading ? <CircularProgress size={24} color="inherit" /> : "Ask Question"}
            </Button>
          </form>
        </Card>

        <Alert 
          severity="info" 
          sx={{ 
            mt: designTokens.spacing[4],
            borderRadius: designTokens.borderRadius.md,
            border: '1px solid rgba(21, 101, 192, 0.2)',
            backgroundColor: 'rgba(21, 101, 192, 0.05)'
          }}
        >
          This information is for general guidance only. For specific legal advice, please consult with a qualified legal professional.
        </Alert>
      </Section>
    </PageLayout>
  );
}

export default RightsPage;