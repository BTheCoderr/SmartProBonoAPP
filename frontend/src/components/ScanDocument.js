import React, { useState, useEffect } from 'react';
import { Box, Typography, Container, Paper, Button, Card, CardContent, CircularProgress, FormControl, InputLabel, Select, MenuItem, Grid } from '@mui/material';
import MobileFileScanner from './MobileFileScanner';
import { useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { styled } from '@mui/system';
import { documentsApi } from '../services/api';
import JSONPretty from 'react-json-pretty';
import 'react-json-pretty/themes/monikai.css';

const ResultCard = styled(Paper)(({ theme }) => ({
  padding: theme.spacing(2),
  marginTop: theme.spacing(2),
  backgroundColor: '#f5f5f5',
  borderRadius: '8px',
  boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
  overflowX: 'auto'
}));

const ImagePreview = styled('img')({
  maxWidth: '100%',
  maxHeight: '300px',
  objectFit: 'contain',
  marginBottom: '16px',
  borderRadius: '4px',
  boxShadow: '0 2px 8px rgba(0,0,0,0.1)'
});

const ScanDocument = () => {
  const [scanResults, setScanResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [documentType, setDocumentType] = useState('general');
  const navigate = useNavigate();
  const location = useLocation();
  const { currentUser, isAuthenticated } = useAuth();
  
  // Get document type from query parameters or use default
  const queryParams = new URLSearchParams(location.search);
  const defaultDocumentType = queryParams.get('type') || 'general';

  // Debug log for component mount
  useEffect(() => {
    console.log('ScanDocument component mounted');
    console.log('Authentication status:', isAuthenticated);
    console.log('Current user:', currentUser);
  }, [isAuthenticated, currentUser]);
  
  const handleScanComplete = async (file) => {
    try {
      setLoading(true);
      setError(null);
      setScanResults(null);
      
      const results = await documentsApi.scanDocument(file, documentType);
      console.log('Scan results:', results);
      setScanResults(results);
    } catch (err) {
      console.error('Error during document scan:', err);
      setError(err.message || 'Failed to scan document');
    } finally {
      setLoading(false);
    }
  };
  
  const handleBack = () => {
    navigate(-1);
  };

  const handleDocumentTypeChange = (event) => {
    setDocumentType(event.target.value);
  };

  const formatDateTimeString = (timestamp) => {
    if (!timestamp) return '';
    const date = new Date(timestamp);
    return date.toLocaleString();
  };

  return (
    <Container maxWidth="md" sx={{ py: 4 }}>
      <Paper elevation={3} sx={{ p: 3, mb: 4, bgcolor: '#f9f9ff', border: '2px solid #1976d2' }}>
        <Typography variant="h4" component="h1" gutterBottom sx={{ color: '#1976d2', borderBottom: '2px solid #1976d2', pb: 2 }}>
          Document Scanner
        </Typography>

        {!isAuthenticated ? (
          <Box sx={{ p: 3, textAlign: 'center' }}>
            <Typography variant="h6" color="error" gutterBottom>
              Authentication Required
            </Typography>
            <Typography variant="body1" paragraph>
              Please log in to access the document scanner.
            </Typography>
            <Button 
              variant="contained" 
              onClick={() => navigate('/')}
            >
              Return to Home Page
            </Button>
          </Box>
        ) : (
          <>
            <Typography variant="body1" color="text.secondary" paragraph>
              Scan documents to extract information using OCR technology. 
              Supported document types: ID cards, immigration documents, legal documents, and general text documents.
            </Typography>
            
            <Typography variant="subtitle2" sx={{ mb: 2, color: 'green' }}>
              Logged in as: {currentUser?.first_name} {currentUser?.last_name}
            </Typography>
            
            <FormControl fullWidth margin="normal" variant="outlined">
              <InputLabel id="document-type-label">Document Type</InputLabel>
              <Select
                labelId="document-type-label"
                id="document-type"
                value={documentType}
                onChange={handleDocumentTypeChange}
                label="Document Type"
              >
                <MenuItem value="general">General Document</MenuItem>
                <MenuItem value="identification">ID Card/Driver's License</MenuItem>
                <MenuItem value="immigration">Immigration Document</MenuItem>
                <MenuItem value="legal">Legal Document</MenuItem>
              </Select>
            </FormControl>
            
            <MobileFileScanner onScanComplete={handleScanComplete} />
            
            {loading && (
              <Box display="flex" justifyContent="center" alignItems="center" my={4}>
                <CircularProgress />
                <Typography variant="body2" color="text.secondary" sx={{ ml: 2 }}>
                  Processing document...
                </Typography>
              </Box>
            )}
            
            {error && (
              <Box mt={2} p={2} bgcolor="error.light" borderRadius={1}>
                <Typography color="error" variant="body2">
                  Error: {error}
                </Typography>
              </Box>
            )}
            
            {scanResults && (
              <Box mt={3}>
                <Typography variant="h6" gutterBottom>
                  Scan Results
                </Typography>
                
                {scanResults.fileUrl && (
                  <Box textAlign="center" mb={2}>
                    <ImagePreview src={scanResults.fileUrl} alt="Scanned document" />
                  </Box>
                )}
                
                <Grid container spacing={2}>
                  <Grid item xs={12} md={6}>
                    <ResultCard elevation={0}>
                      <Typography variant="subtitle1" fontWeight="bold" gutterBottom>
                        Document Information
                      </Typography>
                      <Typography variant="body2" component="div">
                        <Box component="span" fontWeight="medium">Type:</Box> {scanResults.extractedData?.documentType || 'Unknown'}
                        {scanResults.extractedData?.documentClass && (
                          <Box mt={0.5}>
                            <Box component="span" fontWeight="medium">Class:</Box> {scanResults.extractedData.documentClass.replace(/_/g, ' ')}
                          </Box>
                        )}
                        {scanResults.confidence && (
                          <Box mt={0.5}>
                            <Box component="span" fontWeight="medium">Confidence:</Box> {(scanResults.confidence * 100).toFixed(1)}%
                          </Box>
                        )}
                        <Box mt={0.5}>
                          <Box component="span" fontWeight="medium">Processed:</Box> {formatDateTimeString(scanResults.processingTimestamp)}
                        </Box>
                        {scanResults.processingTimeMs && (
                          <Box mt={0.5}>
                            <Box component="span" fontWeight="medium">Processing Time:</Box> {scanResults.processingTimeMs}ms
                          </Box>
                        )}
                      </Typography>
                    </ResultCard>
                  </Grid>
                  
                  <Grid item xs={12} md={6}>
                    <ResultCard elevation={0}>
                      <Typography variant="subtitle1" fontWeight="bold" gutterBottom>
                        Extracted Text
                      </Typography>
                      <Box 
                        component="pre" 
                        sx={{ 
                          whiteSpace: 'pre-wrap',
                          wordBreak: 'break-word',
                          fontFamily: 'monospace',
                          fontSize: '0.875rem',
                          margin: 0,
                          padding: 0
                        }}
                      >
                        {scanResults.extractedText || 'No text extracted'}
                      </Box>
                    </ResultCard>
                  </Grid>
                  
                  <Grid item xs={12}>
                    <ResultCard elevation={0}>
                      <Typography variant="subtitle1" fontWeight="bold" gutterBottom>
                        Structured Data
                      </Typography>
                      <JSONPretty id="json-pretty" data={scanResults.extractedData || {}} />
                    </ResultCard>
                  </Grid>
                </Grid>
                
                <Box mt={3} display="flex" justifyContent="space-between">
                  <Button 
                    variant="outlined" 
                    color="primary"
                    onClick={() => setScanResults(null)}
                  >
                    New Scan
                  </Button>
                  
                  <Button 
                    variant="contained" 
                    color="primary"
                    disabled={!currentUser}
                  >
                    Save to My Documents
                  </Button>
                </Box>
              </Box>
            )}
          </>
        )}
        
        <Box sx={{ mt: 3 }}>
          <Button onClick={handleBack} variant="outlined">
            Back
          </Button>
        </Box>
      </Paper>
    </Container>
  );
};

export default ScanDocument; 