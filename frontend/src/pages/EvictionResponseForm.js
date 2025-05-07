import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Container,
  Paper,
  Typography,
  Stepper,
  Step,
  StepLabel,
  Button,
  Box,
  Grid,
  TextField,
  FormControl,
  FormLabel,
  RadioGroup,
  FormControlLabel,
  Radio,
  Alert,
  CircularProgress,
  Divider,
  Snackbar,
  LinearProgress,
  FormHelperText,
  Checkbox
} from '@mui/material';
import { useFormik } from 'formik';
import * as Yup from 'yup';
import { format } from 'date-fns';
import ApiService from '../services/ApiService';
import useFormDraft from '../hooks/useFormDraft';
import useFormAutoSave from '../hooks/useFormAutoSave';
import useFormValidation from '../hooks/useFormValidation';
import useFormAnalytics from '../hooks/useFormAnalytics';
import DocumentPreview from '../components/DocumentPreview';
import AutorenewIcon from '@mui/icons-material/Autorenew';
import PauseIcon from '@mui/icons-material/Pause';

const steps = [
  'Case Information',
  'Personal Information',
  'Response Details',
  'Defenses',
  'Additional Information',
  'Review & Submit'
];

const EvictionResponseForm = () => {
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

  const validationSchema = Yup.object({
    case_number: Yup.string()
      .required('Case number is required')
      .matches(/^[0-9A-Z-]+$/, 'Invalid case number format'),
    court_county: Yup.string()
      .required('Court county is required')
      .min(2, 'County name must be at least 2 characters'),
    tenant_name: Yup.string()
      .required('Your name is required')
      .min(2, 'Name must be at least 2 characters'),
    tenant_address: Yup.string()
      .required('Your address is required')
      .min(5, 'Please enter a complete address'),
    landlord_name: Yup.string()
      .required('Landlord name is required')
      .min(2, 'Name must be at least 2 characters'),
    eviction_notice_date: Yup.date()
      .required('Notice date is required')
      .max(new Date(), 'Date cannot be in the future'),
    response_type: Yup.string()
      .required('Response type is required')
      .oneOf(['general_denial', 'specific_denial', 'partial_admission'], 'Invalid response type'),
    defenses: Yup.array()
      .of(Yup.string())
      .min(1, 'Select at least one defense'),
    defense_explanation: Yup.string()
      .when('defenses', {
        is: (defenses) => defenses && defenses.length > 0,
        then: Yup.string().required('Please explain your selected defenses')
      }),
    additional_facts: Yup.string()
      .min(10, 'Please provide more details'),
    relief_requested: Yup.string()
      .required('Relief requested is required')
      .min(10, 'Please provide more details about the relief you are seeking'),
    rent_payment_history: Yup.string()
      .required('Rent payment history is required'),
    maintenance_issues: Yup.string(),
    notice_defects: Yup.string(),
    declaration: Yup.boolean()
      .oneOf([true], 'You must declare that all information is true and accurate')
  });

  const initialValues = {
    case_number: '',
    court_county: '',
    tenant_name: '',
    tenant_address: '',
    landlord_name: '',
    eviction_notice_date: '',
    response_type: 'general_denial',
    defenses: [],
    defense_explanation: '',
    additional_facts: '',
    relief_requested: '',
    rent_payment_history: '',
    maintenance_issues: '',
    notice_defects: '',
    declaration: false
  };

  const {
    values,
    setValues,
    lastSaved,
    isSaving,
    saveDraft,
    clearDraft,
    calculateCompletion
  } = useFormDraft('eviction_response', initialValues);

  const {
    autoSaveEnabled,
    toggleAutoSave
  } = useFormAutoSave('eviction_response', values, initialValues);

  const {
    formik,
    fieldErrors,
    isSubmitting,
    submitError,
    validateField,
    validateForm,
    getFieldError,
    hasFieldError
  } = useFormValidation('eviction_response', values, validationSchema, async (values) => {
    try {
      const response = await ApiService.post('/api/templates/generate', {
        template_id: 'eviction_response',
        data: values
      });
      
      clearDraft();
      
      navigate('/documents', { 
        state: { 
          success: true, 
          message: 'Eviction Response form submitted successfully',
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
    trackFormError,
    trackFormAbandonment,
    trackFieldTiming
  } = useFormAnalytics('eviction_response');

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

  const getStepFields = (step) => {
    switch (step) {
      case 0:
        return ['case_number', 'court_county'];
      case 1:
        return ['tenant_name', 'tenant_address', 'landlord_name', 'eviction_notice_date'];
      case 2:
        return ['response_type', 'rent_payment_history'];
      case 3:
        return ['defenses'];
      case 4:
        return ['maintenance_issues', 'notice_defects', 'additional_facts'];
      case 5:
        return ['relief_requested'];
      default:
        return [];
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (await validateForm()) {
      try {
        await formik.submitForm();
        await trackFormCompletion();
      } catch (err) {
        trackFormError('submit', err.message);
        setError(err.message);
      }
    }
  };

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

  const handleSnackbarClose = () => {
    setSnackbar(prev => ({ ...prev, open: false }));
  };

  const getStepContent = (step) => {
    switch (step) {
      case 0:
        return (
          <Grid container spacing={3}>
            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                label="Case Number"
                name="case_number"
                value={formik.values.case_number}
                onChange={handleFieldChange}
                error={formik.touched.case_number && Boolean(formik.errors.case_number)}
                helperText={formik.touched.case_number && formik.errors.case_number}
              />
            </Grid>
            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                label="Court County"
                name="court_county"
                value={formik.values.court_county}
                onChange={handleFieldChange}
                error={formik.touched.court_county && Boolean(formik.errors.court_county)}
                helperText={formik.touched.court_county && formik.errors.court_county}
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                fullWidth
                type="date"
                label="Eviction Notice Date"
                name="eviction_notice_date"
                value={formik.values.eviction_notice_date}
                onChange={handleFieldChange}
                error={formik.touched.eviction_notice_date && Boolean(formik.errors.eviction_notice_date)}
                helperText={formik.touched.eviction_notice_date && formik.errors.eviction_notice_date}
                InputLabelProps={{ shrink: true }}
              />
            </Grid>
          </Grid>
        );

      case 1:
        return (
          <Grid container spacing={3}>
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Your Full Name"
                name="tenant_name"
                value={formik.values.tenant_name}
                onChange={handleFieldChange}
                error={formik.touched.tenant_name && Boolean(formik.errors.tenant_name)}
                helperText={formik.touched.tenant_name && formik.errors.tenant_name}
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Your Address"
                name="tenant_address"
                multiline
                rows={3}
                value={formik.values.tenant_address}
                onChange={handleFieldChange}
                error={formik.touched.tenant_address && Boolean(formik.errors.tenant_address)}
                helperText={formik.touched.tenant_address && formik.errors.tenant_address}
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Landlord's Name"
                name="landlord_name"
                value={formik.values.landlord_name}
                onChange={handleFieldChange}
                error={formik.touched.landlord_name && Boolean(formik.errors.landlord_name)}
                helperText={formik.touched.landlord_name && formik.errors.landlord_name}
              />
            </Grid>
          </Grid>
        );

      case 2:
        return (
          <Grid container spacing={3}>
            <Grid item xs={12}>
              <FormControl component="fieldset">
                <FormLabel component="legend">Type of Response</FormLabel>
                <RadioGroup
                  name="response_type"
                  value={formik.values.response_type}
                  onChange={handleFieldChange}
                >
                  <FormControlLabel
                    value="general_denial"
                    control={<Radio />}
                    label="General Denial - Deny all allegations"
                  />
                  <FormControlLabel
                    value="specific_denial"
                    control={<Radio />}
                    label="Specific Denial - Deny specific allegations"
                  />
                  <FormControlLabel
                    value="partial_admission"
                    control={<Radio />}
                    label="Partial Admission - Admit some allegations but deny others"
                  />
                </RadioGroup>
              </FormControl>
            </Grid>
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Rent Payment History"
                name="rent_payment_history"
                multiline
                rows={4}
                value={formik.values.rent_payment_history}
                onChange={handleFieldChange}
                error={formik.touched.rent_payment_history && Boolean(formik.errors.rent_payment_history)}
                helperText={formik.touched.rent_payment_history && formik.errors.rent_payment_history}
              />
            </Grid>
          </Grid>
        );

      case 3:
        return (
          <Grid container spacing={3}>
            <Grid item xs={12}>
              <FormControl component="fieldset" error={formik.touched.defenses && Boolean(formik.errors.defenses)}>
                <FormLabel component="legend">Select Your Defenses</FormLabel>
                <Grid container spacing={2}>
                  {availableDefenses.map((defense) => (
                    <Grid item xs={12} sm={6} key={defense.value}>
                      <FormControlLabel
                        control={
                          <Checkbox
                            checked={formik.values.defenses.includes(defense.value)}
                            onChange={(e) => {
                              const newDefenses = e.target.checked
                                ? [...formik.values.defenses, defense.value]
                                : formik.values.defenses.filter(d => d !== defense.value);
                              formik.setFieldValue('defenses', newDefenses);
                            }}
                          />
                        }
                        label={defense.label}
                      />
                    </Grid>
                  ))}
                </Grid>
                {formik.touched.defenses && formik.errors.defenses && (
                  <FormHelperText>{formik.errors.defenses}</FormHelperText>
                )}
              </FormControl>
            </Grid>
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Explain Your Defenses"
                name="defense_explanation"
                multiline
                rows={4}
                value={formik.values.defense_explanation}
                onChange={handleFieldChange}
                error={formik.touched.defense_explanation && Boolean(formik.errors.defense_explanation)}
                helperText={formik.touched.defense_explanation && formik.errors.defense_explanation}
              />
            </Grid>
          </Grid>
        );

      case 4:
        return (
          <Grid container spacing={3}>
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Maintenance Issues"
                name="maintenance_issues"
                multiline
                rows={4}
                value={formik.values.maintenance_issues}
                onChange={handleFieldChange}
                error={formik.touched.maintenance_issues && Boolean(formik.errors.maintenance_issues)}
                helperText={formik.touched.maintenance_issues && formik.errors.maintenance_issues}
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Notice Defects"
                name="notice_defects"
                multiline
                rows={4}
                value={formik.values.notice_defects}
                onChange={handleFieldChange}
                error={formik.touched.notice_defects && Boolean(formik.errors.notice_defects)}
                helperText={formik.touched.notice_defects && formik.errors.notice_defects}
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Additional Facts"
                name="additional_facts"
                multiline
                rows={4}
                value={formik.values.additional_facts}
                onChange={handleFieldChange}
                error={formik.touched.additional_facts && Boolean(formik.errors.additional_facts)}
                helperText={formik.touched.additional_facts && formik.errors.additional_facts}
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Relief Requested"
                name="relief_requested"
                multiline
                rows={4}
                value={formik.values.relief_requested}
                onChange={handleFieldChange}
                error={formik.touched.relief_requested && Boolean(formik.errors.relief_requested)}
                helperText={formik.touched.relief_requested && formik.errors.relief_requested}
              />
            </Grid>
          </Grid>
        );

      case 5:
        return (
          <Grid container spacing={3}>
            <Grid item xs={12}>
              <Paper elevation={2} sx={{ p: 3 }}>
                <Typography variant="h6" gutterBottom>Review Your Information</Typography>
                <Grid container spacing={2}>
                  <Grid item xs={12}>
                    <FormControlLabel
                      control={
                        <Checkbox
                          name="declaration"
                          checked={formik.values.declaration}
                          onChange={handleFieldChange}
                        />
                      }
                      label="I declare under penalty of perjury that the information provided is true and correct."
                    />
                    {formik.touched.declaration && formik.errors.declaration && (
                      <FormHelperText error>{formik.errors.declaration}</FormHelperText>
                    )}
                  </Grid>
                  <Grid item xs={12}>
                    <Button
                      variant="outlined"
                      onClick={handlePreview}
                      disabled={!formik.isValid}
                    >
                      Preview Document
                    </Button>
                  </Grid>
                </Grid>
              </Paper>
            </Grid>
          </Grid>
        );

      default:
        return null;
    }
  };

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Paper elevation={3} sx={{ p: 3 }}>
        <Typography variant="h4" gutterBottom>
          Eviction Response Form
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
        
        {/* Add Validation Summary */}
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
                <Step key={step}>
                  <StepLabel 
                    onClick={() => handleStepClick(index)}
                    sx={{ cursor: 'pointer' }}
                  >
                    {step}
                  </StepLabel>
                  <StepContent>
                    <Box sx={{ mb: 2 }}>
                      {getStepContent(index)}
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
                data={previewData}
                onClose={() => setPreviewData(null)}
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

export default EvictionResponseForm; 