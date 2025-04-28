import React, { useState } from 'react';
import {
  Box,
  Button,
  Card,
  CardContent,
  Container,
  Grid,
  Step,
  StepLabel,
  Stepper,
  TextField,
  Typography,
  CircularProgress,
  Alert,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  useTheme,
  useMediaQuery
} from '@mui/material';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { ApiService } from '../services/ApiService';

const steps = ['Legal Category', 'Situation Details', 'Financial Information', 'Contact Preferences'];

const legalCategories = [
  {
    id: 'housing',
    title: 'Housing Law',
    description: 'Eviction, repairs, lease disputes, and housing discrimination.',
    commonIssues: ['Eviction Defense', 'Repairs', 'Security Deposits', 'Discrimination']
  },
  {
    id: 'family',
    title: 'Family Law',
    description: 'Divorce, custody, support, and domestic violence.',
    commonIssues: ['Divorce', 'Child Custody', 'Support Orders', 'Protection Orders']
  },
  {
    id: 'employment',
    title: 'Employment Law',
    description: 'Wage disputes, discrimination, and workplace safety.',
    commonIssues: ['Wage Claims', 'Discrimination', 'Harassment', 'Wrongful Termination']
  }
];

export default function OnboardingFlow() {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('sm'));
  const navigate = useNavigate();
  const { user } = useAuth();
  
  const [activeStep, setActiveStep] = useState(0);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [formData, setFormData] = useState({
    legalCategory: '',
    situationDetails: {
      description: '',
      urgency: 'medium',
      previousLegalHelp: false
    },
    financialInfo: {
      monthlyIncome: '',
      householdSize: '',
      governmentBenefits: []
    },
    contactPreferences: {
      preferredMethod: 'email',
      bestTimeToContact: '',
      additionalNotes: ''
    }
  });

  const handleNext = () => {
    if (activeStep === steps.length - 1) {
      handleSubmit();
    } else {
      setActiveStep((prevStep) => prevStep + 1);
    }
  };

  const handleBack = () => {
    setActiveStep((prevStep) => prevStep - 1);
  };

  const handleSubmit = async () => {
    try {
      setLoading(true);
      setError('');

      const response = await ApiService.post('/api/onboarding', {
        userId: user.id,
        ...formData
      });

      if (response.data.nextSteps) {
        navigate('/dashboard', { 
          state: { 
            onboardingComplete: true,
            nextSteps: response.data.nextSteps 
          }
        });
      }
    } catch (err) {
      setError(err.response?.data?.message || 'An error occurred during submission');
    } finally {
      setLoading(false);
    }
  };

  const handleInputChange = (section, field, value) => {
    setFormData(prev => ({
      ...prev,
      [section]: typeof field === 'string' 
        ? value 
        : {
          ...prev[section],
          [field]: value
        }
    }));
  };

  const isStepValid = () => {
    switch (activeStep) {
      case 0:
        return !!formData.legalCategory;
      case 1:
        return !!formData.situationDetails.description;
      case 2:
        return !!formData.financialInfo.monthlyIncome && 
               !!formData.financialInfo.householdSize;
      case 3:
        return !!formData.contactPreferences.preferredMethod;
      default:
        return false;
    }
  };

  const renderStepContent = (step) => {
    switch (step) {
      case 0:
        return (
          <Grid container spacing={3}>
            {legalCategories.map((category) => (
              <Grid item xs={12} md={4} key={category.id}>
                <Card 
                  sx={{ 
                    height: '100%',
                    cursor: 'pointer',
                    border: formData.legalCategory === category.id 
                      ? `2px solid ${theme.palette.primary.main}` 
                      : 'none'
                  }}
                  onClick={() => handleInputChange('legalCategory', null, category.id)}
                >
                  <CardContent>
                    <Typography variant="h6" gutterBottom>
                      {category.title}
                    </Typography>
                    <Typography variant="body2" color="text.secondary" paragraph>
                      {category.description}
                    </Typography>
                    <Typography variant="subtitle2" gutterBottom>
                      Common Issues:
                    </Typography>
                    <ul>
                      {category.commonIssues.map((issue) => (
                        <li key={issue}>
                          <Typography variant="body2">{issue}</Typography>
                        </li>
                      ))}
                    </ul>
                  </CardContent>
                </Card>
              </Grid>
            ))}
          </Grid>
        );

      case 1:
        return (
          <Box>
            <TextField
              fullWidth
              multiline
              rows={4}
              label="Describe your situation"
              value={formData.situationDetails.description}
              onChange={(e) => handleInputChange('situationDetails', 'description', e.target.value)}
              margin="normal"
            />
            <FormControl fullWidth margin="normal">
              <InputLabel>How urgent is your situation?</InputLabel>
              <Select
                value={formData.situationDetails.urgency}
                onChange={(e) => handleInputChange('situationDetails', 'urgency', e.target.value)}
                label="How urgent is your situation?"
              >
                <MenuItem value="low">Not urgent - I need general advice</MenuItem>
                <MenuItem value="medium">Somewhat urgent - I need help soon</MenuItem>
                <MenuItem value="high">Very urgent - I need immediate assistance</MenuItem>
              </Select>
            </FormControl>
          </Box>
        );

      case 2:
        return (
          <Box>
            <TextField
              fullWidth
              type="number"
              label="Monthly Household Income"
              value={formData.financialInfo.monthlyIncome}
              onChange={(e) => handleInputChange('financialInfo', 'monthlyIncome', e.target.value)}
              margin="normal"
            />
            <TextField
              fullWidth
              type="number"
              label="Number of people in household"
              value={formData.financialInfo.householdSize}
              onChange={(e) => handleInputChange('financialInfo', 'householdSize', e.target.value)}
              margin="normal"
            />
            <FormControl fullWidth margin="normal">
              <InputLabel>Government Benefits Received</InputLabel>
              <Select
                multiple
                value={formData.financialInfo.governmentBenefits}
                onChange={(e) => handleInputChange('financialInfo', 'governmentBenefits', e.target.value)}
                label="Government Benefits Received"
              >
                <MenuItem value="ssi">SSI</MenuItem>
                <MenuItem value="snap">SNAP/Food Stamps</MenuItem>
                <MenuItem value="tanf">TANF</MenuItem>
                <MenuItem value="medicaid">Medicaid</MenuItem>
              </Select>
            </FormControl>
          </Box>
        );

      case 3:
        return (
          <Box>
            <FormControl fullWidth margin="normal">
              <InputLabel>Preferred Contact Method</InputLabel>
              <Select
                value={formData.contactPreferences.preferredMethod}
                onChange={(e) => handleInputChange('contactPreferences', 'preferredMethod', e.target.value)}
                label="Preferred Contact Method"
              >
                <MenuItem value="email">Email</MenuItem>
                <MenuItem value="phone">Phone</MenuItem>
                <MenuItem value="text">Text Message</MenuItem>
              </Select>
            </FormControl>
            <TextField
              fullWidth
              label="Best time to contact you"
              value={formData.contactPreferences.bestTimeToContact}
              onChange={(e) => handleInputChange('contactPreferences', 'bestTimeToContact', e.target.value)}
              margin="normal"
            />
            <TextField
              fullWidth
              multiline
              rows={3}
              label="Additional Notes"
              value={formData.contactPreferences.additionalNotes}
              onChange={(e) => handleInputChange('contactPreferences', 'additionalNotes', e.target.value)}
              margin="normal"
            />
          </Box>
        );

      default:
        return null;
    }
  };

  return (
    <Container maxWidth="lg">
      <Box sx={{ width: '100%', mt: 4 }}>
        <Stepper 
          activeStep={activeStep} 
          orientation={isMobile ? 'vertical' : 'horizontal'}
        >
          {steps.map((label) => (
            <Step key={label}>
              <StepLabel>{label}</StepLabel>
            </Step>
          ))}
        </Stepper>

        <Box sx={{ mt: 4, mb: 2 }}>
          <Typography variant="h5" gutterBottom>
            {steps[activeStep]}
          </Typography>
          {error && (
            <Alert severity="error" sx={{ mb: 2 }}>
              {error}
            </Alert>
          )}
          {renderStepContent(activeStep)}
        </Box>

        <Box sx={{ display: 'flex', justifyContent: 'space-between', mt: 4 }}>
          <Button
            disabled={activeStep === 0 || loading}
            onClick={handleBack}
          >
            Back
          </Button>
          <Button
            variant="contained"
            onClick={handleNext}
            disabled={!isStepValid() || loading}
          >
            {loading ? (
              <CircularProgress size={24} />
            ) : activeStep === steps.length - 1 ? (
              'Submit'
            ) : (
              'Next'
            )}
          </Button>
        </Box>
      </Box>
    </Container>
  );
} 