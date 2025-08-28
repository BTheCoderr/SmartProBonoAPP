import React, { useState } from 'react';
import { Container, Typography, Box, Paper, CircularProgress, Chip, Grid } from '@mui/material';
import ImprovedLegalAIChat from '../components/ImprovedLegalAIChat';
import { useTranslation } from 'react-i18next';
import ComplianceIcon from '@mui/icons-material/VerifiedUser';
import BusinessIcon from '@mui/icons-material/Business';
import SecurityIcon from '@mui/icons-material/Security';

const LegalAIChatPage = () => {
  const { t } = useTranslation();
  const [loading, setLoading] = useState(false);
  
  const complianceTopics = [
    { name: 'GDPR Compliance', color: 'primary', icon: '🛡️' },
    { name: 'SOC 2 Automation', color: 'secondary', icon: '🔒' },
    { name: 'Privacy Policies', color: 'success', icon: '📋' },
    { name: 'Terms of Service', color: 'warning', icon: '📄' },
    { name: 'Data Processing', color: 'info', icon: '⚙️' },
    { name: 'User Agreements', color: 'error', icon: '✍️' }
  ];
  
  return (
    <Container maxWidth="lg">
      <Box py={3}>
        {/* Header Section */}
        <Box sx={{ textAlign: 'center', mb: 4 }}>
          <Typography variant="h3" component="h1" gutterBottom sx={{ fontWeight: 700, color: '#333' }}>
            AI Legal Compliance Assistant
          </Typography>
          <Typography variant="h6" color="text.secondary" paragraph sx={{ maxWidth: 800, mx: 'auto' }}>
            Get instant compliance guidance, generate legal documents, and ensure your startup meets all regulatory requirements. 
            Our AI agents specialize in startup legal needs from GDPR to SOC 2.
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