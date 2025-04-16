import React, { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import {
  Container,
  Typography,
  Button,
  Box,
  TextField,
  MenuItem,
  FormControl,
  FormControlLabel,
  Checkbox,
  InputLabel,
  Select,
  Stepper,
  Step,
  StepLabel,
  CircularProgress,
  Divider,
  Alert,
  IconButton,
  Paper,
  useMediaQuery,
  FormLabel,
  RadioGroup,
  Radio,
  Snackbar,
} from '@mui/material';
import { useTheme } from '@mui/material/styles';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import DescriptionIcon from '@mui/icons-material/Description';
import InfoIcon from '@mui/icons-material/Info';
import HelpOutlineIcon from '@mui/icons-material/HelpOutline';
import DownloadIcon from '@mui/icons-material/Download';
import axios from 'axios';
import { getTemplateFormSchema, fetchTemplateFormSchema, validateDocumentForm } from '../utils/documentUtils';
import { documentTemplates } from '../data/documentTemplates';
const DocumentFormPage = () => {
  const { t } = useTranslation();
  const { templateId } = useParams();
  const navigate = useNavigate();
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('sm'));
  // Find the template from the template library
  const template = documentTemplates.find(t => t.id === templateId);
  // State
  const [activeStep, setActiveStep] = useState(0);
  const [formData, setFormData] = useState({});
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [errors, setErrors] = useState({});
  const [formSchema, setFormSchema] = useState(null);
  const [showSignUpBanner, setShowSignUpBanner] = useState(false);
  // Fetch form schema and initialize data
  useEffect(() => {
    const loadSchema = async () => {
      try {
        // Try to fetch schema from API first
        const schema = await fetchTemplateFormSchema(templateId);
        setFormSchema(schema);
        
        // Initialize form data with default values
        const initialData = {};
        if (schema && schema.sections) {
          schema.sections.forEach(section => {
            section.fields.forEach(field => {
              // Set default values based on field type
              if (field.type === 'checkbox') {
                initialData[field.id] = field.defaultValue || false;
              } else if (field.defaultValue !== undefined) {
                initialData[field.id] = field.defaultValue;
              } else {
                initialData[field.id] = '';
              }
            });
          });
          setFormData(initialData);
        }
      } catch (error) {
        console.error('Error loading template schema:', error);
        // Load synchronous fallback if API fails
        const fallbackSchema = getTemplateFormSchema(templateId);
        setFormSchema(fallbackSchema);
      }
    };
    
    loadSchema();
  }, [templateId]);
  // Validate form when data changes
  useEffect(() => {
    // Define validateForm function inside useEffect to avoid dependency issues
    const validateForm = () => {
      if (!formSchema || !formSchema.sections || activeStep >= formSchema.sections.length) {
        return true;
      }
      return validateSection(activeStep);
    };
    
    if (formData && Object.keys(formData).length > 0 && formSchema) {
      validateForm();
    }
  }, [formData, formSchema, activeStep, validateSection]);
  // If template not found, show error
  if (!template) {
    return (
      <Container maxWidth="md" sx={{ py: 4 }}>
        <Alert severity="error">
          {t(
            'Template not found. Please return to the template library and select a valid template.'
          )}
        </Alert>
        <Box mt={2}>
          <Button
            variant="contained"
            startIcon={<ArrowBackIcon />}
            onClick={() => navigate('/document-templates')}
          >
            {t('Back to Templates')}
          </Button>
        </Box>
      </Container>
    );
  }
  // If form schema is not loaded yet, show loading
  if (!formSchema) {
    return (
      <Container maxWidth="md" sx={{ py: 4, textAlign: 'center' }}>
        <CircularProgress />
        <Typography variant="body1" sx={{ mt: 2 }}>
          {t('Loading template form...')}
        </Typography>
      </Container>
    );
  }
  // Handle input change
  const handleChange = event => {
    const { name, value, checked, type } = event.target;
    setFormData({
      ...formData,
      [name]: type === 'checkbox' ? checked : value,
    });
    // Clear error for this field if it exists
    if (errors[name]) {
      setErrors(prev => {
        const newErrors = { ...prev };
        delete newErrors[name];
        return newErrors;
      });
    }
  };
  // Validate current section
  const validateSection = sectionIndex => {
    const section = formSchema.sections[sectionIndex, validateSection];
    const newErrors = {};
    let isValid = true;
    section.fields.forEach(field => {
      if (field.required) {
        const value = formData[field.id];
        if (
          value === '' ||
          value === null ||
          value === undefined ||
          (field.type === 'checkbox' && !value)
        ) {
          newErrors[field.id] = t('This field is required');
          isValid = false;
        }
      }
    });
    setErrors(newErrors);
    return isValid;
  };
  // Handle next step
  const handleNext = () => {
    if (validateSection(activeStep)) {
      setActiveStep(prevStep => prevStep + 1);
      window.scrollTo(0, 0);
    }
  };
  // Handle back step
  const handleBack = () => {
    setActiveStep(prevStep => prevStep - 1);
    window.scrollTo(0, 0);
  };
  // Handle form submission
  const handleSubmit = async () => {
    if (validateSection(activeStep)) {
      setIsSubmitting(true);
      try {
        // Validate the entire form
        const validation = await validateDocumentForm(formData, templateId);
        
        if (!validation.isValid) {
          setErrors(validation.errors);
          setIsSubmitting(false);
          return;
        }
        
        // Submit to API
        const response = await axios.post('/api/documents/generate', {
          template_id: templateId,
          form_data: formData
        });
        
        // Handle successful document generation
        if (response.data && response.data.document_id) {
          // Download the document
          window.location.href = `/api/documents/download/${response.data.document_id}`;
          
          // Navigate to success page
          navigate('/document-generator/success', { 
            state: { 
              documentId: response.data.document_id,
              templateId: templateId,
              formData: formData
            } 
          });
        } else {
          throw new Error('Invalid response from server');
        }
      } catch (error) {
        console.error('Error generating document:', error);
        setErrors({
          _general: 'Failed to generate document. Please try again or contact support.'
        });
      } finally {
        setIsSubmitting(false);
      }
    }
  };
  // Render field based on type
  const renderField = field => {
    switch (field.type) {
      case 'text':
      case 'email':
      case 'tel':
      case 'date':
        return (
          <TextField
            fullWidth
            id={field.id}
            name={field.id}
            label={field.label}
            type={field.type}
            value={formData[field.id] || ''}
            onChange={handleChange}
            error={!!errors[field.id]}
            helperText={errors[field.id] || field.helpText}
            required={field.required}
            placeholder={field.placeholder || ''}
            margin="normal"
            InputProps={{
              endAdornment: field.helpText ? (
                <IconButton size="small" title={field.helpText}>
                  <HelpOutlineIcon fontSize="small" />
                </IconButton>
              ) : null,
            }}
          />
        );
      case 'textarea':
        return (
          <TextField
            fullWidth
            id={field.id}
            name={field.id}
            label={field.label}
            value={formData[field.id] || ''}
            onChange={handleChange}
            error={!!errors[field.id]}
            helperText={errors[field.id] || field.helpText}
            required={field.required}
            placeholder={field.placeholder || ''}
            margin="normal"
            multiline
            rows={4}
          />
        );
      case 'select':
        return (
          <FormControl
            fullWidth
            margin="normal"
            error={!!errors[field.id]}
            required={field.required}
          >
            <InputLabel id={`${field.id}-label`}>{field.label}</InputLabel>
            <Select
              labelId={`${field.id}-label`}
              id={field.id}
              name={field.id}
              value={formData[field.id] || ''}
              onChange={handleChange}
              label={field.label}
            >
              {field.options.map(option => (
                <MenuItem key={option.value} value={option.value}>
                  {option.label}
                </MenuItem>
              ))}
            </Select>
            {(errors[field.id] || field.helpText) && (
              <Typography variant="caption" color={errors[field.id] ? 'error' : 'text.secondary'}>
                {errors[field.id] || field.helpText}
              </Typography>
            )}
          </FormControl>
        );
      case 'radio':
        return (
          <FormControl
            component="fieldset"
            margin="normal"
            error={!!errors[field.id]}
            required={field.required}
          >
            <FormLabel component="legend">{field.label}</FormLabel>
            <RadioGroup name={field.id} value={formData[field.id] || ''} onChange={handleChange}>
              {field.options.map(option => (
                <FormControlLabel
                  key={option.value}
                  value={option.value}
                  control={<Radio />}
                  label={option.label}
                />
              ))}
            </RadioGroup>
            {(errors[field.id] || field.helpText) && (
              <Typography variant="caption" color={errors[field.id] ? 'error' : 'text.secondary'}>
                {errors[field.id] || field.helpText}
              </Typography>
            )}
          </FormControl>
        );
      case 'checkbox':
        return (
          <FormControl
            component="fieldset"
            margin="normal"
            error={!!errors[field.id]}
            required={field.required}
          >
            <FormControlLabel
              control={
                <Checkbox name={field.id} checked={!!formData[field.id]} onChange={handleChange} />
              }
              label={field.label}
            />
            {(errors[field.id] || field.helpText) && (
              <Typography variant="caption" color={errors[field.id] ? 'error' : 'text.secondary'}>
                {errors[field.id] || field.helpText}
              </Typography>
            )}
          </FormControl>
        );
      default:
        return null;
    }
  };
  // Current section
  const currentSection = formSchema.sections[activeStep];
  const handleSignUpBannerClose = () => {
    setShowSignUpBanner(false);
  };
  return (
    <Container maxWidth="md" sx={{ py: 4 }}>
      {showSignUpBanner && (
        <Alert severity="info" sx={{ mb: 3 }} onClose={handleSignUpBannerClose}>
          <Typography variant="subtitle1" gutterBottom>
            You&apos;re using this template in demo mode
          </Typography>
          <Typography variant="body2">
            Create a free account to save your progress, access your documents later, and get
            notifications about important deadlines.
          </Typography>
          <Box mt={1}>
            <Button
              variant="outlined"
              size="small"
              color="primary"
              onClick={() =>
                navigate(
                  '/register?redirect=' +
                    encodeURIComponent(`/document-templates/form/${templateId}`)
                )
              }
              sx={{ mr: 1 }}
            >
              Create Account
            </Button>
            <Button variant="text" size="small" onClick={handleSignUpBannerClose}>
              Continue in Demo Mode
            </Button>
          </Box>
        </Alert>
      )}
      <Box display="flex" alignItems="center" mb={3}>
        <IconButton onClick={() => navigate('/document-templates')} sx={{ mr: 1 }}>
          <ArrowBackIcon />
        </IconButton>
        <Typography variant="h4" component="h1">
          {template.name}
        </Typography>
      </Box>
      <Paper sx={{ p: { xs: 2, md: 4 }, mb: 4 }}>
        <Box display="flex" alignItems="center" mb={3}>
          <DescriptionIcon color="primary" sx={{ mr: 2, fontSize: 40 }} />
          <Box>
            <Typography variant="h6">{t('Document Template Form')}</Typography>
            <Typography variant="body2" color="text.secondary">
              {t('Fill out the form to generate your document')}
            </Typography>
          </Box>
        </Box>
        <Stepper
          activeStep={activeStep}
          alternativeLabel={!isMobile}
          orientation={isMobile ? 'vertical' : 'horizontal'}
          sx={{ mb: 4 }}
        >
          {formSchema.sections.map((section, index) => (
            <Step key={section.title}>
              <StepLabel>{section.title}</StepLabel>
            </Step>
          ))}
        </Stepper>
        <Divider sx={{ mb: 4 }} />
        <Box mb={4}>
          <Typography variant="h5" gutterBottom>
            {currentSection.title}
          </Typography>
          <Typography variant="body2" color="text.secondary" paragraph>
            {currentSection.description}
          </Typography>
          {currentSection.fields.map(field => (
            <Box key={field.id} mb={2}>
              {renderField(field)}
            </Box>
          ))}
        </Box>
        <Box display="flex" justifyContent="space-between">
          <Button variant="outlined" onClick={handleBack} disabled={activeStep === 0}>
            {t('Back')}
          </Button>
          {activeStep === formSchema.sections.length - 1 ? (
            <Button
              variant="contained"
              color="primary"
              onClick={handleSubmit}
              disabled={isSubmitting}
              startIcon={isSubmitting && <CircularProgress size={20} />}
            >
              {isSubmitting ? t('Generating...') : t('Generate Document')}
            </Button>
          ) : (
            <Button variant="contained" color="primary" onClick={handleNext}>
              {t('Next')}
            </Button>
          )}
        </Box>
      </Paper>
      <Box mb={4}>
        <Alert severity="info" icon={<InfoIcon />}>
          <Typography variant="body2">
            {t(
              'This document template will help you create a basic document. For complex legal matters, please consult with a qualified legal professional.'
            )}
          </Typography>
        </Alert>
      </Box>
    </Container>
  );
};
export default DocumentFormPage;