import React, { useState, useEffect } from 'react';
import {
  Box,
  Stepper,
  Step,
  StepLabel,
  StepContent,
  Button,
  Paper,
  Typography,
  CircularProgress,
  Alert
} from '@mui/material';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';

const GuidedFlow = ({
  steps,
  onComplete,
  onStepComplete,
  allowSkip = false,
  showProgress = true,
  persistProgress = true
}) => {
  const [activeStep, setActiveStep] = useState(0);
  const [completed, setCompleted] = useState({});
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [progress, setProgress] = useState(0);
  
  const navigate = useNavigate();
  const { user } = useAuth();

  useEffect(() => {
    if (persistProgress && user) {
      // Load saved progress
      const savedProgress = localStorage.getItem(`flow-progress-${user.id}`);
      if (savedProgress) {
        const { step, completed: completedSteps } = JSON.parse(savedProgress);
        setActiveStep(step);
        setCompleted(completedSteps);
      }
    }
  }, [user, persistProgress]);

  useEffect(() => {
    // Calculate progress percentage
    const completedSteps = Object.keys(completed).length;
    const totalSteps = steps.length;
    const calculatedProgress = (completedSteps / totalSteps) * 100;
    setProgress(calculatedProgress);
  }, [completed, steps.length]);

  const handleNext = async () => {
    setLoading(true);
    setError(null);

    try {
      // If step has validation/completion logic
      if (steps[activeStep].onComplete) {
        await steps[activeStep].onComplete();
      }

      const newCompleted = { ...completed };
      newCompleted[activeStep] = true;
      setCompleted(newCompleted);

      // Save progress if enabled
      if (persistProgress && user) {
        localStorage.setItem(
          `flow-progress-${user.id}`,
          JSON.stringify({
            step: activeStep + 1,
            completed: newCompleted
          })
        );
      }

      // Notify parent component
      onStepComplete?.(activeStep, steps[activeStep]);

      setActiveStep(prevStep => prevStep + 1);
    } catch (err) {
      setError(err.message || 'Failed to complete step');
    } finally {
      setLoading(false);
    }
  };

  const handleBack = () => {
    setActiveStep(prevStep => prevStep - 1);
  };

  const handleSkip = () => {
    if (!allowSkip || !steps[activeStep].optional) {
      return;
    }
    setActiveStep(prevStep => prevStep + 1);
  };

  const handleComplete = async () => {
    setLoading(true);
    setError(null);

    try {
      // Complete final step if it has completion logic
      if (steps[activeStep].onComplete) {
        await steps[activeStep].onComplete();
      }

      const newCompleted = { ...completed };
      newCompleted[activeStep] = true;
      setCompleted(newCompleted);

      // Clear saved progress
      if (persistProgress && user) {
        localStorage.removeItem(`flow-progress-${user.id}`);
      }

      // Notify parent component
      onComplete?.();
    } catch (err) {
      setError(err.message || 'Failed to complete flow');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box sx={{ maxWidth: 800, mx: 'auto', p: 3 }}>
      {showProgress && (
        <Box sx={{ mb: 4, position: 'relative' }}>
          <CircularProgress
            variant="determinate"
            value={progress}
            size={60}
            sx={{ position: 'absolute', color: 'grey.300' }}
          />
          <CircularProgress
            variant="determinate"
            value={progress}
            size={60}
            color="primary"
          />
          <Box
            sx={{
              position: 'absolute',
              top: 0,
              left: 0,
              bottom: 0,
              right: 0,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
            }}
          >
            <Typography variant="caption" color="text.secondary">
              {`${Math.round(progress)}%`}
            </Typography>
          </Box>
        </Box>
      )}

      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}

      <Stepper activeStep={activeStep} orientation="vertical">
        {steps.map((step, index) => (
          <Step key={step.label} completed={completed[index]}>
            <StepLabel optional={step.optional && <Typography variant="caption">Optional</Typography>}>
              {step.label}
            </StepLabel>
            <StepContent>
              <Box sx={{ mb: 2 }}>
                {step.content}
              </Box>
              <Box sx={{ display: 'flex', gap: 1 }}>
                <Button
                  variant="contained"
                  onClick={index === steps.length - 1 ? handleComplete : handleNext}
                  disabled={loading}
                >
                  {loading && <CircularProgress size={20} sx={{ mr: 1 }} />}
                  {index === steps.length - 1 ? 'Finish' : 'Continue'}
                </Button>
                <Button
                  disabled={index === 0 || loading}
                  onClick={handleBack}
                >
                  Back
                </Button>
                {step.optional && allowSkip && (
                  <Button
                    color="inherit"
                    onClick={handleSkip}
                    disabled={loading}
                  >
                    Skip
                  </Button>
                )}
              </Box>
            </StepContent>
          </Step>
        ))}
      </Stepper>

      {activeStep === steps.length && (
        <Paper square elevation={0} sx={{ p: 3, mt: 3, textAlign: 'center' }}>
          <Typography variant="h6" gutterBottom>
            All steps completed!
          </Typography>
          <Button onClick={() => navigate('/')} sx={{ mt: 1 }}>
            Return to Dashboard
          </Button>
        </Paper>
      )}
    </Box>
  );
};

export default GuidedFlow; 