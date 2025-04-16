import React from 'react';
import { Container, Paper, Box } from '@mui/material';
import DocumentAnalyzer from '../components/DocumentAnalyzer';
import Navigation from '../components/Navigation';

const DocumentAnalyzerPage = () => {
  return (
    <Box>
      <Navigation />
      <Container maxWidth="lg" sx={{ mt: 4, mb: 8 }}>
        <Paper elevation={0} sx={{ p: { xs: 2, md: 4 } }}>
          <DocumentAnalyzer />
        </Paper>
      </Container>
    </Box>
  );
};

export default DocumentAnalyzerPage;
