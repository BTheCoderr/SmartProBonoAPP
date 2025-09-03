import React from 'react';
import { Container, Typography } from '@mui/material';
import PageLayout from '../components/PageLayout';

const TermsOfServicePage = () => (
  <PageLayout>
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Typography variant="h2" component="h1" gutterBottom sx={{ fontWeight: 'bold' }}>
        Terms of Service
      </Typography>
      <Typography variant="body1" color="text.secondary">
        This page contains our terms of service and user agreement.
      </Typography>
    </Container>
  </PageLayout>
);

export default TermsOfServicePage;
