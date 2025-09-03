import React from 'react';
import { Container, Typography } from '@mui/material';
import PageLayout from '../components/PageLayout';

const AccessibilityPage = () => (
  <PageLayout>
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Typography variant="h2" component="h1" gutterBottom sx={{ fontWeight: 'bold' }}>
        Accessibility
      </Typography>
      <Typography variant="body1" color="text.secondary">
        Our commitment to making our platform accessible to everyone.
      </Typography>
    </Container>
  </PageLayout>
);

export default AccessibilityPage;
