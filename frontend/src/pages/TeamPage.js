import React from 'react';
import { Container, Typography, Box } from '@mui/material';
import PageLayout from '../components/PageLayout';

const TeamPage = () => (
  <PageLayout>
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Typography variant="h2" component="h1" gutterBottom sx={{ fontWeight: 'bold' }}>
        Our Team
      </Typography>
      <Typography variant="body1" color="text.secondary">
        Meet the people behind SmartProBono.
      </Typography>
    </Container>
  </PageLayout>
);

export default TeamPage;
