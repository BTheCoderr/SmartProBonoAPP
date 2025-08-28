import React from 'react';
import { Box, Container, Typography, Paper } from '@mui/material';
import LegalAIChat from '../components/LegalAIChat';

const LegalChatPage = () => {
  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Paper elevation={3} sx={{ p: 3 }}>
        <Typography variant="h4" gutterBottom>
          Legal AI Assistant
        </Typography>
        <Typography variant="body1" paragraph>
          Ask our AI assistant any legal question. We're here to help with understanding legal concepts, processes, and forms.
        </Typography>
        <Box sx={{ mt: 3 }}>
          <LegalAIChat />
        </Box>
      </Paper>
    </Container>
  );
};

export default LegalChatPage; 