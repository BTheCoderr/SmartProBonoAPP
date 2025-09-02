import React from 'react';
import { Container, Typography, Box } from '@mui/material';
import PageLayout from '../components/PageLayout';

const EducationalContentPage = () => (
  <PageLayout>
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Typography variant="h2" component="h1" gutterBottom sx={{ fontWeight: 'bold' }}>
        Educational Content
      </Typography>
      <Typography variant="body1" color="text.secondary">
        Learn about your legal rights and responsibilities.
      </Typography>
    </Container>
  </PageLayout>
);

export default EducationalContentPage;
