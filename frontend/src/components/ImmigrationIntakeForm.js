import React, { useState, useEffect } from 'react';
import {
  Box,
  Paper,
  Typography,
  TextField,
  Button,
  Stepper,
  Step,
  StepLabel,
  Grid,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Checkbox,
  FormControlLabel,
  Divider,
  Alert,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Chip,
  FormHelperText,
  Snackbar,
  CircularProgress
} from '@mui/material';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import DescriptionIcon from '@mui/icons-material/Description';
import FileUploadIcon from '@mui/icons-material/FileUpload';
import PersonIcon from '@mui/icons-material/Person';
import FlagIcon from '@mui/icons-material/Flag';
import EventIcon from '@mui/icons-material/Event';
import { immigrationApi } from '../services/api';
import { useAuth } from '../context/AuthContext';
import { useMediaQuery } from '@mui/material';
import { useTheme } from '@mui/material/styles';
import { useNavigate } from 'react-router-dom';
import { Formik, Form } from 'formik';
import * as Yup from 'yup';
import axios from 'axios';
import { API_BASE_URL } from '../config';

const visaTypes = [
  { value: 'family', label: 'Family-Based Immigration' },
  { value: 'employment', label: 'Employment-Based Immigration' },
  { value: 'student', label: 'Student Visa' },
  { value: 'visitor', label: 'Visitor Visa' },
  { value: 'refugee', label: 'Refugee/Asylum' },
  { value: 'citizenship', label: 'Citizenship/Naturalization' },
  { value: 'other', label: 'Other Immigration Matter' },
];

// Add nationality options
const nationalities = [
  { value: 'Afghanistan', label: 'Afghanistan' },
  { value: 'Albania', label: 'Albania' },
  { value: 'Algeria', label: 'Algeria' },
  { value: 'Argentina', label: 'Argentina' },
  { value: 'Australia', label: 'Australia' },
  { value: 'Bangladesh', label: 'Bangladesh' },
  { value: 'Brazil', label: 'Brazil' },
  { value: 'Canada', label: 'Canada' },
  { value: 'China', label: 'China' },
  { value: 'Colombia', label: 'Colombia' },
  { value: 'Egypt', label: 'Egypt' },
  { value: 'El Salvador', label: 'El Salvador' },
  { value: 'Ethiopia', label: 'Ethiopia' },
  { value: 'France', label: 'France' },
  { value: 'Germany', label: 'Germany' },
  { value: 'Guatemala', label: 'Guatemala' },
  { value: 'Haiti', label: 'Haiti' },
  { value: 'Honduras', label: 'Honduras' },
  { value: 'India', label: 'India' },
  { value: 'Indonesia', label: 'Indonesia' },
  { value: 'Iran', label: 'Iran' },
  { value: 'Iraq', label: 'Iraq' },
  { value: 'Ireland', label: 'Ireland' },
  { value: 'Italy', label: 'Italy' },
  { value: 'Jamaica', label: 'Jamaica' },
  { value: 'Japan', label: 'Japan' },
  { value: 'Kenya', label: 'Kenya' },
  { value: 'Mexico', label: 'Mexico' },
  { value: 'Nigeria', label: 'Nigeria' },
  { value: 'Pakistan', label: 'Pakistan' },
  { value: 'Philippines', label: 'Philippines' },
  { value: 'Poland', label: 'Poland' },
  { value: 'Russia', label: 'Russia' },
  { value: 'South Korea', label: 'South Korea' },
  { value: 'Syria', label: 'Syria' },
  { value: 'Ukraine', label: 'Ukraine' },
  { value: 'United Kingdom', label: 'United Kingdom' },
  { value: 'Venezuela', label: 'Venezuela' },
  { value: 'Vietnam', label: 'Vietnam' },
  { value: 'Yemen', label: 'Yemen' },
];

// Add immigration status options
const immigrationStatuses = [
  { value: 'us_citizen', label: 'U.S. Citizen' },
  { value: 'permanent_resident', label: 'Permanent Resident (Green Card)' },
  { value: 'conditional_resident', label: 'Conditional Resident' },
  { value: 'temporary_visa', label: 'Temporary Visa Holder' },
  { value: 'refugee', label: 'Refugee' },
  { value: 'asylee', label: 'Asylee' },
  { value: 'daca', label: 'DACA Recipient' },
  { value: 'tps', label: 'Temporary Protected Status (TPS)' },
  { value: 'undocumented', label: 'Undocumented' },
  { value: 'visa_overstay', label: 'Visa Overstay' },
  { value: 'student_visa', label: 'Student Visa (F-1/M-1)' },
  { value: 'work_visa', label: 'Work Visa (H-1B, L-1, etc.)' },
  { value: 'visitor_visa', label: 'Visitor Visa (B-1/B-2)' },
  { value: 'pending_asylum', label: 'Pending Asylum Application' },
  { value: 'pending_adjustment', label: 'Pending Adjustment of Status' },
  { value: 'other', label: 'Other' },
];

// Add desired service options
const desiredServices = [
  { value: 'family_petition', label: 'Family-Based Petition' },
  { value: 'employment_petition', label: 'Employment-Based Petition' },
  { value: 'green_card', label: 'Green Card Application' },
  { value: 'citizenship', label: 'Citizenship/Naturalization' },
  { value: 'asylum', label: 'Asylum Application' },
  { value: 'deportation_defense', label: 'Deportation Defense' },
  { value: 'visa_application', label: 'Visa Application' },
  { value: 'visa_renewal', label: 'Visa Renewal' },
  { value: 'work_permit', label: 'Work Permit (EAD)' },
  { value: 'travel_document', label: 'Travel Document' },
  { value: 'daca_renewal', label: 'DACA Renewal' },
  { value: 'tps_application', label: 'TPS Application' },
  { value: 'waiver', label: 'Waiver Application' },
  { value: 'consular_processing', label: 'Consular Processing' },
  { value: 'adjustment_of_status', label: 'Adjustment of Status' },
  { value: 'other', label: 'Other Immigration Services' },
];

// Add income level options
const incomeLevels = [
  { value: 'below_15k', label: 'Below $15,000' },
  { value: '15k_30k', label: '$15,000 - $30,000' },
  { value: '30k_50k', label: '$30,000 - $50,000' },
  { value: '50k_75k', label: '$50,000 - $75,000' },
  { value: '75k_100k', label: '$75,000 - $100,000' },
  { value: 'above_100k', label: 'Above $100,000' },
  { value: 'prefer_not_to_say', label: 'Prefer not to say' },
];

// Add referral source options
const referralSources = [
  { value: 'search_engine', label: 'Search Engine (Google, Bing, etc.)' },
  { value: 'social_media', label: 'Social Media' },
  { value: 'friend_family', label: 'Friend or Family Member' },
  { value: 'legal_clinic', label: 'Legal Clinic or Workshop' },
  { value: 'community_org', label: 'Community Organization' },
  { value: 'lawyer_referral', label: 'Lawyer Referral' },
  { value: 'advertisement', label: 'Advertisement' },
  { value: 'other', label: 'Other' },
];

// Required documents by visa type
const requiredDocuments = {
  family: [
    'Birth certificates',
    'Marriage certificates',
    'Passport (valid for at least 6 months)',
    'Proof of financial support',
    'Sponsor\'s proof of citizenship/residency',
    'Affidavit of Support (Form I-864)',
    'Passport photos',
  ],
  employment: [
    'Job offer letter',
    'Resume/CV',
    'Educational credentials',
    'Work experience letters',
    'Passport (valid for at least 6 months)',
    'Labor certification',
    'Passport photos',
  ],
  student: [
    'Acceptance letter from U.S. institution',
    'Proof of financial support',
    'Academic transcripts',
    'Standardized test scores',
    'Passport (valid for at least 6 months)',
    'SEVIS fee receipt',
    'Passport photos',
  ],
  visitor: [
    'Passport (valid for at least 6 months)',
    'Travel itinerary',
    'Proof of ties to home country',
    'Proof of financial means',
    'Invitation letter (if applicable)',
    'Passport photos',
  ],
  refugee: [
    'Evidence of persecution',
    'Identity documents',
    'Passport or travel documents',
    'Photos documenting persecution (if available)',
    'Medical records (if applicable)',
    'Passport photos',
  ],
  citizenship: [
    'Green card',
    'Passport',
    'Tax returns (last 5 years)',
    'Travel history documentation',
    'Proof of continuous residence',
    'Passport photos',
  ],
  other: [
    'Passport',
    'Any relevant immigration documents',
    'Personal identification',
    'Passport photos',
  ],
};

const steps = ['Personal Information', 'Case Details', 'Document Checklist', 'Review & Submit'];

// Add validation schemas for each step
const personalInfoSchema = Yup.object().shape({
  firstName: Yup.string()
    .required('First name is required')
    .min(2, 'First name must be at least 2 characters')
    .matches(/^[a-zA-Z\s-']+$/, 'First name can only contain letters, spaces, hyphens, and apostrophes'),
  lastName: Yup.string()
    .required('Last name is required')
    .min(2, 'Last name must be at least 2 characters')
    .matches(/^[a-zA-Z\s-']+$/, 'Last name can only contain letters, spaces, hyphens, and apostrophes'),
  email: Yup.string()
    .email('Invalid email address')
    .required('Email is required'),
  phone: Yup.string()
    .matches(/^[0-9-+()]*$/, 'Invalid phone number format')
    .min(10, 'Phone number must be at least 10 digits')
    .required('Phone number is required'),
  dateOfBirth: Yup.date()
    .max(new Date(), 'Date of birth cannot be in the future')
    .min(new Date(1900, 0, 1), 'Invalid date of birth')
    .required('Date of birth is required'),
  nationality: Yup.string()
    .required('Nationality is required'),
  currentResidence: Yup.string()
    .required('Current residence is required'),
});

const caseDetailsSchema = Yup.object().shape({
  visaType: Yup.string()
    .required('Please select an immigration matter type'),
  currentImmigrationStatus: Yup.string()
    .required('Current immigration status is required'),
  desiredService: Yup.string()
    .required('Desired service is required'),
  urgency: Yup.string()
    .oneOf(['high', 'medium', 'low'], 'Please select urgency level')
    .required('Please indicate the urgency of your case'),
  priorApplications: Yup.boolean(),
  priorApplicationDetails: Yup.string()
    .when('priorApplications', {
      is: true,
      then: Yup.string()
        .required('Please provide details about prior applications')
        .min(20, 'Please provide more details about prior applications'),
    }),
  specialCircumstances: Yup.string()
    .max(1000, 'Special circumstances description is too long'),
});

const legalAssistanceSchema = Yup.object().shape({
  caseDescription: Yup.string()
    .required('Case description is required')
    .min(50, 'Please provide more detail about your case')
    .max(2000, 'Case description is too long'),
  hasLegalRepresentation: Yup.string()
    .oneOf(['yes', 'no'], 'Please indicate if you have legal representation')
    .required('Please indicate if you have legal representation'),
  incomeLevel: Yup.string()
    .required('Income level is required for determining eligibility'),
  howDidYouHear: Yup.string()
    .required('Please let us know how you heard about us'),
  preferredLanguage: Yup.string()
    .required('Preferred language is required'),
  agreeToTerms: Yup.boolean()
    .oneOf([true], 'You must agree to the terms and conditions'),
});

const ImmigrationIntakeForm = ({ onCancel, initialServiceType = '' }) => {
  const { accessToken } = useAuth();
  const [activeStep, setActiveStep] = useState(0);
  
  // Add theme and media query for responsive design
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('sm'));
  
  const [formData, setFormData] = useState({
    firstName: '',
    lastName: '',
    email: '',
    phone: '',
    dateOfBirth: null,
    countryOfBirth: '',
    currentResidence: '',
    visaType: initialServiceType,
    urgency: 'normal',
    priorApplications: false,
    priorApplicationDetails: '',
    specialCircumstances: '',
    preferredLanguage: 'English',
    documents: initialServiceType ? requiredDocuments[initialServiceType] || [] : [],
    nationality: '',
    currentImmigrationStatus: '',
    desiredService: '',
    caseDescription: '',
    hasLegalRepresentation: 'no',
    incomeLevel: '',
    howDidYouHear: ''
  });
  const [submitted, setSubmitted] = useState(false);
  const [errors, setErrors] = useState({});
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [notification, setNotification] = useState({
    open: false,
    message: '',
    severity: 'success'
  });
  const navigate = useNavigate();

  useEffect(() => {
    if (initialServiceType) {
      setFormData(prevData => ({
        ...prevData,
        visaType: initialServiceType,
        documents: requiredDocuments[initialServiceType] || []
      }));
    }
  }, [initialServiceType]);

  const handleInputChange = (field) => (event) => {
    const value = event.target.type === 'checkbox' ? event.target.checked : event.target.value;
    setFormData({ ...formData, [field]: value });
    
    // Clear error for this field if it exists
    if (errors[field]) {
      setErrors({
        ...errors,
        [field]: ''
      });
    }
  };

  const handleDateChange = (event) => {
    setFormData({
      ...formData,
      dateOfBirth: event.target.value
    });
    
    // Clear error for this field if it exists
    if (errors.dateOfBirth) {
      setErrors({
        ...errors,
        dateOfBirth: ''
      });
    }
  };

  const handleNext = async (values) => {
    setFormData({ ...formData, ...values });
    setActiveStep((prevStep) => prevStep + 1);
  };

  const handleBack = () => {
    setActiveStep((prevStep) => prevStep - 1);
  };

  const handleSubmit = async (values) => {
    setIsSubmitting(true);
    setError('');

    try {
      // Validate all required documents are present
      const requiredDocs = requiredDocuments[values.visaType] || [];
      const missingDocs = requiredDocs.filter(doc => !values.documents.includes(doc));
      
      if (missingDocs.length > 0) {
        setError(`Missing required documents: ${missingDocs.join(', ')}`);
        return;
      }

      const response = await axios.post(`${API_BASE_URL}/api/intake/immigration`, {
        ...values,
        submissionDate: new Date().toISOString(),
        status: 'pending_review',
        documents: values.documents,
        metadata: {
          browser: navigator.userAgent,
          submissionPlatform: 'web',
          formVersion: '1.0',
        }
      });

      if (response.status === 201) {
        // Navigate to thank you page with form data
        navigate('/thank-you', {
          state: {
            formData: values,
            intakeId: response.data.id
          }
        });
      }
    } catch (err) {
      const errorMessage = err.response?.data?.message || 'An error occurred while submitting the form';
      setError(errorMessage);
      setNotification({
        open: true,
        message: errorMessage,
        severity: 'error'
      });
    } finally {
      setIsSubmitting(false);
    }
  };

  const validateForm = () => {
    const newErrors = {};
    
    // Validate required personal information
    if (!formData.firstName.trim()) newErrors.firstName = 'First name is required';
    if (!formData.lastName.trim()) newErrors.lastName = 'Last name is required';
    if (!formData.email.trim()) newErrors.email = 'Email is required';
    else if (!/\S+@\S+\.\S+/.test(formData.email)) newErrors.email = 'Email is invalid';
    if (!formData.phone.trim()) newErrors.phone = 'Phone number is required';
    if (!formData.dateOfBirth) newErrors.dateOfBirth = 'Date of birth is required';
    
    // Validate immigration information
    if (!formData.nationality) newErrors.nationality = 'Nationality is required';
    if (!formData.currentImmigrationStatus) newErrors.currentImmigrationStatus = 'Current immigration status is required';
    if (!formData.desiredService) newErrors.desiredService = 'Desired service is required';
    if (!formData.caseDescription.trim()) newErrors.caseDescription = 'Case description is required';
    
    // Validate visa type if on that step
    if (activeStep >= 1 && !formData.visaType) newErrors.visaType = 'Please select an immigration matter type';
    
    // If prior applications is checked, require details
    if (formData.priorApplications && !formData.priorApplicationDetails.trim()) {
      newErrors.priorApplicationDetails = 'Please provide details about prior applications';
    }
    
    setErrors(newErrors);
    
    // Form is valid if there are no errors
    return Object.keys(newErrors).length === 0;
  };

  const renderStepContent = () => {
    switch (activeStep) {
      case 0:
        return (
          <Formik
            initialValues={{
              firstName: formData.firstName || '',
              lastName: formData.lastName || '',
              email: formData.email || '',
              phone: formData.phone || ''
            }}
            validationSchema={personalInfoSchema}
            onSubmit={handleNext}
          >
            {({ errors, touched, handleChange, handleBlur, values }) => (
              <Form>
                <Box sx={{ mb: 3 }}>
                  <TextField
                    fullWidth
                    name="firstName"
                    label="First Name"
                    value={values.firstName}
                    onChange={handleChange}
                    onBlur={handleBlur}
                    error={touched.firstName && Boolean(errors.firstName)}
                    helperText={touched.firstName && errors.firstName}
                    sx={{ mb: 2 }}
                  />
                  <TextField
                    fullWidth
                    name="lastName"
                    label="Last Name"
                    value={values.lastName}
                    onChange={handleChange}
                    onBlur={handleBlur}
                    error={touched.lastName && Boolean(errors.lastName)}
                    helperText={touched.lastName && errors.lastName}
                    sx={{ mb: 2 }}
                  />
                  <TextField
                    fullWidth
                    name="email"
                    label="Email"
                    type="email"
                    value={values.email}
                    onChange={handleChange}
                    onBlur={handleBlur}
                    error={touched.email && Boolean(errors.email)}
                    helperText={touched.email && errors.email}
                    sx={{ mb: 2 }}
                  />
                  <TextField
                    fullWidth
                    name="phone"
                    label="Phone Number"
                    value={values.phone}
                    onChange={handleChange}
                    onBlur={handleBlur}
                    error={touched.phone && Boolean(errors.phone)}
                    helperText={touched.phone && errors.phone}
                  />
                </Box>
                <Box sx={{ display: 'flex', justifyContent: 'flex-end' }}>
                  <Button
                    type="submit"
                    variant="contained"
                    sx={{ mt: 3, ml: 1 }}
                  >
                    Next
                  </Button>
                </Box>
              </Form>
            )}
          </Formik>
        );
      case 1:
        return (
          <Formik
            initialValues={{
              immigrationStatus: formData.currentImmigrationStatus || '',
              countryOfOrigin: formData.nationality || '',
              dateOfEntry: formData.dateOfBirth ? new Date(formData.dateOfBirth).toISOString().split('T')[0] : '',
              visaType: formData.visaType || ''
            }}
            validationSchema={caseDetailsSchema}
            onSubmit={handleNext}
          >
            {({ errors, touched, handleChange, handleBlur, values }) => (
              <Form>
                <Box sx={{ mb: 3 }}>
                  <TextField
                    fullWidth
                    name="immigrationStatus"
                    label="Current Immigration Status"
                    value={values.immigrationStatus}
                    onChange={handleChange}
                    onBlur={handleBlur}
                    error={touched.immigrationStatus && Boolean(errors.immigrationStatus)}
                    helperText={touched.immigrationStatus && errors.immigrationStatus}
                    sx={{ mb: 2 }}
                  />
                  <TextField
                    fullWidth
                    name="countryOfOrigin"
                    label="Country of Origin"
                    value={values.countryOfOrigin}
                    onChange={handleChange}
                    onBlur={handleBlur}
                    error={touched.countryOfOrigin && Boolean(errors.countryOfOrigin)}
                    helperText={touched.countryOfOrigin && errors.countryOfOrigin}
                    sx={{ mb: 2 }}
                  />
                  <TextField
                    fullWidth
                    name="dateOfEntry"
                    label="Date of Entry"
                    type="date"
                    InputLabelProps={{ shrink: true }}
                    value={values.dateOfEntry}
                    onChange={handleChange}
                    onBlur={handleBlur}
                    error={touched.dateOfEntry && Boolean(errors.dateOfEntry)}
                    helperText={touched.dateOfEntry && errors.dateOfEntry}
                    sx={{ mb: 2 }}
                  />
                  <TextField
                    fullWidth
                    name="visaType"
                    label="Visa Type"
                    value={values.visaType}
                    onChange={handleChange}
                    onBlur={handleBlur}
                    error={touched.visaType && Boolean(errors.visaType)}
                    helperText={touched.visaType && errors.visaType}
                  />
                </Box>
                <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                  <Button onClick={handleBack}>Back</Button>
                  <Button
                    type="submit"
                    variant="contained"
                    sx={{ mt: 3, ml: 1 }}
                  >
                    Next
                  </Button>
                </Box>
              </Form>
            )}
          </Formik>
        );
      case 2:
        return (
          <Formik
            initialValues={{
              legalIssue: formData.caseDescription || '',
              hasAttorney: formData.hasLegalRepresentation === 'yes',
              urgency: formData.urgency || ''
            }}
            validationSchema={legalAssistanceSchema}
            onSubmit={handleSubmit}
          >
            {({ errors, touched, handleChange, handleBlur, values }) => (
              <Form>
                <Box sx={{ mb: 3 }}>
                  <TextField
                    fullWidth
                    multiline
                    rows={4}
                    name="legalIssue"
                    label="Describe Your Legal Issue"
                    value={values.legalIssue}
                    onChange={handleChange}
                    onBlur={handleBlur}
                    error={touched.legalIssue && Boolean(errors.legalIssue)}
                    helperText={touched.legalIssue && errors.legalIssue}
                    sx={{ mb: 2 }}
                  />
                  <FormControl component="fieldset">
                    <FormControlLabel
                      control={
                        <Checkbox
                          checked={values.hasAttorney}
                          onChange={(e) => handleChange({ target: { name: 'hasAttorney', value: e.target.checked } })}
                        />
                      }
                      label="Do you currently have an attorney?"
                    />
                  </FormControl>
                  <FormControl component="fieldset">
                    <FormLabel component="legend">How urgent is your case?</FormLabel>
                    <RadioGroup
                      name="urgency"
                      value={values.urgency}
                      onChange={handleChange}
                    >
                      <FormControlLabel value="high" control={<Radio />} label="Urgent (Need assistance within 24-48 hours)" />
                      <FormControlLabel value="medium" control={<Radio />} label="Moderate (Need assistance within 1 week)" />
                      <FormControlLabel value="low" control={<Radio />} label="Low (Can wait more than 1 week)" />
                    </RadioGroup>
                  </FormControl>
                </Box>
                {error && (
                  <Alert severity="error" sx={{ mb: 2 }}>
                    {error}
                  </Alert>
                )}
                <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                  <Button onClick={handleBack}>Back</Button>
                  <Button
                    type="submit"
                    variant="contained"
                    disabled={isSubmitting}
                    sx={{ mt: 3, ml: 1 }}
                  >
                    {isSubmitting ? <CircularProgress size={24} /> : 'Submit'}
                  </Button>
                </Box>
              </Form>
            )}
          </Formik>
        );
      case 3:
        return (
          <Box>
            <Typography variant="h6" gutterBottom>
              Review Your Information
            </Typography>
            <Grid container spacing={2}>
              <Grid item xs={12} md={6}>
                <Paper variant="outlined" sx={{ p: 2, mb: 2 }}>
                  <Typography variant="subtitle1" sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                    <PersonIcon sx={{ mr: 1 }} /> Personal Information
                  </Typography>
                  <Typography>
                    <strong>Name:</strong> {formData.firstName} {formData.lastName}
                  </Typography>
                  <Typography>
                    <strong>Email:</strong> {formData.email}
                  </Typography>
                  <Typography>
                    <strong>Phone:</strong> {formData.phone}
                  </Typography>
                  <Typography>
                    <strong>Date of Birth:</strong> {formData.dateOfBirth ? new Date(formData.dateOfBirth).toLocaleDateString() : 'Not provided'}
                  </Typography>
                  <Typography>
                    <strong>Country of Birth:</strong> {formData.countryOfBirth || 'Not provided'}
                  </Typography>
                  <Typography>
                    <strong>Current Residence:</strong> {formData.currentResidence || 'Not provided'}
                  </Typography>
                </Paper>
              </Grid>
              <Grid item xs={12} md={6}>
                <Paper variant="outlined" sx={{ p: 2, mb: 2 }}>
                  <Typography variant="subtitle1" sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                    <FlagIcon sx={{ mr: 1 }} /> Case Information
                  </Typography>
                  <Typography>
                    <strong>Immigration Matter:</strong> {visaTypes.find(t => t.value === formData.visaType)?.label}
                  </Typography>
                  <Typography>
                    <strong>Urgency:</strong> {formData.urgency}
                  </Typography>
                  <Typography>
                    <strong>Prior Applications:</strong> {formData.priorApplications ? 'Yes' : 'No'}
                  </Typography>
                  {formData.priorApplications && (
                    <Typography>
                      <strong>Prior Application Details:</strong> {formData.priorApplicationDetails}
                    </Typography>
                  )}
                  <Typography>
                    <strong>Special Circumstances:</strong> {formData.specialCircumstances || 'None'}
                  </Typography>
                  <Typography>
                    <strong>Preferred Language:</strong> {formData.preferredLanguage}
                  </Typography>
                </Paper>
              </Grid>
              <Grid item xs={12}>
                <Paper variant="outlined" sx={{ p: 2 }}>
                  <Typography variant="subtitle1" sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                    <DescriptionIcon sx={{ mr: 1 }} /> Document Checklist
                  </Typography>
                  <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                    {formData.documents.map((doc, index) => (
                      <Chip key={index} label={doc} icon={<CheckCircleIcon />} />
                    ))}
                  </Box>
                </Paper>
              </Grid>
            </Grid>
          </Box>
        );
      default:
        return null;
    }
  };

  const handleCloseNotification = () => {
    setNotification({
      ...notification,
      open: false
    });
  };

  return (
    <Paper 
      elevation={3} 
      sx={{ 
        p: { xs: 2, sm: 4 }, // Reduce padding on mobile
        maxWidth: 800, 
        mx: 'auto', 
        my: 3,
        overflowX: 'hidden' // Prevent horizontal scroll on mobile
      }}
    >
      <Typography 
        variant={isMobile ? "h5" : "h4"} 
        align="center" 
        gutterBottom
      >
        Immigration Services Intake Form
      </Typography>
      
      <Typography 
        variant="body1" 
        paragraph 
        align="center" 
        color="text.secondary" 
        sx={{ mb: 4 }}
      >
        Please complete this form to help us understand your immigration needs. All information is confidential.
      </Typography>
      
      {/* Mobile stepper view */}
      {isMobile && (
        <Stepper 
          activeStep={activeStep} 
          alternativeLabel 
          sx={{ mb: 3 }}
        >
          {steps.map((label) => (
            <Step key={label}>
              <StepLabel>{label}</StepLabel>
            </Step>
          ))}
        </Stepper>
      )}
      
      <form onSubmit={handleSubmit}>
        <Grid container spacing={isMobile ? 2 : 3}>
          <Grid item xs={12}>
            <Typography variant="h6" color="primary" gutterBottom>
              {!isMobile && activeStep === 0 && "Personal Information"}
              {!isMobile && activeStep === 1 && "Case Details"}
              {!isMobile && activeStep === 2 && "Legal Assistance"}
              {!isMobile && activeStep === 3 && "Review & Submit"}
              {isMobile && steps[activeStep]}
            </Typography>
            <Divider sx={{ mb: 2 }} />
          </Grid>
          
          {renderStepContent()}
          
          {/* Mobile navigation buttons */}
          {isMobile && (
            <Grid item xs={12}>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', mt: 2 }}>
                <Button
                  variant="outlined"
                  onClick={activeStep === 0 ? onCancel : handleBack}
                  sx={{ minWidth: '40%' }}
                >
                  {activeStep === 0 ? 'Cancel' : 'Back'}
                </Button>
                {activeStep < steps.length - 1 ? (
                  <Button
                    variant="contained"
                    onClick={handleNext}
                    sx={{ minWidth: '40%' }}
                  >
                    Next
                  </Button>
                ) : (
                  <Button
                    type="submit"
                    variant="contained"
                    color="primary"
                    disabled={isSubmitting}
                    sx={{ minWidth: '40%' }}
                  >
                    {isSubmitting ? 'Submitting...' : 'Submit'}
                  </Button>
                )}
              </Box>
            </Grid>
          )}
          
          {/* Only show these sections on desktop or last step on mobile */}
          {(!isMobile || activeStep === steps.length - 1) && (
            <>
              <Grid item xs={12}>
                <Typography variant="h6" color="primary" gutterBottom sx={{ mt: 2 }}>
                  Immigration Information
                </Typography>
                <Divider sx={{ mb: 2 }} />
              </Grid>
              
              <Grid item xs={12} sm={6}>
                <FormControl fullWidth error={!!errors.nationality}>
                  <InputLabel>Nationality</InputLabel>
                  <Select
                    name="nationality"
                    value={formData.nationality}
                    onChange={handleInputChange('nationality')}
                    label="Nationality"
                    required
                    // Improve touch experience on mobile
                    MenuProps={{
                      PaperProps: {
                        style: {
                          maxHeight: isMobile ? 300 : 450,
                        },
                      },
                    }}
                  >
                    {nationalities.map((nationality) => (
                      <MenuItem key={nationality.value} value={nationality.value}>
                        {nationality.label}
                      </MenuItem>
                    ))}
                  </Select>
                  {errors.nationality && (
                    <FormHelperText error>{errors.nationality}</FormHelperText>
                  )}
                </FormControl>
              </Grid>
              
              <Grid item xs={12} sm={6}>
                <FormControl fullWidth error={!!errors.currentImmigrationStatus}>
                  <InputLabel>Current Immigration Status</InputLabel>
                  <Select
                    name="currentImmigrationStatus"
                    value={formData.currentImmigrationStatus}
                    onChange={handleInputChange('currentImmigrationStatus')}
                    label="Current Immigration Status"
                    required
                  >
                    {immigrationStatuses.map((status) => (
                      <MenuItem key={status.value} value={status.value}>
                        {status.label}
                      </MenuItem>
                    ))}
                  </Select>
                </FormControl>
              </Grid>
              
              <Grid item xs={12} sm={6}>
                <FormControl fullWidth error={!!errors.desiredService}>
                  <InputLabel>Desired Immigration Service</InputLabel>
                  <Select
                    name="desiredService"
                    value={formData.desiredService}
                    onChange={handleInputChange('desiredService')}
                    label="Desired Immigration Service"
                    required
                  >
                    {desiredServices.map((service) => (
                      <MenuItem key={service.value} value={service.value}>
                        {service.label}
                      </MenuItem>
                    ))}
                  </Select>
                </FormControl>
              </Grid>
              
              <Grid item xs={12}>
                <TextField
                  fullWidth
                  label="Brief description of your case"
                  name="caseDescription"
                  value={formData.caseDescription}
                  onChange={handleInputChange('caseDescription')}
                  multiline
                  rows={4}
                  error={!!errors.caseDescription}
                  helperText={errors.caseDescription}
                  required
                />
              </Grid>
              
              <Grid item xs={12} sm={6}>
                <FormControl fullWidth>
                  <InputLabel>Do you currently have legal representation?</InputLabel>
                  <Select
                    name="hasLegalRepresentation"
                    value={formData.hasLegalRepresentation}
                    onChange={handleInputChange('hasLegalRepresentation')}
                    label="Do you currently have legal representation?"
                  >
                    <MenuItem value="yes">Yes</MenuItem>
                    <MenuItem value="no">No</MenuItem>
                  </Select>
                </FormControl>
              </Grid>
              
              <Grid item xs={12} sm={6}>
                <FormControl fullWidth>
                  <InputLabel>Annual Income Level</InputLabel>
                  <Select
                    name="incomeLevel"
                    value={formData.incomeLevel}
                    onChange={handleInputChange('incomeLevel')}
                    label="Annual Income Level"
                  >
                    {incomeLevels.map((level) => (
                      <MenuItem key={level.value} value={level.value}>
                        {level.label}
                      </MenuItem>
                    ))}
                  </Select>
                </FormControl>
              </Grid>
              
              <Grid item xs={12} sm={6}>
                <FormControl fullWidth>
                  <InputLabel>How did you hear about us?</InputLabel>
                  <Select
                    name="howDidYouHear"
                    value={formData.howDidYouHear}
                    onChange={handleInputChange('howDidYouHear')}
                    label="How did you hear about us?"
                  >
                    {referralSources.map((source) => (
                      <MenuItem key={source.value} value={source.value}>
                        {source.label}
                      </MenuItem>
                    ))}
                  </Select>
                </FormControl>
              </Grid>
              
              <Grid item xs={12}>
                <Box 
                  sx={{ 
                    mt: 3, 
                    display: 'flex', 
                    justifyContent: 'space-between',
                    flexDirection: isMobile ? 'column' : 'row',
                    gap: isMobile ? 2 : 0
                  }}
                >
                  <Button
                    variant="outlined"
                    color="secondary"
                    onClick={onCancel}
                    disabled={isSubmitting}
                    sx={{ 
                      width: isMobile ? '100%' : 'auto',
                      py: isMobile ? 1.5 : 1
                    }}
                  >
                    Cancel
                  </Button>
                  <Button
                    type="submit"
                    variant="contained"
                    color="primary"
                    disabled={isSubmitting}
                    sx={{ 
                      width: isMobile ? '100%' : 'auto',
                      py: isMobile ? 1.5 : 1
                    }}
                  >
                    {isSubmitting ? 'Submitting...' : 'Submit'}
                  </Button>
                </Box>
              </Grid>
            </>
          )}
        </Grid>
      </form>
      
      <Snackbar
        open={notification.open}
        autoHideDuration={6000}
        onClose={handleCloseNotification}
        anchorOrigin={{ 
          vertical: 'bottom', 
          horizontal: 'center' 
        }}
      >
        <Alert 
          onClose={handleCloseNotification} 
          severity={notification.severity}
          variant="filled"
          sx={{ 
            width: '100%',
            // Make alert more visible on mobile
            fontSize: isMobile ? '1rem' : 'inherit',
            '& .MuiAlert-icon': {
              fontSize: isMobile ? '1.5rem' : 'inherit'
            }
          }}
        >
          {notification.message}
        </Alert>
      </Snackbar>
    </Paper>
  );
};

export default ImmigrationIntakeForm; 