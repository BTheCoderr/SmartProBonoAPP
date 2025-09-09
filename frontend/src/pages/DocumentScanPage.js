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
    name: 'Non-Disclosure-Agreement.pdf',
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
  
  const handleSampleSelect = async (sample) => {
    try {
      // Load the actual PDF file from the public directory
      const response = await fetch(`/sample-documents/${sample.name}`);
      if (!response.ok) {
        throw new Error('Failed to load sample document');
      }
      
      const blob = await response.blob();
      const file = new File([blob], sample.name, { type: 'application/pdf' });
      
      // Create document object with actual file data
      const document = {
        id: sample.id,
        name: sample.name,
        type: sample.type,
        description: sample.description,
        file: file,
        isSample: true
      };
      
      setSelectedDocument(document);
      handleNext();
    } catch (error) {
      console.error('Error loading sample document:', error);
      alert('Failed to load sample document. Please try uploading your own file.');
    }
  };
  
  const handleAnalysisComplete = (result) => {
    setAnalysisResult(result);
    // Don't auto-advance - let user manually proceed to review step
    // The results are already displayed in the DocumentScanner component
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
        {analysisResult && (
          <Box sx={{ mt: 3, textAlign: 'center' }}>
            <Button 
              variant="contained" 
              onClick={handleNext}
              size="large"
            >
              Proceed to Review
            </Button>
          </Box>
        )}
      </Box>
    );
  };
  
  // Step 3: Results Review
  const renderResultsReview = () => {
    return (
      <Box>
        <Paper sx={{ p: 3, mb: 3 }}>
          <Typography variant="h6" gutterBottom>
            Analysis Complete
          </Typography>
          <Typography variant="body1" paragraph>
            🎉 Great news! We've analyzed your document and given you the knowledge you need to handle it confidently.
          </Typography>
          
          {/* Summary of what happened */}
          <Box sx={{ bgcolor: 'success.50', p: 2, borderRadius: 1, mb: 3, border: '1px solid', borderColor: 'success.200' }}>
            <Typography variant="subtitle2" gutterBottom color="success.dark">
              🚀 What You Now Know:
            </Typography>
            <Typography variant="body2" paragraph>
              • You understand what type of document this is and who's involved
            </Typography>
            <Typography variant="body2" paragraph>
              • You know the key financial terms, dates, and legal language
            </Typography>
            <Typography variant="body2" paragraph>
              • You've identified any potential issues or concerns
            </Typography>
            <Typography variant="body2" paragraph>
              • You have specific action steps to protect your interests
            </Typography>
            <Typography variant="body2">
              • You're now equipped to make informed decisions about this document
            </Typography>
          </Box>

          <Typography variant="body1" paragraph>
            You now have the knowledge and tools to handle this document like a pro! Review the detailed analysis above to see exactly what you need to do next.
          </Typography>
          
          <Box sx={{ display: 'flex', gap: 2, justifyContent: 'center' }}>
            <Button variant="outlined" onClick={handleBack}>
              Back to Analysis
            </Button>
            <Button variant="contained" onClick={handleReset}>
              Analyze Another Document
            </Button>
          </Box>
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
        Take control of your legal documents! Our AI-powered scanner acts as your personal legal assistant, helping you understand complex terms, spot potential issues, and make informed decisions - all without needing a lawyer for every document.
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