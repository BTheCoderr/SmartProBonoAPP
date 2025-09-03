import React, { useState, useEffect } from 'react';
import {
  Box,
  Container,
  Typography,
  Card,
  CardContent,
  TextField,
  Button,
  Alert,
  Chip,
  Stack,
  Grid,
} from '@mui/material';
import { Edit as EditIcon, CheckCircle as CheckCircleIcon } from '@mui/icons-material';
import SignatureCapture from '../components/SignatureCapture';
import PdfService from '../services/PdfService';

const SignaturePage = () => {
  const [caseNumber, setCaseNumber] = useState('SPB-2025-0912');
  const [hasSignature, setHasSignature] = useState(false);
  const [showSignatureCapture, setShowSignatureCapture] = useState(false);
  const [signatureUrl, setSignatureUrl] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Check if signature exists for the case
  useEffect(() => {
    const checkSignature = async () => {
      if (!caseNumber) return;
      
      setLoading(true);
      try {
        const exists = await PdfService.hasSignature(caseNumber);
        setHasSignature(exists);
        
        if (exists) {
          const url = await PdfService.getSignatureUrl(caseNumber);
          setSignatureUrl(url);
        } else {
          setSignatureUrl(null);
        }
      } catch (err) {
        setError(err.message || 'Error checking signature');
      } finally {
        setLoading(false);
      }
    };
    
    checkSignature();
  }, [caseNumber]);

  const handleSignatureUploaded = (path) => {
    setHasSignature(true);
    setShowSignatureCapture(false);
    setError(null);
    
    // Refresh signature URL
    PdfService.getSignatureUrl(caseNumber).then(url => {
      setSignatureUrl(url);
    });
  };

  const handleSignatureCleared = () => {
    setHasSignature(false);
    setSignatureUrl(null);
  };

  const handleCaseNumberChange = (event) => {
    setCaseNumber(event.target.value);
    setShowSignatureCapture(false);
  };

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Box sx={{ textAlign: 'center', mb: 4 }}>
        <Typography variant="h3" gutterBottom sx={{ fontWeight: 700, color: '#1565C0' }}>
          Digital Signature Management
        </Typography>
        <Typography variant="h6" color="text.secondary" sx={{ maxWidth: 600, mx: 'auto' }}>
          Capture, store, and manage digital signatures for your legal documents. 
          Signatures are securely stored and automatically added to generated PDFs.
        </Typography>
      </Box>

      <Grid container spacing={4}>
        {/* Case Number Input */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Case Information
              </Typography>
              
              <TextField
                fullWidth
                label="Case Number"
                value={caseNumber}
                onChange={handleCaseNumberChange}
                variant="outlined"
                sx={{ mb: 3 }}
                placeholder="e.g., SPB-2025-0912"
              />

              {/* Signature Status */}
              <Box sx={{ mb: 3 }}>
                <Typography variant="subtitle1" gutterBottom>
                  Signature Status:
                </Typography>
                
                {loading ? (
                  <Chip label="Checking..." color="default" />
                ) : hasSignature ? (
                  <Stack direction="row" spacing={1} alignItems="center">
                    <Chip 
                      label="Signature Available" 
                      color="success" 
                      icon={<CheckCircleIcon />}
                    />
                    {signatureUrl && (
                      <Button
                        size="small"
                        variant="outlined"
                        onClick={() => window.open(signatureUrl, '_blank')}
                        sx={{ ml: 1 }}
                      >
                        Preview
                      </Button>
                    )}
                  </Stack>
                ) : (
                  <Chip label="No Signature Found" color="default" />
                )}
              </Box>

              {/* Actions */}
              <Stack spacing={2}>
                <Button
                  variant="contained"
                  startIcon={<EditIcon />}
                  onClick={() => setShowSignatureCapture(!showSignatureCapture)}
                  fullWidth
                  sx={{
                    backgroundColor: '#1565C0',
                    '&:hover': {
                      backgroundColor: '#0D47A1',
                    },
                  }}
                >
                  {showSignatureCapture ? 'Hide Signature Capture' : 'Capture New Signature'}
                </Button>
              </Stack>
            </CardContent>
          </Card>
        </Grid>

        {/* Signature Capture */}
        <Grid item xs={12} md={6}>
          {showSignatureCapture ? (
            <SignatureCapture
              caseNumber={caseNumber}
              onUploaded={handleSignatureUploaded}
              onClear={handleSignatureCleared}
            />
          ) : (
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Signature Capture
                </Typography>
                <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
                  Click "Capture New Signature" to start the signature capture process.
                </Typography>
                
                <Box sx={{ 
                  border: '2px dashed #e0e0e0', 
                  borderRadius: 2, 
                  p: 4, 
                  textAlign: 'center',
                  backgroundColor: '#fafafa'
                }}>
                  <EditIcon sx={{ fontSize: 48, color: '#bdbdbd', mb: 2 }} />
                  <Typography variant="body2" color="text.secondary">
                    Signature capture area will appear here
                  </Typography>
                </Box>
              </CardContent>
            </Card>
          )}
        </Grid>
      </Grid>

      {/* Error Display */}
      {error && (
        <Alert severity="error" sx={{ mt: 3 }}>
          {error}
        </Alert>
      )}

      {/* Information Card */}
      <Card sx={{ mt: 4 }}>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            📋 How Digital Signatures Work
          </Typography>
          
          <Grid container spacing={3}>
            <Grid item xs={12} md={4}>
              <Typography variant="subtitle2" gutterBottom color="primary">
                1. Capture
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Use your finger, mouse, or stylus to sign in the capture area. 
                The signature is converted to a high-quality PNG image.
              </Typography>
            </Grid>
            
            <Grid item xs={12} md={4}>
              <Typography variant="subtitle2" gutterBottom color="primary">
                2. Store
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Your signature is securely stored in Supabase Storage with 
                case-based organization for easy retrieval.
              </Typography>
            </Grid>
            
            <Grid item xs={12} md={4}>
              <Typography variant="subtitle2" gutterBottom color="primary">
                3. Apply
              </Typography>
              <Typography variant="body2" color="text.secondary">
                When generating PDFs, signatures are automatically placed 
                in the designated signature area of the document.
              </Typography>
            </Grid>
          </Grid>
        </CardContent>
      </Card>
    </Container>
  );
};

export default SignaturePage;
