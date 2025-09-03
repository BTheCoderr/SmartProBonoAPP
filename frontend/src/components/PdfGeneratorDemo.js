import React, { useState } from 'react';
import {
  Box,
  Button,
  Card,
  CardContent,
  Typography,
  TextField,
  Grid,
  Alert,
  CircularProgress,
  Chip,
  Stack,
} from '@mui/material';
import { Download as DownloadIcon, CloudUpload as CloudUploadIcon } from '@mui/icons-material';
import PdfService from '../services/PdfService';

const PdfGeneratorDemo = () => {
  const [formData, setFormData] = useState({
    clientName: 'Maria Lopez',
    caseNumber: 'SPB-2025-0912',
    dateIssued: new Date().toLocaleDateString(),
    bodyText: 'Intake summary and pro se instructions below.',
  });
  
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleInputChange = (field) => (event) => {
    setFormData(prev => ({
      ...prev,
      [field]: event.target.value
    }));
  };

  const handleGenerateAndSave = async () => {
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const pdfData = {
        ...formData,
        tableRows: [
          { cols: ['Document', 'Status', 'Notes'] },
          { cols: ['Fee Waiver', 'Prepared', 'Signature pending'] },
          { cols: ['Summons', 'Queued', 'Serve via sheriff'] },
        ],
        filenameBase: 'intake-summary'
      };

      const result = await PdfService.generateAndSaveToStorage(pdfData, 'demo-user');
      setResult(result);
    } catch (err) {
      setError(err.message || 'PDF generation failed');
    } finally {
      setLoading(false);
    }
  };

  const handleDownload = () => {
    if (result && result.signedUrl) {
      window.open(result.signedUrl, '_blank');
    }
  };

  return (
    <Box sx={{ maxWidth: 800, mx: 'auto', p: 3 }}>
      <Typography variant="h4" gutterBottom sx={{ textAlign: 'center', mb: 4 }}>
        SmartProBono PDF Generator Demo
      </Typography>

      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            PDF Generation Form
          </Typography>
          
          <Grid container spacing={2}>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="Client Name"
                value={formData.clientName}
                onChange={handleInputChange('clientName')}
                variant="outlined"
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="Case Number"
                value={formData.caseNumber}
                onChange={handleInputChange('caseNumber')}
                variant="outlined"
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="Date Issued"
                value={formData.dateIssued}
                onChange={handleInputChange('dateIssued')}
                variant="outlined"
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                fullWidth
                multiline
                rows={3}
                label="Body Text"
                value={formData.bodyText}
                onChange={handleInputChange('bodyText')}
                variant="outlined"
              />
            </Grid>
          </Grid>

          <Box sx={{ mt: 3, textAlign: 'center' }}>
            <Button
              variant="contained"
              size="large"
              startIcon={loading ? <CircularProgress size={20} /> : <CloudUploadIcon />}
              onClick={handleGenerateAndSave}
              disabled={loading}
              sx={{
                backgroundColor: '#1565C0',
                '&:hover': {
                  backgroundColor: '#0D47A1',
                },
              }}
            >
              {loading ? 'Generating & Saving...' : 'Generate & Save to Supabase'}
            </Button>
          </Box>
        </CardContent>
      </Card>

      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}

      {result && (
        <Card>
          <CardContent>
            <Typography variant="h6" gutterBottom color="success.main">
              ✅ PDF Generated Successfully!
            </Typography>
            
            <Stack spacing={2}>
              <Box>
                <Typography variant="body2" color="text.secondary">
                  Case Number:
                </Typography>
                <Chip label={result.caseNumber} color="primary" />
              </Box>
              
              <Box>
                <Typography variant="body2" color="text.secondary">
                  Storage Path:
                </Typography>
                <Typography variant="body2" sx={{ fontFamily: 'monospace', fontSize: '0.8rem' }}>
                  {result.storagePath}
                </Typography>
              </Box>
              
              <Box>
                <Button
                  variant="outlined"
                  startIcon={<DownloadIcon />}
                  onClick={handleDownload}
                  sx={{
                    borderColor: '#1565C0',
                    color: '#1565C0',
                    '&:hover': {
                      borderColor: '#0D47A1',
                      backgroundColor: 'rgba(21, 101, 192, 0.04)',
                    },
                  }}
                >
                  Download PDF
                </Button>
              </Box>
            </Stack>
          </CardContent>
        </Card>
      )}

      <Box sx={{ mt: 4, p: 2, backgroundColor: '#f5f5f5', borderRadius: 2 }}>
        <Typography variant="h6" gutterBottom>
          🚀 Features Demonstrated:
        </Typography>
        <Stack spacing={1}>
          <Typography variant="body2">• PDF generation with pdfme templates</Typography>
          <Typography variant="body2">• Professional headers and footers</Typography>
          <Typography variant="body2">• Dynamic table generation</Typography>
          <Typography variant="body2">• Supabase Storage integration</Typography>
          <Typography variant="body2">• Signed URL generation</Typography>
          <Typography variant="body2">• Database record tracking</Typography>
        </Stack>
      </Box>
    </Box>
  );
};

export default PdfGeneratorDemo;
