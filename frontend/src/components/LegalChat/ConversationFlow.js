import React, { useState, useEffect } from 'react';
import {
  Box,
  Stepper,
  Step,
  StepLabel,
  Typography,
  TextField,
  Button,
  Card,
  CardContent,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Chip,
} from '@mui/material';
import { styled } from '@mui/material/styles';

const ConversationCard = styled(Card)(({ theme }) => ({
  marginBottom: theme.spacing(2),
  backgroundColor: theme.palette.background.default,
}));

const legalCategories = [
  'Housing & Eviction',
  'Employment',
  'Family Law',
  'Immigration',
  'Consumer Rights',
  'Criminal Record',
  'Small Claims',
  'Public Benefits',
];

const initialQuestions = {
  'Housing & Eviction': [
    'Are you currently facing eviction?',
    'Do you have a written lease?',
    'Have you received any formal notices?',
    'What is your current rental situation?',
  ],
  'Employment': [
    'Are you currently employed?',
    'What type of employment issue are you facing?',
    'Have you filed any formal complaints?',
    'When did this issue begin?',
  ],
  // Add questions for other categories...
};

const ConversationFlow = () => {
  const [activeStep, setActiveStep] = useState(0);
  const [category, setCategory] = useState('');
  const [answers, setAnswers] = useState({});
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [summary, setSummary] = useState('');

  const steps = ['Legal Category', 'Initial Assessment', 'Detailed Information', 'Summary & Next Steps'];

  const handleCategoryChange = (event) => {
    setCategory(event.target.value);
    setAnswers({});
    setCurrentQuestion(0);
  };

  const handleAnswerChange = (question, answer) => {
    setAnswers(prev => ({
      ...prev,
      [question]: answer
    }));
  };

  const handleNext = () => {
    if (activeStep === steps.length - 1) {
      // Handle completion
      return;
    }
    setActiveStep(prev => prev + 1);
  };

  const handleBack = () => {
    setActiveStep(prev => prev - 1);
  };

  useEffect(() => {
    if (activeStep === 3) {
      // Generate summary based on answers
      const summaryText = `Legal Category: ${category}\n\n` +
        Object.entries(answers)
          .map(([question, answer]) => `${question}:\n${answer}`)
          .join('\n\n');
      setSummary(summaryText);
    }
  }, [activeStep, category, answers]);

  const renderStepContent = (step) => {
    switch (step) {
      case 0:
        return (
          <FormControl fullWidth>
            <InputLabel>Select Legal Category</InputLabel>
            <Select value={category} onChange={handleCategoryChange}>
              {legalCategories.map((cat) => (
                <MenuItem key={cat} value={cat}>{cat}</MenuItem>
              ))}
            </Select>
          </FormControl>
        );

      case 1:
        return category ? (
          <Box>
            <Typography variant="h6" gutterBottom>
              Initial Assessment Questions
            </Typography>
            {initialQuestions[category]?.map((question, index) => (
              <TextField
                key={index}
                fullWidth
                multiline
                label={question}
                value={answers[question] || ''}
                onChange={(e) => handleAnswerChange(question, e.target.value)}
                margin="normal"
              />
            ))}
          </Box>
        ) : (
          <Typography color="error">Please select a legal category first</Typography>
        );

      case 2:
        return (
          <Box>
            <Typography variant="h6" gutterBottom>
              Additional Information
            </Typography>
            <TextField
              fullWidth
              multiline
              rows={4}
              label="Please provide any additional details about your situation"
              value={answers.additionalInfo || ''}
              onChange={(e) => handleAnswerChange('additionalInfo', e.target.value)}
              margin="normal"
            />
            <TextField
              fullWidth
              label="Have you taken any steps to address this issue?"
              value={answers.stepsTaken || ''}
              onChange={(e) => handleAnswerChange('stepsTaken', e.target.value)}
              margin="normal"
            />
          </Box>
        );

      case 3:
        return (
          <Box>
            <Typography variant="h6" gutterBottom>
              Summary of Your Legal Matter
            </Typography>
            <ConversationCard>
              <CardContent>
                <Typography variant="body1" style={{ whiteSpace: 'pre-line' }}>
                  {summary}
                </Typography>
              </CardContent>
            </ConversationCard>
            <Box sx={{ mt: 2 }}>
              <Typography variant="h6" gutterBottom>
                Recommended Next Steps:
              </Typography>
              <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
                <Chip label="Schedule Consultation" color="primary" />
                <Chip label="Review Documents" color="primary" />
                <Chip label="Legal Research" color="primary" />
              </Box>
            </Box>
          </Box>
        );

      default:
        return null;
    }
  };

  return (
    <Box sx={{ width: '100%', mt: 3 }}>
      <Stepper activeStep={activeStep} alternativeLabel>
        {steps.map((label) => (
          <Step key={label}>
            <StepLabel>{label}</StepLabel>
          </Step>
        ))}
      </Stepper>
      <Box sx={{ mt: 4, mb: 2 }}>
        {renderStepContent(activeStep)}
      </Box>
      <Box sx={{ display: 'flex', justifyContent: 'flex-end', mt: 2 }}>
        <Button
          disabled={activeStep === 0}
          onClick={handleBack}
          sx={{ mr: 1 }}
        >
          Back
        </Button>
        <Button
          variant="contained"
          onClick={handleNext}
          disabled={!category || (activeStep === 1 && Object.keys(answers).length === 0)}
        >
          {activeStep === steps.length - 1 ? 'Finish' : 'Next'}
        </Button>
      </Box>
    </Box>
  );
};

export default ConversationFlow; 