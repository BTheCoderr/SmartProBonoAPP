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
} from '@mui/material';
import { expungementApi, documentsApi } from '../services/api';
import useApi from '../hooks/useApi';
const steps = ['eligibility', 'stateRules', 'caseDetails', 'documents', 'review'];
const ExpungementWizard = () => {
  const { t } = useTranslation();
  const [activeStep, setActiveStep] = useState(0);
  const [answers, setAnswers] = useState({});
  const [savedProgress, setSavedProgress] = useState(null);
  const [loading, setLoading] = useState(false);
  const [formData, setFormData] = useState({
    state: '',
    county: '',
    convictionType: '',
    convictionDate: '',
    hasMultipleConvictions: false,
    documents: [],
  });
  
  // API hooks
  const [checkingEligibility, setCheckingEligibility] = useState(false);
  const [eligibilityResult, setEligibilityResult] = useState(null);
  
  const [fetchingRules, setFetchingRules] = useState(false);
  const [stateRules, setStateRules] = useState(null);
  
  const [savingProgress, setSavingProgress] = useState(false);
  const [progressSaved, setProgressSaved] = useState(false);
  
  const [generatingDocs, setGeneratingDocs] = useState(false);
  const [generatedDocs, setGeneratedDocs] = useState([]);
  const {
    loading: eligibilityLoading,
    error: eligibilityError,
    execute: checkEligibility,
  } = useApi(expungementApi.checkEligibility);
  const {
    loading: rulesLoading,
    error: rulesError,
    execute: fetchStateRules,
  } = useApi(expungementApi.getStateRules);
  const {
    loading: progressLoading,
    error: saveError,
    execute: saveProgress,
  } = useApi(expungementApi.saveProgress);
  const {
    loading: docsLoading,
    error: docsError,
    execute: generateDocument,
  } = useApi(documentsApi.generateDocument);
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
      let eligibility, rules, docs;
      if (activeStep === 0) {
        // Eligibility
        eligibility = await checkEligibility(formData);
        if (!eligibility.eligible) {
          throw new Error(eligibility.reason);
        }
      } else if (activeStep === 1) {
        // State Rules
        rules = await fetchStateRules(formData.state);
        setFormData(prev => ({ ...prev, stateRules: rules }));
      } else if (activeStep === 2) {
        // Case Details
        // Additional validation can be added here
      } else if (activeStep === 3) {
        // Documents
        docs = await generateDocument('expungement', formData);
        setFormData(prev => ({ ...prev, documents: [...prev.documents, docs] }));
      }
      setActiveStep(prevStep => prevStep + 1);
    } catch (error) {
      console.error('Error proceeding to next step:', error);
    }
  };
  const handleBack = () => {
    setActiveStep(prevStep => prevStep - 1);
  };
  const validateStep = step => {
    switch (step) {
      case 0:
        return formData.state && formData.caseType;
      case 1:
        return true; // State rules are informational
      case 2:
        return Object.keys(formData.caseDetails).length > 0;
      case 3:
        return formData.documents.length > 0;
      default:
        return true;
    }
  };
  const renderStepContent = step => {
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
                    onChange={e => setFormData({ ...formData, state: e.target.value })}
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
                    onChange={e => setFormData({ ...formData, caseType: e.target.value })}
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
                <Typography variant="body1">{formData.stateRules.description}</Typography>
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
                  onChange={e =>
                    setFormData({
                      ...formData,
                      caseDetails: { ...formData.caseDetails, caseNumber: e.target.value },
                    })
                  }
                />
              </Grid>
              <Grid item xs={12}>
                <TextField
                  fullWidth
                  label={t('expungement.caseDetails.courtName')}
                  value={formData.caseDetails.courtName || ''}
                  onChange={e =>
                    setFormData({
                      ...formData,
                      caseDetails: { ...formData.caseDetails, courtName: e.target.value },
                    })
                  }
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
                  <Paper
                    sx={{
                      p: 2,
                      display: 'flex',
                      justifyContent: 'space-between',
                      alignItems: 'center',
                    }}
                  >
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
            <Paper sx={{ p: 2 }}>{/* Add summary of all information */}</Paper>
          </Box>
        );
      default:
        return null;
    }
  };
  return (
    <Box sx={{ maxWidth: 800, mx: 'auto', p: 3 }}>
      <Paper sx={{ p: 3 }}>
        <Stepper activeStep={activeStep} sx={{ mb: 4 }}>
          {steps.map(label => (
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
        <Box sx={{ display: 'flex', justifyContent: 'space-between', mt: 4 }}>
          <Button 
            disabled={activeStep === 0 || eligibilityLoading || rulesLoading || progressLoading || docsLoading} 
            onClick={handleBack}
          >
            {t('common.back')}
          </Button>
          <Button
            variant="contained"
            onClick={handleNext}
            disabled={eligibilityLoading || rulesLoading || progressLoading || docsLoading}
            endIcon={(eligibilityLoading || rulesLoading || progressLoading || docsLoading) && <CircularProgress size={20} />}
          >
            {activeStep === steps.length - 1 ? t('common.finish') : t('common.next')}
          </Button>
        </Box>
      </Paper>
    </Box>
  );
};
export default ExpungementWizard;