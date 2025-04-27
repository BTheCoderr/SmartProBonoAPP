import React, { useState } from 'react';
import { Box, Typography, Container, Button } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import MobileFileScanner from '../components/MobileFileScanner';
import { useAuth } from '../context/AuthContext';

const ScannerTestPage = () => {
  const { currentUser, isAuthenticated, mockLogin } = useAuth();
  const navigate = useNavigate();
  const [scanResult, setScanResult] = useState(null);

  const handleScanComplete = (result) => {
    console.log('Scan completed:', result);
    setScanResult(result);
  };

  // Function to directly test scanner without auth
  const handleDirectTest = () => {
    // Force the page to show the scanner regardless of auth state
    document.getElementById('scanner-container').style.display = 'block';
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
              Authentication is currently bypassed for testing. Click the button below to test scanner directly:
            </Typography>
            <Button 
              variant="contained" 
              color="primary" 
              onClick={handleDirectTest}
              sx={{ mr: 2 }}
            >
              TEST SCANNER DIRECTLY
            </Button>
            <Button 
              variant="outlined" 
              color="secondary" 
              onClick={mockLogin}
              sx={{ mr: 2 }}
            >
              USE MOCK LOGIN (OPTIONAL)
            </Button>
          </Box>
        ) : (
          <Typography variant="body2" color="success.main" paragraph>
            Logged in as: {currentUser?.first_name} {currentUser?.last_name}
          </Typography>
        )}
        
        <Box id="scanner-container" sx={{ mt: 4, display: 'block' }}>
          <Typography variant="h5" gutterBottom>
            Document Scanner
          </Typography>
          <MobileFileScanner 
            onScanComplete={handleScanComplete}
            documentType="general"
          />
        </Box>
        
        {scanResult && (
          <Box sx={{ mt: 4, p: 2, bgcolor: '#f5f5f5', borderRadius: 1 }}>
            <Typography variant="h6" gutterBottom>
              Scan Results:
            </Typography>
            <pre style={{ overflow: 'auto', maxHeight: '200px' }}>
              {JSON.stringify(scanResult, null, 2)}
            </pre>
          </Box>
        )}
        
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