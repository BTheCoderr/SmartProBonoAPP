import React from 'react';
import { Box, Typography, Button, Container } from '@mui/material';
import { styled } from '@mui/material/styles';
import TrustSignals from '../components/TrustSignals';

const LandingPage = () => {
  return (
    <Box sx={{ py: 8 }}>
      <Container maxWidth="lg">
        {/* Hero Section */}
        <Box sx={{ mb: 8, textAlign: 'center' }}>
          <Typography variant="h2" component="h1" gutterBottom>
            Legal Help Made Simple
            {/* Main heading with primary action */}
          </Typography>
          <Typography variant="h5" color="text.secondary" paragraph>
            Access legal tools, resources, and pro bono assistance all in one place.
          </Typography>
          <Button variant="contained" size="large" sx={{ mt: 2 }}>
            Get Started Now
          </Button>
        </Box>
      </Container>

      {/* Trust Signals */}
      <TrustSignals />

      {/* Rest of the landing page content */}
      // ... existing code ...
    </Box>
  );
};

export default LandingPage; 