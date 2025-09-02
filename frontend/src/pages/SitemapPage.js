import React from 'react';
import { Container, Typography, Box } from '@mui/material';
import PageLayout from '../components/PageLayout';

const SitemapPage = () => (
  <PageLayout>
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Typography variant="h2" component="h1" gutterBottom sx={{ fontWeight: 'bold' }}>
        Sitemap
      </Typography>
      <Typography variant="body1" color="text.secondary">
        Find all pages and sections of our website.
      </Typography>
    </Container>
  </PageLayout>
);

export default SitemapPage;
