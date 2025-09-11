import React, { useState } from 'react';
import {
  Box,
  Paper,
  Typography,
  TextField,
  Button,
  Grid,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  FormControlLabel,
  Checkbox,
  Alert,
  CircularProgress,
  Stepper,
  Step,
  StepLabel,
  StepContent
} from '@mui/material';
import { DatePicker } from '@mui/x-date-pickers/DatePicker';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';
import virtualParalegalAPI from '../services/VirtualParalegalAPI';

const steps = [
  'Personal Information',
  'Legal Issue Details',
  'Financial Information',
  'Review & Submit'
];

const legalIssueTypes = [
  'Immigration',
  'Family Law',
  'Criminal Defense',
  'Civil Rights',
  'Employment Law',
  'Personal Injury',
  'Estate Planning',
  'Bankruptcy',
  'Real Estate',
  'Other'
];

const urgencyLevels = [
  { value: 'low', label: 'Low - Can wait several weeks' },
  { value: 'medium', label: 'Medium - Needs attention within 2 weeks' },
  { value: 'high', label: 'High - Urgent, needs immediate attention' },
  { value: 'emergency', label: 'Emergency - Critical situation' }
];

const incomeLevels = [
  { value: 'low', label: 'Low Income (Under $25,000)' },
  { value: 'medium', label: 'Medium Income ($25,000 - $75,000)' },
  { value: 'high', label: 'High Income (Over $75,000)' }
];

function ClientIntakeForm({ onSuccess, onCancel }) {
  const [activeStep, setActiveStep] = useState(0);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(false);

  const [formData, setFormData] = useState({
    // Personal Information
    first_name: '',
    last_name: '',
    email: '',
    phone: '',
    date_of_birth: null,
    street_address: '',
    city: '',
    state: '',
    zip_code: '',
    country: 'USA',
    
    // Legal Information
    legal_issue_type: '',
    case_description: '',
    urgency_level: 'medium',
    case_start_date: null,
    previous_legal_representation: false,
    previous_attorney_name: '',
    
    // Financial Information
    income_level: '',
    can_afford_legal_fees: null,
    needs_pro_bono: false,
    
    // Additional Information
    notes: ''
  });

  const handleInputChange = (field) => (event) => {
    const value = event.target.type === 'checkbox' ? event.target.checked : event.target.value;
    setFormData(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const handleDateChange = (field) => (date) => {
    setFormData(prev => ({
      ...prev,
      [field]: date
    }));
  };

  const handleNext = () => {
    setActiveStep((prevActiveStep) => prevActiveStep + 1);
  };

  const handleBack = () => {
    setActiveStep((prevActiveStep) => prevActiveStep - 1);
  };

  const handleSubmit = async () => {
    setLoading(true);
    setError('');

    try {
      // Prepare data for submission
      const submitData = {
        ...formData,
        date_of_birth: formData.date_of_birth ? formData.date_of_birth.toISOString().split('T')[0] : null,
        case_start_date: formData.case_start_date ? formData.case_start_date.toISOString().split('T')[0] : null
      };

      const result = await virtualParalegalAPI.createClientIntake(submitData);
      
      if (result) {
        setSuccess(true);
        if (onSuccess) {
          onSuccess(result);
        }
      } else {
        setError('Failed to submit intake form. Please try again.');
      }
    } catch (err) {
      setError(err.message || 'An error occurred while submitting the form.');
    } finally {
      setLoading(false);
    }
  };

  const renderPersonalInfo = () => (
    <Grid container spacing={3}>
      <Grid item xs={12} sm={6}>
        <TextField
          fullWidth
          label="First Name"
          value={formData.first_name}
          onChange={handleInputChange('first_name')}
          required
        />
      </Grid>
      <Grid item xs={12} sm={6}>
        <TextField
          fullWidth
          label="Last Name"
          value={formData.last_name}
          onChange={handleInputChange('last_name')}
          required
        />
      </Grid>
      <Grid item xs={12} sm={6}>
        <TextField
          fullWidth
          label="Email"
          type="email"
          value={formData.email}
          onChange={handleInputChange('email')}
          required
        />
      </Grid>
      <Grid item xs={12} sm={6}>
        <TextField
          fullWidth
          label="Phone"
          value={formData.phone}
          onChange={handleInputChange('phone')}
          required
        />
      </Grid>
      <Grid item xs={12} sm={6}>
        <LocalizationProvider dateAdapter={AdapterDateFns}>
          <DatePicker
            label="Date of Birth"
            value={formData.date_of_birth}
            onChange={handleDateChange('date_of_birth')}
            renderInput={(params) => <TextField {...params} fullWidth />}
          />
        </LocalizationProvider>
      </Grid>
      <Grid item xs={12} sm={6}>
        <TextField
          fullWidth
          label="Country"
          value={formData.country}
          onChange={handleInputChange('country')}
        />
      </Grid>
      <Grid item xs={12}>
        <TextField
          fullWidth
          label="Street Address"
          value={formData.street_address}
          onChange={handleInputChange('street_address')}
        />
      </Grid>
      <Grid item xs={12} sm={4}>
        <TextField
          fullWidth
          label="City"
          value={formData.city}
          onChange={handleInputChange('city')}
        />
      </Grid>
      <Grid item xs={12} sm={4}>
        <TextField
          fullWidth
          label="State"
          value={formData.state}
          onChange={handleInputChange('state')}
        />
      </Grid>
      <Grid item xs={12} sm={4}>
        <TextField
          fullWidth
          label="ZIP Code"
          value={formData.zip_code}
          onChange={handleInputChange('zip_code')}
        />
      </Grid>
    </Grid>
  );

  const renderLegalInfo = () => (
    <Grid container spacing={3}>
      <Grid item xs={12}>
        <FormControl fullWidth required>
          <InputLabel>Legal Issue Type</InputLabel>
          <Select
            value={formData.legal_issue_type}
            onChange={handleInputChange('legal_issue_type')}
            label="Legal Issue Type"
          >
            {legalIssueTypes.map((type) => (
              <MenuItem key={type} value={type}>
                {type}
              </MenuItem>
            ))}
          </Select>
        </FormControl>
      </Grid>
      <Grid item xs={12}>
        <TextField
          fullWidth
          label="Case Description"
          multiline
          rows={4}
          value={formData.case_description}
          onChange={handleInputChange('case_description')}
          required
          placeholder="Please provide a detailed description of your legal issue..."
        />
      </Grid>
      <Grid item xs={12} sm={6}>
        <FormControl fullWidth>
          <InputLabel>Urgency Level</InputLabel>
          <Select
            value={formData.urgency_level}
            onChange={handleInputChange('urgency_level')}
            label="Urgency Level"
          >
            {urgencyLevels.map((level) => (
              <MenuItem key={level.value} value={level.value}>
                {level.label}
              </MenuItem>
            ))}
          </Select>
        </FormControl>
      </Grid>
      <Grid item xs={12} sm={6}>
        <LocalizationProvider dateAdapter={AdapterDateFns}>
          <DatePicker
            label="When did this legal issue start?"
            value={formData.case_start_date}
            onChange={handleDateChange('case_start_date')}
            renderInput={(params) => <TextField {...params} fullWidth />}
          />
        </LocalizationProvider>
      </Grid>
      <Grid item xs={12}>
        <FormControlLabel
          control={
            <Checkbox
              checked={formData.previous_legal_representation}
              onChange={handleInputChange('previous_legal_representation')}
            />
          }
          label="Have you had previous legal representation for this matter?"
        />
      </Grid>
      {formData.previous_legal_representation && (
        <Grid item xs={12}>
          <TextField
            fullWidth
            label="Previous Attorney Name"
            value={formData.previous_attorney_name}
            onChange={handleInputChange('previous_attorney_name')}
          />
        </Grid>
      )}
    </Grid>
  );

  const renderFinancialInfo = () => (
    <Grid container spacing={3}>
      <Grid item xs={12}>
        <FormControl fullWidth>
          <InputLabel>Income Level</InputLabel>
          <Select
            value={formData.income_level}
            onChange={handleInputChange('income_level')}
            label="Income Level"
          >
            {incomeLevels.map((level) => (
              <MenuItem key={level.value} value={level.value}>
                {level.label}
              </MenuItem>
            ))}
          </Select>
        </FormControl>
      </Grid>
      <Grid item xs={12}>
        <Typography variant="h6" gutterBottom>
          Can you afford legal fees?
        </Typography>
        <FormControlLabel
          control={
            <Checkbox
              checked={formData.can_afford_legal_fees === true}
              onChange={() => setFormData(prev => ({ ...prev, can_afford_legal_fees: true }))}
            />
          }
          label="Yes, I can afford legal fees"
        />
        <FormControlLabel
          control={
            <Checkbox
              checked={formData.can_afford_legal_fees === false}
              onChange={() => setFormData(prev => ({ ...prev, can_afford_legal_fees: false }))}
            />
          }
          label="No, I need pro bono assistance"
        />
      </Grid>
      <Grid item xs={12}>
        <FormControlLabel
          control={
            <Checkbox
              checked={formData.needs_pro_bono}
              onChange={handleInputChange('needs_pro_bono')}
            />
          }
          label="I specifically need pro bono (free) legal assistance"
        />
      </Grid>
    </Grid>
  );

  const renderReview = () => (
    <Grid container spacing={3}>
      <Grid item xs={12}>
        <Typography variant="h6" gutterBottom>
          Review Your Information
        </Typography>
        <Box sx={{ mt: 2 }}>
          <Typography><strong>Name:</strong> {formData.first_name} {formData.last_name}</Typography>
          <Typography><strong>Email:</strong> {formData.email}</Typography>
          <Typography><strong>Phone:</strong> {formData.phone}</Typography>
          <Typography><strong>Legal Issue:</strong> {formData.legal_issue_type}</Typography>
          <Typography><strong>Urgency:</strong> {formData.urgency_level}</Typography>
          <Typography><strong>Description:</strong> {formData.case_description}</Typography>
        </Box>
      </Grid>
      <Grid item xs={12}>
        <TextField
          fullWidth
          label="Additional Notes (Optional)"
          multiline
          rows={3}
          value={formData.notes}
          onChange={handleInputChange('notes')}
          placeholder="Any additional information you'd like to share..."
        />
      </Grid>
    </Grid>
  );

  const getStepContent = (step) => {
    switch (step) {
      case 0:
        return renderPersonalInfo();
      case 1:
        return renderLegalInfo();
      case 2:
        return renderFinancialInfo();
      case 3:
        return renderReview();
      default:
        return 'Unknown step';
    }
  };

  if (success) {
    return (
      <Paper sx={{ p: 4, textAlign: 'center' }}>
        <Typography variant="h5" color="success.main" gutterBottom>
          Intake Submitted Successfully!
        </Typography>
        <Typography variant="body1" sx={{ mb: 3 }}>
          Thank you for submitting your intake form. We will review your information and contact you within 2-3 business days.
        </Typography>
        <Button variant="contained" onClick={onCancel}>
          Close
        </Button>
      </Paper>
    );
  }

  return (
    <Paper sx={{ p: 4 }}>
      <Typography variant="h4" gutterBottom>
        Client Intake Form
      </Typography>
      <Typography variant="body1" color="text.secondary" sx={{ mb: 4 }}>
        Please fill out this form to begin your legal consultation process.
      </Typography>

      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}

      <Stepper activeStep={activeStep} orientation="vertical">
        {steps.map((label, index) => (
          <Step key={label}>
            <StepLabel>{label}</StepLabel>
            <StepContent>
              {getStepContent(index)}
              <Box sx={{ mb: 2, mt: 2 }}>
                <div>
                  <Button
                    variant="contained"
                    onClick={index === steps.length - 1 ? handleSubmit : handleNext}
                    sx={{ mt: 1, mr: 1 }}
                    disabled={loading}
                  >
                    {loading ? (
                      <CircularProgress size={24} />
                    ) : index === steps.length - 1 ? (
                      'Submit'
                    ) : (
                      'Continue'
                    )}
                  </Button>
                  <Button
                    disabled={index === 0}
                    onClick={handleBack}
                    sx={{ mt: 1, mr: 1 }}
                  >
                    Back
                  </Button>
                  {onCancel && (
                    <Button
                      onClick={onCancel}
                      sx={{ mt: 1 }}
                    >
                      Cancel
                    </Button>
                  )}
                </div>
              </Box>
            </StepContent>
          </Step>
        ))}
      </Stepper>
    </Paper>
  );
}

export default ClientIntakeForm;
