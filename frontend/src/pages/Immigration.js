import React, { useState } from 'react';
import {
  Box,
  Stepper,
  Step,
  StepLabel,
  Button,
  Typography,
  Grid,
  Card,
  CardContent,
  CardActions,
  Chip,
  Paper,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Divider,
} from '@mui/material';
import PageLayout from '../components/PageLayout';
import DescriptionIcon from '@mui/icons-material/Description';
import GroupsIcon from '@mui/icons-material/Groups';
import SchoolIcon from '@mui/icons-material/School';
import WorkIcon from '@mui/icons-material/Work';
import FamilyRestroomIcon from '@mui/icons-material/FamilyRestroom';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import ArticleIcon from '@mui/icons-material/Article';
import AssignmentIcon from '@mui/icons-material/Assignment';
import SendIcon from '@mui/icons-material/Send';
import { useNavigate } from 'react-router-dom';
const services = [
  {
    title: 'Family-Based Immigration',
    icon: <FamilyRestroomIcon sx={{ fontSize: 40, color: '#1976d2' }} />,
    description: 'Reunite with your family members through proper immigration channels',
    documents: [
      'Birth certificates',
      'Marriage certificates',
      'Proof of citizenship',
      'Financial documents',
    ],
    color: '#1976d2',
  },
  {
    title: 'Student Visas',
    icon: <SchoolIcon sx={{ fontSize: 40, color: '#2e7d32' }} />,
    description: 'Pursue your education in the United States',
    documents: ['Acceptance letter', 'Financial proof', 'Academic records', 'Passport'],
    color: '#2e7d32',
  },
  {
    title: 'Work Visas',
    icon: <WorkIcon sx={{ fontSize: 40, color: '#ed6c02' }} />,
    description: 'Employment-based immigration assistance',
    documents: ['Job offer letter', 'Educational credentials', 'Work experience letters', 'Resume'],
    color: '#ed6c02',
  },
  {
    title: 'Citizenship',
    icon: <GroupsIcon sx={{ fontSize: 40, color: '#9c27b0' }} />,
    description: 'Guide through the naturalization process',
    documents: ['Green card', 'Tax returns', 'Residency proof', 'Civil documents'],
    color: '#9c27b0',
  },
];
const steps = [
  {
    label: 'Initial Consultation',
    description: 'Free consultation to understand your case and eligibility',
    icon: <ArticleIcon />,
  },
  {
    label: 'Document Collection',
    description: 'Gather and organize required documentation',
    icon: <DescriptionIcon />,
  },
  {
    label: 'Application Process',
    description: 'Complete and review all necessary forms',
    icon: <AssignmentIcon />,
  },
  {
    label: 'Review & Submit',
    description: 'Final review and submission of your application',
    icon: <SendIcon />,
  },
];
function Immigration() {
  const [activeStep, setActiveStep] = useState(0);
  const navigate = useNavigate();
  const handleNext = () => {
    setActiveStep(prevStep => prevStep + 1);
  };
  const handleBack = () => {
    setActiveStep(prevStep => prevStep - 1);
  };
  return (
    <PageLayout
      title="Immigration Legal Services"
      description="Free assistance with visa applications, citizenship, and other immigration matters"
    >
      {/* Services Grid */}
      <Grid container spacing={4} sx={{ mb: 8 }}>
        {services.map((service, index) => (
          <Grid item xs={12} sm={6} md={3} key={index}>
            <Card
              sx={{
                height: '100%',
                display: 'flex',
                flexDirection: 'column',
                transition: 'transform 0.2s',
                '&:hover': {
                  transform: 'translateY(-4px)',
                  boxShadow: 4,
                },
              }}
            >
              <CardContent sx={{ flexGrow: 1 }}>
                <Box
                  sx={{
                    display: 'flex',
                    alignItems: 'center',
                    mb: 2,
                    gap: 1,
                  }}
                >
                  {service.icon}
                  <Typography variant="h6" component="div">
                    {service.title}
                  </Typography>
                </Box>
                <Typography color="text.secondary" paragraph>
                  {service.description}
                </Typography>
                <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                  {service.documents.map((doc, i) => (
                    <Chip
                      key={i}
                      label={doc}
                      size="small"
                      icon={<CheckCircleIcon />}
                      sx={{ bgcolor: `${service.color}15` }}
                    />
                  ))}
                </Box>
              </CardContent>
              <CardActions sx={{ p: 2, pt: 0 }}>
                <Button
                  variant="outlined"
                  fullWidth
                  onClick={() => navigate('/legal-chat')}
                  sx={{ borderColor: service.color, color: service.color }}
                >
                  Get Help
                </Button>
              </CardActions>
            </Card>
          </Grid>
        ))}
      </Grid>
      {/* Process Section */}
      <Paper sx={{ p: 4, mb: 4 }}>
        <Typography variant="h5" gutterBottom>
          Our Process
        </Typography>
        <Stepper activeStep={activeStep} alternativeLabel sx={{ mb: 4 }}>
          {steps.map((step, index) => (
            <Step key={index}>
              <StepLabel
                StepIconComponent={() => (
                  <Box
                    sx={{
                      width: 40,
                      height: 40,
                      borderRadius: '50%',
                      bgcolor: activeStep >= index ? 'primary.main' : 'grey.300',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      color: 'white',
                    }}
                  >
                    {step.icon}
                  </Box>
                )}
              >
                <Typography variant="subtitle2" sx={{ fontWeight: 600 }}>
                  {step.label}
                </Typography>
                <Typography variant="caption" color="text.secondary">
                  {step.description}
                </Typography>
              </StepLabel>
            </Step>
          ))}
        </Stepper>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', pt: 2 }}>
          <Button variant="outlined" disabled={activeStep === 0} onClick={handleBack}>
            Back
          </Button>
          <Button
            variant="contained"
            onClick={activeStep === steps.length - 1 ? () => navigate('/legal-chat') : handleNext}
          >
            {activeStep === steps.length - 1 ? 'Start Application' : 'Next'}
          </Button>
        </Box>
      </Paper>
      {/* Free Services Highlight */}
      <Paper sx={{ p: 4, bgcolor: 'primary.main', color: 'white' }}>
        <Grid container spacing={4} alignItems="center">
          <Grid item xs={12} md={8}>
            <Typography variant="h5" gutterBottom>
              Need Help With Immigration Paperwork?
            </Typography>
            <Typography paragraph>
              We provide free assistance with document preparation, form filing, and legal guidance
              for immigration matters. Our team of volunteers and legal professionals is here to
              help you navigate the immigration process.
            </Typography>
            <List>
              <ListItem>
                <ListItemIcon>
                  <CheckCircleIcon sx={{ color: 'white' }} />
                </ListItemIcon>
                <ListItemText primary="Free document review and preparation" />
              </ListItem>
              <ListItem>
                <ListItemIcon>
                  <CheckCircleIcon sx={{ color: 'white' }} />
                </ListItemIcon>
                <ListItemText primary="Assistance with form filing" />
              </ListItem>
              <ListItem>
                <ListItemIcon>
                  <CheckCircleIcon sx={{ color: 'white' }} />
                </ListItemIcon>
                <ListItemText primary="Legal guidance and consultation" />
              </ListItem>
            </List>
          </Grid>
          <Grid item xs={12} md={4} sx={{ textAlign: 'center' }}>
            <Button
              variant="contained"
              size="large"
              onClick={() => navigate('/legal-chat')}
              sx={{
                bgcolor: 'white',
                color: 'primary.main',
                '&:hover': {
                  bgcolor: 'rgba(255, 255, 255, 0.9)',
                },
              }}
            >
              Start Free Consultation
            </Button>
          </Grid>
        </Grid>
      </Paper>
    </PageLayout>
  );
}
export default Immigration;