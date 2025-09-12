import React, { useState } from 'react';
import { Container, Typography, Box, CircularProgress, Chip, Grid, Paper, Button } from '@mui/material';
import ImprovedLegalAIChat from '../components/ImprovedLegalAIChat';
import { useTranslation } from 'react-i18next';
import ComplianceIcon from '@mui/icons-material/VerifiedUser';
import BusinessIcon from '@mui/icons-material/Business';
import SecurityIcon from '@mui/icons-material/Security';
import { Card } from '../design-system';

const LegalAIChatPage = () => {
  const [loading, setLoading] = useState(false);
  const { t } = useTranslation();
  
  const handleStartChat = () => {
    setLoading(true);
    setTimeout(() => setLoading(false), 2000);
  };
  
  const complianceTopics = [
    { name: 'Immigration Law', color: 'primary', icon: '🛂', description: 'I-485, N-400, I-130 applications' },
    { name: 'Family Law', color: 'secondary', icon: '👨‍👩‍👧‍👦', description: 'Divorce, custody, support cases' },
    { name: 'Criminal Defense', color: 'success', icon: '⚖️', description: 'DUI, misdemeanor, felony cases' },
    { name: 'Personal Injury', color: 'warning', icon: '🏥', description: 'Car accidents, medical malpractice' },
    { name: 'Civil Rights', color: 'info', icon: '✊', description: 'Discrimination, employment issues' },
    { name: 'Business Law', color: 'error', icon: '🏢', description: 'Contracts, corporate matters' }
  ];

  const quickActions = [
    { title: 'Document Analysis', description: 'Upload and analyze legal documents', icon: '📄' },
    { title: 'Case Research', description: 'Research similar cases and precedents', icon: '🔍' },
    { title: 'Form Generation', description: 'Generate legal forms and applications', icon: '📝' },
    { title: 'Deadline Tracking', description: 'Track important legal deadlines', icon: '⏰' }
  ];
  
  return (
    <Container maxWidth="lg">
      <Box py={3}>
        <Card sx={{ p: 3, mb: 3 }}>
          <Typography variant="h6" gutterBottom>
            AI Assistant Status: {loading ? 'Processing...' : 'Ready'}
          </Typography>
          <Button variant="contained" onClick={handleStartChat} disabled={loading}>
            {loading ? 'Starting...' : 'Start Chat'}
          </Button>
        </Card>
        {/* Header Section */}
        <Box sx={{ textAlign: 'center', mb: 4 }}>
          <Typography variant="h3" component="h1" gutterBottom sx={{ fontWeight: 700, color: '#333' }}>
            {t('legalAI.title', 'AI Legal Compliance Assistant')}
          </Typography>
          {loading && <CircularProgress sx={{ mb: 2 }} />}
          <Typography variant="h6" color="text.secondary" paragraph sx={{ maxWidth: 800, mx: 'auto' }}>
            Get instant legal guidance, analyze documents, and connect with legal professionals. 
            Our AI-powered platform specializes in immigration, family law, criminal defense, and personal injury cases.
          </Typography>
          
          {/* Compliance Topics */}
          <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1, justifyContent: 'center', mb: 3 }}>
            {complianceTopics.map((topic, index) => (
              <Chip
                key={index}
                label={`${topic.icon} ${topic.name}`}
                color={topic.color}
                variant="outlined"
                sx={{ 
                  fontSize: '0.9rem',
                  '&:hover': { 
                    backgroundColor: `${topic.color}.50`,
                    cursor: 'pointer'
                  }
                }}
              />
            ))}
          </Box>
        </Box>

        {/* Quick Actions */}
        <Box sx={{ mb: 4 }}>
          <Typography variant="h5" gutterBottom align="center">
            Quick Actions
          </Typography>
          <Grid container spacing={2}>
            {quickActions.map((action, index) => (
              <Grid item xs={12} sm={6} md={3} key={index}>
                <Paper 
                  sx={{ 
                    p: 2, 
                    textAlign: 'center', 
                    height: '100%',
                    cursor: 'pointer',
                    '&:hover': { 
                      backgroundColor: 'primary.50',
                      transform: 'translateY(-2px)',
                      transition: 'all 0.2s'
                    }
                  }}
                >
                  <Typography variant="h4" sx={{ mb: 1 }}>
                    {action.icon}
                  </Typography>
                  <Typography variant="h6" gutterBottom>
                    {action.title}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    {action.description}
                  </Typography>
                </Paper>
              </Grid>
            ))}
          </Grid>
        </Box>

        {/* Features Grid */}
        <Grid container spacing={3} sx={{ mb: 4 }}>
          <Grid item xs={12} md={4}>
            <Paper sx={{ p: 3, textAlign: 'center', height: '100%' }}>
              <ComplianceIcon sx={{ fontSize: 48, color: 'primary.main', mb: 2 }} />
              <Typography variant="h6" gutterBottom>
                Compliance Scanner
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Analyze your current setup and identify compliance gaps automatically
              </Typography>
            </Paper>
          </Grid>
          <Grid item xs={12} md={4}>
            <Paper sx={{ p: 3, textAlign: 'center', height: '100%' }}>
              <BusinessIcon sx={{ fontSize: 48, color: 'secondary.main', mb: 2 }} />
              <Typography variant="h6" gutterBottom>
                Policy Generator
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Auto-generate privacy policies, terms of service, and legal documents
              </Typography>
            </Paper>
          </Grid>
          <Grid item xs={12} md={4}>
            <Paper sx={{ p: 3, textAlign: 'center', height: '100%' }}>
              <SecurityIcon sx={{ fontSize: 48, color: 'success.main', mb: 2 }} />
              <Typography variant="h6" gutterBottom>
                Risk Assessment
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Get real-time risk scores and actionable recommendations
              </Typography>
            </Paper>
          </Grid>
        </Grid>
        
        <Paper elevation={3} sx={{ p: 3 }}>
          {loading ? (
            <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
              <CircularProgress />
            </Box>
          ) : (
            <ImprovedLegalAIChat />
          )}
        </Paper>
      </Box>
    </Container>
  );
};

export default LegalAIChatPage; 