import React from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import {
  Container,
  Typography,
  Button,
  Box,
  Paper,
  Divider,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Card,
  CardContent,
  Alert,
  CircularProgress,
} from '@mui/material';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import DownloadIcon from '@mui/icons-material/Download';
import PictureAsPdfIcon from '@mui/icons-material/PictureAsPdf';
import DescriptionIcon from '@mui/icons-material/Description';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import EmailIcon from '@mui/icons-material/Email';
import ShareIcon from '@mui/icons-material/Share';
import PropTypes from 'prop-types';

/**
 * Document Success Page - Shown after successful document generation
 * Provides options to download the document in different formats
 */
const DocumentSuccessPage = () => {
  const { t } = useTranslation();
  const location = useLocation();
  const navigate = useNavigate();
  
  // Get document info from location state
  const documentId = location.state?.documentId;
  const templateId = location.state?.templateId;
  
  // If no document ID is provided, show error
  if (!documentId) {
    return (
      <Container maxWidth="md" sx={{ py: 4 }}>
        <Alert severity="error">
          {t('Document information not found. Please try generating your document again.')}
        </Alert>
        <Box mt={2}>
          <Button
            variant="contained"
            startIcon={<ArrowBackIcon />}
            onClick={() => navigate('/document-generator')}
          >
            {t('Back to Document Generator')}
          </Button>
        </Box>
      </Container>
    );
  }

  // Handle document download
  const handleDownload = (format = 'pdf') => {
    window.location.href = `/api/documents/download/${documentId}?format=${format}`;
  };

  // Handle email document
  const handleEmailDocument = () => {
    // In a real app, this would open a modal to enter email details
    alert('This feature would email the document to you or others');
  };

  return (
    <Container maxWidth="md" sx={{ py: 4 }}>
      <Paper elevation={3} sx={{ p: 4, borderRadius: 2 }}>
        <Box display="flex" alignItems="center" mb={3}>
          <CheckCircleIcon color="success" sx={{ fontSize: 40, mr: 2 }} />
          <Typography variant="h4" component="h1">
            {t('Document Successfully Generated')}
          </Typography>
        </Box>
        
        <Alert severity="success" sx={{ mb: 4 }}>
          {t('Your document has been successfully generated and is ready to download.')}
        </Alert>
        
        <Typography variant="h6" gutterBottom>
          {t('Download Options')}
        </Typography>
        
        <Card variant="outlined" sx={{ mb: 4 }}>
          <CardContent>
            <List>
              <ListItem
                button
                onClick={() => handleDownload('pdf')}
                sx={{
                  '&:hover': {
                    backgroundColor: 'rgba(0, 0, 0, 0.04)',
                  },
                }}
              >
                <ListItemIcon>
                  <PictureAsPdfIcon color="error" />
                </ListItemIcon>
                <ListItemText
                  primary={t('Download as PDF')}
                  secondary={t('Best for printing and sharing')}
                />
                <DownloadIcon color="primary" />
              </ListItem>
              
              <Divider />
              
              <ListItem
                button
                onClick={() => handleDownload('docx')}
                sx={{
                  '&:hover': {
                    backgroundColor: 'rgba(0, 0, 0, 0.04)',
                  },
                }}
              >
                <ListItemIcon>
                  <DescriptionIcon color="primary" />
                </ListItemIcon>
                <ListItemText
                  primary={t('Download as Word Document')}
                  secondary={t('Editable document format')}
                />
                <DownloadIcon color="primary" />
              </ListItem>
            </List>
          </CardContent>
        </Card>
        
        <Typography variant="h6" gutterBottom>
          {t('Share Options')}
        </Typography>
        
        <Box display="flex" gap={2} mb={4}>
          <Button
            variant="outlined"
            startIcon={<EmailIcon />}
            onClick={handleEmailDocument}
          >
            {t('Email Document')}
          </Button>
          
          <Button
            variant="outlined"
            startIcon={<ShareIcon />}
            onClick={() => alert('Share functionality would open here')}
          >
            {t('Share Document')}
          </Button>
        </Box>
        
        <Divider sx={{ my: 3 }} />
        
        <Box display="flex" justifyContent="space-between">
          <Button
            variant="outlined"
            startIcon={<ArrowBackIcon />}
            onClick={() => navigate('/document-generator')}
          >
            {t('Back to Document Generator')}
          </Button>
          
          <Button 
            variant="contained" 
            color="primary"
            onClick={() => navigate('/cases')}
          >
            {t('View My Cases')}
          </Button>
        </Box>
      </Paper>
    </Container>
  );
};

export default DocumentSuccessPage; 