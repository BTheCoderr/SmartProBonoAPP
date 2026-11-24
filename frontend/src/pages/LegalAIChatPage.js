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
            Legacy demo: availability and data handling have not been verified. Use fictional information only. For the current platform, visit smartprobono.org.
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