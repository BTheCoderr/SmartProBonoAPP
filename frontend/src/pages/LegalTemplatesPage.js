import React from 'react';
import { Container, Typography } from '@mui/material';
import PageLayout from '../components/PageLayout';

const LegalTemplatesPage = () => (
  <PageLayout>
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Typography variant="h2" component="h1" gutterBottom sx={{ fontWeight: 'bold' }}>
        Legal Templates
      </Typography>
      <Typography variant="body1" color="text.secondary">
        Browse our collection of legal document templates.
      </Typography>
    </Container>
  </PageLayout>
);

export default LegalTemplatesPage;
