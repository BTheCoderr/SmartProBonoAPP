import React, { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import {
  Box,
  Stepper,
  Step,
  StepLabel,
  Button,
  Typography,
  Paper,
  TextField,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Alert,
  CircularProgress,
  Grid,
  Chip,
  FormControlLabel,
  RadioGroup,
  Radio,
  Checkbox,
  FormGroup,
  FormLabel,
  Card,
  CardContent,
  Divider,
} from '@mui/material';
import { expungementApi, documentsApi } from '../services/api';
import useApi from '../hooks/useApi';
import { useNavigate } from 'react-router-dom';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import CancelIcon from '@mui/icons-material/Cancel';
import HelpIcon from '@mui/icons-material/Help';
import DocumentGenerator from './DocumentGenerator';

const steps = ['eligibility', 'stateRules', 'caseDetails', 'documents', 'review'];

// State-specific eligibility criteria (simplified example)
const stateEligibilityCriteria = {
  california: {
    name: "California",
    misdemeanorWaitingPeriod: 1, // years
    felonyWaitingPeriod: 3, // years
    excludedOffenses: ["murder", "rape", "sex crimes involving children"],
    probationRequired: true,
    finesRequired: true
  },
  newyork: {
    name: "New York",
    misdemeanorWaitingPeriod: 3,
    felonyWaitingPeriod: 5,
    excludedOffenses: ["class A felonies", "sex offenses"],
    probationRequired: true,
    finesRequired: true
  },
  texas: {
    name: "Texas",
    misdemeanorWaitingPeriod: 2,
    felonyWaitingPeriod: 5,
    excludedOffenses: ["family violence", "sex offenses", "homicide"],
    probationRequired: true,
    finesRequired: true
  },
  florida: {
    name: "Florida",
    misdemeanorWaitingPeriod: 5,
    felonyWaitingPeriod: 8,
    excludedOffenses: ["violent crimes", "sex offenses", "drug trafficking"],
    probationRequired: true,
    finesRequired: true
  },
  illinois: {
    name: "Illinois",
    misdemeanorWaitingPeriod: 2,
    felonyWaitingPeriod: 3,
    excludedOffenses: ["DUI", "domestic battery", "sex offenses"],
    probationRequired: true,
    finesRequired: true
  }
};

const ExpungementWizard = () => {
  const { t } = useTranslation();
  const navigate = useNavigate();
  const [activeStep, setActiveStep] = useState(0);
  const [formData, setFormData] = useState({
    state: '',
    caseType: '',
    caseDetails: {},
    documents: [],
    convictionType: '',
    convictionDate: '',
    offenseDetails: '',
    completedSentence: false,
    paidFines: false,
    onProbation: false,
    additionalCharges: false,
    additionalDetails: ''
  });
  const [savedProgress, setSavedProgress] = useState(null);
  const [eligibility, setEligibility] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [showDocumentGenerator, setShowDocumentGenerator] = useState(false);

  // API hooks
  const { loading: checkingEligibility, error: eligibilityError, execute: checkEligibility } = useApi(expungementApi.checkEligibility);
  const { loading: fetchingRules, error: rulesError, execute: fetchStateRules } = useApi(expungementApi.getStateRules);
  const { loading: savingProgress, error: saveError, execute: saveProgress } = useApi(expungementApi.saveProgress);
  const { loading: generatingDocs, error: docsError, execute: generateDocument } = useApi(documentsApi.generateDocument);

  useEffect(() => {
    // Load saved progress if available
    const loadSavedProgress = async () => {
      try {
        const progress = localStorage.getItem('expungementProgress');
        if (progress) {
          const parsed = JSON.parse(progress);
          setFormData(parsed.formData);
          setActiveStep(parsed.step);
          setSavedProgress(parsed);
        }
      } catch (error) {
        console.error('Error loading saved progress:', error);
      }
    };

    loadSavedProgress();
  }, []);

  const handleNext = async () => {
    try {
      // Validate current step
      if (!validateStep(activeStep)) {
        return;
      }

      // Save progress
      const progress = { step: activeStep + 1, formData };
      await saveProgress(progress);
      localStorage.setItem('expungementProgress', JSON.stringify(progress));

      // Perform step-specific actions
      switch (activeStep) {
        case 0: // Eligibility
          const eligibility = await checkEligibility(formData);
          if (!eligibility.eligible) {
            throw new Error(eligibility.reason);
          }
          break;
        case 1: // State Rules
          const rules = await fetchStateRules(formData.state);
          setFormData(prev => ({ ...prev, stateRules: rules }));
          break;
        case 2: // Case Details
          // Additional validation can be added here
          break;
        case 3: // Documents
          const docs = await generateDocument('expungement', formData);
          setFormData(prev => ({ ...prev, documents: [...prev.documents, docs] }));
          break;
        case 4: // Eligibility Check
          await checkEligibility();
          break;
        default:
          break;
      }

      setActiveStep((prevStep) => prevStep + 1);
    } catch (error) {
      console.error('Error proceeding to next step:', error);
    }
  };

  const handleBack = () => {
    setActiveStep((prevStep) => prevStep - 1);
  };

  const validateStep = (step) => {
    switch (step) {
      case 0:
        return formData.state && formData.caseType;
      case 1:
        return true; // State rules are informational
      case 2:
        return Object.keys(formData.caseDetails).length > 0;
      case 3:
        return formData.documents.length > 0;
      case 4:
        return true; // Eligibility check is handled separately
      default:
        return true;
    }
  };

  const handleInputChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData({
      ...formData,
      [name]: type === 'checkbox' ? checked : value
    });
  };

  const handleReset = () => {
    setFormData({
      state: '',
      caseType: '',
      caseDetails: {},
      documents: [],
      convictionType: '',
      convictionDate: '',
      offenseDetails: '',
      completedSentence: false,
      paidFines: false,
      onProbation: false,
      additionalCharges: false,
      additionalDetails: ''
    });
    setEligibility(null);
    setActiveStep(0);
    localStorage.removeItem('expungementProgress');
  };

  const renderStepContent = (step) => {
    switch (step) {
      case 0:
        return (
          <Box>
            <Typography variant="h6" gutterBottom>
              {t('expungement.eligibility.title')}
            </Typography>
            <Grid container spacing={3}>
              <Grid item xs={12} md={6}>
                <FormControl fullWidth>
                  <InputLabel>{t('expungement.eligibility.state')}</InputLabel>
                  <Select
                    value={formData.state}
                    onChange={(e) => setFormData({ ...formData, state: e.target.value })}
                  >
                    <MenuItem value="CA">California</MenuItem>
                    <MenuItem value="NY">New York</MenuItem>
                    <MenuItem value="TX">Texas</MenuItem>
                    {/* Add more states */}
                  </Select>
                </FormControl>
              </Grid>
              <Grid item xs={12} md={6}>
                <FormControl fullWidth>
                  <InputLabel>{t('expungement.eligibility.caseType')}</InputLabel>
                  <Select
                    value={formData.caseType}
                    onChange={(e) => setFormData({ ...formData, caseType: e.target.value })}
                  >
                    <MenuItem value="misdemeanor">Misdemeanor</MenuItem>
                    <MenuItem value="felony">Felony</MenuItem>
                    <MenuItem value="arrest">Arrest Record</MenuItem>
                  </Select>
                </FormControl>
              </Grid>
            </Grid>
          </Box>
        );

      case 1:
        return (
          <Box>
            <Typography variant="h6" gutterBottom>
              {t('expungement.stateRules.title')}
            </Typography>
            {formData.stateRules && (
              <Paper sx={{ p: 2 }}>
                <Typography variant="body1">
                  {formData.stateRules.description}
                </Typography>
                <Box sx={{ mt: 2 }}>
                  {formData.stateRules.requirements?.map((req, index) => (
                    <Chip
                      key={index}
                      label={req}
                      sx={{ m: 0.5 }}
                      color="primary"
                      variant="outlined"
                    />
                  ))}
                </Box>
              </Paper>
            )}
          </Box>
        );

      case 2:
        return (
          <Box>
            <Typography variant="h6" gutterBottom>
              {t('expungement.caseDetails.title')}
            </Typography>
            <Grid container spacing={3}>
              <Grid item xs={12}>
                <TextField
                  fullWidth
                  label={t('expungement.caseDetails.caseNumber')}
                  value={formData.caseDetails.caseNumber || ''}
                  onChange={(e) => setFormData({
                    ...formData,
                    caseDetails: { ...formData.caseDetails, caseNumber: e.target.value }
                  })}
                />
              </Grid>
              <Grid item xs={12}>
                <TextField
                  fullWidth
                  label={t('expungement.caseDetails.courtName')}
                  value={formData.caseDetails.courtName || ''}
                  onChange={(e) => setFormData({
                    ...formData,
                    caseDetails: { ...formData.caseDetails, courtName: e.target.value }
                  })}
                />
              </Grid>
              {/* Add more case detail fields */}
            </Grid>
          </Box>
        );

      case 3:
        return (
          <Box>
            <Typography variant="h6" gutterBottom>
              {t('expungement.documents.title')}
            </Typography>
            <Grid container spacing={2}>
              {formData.documents.map((doc, index) => (
                <Grid item xs={12} key={index}>
                  <Paper sx={{ p: 2, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <Typography>{doc.name}</Typography>
                    <Button variant="outlined" onClick={() => window.open(doc.url)}>
                      {t('common.view')}
                    </Button>
                  </Paper>
                </Grid>
              ))}
            </Grid>
          </Box>
        );

      case 4:
        return (
          <Box>
            <Typography variant="h6" gutterBottom>
              {t('expungement.review.title')}
            </Typography>
            <Alert severity="success" sx={{ mb: 2 }}>
              {t('expungement.review.success')}
            </Alert>
            <Paper sx={{ p: 2 }}>
              {/* Add summary of all information */}
            </Paper>
          </Box>
        );

      default:
        return null;
    }
  };

  const renderEligibilityCheck = () => {
    return (
      <Grid container spacing={3}>
        <Grid item xs={12}>
          <Typography variant="h6" gutterBottom>
            Eligibility Check
          </Typography>
          <Typography variant="body2" color="text.secondary" paragraph>
            Based on the information provided, we will check your potential eligibility for expungement.
          </Typography>
          <Alert severity="warning" sx={{ mb: 2 }}>
            This is not legal advice. Laws vary by state and individual circumstances may affect eligibility.
          </Alert>
        </Grid>
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="subtitle1" gutterBottom>
                Eligibility Summary
              </Typography>
              <Box sx={{ mb: 2 }}>
                <Typography component="span" variant="subtitle2" sx={{ mr: 1 }}>
                  State:
                </Typography>
                <Typography component="span" variant="body1">
                  {formData.state ? stateEligibilityCriteria[formData.state.toLowerCase()]?.name || formData.state : 'Not specified'}
                </Typography>
              </Box>
              <Box sx={{ mb: 2 }}>
                <Typography component="span" variant="subtitle2" sx={{ mr: 1 }}>
                  Conviction Type:
                </Typography>
                <Typography component="span" variant="body1">
                  {formData.convictionType || 'Not specified'}
                </Typography>
              </Box>
              <Box sx={{ mb: 2 }}>
                <Typography component="span" variant="subtitle2" sx={{ mr: 1 }}>
                  Date of Conviction:
                </Typography>
                <Typography component="span" variant="body1">
                  {formData.convictionDate ? new Date(formData.convictionDate).toLocaleDateString() : 'Not specified'}
                </Typography>
              </Box>
              
              <Divider sx={{ my: 2 }} />
              
              <Typography variant="subtitle1" gutterBottom>
                Key Eligibility Factors
              </Typography>
              <Grid container spacing={2}>
                <Grid item xs={12} sm={6}>
                  <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                    {formData.completedSentence ? (
                      <CheckCircleIcon color="success" sx={{ mr: 1 }} />
                    ) : (
                      <CancelIcon color="error" sx={{ mr: 1 }} />
                    )}
                    <Typography>Completed Sentence</Typography>
                  </Box>
                  <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                    {formData.paidFines ? (
                      <CheckCircleIcon color="success" sx={{ mr: 1 }} />
                    ) : (
                      <CancelIcon color="error" sx={{ mr: 1 }} />
                    )}
                    <Typography>Paid All Fines</Typography>
                  </Box>
                </Grid>
                <Grid item xs={12} sm={6}>
                  <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                    {!formData.onProbation ? (
                      <CheckCircleIcon color="success" sx={{ mr: 1 }} />
                    ) : (
                      <CancelIcon color="error" sx={{ mr: 1 }} />
                    )}
                    <Typography>Not on Probation/Parole</Typography>
                  </Box>
                  <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                    {!formData.additionalCharges ? (
                      <CheckCircleIcon color="success" sx={{ mr: 1 }} />
                    ) : (
                      <CancelIcon color="error" sx={{ mr: 1 }} />
                    )}
                    <Typography>No Pending Charges</Typography>
                  </Box>
                </Grid>
              </Grid>
            </CardContent>
          </Card>
        </Grid>
        {loading && (
          <Grid item xs={12} sx={{ textAlign: 'center', py: 3 }}>
            <CircularProgress />
            <Typography variant="body2" sx={{ mt: 2 }}>
              Checking eligibility...
            </Typography>
          </Grid>
        )}
        {error && (
          <Grid item xs={12}>
            <Alert severity="error">{error}</Alert>
          </Grid>
        )}
      </Grid>
    );
  };

  const renderEligibilityResults = () => {
    return (
      <Grid container spacing={3}>
        <Grid item xs={12}>
          <Typography variant="h6" gutterBottom>
            Eligibility Results
          </Typography>
          <Typography variant="body2" color="text.secondary" paragraph>
            Based on the information you provided, here's your potential eligibility for expungement.
          </Typography>
        </Grid>
        <Grid item xs={12}>
          {eligibility && (
            <Card>
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                  {eligibility.isEligible ? (
                    <CheckCircleIcon color="success" sx={{ fontSize: 40, mr: 2 }} />
                  ) : (
                    <CancelIcon color="error" sx={{ fontSize: 40, mr: 2 }} />
                  )}
                  <Typography variant="h6">
                    {eligibility.isEligible 
                      ? 'You may be eligible for expungement' 
                      : 'You may not be eligible for expungement at this time'}
                  </Typography>
                </Box>
                
                <Alert severity={eligibility.isEligible ? "success" : "warning"} sx={{ mb: 3 }}>
                  {eligibility.isEligible
                    ? 'Based on the information provided, you may qualify for expungement. Continue to the next steps for documentation.'
                    : 'Based on the information provided, you may not qualify for expungement at this time. See the reasons below for more details.'}
                </Alert>
                
                <Typography variant="subtitle1" gutterBottom>
                  Details:
                </Typography>
                <Box sx={{ mb: 2 }}>
                  <Typography variant="body2">
                    <strong>State:</strong> {eligibility.state}
                  </Typography>
                  <Typography variant="body2">
                    <strong>Conviction Type:</strong> {eligibility.convictionType}
                  </Typography>
                  <Typography variant="body2">
                    <strong>Years Since Conviction:</strong> {eligibility.yearsSinceConviction}
                  </Typography>
                  <Typography variant="body2">
                    <strong>Waiting Period Required:</strong> {eligibility.waitingPeriod} years
                  </Typography>
                </Box>
                
                {!eligibility.isEligible && eligibility.reasons.length > 0 && (
                  <>
                    <Typography variant="subtitle1" gutterBottom>
                      Reasons for Ineligibility:
                    </Typography>
                    <Box component="ul" sx={{ pl: 2 }}>
                      {eligibility.reasons.map((reason, index) => (
                        <Box component="li" key={index} sx={{ mb: 1 }}>
                          <Typography variant="body2">{reason}</Typography>
                        </Box>
                      ))}
                    </Box>
                  </>
                )}
                
                <Divider sx={{ my: 3 }} />
                
                <Typography variant="subtitle1" gutterBottom>
                  Next Steps:
                </Typography>
                {eligibility.isEligible ? (
                  <>
                    <Typography variant="body2" paragraph>
                      While you may be eligible for expungement, the process can be complex. We recommend:
                    </Typography>
                    <Box component="ol" sx={{ pl: 2 }}>
                      <Box component="li" sx={{ mb: 1 }}>
                        <Typography variant="body2">
                          Use our document generator to create a petition for expungement
                        </Typography>
                      </Box>
                      <Box component="li" sx={{ mb: 1 }}>
                        <Typography variant="body2">
                          Gather supporting documents (court records, certificates of completion)
                        </Typography>
                      </Box>
                      <Box component="li" sx={{ mb: 1 }}>
                        <Typography variant="body2">
                          Consider consulting with a legal aid organization in your area
                        </Typography>
                      </Box>
                    </Box>
                    <Box sx={{ mt: 3 }}>
                      <Button 
                        variant="contained" 
                        color="primary"
                        onClick={() => setShowDocumentGenerator(true)}
                      >
                        Generate Expungement Petition
                      </Button>
                    </Box>
                  </>
                ) : (
                  <>
                    <Typography variant="body2" paragraph>
                      While you may not be eligible at this time, we recommend:
                    </Typography>
                    <Box component="ol" sx={{ pl: 2 }}>
                      <Box component="li" sx={{ mb: 1 }}>
                        <Typography variant="body2">
                          Consult with a legal aid organization in your area for personalized advice
                        </Typography>
                      </Box>
                      <Box component="li" sx={{ mb: 1 }}>
                        <Typography variant="body2">
                          Continue to fulfill all requirements (paying fines, completing probation)
                        </Typography>
                      </Box>
                      <Box component="li" sx={{ mb: 1 }}>
                        <Typography variant="body2">
                          Check back when more time has passed since your conviction
                        </Typography>
                      </Box>
                    </Box>
                    <Box sx={{ mt: 3 }}>
                      <Button 
                        variant="outlined" 
                        color="primary"
                        onClick={() => navigate('/resources')}
                      >
                        Find Legal Resources
                      </Button>
                    </Box>
                  </>
                )}
              </CardContent>
            </Card>
          )}
        </Grid>
      </Grid>
    );
  };

  return (
    <Box sx={{ maxWidth: 800, mx: 'auto', p: 3 }}>
      <Paper sx={{ p: 3 }}>
        <Stepper activeStep={activeStep} sx={{ mb: 4 }}>
          {steps.map((label) => (
            <Step key={label}>
              <StepLabel>{t(`expungement.steps.${label}`)}</StepLabel>
            </Step>
          ))}
        </Stepper>

        {(eligibilityError || rulesError || saveError || docsError) && (
          <Alert severity="error" sx={{ mb: 2 }}>
            {eligibilityError || rulesError || saveError || docsError}
          </Alert>
        )}

        {renderStepContent(activeStep)}

        {activeStep === 4 && renderEligibilityCheck()}

        {activeStep === 5 && renderEligibilityResults()}

        <Box sx={{ display: 'flex', justifyContent: 'space-between', mt: 4 }}>
          <Button
            disabled={activeStep === 0 || checkingEligibility || fetchingRules || savingProgress || generatingDocs}
            onClick={handleBack}
          >
            {t('common.back')}
          </Button>
          <Button
            variant="contained"
            onClick={handleNext}
            disabled={checkingEligibility || fetchingRules || savingProgress || generatingDocs}
            endIcon={(checkingEligibility || fetchingRules || savingProgress || generatingDocs) && <CircularProgress size={20} />}
          >
            {activeStep === steps.length - 1 ? t('common.finish') : t('common.next')}
          </Button>
        </Box>
      </Paper>

      {showDocumentGenerator && (
        <Box sx={{ mt: 4 }}>
          <Paper elevation={3} sx={{ p: 3 }}>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
              <Typography variant="h5">
                Expungement Petition Generator
              </Typography>
              <Button
                variant="outlined"
                onClick={() => setShowDocumentGenerator(false)}
              >
                Back to Eligibility Results
              </Button>
            </Box>
            
            <DocumentGenerator
              documentType="expungement"
              initialValues={{
                fullName: '',
                dateOfBirth: '',
                address: '',
                phoneNumber: '',
                email: '',
                caseNumber: '',
                courtName: '',
                convictionDate: formData.convictionDate,
                offenseDescription: formData.offenseDetails,
                state: stateEligibilityCriteria[formData.state?.toLowerCase()]?.name || formData.state,
                completedSentence: formData.completedSentence ? 'Yes' : 'No',
                timeSinceConviction: eligibility?.yearsSinceConviction.toString() || '',
                otherConvictions: formData.additionalCharges ? 'Yes' : 'No'
              }}
              onSubmit={(data) => {
                console.log('Submitting expungement petition:', data);
                // This would typically send the data to a backend API
                navigate('/documents');
              }}
            />
          </Paper>
        </Box>
      )}
    </Box>
  );
};

export default ExpungementWizard; 