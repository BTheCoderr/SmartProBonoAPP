import React, { useState } from 'react';
import { Box, Card, CardContent, CardHeader, Typography, Divider, Link, Grid, Paper } from '@mui/material';
import FileUpload from './FileUpload';

const DocumentUpload = () => {
  const [uploadedDocument, setUploadedDocument] = useState(null);
  const [uploadedTemplate, setUploadedTemplate] = useState(null);
  const [uploadedUserFile, setUploadedUserFile] = useState(null);

  const handleDocumentUpload = (fileData) => {
    console.log('Document uploaded:', fileData);
    setUploadedDocument(fileData);
  };

  const handleTemplateUpload = (fileData) => {
    console.log('Template uploaded:', fileData);
    setUploadedTemplate(fileData);
  };

  const handleUserFileUpload = (fileData) => {
    console.log('User file uploaded:', fileData);
    setUploadedUserFile(fileData);
  };

  const renderUploadedFile = (fileData, title) => {
    if (!fileData) return null;

    return (
      <Paper elevation={2} sx={{ p: 2, mb: 2, bgcolor: 'background.paper' }}>
        <Typography variant="subtitle1" fontWeight="bold">{title}</Typography>
        <Typography variant="body2">File name: {fileData.original_filename}</Typography>
        <Typography variant="body2">Size: {Math.round(fileData.bytes / 1024)} KB</Typography>
        <Typography variant="body2">Type: {fileData.format || 'Document'}</Typography>
        <Typography variant="body2">
          URL: <Link href={fileData.secure_url} target="_blank" rel="noopener">{fileData.secure_url}</Link>
        </Typography>

        {fileData.resource_type === 'image' && (
          <Box sx={{ mt: 2, textAlign: 'center' }}>
            <img 
              src={fileData.secure_url} 
              alt={fileData.original_filename}
              style={{ maxWidth: '100%', maxHeight: '200px' }}
            />
          </Box>
        )}
      </Paper>
    );
  };

  return (
    <Card>
      <CardHeader title="Document Upload" />
      <Divider />
      <CardContent>
        <Grid container spacing={3}>
          <Grid item xs={12} md={4}>
            <Box>
              <Typography variant="h6">Case Documents</Typography>
              <Typography variant="body2" color="text.secondary" paragraph>
                Upload documents related to legal cases.
                Supported formats: PDF, DOC, DOCX
              </Typography>
              <FileUpload 
                onUploadComplete={handleDocumentUpload}
                uploadType="document" 
                buttonText="Select Case Document"
                allowedFormats={['pdf', 'doc', 'docx']}
              />
              {renderUploadedFile(uploadedDocument, 'Uploaded Case Document')}
            </Box>
          </Grid>

          <Grid item xs={12} md={4}>
            <Box>
              <Typography variant="h6">Document Templates</Typography>
              <Typography variant="body2" color="text.secondary" paragraph>
                Upload document templates for generating legal documents.
                Supported formats: DOC, DOCX, TXT, HTML
              </Typography>
              <FileUpload 
                onUploadComplete={handleTemplateUpload}
                uploadType="template" 
                buttonText="Select Template"
                allowedFormats={['doc', 'docx', 'txt', 'html']}
              />
              {renderUploadedFile(uploadedTemplate, 'Uploaded Template')}
            </Box>
          </Grid>

          <Grid item xs={12} md={4}>
            <Box>
              <Typography variant="h6">User Files</Typography>
              <Typography variant="body2" color="text.secondary" paragraph>
                Upload general files and images.
                Supported formats: PDF, DOC, DOCX, JPG, JPEG, PNG
              </Typography>
              <FileUpload 
                onUploadComplete={handleUserFileUpload}
                uploadType="user" 
                buttonText="Select File"
                allowedFormats={['pdf', 'doc', 'docx', 'jpg', 'jpeg', 'png']}
              />
              {renderUploadedFile(uploadedUserFile, 'Uploaded User File')}
            </Box>
          </Grid>
        </Grid>
      </CardContent>
    </Card>
  );
};

export default DocumentUpload; 