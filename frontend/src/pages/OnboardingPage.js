import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import ApiService from '../services/ApiService';
import { Button, TextField, Typography, Box, Paper, Stepper, Step, StepLabel } from '@mui/material';
import ErrorOutlineIcon from '@mui/icons-material/ErrorOutline';

const questions = [
  {
    key: 'legalCategory',
    label: 'What type of legal help do you need?',
    placeholder: 'e.g., Housing, Family, Employment, Immigration',
    required: true,
  },
  {
    key: 'situation',
    label: 'Briefly describe your situation.',
    placeholder: 'Tell us what happened...',
    required: true,
  },
  {
    key: 'urgency',
    label: 'How urgent is your situation?',
    placeholder: 'e.g., Emergency, Soon, Not urgent',
    required: true,
  },
  {
    key: 'location',
    label: 'Where is your legal issue taking place?',
    placeholder: 'City, State',
    required: false,
  },
];

const OnboardingPage = () => {
  const [step, setStep] = useState(0);
  const [answers, setAnswers] = useState({});
  const [error, setError] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const navigate = useNavigate();

  const handleChange = (e) => {
    setAnswers({ ...answers, [questions[step].key]: e.target.value });
    setError('');
  };

  const handleNext = () => {
    if (questions[step].required && !answers[questions[step].key]) {
      setError('This field is required.');
      return;
    }
    setStep((prev) => prev + 1);
    setError('');
  };

  const handleBack = () => {
    setStep((prev) => prev - 1);
    setError('');
  };

  const handleSubmit = async () => {
    if (questions[step].required && !answers[questions[step].key]) {
      setError('This field is required.');
      return;
    }
    setSubmitting(true);
    setError('');
    try {
      await ApiService.post('/api/onboarding', answers);
      navigate('/dashboard');
    } catch (err) {
      setError('Failed to submit onboarding. Please try again.');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <Box display="flex" justifyContent="center" alignItems="center" minHeight="80vh" bgcolor="#f5f6fa">
      <Paper elevation={3} sx={{ p: 4, width: 400 }}>
        <Typography variant="h5" gutterBottom>
          Welcome! Let's get you started
        </Typography>
        <Stepper activeStep={step} alternativeLabel sx={{ mb: 3 }}>
          {questions.map((q, idx) => (
            <Step key={q.key} completed={step > idx}>
              <StepLabel>{q.label}</StepLabel>
            </Step>
          ))}
        </Stepper>
        <Typography variant="subtitle1" sx={{ mb: 1 }}>
          {questions[step].label}
        </Typography>
        <TextField
          fullWidth
          placeholder={questions[step].placeholder}
          value={answers[questions[step].key] || ''}
          onChange={handleChange}
          disabled={submitting}
          autoFocus
          error={!!error}
          helperText={error ? (
            <span style={{ color: 'red', display: 'flex', alignItems: 'center' }}><ErrorOutlineIcon fontSize="small" style={{ marginRight: 4 }} />{error}</span>
          ) : ''}
        />
        <Box display="flex" justifyContent="space-between" mt={3}>
          <Button
            variant="outlined"
            onClick={handleBack}
            disabled={step === 0 || submitting}
          >
            Back
          </Button>
          {step < questions.length - 1 ? (
            <Button
              variant="contained"
              onClick={handleNext}
              disabled={submitting}
            >
              Next
            </Button>
          ) : (
            <Button
              variant="contained"
              onClick={handleSubmit}
              disabled={submitting}
            >
              {submitting ? 'Submitting...' : 'Finish'}
            </Button>
          )}
        </Box>
      </Paper>
    </Box>
  );
};

export default OnboardingPage; 