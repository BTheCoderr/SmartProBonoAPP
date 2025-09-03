import React from 'react';
import { Container, Typography } from '@mui/material';
import PageLayout from '../components/PageLayout';

const OurMissionPage = () => (
  <PageLayout>
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Typography variant="h2" component="h1" gutterBottom sx={{ fontWeight: 'bold' }}>
        Our Mission
      </Typography>
      <Typography variant="body1" color="text.secondary">
        Learn about our mission to make legal help accessible to everyone.
      </Typography>
    </Container>
  </PageLayout>
);

export default OurMissionPage;
