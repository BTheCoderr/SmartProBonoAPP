import React from 'react';
import { Box, Container, Typography, Paper } from '@mui/material';
import SaulTestComponent from '../components/SaulTestComponent';

const SaulTestPage = () => {
  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          Saul Legal AI Integration Test
        </Typography>
        <Typography variant="body1" color="text.secondary" paragraph>
          Test the Saul-7B-Instruct-v1 legal language model integration with SmartProBono.
          This page allows you to interact directly with the Saul model and test its capabilities.
        </Typography>
        
        <Paper sx={{ p: 2, mb: 3, bgcolor: 'info.light', color: 'info.contrastText' }}>
          <Typography variant="body2">
            <strong>About Saul:</strong> Saul-7B-Instruct-v1 is a specialized legal language model 
            from Equall, trained on 30+ billion legal tokens. It's designed specifically for 
            legal text comprehension and generation.
          </Typography>
        </Paper>
      </Box>

      <SaulTestComponent />
    </Container>
  );
};

export default SaulTestPage;
