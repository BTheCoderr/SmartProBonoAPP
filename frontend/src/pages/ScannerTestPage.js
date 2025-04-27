import React from 'react';
import { Box, Typography, Container, Button } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import MobileFileScanner from '../components/MobileFileScanner';
import { useAuth } from '../context/AuthContext';

const ScannerTestPage = () => {
  const { currentUser, isAuthenticated, mockLogin } = useAuth();
  const navigate = useNavigate();

  const handleScanComplete = (result) => {
    console.log('Scan completed:', result);
  };

  return (
    <Container maxWidth="md" sx={{ py: 4 }}>
      <Box sx={{ bgcolor: '#e3f2fd', p: 3, borderRadius: 2, mb: 3, border: '2px solid #1976d2' }}>
        <Typography variant="h4" gutterBottom color="primary">
          Scanner Test Page
        </Typography>
        
        <Typography variant="body1" paragraph>
          This is a dedicated test page for the document scanner functionality.
        </Typography>
        
        {!isAuthenticated ? (
          <Box sx={{ mb: 3 }}>
            <Typography variant="body2" color="error" paragraph>
              You are not logged in. Click the button below to use mock login:
            </Typography>
            <Button variant="contained" color="secondary" onClick={mockLogin}>
              USE MOCK LOGIN
            </Button>
          </Box>
        ) : (
          <Typography variant="body2" color="success.main" paragraph>
            Logged in as: {currentUser?.first_name} {currentUser?.last_name}
          </Typography>
        )}
        
        <Box sx={{ mt: 4 }}>
          <Typography variant="h5" gutterBottom>
            Document Scanner
          </Typography>
          <MobileFileScanner 
            onScanComplete={handleScanComplete}
            documentType="general"
          />
        </Box>
        
        <Box sx={{ mt: 3 }}>
          <Button 
            variant="outlined" 
            onClick={() => navigate('/')}
            sx={{ mr: 2 }}
          >
            Back to Home
          </Button>
        </Box>
      </Box>
    </Container>
  );
};

export default ScannerTestPage; 