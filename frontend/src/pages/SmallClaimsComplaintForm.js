import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  Container, Grid, Paper, Typography, TextField, Button, Divider,
  Box, Stepper, Step, StepLabel, StepContent, Alert, Snackbar,
  CircularProgress, LinearProgress, Tooltip, IconButton
} from '@mui/material';
import InfoIcon from '@mui/icons-material/Info';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import ErrorIcon from '@mui/icons-material/Error';
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

// Validation schema for the form
const validationSchema = Yup.object().shape({
  plaintiffName: Yup.string()
    .required('Plaintiff name is required')
    .min(2, 'Name must be at least 2 characters'),
  plaintiffAddress: Yup.string()
    .required('Plaintiff address is required'),
  defendantName: Yup.string()
    .required('Defendant name is required')
    .min(2, 'Name must be at least 2 characters'),
  defendantAddress: Yup.string()
    .required('Defendant address is required'),
  claimAmount: Yup.number()
    .required('Claim amount is required')
    .positive('Amount must be positive')
    .max(10000, 'Amount cannot exceed $10,000'),
  claimReason: Yup.string()
    .required('Reason for claim is required')
    .min(20, 'Please provide more details about your claim'),
  incidentDate: Yup.date()
    .required('Date of incident is required')
    .max(new Date(), 'Date cannot be in the future'),
  attemptedResolution: Yup.string()
    .required('Please describe attempts to resolve this dispute')
    .min(20, 'Please provide more details about resolution attempts'),
});

const SmallClaimsComplaintForm = () => {
  const navigate = useNavigate();
  const [activeStep, setActiveStep] = useState(0);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState(null);
  const [showPreview, setShowPreview] = useState(false);
  const [autoSaveEnabled, setAutoSaveEnabled] = useState(true);
  const [lastSaved, setLastSaved] = useState(null);
  const [completionStatus, setCompletionStatus] = useState({});

  // Initialize form with validation and auto-save
  const {
    formik,
    fieldErrors,
    validateField,
    validateForm,
    getFieldError,
    hasFieldError,
    getFormValidationStatus
  } = useFormValidation('small_claims', {
    plaintiffName: '',
    plaintiffAddress: '',
    defendantName: '',
    defendantAddress: '',
    claimAmount: '',
    claimReason: '',
    incidentDate: '',
    attemptedResolution: '',
  }, validationSchema);

  // Auto-save functionality
  const { draftId, saveDraft, loadDraft } = useFormDraft('small_claims');
  const { startAutoSave, stopAutoSave } = useFormAutoSave(formik.values, saveDraft);

  // Analytics tracking
  const { trackFormProgress, trackFieldCompletion } = useFormAnalytics('small_claims');

  useEffect(() => {
    if (autoSaveEnabled) {
      startAutoSave();
    } else {
      stopAutoSave();
    }
  }, [autoSaveEnabled, formik.values]);

  // Load draft on mount
  useEffect(() => {
    const loadSavedDraft = async () => {
      const draft = await loadDraft();
      if (draft) {
        formik.setValues(draft.data);
        setLastSaved(draft.lastSaved);
      }
    };
    loadSavedDraft();
  }, []);

  // Track form progress
  useEffect(() => {
    const status = getFormValidationStatus();
    setCompletionStatus(status);
    trackFormProgress(status.progress);
  }, [formik.values, fieldErrors]);

  const handleFieldChange = async (e) => {
    const { name, value } = e.target;
    formik.setFieldValue(name, value);
    const isValid = await validateField(name, value);
    if (isValid) {
      trackFieldCompletion(name);
    }
  };

  const toggleAutoSave = () => {
    setAutoSaveEnabled(!autoSaveEnabled);
  };

  const calculateCompletion = () => {
    return completionStatus.progress || 0;
  };

  // Field-level validation tooltip content
  const getFieldTooltip = (fieldName) => {
    const requirements = {
      plaintiffName: 'Enter your full legal name (minimum 2 characters)',
      plaintiffAddress: 'Enter your current mailing address',
      defendantName: 'Enter the full name of the person or business you are suing',
      defendantAddress: 'Enter the address where the defendant can be served',
      claimAmount: 'Enter the amount you are claiming (maximum $10,000)',
      claimReason: 'Describe why you are filing this claim (minimum 20 characters)',
      incidentDate: 'Enter the date when the incident occurred',
      attemptedResolution: 'Describe how you tried to resolve this dispute (minimum 20 characters)',
    };
    return requirements[fieldName];
  };

  // Render field with validation and tooltip
  const renderField = (name, label, type = 'text', multiline = false) => (
    <Box sx={{ position: 'relative', mb: 2 }}>
      <TextField
        fullWidth
        id={name}
        name={name}
        label={label}
        type={type}
        multiline={multiline}
        rows={multiline ? 4 : 1}
        value={formik.values[name]}
        onChange={handleFieldChange}
        onBlur={formik.handleBlur}
        error={formik.touched[name] && Boolean(formik.errors[name])}
        helperText={formik.touched[name] && formik.errors[name]}
      />
      <Tooltip title={getFieldTooltip(name)} placement="right">
        <IconButton
          size="small"
          sx={{
            position: 'absolute',
            right: -36,
            top: '50%',
            transform: 'translateY(-50%)',
          }}
        >
          {hasFieldError(name) ? (
            <ErrorIcon color="error" />
          ) : formik.touched[name] ? (
            <CheckCircleIcon color="success" />
          ) : (
            <InfoIcon color="primary" />
          )}
        </IconButton>
      </Tooltip>
    </Box>
  );

  // Form steps with sections
  const steps = [
    {
      label: 'Plaintiff Information',
      content: (
        <Grid container spacing={2}>
          <Grid item xs={12}>
            {renderField('plaintiffName', 'Your Full Name')}
            {renderField('plaintiffAddress', 'Your Address', 'text', true)}
          </Grid>
        </Grid>
      )
    },
    {
      label: 'Defendant Information',
      content: (
        <Grid container spacing={2}>
          <Grid item xs={12}>
            {renderField('defendantName', 'Defendant Name')}
            {renderField('defendantAddress', 'Defendant Address', 'text', true)}
          </Grid>
        </Grid>
      )
    },
    {
      label: 'Claim Details',
      content: (
        <Grid container spacing={2}>
          <Grid item xs={12}>
            {renderField('claimAmount', 'Claim Amount', 'number')}
            {renderField('claimReason', 'Reason for Claim', 'text', true)}
            {renderField('incidentDate', 'Date of Incident', 'date')}
            {renderField('attemptedResolution', 'Attempts to Resolve', 'text', true)}
          </Grid>
        </Grid>
      )
    }
  ];

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Paper elevation={3} sx={{ p: 3 }}>
        <Typography variant="h4" gutterBottom>
          Small Claims Complaint Form
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

        {/* Section Completion Indicators */}
        <Box sx={{ mb: 3 }}>
          <Typography variant="subtitle2" gutterBottom>
            Section Completion:
          </Typography>
          <Grid container spacing={1}>
            {steps.map((step, index) => {
              const sectionFields = Object.keys(formik.values).filter(field => 
                index === 0 ? field.includes('plaintiff') :
                index === 1 ? field.includes('defendant') :
                !field.includes('plaintiff') && !field.includes('defendant')
              );
              const sectionComplete = sectionFields.every(field => 
                !getFieldError(field) && formik.touched[field]
              );
              return (
                <Grid item xs={4} key={index}>
                  <Paper 
                    sx={{ 
                      p: 1, 
                      textAlign: 'center',
                      bgcolor: sectionComplete ? 'success.light' : 'grey.100'
                    }}
                  >
                    <Typography variant="body2">
                      {step.label}
                      {sectionComplete && (
                        <CheckCircleIcon 
                          sx={{ ml: 1, verticalAlign: 'middle', fontSize: 16 }}
                          color="success"
                        />
                      )}
                    </Typography>
                  </Paper>
                </Grid>
              );
            })}
          </Grid>
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

        {/* Form Steps */}
        <Stepper activeStep={activeStep} orientation="vertical">
          {steps.map((step, index) => (
            <Step key={index}>
              <StepLabel>{step.label}</StepLabel>
              <StepContent>
                <form onSubmit={formik.handleSubmit}>
                  {step.content}
                  <Box sx={{ mb: 2 }}>
                    <div>
                      <Button
                        variant="contained"
                        onClick={() => setActiveStep(index + 1)}
                        sx={{ mt: 1, mr: 1 }}
                        disabled={!formik.isValid}
                      >
                        Continue
                      </Button>
                      <Button
                        disabled={index === 0}
                        onClick={() => setActiveStep(index - 1)}
                        sx={{ mt: 1, mr: 1 }}
                      >
                        Back
                      </Button>
                    </div>
                  </Box>
                </form>
              </StepContent>
            </Step>
          ))}
        </Stepper>

        {/* Preview Button */}
        <Box sx={{ mt: 3, display: 'flex', justifyContent: 'flex-end' }}>
          <Button
            variant="outlined"
            onClick={() => setShowPreview(true)}
            disabled={!formik.isValid}
          >
            Preview Form
          </Button>
        </Box>

        {/* Document Preview Dialog */}
        {showPreview && (
          <DocumentPreview
            open={showPreview}
            onClose={() => setShowPreview(false)}
            formData={formik.values}
            formType="small_claims"
          />
        )}

        {/* Error Snackbar */}
        <Snackbar
          open={Boolean(error)}
          autoHideDuration={6000}
          onClose={() => setError(null)}
        >
          <Alert severity="error" onClose={() => setError(null)}>
            {error}
          </Alert>
        </Snackbar>
      </Paper>
    </Container>
  );
};

export default SmallClaimsComplaintForm; 