import React from 'react';
import { Container, Typography } from '@mui/material';
import PageLayout from '../components/PageLayout';

const CareersPage = () => (
  <PageLayout>
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Typography variant="h2" component="h1" gutterBottom sx={{ fontWeight: 'bold' }}>
        Careers
      </Typography>
      <Typography variant="body1" color="text.secondary">
        Join our team and help make legal assistance accessible to everyone.
      </Typography>
    </Container>
  </PageLayout>
);

export default CareersPage;
