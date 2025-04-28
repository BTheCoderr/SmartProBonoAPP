import React, { useState } from 'react';
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
  CircularProgress
} from '@mui/material';
import { useFormik } from 'formik';
import * as Yup from 'yup';
import ApiService from '../services/ApiService';

const steps = ['Case Information', 'Your Response', 'Defenses', 'Review & Submit'];

const EvictionResponseForm = () => {
  const navigate = useNavigate();
  const [activeStep, setActiveStep] = useState(0);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const validationSchema = Yup.object({
    case_number: Yup.string().required('Case number is required'),
    court_county: Yup.string().required('Court county is required'),
    tenant_name: Yup.string().required('Your name is required'),
    tenant_address: Yup.string().required('Your address is required'),
    landlord_name: Yup.string().required('Landlord name is required'),
    eviction_notice_date: Yup.date().required('Notice date is required'),
    response_type: Yup.string().required('Response type is required'),
    defenses: Yup.array().min(1, 'Select at least one defense'),
    additional_facts: Yup.string(),
    relief_requested: Yup.string().required('Relief requested is required')
  });

  const formik = useFormik({
    initialValues: {
      case_number: '',
      court_county: '',
      tenant_name: '',
      tenant_address: '',
      landlord_name: '',
      eviction_notice_date: '',
      response_type: 'general_denial',
      defenses: [],
      additional_facts: '',
      relief_requested: ''
    },
    validationSchema,
    onSubmit: async (values) => {
      setLoading(true);
      setError(null);
      try {
        const response = await ApiService.post('/api/templates/generate', {
          template_id: 'eviction_response',
          data: values
        });
        
        // Handle successful form submission
        navigate('/documents', { 
          state: { 
            success: true, 
            message: 'Eviction Response form generated successfully',
            documentId: response.data.document_id 
          }
        });
      } catch (err) {
        setError(err.message || 'Failed to generate document');
        setLoading(false);
      }
    }
  });

  const handleNext = () => {
    if (activeStep === steps.length - 1) {
      formik.submitForm();
    } else {
      setActiveStep((prevStep) => prevStep + 1);
    }
  };

  const handleBack = () => {
    setActiveStep((prevStep) => prevStep - 1);
  };

  const getStepContent = (step) => {
    switch (step) {
      case 0:
        return (
          <Grid container spacing={3}>
            <Grid item xs={12}>
              <TextField
                fullWidth
                name="case_number"
                label="Case Number"
                value={formik.values.case_number}
                onChange={formik.handleChange}
                error={formik.touched.case_number && Boolean(formik.errors.case_number)}
                helperText={formik.touched.case_number && formik.errors.case_number}
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                fullWidth
                name="court_county"
                label="Court County"
                value={formik.values.court_county}
                onChange={formik.handleChange}
                error={formik.touched.court_county && Boolean(formik.errors.court_county)}
                helperText={formik.touched.court_county && formik.errors.court_county}
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
                name="tenant_name"
                label="Your Full Name"
                value={formik.values.tenant_name}
                onChange={formik.handleChange}
                error={formik.touched.tenant_name && Boolean(formik.errors.tenant_name)}
                helperText={formik.touched.tenant_name && formik.errors.tenant_name}
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                fullWidth
                name="tenant_address"
                label="Your Address"
                value={formik.values.tenant_address}
                onChange={formik.handleChange}
                error={formik.touched.tenant_address && Boolean(formik.errors.tenant_address)}
                helperText={formik.touched.tenant_address && formik.errors.tenant_address}
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                fullWidth
                name="landlord_name"
                label="Landlord's Name"
                value={formik.values.landlord_name}
                onChange={formik.handleChange}
                error={formik.touched.landlord_name && Boolean(formik.errors.landlord_name)}
                helperText={formik.touched.landlord_name && formik.errors.landlord_name}
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                fullWidth
                type="date"
                name="eviction_notice_date"
                label="Date of Eviction Notice"
                InputLabelProps={{ shrink: true }}
                value={formik.values.eviction_notice_date}
                onChange={formik.handleChange}
                error={formik.touched.eviction_notice_date && Boolean(formik.errors.eviction_notice_date)}
                helperText={formik.touched.eviction_notice_date && formik.errors.eviction_notice_date}
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
                  onChange={formik.handleChange}
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
                </RadioGroup>
              </FormControl>
            </Grid>
            <Grid item xs={12}>
              <TextField
                fullWidth
                multiline
                rows={4}
                name="additional_facts"
                label="Additional Facts (Optional)"
                value={formik.values.additional_facts}
                onChange={formik.handleChange}
                error={formik.touched.additional_facts && Boolean(formik.errors.additional_facts)}
                helperText={formik.touched.additional_facts && formik.errors.additional_facts}
              />
            </Grid>
          </Grid>
        );

      case 3:
        return (
          <Grid container spacing={3}>
            <Grid item xs={12}>
              <TextField
                fullWidth
                multiline
                rows={4}
                name="relief_requested"
                label="Relief Requested"
                value={formik.values.relief_requested}
                onChange={formik.handleChange}
                error={formik.touched.relief_requested && Boolean(formik.errors.relief_requested)}
                helperText={formik.touched.relief_requested && formik.errors.relief_requested}
              />
            </Grid>
          </Grid>
        );

      default:
        return 'Unknown step';
    }
  };

  return (
    <Container maxWidth="md" sx={{ mb: 4 }}>
      <Paper elevation={3} sx={{ p: 4, mt: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom align="center">
          Eviction Response Form
        </Typography>
        
        <Stepper activeStep={activeStep} sx={{ pt: 3, pb: 5 }}>
          {steps.map((label) => (
            <Step key={label}>
              <StepLabel>{label}</StepLabel>
            </Step>
          ))}
        </Stepper>

        {error && (
          <Alert severity="error" sx={{ mb: 2 }}>
            {error}
          </Alert>
        )}

        <form onSubmit={formik.handleSubmit}>
          {getStepContent(activeStep)}

          <Box sx={{ display: 'flex', justifyContent: 'flex-end', mt: 3 }}>
            {activeStep !== 0 && (
              <Button onClick={handleBack} sx={{ mr: 1 }}>
                Back
              </Button>
            )}
            <Button
              variant="contained"
              onClick={handleNext}
              disabled={loading}
            >
              {loading ? (
                <CircularProgress size={24} />
              ) : activeStep === steps.length - 1 ? (
                'Submit'
              ) : (
                'Next'
              )}
            </Button>
          </Box>
        </form>
      </Paper>
    </Container>
  );
};

export default EvictionResponseForm; 