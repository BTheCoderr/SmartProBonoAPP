import React, { useState, useEffect } from 'react';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  TextField,
  Box,
  Typography,
  CircularProgress,
  Alert,
  Stepper,
  Step,
  StepLabel,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Divider,
  Paper,
  Grid,
  Autocomplete
} from '@mui/material';
import { documentsApi } from '../services/api';

const DocumentFromTemplateDialog = ({ open, onClose, onDocumentCreated, initialTemplateId = null }) => {
  const [activeStep, setActiveStep] = useState(0);
  const [templates, setTemplates] = useState([]);
  const [selectedTemplate, setSelectedTemplate] = useState(null);
  const [templateVariables, setTemplateVariables] = useState([]);
  const [formData, setFormData] = useState({});
  const [documentTitle, setDocumentTitle] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(false);
  const [previewContent, setPreviewContent] = useState('');
  
  const steps = ['Select Template', 'Fill Details', 'Preview & Create'];
  
  useEffect(() => {
    if (open) {
      fetchTemplates();
      if (initialTemplateId) {
        fetchTemplate(initialTemplateId);
      }
    }
  }, [open, initialTemplateId]);
  
  const fetchTemplates = async () => {
    try {
      setLoading(true);
      const response = await documentsApi.getTemplates();
      setTemplates(response.templates || []);
      setLoading(false);
    } catch (err) {
      console.error('Error fetching templates:', err);
      setError('Failed to load templates. Please try again.');
      setLoading(false);
    }
  };
  
  const fetchTemplate = async (templateId) => {
    try {
      setLoading(true);
      const template = await documentsApi.getTemplateById(templateId);
      setSelectedTemplate(template);
      extractVariables(template);
      setDocumentTitle(template.title);
      setLoading(false);
    } catch (err) {
      console.error('Error fetching template:', err);
      setError('Failed to load template. Please try again.');
      setLoading(false);
    }
  };
  
  const extractVariables = (template) => {
    if (!template || !template.content) return;
    
    // Extract variables from {{variable}} syntax
    const regex = /{{([^}]+)}}/g;
    const matches = [...template.content.matchAll(regex)];
    const variables = [...new Set(matches.map(match => match[1].trim()))];
    
    // Initialize form data with empty values
    const initialFormData = variables.reduce((acc, variable) => {
      acc[variable] = '';
      return acc;
    }, {});
    
    setTemplateVariables(variables);
    setFormData(initialFormData);
  };
  
  const handleTemplateChange = (event, template) => {
    setSelectedTemplate(template);
    if (template) {
      extractVariables(template);
      setDocumentTitle(template.title);
    } else {
      setTemplateVariables([]);
      setFormData({});
      setDocumentTitle('');
    }
  };
  
  const handleFormDataChange = (variable, value) => {
    setFormData(prev => ({
      ...prev,
      [variable]: value
    }));
  };
  
  const handleNext = () => {
    if (activeStep === 1) {
      // Generate preview before going to the final step
      generatePreview();
    }
    setActiveStep(prev => prev + 1);
  };
  
  const handleBack = () => {
    setActiveStep(prev => prev - 1);
  };
  
  const generatePreview = () => {
    if (!selectedTemplate || !selectedTemplate.content) return;
    
    // Replace variables in template with form data
    let content = selectedTemplate.content;
    
    for (const [key, value] of Object.entries(formData)) {
      const placeholder = `{{${key}}}`;
      content = content.replace(new RegExp(placeholder, 'g'), value || placeholder);
    }
    
    setPreviewContent(content);
  };
  
  const handleCreate = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const newDocument = await documentsApi.generateDocument(selectedTemplate._id, {
        title: documentTitle,
        variables: formData
      });
      
      setSuccess(true);
      
      // Notify parent component
      if (onDocumentCreated) {
        onDocumentCreated(newDocument);
      }
      
      // Close dialog after 1.5 seconds
      setTimeout(() => {
        setSuccess(false);
        resetDialog();
        onClose();
      }, 1500);
    } catch (err) {
      console.error('Error creating document:', err);
      setError('Failed to create document. Please try again.');
    } finally {
      setLoading(false);
    }
  };
  
  const resetDialog = () => {
    setActiveStep(0);
    setSelectedTemplate(null);
    setTemplateVariables([]);
    setFormData({});
    setDocumentTitle('');
    setPreviewContent('');
    setError(null);
    setSuccess(false);
  };
  
  const validateStep = () => {
    if (activeStep === 0) {
      return !!selectedTemplate;
    } else if (activeStep === 1) {
      // Check if all required variables have values
      return documentTitle.trim() !== '' && 
        templateVariables.every(variable => formData[variable] && formData[variable].trim() !== '');
    }
    
    return true;
  };
  
  const renderStepContent = () => {
    switch (activeStep) {
      case 0:
        return (
          <Box sx={{ mt: 2 }}>
            <Typography variant="body1" gutterBottom>
              Select a template to use for your new document.
            </Typography>
            
            <Autocomplete
              options={templates}
              getOptionLabel={(option) => option.title}
              value={selectedTemplate}
              onChange={handleTemplateChange}
              loading={loading}
              renderInput={(params) => (
                <TextField
                  {...params}
                  label="Select Template"
                  variant="outlined"
                  margin="normal"
                  required
                  error={!selectedTemplate && error}
                  helperText={!selectedTemplate && error ? 'Please select a template' : ''}
                  InputProps={{
                    ...params.InputProps,
                    endAdornment: (
                      <>
                        {loading ? <CircularProgress color="inherit" size={20} /> : null}
                        {params.InputProps.endAdornment}
                      </>
                    ),
                  }}
                />
              )}
            />
            
            {selectedTemplate && (
              <Paper variant="outlined" sx={{ p: 2, mt: 3 }}>
                <Typography variant="subtitle1" gutterBottom>
                  Template Preview
                </Typography>
                <Typography variant="body2" color="text.secondary" gutterBottom>
                  {selectedTemplate.description}
                </Typography>
                <Divider sx={{ my: 1 }} />
                <Typography variant="body2">
                  Category: {selectedTemplate.category}
                </Typography>
                {selectedTemplate.tags && selectedTemplate.tags.length > 0 && (
                  <Typography variant="body2">
                    Tags: {selectedTemplate.tags.join(', ')}
                  </Typography>
                )}
                <Typography variant="body2">
                  Variables: {templateVariables.join(', ')}
                </Typography>
              </Paper>
            )}
          </Box>
        );
      
      case 1:
        return (
          <Box sx={{ mt: 2 }}>
            <Typography variant="body1" gutterBottom>
              Fill in the details for your document.
            </Typography>
            
            <TextField
              fullWidth
              label="Document Title"
              value={documentTitle}
              onChange={(e) => setDocumentTitle(e.target.value)}
              margin="normal"
              required
              error={!documentTitle && error}
              helperText={!documentTitle && error ? 'Document title is required' : ''}
            />
            
            <Typography variant="subtitle1" sx={{ mt: 3, mb: 2 }}>
              Template Variables
            </Typography>
            
            <Grid container spacing={2}>
              {templateVariables.map((variable) => (
                <Grid item xs={12} sm={6} key={variable}>
                  <TextField
                    fullWidth
                    label={variable.replace(/_/g, ' ')}
                    value={formData[variable] || ''}
                    onChange={(e) => handleFormDataChange(variable, e.target.value)}
                    margin="normal"
                    required
                  />
                </Grid>
              ))}
            </Grid>
          </Box>
        );
      
      case 2:
        return (
          <Box sx={{ mt: 2 }}>
            <Typography variant="body1" gutterBottom>
              Review your document before creating it.
            </Typography>
            
            <Paper variant="outlined" sx={{ p: 2, mt: 2 }}>
              <Typography variant="h6" gutterBottom>
                {documentTitle}
              </Typography>
              
              <Divider sx={{ my: 1 }} />
              
              <Box sx={{ mt: 2, maxHeight: '400px', overflow: 'auto' }}>
                <div dangerouslySetInnerHTML={{ __html: previewContent }} />
              </Box>
            </Paper>
          </Box>
        );
      
      default:
        return null;
    }
  };
  
  return (
    <Dialog 
      open={open} 
      onClose={onClose} 
      maxWidth="md" 
      fullWidth
      PaperProps={{ sx: { minHeight: '60vh' } }}
    >
      <DialogTitle>Create Document from Template</DialogTitle>
      
      <DialogContent dividers>
        {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
        {success && <Alert severity="success" sx={{ mb: 2 }}>Document created successfully!</Alert>}
        
        <Stepper activeStep={activeStep} sx={{ mb: 4 }}>
          {steps.map((label) => (
            <Step key={label}>
              <StepLabel>{label}</StepLabel>
            </Step>
          ))}
        </Stepper>
        
        {renderStepContent()}
      </DialogContent>
      
      <DialogActions>
        <Button onClick={onClose} disabled={loading}>
          Cancel
        </Button>
        
        {activeStep > 0 && (
          <Button onClick={handleBack} disabled={loading}>
            Back
          </Button>
        )}
        
        {activeStep < steps.length - 1 ? (
          <Button 
            variant="contained" 
            onClick={handleNext}
            disabled={!validateStep() || loading}
          >
            Next
          </Button>
        ) : (
          <Button 
            variant="contained" 
            color="primary"
            onClick={handleCreate}
            disabled={loading}
          >
            {loading ? <CircularProgress size={24} sx={{ mr: 1 }} /> : null}
            Create Document
          </Button>
        )}
      </DialogActions>
    </Dialog>
  );
};

export default DocumentFromTemplateDialog; 