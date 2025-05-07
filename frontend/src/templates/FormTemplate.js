import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Container, Grid, Paper, Typography, TextField, Button, Divider,
  Box, Stepper, Step, StepLabel, StepContent, Alert, Snackbar,
  CircularProgress, LinearProgress
} from '@mui/material';
import { useFormik } from 'formik';
import * as Yup from 'yup';
import { format } from 'date-fns';
import DocumentPreview from '../components/DocumentPreview';
import ApiService from '../services/ApiService';
import useFormDraft from '../hooks/useFormDraft';
import useFormAutoSave from '../hooks/useFormAutoSave';
import useFormValidation from '../hooks/useFormValidation';
import useFormAnalytics from '../hooks/useFormAnalytics';
import AutorenewIcon from '@mui/icons-material/Autorenew';
import PauseIcon from '@mui/icons-material/Pause';

/**
 * Template for creating new forms with standardized patterns and features.
 * To use this template:
 * 1. Copy this file and rename it to your form name
 * 2. Replace FORM_TYPE with your form's type (e.g., 'small_claims')
 * 3. Update validationSchema with your form's fields
 * 4. Update initialValues with your form's fields
 * 5. Update steps array with your form's steps
 * 6. Update getStepFields to match your steps
 */

// Validation schema using Yup
const validationSchema = Yup.object().shape({
  // Add your form fields validation here
  field_1: Yup.string().required('Field 1 is required'),
  field_2: Yup.number().required('Field 2 is required').min(0, 'Must be positive'),
  // ... add more fields
});

const FormTemplate = () => {
  const navigate = useNavigate();
  const [activeStep, setActiveStep] = useState(0);
  const [previewData, setPreviewData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [snackbar, setSnackbar] = useState({
    open: false,
    message: '',
    severity: 'success'
  });

  // Initial form values
  const initialValues = {
    field_1: '',
    field_2: '',
    // ... add more fields
  };

  // Initialize form hooks
  const {
    values,
    setValues,
    lastSaved,
    isSaving,
    saveDraft,
    clearDraft,
    calculateCompletion
  } = useFormDraft('FORM_TYPE', initialValues);

  const {
    autoSaveEnabled,
    toggleAutoSave
  } = useFormAutoSave('FORM_TYPE', values, initialValues);

  const {
    formik,
    fieldErrors,
    isSubmitting,
    submitError,
    validateField,
    validateForm,
    getFieldError,
    hasFieldError
  } = useFormValidation('FORM_TYPE', values, validationSchema, async (values) => {
    try {
      const response = await ApiService.post('/api/templates/generate', {
        template_id: 'FORM_TYPE',
        data: values
      });
      
      // Clear draft on successful submission
      clearDraft();
      
      // Track form completion
      await trackFormCompletion();
      
      // Navigate to documents page with success message
      navigate('/documents', { 
        state: { 
          success: true, 
          message: 'Form submitted successfully',
          documentId: response.data.document_id 
        }
      });
    } catch (err) {
      throw new Error(err.message || 'Failed to generate document');
    }
  });

  const {
    trackFormStart,
    trackFormCompletion,
    trackFieldInteraction,
    trackFieldTiming,
    trackFormAbandonment,
    trackFormError,
    getFormAnalytics
  } = useFormAnalytics('FORM_TYPE');

  // Start tracking when form loads
  useEffect(() => {
    trackFormStart();
    
    // Track form abandonment
    const handleBeforeUnload = (e) => {
      if (!formik.isSubmitting && calculateCompletion() < 100) {
        trackFormAbandonment(calculateCompletion());
      }
    };
    
    window.addEventListener('beforeunload', handleBeforeUnload);
    return () => {
      window.removeEventListener('beforeunload', handleBeforeUnload);
      if (!formik.isSubmitting && calculateCompletion() < 100) {
        trackFormAbandonment(calculateCompletion());
      }
    };
  }, []);

  // Track field interactions and timing
  const handleFieldChange = (e) => {
    const { name, value } = e.target;
    const startTime = formik.values[`${name}_start_time`] || Date.now();
    
    formik.handleChange(e);
    trackFieldInteraction(name, value);
    
    // Track field timing
    if (!formik.values[name] && value) {
      formik.setFieldValue(`${name}_start_time`, startTime);
    } else if (formik.values[name] && !value) {
      trackFieldTiming(name, Date.now() - startTime);
      formik.setFieldValue(`${name}_start_time`, null);
    }
  };

  // Handle step navigation
  const handleNext = () => {
    const stepFields = getStepFields(activeStep);
    const hasErrors = stepFields.some(field => hasFieldError(field));
    
    if (!hasErrors) {
      setActiveStep((prevStep) => prevStep + 1);
    } else {
      setSnackbar({
        open: true,
        message: 'Please fix the errors before proceeding',
        severity: 'error'
      });
    }
  };

  const handleBack = () => {
    setActiveStep((prevStep) => prevStep - 1);
  };

  const handleStepClick = (step) => {
    if (step < activeStep) {
      setActiveStep(step);
    }
  };

  // Get fields for current step validation
  const getStepFields = (step) => {
    switch (step) {
      case 0:
        return ['field_1'];
      case 1:
        return ['field_2'];
      // ... add more steps
      default:
        return [];
    }
  };

  // Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();
    if (await validateForm()) {
      try {
        await formik.submitForm();
      } catch (err) {
        trackFormError('submit', err.message);
        setError(err.message);
      }
    }
  };

  // Handle form preview
  const handlePreview = () => {
    validateForm().then(isValid => {
      if (isValid) {
        setPreviewData(formik.values);
      } else {
        setSnackbar({
          open: true,
          message: 'Please fix form errors before preview',
          severity: 'error'
        });
      }
    });
  };

  // Handle draft saving
  const handleSaveDraft = async () => {
    try {
      await saveDraft();
      setSnackbar({
        open: true,
        message: 'Draft saved successfully',
        severity: 'success'
      });
    } catch (err) {
      setSnackbar({
        open: true,
        message: 'Failed to save draft',
        severity: 'error'
      });
    }
  };

  // Close snackbar
  const handleSnackbarClose = () => {
    setSnackbar(prev => ({ ...prev, open: false }));
  };

  // Form steps
  const steps = [
    {
      label: 'Step 1',
      content: (
        <Grid container spacing={2}>
          <Grid item xs={12}>
            <TextField
              fullWidth
              label="Field 1"
              name="field_1"
              value={formik.values.field_1}
              onChange={handleFieldChange}
              onBlur={formik.handleBlur}
              error={formik.touched.field_1 && Boolean(formik.errors.field_1)}
              helperText={formik.touched.field_1 && formik.errors.field_1}
              margin="normal"
            />
          </Grid>
        </Grid>
      )
    },
    {
      label: 'Step 2',
      content: (
        <Grid container spacing={2}>
          <Grid item xs={12}>
            <TextField
              fullWidth
              label="Field 2"
              name="field_2"
              type="number"
              value={formik.values.field_2}
              onChange={handleFieldChange}
              onBlur={formik.handleBlur}
              error={formik.touched.field_2 && Boolean(formik.errors.field_2)}
              helperText={formik.touched.field_2 && formik.errors.field_2}
              margin="normal"
            />
          </Grid>
        </Grid>
      )
    }
    // ... add more steps
  ];

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Paper elevation={3} sx={{ p: 3 }}>
        <Typography variant="h4" gutterBottom>
          Form Template
        </Typography>
        <Divider sx={{ mb: 3 }} />
        
        {/* Form Progress */}
        <Box sx={{ mb: 3 }}>
          <Typography variant="subtitle1" gutterBottom>
            Form Progress: {calculateCompletion()}%
          </Typography>
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
            <Box sx={{ flexGrow: 1 }}>
              <LinearProgress 
                variant="determinate" 
                value={calculateCompletion()} 
                sx={{ height: 8, borderRadius: 4 }}
              />
            </Box>
            <Button
              size="small"
              onClick={toggleAutoSave}
              color={autoSaveEnabled ? 'primary' : 'inherit'}
              startIcon={autoSaveEnabled ? <AutorenewIcon /> : <PauseIcon />}
            >
              Auto-save {autoSaveEnabled ? 'On' : 'Off'}
            </Button>
          </Box>
          {lastSaved && (
            <Typography variant="caption" color="text.secondary">
              Last saved: {format(new Date(lastSaved), 'PPpp')}
            </Typography>
          )}
        </Box>
        
        {/* Validation Summary */}
        {Object.keys(formik.errors).length > 0 && (
          <Alert severity="warning" sx={{ mb: 3 }}>
            <Typography variant="subtitle2" gutterBottom>
              Please fix the following errors:
            </Typography>
            <ul>
              {Object.entries(formik.errors).map(([field, error]) => (
                <li key={field}>
                  {field}: {error}
                </li>
              ))}
            </ul>
          </Alert>
        )}
        
        {error && (
          <Alert severity="error" sx={{ mb: 3 }}>
            {error}
          </Alert>
        )}
        
        <Grid container spacing={3}>
          <Grid item xs={12} md={8}>
            <Stepper activeStep={activeStep} orientation="vertical">
              {steps.map((step, index) => (
                <Step key={step.label}>
                  <StepLabel 
                    onClick={() => handleStepClick(index)}
                    sx={{ cursor: 'pointer' }}
                  >
                    {step.label}
                  </StepLabel>
                  <StepContent>
                    <Box sx={{ mb: 2 }}>
                      {step.content}
                    </Box>
                    <Box sx={{ mb: 2, display: 'flex', gap: 1 }}>
                      <Button
                        disabled={activeStep === 0}
                        onClick={handleBack}
                        variant="outlined"
                      >
                        Back
                      </Button>
                      <Button
                        variant="contained"
                        onClick={activeStep === steps.length - 1 ? handleSubmit : handleNext}
                        disabled={loading || isSubmitting}
                      >
                        {activeStep === steps.length - 1 ? 'Submit' : 'Next'}
                        {(loading || isSubmitting) && activeStep === steps.length - 1 && (
                          <CircularProgress size={24} sx={{ ml: 1 }} />
                        )}
                      </Button>
                      <Button
                        variant="outlined"
                        color="secondary"
                        onClick={handleSaveDraft}
                        disabled={isSaving}
                      >
                        Save Draft
                        {isSaving && <CircularProgress size={24} sx={{ ml: 1 }} />}
                      </Button>
                      {activeStep === steps.length - 1 && (
                        <Button
                          variant="outlined"
                          color="info"
                          onClick={handlePreview}
                          disabled={loading || isSubmitting}
                        >
                          Preview
                        </Button>
                      )}
                    </Box>
                  </StepContent>
                </Step>
              ))}
            </Stepper>
          </Grid>
          
          {previewData && (
            <Grid item xs={12} md={4}>
              <DocumentPreview
                templateId="FORM_TYPE"
                data={previewData}
                title="Document Preview"
                realTimePreview={true}
              />
            </Grid>
          )}
        </Grid>
      </Paper>

      <Snackbar
        open={snackbar.open}
        autoHideDuration={6000}
        onClose={handleSnackbarClose}
        message={snackbar.message}
        severity={snackbar.severity}
      />
    </Container>
  );
};

export default FormTemplate; 