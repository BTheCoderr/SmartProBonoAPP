import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Box,
  Container,
  Typography,
  Button,
  Paper,
  MobileStepper,
  Card,
  CardContent,
  CardMedia,
  CardActions,
  Grid,
} from '@mui/material';
import KeyboardArrowLeft from '@mui/icons-material/KeyboardArrowLeft';
import KeyboardArrowRight from '@mui/icons-material/KeyboardArrowRight';

const steps = [
  {
    label: "Welcome to Smart Pro Bono",
    description: "We're here to help you navigate your legal journey. Let's get started with a few simple steps.",
    image: "/onboarding/welcome.jpg",
    action: {
      label: "Start Your Journey",
      path: "/intake",
    },
  },
  {
    label: "Complete Your Profile",
    description: "Help us understand your situation better by providing some basic information about yourself.",
    image: "/onboarding/profile.jpg",
    action: {
      label: "Update Profile",
      path: "/profile",
    },
  },
  {
    label: "Review Legal Resources",
    description: "Access our library of legal guides, templates, and helpful information tailored to your needs.",
    image: "/onboarding/resources.jpg",
    action: {
      label: "Browse Resources",
      path: "/resources",
    },
  },
  {
    label: "Document Upload Center",
    description: "Securely upload and manage your important documents for legal review.",
    image: "/onboarding/documents.jpg",
    action: {
      label: "Upload Documents",
      path: "/documents",
    },
  },
  {
    label: "Schedule Consultation",
    description: "Book a consultation with one of our legal professionals to discuss your case.",
    image: "/onboarding/consultation.jpg",
    action: {
      label: "Schedule Now",
      path: "/schedule",
    },
  },
];

export default function OnboardingPage() {
  const [activeStep, setActiveStep] = useState(0);
  const navigate = useNavigate();
  const maxSteps = steps.length;

  const handleNext = () => {
    setActiveStep((prevStep) => prevStep + 1);
  };

  const handleBack = () => {
    setActiveStep((prevStep) => prevStep - 1);
  };

  const handleSkip = () => {
    navigate('/home');
  };

  const currentStep = steps[activeStep];

  return (
    <Container maxWidth="md">
      <Box sx={{ mt: 4, mb: 8 }}>
        <Paper elevation={3} sx={{ p: 3 }}>
          <Typography variant="h4" component="h1" gutterBottom align="center" sx={{ mb: 4 }}>
            Getting Started
          </Typography>

          <Card sx={{ maxWidth: '100%', mb: 4 }}>
            <CardMedia
              component="img"
              height="240"
              image={currentStep.image}
              alt={currentStep.label}
              sx={{ objectFit: 'cover' }}
            />
            <CardContent>
              <Typography variant="h5" gutterBottom>
                {currentStep.label}
              </Typography>
              <Typography variant="body1" color="text.secondary" paragraph>
                {currentStep.description}
              </Typography>
            </CardContent>
            <CardActions>
              <Button
                size="large"
                variant="contained"
                onClick={() => navigate(currentStep.action.path)}
                sx={{ mx: 2, mb: 2 }}
                fullWidth
              >
                {currentStep.action.label}
              </Button>
            </CardActions>
          </Card>

          <Box sx={{ mb: 2 }}>
            <Grid container spacing={2}>
              <Grid item xs={12} sm={6}>
                <Button
                  size="small"
                  onClick={handleSkip}
                  sx={{ mr: 1 }}
                >
                  Skip Tutorial
                </Button>
              </Grid>
              <Grid item xs={12} sm={6}>
                <MobileStepper
                  variant="dots"
                  steps={maxSteps}
                  position="static"
                  activeStep={activeStep}
                  sx={{ flexGrow: 1, bgcolor: 'background.paper' }}
                  nextButton={
                    <Button
                      size="small"
                      onClick={handleNext}
                      disabled={activeStep === maxSteps - 1}
                    >
                      Next
                      <KeyboardArrowRight />
                    </Button>
                  }
                  backButton={
                    <Button
                      size="small"
                      onClick={handleBack}
                      disabled={activeStep === 0}
                    >
                      <KeyboardArrowLeft />
                      Back
                    </Button>
                  }
                />
              </Grid>
            </Grid>
          </Box>

          <Box sx={{ mt: 4, textAlign: 'center' }}>
            <Typography variant="body2" color="text.secondary">
              Need help? Contact our support team at support@smartprobono.com
            </Typography>
          </Box>
        </Paper>
      </Box>
    </Container>
  );
} 