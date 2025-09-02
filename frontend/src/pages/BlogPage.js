import React from 'react';
import { Container, Typography, Box } from '@mui/material';
import PageLayout from '../components/PageLayout';

const BlogPage = () => (
  <PageLayout>
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Typography variant="h2" component="h1" gutterBottom sx={{ fontWeight: 'bold' }}>
        Blog
      </Typography>
      <Typography variant="body1" color="text.secondary">
        Read our latest articles and legal insights.
      </Typography>
    </Container>
  </PageLayout>
);

export default BlogPage;
