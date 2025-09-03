import React from 'react';
import { Container, Typography } from '@mui/material';
import PageLayout from '../components/PageLayout';

const PrivacyPolicyPage = () => (
  <PageLayout>
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Typography variant="h2" component="h1" gutterBottom sx={{ fontWeight: 'bold' }}>
        Privacy Policy
      </Typography>
      <Typography variant="body1" color="text.secondary">
        This page contains our privacy policy and data protection information.
      </Typography>
    </Container>
  </PageLayout>
);

export default PrivacyPolicyPage;
