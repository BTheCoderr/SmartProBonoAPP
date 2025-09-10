import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Paper,
  Button,
  TextField,
  Grid,
  Card,
  CardContent,
  CardActionArea,
  Chip,
  Alert,
  CircularProgress,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  List,
  ListItem,
  ListItemText,
  ListItemIcon
} from '@mui/material';
import {
  Description as DocumentIcon,
  Download as DownloadIcon,
  Add as AddIcon,
  CheckCircle as CheckIcon
} from '@mui/icons-material';

const PDFGenerator = () => {
  const [templates, setTemplates] = useState([]);
  const [selectedTemplate, setSelectedTemplate] = useState(null);
  const [formData, setFormData] = useState({});
  const [generating, setGenerating] = useState(false);
  const [generatedPDF, setGeneratedPDF] = useState(null);
  const [showPreview, setShowPreview] = useState(false);
  const [error, setError] = useState(null);

  // Load templates on component mount
  useEffect(() => {
    loadTemplates();
  }, []);

  const loadTemplates = async () => {
    try {
      const response = await fetch('http://localhost:3001/api/generator/templates');
      const data = await response.json();
      
      if (data.success) {
        setTemplates(data.templates);
      } else {
        setError('Failed to load document templates');
      }
    } catch (err) {
      setError('Failed to connect to document generator');
      console.error('Error loading templates:', err);
    }
  };

  const handleTemplateSelect = (template) => {
    setSelectedTemplate(template);
    setFormData({});
    setGeneratedPDF(null);
    setError(null);
  };

  const handleInputChange = (field, value) => {
    setFormData(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const generatePDF = async () => {
    if (!selectedTemplate) return;

    setGenerating(true);
    setError(null);

    try {
      const response = await fetch('http://localhost:3001/api/generator/create', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          document_type: selectedTemplate.id,
          title: selectedTemplate.name,
          content: formData,
          parties: [
            formData[selectedTemplate.fields[0]] || '',
            formData[selectedTemplate.fields[1]] || ''
          ].filter(Boolean)
        })
      });

      const data = await response.json();

      if (data.success) {
        setGeneratedPDF(data.pdf_data);
        setShowPreview(true);
      } else {
        setError(data.error || 'Failed to generate document');
      }
    } catch (err) {
      setError('Failed to generate document');
      console.error('Error generating PDF:', err);
    } finally {
      setGenerating(false);
    }
  };

  const downloadPDF = () => {
    if (generatedPDF) {
      const link = document.createElement('a');
      link.href = `data:application/pdf;base64,${generatedPDF}`;
      link.download = `${selectedTemplate.name.replace(/\s+/g, '_')}.pdf`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    }
  };

  const renderTemplateSelection = () => (
    <Box>
      <Typography variant="h6" gutterBottom>
        Choose Document Template
      </Typography>
      <Typography variant="body2" color="text.secondary" paragraph>
        Select a template to get started with your legal document.
      </Typography>
      
      <Grid container spacing={2}>
        {templates.map((template) => (
          <Grid item xs={12} sm={6} md={4} key={template.id}>
            <Card 
              sx={{ 
                height: '100%',
                transition: 'transform 0.2s',
                '&:hover': {
                  transform: 'translateY(-4px)',
                  boxShadow: 4
                }
              }}
            >
              <CardActionArea onClick={() => handleTemplateSelect(template)}>
                <Box sx={{ bgcolor: 'primary.lighter', p: 2, display: 'flex', justifyContent: 'center' }}>
                  <DocumentIcon fontSize="large" color="primary" />
                </Box>
                <CardContent>
                  <Typography variant="h6" component="div" gutterBottom>
                    {template.name}
                  </Typography>
                  <Typography variant="body2" color="text.secondary" paragraph>
                    {template.description}
                  </Typography>
                  <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                    {template.fields.slice(0, 3).map((field) => (
                      <Chip 
                        key={field} 
                        label={field.replace('_', ' ')} 
                        size="small" 
                        variant="outlined"
                      />
                    ))}
                    {template.fields.length > 3 && (
                      <Chip 
                        label={`+${template.fields.length - 3} more`} 
                        size="small" 
                        variant="outlined"
                        color="primary"
                      />
                    )}
                  </Box>
                </CardContent>
              </CardActionArea>
            </Card>
          </Grid>
        ))}
      </Grid>
    </Box>
  );

  const renderForm = () => {
    if (!selectedTemplate) return null;

    return (
      <Box>
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
          <DocumentIcon color="primary" sx={{ mr: 1 }} />
          <Typography variant="h6">
            {selectedTemplate.name}
          </Typography>
          <Button 
            variant="outlined" 
            size="small" 
            onClick={() => setSelectedTemplate(null)}
            sx={{ ml: 'auto' }}
          >
            Change Template
          </Button>
        </Box>

        <Typography variant="body2" color="text.secondary" paragraph>
          Fill in the details below to generate your document.
        </Typography>

        <Grid container spacing={2}>
          {selectedTemplate.fields.map((field) => (
            <Grid item xs={12} sm={6} key={field}>
              <TextField
                fullWidth
                label={field.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())}
                value={formData[field] || ''}
                onChange={(e) => handleInputChange(field, e.target.value)}
                variant="outlined"
                size="small"
              />
            </Grid>
          ))}
        </Grid>

        <Box sx={{ mt: 3, display: 'flex', gap: 2 }}>
          <Button
            variant="contained"
            onClick={generatePDF}
            disabled={generating}
            startIcon={generating ? <CircularProgress size={20} /> : <AddIcon />}
          >
            {generating ? 'Generating...' : 'Generate Document'}
          </Button>
        </Box>
      </Box>
    );
  };

  const renderPreview = () => (
    <Dialog 
      open={showPreview} 
      onClose={() => setShowPreview(false)}
      maxWidth="md"
      fullWidth
    >
      <DialogTitle>
        <Box sx={{ display: 'flex', alignItems: 'center' }}>
          <CheckIcon color="success" sx={{ mr: 1 }} />
          Document Generated Successfully!
        </Box>
      </DialogTitle>
      <DialogContent>
        <Alert severity="success" sx={{ mb: 2 }}>
          Your {selectedTemplate?.name} has been generated and is ready for download.
        </Alert>
        
        <Typography variant="body2" color="text.secondary" paragraph>
          <strong>What's next:</strong>
        </Typography>
        <List dense>
          <ListItem>
            <ListItemIcon>
              <CheckIcon color="success" fontSize="small" />
            </ListItemIcon>
            <ListItemText primary="Review the document for accuracy" />
          </ListItem>
          <ListItem>
            <ListItemIcon>
              <CheckIcon color="success" fontSize="small" />
            </ListItemIcon>
            <ListItemText primary="Download and save a copy" />
          </ListItem>
          <ListItem>
            <ListItemIcon>
              <CheckIcon color="success" fontSize="small" />
            </ListItemIcon>
            <ListItemText primary="Share with the other party for review" />
          </ListItem>
          <ListItem>
            <ListItemIcon>
              <CheckIcon color="success" fontSize="small" />
            </ListItemIcon>
            <ListItemText primary="Consider having it reviewed by an attorney if needed" />
          </ListItem>
        </List>
      </DialogContent>
      <DialogActions>
        <Button onClick={() => setShowPreview(false)}>
          Close
        </Button>
        <Button 
          variant="contained" 
          onClick={downloadPDF}
          startIcon={<DownloadIcon />}
        >
          Download PDF
        </Button>
      </DialogActions>
    </Dialog>
  );

  return (
    <Box>
      <Paper sx={{ p: 3, mb: 3 }}>
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
          <DocumentIcon color="primary" sx={{ mr: 1, fontSize: 32 }} />
          <Typography variant="h5">
            PDF Generator
          </Typography>
        </Box>
        
        <Typography variant="body1" paragraph>
          Create professional legal documents in minutes! Choose a template, fill in your details, and generate a ready-to-use PDF.
        </Typography>
      </Paper>

      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}

      {!selectedTemplate ? renderTemplateSelection() : renderForm()}
      {renderPreview()}
    </Box>
  );
};

export default PDFGenerator;
