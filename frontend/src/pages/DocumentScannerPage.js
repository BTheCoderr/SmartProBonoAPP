import React, { useState } from 'react';
import {
  Container,
  Typography,
  Box,
  Grid,
  Card,
  CardContent,
  CardHeader,
  Button,
  Alert,
  CircularProgress,
  Paper,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Chip,
  Divider
} from '@mui/material';
import {
  CloudUpload as CloudUploadIcon,
  Scanner as ScannerIcon,
  Security as SecurityIcon,
  CheckCircle as CheckCircleIcon,
  Description as DescriptionIcon,
  AutoAwesome as AutoAwesomeIcon,
  Download as DownloadIcon
} from '@mui/icons-material';
import PageLayout from '../components/PageLayout';

const DocumentScannerPage = () => {
  const [isScanning, setIsScanning] = useState(false);
  const [uploadedFile, setUploadedFile] = useState(null);
  const [scanResults, setScanResults] = useState(null);

  const handleFileUpload = (event) => {
    const file = event.target.files[0];
    if (file) {
      setUploadedFile(file);
      setScanResults(null);
    }
  };

  const handleScanDocument = async () => {
    if (!uploadedFile) return;
    
    setIsScanning(true);
    // Simulate document scanning
    setTimeout(() => {
      setScanResults({
        documentType: 'Contract',
        confidence: 95,
        issues: [
          { type: 'warning', message: 'Missing signature line' },
          { type: 'info', message: 'Consider adding termination clause' }
        ],
        suggestions: [
          'Add force majeure clause',
          'Include dispute resolution section',
          'Specify governing law'
        ],
        extractedText: 'Sample extracted text from the document...'
      });
      setIsScanning(false);
    }, 3000);
  };

  const documentTypes = [
    { name: 'Contracts', icon: <DescriptionIcon />, count: '50+' },
    { name: 'Legal Forms', icon: <DescriptionIcon />, count: '100+' },
    { name: 'Court Documents', icon: <DescriptionIcon />, count: '25+' },
    { name: 'Business Agreements', icon: <DescriptionIcon />, count: '75+' }
  ];

  return (
    <PageLayout>
      <Container maxWidth="lg" sx={{ py: 4 }}>
        {/* Hero Section */}
        <Box sx={{ textAlign: 'center', mb: 6 }}>
          <Typography variant="h2" component="h1" gutterBottom sx={{ fontWeight: 'bold' }}>
            Document Scanner
          </Typography>
          <Typography variant="h5" color="text.secondary" sx={{ mb: 3 }}>
            AI-powered document analysis and legal review
          </Typography>
          <Alert severity="info" sx={{ maxWidth: 600, mx: 'auto' }}>
            <Typography variant="body2">
              <strong>Free to use!</strong> Upload any legal document for instant analysis, 
              issue detection, and improvement suggestions. No login required.
            </Typography>
          </Alert>
        </Box>

        {/* Features */}
        <Grid container spacing={3} sx={{ mb: 6 }}>
          <Grid item xs={12} md={4}>
            <Card sx={{ height: '100%', textAlign: 'center', p: 2 }}>
              <CardContent>
                <ScannerIcon sx={{ fontSize: 48, color: 'primary.main', mb: 2 }} />
                <Typography variant="h6" gutterBottom>
                  Smart Analysis
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Advanced AI analyzes your documents for legal issues and compliance
                </Typography>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} md={4}>
            <Card sx={{ height: '100%', textAlign: 'center', p: 2 }}>
              <CardContent>
                <SecurityIcon sx={{ fontSize: 48, color: 'success.main', mb: 2 }} />
                <Typography variant="h6" gutterBottom>
                  Secure Processing
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Your documents are processed securely and never stored permanently
                </Typography>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} md={4}>
            <Card sx={{ height: '100%', textAlign: 'center', p: 2 }}>
              <CardContent>
                <AutoAwesomeIcon sx={{ fontSize: 48, color: 'info.main', mb: 2 }} />
                <Typography variant="h6" gutterBottom>
                  Instant Results
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Get detailed analysis and recommendations in seconds
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        </Grid>

        <Grid container spacing={4}>
          {/* Upload Section */}
          <Grid item xs={12} md={6}>
            <Card>
              <CardHeader title="Upload Document" />
              <CardContent>
                <Paper
                  sx={{
                    p: 4,
                    textAlign: 'center',
                    border: '2px dashed',
                    borderColor: 'primary.main',
                    bgcolor: 'primary.light',
                    color: 'primary.contrastText',
                    cursor: 'pointer',
                    '&:hover': { bgcolor: 'primary.main' }
                  }}
                  onClick={() => document.getElementById('file-upload').click()}
                >
                  <CloudUploadIcon sx={{ fontSize: 64, mb: 2 }} />
                  <Typography variant="h6" gutterBottom>
                    Click to Upload Document
                  </Typography>
                  <Typography variant="body2">
                    PDF, DOC, DOCX files supported
                  </Typography>
                  <input
                    id="file-upload"
                    type="file"
                    accept=".pdf,.doc,.docx"
                    onChange={handleFileUpload}
                    style={{ display: 'none' }}
                  />
                </Paper>

                {uploadedFile && (
                  <Box sx={{ mt: 2 }}>
                    <Alert severity="success">
                      <Typography variant="body2">
                        <strong>File uploaded:</strong> {uploadedFile.name}
                      </Typography>
                    </Alert>
                    <Button
                      variant="contained"
                      startIcon={isScanning ? <CircularProgress size={20} /> : <ScannerIcon />}
                      onClick={handleScanDocument}
                      disabled={isScanning}
                      fullWidth
                      sx={{ mt: 2 }}
                      size="large"
                    >
                      {isScanning ? 'Scanning Document...' : 'Scan Document'}
                    </Button>
                  </Box>
                )}
              </CardContent>
            </Card>
          </Grid>

          {/* Results Section */}
          <Grid item xs={12} md={6}>
            <Card>
              <CardHeader title="Analysis Results" />
              <CardContent>
                {!scanResults ? (
                  <Box sx={{ textAlign: 'center', py: 4 }}>
                    <ScannerIcon sx={{ fontSize: 64, color: 'text.secondary', mb: 2 }} />
                    <Typography variant="h6" color="text.secondary">
                      Upload a document to see analysis results
                    </Typography>
                  </Box>
                ) : (
                  <Box>
                    <Alert severity="success" sx={{ mb: 3 }}>
                      <Typography variant="body2">
                        <strong>Document Type:</strong> {scanResults.documentType} 
                        <br />
                        <strong>Confidence:</strong> {scanResults.confidence}%
                      </Typography>
                    </Alert>

                    {scanResults.issues.length > 0 && (
                      <Box sx={{ mb: 3 }}>
                        <Typography variant="h6" gutterBottom>
                          Issues Found
                        </Typography>
                        <List dense>
                          {scanResults.issues.map((issue, index) => (
                            <ListItem key={index}>
                              <ListItemIcon>
                                <CheckCircleIcon color={issue.type === 'warning' ? 'warning' : 'info'} />
                              </ListItemIcon>
                              <ListItemText primary={issue.message} />
                            </ListItem>
                          ))}
                        </List>
                      </Box>
                    )}

                    {scanResults.suggestions.length > 0 && (
                      <Box sx={{ mb: 3 }}>
                        <Typography variant="h6" gutterBottom>
                          Suggestions
                        </Typography>
                        <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                          {scanResults.suggestions.map((suggestion, index) => (
                            <Chip
                              key={index}
                              label={suggestion}
                              color="primary"
                              variant="outlined"
                              size="small"
                            />
                          ))}
                        </Box>
                      </Box>
                    )}

                    <Button
                      variant="contained"
                      startIcon={<DownloadIcon />}
                      fullWidth
                    >
                      Download Analysis Report
                    </Button>
                  </Box>
                )}
              </CardContent>
            </Card>
          </Grid>
        </Grid>

        {/* Supported Document Types */}
        <Box sx={{ mt: 6 }}>
          <Typography variant="h4" gutterBottom sx={{ textAlign: 'center', mb: 4 }}>
            Supported Document Types
          </Typography>
          <Grid container spacing={3}>
            {documentTypes.map((type, index) => (
              <Grid item xs={12} sm={6} md={3} key={index}>
                <Card sx={{ textAlign: 'center', p: 2 }}>
                  <CardContent>
                    {type.icon}
                    <Typography variant="h6" gutterBottom>
                      {type.name}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      {type.count} templates
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
            ))}
          </Grid>
        </Box>

        {/* How it Works */}
        <Box sx={{ mt: 6 }}>
          <Typography variant="h4" gutterBottom sx={{ textAlign: 'center', mb: 4 }}>
            How Document Scanning Works
          </Typography>
          <Grid container spacing={3}>
            <Grid item xs={12} md={4}>
              <Box sx={{ textAlign: 'center' }}>
                <Box sx={{ 
                  width: 60, 
                  height: 60, 
                  borderRadius: '50%', 
                  bgcolor: 'primary.main', 
                  color: 'white',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  mx: 'auto',
                  mb: 2
                }}>
                  <Typography variant="h4" sx={{ fontWeight: 'bold' }}>1</Typography>
                </Box>
                <Typography variant="h6" gutterBottom>Upload Document</Typography>
                <Typography variant="body2" color="text.secondary">
                  Upload your legal document in PDF, DOC, or DOCX format
                </Typography>
              </Box>
            </Grid>
            <Grid item xs={12} md={4}>
              <Box sx={{ textAlign: 'center' }}>
                <Box sx={{ 
                  width: 60, 
                  height: 60, 
                  borderRadius: '50%', 
                  bgcolor: 'primary.main', 
                  color: 'white',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  mx: 'auto',
                  mb: 2
                }}>
                  <Typography variant="h4" sx={{ fontWeight: 'bold' }}>2</Typography>
                </Box>
                <Typography variant="h6" gutterBottom>AI Analysis</Typography>
                <Typography variant="body2" color="text.secondary">
                  Our AI analyzes the document for legal issues and compliance
                </Typography>
              </Box>
            </Grid>
            <Grid item xs={12} md={4}>
              <Box sx={{ textAlign: 'center' }}>
                <Box sx={{ 
                  width: 60, 
                  height: 60, 
                  borderRadius: '50%', 
                  bgcolor: 'primary.main', 
                  color: 'white',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  mx: 'auto',
                  mb: 2
                }}>
                  <Typography variant="h4" sx={{ fontWeight: 'bold' }}>3</Typography>
                </Box>
                <Typography variant="h6" gutterBottom>Get Results</Typography>
                <Typography variant="body2" color="text.secondary">
                  Receive detailed analysis, issues, and improvement suggestions
                </Typography>
              </Box>
            </Grid>
          </Grid>
        </Box>
      </Container>
    </PageLayout>
  );
};

export default DocumentScannerPage;
