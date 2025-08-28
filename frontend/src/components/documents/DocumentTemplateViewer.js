import React, { useState, useEffect } from 'react';
import {
  Box,
  Paper,
  Typography,
  Button,
  TextField,
  Grid,
  CircularProgress,
  Alert,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  MenuItem,
  Select,
  FormControl,
  InputLabel,
  FormHelperText,
  Divider
} from '@mui/material';
import DescriptionIcon from '@mui/icons-material/Description';
import DownloadIcon from '@mui/icons-material/Download';
import PreviewIcon from '@mui/icons-material/Preview';
import ApiService from '../../services/ApiService';

// API service for templates
const getTemplates = async () => {
  try {
    // Try to use the actual API endpoint
    const response = await ApiService.get('/api/documents/templates');
    return response.data || [];
  } catch (error) {
    console.error('Error fetching templates from API:', error);
    
    // Fallback to mock data if API fails
    console.log('Using fallback mock template data');
    return [
      {
        id: 'sample_template',
        name: 'Sample Template',
        description: 'A basic legal document template',
        type: 'HTML'
      },
      {
        id: 'legal_letter',
        name: 'Legal Letter',
        description: 'Standard legal letter template',
        type: 'HTML'
      },
      {
        id: 'contract_agreement',
        name: 'Contract Agreement',
        description: 'Basic contract agreement template',
        type: 'HTML'
      }
    ];
  }
};

const getTemplateFields = async (templateId) => {
  try {
    // Try to use the actual API endpoint
    const response = await ApiService.get(`/api/documents/templates/${templateId}/fields`);
    return response.data || { fields: [] };
  } catch (error) {
    console.error('Error fetching template fields from API:', error);
    
    // Fallback to mock data if API fails
    console.log('Using fallback mock template fields');
    return {
      fields: [
        { name: 'title', label: 'Document Title', type: 'text', required: true },
        { name: 'client_name', label: 'Client Name', type: 'text', required: true },
        { name: 'matter_description', label: 'Matter Description', type: 'text', required: true },
        { name: 'content', label: 'Document Content', type: 'textarea', required: true },
        { name: 'user_name', label: 'User Name', type: 'text', required: true }
      ]
    };
  }
};

const DocumentTemplateViewer = () => {
  const [templates, setTemplates] = useState([]);
  const [selectedTemplate, setSelectedTemplate] = useState(null);
  const [templateFields, setTemplateFields] = useState([]);
  const [formValues, setFormValues] = useState({});
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [dialogOpen, setDialogOpen] = useState(false);
  const [previewDialogOpen, setPreviewDialogOpen] = useState(false);
  const [previewContent, setPreviewContent] = useState('');
  const [formErrors, setFormErrors] = useState({});
  const [downloadUrl, setDownloadUrl] = useState(null);
  const [downloadFilename, setDownloadFilename] = useState('');
  
  // Fetch templates on component mount
  useEffect(() => {
    const fetchTemplates = async () => {
      setIsLoading(true);
      try {
        const templatesData = await getTemplates();
        setTemplates(templatesData);
      } catch (err) {
        setError('Failed to load templates');
        console.error(err);
      } finally {
        setIsLoading(false);
      }
    };
    
    fetchTemplates();
  }, []);
  
  // Handle template selection
  const handleTemplateSelect = async (templateId) => {
    if (!templateId) return;
    
    setIsLoading(true);
    setSelectedTemplate(templateId);
    
    try {
      const { fields } = await getTemplateFields(templateId);
      setTemplateFields(fields);
      
      // Initialize form values
      const initialValues = {};
      fields.forEach(field => {
        initialValues[field.name] = '';
      });
      setFormValues(initialValues);
      setFormErrors({});
      
      setDialogOpen(true);
    } catch (err) {
      setError('Failed to load template details');
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };
  
  // Handle form field changes
  const handleFieldChange = (e) => {
    const { name, value } = e.target;
    setFormValues({
      ...formValues,
      [name]: value
    });
    
    // Clear error for this field if it exists
    if (formErrors[name]) {
      setFormErrors({
        ...formErrors,
        [name]: null
      });
    }
  };
  
  // Validate form
  const validateForm = () => {
    const errors = {};
    let isValid = true;
    
    templateFields.forEach(field => {
      if (field.required && !formValues[field.name]) {
        errors[field.name] = `${field.label} is required`;
        isValid = false;
      }
    });
    
    setFormErrors(errors);
    return isValid;
  };
  
  // Handle form submission
  const handleSubmit = async () => {
    if (!validateForm()) return;
    
    setIsLoading(true);
    try {
      // Try to use the actual document generation API
      const template = templates.find(t => t.id === selectedTemplate);
      
      try {
        // Call the document generation API
        const response = await ApiService.post('/api/documents/generate', {
          template_id: selectedTemplate,
          data: formValues
        }, { responseType: 'blob' });
        
        // Create a download URL for the generated document
        const url = window.URL.createObjectURL(new Blob([response.data]));
        const filename = `${template?.name || selectedTemplate}_${new Date().toISOString().slice(0, 10)}.pdf`;
        
        // Store the URL for preview (for PDF preview, this would require a PDF viewer component)
        // For now, show the form data in a formatted HTML preview
        generateClientSidePreview(template);
        
        // Store the document URL for later download
        setDownloadUrl(url);
        setDownloadFilename(filename);
        
        setDialogOpen(false);
        setPreviewDialogOpen(true);
      } catch (apiError) {
        console.error('API document generation failed, using client-side fallback:', apiError);
        // Fallback to client-side preview generation
        generateClientSidePreview(template);
        setDialogOpen(false);
        setPreviewDialogOpen(true);
      }
    } catch (err) {
      setError('Failed to generate document');
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };
  
  // Generate a client-side preview of the document
  const generateClientSidePreview = (template) => {
    // Generate a formatted document preview
    const previewText = `
      <!DOCTYPE html>
      <html>
      <head>
        <meta charset="utf-8">
        <title>${formValues.title || 'Generated Document'}</title>
        <style>
          body { font-family: Arial, sans-serif; margin: 40px; }
          .header { text-align: center; margin-bottom: 30px; }
          .content { line-height: 1.6; }
          .signature { margin-top: 50px; }
          .footer { margin-top: 50px; text-align: center; font-size: 12px; }
        </style>
      </head>
      <body>
        <div class="header">
          <h1>${formValues.title || 'Generated Document'}</h1>
          <p>Generated on ${new Date().toLocaleDateString()}</p>
        </div>
        
        <div class="content">
          <p>This document certifies that <strong>${formValues.client_name || 'Client'}</strong> has received legal assistance regarding <strong>${formValues.matter_description || 'Legal Matter'}</strong>.</p>
          
          <p>${formValues.content || 'Document content goes here.'}</p>
          
          <div class="signature">
            <p>Signed:</p>
            <p>___________________________</p>
            <p>${formValues.user_name || 'User'}</p>
            <p>Date: ${new Date().toLocaleDateString()}</p>
          </div>
        </div>
        
        <div class="footer">
          <p>SmartProBono Legal Platform | Template: ${template?.name || selectedTemplate} | Confidential</p>
        </div>
      </body>
      </html>
    `;
    
    setPreviewContent(previewText);
  };
  
  const handleCloseDialog = () => {
    setDialogOpen(false);
  };
  
  const handleClosePreview = () => {
    setPreviewDialogOpen(false);
  };
  
  return (
    <Box>
      <Typography variant="h5" gutterBottom>
        Document Templates
      </Typography>
      
      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>
      )}
      
      {isLoading && !dialogOpen ? (
        <Box sx={{ display: 'flex', justifyContent: 'center', my: 4 }}>
          <CircularProgress />
        </Box>
      ) : (
        <Grid container spacing={3} sx={{ mt: 1 }}>
          {templates.map((template) => (
            <Grid item xs={12} sm={6} md={4} key={template.id}>
              <Paper 
                elevation={3} 
                sx={{ 
                  p: 2, 
                  height: '100%',
                  display: 'flex',
                  flexDirection: 'column',
                  transition: 'transform 0.2s',
                  '&:hover': {
                    transform: 'translateY(-4px)',
                    boxShadow: 6
                  }
                }}
              >
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                  <DescriptionIcon color="primary" sx={{ mr: 1 }} />
                  <Typography variant="h6">{template.name}</Typography>
                </Box>
                <Typography variant="body2" color="text.secondary" sx={{ flexGrow: 1 }}>
                  {template.description}
                </Typography>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mt: 2 }}>
                  <Typography variant="caption">Type: {template.type}</Typography>
                  <Button 
                    variant="outlined" 
                    size="small"
                    startIcon={<PreviewIcon />}
                    onClick={() => handleTemplateSelect(template.id)}
                  >
                    Use Template
                  </Button>
                </Box>
              </Paper>
            </Grid>
          ))}
        </Grid>
      )}
      
      {/* Template Form Dialog */}
      <Dialog 
        open={dialogOpen} 
        onClose={handleCloseDialog}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle>
          {templates.find(t => t.id === selectedTemplate)?.name || 'Fill Template'}
        </DialogTitle>
        <DialogContent>
          {isLoading ? (
            <Box sx={{ display: 'flex', justifyContent: 'center', my: 4 }}>
              <CircularProgress />
            </Box>
          ) : (
            <Grid container spacing={3} sx={{ mt: 1 }}>
              {templateFields.map((field) => (
                <Grid item xs={12} key={field.name}>
                  {field.type === 'textarea' ? (
                    <TextField
                      fullWidth
                      multiline
                      rows={4}
                      label={field.label}
                      name={field.name}
                      value={formValues[field.name] || ''}
                      onChange={handleFieldChange}
                      required={field.required}
                      error={Boolean(formErrors[field.name])}
                      helperText={formErrors[field.name]}
                    />
                  ) : (
                    <TextField
                      fullWidth
                      label={field.label}
                      name={field.name}
                      value={formValues[field.name] || ''}
                      onChange={handleFieldChange}
                      required={field.required}
                      error={Boolean(formErrors[field.name])}
                      helperText={formErrors[field.name]}
                    />
                  )}
                </Grid>
              ))}
            </Grid>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseDialog}>Cancel</Button>
          <Button 
            onClick={handleSubmit} 
            variant="contained" 
            disabled={isLoading}
          >
            {isLoading ? 'Generating...' : 'Generate Document'}
          </Button>
        </DialogActions>
      </Dialog>
      
      {/* Preview Dialog */}
      <Dialog
        open={previewDialogOpen}
        onClose={handleClosePreview}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle>Document Preview</DialogTitle>
        <DialogContent>
          <Paper sx={{ p: 3, mt: 2 }}>
            <div dangerouslySetInnerHTML={{ __html: previewContent }} />
          </Paper>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleClosePreview}>Close</Button>
          <Button 
            variant="contained" 
            startIcon={<DownloadIcon />}
            onClick={() => {
              // Download the document - use the API-generated file if available
              if (downloadUrl && downloadFilename) {
                // Use the stored download URL from API response
                const element = document.createElement('a');
                element.href = downloadUrl;
                element.download = downloadFilename;
                document.body.appendChild(element);
                element.click();
                document.body.removeChild(element);
                
                // Clean up
                setTimeout(() => {
                  URL.revokeObjectURL(downloadUrl);
                  setDownloadUrl(null);
                  setDownloadFilename('');
                }, 100);
              } else {
                // Fallback to HTML content
                const element = document.createElement('a');
                const file = new Blob([previewContent], {type: 'text/html'});
                element.href = URL.createObjectURL(file);
                element.download = `${selectedTemplate}_document_${new Date().toISOString().slice(0, 10)}.html`;
                document.body.appendChild(element);
                element.click();
                document.body.removeChild(element);
                URL.revokeObjectURL(element.href);
              }
              handleClosePreview();
            }}
          >
            Download
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default DocumentTemplateViewer; 