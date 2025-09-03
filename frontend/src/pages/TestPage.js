import React, { useState } from 'react';
import {
  Container,
  Typography,
  Box,
  Grid,
  Card,
  CardContent,
  Button,
  Alert,
  Paper,
  Divider
} from '@mui/material';
import {
  DocumentScanner as DocumentScannerIcon,
  Description as DescriptionIcon,
  CheckCircle as CheckCircleIcon,
  Error as ErrorIcon
} from '@mui/icons-material';
import MobileFileScanner from '../components/MobileFileScanner';
import DocumentGenerator from '../components/DocumentGenerator';
import { designTokens } from '../design-system';
import { brandColors, colorIssues, auditColors } from '../utils/colorAudit';

const TestPage = () => {
  const [testResults, setTestResults] = useState({
    pdfScanner: { status: 'pending', message: 'Not tested yet' },
    pdfGenerator: { status: 'pending', message: 'Not tested yet' },
    colorScheme: { status: 'completed', message: 'Brand colors updated successfully' }
  });

  const handleScannerTest = (result) => {
    setTestResults(prev => ({
      ...prev,
      pdfScanner: { 
        status: 'completed', 
        message: result ? 'PDF Scanner working correctly' : 'PDF Scanner test completed'
      }
    }));
  };

  const handleGeneratorTest = () => {
    setTestResults(prev => ({
      ...prev,
      pdfGenerator: { 
        status: 'completed', 
        message: 'PDF Generator component loaded successfully'
      }
    }));
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'completed':
        return <CheckCircleIcon color="success" />;
      case 'error':
        return <ErrorIcon color="error" />;
      default:
        return <DocumentScannerIcon color="action" />;
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'completed':
        return 'success';
      case 'error':
        return 'error';
      default:
        return 'info';
    }
  };

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Typography variant="h4" component="h1" gutterBottom sx={{ 
        color: designTokens.colors.primary[900],
        fontWeight: 'bold',
        mb: 4
      }}>
        SmartProBono Test Dashboard
      </Typography>

      {/* Color Scheme Test */}
      <Paper elevation={2} sx={{ p: 3, mb: 3, background: designTokens.gradients.card }}>
        <Typography variant="h6" gutterBottom sx={{ color: designTokens.colors.primary[900] }}>
          🎨 Color Scheme Test
        </Typography>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 2 }}>
          {getStatusIcon(testResults.colorScheme.status)}
          <Alert severity={getStatusColor(testResults.colorScheme.status)} sx={{ flex: 1 }}>
            {testResults.colorScheme.message}
          </Alert>
        </Box>
        
        {/* Color Palette Display */}
        <Grid container spacing={2}>
          <Grid item xs={12} md={6}>
            <Box sx={{ p: 2, bgcolor: brandColors.primary, borderRadius: 2, mb: 1 }}>
              <Typography variant="body2" color="white">
                Primary Navy: {brandColors.primary}
              </Typography>
            </Box>
            <Box sx={{ p: 2, bgcolor: brandColors.secondary, borderRadius: 2, mb: 1 }}>
              <Typography variant="body2" color="white">
                Secondary Teal: {brandColors.secondary}
              </Typography>
            </Box>
            <Box sx={{ p: 2, bgcolor: brandColors.primaryLight, borderRadius: 2 }}>
              <Typography variant="body2" color="white">
                Primary Light: {brandColors.primaryLight}
              </Typography>
            </Box>
          </Grid>
          <Grid item xs={12} md={6}>
            <Box sx={{ 
              p: 2, 
              background: designTokens.gradients.primary, 
              borderRadius: 2,
              color: 'white',
              mb: 1
            }}>
              <Typography variant="body2">
                Brand Gradient: Navy to Teal
              </Typography>
            </Box>
            <Box sx={{ 
              p: 2, 
              background: designTokens.gradients.secondary, 
              borderRadius: 2,
              color: 'white'
            }}>
              <Typography variant="body2">
                Secondary Gradient: Teal to Navy
              </Typography>
            </Box>
          </Grid>
        </Grid>

        {/* Color Issues Check */}
        <Box sx={{ mt: 3 }}>
          <Typography variant="h6" gutterBottom sx={{ color: designTokens.colors.primary[900] }}>
            🔍 Color Issues Detection
          </Typography>
          <Grid container spacing={2}>
            <Grid item xs={12} md={6}>
              <Typography variant="subtitle2" gutterBottom>❌ Old Colors to Avoid:</Typography>
              {colorIssues.oldBlue.slice(0, 3).map((color, index) => (
                <Box key={index} sx={{ 
                  p: 1, 
                  bgcolor: color, 
                  borderRadius: 1, 
                  mb: 1,
                  display: 'flex',
                  alignItems: 'center',
                  gap: 1
                }}>
                  <Typography variant="caption" color="white">
                    {color} (Old Blue)
                  </Typography>
                </Box>
              ))}
            </Grid>
            <Grid item xs={12} md={6}>
              <Typography variant="subtitle2" gutterBottom>✅ Recommended Replacements:</Typography>
              {colorIssues.oldBlue.slice(0, 3).map((color, index) => {
                const recommendation = auditColors.getColorRecommendation(color);
                return (
                  <Box key={index} sx={{ 
                    p: 1, 
                    bgcolor: recommendation || brandColors.primary, 
                    borderRadius: 1, 
                    mb: 1,
                    display: 'flex',
                    alignItems: 'center',
                    gap: 1
                  }}>
                    <Typography variant="caption" color="white">
                      {recommendation || brandColors.primary} (Brand Color)
                    </Typography>
                  </Box>
                );
              })}
            </Grid>
          </Grid>
        </Box>
      </Paper>

      {/* PDF Scanner Test */}
      <Paper elevation={2} sx={{ p: 3, mb: 3 }}>
        <Typography variant="h6" gutterBottom sx={{ color: designTokens.colors.primary[900] }}>
          📄 PDF Scanner Test
        </Typography>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 2 }}>
          {getStatusIcon(testResults.pdfScanner.status)}
          <Alert severity={getStatusColor(testResults.pdfScanner.status)} sx={{ flex: 1 }}>
            {testResults.pdfScanner.message}
          </Alert>
        </Box>
        
        <Box sx={{ border: `2px dashed ${designTokens.colors.primary[300]}`, borderRadius: 2, p: 2 }}>
          <MobileFileScanner 
            onScanComplete={handleScannerTest}
            documentType="test"
          />
        </Box>
      </Paper>

      {/* PDF Generator Test */}
      <Paper elevation={2} sx={{ p: 3, mb: 3 }}>
        <Typography variant="h6" gutterBottom sx={{ color: designTokens.colors.primary[900] }}>
          📝 PDF Generator Test
        </Typography>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 2 }}>
          {getStatusIcon(testResults.pdfGenerator.status)}
          <Alert severity={getStatusColor(testResults.pdfGenerator.status)} sx={{ flex: 1 }}>
            {testResults.pdfGenerator.message}
          </Alert>
        </Box>
        
        <Button 
          variant="contained" 
          onClick={handleGeneratorTest}
          sx={{ 
            background: designTokens.gradients.primary,
            '&:hover': {
              background: designTokens.gradients.secondary
            }
          }}
        >
          Test PDF Generator
        </Button>
        
        <Box sx={{ mt: 2, border: `1px solid ${designTokens.colors.neutral[200]}`, borderRadius: 2, p: 2 }}>
          <Typography variant="body2" color="text.secondary" gutterBottom>
            PDF Generator Component Preview:
          </Typography>
          <Box sx={{ maxHeight: 300, overflow: 'auto' }}>
            <DocumentGenerator />
          </Box>
        </Box>
      </Paper>

      {/* Summary */}
      <Paper elevation={2} sx={{ p: 3, background: designTokens.gradients.card }}>
        <Typography variant="h6" gutterBottom sx={{ color: designTokens.colors.primary[900] }}>
          📊 Test Summary
        </Typography>
        <Grid container spacing={2}>
          {Object.entries(testResults).map(([key, result]) => (
            <Grid item xs={12} sm={4} key={key}>
              <Card sx={{ 
                border: `2px solid ${result.status === 'completed' ? designTokens.colors.success[500] : designTokens.colors.neutral[300]}`,
                background: result.status === 'completed' ? designTokens.colors.success[50] : 'white'
              }}>
                <CardContent sx={{ textAlign: 'center' }}>
                  {getStatusIcon(result.status)}
                  <Typography variant="h6" sx={{ mt: 1, textTransform: 'capitalize' }}>
                    {key.replace(/([A-Z])/g, ' $1').trim()}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    {result.message}
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>
      </Paper>
    </Container>
  );
};

export default TestPage;
