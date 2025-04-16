import React, { useState, useEffect } from 'react';
import {
  Box,
  Container,
  Typography,
  Card,
  CardContent,
  Grid,
  TextField,
  Button,
  Alert,
  CircularProgress,
  Stepper,
  Step,
  StepLabel,
} from '@mui/material';
import { useTranslation } from 'react-i18next';

const DocumentGenerator = () => {
  const { t } = useTranslation();
  const [templates, setTemplates] = useState([]);
  const [selectedTemplate, setSelectedTemplate] = useState(null);
  const [formData, setFormData] = useState({});
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);
  const [activeStep, setActiveStep] = useState(0);

  useEffect(() => {
    fetchTemplates();
  }, []);

  const fetchTemplates = async () => {
    try {
      const response = await fetch('/api/documents/templates');
      if (!response.ok) throw new Error('Failed to fetch templates');
      const data = await response.json();
      setTemplates(data);
    } catch (err) {
      setError('Failed to load document templates');
    }
  };

  const handleTemplateSelect = (template) => {
    setSelectedTemplate(template);
    setFormData({});
    setActiveStep(1);
  };

  const handleInputChange = (field) => (event) => {
    setFormData(prev => ({
      ...prev,
      [field]: event.target.value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setSuccess(null);

    try {
      const response = await fetch('/api/documents/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          template_id: selectedTemplate.id,
          ...formData
        }),
      });

      if (!response.ok) throw new Error('Failed to generate document');
      
      const result = await response.json();
      setSuccess('Document generated successfully!');
      setActiveStep(2);
      
      // Trigger download
      window.location.href = result.document.download_url;
    } catch (err) {
      setError('Failed to generate document. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const steps = ['Select Template', 'Fill Details', 'Download'];

  return (
    <Container maxWidth="md" sx={{ py: 4 }}>
      <Typography variant="h4" component="h1" gutterBottom>
        {t('Free Document Generator')}
      </Typography>
      
      <Stepper activeStep={activeStep} sx={{ mb: 4 }}>
        {steps.map((label) => (
          <Step key={label}>
            <StepLabel>{label}</StepLabel>
          </Step>
        ))}
      </Stepper>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}

      {success && (
        <Alert severity="success" sx={{ mb: 2 }}>
          {success}
        </Alert>
      )}

      {activeStep === 0 && (
        <Grid container spacing={2}>
          {templates.map((template) => (
            <Grid item xs={12} md={6} key={template.id}>
              <Card 
                sx={{ 
                  cursor: 'pointer',
                  '&:hover': { boxShadow: 6 }
                }}
                onClick={() => handleTemplateSelect(template)}
              >
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    {template.name}
                  </Typography>
                  <Typography color="textSecondary" gutterBottom>
                    {template.category}
                  </Typography>
                  <Typography variant="body2">
                    {template.description}
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>
      )}

      {activeStep === 1 && selectedTemplate && (
        <Box component="form" onSubmit={handleSubmit}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                {selectedTemplate.name}
              </Typography>
              
              <Grid container spacing={2}>
                {selectedTemplate.fields.map((field) => (
                  <Grid item xs={12} sm={6} key={field}>
                    <TextField
                      required
                      fullWidth
                      label={field.split('_').map(word => 
                        word.charAt(0).toUpperCase() + word.slice(1)
                      ).join(' ')}
                      value={formData[field] || ''}
                      onChange={handleInputChange(field)}
                    />
                  </Grid>
                ))}
              </Grid>

              <Box sx={{ mt: 3, display: 'flex', justifyContent: 'space-between' }}>
                <Button
                  variant="outlined"
                  onClick={() => setActiveStep(0)}
                >
                  Back
                </Button>
                <Button
                  type="submit"
                  variant="contained"
                  disabled={loading}
                >
                  {loading ? <CircularProgress size={24} /> : 'Generate Document'}
                </Button>
              </Box>
            </CardContent>
          </Card>
        </Box>
      )}

      {activeStep === 2 && (
        <Card>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              Document Generated Successfully!
            </Typography>
            <Typography paragraph>
              Your document has been generated and the download should start automatically.
            </Typography>
            <Button
              variant="contained"
              onClick={() => {
                setSelectedTemplate(null);
                setFormData({});
                setActiveStep(0);
              }}
            >
              Generate Another Document
            </Button>
          </CardContent>
        </Card>
      )}
    </Container>
  );
};

export default DocumentGenerator; 