import React, { useState, useEffect } from 'react';
import {
  Box,
  Button,
  Paper,
  Step,
  StepLabel,
  Stepper,
  Typography,
  TextField,
  CircularProgress,
  Alert,
  MenuItem,
} from '@mui/material';
import { useTranslation } from 'react-i18next';

const DocumentGenerator = () => {
  const { t } = useTranslation();
  const [activeStep, setActiveStep] = useState(0);
  const [selectedTemplate, setSelectedTemplate] = useState(null);
  const [formData, setFormData] = useState({});
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [templates, setTemplates] = useState([]);

  useEffect(() => {
    fetchTemplates();
  }, []);

  const fetchTemplates = async () => {
    try {
      setIsLoading(true);
      const response = await fetch('/api/templates');
      const data = await response.json();
      setTemplates(data);
    } catch (err) {
      setError('Failed to load templates');
    } finally {
      setIsLoading(false);
    }
  };

  const handleInputChange = (field) => (event) => {
    setFormData({
      ...formData,
      [field]: event.target.value
    });
  };

  const handleNext = () => {
    setActiveStep((prevStep) => prevStep + 1);
  };

  const handleBack = () => {
    setActiveStep((prevStep) => prevStep - 1);
  };

  const handleTemplateChange = (event) => {
    const template = templates.find(t => t.id === event.target.value);
    setSelectedTemplate(template);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    try {
      setIsLoading(true);
      const response = await fetch('/api/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          template: selectedTemplate,
          data: formData,
        }),
      });
      
      if (!response.ok) throw new Error('Failed to generate document');
      
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `${selectedTemplate.name}.docx`;
      a.click();
      window.URL.revokeObjectURL(url);
      handleNext();
    } catch (err) {
      setError('Failed to generate document');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Box sx={{ maxWidth: 800, mx: 'auto', p: 3 }}>
      <Paper
        elevation={3}
        sx={{
          p: 4,
        }}
      >
        <Typography variant="h4" component="h1" gutterBottom>
          {t('documents.title')}
        </Typography>

        {error && (
          <Alert severity="error" sx={{ mb: 3 }}>
            {error}
          </Alert>
        )}

        <Stepper activeStep={activeStep} sx={{ mb: 4 }}>
          <Step>
            <StepLabel>{t('documents.steps.selectTemplate')}</StepLabel>
          </Step>
          <Step>
            <StepLabel>{t('documents.steps.fillDetails')}</StepLabel>
          </Step>
          <Step>
            <StepLabel>{t('documents.steps.review')}</StepLabel>
          </Step>
        </Stepper>

        {activeStep === 0 && (
          <Box>
            <TextField
              select
              fullWidth
              label={t('documents.selectTemplate')}
              value={selectedTemplate?.id || ''}
              onChange={handleTemplateChange}
            >
              {templates.map((template) => (
                <MenuItem key={template.id} value={template.id}>
                  {template.name}
                </MenuItem>
              ))}
            </TextField>
          </Box>
        )}

        {activeStep === 1 && selectedTemplate && (
          <Box>
            <Typography variant="h6" gutterBottom>
              {selectedTemplate.name}
            </Typography>
            <Box component="form" sx={{ mt: 2 }}>
              {selectedTemplate.fields?.map((field) => (
                <TextField
                  key={field}
                  fullWidth
                  label={field.split('_').map(word => 
                    word.charAt(0).toUpperCase() + word.slice(1)
                  ).join(' ')}
                  value={formData[field] || ''}
                  onChange={handleInputChange(field)}
                  sx={{ mb: 2 }}
                />
              ))}
            </Box>
          </Box>
        )}

        {activeStep === 2 && (
          <Box>
            <Typography variant="h6" gutterBottom>
              {t('documents.review.title')}
            </Typography>
            <Box sx={{ mt: 2 }}>
              {Object.entries(formData).map(([field, value]) => (
                <Typography key={field}>
                  <strong>{field}:</strong> {value}
                </Typography>
              ))}
            </Box>
          </Box>
        )}

        <Box sx={{ mt: 4, display: 'flex', justifyContent: 'space-between' }}>
          <Button
            onClick={handleBack}
            disabled={activeStep === 0 || isLoading}
          >
            {t('common.back')}
          </Button>
          {activeStep === 2 ? (
            <Button
              variant="contained"
              onClick={handleSubmit}
              disabled={!selectedTemplate || isLoading}
              endIcon={isLoading ? <CircularProgress size={20} /> : null}
            >
              {t('documents.generate')}
            </Button>
          ) : (
            <Button
              variant="contained"
              onClick={handleNext}
              disabled={!selectedTemplate || isLoading}
            >
              {t('common.next')}
            </Button>
          )}
        </Box>
      </Paper>
    </Box>
  );
};

export default DocumentGenerator;
