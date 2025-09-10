import React, { useState } from 'react';
import {
  Box,
  Typography,
  Paper,
  Button,
  Alert,
  Chip,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  Divider,
  CircularProgress,
  Stepper,
  Step,
  StepLabel,
  Card,
  CardContent
} from '@mui/material';
import {
  Scanner as ScannerIcon,
  CheckCircle as CheckCircleIcon,
  Warning as WarningIcon,
  Info as InfoIcon,
  Security as SecurityIcon,
  Gavel as GavelIcon
} from '@mui/icons-material';

const EnhancedDocumentScanner = ({ document, onAnalysisComplete }) => {
  const [scanning, setScanning] = useState(false);
  const [scanResult, setScanResult] = useState(null);
  const [error, setError] = useState(null);
  const [activeStep, setActiveStep] = useState(0);

  const steps = ['Upload Document', 'AI Analysis', 'Safety Check', 'Review Results'];

  const scanDocument = async () => {
    if (!document?.file) {
      setError('Please select a document first');
      return;
    }

    setScanning(true);
    setError(null);
    setActiveStep(1);

    try {
      const formData = new FormData();
      formData.append('file', document.file);
      formData.append('document_type', document.type || 'generic');

      const response = await fetch('http://localhost:3001/api/v1/documents/analyze', {
        method: 'POST',
        body: formData,
      });

      const data = await response.json();
      setActiveStep(2);

      if (data.success) {
        const analysis = data.analysis;
        const result = {
          documentType: analysis.document_type || 'Unknown',
          confidence: analysis.confidence || 0,
          pages: analysis.pages || 1,
          words: analysis.words || 0,
          clientSummary: analysis.client_summary || '',
          parties: analysis.parties || [],
          keyDates: analysis.key_dates || [],
          monetaryAmounts: analysis.monetary_amounts || [],
          legalTerms: analysis.legal_terms || [],
          potentialIssues: analysis.potential_issues || [],
          recommendations: analysis.recommendations || [],
          actionItems: analysis.action_items || [],
          riskLevel: analysis.risk_level || 'medium',
          escalationNeeded: analysis.escalation_needed || false,
          safetyChecked: analysis.safety_checked || false,
          analysisTimestamp: analysis.analysis_timestamp
        };

        setScanResult(result);
        setActiveStep(3);
        
        if (onAnalysisComplete) {
          onAnalysisComplete(result);
        }
      } else {
        setError(data.error || 'Analysis failed');
        setActiveStep(0);
      }
    } catch (err) {
      setError('Failed to analyze document');
      setActiveStep(0);
      console.error('Error scanning document:', err);
    } finally {
      setScanning(false);
    }
  };

  const renderSafetyAlert = () => {
    if (!scanResult?.escalationNeeded) return null;

    return (
      <Alert 
        severity="warning" 
        icon={<SecurityIcon />}
        sx={{ mb: 3, bgcolor: 'warning.50', border: '1px solid', borderColor: 'warning.200' }}
      >
        <Typography variant="subtitle2" gutterBottom>
          <strong>Legal Disclaimer Required</strong>
        </Typography>
        <Typography variant="body2">
          This document contains complex legal matters that may require professional legal advice. 
          Our analysis is for informational purposes only and should not be considered legal advice.
        </Typography>
      </Alert>
    );
  };

  const renderAnalysisResults = () => {
    if (!scanResult) return null;

    return (
      <Box>
        {/* Safety Alert */}
        {renderSafetyAlert()}

        {/* Analysis Summary */}
        <Paper sx={{ p: 3, mb: 3, bgcolor: 'primary.50', border: '1px solid', borderColor: 'primary.200' }}>
          <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
            <ScannerIcon color="primary" sx={{ mr: 1 }} />
            <Typography variant="h6" color="primary">
              Enhanced Document Analysis
            </Typography>
            {scanResult.safetyChecked && (
              <Chip 
                icon={<SecurityIcon />} 
                label="Safety Checked" 
                color="success" 
                size="small" 
                sx={{ ml: 2 }}
              />
            )}
          </Box>

          <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap', mb: 2 }}>
            <Chip 
              icon={<InfoIcon />} 
              label={`Type: ${scanResult.documentType}`}
              color="primary"
              variant="outlined"
            />
            <Chip 
              icon={<InfoIcon />} 
              label={`Pages: ${scanResult.pages}`}
              color="info"
              variant="outlined"
            />
            <Chip 
              icon={<InfoIcon />} 
              label={`Words: ${scanResult.words}`}
              color="info"
              variant="outlined"
            />
            <Chip 
              icon={<CheckCircleIcon />} 
              label={`Confidence: ${Math.round(scanResult.confidence * 100)}%`}
              color={scanResult.confidence > 0.8 ? 'success' : scanResult.confidence > 0.6 ? 'warning' : 'error'}
            />
            <Chip 
              icon={<WarningIcon />} 
              label={`Risk: ${scanResult.riskLevel?.toUpperCase()}`}
              color={scanResult.riskLevel === 'high' ? 'error' : scanResult.riskLevel === 'low' ? 'success' : 'warning'}
            />
          </Box>
        </Paper>

        {/* Client Summary */}
        {scanResult.clientSummary && (
          <Paper elevation={2} sx={{ p: 3, mb: 3, bgcolor: 'success.50', border: '1px solid', borderColor: 'success.200' }}>
            <Typography variant="h6" gutterBottom color="success.dark" sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
              <InfoIcon />
              What This Document Means
            </Typography>
            <Typography variant="body1" sx={{ lineHeight: 1.6 }}>
              {scanResult.clientSummary}
            </Typography>
          </Paper>
        )}

        {/* Action Items */}
        {scanResult.actionItems && scanResult.actionItems.length > 0 && (
          <Paper elevation={2} sx={{ p: 3, mb: 3, bgcolor: 'warning.50', border: '1px solid', borderColor: 'warning.200' }}>
            <Typography variant="h6" gutterBottom color="warning.dark" sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
              <CheckCircleIcon />
              What You Should Do Next
            </Typography>
            <List dense>
              {scanResult.actionItems.map((item, index) => (
                <ListItem key={index} sx={{ py: 0.5 }}>
                  <ListItemIcon sx={{ minWidth: 32 }}>
                    <Typography variant="body2" color="warning.dark" fontWeight="bold">
                      {index + 1}.
                    </Typography>
                  </ListItemIcon>
                  <ListItemText
                    primary={item}
                    primaryTypographyProps={{ variant: 'body2' }}
                  />
                </ListItem>
              ))}
            </List>
          </Paper>
        )}

        {/* Safety Notice */}
        {scanResult.escalationNeeded && (
          <Card sx={{ bgcolor: 'error.50', border: '1px solid', borderColor: 'error.200' }}>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                <GavelIcon color="error" sx={{ mr: 1 }} />
                <Typography variant="h6" color="error">
                  Professional Legal Advice Recommended
                </Typography>
              </Box>
              <Typography variant="body2" color="error.dark">
                This document contains complex legal matters that may require the expertise of a qualified attorney. 
                Our analysis is for informational purposes only and should not be considered legal advice.
              </Typography>
            </CardContent>
          </Card>
        )}
      </Box>
    );
  };

  return (
    <Box>
      <Paper sx={{ p: 3, mb: 3 }}>
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
          <ScannerIcon color="primary" sx={{ mr: 1, fontSize: 32 }} />
          <Typography variant="h5">
            Enhanced Document Scanner
          </Typography>
        </Box>
        
        <Typography variant="body1" paragraph>
          Our AI-powered document scanner with built-in safety features and compliance checks will analyze your document 
          and provide you with comprehensive insights while ensuring legal compliance.
        </Typography>

        {/* Progress Stepper */}
        <Stepper activeStep={activeStep} sx={{ mb: 3 }}>
          {steps.map((label) => (
            <Step key={label}>
              <StepLabel>{label}</StepLabel>
            </Step>
          ))}
        </Stepper>

        {document && (
          <Box sx={{ mb: 2 }}>
            <Typography variant="subtitle2" gutterBottom>
              Selected Document:
            </Typography>
            <Typography variant="body2" color="text.secondary">
              {document.name}
            </Typography>
          </Box>
        )}

        <Button
          variant="contained"
          onClick={scanDocument}
          disabled={scanning || !document?.file}
          startIcon={scanning ? <CircularProgress size={20} /> : <ScannerIcon />}
          sx={{ mb: 3 }}
        >
          {scanning ? 'Analyzing with Safety Checks...' : 'Analyze Document Safely'}
        </Button>

        {error && (
          <Alert severity="error" sx={{ mb: 3 }}>
            {error}
          </Alert>
        )}

        {renderAnalysisResults()}
      </Paper>
    </Box>
  );
};

export default EnhancedDocumentScanner;
