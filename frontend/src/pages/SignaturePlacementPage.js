import React, { useState, useEffect } from 'react';
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
} from '@mui/material';
import { PageLayout, Section } from '../design-system';
import SignaturePlacementEditor from '../components/SignaturePlacementEditor';

const SignaturePlacementPage = () => {
  const [pdfUrl, setPdfUrl] = useState('/sample.pdf');
  const [templateName, setTemplateName] = useState('default-intake-v1');
  const [lastPlacements, setLastPlacements] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [savedPlacements, setSavedPlacements] = useState(null);

  // Load existing placements when template name changes
  useEffect(() => {
    const loadPlacements = async () => {
      if (!templateName) return;
      
      try {
        setLoading(true);
        setError(null);
        
        const response = await fetch(`/api/templates/placements?templateName=${encodeURIComponent(templateName)}`);
        const data = await response.json();
        
        if (data.ok && data.placements) {
          setSavedPlacements(data.placements);
        } else {
          setSavedPlacements(null);
        }
      } catch (err) {
        console.error('Error loading placements:', err);
        setError('Failed to load existing placements');
      } finally {
        setLoading(false);
      }
    };

    loadPlacements();
  }, [templateName]);

  const handlePlacementsSaved = (placements) => {
    setLastPlacements(placements);
    setSavedPlacements(placements);
  };

  const handleGenerateTestPdf = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const response = await fetch('/api/pdf/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          caseNumber: 'SPB-2025-TEST',
          templateName: templateName,
          includeSignature: true,
          clientSignature: { type: 'image' },
          attorneySignature: { type: 'typed', text: 'A. Rivera, Esq.' },
          bodyText: 'Test document with auto-loaded signature placements.',
        }),
      });
      
      const data = await response.json();
      
      if (data.ok && data.signedUrl) {
        // Update PDF URL to the generated one for testing
        setPdfUrl(data.signedUrl);
        setLastPlacements('Generated test PDF with saved placements');
      } else {
        throw new Error(data.error || 'Failed to generate test PDF');
      }
    } catch (err) {
      console.error('Error generating test PDF:', err);
      setError(err.message || 'Failed to generate test PDF');
    } finally {
      setLoading(false);
    }
  };

  return (
    <PageLayout>
      <Section>
        <Box sx={{ maxWidth: 1200, mx: 'auto', p: 3 }}>
          <Typography variant="h4" gutterBottom sx={{ textAlign: 'center', mb: 4 }}>
            Signature Placement Editor
          </Typography>
          
          <Typography variant="body1" color="text.secondary" sx={{ textAlign: 'center', mb: 4 }}>
            Design signature placement layouts for your contract templates. 
            Drag and resize signature boxes to position them exactly where you want.
          </Typography>

          {/* Configuration */}
          <Card sx={{ mb: 4 }}>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Configuration
              </Typography>
              
              <Stack direction="row" spacing={3} alignItems="center" sx={{ mb: 3 }}>
                <TextField
                  label="PDF URL"
                  value={pdfUrl}
                  onChange={(e) => setPdfUrl(e.target.value)}
                  fullWidth
                  size="small"
                  helperText="URL to the PDF you want to use for placement design"
                />
                
                <TextField
                  label="Template Name"
                  value={templateName}
                  onChange={(e) => setTemplateName(e.target.value)}
                  size="small"
                  sx={{ minWidth: 200 }}
                  helperText="Unique name for this template layout"
                />
              </Stack>

              <Stack direction="row" spacing={2}>
                <Button
                  variant="outlined"
                  onClick={handleGenerateTestPdf}
                  disabled={loading}
                  sx={{
                    borderColor: '#1565C0',
                    color: '#1565C0',
                    '&:hover': {
                      borderColor: '#0D47A1',
                      backgroundColor: 'rgba(21, 101, 192, 0.04)',
                    },
                  }}
                >
                  {loading ? 'Generating...' : 'Generate Test PDF'}
                </Button>
              </Stack>
            </CardContent>
          </Card>

          {error && (
            <Alert severity="error" sx={{ mb: 3 }}>
              {error}
            </Alert>
          )}

          {/* Signature Placement Editor */}
          <SignaturePlacementEditor
            pdfUrl={pdfUrl}
            templateName={templateName}
            initial={savedPlacements}
            onSave={handlePlacementsSaved}
          />

          {/* Results */}
          {lastPlacements && (
            <Card sx={{ mt: 4 }}>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Saved Placements
                </Typography>
                
                <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                  These coordinates will be automatically used when generating PDFs with this template.
                </Typography>

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
                  {JSON.stringify(lastPlacements, null, 2)}
                </Box>

                <Typography variant="caption" color="text.secondary" sx={{ mt: 2, display: 'block' }}>
                  Copy these coordinates into your PDF generation calls or let the system auto-load them by template name.
                </Typography>
              </CardContent>
            </Card>
          )}

          {/* Instructions */}
          <Card sx={{ mt: 4 }}>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                How to Use
              </Typography>
              
              <Stack spacing={2}>
                <Typography variant="body2">
                  <strong>1. Load a PDF:</strong> Enter a PDF URL or generate a test PDF to see the layout.
                </Typography>
                
                <Typography variant="body2">
                  <strong>2. Position Signatures:</strong> Drag the blue signature boxes to where you want signatures to appear.
                </Typography>
                
                <Typography variant="body2">
                  <strong>3. Resize:</strong> Use the bottom-right corner handle to resize signature areas.
                </Typography>
                
                <Typography variant="body2">
                  <strong>4. Save:</strong> Click "Save Placements" to store the coordinates for this template.
                </Typography>
                
                <Typography variant="body2">
                  <strong>5. Use in Generation:</strong> When generating PDFs, the system will automatically use these saved placements.
                </Typography>
              </Stack>

              <Divider sx={{ my: 3 }} />

              <Typography variant="h6" gutterBottom>
                Integration Example
              </Typography>
              
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
{`// Generate PDF with auto-loaded placements
await fetch('/api/pdf/generate', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    caseNumber: 'SPB-2025-0912',
    templateName: '${templateName}',
    includeSignature: true,
    clientSignature: { type: 'image' },
    attorneySignature: { type: 'typed', text: 'A. Rivera, Esq.' }
  })
});`}
              </Box>
            </CardContent>
          </Card>
        </Box>
      </Section>
    </PageLayout>
  );
};

export default SignaturePlacementPage;
