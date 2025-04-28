import React, { useState } from 'react';
import { 
  Container, Grid, Paper, Typography, TextField, Button, Divider,
  Box, Stepper, Step, StepLabel, StepContent, Alert
} from '@mui/material';
import { useFormik } from 'formik';
import * as Yup from 'yup';
import { format } from 'date-fns';
import DocumentPreview from '../components/DocumentPreview';

// Validation schema using Yup
const validationSchema = Yup.object().shape({
  // Court Information
  court_county: Yup.string().required('County is required'),
  court_state: Yup.string().required('State is required'),
  
  // Plaintiff Information
  plaintiff_name: Yup.string().required('Plaintiff name is required'),
  plaintiff_address: Yup.string().required('Plaintiff address is required'),
  
  // Defendant Information
  defendant_name: Yup.string().required('Defendant name is required'),
  defendant_address: Yup.string().required('Defendant address is required'),
  
  // Claim Information
  claim_amount: Yup.number()
    .required('Claim amount is required')
    .positive('Claim amount must be positive')
    .max(10000, 'Claim amount must not exceed small claims limit'),
  
  claim_description: Yup.string()
    .required('Claim description is required')
    .min(20, 'Please provide more details in your claim description'),
  
  // Optional Fields
  case_number: Yup.string()
    .matches(/^[A-Za-z0-9-]*$/, 'Only alphanumeric characters and hyphens are allowed'),
  
  incident_location: Yup.string(),
  
  incident_date: Yup.date()
    .max(new Date(), 'Incident date cannot be in the future'),
  
  filing_date: Yup.date()
    .required('Filing date is required')
    .max(new Date(), 'Filing date cannot be in the future'),
  
  filing_fee: Yup.number()
    .positive('Filing fee must be positive'),
    
  // Facts
  fact_1: Yup.string().required('At least one fact is required'),
  fact_2: Yup.string(),
  fact_3: Yup.string(),
  
  // Evidence and Witnesses
  evidence_list: Yup.string(),
  witness_list: Yup.string()
});

const SmallClaimsComplaintForm = () => {
  const [activeStep, setActiveStep] = useState(0);
  const [previewData, setPreviewData] = useState(null);

  const initialValues = {
    court_county: '',
    court_state: '',
    plaintiff_name: '',
    plaintiff_address: '',
    defendant_name: '',
    defendant_address: '',
    claim_amount: '',
    claim_description: '',
    case_number: '',
    incident_location: '',
    incident_date: format(new Date(), 'yyyy-MM-dd'),
    filing_date: format(new Date(), 'yyyy-MM-dd'),
    filing_fee: '',
    fact_1: '',
    fact_2: '',
    fact_3: '',
    evidence_list: '',
    witness_list: ''
  };

  const formik = useFormik({
    initialValues,
    validationSchema,
    onSubmit: (values) => {
      console.log('Form submitted:', values);
      setPreviewData(values);
    }
  });

  const steps = [
    {
      label: 'Court Information',
      content: (
        <Grid container spacing={2}>
          <Grid item xs={12} md={6}>
            <TextField
              fullWidth
              label="Court County"
              name="court_county"
              value={formik.values.court_county}
              onChange={formik.handleChange}
              onBlur={formik.handleBlur}
              error={formik.touched.court_county && Boolean(formik.errors.court_county)}
              helperText={formik.touched.court_county && formik.errors.court_county}
              margin="normal"
            />
          </Grid>
          <Grid item xs={12} md={6}>
            <TextField
              fullWidth
              label="Court State"
              name="court_state"
              value={formik.values.court_state}
              onChange={formik.handleChange}
              onBlur={formik.handleBlur}
              error={formik.touched.court_state && Boolean(formik.errors.court_state)}
              helperText={formik.touched.court_state && formik.errors.court_state}
              margin="normal"
            />
          </Grid>
          <Grid item xs={12}>
            <TextField
              fullWidth
              label="Case Number (Optional)"
              name="case_number"
              value={formik.values.case_number}
              onChange={formik.handleChange}
              onBlur={formik.handleBlur}
              error={formik.touched.case_number && Boolean(formik.errors.case_number)}
              helperText={formik.touched.case_number && formik.errors.case_number}
              margin="normal"
            />
          </Grid>
        </Grid>
      )
    },
    {
      label: 'Party Information',
      content: (
        <Grid container spacing={2}>
          <Grid item xs={12}>
            <Typography variant="h6">Plaintiff</Typography>
          </Grid>
          <Grid item xs={12} md={6}>
            <TextField
              fullWidth
              label="Plaintiff Name"
              name="plaintiff_name"
              value={formik.values.plaintiff_name}
              onChange={formik.handleChange}
              onBlur={formik.handleBlur}
              error={formik.touched.plaintiff_name && Boolean(formik.errors.plaintiff_name)}
              helperText={formik.touched.plaintiff_name && formik.errors.plaintiff_name}
              margin="normal"
            />
          </Grid>
          <Grid item xs={12} md={6}>
            <TextField
              fullWidth
              label="Plaintiff Address"
              name="plaintiff_address"
              value={formik.values.plaintiff_address}
              onChange={formik.handleChange}
              onBlur={formik.handleBlur}
              error={formik.touched.plaintiff_address && Boolean(formik.errors.plaintiff_address)}
              helperText={formik.touched.plaintiff_address && formik.errors.plaintiff_address}
              margin="normal"
            />
          </Grid>
          
          <Grid item xs={12}>
            <Divider sx={{ my: 2 }} />
            <Typography variant="h6">Defendant</Typography>
          </Grid>
          <Grid item xs={12} md={6}>
            <TextField
              fullWidth
              label="Defendant Name"
              name="defendant_name"
              value={formik.values.defendant_name}
              onChange={formik.handleChange}
              onBlur={formik.handleBlur}
              error={formik.touched.defendant_name && Boolean(formik.errors.defendant_name)}
              helperText={formik.touched.defendant_name && formik.errors.defendant_name}
              margin="normal"
            />
          </Grid>
          <Grid item xs={12} md={6}>
            <TextField
              fullWidth
              label="Defendant Address"
              name="defendant_address"
              value={formik.values.defendant_address}
              onChange={formik.handleChange}
              onBlur={formik.handleBlur}
              error={formik.touched.defendant_address && Boolean(formik.errors.defendant_address)}
              helperText={formik.touched.defendant_address && formik.errors.defendant_address}
              margin="normal"
            />
          </Grid>
        </Grid>
      )
    },
    {
      label: 'Claim Information',
      content: (
        <Grid container spacing={2}>
          <Grid item xs={12} md={6}>
            <TextField
              fullWidth
              label="Claim Amount ($)"
              name="claim_amount"
              type="number"
              value={formik.values.claim_amount}
              onChange={formik.handleChange}
              onBlur={formik.handleBlur}
              error={formik.touched.claim_amount && Boolean(formik.errors.claim_amount)}
              helperText={formik.touched.claim_amount && formik.errors.claim_amount}
              margin="normal"
              inputProps={{ step: '0.01' }}
            />
          </Grid>
          <Grid item xs={12} md={6}>
            <TextField
              fullWidth
              label="Filing Fee (Optional)"
              name="filing_fee"
              type="number"
              value={formik.values.filing_fee}
              onChange={formik.handleChange}
              onBlur={formik.handleBlur}
              error={formik.touched.filing_fee && Boolean(formik.errors.filing_fee)}
              helperText={formik.touched.filing_fee && formik.errors.filing_fee}
              margin="normal"
              inputProps={{ step: '0.01' }}
            />
          </Grid>
          <Grid item xs={12} md={6}>
            <TextField
              fullWidth
              label="Incident Location"
              name="incident_location"
              value={formik.values.incident_location}
              onChange={formik.handleChange}
              onBlur={formik.handleBlur}
              error={formik.touched.incident_location && Boolean(formik.errors.incident_location)}
              helperText={formik.touched.incident_location && formik.errors.incident_location}
              margin="normal"
            />
          </Grid>
          <Grid item xs={12} md={6}>
            <TextField
              fullWidth
              label="Incident Date"
              name="incident_date"
              type="date"
              value={formik.values.incident_date}
              onChange={formik.handleChange}
              onBlur={formik.handleBlur}
              error={formik.touched.incident_date && Boolean(formik.errors.incident_date)}
              helperText={formik.touched.incident_date && formik.errors.incident_date}
              margin="normal"
              InputLabelProps={{ shrink: true }}
            />
          </Grid>
          <Grid item xs={12}>
            <TextField
              fullWidth
              label="Filing Date"
              name="filing_date"
              type="date"
              value={formik.values.filing_date}
              onChange={formik.handleChange}
              onBlur={formik.handleBlur}
              error={formik.touched.filing_date && Boolean(formik.errors.filing_date)}
              helperText={formik.touched.filing_date && formik.errors.filing_date}
              margin="normal"
              InputLabelProps={{ shrink: true }}
            />
          </Grid>
          <Grid item xs={12}>
            <TextField
              fullWidth
              multiline
              rows={4}
              label="Claim Description"
              name="claim_description"
              value={formik.values.claim_description}
              onChange={formik.handleChange}
              onBlur={formik.handleBlur}
              error={formik.touched.claim_description && Boolean(formik.errors.claim_description)}
              helperText={formik.touched.claim_description && formik.errors.claim_description}
              margin="normal"
            />
          </Grid>
        </Grid>
      )
    },
    {
      label: 'Facts, Evidence, and Witnesses',
      content: (
        <Grid container spacing={2}>
          <Grid item xs={12}>
            <Typography variant="h6">Facts</Typography>
            <Alert severity="info" sx={{ mb: 2 }}>
              Please provide at least one fact supporting your claim
            </Alert>
          </Grid>
          <Grid item xs={12}>
            <TextField
              fullWidth
              multiline
              rows={2}
              label="Fact 1"
              name="fact_1"
              value={formik.values.fact_1}
              onChange={formik.handleChange}
              onBlur={formik.handleBlur}
              error={formik.touched.fact_1 && Boolean(formik.errors.fact_1)}
              helperText={formik.touched.fact_1 && formik.errors.fact_1}
              margin="normal"
            />
          </Grid>
          <Grid item xs={12}>
            <TextField
              fullWidth
              multiline
              rows={2}
              label="Fact 2 (Optional)"
              name="fact_2"
              value={formik.values.fact_2}
              onChange={formik.handleChange}
              onBlur={formik.handleBlur}
              error={formik.touched.fact_2 && Boolean(formik.errors.fact_2)}
              helperText={formik.touched.fact_2 && formik.errors.fact_2}
              margin="normal"
            />
          </Grid>
          <Grid item xs={12}>
            <TextField
              fullWidth
              multiline
              rows={2}
              label="Fact 3 (Optional)"
              name="fact_3"
              value={formik.values.fact_3}
              onChange={formik.handleChange}
              onBlur={formik.handleBlur}
              error={formik.touched.fact_3 && Boolean(formik.errors.fact_3)}
              helperText={formik.touched.fact_3 && formik.errors.fact_3}
              margin="normal"
            />
          </Grid>
          
          <Grid item xs={12}>
            <Divider sx={{ my: 2 }} />
            <Typography variant="h6">Evidence (Optional)</Typography>
          </Grid>
          <Grid item xs={12}>
            <TextField
              fullWidth
              multiline
              rows={4}
              label="Evidence List"
              name="evidence_list"
              value={formik.values.evidence_list}
              onChange={formik.handleChange}
              onBlur={formik.handleBlur}
              error={formik.touched.evidence_list && Boolean(formik.errors.evidence_list)}
              helperText={
                (formik.touched.evidence_list && formik.errors.evidence_list) ||
                "List any evidence (documents, photos, etc.) that supports your claim"
              }
              margin="normal"
            />
          </Grid>
          
          <Grid item xs={12}>
            <Divider sx={{ my: 2 }} />
            <Typography variant="h6">Witnesses (Optional)</Typography>
          </Grid>
          <Grid item xs={12}>
            <TextField
              fullWidth
              multiline
              rows={4}
              label="Witness List"
              name="witness_list"
              value={formik.values.witness_list}
              onChange={formik.handleChange}
              onBlur={formik.handleBlur}
              error={formik.touched.witness_list && Boolean(formik.errors.witness_list)}
              helperText={
                (formik.touched.witness_list && formik.errors.witness_list) ||
                "List any witnesses who can testify to the facts of your claim"
              }
              margin="normal"
            />
          </Grid>
        </Grid>
      )
    }
  ];

  const handleNext = () => {
    setActiveStep((prevActiveStep) => prevActiveStep + 1);
  };

  const handleBack = () => {
    setActiveStep((prevActiveStep) => prevActiveStep - 1);
  };

  const handleStepClick = (step) => {
    setActiveStep(step);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    formik.handleSubmit();
  };

  const handlePreview = () => {
    formik.validateForm().then(errors => {
      if (Object.keys(errors).length === 0) {
        setPreviewData(formik.values);
      } else {
        // Mark all fields as touched to show validation errors
        Object.keys(formik.values).forEach(key => {
          formik.setFieldTouched(key, true);
        });
      }
    });
  };

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Typography variant="h4" component="h1" gutterBottom>
        Small Claims Complaint Form
      </Typography>
      
      <Grid container spacing={3}>
        <Grid item xs={12} md={7}>
          <Paper elevation={3} sx={{ p: 3 }}>
            <form onSubmit={handleSubmit}>
              <Stepper activeStep={activeStep} orientation="vertical">
                {steps.map((step, index) => (
                  <Step key={step.label}>
                    <StepLabel onClick={() => handleStepClick(index)} style={{ cursor: 'pointer' }}>
                      {step.label}
                    </StepLabel>
                    <StepContent>
                      {step.content}
                      <Box sx={{ mb: 2, mt: 2 }}>
                        <div>
                          <Button
                            variant="contained"
                            onClick={index === steps.length - 1 ? handlePreview : handleNext}
                            sx={{ mt: 1, mr: 1 }}
                          >
                            {index === steps.length - 1 ? 'Preview Document' : 'Continue'}
                          </Button>
                          <Button
                            disabled={index === 0}
                            onClick={handleBack}
                            sx={{ mt: 1, mr: 1 }}
                          >
                            Back
                          </Button>
                        </div>
                      </Box>
                    </StepContent>
                  </Step>
                ))}
              </Stepper>
              
              {activeStep === steps.length && (
                <Box sx={{ mt: 3 }}>
                  <Typography variant="h6" gutterBottom>
                    All steps completed - you're finished
                  </Typography>
                  <Button onClick={() => setActiveStep(0)} sx={{ mt: 1, mr: 1 }}>
                    Edit Information
                  </Button>
                  <Button
                    variant="contained"
                    color="primary"
                    type="submit"
                    sx={{ mt: 1, mr: 1 }}
                  >
                    Generate Final Document
                  </Button>
                </Box>
              )}
            </form>
          </Paper>
        </Grid>
        
        <Grid item xs={12} md={5}>
          <Box sx={{ position: 'sticky', top: 20, height: 'calc(100vh - 150px)' }}>
            <DocumentPreview 
              templateId="small_claims_complaint"
              data={previewData}
              title="Small Claims Complaint Preview"
            />
          </Box>
        </Grid>
      </Grid>
    </Container>
  );
};

export default SmallClaimsComplaintForm; 