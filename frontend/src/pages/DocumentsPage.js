import React from 'react';
import { Box, Container, Typography, Paper, Divider } from '@mui/material';
import PageLayout from '../components/PageLayout';
import DocumentUpload from '../components/DocumentUpload';

const DocumentsPage = () => {
  return (
    <PageLayout>
      <Container maxWidth="lg">
        <Paper sx={{ p: 3, mb: 4 }}>
          <Typography variant="h4" component="h1" gutterBottom>
            Document Management
          </Typography>
          <Typography variant="body1" paragraph>
            Upload, manage, and share your legal documents securely with SmartProBono.
            Our platform uses Cloudinary for reliable document storage and fast access.
          </Typography>
          <Divider sx={{ my: 3 }} />
          
          <Box sx={{ mb: 4 }}>
            <Typography variant="h5" gutterBottom>
              Upload Documents
            </Typography>
            <Typography variant="body1" paragraph>
              Select the appropriate category for your files to ensure they are stored correctly.
              All uploads are secure and only accessible to authorized users.
            </Typography>
            <DocumentUpload />
          </Box>
        </Paper>
      </Container>
    </PageLayout>
  );
};

export default DocumentsPage; 