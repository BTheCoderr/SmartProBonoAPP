import React, { useState } from 'react';
import {
  Box,
  Typography,
  TextField,
  Button,
  Card,
  CardContent,
  Stack,
  Alert,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Divider,
  Chip,
} from '@mui/material';
import { PageLayout, Section } from '../design-system';
import PdfService from '../services/PdfService';

const SignatureDemoPage = () => {
  const [caseNumber, setCaseNumber] = useState('SPB-2025-0912');
  const [templateName, setTemplateName] = useState('default-intake-v1');
  const [clientSignatureType, setClientSignatureType] = useState('image');
  const [attorneySignatureType, setAttorneySignatureType] = useState('typed');
  const [attorneySignatureText, setAttorneySignatureText] = useState('A. Rivera, Esq.');
  const [bodyText, setBodyText] = useState('This document demonstrates auto-loaded signature placements.');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleGenerate = async () => {
    try {
      setLoading(true);
      setError(null);
      setResult(null);

      const input = {
        caseNumber,
        templateName,
        includeSignature: true,
        clientSignature: { type: clientSignatureType },
        attorneySignature: { 
          type: attorneySignatureType,
          text: attorneySignatureType === 'typed' ? attorneySignatureText : undefined
        },
        bodyText,
        clientName: 'John Doe',
        dateIssued: new Date().toLocaleDateString(),
        tableRows: [
          { cols: ['Document', 'Status', 'Notes'] },
          { cols: ['Contract', 'Generated', 'With auto-loaded signatures'] },
          { cols: ['Signatures', 'Applied', 'Client + Attorney'] },
        ]
      };

      const response = await PdfService.generatePdfWithTemplate(input);
      setResult(response);
    } catch (err) {
      console.error('Generation error:', err);
      setError(err.message || 'Failed to generate PDF');
    } finally {
      setLoading(false);
    }
  };

  return (
    <PageLayout>
      <Section>
        <Box sx={{ maxWidth: 800, mx: 'auto', p: 3 }}>
          <Typography variant="h4" gutterBottom sx={{ textAlign: 'center', mb: 4 }}>
            Signature Placement Demo
          </Typography>
          
          <Typography variant="body1" color="text.secondary" sx={{ textAlign: 'center', mb: 4 }}>
            Test the auto-loaded signature placement system. The system will automatically 
            load saved signature positions for the specified template, or use defaults if none exist.
          </Typography>

          {/* Configuration Form */}
          <Card sx={{ mb: 4 }}>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                PDF Generation Settings
              </Typography>
              
              <Stack spacing={3}>
                <Stack direction="row" spacing={2}>
                  <TextField
                    label="Case Number"
                    value={caseNumber}
                    onChange={(e) => setCaseNumber(e.target.value)}
                    fullWidth
                    size="small"
                  />
                  
                  <TextField
                    label="Template Name"
                    value={templateName}
                    onChange={(e) => setTemplateName(e.target.value)}
                    fullWidth
                    size="small"
                    helperText="Template to load signature placements from"
                  />
                </Stack>

                <TextField
                  label="Document Body Text"
                  value={bodyText}
                  onChange={(e) => setBodyText(e.target.value)}
                  fullWidth
                  multiline
                  rows={3}
                  size="small"
                />

                <Divider />

                <Typography variant="subtitle1" gutterBottom>
                  Signature Configuration
                </Typography>

                <Stack direction="row" spacing={2}>
                  <FormControl size="small" sx={{ minWidth: 150 }}>
                    <InputLabel>Client Signature</InputLabel>
                    <Select
                      value={clientSignatureType}
                      onChange={(e) => setClientSignatureType(e.target.value)}
                      label="Client Signature"
                    >
                      <MenuItem value="image">Image Signature</MenuItem>
                      <MenuItem value="typed">Typed Signature</MenuItem>
                    </Select>
                  </FormControl>

                  <FormControl size="small" sx={{ minWidth: 150 }}>
                    <InputLabel>Attorney Signature</InputLabel>
                    <Select
                      value={attorneySignatureType}
                      onChange={(e) => setAttorneySignatureType(e.target.value)}
                      label="Attorney Signature"
                    >
                      <MenuItem value="image">Image Signature</MenuItem>
                      <MenuItem value="typed">Typed Signature</MenuItem>
                    </Select>
                  </FormControl>
                </Stack>

                {attorneySignatureType === 'typed' && (
                  <TextField
                    label="Attorney Signature Text"
                    value={attorneySignatureText}
                    onChange={(e) => setAttorneySignatureText(e.target.value)}
                    fullWidth
                    size="small"
                    helperText="Text to use for typed attorney signature"
                  />
                )}

                <Button
                  variant="contained"
                  onClick={handleGenerate}
                  disabled={loading}
                  sx={{
                    backgroundColor: '#1565C0',
                    '&:hover': {
                      backgroundColor: '#0D47A1',
                    },
                  }}
                >
                  {loading ? 'Generating PDF...' : 'Generate PDF with Auto-Loaded Placements'}
                </Button>
              </Stack>
            </CardContent>
          </Card>

          {/* Error Display */}
          {error && (
            <Alert severity="error" sx={{ mb: 3 }}>
              {error}
            </Alert>
          )}

          {/* Results */}
          {result && (
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Generation Results
                </Typography>
                
                <Stack spacing={2}>
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                    <Chip 
                      label={result.usedPlacements} 
                      color={result.usedPlacements === 'auto-loaded' ? 'success' : 'default'}
                      size="small"
                    />
                    <Typography variant="body2" color="text.secondary">
                      Signature placements: {result.usedPlacements}
                    </Typography>
                  </Box>

                  <Box
                    component="pre"
                    sx={{
                      backgroundColor: '#f5f5f5',
                      p: 2,
                      borderRadius: 1,
                      overflow: 'auto',
                      fontSize: '0.875rem',
                      border: '1px solid #e0e0e0',
                    }}
                  >
                    {JSON.stringify(result, null, 2)}
                  </Box>

                  {result.signedUrl && (
                    <Box sx={{ textAlign: 'center' }}>
                      <Button
                        variant="contained"
                        href={result.signedUrl}
                        target="_blank"
                        sx={{
                          backgroundColor: '#1565C0',
                          '&:hover': {
                            backgroundColor: '#0D47A1',
                          },
                        }}
                      >
                        Open Generated PDF
                      </Button>
                    </Box>
                  )}
                </Stack>
              </CardContent>
            </Card>
          )}

          {/* Instructions */}
          <Card sx={{ mt: 4 }}>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                How It Works
              </Typography>
              
              <Stack spacing={2}>
                <Typography variant="body2">
                  <strong>1. Template-Based Placements:</strong> The system looks for saved signature placements 
                  using the template name. If found, it uses those exact coordinates.
                </Typography>
                
                <Typography variant="body2">
                  <strong>2. Fallback to Defaults:</strong> If no saved placements exist for the template, 
                  the system uses sensible default positions.
                </Typography>
                
                <Typography variant="body2">
                  <strong>3. Signature Types:</strong> Supports both image signatures (from signature capture) 
                  and typed signatures (text-based).
                </Typography>
                
                <Typography variant="body2">
                  <strong>4. Auto-Loading:</strong> No need to manually specify signature positions - 
                  the system automatically loads the best available placements.
                </Typography>
              </Stack>

              <Divider sx={{ my: 3 }} />

              <Typography variant="h6" gutterBottom>
                Next Steps
              </Typography>
              
              <Typography variant="body2" sx={{ mb: 2 }}>
                To create custom signature placements for your templates:
              </Typography>
              
              <Typography variant="body2">
                1. Go to the <strong>Signature Placement Editor</strong> page
              </Typography>
              <Typography variant="body2">
                2. Load a PDF and drag signature boxes to desired positions
              </Typography>
              <Typography variant="body2">
                3. Save the placements with a template name
              </Typography>
              <Typography variant="body2">
                4. Use that template name here to auto-load your custom placements
              </Typography>
            </CardContent>
          </Card>
        </Box>
      </Section>
    </PageLayout>
  );
};

export default SignatureDemoPage;
