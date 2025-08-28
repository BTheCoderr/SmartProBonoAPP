import React, { useState } from 'react';
import { 
  Container, 
  Typography, 
  Paper, 
  Box, 
  Stepper, 
  Step, 
  StepLabel,
  Button,
  Divider,
  Grid,
  Card,
  CardActionArea,
  CardContent,
  CardMedia
} from '@mui/material';
import { styled } from '@mui/material/styles';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';
import DocumentScanner from '../components/documents/DocumentScanner';
import DocumentIcon from '@mui/icons-material/Description';
import ArticleIcon from '@mui/icons-material/Article';
import GavelIcon from '@mui/icons-material/Gavel';
import MenuBookIcon from '@mui/icons-material/MenuBook';

// Styled component for the file input
const VisuallyHiddenInput = styled('input')({
  clip: 'rect(0 0 0 0)',
  clipPath: 'inset(50%)',
  height: 1,
  overflow: 'hidden',
  position: 'absolute',
  bottom: 0,
  left: 0,
  whiteSpace: 'nowrap',
  width: 1,
});

// Sample documents for quick start
const sampleDocuments = [
  {
    id: 'contract1',
    name: 'Service Agreement.pdf',
    description: 'Standard service contract template',
    type: 'Contract',
    icon: <ArticleIcon fontSize="large" />
  },
  {
    id: 'lease1',
    name: 'Residential Lease.pdf',
    description: 'Apartment rental agreement',
    type: 'Lease',
    icon: <GavelIcon fontSize="large" />
  },
  {
    id: 'nda1',
    name: 'Non-Disclosure Agreement.pdf',
    description: 'Standard confidentiality agreement',
    type: 'NDA',
    icon: <MenuBookIcon fontSize="large" />
  }
];

const DocumentScanPage = () => {
  const [activeStep, setActiveStep] = useState(0);
  const [selectedDocument, setSelectedDocument] = useState(null);
  const [analysisResult, setAnalysisResult] = useState(null);
  
  const steps = ['Select Document', 'Analyze Document', 'Review Results'];
  
  const handleNext = () => {
    setActiveStep((prevActiveStep) => prevActiveStep + 1);
  };
  
  const handleBack = () => {
    setActiveStep((prevActiveStep) => prevActiveStep - 1);
  };
  
  const handleReset = () => {
    setActiveStep(0);
    setSelectedDocument(null);
    setAnalysisResult(null);
  };
  
  const handleFileUpload = (event) => {
    const file = event.target.files[0];
    if (file) {
      // Create document object from file
      const document = {
        id: 'upload-' + Date.now(),
        name: file.name,
        type: file.type.split('/')[1].toUpperCase(),
        size: file.size,
        file: file,
        isUpload: true
      };
      
      setSelectedDocument(document);
      handleNext();
    }
  };
  
  const handleSampleSelect = (sample) => {
    setSelectedDocument(sample);
    handleNext();
  };
  
  const handleAnalysisComplete = (result) => {
    setAnalysisResult(result);
    // Move to the next step automatically after analysis
    setTimeout(() => {
      handleNext();
    }, 1000);
  };
  
  // Step 1: Document Selection
  const renderDocumentSelection = () => {
    return (
      <Box>
        <Typography variant="h6" gutterBottom>
          Select Document to Analyze
        </Typography>
        
        <Box sx={{ display: 'flex', justifyContent: 'center', mb: 3 }}>
          <Button
            component="label"
            variant="contained"
            startIcon={<CloudUploadIcon />}
            sx={{ mt: 2 }}
          >
            Upload Document
            <VisuallyHiddenInput type="file" onChange={handleFileUpload} accept=".pdf,.doc,.docx,.txt" />
          </Button>
        </Box>
        
        <Divider sx={{ my: 4 }}>
          <Typography variant="body2" color="text.secondary">
            OR SELECT A SAMPLE DOCUMENT
          </Typography>
        </Divider>
        
        <Grid container spacing={3} sx={{ mt: 2 }}>
          {sampleDocuments.map((doc) => (
            <Grid item xs={12} sm={6} md={4} key={doc.id}>
              <Card 
                sx={{ 
                  height: '100%',
                  transition: 'transform 0.2s',
                  '&:hover': {
                    transform: 'translateY(-4px)',
                    boxShadow: 4
                  }
                }}
              >
                <CardActionArea onClick={() => handleSampleSelect(doc)} sx={{ height: '100%' }}>
                  <Box sx={{ bgcolor: 'primary.lighter', p: 2, display: 'flex', justifyContent: 'center' }}>
                    {doc.icon || <DocumentIcon fontSize="large" color="primary" />}
                  </Box>
                  <CardContent>
                    <Typography variant="h6" component="div" gutterBottom noWrap>
                      {doc.name}
                    </Typography>
                    <Typography variant="body2" color="text.secondary" paragraph>
                      {doc.description}
                    </Typography>
                    <Typography variant="caption" color="primary">
                      Sample {doc.type} Document
                    </Typography>
                  </CardContent>
                </CardActionArea>
              </Card>
            </Grid>
          ))}
        </Grid>
      </Box>
    );
  };
  
  // Step 2: Document Analysis
  const renderDocumentAnalysis = () => {
    return (
      <Box>
        <DocumentScanner 
          document={selectedDocument} 
          onAnalysisComplete={handleAnalysisComplete} 
        />
      </Box>
    );
  };
  
  // Step 3: Results Review (reuse the results already displayed in DocumentScanner)
  const renderResultsReview = () => {
    return (
      <Box>
        <Paper sx={{ p: 3, mb: 3 }}>
          <Typography variant="h6" gutterBottom>
            Analysis Complete
          </Typography>
          <Typography variant="body1" paragraph>
            The document analysis is complete. You can now review the detailed results or start a new analysis.
          </Typography>
          <Button variant="contained" onClick={handleReset}>
            Analyze Another Document
          </Button>
        </Paper>
      </Box>
    );
  };
  
  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 8 }}>
      <Typography variant="h4" component="h1" gutterBottom>
        Document Analysis
      </Typography>
      <Typography variant="body1" paragraph color="text.secondary">
        Our AI-powered document scanner helps you quickly understand key terms, identify potential issues, and get recommendations for legal documents.
      </Typography>
      
      <Paper sx={{ p: 3, mb: 4 }}>
        <Stepper activeStep={activeStep} sx={{ mb: 4 }}>
          {steps.map((label) => (
            <Step key={label}>
              <StepLabel>{label}</StepLabel>
            </Step>
          ))}
        </Stepper>
        
        {activeStep === 0 && renderDocumentSelection()}
        {activeStep === 1 && renderDocumentAnalysis()}
        {activeStep === 2 && renderResultsReview()}
        
        <Box sx={{ display: 'flex', justifyContent: 'space-between', mt: 4 }}>
          <Button 
            variant="outlined"
            disabled={activeStep === 0}
            onClick={handleBack}
          >
            Back
          </Button>
          
          {activeStep !== 1 && (
            <Button
              variant="contained"
              disabled={activeStep === 0 && !selectedDocument}
              onClick={handleNext}
            >
              {activeStep === steps.length - 1 ? 'Finish' : 'Next'}
            </Button>
          )}
        </Box>
      </Paper>
    </Container>
  );
};

export default DocumentScanPage; 