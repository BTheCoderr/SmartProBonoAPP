import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Container, Grid, Paper, Typography, TextField, Button, Divider,
  Box, Stepper, Step, StepLabel, StepContent, Alert, MenuItem,
  FormControl, FormControlLabel, Checkbox, RadioGroup, Radio, FormLabel,
  CircularProgress, Snackbar, LinearProgress, Tooltip, IconButton
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
  fullName: Yup.string()
    .required('Full name is required')
    .min(2, 'Name must be at least 2 characters'),
  address: Yup.string()
    .required('Address is required'),
  phone: Yup.string()
    .required('Phone number is required')
    .matches(/^[0-9-+()]*$/, 'Invalid phone number format'),
  email: Yup.string()
    .email('Invalid email address')
    .required('Email is required'),
  caseNumber: Yup.string()
    .required('Case number is required'),
  employmentStatus: Yup.string()
    .required('Employment status is required'),
  monthlyIncome: Yup.number()
    .required('Monthly income is required')
    .min(0, 'Income cannot be negative'),
  householdSize: Yup.number()
    .required('Household size is required')
    .min(1, 'Must be at least 1')
    .integer('Must be a whole number'),
  publicBenefits: Yup.array()
    .of(Yup.string()),
  expenses: Yup.object().shape({
    rent: Yup.number().min(0, 'Cannot be negative'),
    utilities: Yup.number().min(0, 'Cannot be negative'),
    food: Yup.number().min(0, 'Cannot be negative'),
    medical: Yup.number().min(0, 'Cannot be negative'),
    other: Yup.number().min(0, 'Cannot be negative'),
  }),
  declaration: Yup.boolean()
    .oneOf([true], 'You must declare that the information is true'),
});

const FeeWaiverRequestForm = () => {
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
  } = useFormValidation('fee_waiver', {
    fullName: '',
    address: '',
    phone: '',
    email: '',
    caseNumber: '',
    employmentStatus: '',
    monthlyIncome: '',
    householdSize: '',
    publicBenefits: [],
    expenses: {
      rent: '',
      utilities: '',
      food: '',
      medical: '',
      other: '',
    },
    declaration: false,
  }, validationSchema);

  // Auto-save functionality
  const { draftId, saveDraft, loadDraft } = useFormDraft('fee_waiver');
  const { startAutoSave, stopAutoSave } = useFormAutoSave(formik.values, saveDraft);

  // Analytics tracking
  const { trackFormProgress, trackFieldCompletion } = useFormAnalytics('fee_waiver');

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

  const handleCheckboxChange = async (e) => {
    const { name, checked } = e.target;
    formik.setFieldValue(name, checked);
    const isValid = await validateField(name, checked);
    if (isValid) {
      trackFieldCompletion(name);
    }
  };

  const handleExpenseChange = async (expense, value) => {
    const name = `expenses.${expense}`;
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
      fullName: 'Enter your full legal name (minimum 2 characters)',
      address: 'Enter your current mailing address',
      phone: 'Enter a valid phone number',
      email: 'Enter a valid email address',
      caseNumber: 'Enter the case number for which you are requesting a fee waiver',
      employmentStatus: 'Select your current employment status',
      monthlyIncome: 'Enter your total monthly income from all sources',
      householdSize: 'Enter the number of people in your household',
      'expenses.rent': 'Enter your monthly rent or mortgage payment',
      'expenses.utilities': 'Enter your monthly utilities cost',
      'expenses.food': 'Enter your monthly food expenses',
      'expenses.medical': 'Enter your monthly medical expenses',
      'expenses.other': 'Enter any other monthly expenses',
      declaration: 'You must declare that all information provided is true and accurate',
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

  // Form steps
  const steps = [
    {
      label: 'Personal Information',
      content: (
        <Grid container spacing={2}>
          <Grid item xs={12}>
            {renderField('fullName', 'Full Name')}
            {renderField('address', 'Address', 'text', true)}
            {renderField('phone', 'Phone Number')}
            {renderField('email', 'Email Address')}
            {renderField('caseNumber', 'Case Number')}
          </Grid>
        </Grid>
      )
    },
    {
      label: 'Financial Information',
      content: (
        <Grid container spacing={2}>
          <Grid item xs={12}>
            <FormControl fullWidth sx={{ mb: 2 }}>
              <FormLabel>Employment Status</FormLabel>
              <RadioGroup
                name="employmentStatus"
                value={formik.values.employmentStatus}
                onChange={handleFieldChange}
              >
                <FormControlLabel value="employed" control={<Radio />} label="Employed" />
                <FormControlLabel value="unemployed" control={<Radio />} label="Unemployed" />
                <FormControlLabel value="retired" control={<Radio />} label="Retired" />
                <FormControlLabel value="disabled" control={<Radio />} label="Disabled" />
              </RadioGroup>
            </FormControl>
            {renderField('monthlyIncome', 'Monthly Income', 'number')}
            {renderField('householdSize', 'Household Size', 'number')}
          </Grid>
        </Grid>
      )
    },
    {
      label: 'Monthly Expenses',
      content: (
        <Grid container spacing={2}>
          <Grid item xs={12}>
            {renderField('expenses.rent', 'Rent/Mortgage', 'number')}
            {renderField('expenses.utilities', 'Utilities', 'number')}
            {renderField('expenses.food', 'Food', 'number')}
            {renderField('expenses.medical', 'Medical Expenses', 'number')}
            {renderField('expenses.other', 'Other Expenses', 'number')}
          </Grid>
        </Grid>
      )
    },
    {
      label: 'Declaration',
      content: (
        <Grid container spacing={2}>
          <Grid item xs={12}>
            <FormControlLabel
              control={
                <Checkbox
                  name="declaration"
                  checked={formik.values.declaration}
                  onChange={handleCheckboxChange}
                />
              }
              label="I declare under penalty of perjury that the information I have provided is true and correct."
            />
            {formik.touched.declaration && formik.errors.declaration && (
              <Typography color="error" variant="caption">
                {formik.errors.declaration}
              </Typography>
            )}
          </Grid>
        </Grid>
      )
    }
  ];

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Paper elevation={3} sx={{ p: 3 }}>
        <Typography variant="h4" gutterBottom>
          Fee Waiver Request Form
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
                index === 0 ? ['fullName', 'address', 'phone', 'email', 'caseNumber'].includes(field) :
                index === 1 ? ['employmentStatus', 'monthlyIncome', 'householdSize'].includes(field) :
                index === 2 ? field.startsWith('expenses.') :
                field === 'declaration'
              );
              const sectionComplete = sectionFields.every(field => 
                !getFieldError(field) && formik.touched[field]
              );
              return (
                <Grid item xs={3} key={index}>
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
            formType="fee_waiver"
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

export default FeeWaiverRequestForm; 