import React from 'react';
import { Container, Typography } from '@mui/material';
import PageLayout from '../components/PageLayout';

const PartnersPage = () => (
  <PageLayout>
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Typography variant="h2" component="h1" gutterBottom sx={{ fontWeight: 'bold' }}>
        Partners
      </Typography>
      <Typography variant="body1" color="text.secondary">
        Our partners who help us make legal assistance accessible.
      </Typography>
    </Container>
  </PageLayout>
);

export default PartnersPage;
