import React, { useState } from 'react';
import {
  Box,
  Typography,
  TextField,
  Button,
  Card,
  CardContent,
  FormControl,
  FormControlLabel,
  RadioGroup,
  Radio,
  FormLabel,
  CircularProgress,
  Alert,
  Divider,
  Paper,
  Stepper,
  Step,
  StepLabel,
} from '@mui/material';
import { useTranslation } from 'react-i18next';
import LocationOnIcon from '@mui/icons-material/LocationOn';
import PropTypes from 'prop-types';
const EmergencyLegalTriage = ({ onComplete }) => {
  const { t } = useTranslation();
  const [activeStep, setActiveStep] = useState(0);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [location, setLocation] = useState('');
  const [locationError, setLocationError] = useState('');
  const [isGettingLocation, setIsGettingLocation] = useState(false);
  const [formData, setFormData] = useState({
    situation: '',
    urgency: 'medium', // default to medium priority
    description: '',
    phoneNumber: '',
    shareLocation: false,
    latitude: null,
    longitude: null,
  });
  const steps = [t('Situation Type'), t('Details'), t('Contact Info')];
  const situations = [
    { id: 'police', label: t('Police Encounter / Detention'), urgency: 'high' },
    { id: 'eviction', label: t('Eviction / Housing Crisis'), urgency: 'high' },
    { id: 'immigration', label: t('Immigration Issue'), urgency: 'medium' },
    { id: 'legal_document', label: t('Legal Document Help'), urgency: 'low' },
    { id: 'court', label: t('Court Appearance'), urgency: 'medium' },
    { id: 'other', label: t('Other Emergency'), urgency: 'medium' },
  ];
  const handleInputChange = e => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value,
    });
    // Auto-set urgency based on situation
    if (name === 'situation') {
      const selectedSituation = situations.find(s => s.id === value);
      if (selectedSituation) {
        setFormData(prev => ({
          ...prev,
          urgency: selectedSituation.urgency,
          situation: value,
        }));
      }
    }
  };
  const handleLocationRequest = () => {
    setIsGettingLocation(true);
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        position => {
          setFormData({
            ...formData,
            latitude: position.coords.latitude,
            longitude: position.coords.longitude,
            shareLocation: true,
          });
          // Simulate reverse geocoding (in a real app, you'd use a geocoding service)
          setTimeout(() => {
            setLocation('Location detected');
            setIsGettingLocation(false);
          }, 1000);
        },
        error => {
          setLocationError(t('Unable to get your location. Please enter it manually.'));
          setIsGettingLocation(false);
        }
      );
    } else {
      setLocationError(t('Geolocation is not supported by your browser.'));
      setIsGettingLocation(false);
    }
  };
  const validateStep = () => {
    if (activeStep === 0 && !formData.situation) {
      return false;
    }
    if (activeStep === 1 && !formData.description) {
      return false;
    }
    if (activeStep === 2 && !formData.phoneNumber) {
      return false;
    }
    return true;
  };
  const handleNext = () => {
    if (validateStep()) {
      if (activeStep === steps.length - 1) {
        handleSubmit();
      } else {
        setActiveStep(prevStep => prevStep + 1);
      }
    }
  };
  const handleBack = () => {
    setActiveStep(prevStep => prevStep - 1);
  };
  const handleSubmit = () => {
    setIsSubmitting(true);
    // Simulate API call
    setTimeout(() => {
      if (onComplete) {
        onComplete(formData);
      }
      setIsSubmitting(false);
    }, 1500);
  };
  const renderStepContent = step => {
    switch (step) {
      case 0:
        return (
          <Box sx={{ mt: 4 }}>
            <FormControl component="fieldset" fullWidth>
              <FormLabel component="legend">
                {t('What type of legal situation are you facing?')}
              </FormLabel>
              <RadioGroup
                name="situation"
                value={formData.situation}
                onChange={handleInputChange}
                sx={{ mt: 2 }}
              >
                {situations.map(situation => (
                  <Paper
                    key={situation.id}
                    elevation={formData.situation === situation.id ? 3 : 1}
                    sx={{
                      mb: 2,
                      p: 1,
                      borderLeft:
                        formData.situation === situation.id ? '4px solid #f44336' : 'none',
                      transition: 'all 0.2s',
                    }}
                  >
                    <FormControlLabel
                      value={situation.id}
                      control={<Radio />}
                      label={
                        <Box>
                          <Typography variant="body1">{situation.label}</Typography>
                          <Typography variant="caption" color="text.secondary">
                            {situation.urgency === 'high'
                              ? t('High Priority')
                              : situation.urgency === 'medium'
                                ? t('Medium Priority')
                                : t('Standard Priority')}
                          </Typography>
                        </Box>
                      }
                    />
                  </Paper>
                ))}
              </RadioGroup>
            </FormControl>
          </Box>
        );
      case 1:
        return (
          <Box sx={{ mt: 4 }}>
            <Typography variant="body1" gutterBottom>
              {t('Please provide more details about your situation:')}
            </Typography>
            <TextField
              name="description"
              value={formData.description}
              onChange={handleInputChange}
              multiline
              rows={4}
              fullWidth
              placeholder={t('Describe your current legal situation in detail...')}
              required
              sx={{ mt: 2 }}
            />
            <Box sx={{ mt: 3 }}>
              <Typography variant="body1" gutterBottom>
                {t('Your location:')}
              </Typography>
              <Box sx={{ display: 'flex', alignItems: 'center', mt: 1 }}>
                <TextField
                  name="location"
                  value={location}
                  onChange={e => setLocation(e.target.value)}
                  fullWidth
                  placeholder={t('Your current location')}
                  sx={{ mr: 1 }}
                  error={!!locationError}
                  helperText={locationError}
                  disabled={isGettingLocation}
                />
                <Button
                  variant="outlined"
                  startIcon={<LocationOnIcon />}
                  onClick={handleLocationRequest}
                  disabled={isGettingLocation}
                >
                  {isGettingLocation ? <CircularProgress size={24} /> : t('Get Location')}
                </Button>
              </Box>
              {formData.latitude && formData.longitude && (
                <Alert severity="success" sx={{ mt: 2 }}>
                  {t('Location successfully captured')}
                  <Box
                    sx={{
                      mt: 2,
                      height: 150,
                      bgcolor: 'rgba(0,0,0,0.03)',
                      borderRadius: 1,
                      overflow: 'hidden',
                      position: 'relative',
                    }}
                  >
                    <Box
                      component="img"
                      sx={{
                        width: '100%',
                        height: '100%',
                        objectFit: 'cover',
                      }}
                      alt="Location map"
                      src={`https://maps.googleapis.com/maps/api/staticmap?center=${formData.latitude},${formData.longitude}&zoom=14&size=600x150&maptype=roadmap&markers=color:red%7C${formData.latitude},${formData.longitude}&key=YOUR_API_KEY_HERE`}
                    />
                    <Typography
                      variant="caption"
                      sx={{
                        position: 'absolute',
                        bottom: 0,
                        left: 0,
                        width: '100%',
                        bgcolor: 'rgba(255,255,255,0.7)',
                        p: 0.5,
                        textAlign: 'center',
                      }}
                    >
                      {t('This is a placeholder. In a production app, this would show a real map.')}
                    </Typography>
                  </Box>
                </Alert>
              )}
            </Box>
          </Box>
        );
      case 2:
        return (
          <Box sx={{ mt: 4 }}>
            <Typography variant="body1" gutterBottom>
              {t('How can we contact you?')}
            </Typography>
            <TextField
              name="phoneNumber"
              value={formData.phoneNumber}
              onChange={handleInputChange}
              fullWidth
              placeholder={t('Phone number')}
              required
              sx={{ mt: 2 }}
              helperText={t('This is required so we can call you back if disconnected')}
            />
            <Alert severity="info" sx={{ mt: 4 }}>
              <Typography variant="body2">
                {t(
                  "After you submit, we'll connect you with a legal advocate as quickly as possible based on your situation priority."
                )}
              </Typography>
            </Alert>
          </Box>
        );
      default:
        return null;
    }
  };
  return (
    <Card sx={{ maxWidth: 800, mx: 'auto', mt: 4 }}>
      <CardContent>
        <Typography variant="h5" component="h2" gutterBottom>
          {t('Emergency Legal Assistance')}
        </Typography>
        <Stepper activeStep={activeStep} sx={{ mb: 4 }}>
          {steps.map(label => (
            <Step key={label}>
              <StepLabel>{label}</StepLabel>
            </Step>
          ))}
        </Stepper>
        <Divider sx={{ mb: 3 }} />
        {renderStepContent(activeStep)}
        <Box sx={{ display: 'flex', justifyContent: 'space-between', mt: 4 }}>
          <Button onClick={handleBack} disabled={activeStep === 0 || isSubmitting}>
            {t('Back')}
          </Button>
          <Button
            variant="contained"
            color={activeStep === steps.length - 1 ? 'error' : 'primary'}
            onClick={handleNext}
            disabled={!validateStep() || isSubmitting}
          >
            {isSubmitting ? (
              <CircularProgress size={24} color="inherit" />
            ) : activeStep === steps.length - 1 ? (
              t('Connect Now')
            ) : (
              t('Next')
            )}
          </Button>
        </Box>
      </CardContent>
    </Card>
  );
};

// Define PropTypes
EmergencyLegalTriage.propTypes = {
  /** TODO: Add description */
  onComplete: PropTypes.any,
};

export default EmergencyLegalTriage;