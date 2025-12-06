import React from 'react';
import { Box, Typography, Container } from '@mui/material';
import LegalAIAssistant from '../components/LegalAIAssistant';
import { useTranslation } from 'react-i18next';

const LegalAIChatPage = () => {
  const { t } = useTranslation();
  
  return (
    <Box sx={{ minHeight: '100vh', bgcolor: '#f5f5f5' }}>
      {/* Header Banner */}
      <Box sx={{ bgcolor: 'primary.main', color: 'white', py: 2, textAlign: 'center' }}>
        <Container maxWidth="lg">
          <Typography variant="h5" sx={{ fontWeight: 600, mb: 1 }}>
            Experience the power of AI-assisted legal document preparation.
          </Typography>
          <Typography variant="body2" sx={{ opacity: 0.9 }}>
            Demo Mode: This is a preview of SmartProBono. Your conversations and documents won't be saved. Sign up for full access →
          </Typography>
        </Container>
      </Box>

      {/* Main Content */}
      <Container maxWidth="xl" sx={{ py: 2 }}>
        <LegalAIAssistant />
      </Container>
    </Box>
  );
};

export default LegalAIChatPage; 