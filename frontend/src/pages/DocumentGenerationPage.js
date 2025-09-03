import React, { useState } from 'react';
import {
  Container,
  Typography,
  Box,
  Grid,
  Card,
  CardContent,
  CardHeader,
  Button,
  TextField,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Chip,
  Alert,
  CircularProgress,
  Divider,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Paper
} from '@mui/material';
import {
  Description as DescriptionIcon,
  AutoAwesome as AutoAwesomeIcon,
  Security as SecurityIcon,
  CheckCircle as CheckCircleIcon,
  Download as DownloadIcon,
  Edit as EditIcon,
  Save as SaveIcon
} from '@mui/icons-material';
import PageLayout from '../components/PageLayout';

const DocumentGenerationPage = () => {
  const [selectedTemplate, setSelectedTemplate] = useState('');
  const [formData, setFormData] = useState({});
  const [isGenerating, setIsGenerating] = useState(false);
  const [generatedDocument, setGeneratedDocument] = useState(null);

  const documentTemplates = [
    {
      id: 'lease-agreement',
      name: 'Lease Agreement',
      description: 'Residential rental agreement template',
      category: 'Real Estate',
      icon: <DescriptionIcon />
    },
    {
      id: 'employment-contract',
      name: 'Employment Contract',
      description: 'Standard employment agreement',
      category: 'Employment',
      icon: <DescriptionIcon />
    },
    {
      id: 'nda',
      name: 'Non-Disclosure Agreement',
      description: 'Confidentiality agreement template',
      category: 'Business',
      icon: <SecurityIcon />
    },
    {
      id: 'power-of-attorney',
      name: 'Power of Attorney',
      description: 'Legal authorization document',
      category: 'Estate Planning',
      icon: <DescriptionIcon />
    },
    {
      id: 'will',
      name: 'Last Will and Testament',
      description: 'Estate planning document',
      category: 'Estate Planning',
      icon: <DescriptionIcon />
    },
    {
      id: 'partnership-agreement',
      name: 'Partnership Agreement',
      description: 'Business partnership contract',
      category: 'Business',
      icon: <DescriptionIcon />
    }
  ];

  const handleTemplateSelect = (templateId) => {
    setSelectedTemplate(templateId);
    setFormData({});
    setGeneratedDocument(null);
  };

  const handleFormChange = (field, value) => {
    setFormData(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const handleGenerateDocument = async () => {
    setIsGenerating(true);
    // Simulate document generation
    setTimeout(() => {
      setGeneratedDocument({
        id: Date.now(),
        name: `${selectedTemplate}-${Date.now()}.pdf`,
        content: 'Generated document content...',
        downloadUrl: '#'
      });
      setIsGenerating(false);
    }, 2000);
  };

  const renderFormFields = () => {
    if (!selectedTemplate) return null;

    const template = documentTemplates.find(t => t.id === selectedTemplate);
    if (!template) return null;

    // Dynamic form fields based on template
    const fields = {
      'lease-agreement': [
        { name: 'landlordName', label: 'Landlord Name', type: 'text' },
        { name: 'tenantName', label: 'Tenant Name', type: 'text' },
        { name: 'propertyAddress', label: 'Property Address', type: 'text' },
        { name: 'rentAmount', label: 'Monthly Rent', type: 'number' },
        { name: 'leaseTerm', label: 'Lease Term (months)', type: 'number' }
      ],
      'employment-contract': [
        { name: 'employeeName', label: 'Employee Name', type: 'text' },
        { name: 'employerName', label: 'Employer Name', type: 'text' },
        { name: 'position', label: 'Position', type: 'text' },
        { name: 'salary', label: 'Annual Salary', type: 'number' },
        { name: 'startDate', label: 'Start Date', type: 'date' }
      ],
      'nda': [
        { name: 'disclosingParty', label: 'Disclosing Party', type: 'text' },
        { name: 'receivingParty', label: 'Receiving Party', type: 'text' },
        { name: 'purpose', label: 'Purpose of Disclosure', type: 'text' },
        { name: 'duration', label: 'Duration (years)', type: 'number' }
      ]
    };

    const templateFields = fields[selectedTemplate] || [];

    return (
      <Paper sx={{ p: 3, mt: 2 }}>
        <Typography variant="h6" gutterBottom>
          Document Information
        </Typography>
        <Grid container spacing={2}>
          {templateFields.map((field) => (
            <Grid item xs={12} sm={6} key={field.name}>
              <TextField
                fullWidth
                label={field.label}
                type={field.type}
                value={formData[field.name] || ''}
                onChange={(e) => handleFormChange(field.name, e.target.value)}
                variant="outlined"
              />
            </Grid>
          ))}
        </Grid>
        <Box sx={{ mt: 3, display: 'flex', gap: 2 }}>
          <Button
            variant="contained"
            startIcon={<AutoAwesomeIcon />}
            onClick={handleGenerateDocument}
            disabled={isGenerating}
            size="large"
          >
            {isGenerating ? (
              <>
                <CircularProgress size={20} sx={{ mr: 1 }} />
                Generating...
              </>
            ) : (
              'Generate Document'
            )}
          </Button>
        </Box>
      </Paper>
    );
  };

  return (
    <PageLayout>
      <Container maxWidth="lg" sx={{ py: 4 }}>
        {/* Hero Section */}
        <Box sx={{ textAlign: 'center', mb: 6 }}>
          <Typography variant="h2" component="h1" gutterBottom sx={{ fontWeight: 'bold' }}>
            Document Generation
          </Typography>
          <Typography variant="h5" color="text.secondary" sx={{ mb: 3 }}>
            Create professional legal documents with AI assistance
          </Typography>
          <Alert severity="info" sx={{ maxWidth: 600, mx: 'auto' }}>
            <Typography variant="body2">
              <strong>Free to use!</strong> Generate professional legal documents without any login required. 
              All documents are created using industry-standard templates and best practices.
            </Typography>
          </Alert>
        </Box>

        {/* Features */}
        <Grid container spacing={3} sx={{ mb: 6 }}>
          <Grid item xs={12} md={4}>
            <Card sx={{ height: '100%', textAlign: 'center', p: 2 }}>
              <CardContent>
                <AutoAwesomeIcon sx={{ fontSize: 48, color: 'primary.main', mb: 2 }} />
                <Typography variant="h6" gutterBottom>
                  AI-Powered
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Advanced AI technology ensures accurate and professional document generation
                </Typography>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} md={4}>
            <Card sx={{ height: '100%', textAlign: 'center', p: 2 }}>
              <CardContent>
                <SecurityIcon sx={{ fontSize: 48, color: 'success.main', mb: 2 }} />
                <Typography variant="h6" gutterBottom>
                  Secure & Private
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Your information is protected with bank-level security and privacy
                </Typography>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} md={4}>
            <Card sx={{ height: '100%', textAlign: 'center', p: 2 }}>
              <CardContent>
                <CheckCircleIcon sx={{ fontSize: 48, color: 'info.main', mb: 2 }} />
                <Typography variant="h6" gutterBottom>
                  Legal Compliance
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  All templates follow current legal standards and best practices
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        </Grid>

        <Grid container spacing={4}>
          {/* Template Selection */}
          <Grid item xs={12} md={6}>
            <Card>
              <CardHeader title="Choose a Template" />
              <CardContent>
                <FormControl fullWidth sx={{ mb: 2 }}>
                  <InputLabel>Quick Select Template</InputLabel>
                  <Select
                    value={selectedTemplate || ''}
                    onChange={(e) => handleTemplateSelect(e.target.value)}
                    label="Quick Select Template"
                  >
                    {documentTemplates.map((template) => (
                      <MenuItem key={template.id} value={template.id}>
                        {template.name}
                      </MenuItem>
                    ))}
                  </Select>
                </FormControl>
                <Divider sx={{ my: 2 }} />
                <Grid container spacing={2}>
                  {documentTemplates.map((template) => (
                    <Grid item xs={12} key={template.id}>
                      <Card
                        sx={{
                          cursor: 'pointer',
                          border: selectedTemplate === template.id ? 2 : 1,
                          borderColor: selectedTemplate === template.id ? 'primary.main' : 'divider',
                          '&:hover': { borderColor: 'primary.main' }
                        }}
                        onClick={() => handleTemplateSelect(template.id)}
                      >
                        <CardContent>
                          <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                            {template.icon}
                            <Box sx={{ flex: 1 }}>
                              <Typography variant="h6">{template.name}</Typography>
                              <Typography variant="body2" color="text.secondary">
                                {template.description}
                              </Typography>
                              <Chip
                                label={template.category}
                                size="small"
                                sx={{ mt: 1 }}
                                color="primary"
                                variant="outlined"
                              />
                            </Box>
                          </Box>
                        </CardContent>
                      </Card>
                    </Grid>
                  ))}
                </Grid>
              </CardContent>
            </Card>
          </Grid>

          {/* Form and Generation */}
          <Grid item xs={12} md={6}>
            {renderFormFields()}
            
            <Paper sx={{ p: 2, mt: 2 }}>
              <Typography variant="h6" gutterBottom>
                Document Features:
              </Typography>
              <List dense>
                <ListItem>
                  <ListItemIcon>
                    <CheckCircleIcon color="success" />
                  </ListItemIcon>
                  <ListItemText primary="Professional formatting" />
                </ListItem>
                <ListItem>
                  <ListItemIcon>
                    <CheckCircleIcon color="success" />
                  </ListItemIcon>
                  <ListItemText primary="Legal compliance" />
                </ListItem>
                <ListItem>
                  <ListItemIcon>
                    <CheckCircleIcon color="success" />
                  </ListItemIcon>
                  <ListItemText primary="Instant download" />
                </ListItem>
              </List>
            </Paper>
            
            {generatedDocument && (
              <Paper sx={{ p: 3, mt: 2, bgcolor: 'success.light', color: 'success.contrastText' }}>
                <Typography variant="h6" gutterBottom>
                  Document Generated Successfully!
                </Typography>
                <Typography variant="body2" sx={{ mb: 2 }}>
                  Your document "{generatedDocument.name}" has been created and is ready for download.
                </Typography>
                <Button
                  variant="contained"
                  startIcon={<DownloadIcon />}
                  sx={{ bgcolor: 'white', color: 'success.main', '&:hover': { bgcolor: 'grey.100' } }}
                >
                  Download Document
                </Button>
              </Paper>
            )}
          </Grid>
        </Grid>

        {/* How it Works */}
        <Box sx={{ mt: 6 }}>
          <Typography variant="h4" gutterBottom sx={{ textAlign: 'center', mb: 4 }}>
            How It Works
          </Typography>
          <Grid container spacing={3}>
            <Grid item xs={12} md={4}>
              <Box sx={{ textAlign: 'center' }}>
                <Box sx={{ 
                  width: 60, 
                  height: 60, 
                  borderRadius: '50%', 
                  bgcolor: 'primary.main', 
                  color: 'white',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  mx: 'auto',
                  mb: 2
                }}>
                  <Typography variant="h4" sx={{ fontWeight: 'bold' }}>1</Typography>
                </Box>
                <Typography variant="h6" gutterBottom>Choose Template</Typography>
                <Typography variant="body2" color="text.secondary">
                  Select from our library of professional legal document templates
                </Typography>
              </Box>
            </Grid>
            <Grid item xs={12} md={4}>
              <Box sx={{ textAlign: 'center' }}>
                <Box sx={{ 
                  width: 60, 
                  height: 60, 
                  borderRadius: '50%', 
                  bgcolor: 'primary.main', 
                  color: 'white',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  mx: 'auto',
                  mb: 2
                }}>
                  <Typography variant="h4" sx={{ fontWeight: 'bold' }}>2</Typography>
                </Box>
                <Typography variant="h6" gutterBottom>Fill Information</Typography>
                <Typography variant="body2" color="text.secondary">
                  Provide the required information using our simple form
                </Typography>
                <Box sx={{ mt: 2 }}>
                  <EditIcon color="primary" sx={{ mr: 1 }} />
                  <SaveIcon color="primary" />
                </Box>
              </Box>
            </Grid>
            <Grid item xs={12} md={4}>
              <Box sx={{ textAlign: 'center' }}>
                <Box sx={{ 
                  width: 60, 
                  height: 60, 
                  borderRadius: '50%', 
                  bgcolor: 'primary.main', 
                  color: 'white',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  mx: 'auto',
                  mb: 2
                }}>
                  <Typography variant="h4" sx={{ fontWeight: 'bold' }}>3</Typography>
                </Box>
                <Typography variant="h6" gutterBottom>Download Document</Typography>
                <Typography variant="body2" color="text.secondary">
                  Get your professionally formatted legal document instantly
                </Typography>
              </Box>
            </Grid>
          </Grid>
        </Box>
      </Container>
    </PageLayout>
  );
};

export default DocumentGenerationPage;
