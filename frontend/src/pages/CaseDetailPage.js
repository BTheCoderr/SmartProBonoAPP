import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
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
  Chip,
  Grid,
  Paper,
} from '@mui/material';
import { 
  PageLayout, 
  Section, 
  designTokens 
} from '../design-system';
import { 
  GetApp as DownloadIcon,
  ArrowBack as BackIcon,
} from '@mui/icons-material';

const CaseDetailPage = () => {
  const { caseNumber } = useParams();
  const navigate = useNavigate();
  const [templates, setTemplates] = useState([]);
  const [templateName, setTemplateName] = useState('');
  const [busy, setBusy] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);

  const loadTemplates = async () => {
    try {
      const res = await fetch('/api/templates/list');
      const json = await res.json();
      if (json?.items) {
        setTemplates(json.items);
        if (json.items.length > 0) {
          setTemplateName(json.items[0].template_name);
        }
      }
    } catch (err) {
      console.error('Error loading templates:', err);
      setError('Failed to load templates');
    }
  };

  useEffect(() => {
    loadTemplates();
  }, []);

  const handleGenerate = async () => {
    try {
      setBusy(true);
      setError(null);
      setResult(null);
      setSuccess(null);

      const payload = {
        caseNumber,
        templateName,
        includeSignature: true,
        clientSignature: { type: 'image' },
        attorneySignature: { type: 'typed', text: 'Attorney Name, Esq.' },
        bodyText: 'Generated for case ' + caseNumber,
        tableRows: [
          { cols: ['Document', 'Status', 'Notes'] },
          { cols: ['Case File', 'Generated', 'Case ' + caseNumber] },
          { cols: ['Template', 'Applied', templateName] },
        ],
      };

      const res = await fetch('/api/pdf/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });
      
      const json = await res.json();
      setResult(json);
      
      if (!res.ok) {
        throw new Error(json?.error || 'Generate failed');
      }

      setSuccess('PDF generated successfully!');
      setTimeout(() => setSuccess(null), 5000);
    } catch (e) {
      console.error('Generate error:', e);
      setError(e?.message || 'Generate failed');
    } finally {
      setBusy(false);
    }
  };

  return (
    <PageLayout>
      <Section>
        <Box sx={{ 
          maxWidth: 800, 
          mx: 'auto', 
          p: 3,
          backgroundColor: designTokens.colors.background,
          borderRadius: designTokens.borderRadius.medium
        }}>
          <Stack direction="row" alignItems="center" spacing={2} sx={{ mb: 4 }}>
            <Button
              startIcon={<BackIcon />}
              onClick={() => navigate(-1)}
              sx={{
                color: '#1565C0',
                '&:hover': {
                  backgroundColor: 'rgba(21, 101, 192, 0.04)',
                },
              }}
            >
              Back
            </Button>
            <Typography variant="h4" sx={{ fontWeight: 700 }}>
              Case {caseNumber}
            </Typography>
          </Stack>
          
          <Typography variant="body1" color="text.secondary" sx={{ mb: 4 }}>
            Generate a PDF document for this case using one of the available templates.
          </Typography>

          {/* Status Messages */}
          {error && (
            <Alert severity="error" sx={{ mb: 3 }} onClose={() => setError(null)}>
              {error}
            </Alert>
          )}
          
          {success && (
            <Alert severity="success" sx={{ mb: 3 }} onClose={() => setSuccess(null)}>
              {success}
            </Alert>
          )}

          {/* Template Selection and Generation */}
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Generate PDF Document
              </Typography>
              
              <Stack spacing={3}>
                <TextField
                  fullWidth
                  label="Case Notes"
                  multiline
                  rows={3}
                  placeholder="Add any additional notes about this case..."
                  sx={{ mb: 2 }}
                />
                <FormControl fullWidth>
                  <InputLabel>Select Template</InputLabel>
                  <Select
                    value={templateName}
                    onChange={(e) => setTemplateName(e.target.value)}
                    label="Select Template"
                  >
                    {templates.map((template) => (
                      <MenuItem key={template.template_name} value={template.template_name}>
                        <Stack direction="row" alignItems="center" spacing={1}>
                          <Typography>{template.template_name}</Typography>
                          <Chip 
                            label={template.version || 'v1'} 
                            size="small" 
                            variant="outlined"
                          />
                          {template.base_pdf_path && (
                            <Chip 
                              label="Base PDF" 
                              size="small" 
                              color="success" 
                              variant="outlined"
                            />
                          )}
                        </Stack>
                      </MenuItem>
                    ))}
                  </Select>
                </FormControl>

                <Button
                  variant="contained"
                  startIcon={<DownloadIcon />}
                  onClick={handleGenerate}
                  disabled={busy || !templateName}
                  fullWidth
                  sx={{
                    backgroundColor: '#1565C0',
                    '&:hover': {
                      backgroundColor: '#0D47A1',
                    },
                  }}
                >
                  {busy ? 'Generating PDF...' : 'Use this template'}
                </Button>
              </Stack>
            </CardContent>
          </Card>

          {/* Results */}
          {result && (
            <Paper elevation={2} sx={{ mt: 3 }}>
              <Card sx={{ mt: 3 }}>
                <CardContent>
                <Typography variant="h6" gutterBottom>
                  Generation Results
                </Typography>
                
                <Stack spacing={2}>
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                    <Chip 
                      label={result.usedPlacements || 'default'} 
                      color={result.usedPlacements === 'auto-loaded' ? 'success' : 'default'}
                      size="small"
                    />
                    <Typography variant="body2" color="text.secondary">
                      Signature placements: {result.usedPlacements || 'default'}
                    </Typography>
                  </Box>

                  {result.signedUrl && (
                    <Box sx={{ textAlign: 'center' }}>
                      <Button
                        variant="contained"
                        href={result.signedUrl}
                        target="_blank"
                        startIcon={<DownloadIcon />}
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
                </Stack>
              </CardContent>
            </Card>
          )}

          {/* Case Information */}
          <Card sx={{ mt: 3 }}>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Case Information
              </Typography>
              
              <Grid container spacing={2}>
                <Grid item xs={12} sm={6}>
                  <Typography variant="body2" color="text.secondary">
                    Case Number
                  </Typography>
                  <Typography variant="body1" sx={{ fontWeight: 600 }}>
                    {caseNumber}
                  </Typography>
                </Grid>
                <Grid item xs={12} sm={6}>
                  <Typography variant="body2" color="text.secondary">
                    Available Templates
                  </Typography>
                  <Typography variant="body1" sx={{ fontWeight: 600 }}>
                    {templates.length}
                  </Typography>
                </Grid>
              </Grid>
            </CardContent>
          </Card>
            </Paper>
          )}
        </Box>
      </Section>
    </PageLayout>
  );
};

export default CaseDetailPage;
