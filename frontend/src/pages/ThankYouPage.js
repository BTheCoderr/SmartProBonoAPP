import React, { useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import {
  Box,
  Container,
  Typography,
  Button,
  Paper,
  Stepper,
  Step,
  StepLabel,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Grid,
  Card,
  CardContent,
  Alert,
  Divider,
} from '@mui/material';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import ArticleIcon from '@mui/icons-material/Article';
import PersonIcon from '@mui/icons-material/Person';
import CalendarTodayIcon from '@mui/icons-material/CalendarToday';
import UploadFileIcon from '@mui/icons-material/UploadFile';
import AssignmentIcon from '@mui/icons-material/Assignment';

const steps = ['Form Submitted', 'Document Upload', 'Review Process', 'Consultation'];

export default function ThankYouPage() {
  const navigate = useNavigate();
  const location = useLocation();
  const formData = location.state?.formData || {};
  const intakeId = location.state?.intakeId;

  useEffect(() => {
    if (!intakeId) {
      navigate('/intake');
    }
  }, [intakeId, navigate]);

  const requiredDocuments = [
    'Government-issued ID',
    'Proof of residence',
    'Immigration documents',
    'Supporting evidence',
    'Financial documents',
  ];

  const nextSteps = [
    {
      title: 'Upload Required Documents',
      icon: <UploadFileIcon color="primary" />,
      description: 'Submit all necessary documentation for your case',
      action: () => navigate('/documents'),
      urgent: true,
    },
    {
      title: 'Complete Your Profile',
      icon: <PersonIcon color="primary" />,
      description: 'Add additional information to your profile',
      action: () => navigate('/profile'),
    },
    {
      title: 'Review Legal Resources',
      icon: <ArticleIcon color="primary" />,
      description: 'Access guides and information relevant to your case',
      action: () => navigate('/resources'),
    },
    {
      title: 'Schedule Consultation',
      icon: <CalendarTodayIcon color="primary" />,
      description: 'Book a meeting with a legal professional',
      action: () => navigate('/schedule'),
    },
  ];

  return (
    <Container maxWidth="md">
      <Box sx={{ mt: 8, mb: 4 }}>
        <Paper elevation={3} sx={{ p: 4 }}>
          <Box sx={{ textAlign: 'center', mb: 4 }}>
            <CheckCircleIcon color="success" sx={{ fontSize: 64, mb: 2 }} />
            <Typography variant="h4" component="h1" gutterBottom>
              Thank You for Your Submission!
            </Typography>
            <Typography variant="subtitle1" color="text.secondary" paragraph>
              Your intake form has been successfully submitted. Case ID: {intakeId}
            </Typography>
          </Box>

          <Alert severity="info" sx={{ mb: 4 }}>
            Please check your email for confirmation and additional instructions.
          </Alert>

          <Box sx={{ mb: 4 }}>
            <Stepper activeStep={0} alternativeLabel>
              {steps.map((label) => (
                <Step key={label}>
                  <StepLabel>{label}</StepLabel>
                </Step>
              ))}
            </Stepper>
          </Box>

          <Grid container spacing={3}>
            <Grid item xs={12} md={6}>
              <Card>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    <AssignmentIcon sx={{ verticalAlign: 'middle', mr: 1 }} />
                    Required Documents
                  </Typography>
                  <Divider sx={{ my: 2 }} />
                  <List dense>
                    {requiredDocuments.map((doc, index) => (
                      <ListItem key={index}>
                        <ListItemIcon>
                          <ArticleIcon color="primary" />
                        </ListItemIcon>
                        <ListItemText primary={doc} />
                      </ListItem>
                    ))}
                  </List>
                  <Button
                    variant="contained"
                    fullWidth
                    onClick={() => navigate('/documents')}
                    startIcon={<UploadFileIcon />}
                    sx={{ mt: 2 }}
                  >
                    Upload Documents
                  </Button>
                </CardContent>
              </Card>
            </Grid>

            <Grid item xs={12} md={6}>
              <Card>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    Next Steps
                  </Typography>
                  <Divider sx={{ my: 2 }} />
                  <List>
                    {nextSteps.map((step, index) => (
                      <ListItem
                        key={index}
                        button
                        onClick={step.action}
                        sx={{
                          mb: 1,
                          bgcolor: step.urgent ? 'action.hover' : 'transparent',
                          borderRadius: 1,
                        }}
                      >
                        <ListItemIcon>{step.icon}</ListItemIcon>
                        <ListItemText
                          primary={step.title}
                          secondary={step.description}
                        />
                      </ListItem>
                    ))}
                  </List>
                </CardContent>
              </Card>
            </Grid>
          </Grid>

          <Box sx={{ mt: 4, display: 'flex', justifyContent: 'space-between' }}>
            <Button
              variant="outlined"
              onClick={() => navigate('/home')}
              sx={{ mr: 1 }}
            >
              Return to Home
            </Button>
            <Button
              variant="contained"
              onClick={() => navigate('/documents')}
              endIcon={<UploadFileIcon />}
            >
              Continue to Document Upload
            </Button>
          </Box>
        </Paper>
      </Box>
    </Container>
  );
} 