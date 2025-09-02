import React from 'react';
import { Container, Typography, Box } from '@mui/material';
import PageLayout from '../components/PageLayout';

const PressPage = () => (
  <PageLayout>
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Typography variant="h2" component="h1" gutterBottom sx={{ fontWeight: 'bold' }}>
        Press
      </Typography>
      <Typography variant="body1" color="text.secondary">
        Press releases and media coverage of SmartProBono.
      </Typography>
    </Container>
  </PageLayout>
);

export default PressPage;
