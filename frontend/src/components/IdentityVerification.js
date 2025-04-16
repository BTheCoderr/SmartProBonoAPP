import React, { useState } from 'react';
import {
  Box,
  Paper,
  Typography,
  Stepper,
  Step,
  StepLabel,
  Button,
  CircularProgress,
  Alert,
  TextField,
  FormControlLabel,
  Checkbox,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
} from '@mui/material';
import {
  VerifiedUser as VerifiedUserIcon,
  PhotoCamera as PhotoCameraIcon,
  Upload as UploadIcon,
  CheckCircle as CheckCircleIcon,
} from '@mui/icons-material';
import { useTranslation } from 'react-i18next';
import PropTypes from 'prop-types';
const IdentityVerification = ({ onVerificationComplete }) => {
  const { t } = useTranslation();
  const [activeStep, setActiveStep] = useState(0);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [verificationData, setVerificationData] = useState({
    documentType: '',
    documentNumber: '',
    consentToVerification: false,
  });
  const [showCamera, setShowCamera] = useState(false);
  const [documentImage, setDocumentImage] = useState(null);
  const steps = [
    t('verification.steps.consent'),
    t('verification.steps.document'),
    t('verification.steps.photo'),
    t('verification.steps.verify'),
  ];
  const handleDocumentCapture = async file => {
    setLoading(true);
    try {
      const formData = new FormData();
      formData.append('document', file);
      const response = await fetch('/api/verify/document', {
        method: 'POST',
        body: formData,
      });
      if (!response.ok) throw new Error('Document verification failed');
      const data = await response.json();
      setDocumentImage(data.imageUrl);
      setVerificationData(prev => ({
        ...prev,
        documentData: data.documentData,
      }));
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };
  const handleVerification = async () => {
    setLoading(true);
    try {
      const response = await fetch('/api/verify/identity', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(verificationData),
      });
      if (!response.ok) throw new Error('Verification failed');
      const data = await response.json();
      onVerificationComplete(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };
  const renderStepContent = step => {
    switch (step) {
      case 0:
        return (
          <Box>
            <Typography paragraph>{t('verification.consent.description')}</Typography>
            <FormControlLabel
              control={
                <Checkbox
                  checked={verificationData.consentToVerification}
                  onChange={e =>
                    setVerificationData(prev => ({
                      ...prev,
                      consentToVerification: e.target.checked,
                    }))
                  }
                />
              }
              label={t('verification.consent.agree')}
            />
          </Box>
        );
      case 1:
        return (
          <Box>
            <TextField
              fullWidth
              select
              label={t('verification.document.type')}
              value={verificationData.documentType}
              onChange={e =>
                setVerificationData(prev => ({
                  ...prev,
                  documentType: e.target.value,
                }))
              }
              SelectProps={{
                native: true,
              }}
              sx={{ mb: 2 }}
            >
              <option value="">{t('common.select')}</option>
              <option value="drivers_license">{t('verification.document.driversLicense')}</option>
              <option value="passport">{t('verification.document.passport')}</option>
              <option value="state_id">{t('verification.document.stateId')}</option>
            </TextField>
            <TextField
              fullWidth
              label={t('verification.document.number')}
              value={verificationData.documentNumber}
              onChange={e =>
                setVerificationData(prev => ({
                  ...prev,
                  documentNumber: e.target.value,
                }))
              }
            />
          </Box>
        );
      case 2:
        return (
          <Box sx={{ textAlign: 'center' }}>
            {documentImage ? (
              <Box>
                <img
                  src={documentImage}
                  alt="Document"
                  style={{ maxWidth: '100%', maxHeight: 200, marginBottom: 16 }}
                />
                <Button
                  variant="outlined"
                  startIcon={<PhotoCameraIcon />}
                  onClick={() => setShowCamera(true)}
                >
                  {t('verification.photo.retake')}
                </Button>
              </Box>
            ) : (
              <Button
                variant="contained"
                startIcon={<PhotoCameraIcon />}
                onClick={() => setShowCamera(true)}
              >
                {t('verification.photo.take')}
              </Button>
            )}
          </Box>
        );
      case 3:
        return (
          <Box sx={{ textAlign: 'center' }}>
            <CircularProgress sx={{ mb: 2 }} />
            <Typography>{t('verification.verify.processing')}</Typography>
          </Box>
        );
      default:
        return null;
    }
  };
  return (
    <Box sx={{ mb: 4 }}>
      <Paper elevation={3} sx={{ p: 3 }}>
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 3 }}>
          <VerifiedUserIcon sx={{ fontSize: 32, mr: 2, color: 'primary.main' }} />
          <Typography variant="h5">{t('verification.title')}</Typography>
        </Box>
        <Stepper activeStep={activeStep} sx={{ mb: 4 }}>
          {steps.map(label => (
            <Step key={label}>
              <StepLabel>{label}</StepLabel>
            </Step>
          ))}
        </Stepper>
        {error && (
          <Alert severity="error" sx={{ mb: 3 }} onClose={() => setError(null)}>
            {error}
          </Alert>
        )}
        {renderStepContent(activeStep)}
        <Box sx={{ mt: 4, display: 'flex', justifyContent: 'space-between' }}>
          <Button
            disabled={activeStep === 0 || loading}
            onClick={() => setActiveStep(prev => prev - 1)}
          >
            {t('common.back')}
          </Button>
          <Button
            variant="contained"
            disabled={loading || (activeStep === 0 && !verificationData.consentToVerification)}
            onClick={() => {
              if (activeStep === steps.length - 1) {
                handleVerification();
              } else {
                setActiveStep(prev => prev + 1);
              }
            }}
          >
            {activeStep === steps.length - 1 ? t('verification.verify.submit') : t('common.next')}
          </Button>
        </Box>
        <Dialog open={showCamera} onClose={() => setShowCamera(false)} maxWidth="md" fullWidth>
          <DialogTitle>{t('verification.photo.instructions')}</DialogTitle>
          <DialogContent>
            {/* Add your camera component here */}
            <Box
              sx={{
                height: 400,
                bgcolor: 'grey.100',
                display: 'flex',
                justifyContent: 'center',
                alignItems: 'center',
              }}
            >
              <Typography color="text.secondary">Camera Preview</Typography>
            </Box>
          </DialogContent>
          <DialogActions>
            <Button onClick={() => setShowCamera(false)}>{t('common.cancel')}</Button>
            <Button
              variant="contained"
              onClick={() => {
                // Handle photo capture
                setShowCamera(false);
              }}
            >
              {t('verification.photo.capture')}
            </Button>
          </DialogActions>
        </Dialog>
      </Paper>
    </Box>
  );
};

// Define PropTypes
IdentityVerification.propTypes = {
  /** TODO: Add description */
  onVerificationComplete: PropTypes.any,
};

export default IdentityVerification;