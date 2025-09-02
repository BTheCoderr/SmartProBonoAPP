import React, { useState } from 'react';
import {
  Container,
  Typography,
  Box,
  Grid,
  Card,
  CardContent,
  CardHeader,
  Button,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Chip,
  Alert,
  Paper,
  Divider
} from '@mui/material';
import {
  ExpandMore as ExpandMoreIcon,
  Gavel as GavelIcon,
  Security as SecurityIcon,
  Work as WorkIcon,
  Home as HomeIcon,
  School as SchoolIcon,
  HealthAndSafety as HealthAndSafetyIcon,
  FamilyRestroom as FamilyRestroomIcon,
  DirectionsCar as DirectionsCarIcon,
  Receipt as ReceiptIcon,
  Public as PublicIcon,
  AccountBalance as AccountBalanceIcon
} from '@mui/icons-material';
import PageLayout from '../components/PageLayout';

const KnowYourRightsPage = () => {
  const [expandedCategory, setExpandedCategory] = useState('employment');

  const handleCategoryChange = (category) => {
    setExpandedCategory(expandedCategory === category ? false : category);
  };

  const rightsCategories = [
    {
      id: 'employment',
      title: 'Employment Rights',
      icon: <WorkIcon />,
      color: 'primary',
      rights: [
        {
          title: 'Minimum Wage Rights',
          description: 'You have the right to receive at least the federal or state minimum wage, whichever is higher.',
          details: [
            'Federal minimum wage is currently $7.25 per hour',
            'Many states have higher minimum wages',
            'Tipped employees have different minimum wage rules',
            'You must be paid for all hours worked'
          ]
        },
        {
          title: 'Overtime Pay',
          description: 'Most employees are entitled to overtime pay for hours worked over 40 in a week.',
          details: [
            'Overtime rate is typically 1.5 times your regular rate',
            'Some employees are exempt from overtime rules',
            'Independent contractors are not entitled to overtime',
            'State laws may provide additional protections'
          ]
        },
        {
          title: 'Workplace Safety',
          description: 'You have the right to a safe workplace free from recognized hazards.',
          details: [
            'OSHA protects most private sector workers',
            'You can report safety violations anonymously',
            'You cannot be fired for reporting safety issues',
            'Employers must provide safety training'
          ]
        },
        {
          title: 'Anti-Discrimination',
          description: 'You cannot be discriminated against based on protected characteristics.',
          details: [
            'Protected classes include race, color, religion, sex, national origin, age, disability',
            'Harassment based on protected characteristics is illegal',
            'You can file complaints with the EEOC',
            'Retaliation for reporting discrimination is illegal'
          ]
        }
      ]
    },
    {
      id: 'housing',
      title: 'Housing Rights',
      icon: <HomeIcon />,
      color: 'secondary',
      rights: [
        {
          title: 'Fair Housing Rights',
          description: 'You cannot be discriminated against when renting or buying housing.',
          details: [
            'Protected classes include race, color, religion, sex, national origin, familial status, disability',
            'Landlords cannot refuse to rent based on protected characteristics',
            'You can file complaints with HUD',
            'Reasonable accommodations must be provided for disabilities'
          ]
        },
        {
          title: 'Tenant Rights',
          description: 'As a tenant, you have specific rights regarding your rental property.',
          details: [
            'Right to habitable living conditions',
            'Right to privacy and notice before entry',
            'Right to security deposit return',
            'Protection against illegal eviction'
          ]
        }
      ]
    },
    {
      id: 'education',
      title: 'Education Rights',
      icon: <SchoolIcon />,
      color: 'success',
      rights: [
        {
          title: 'Equal Access to Education',
          description: 'All students have the right to equal access to educational opportunities.',
          details: [
            'Public schools must provide free education',
            'Students with disabilities have right to accommodations',
            'English Language Learners have right to language support',
            'Schools cannot discriminate based on protected characteristics'
          ]
        }
      ]
    },
    {
      id: 'healthcare',
      title: 'Healthcare Rights',
      icon: <HealthAndSafetyIcon />,
      color: 'error',
      rights: [
        {
          title: 'Patient Rights',
          description: 'You have specific rights as a patient receiving medical care.',
          details: [
            'Right to informed consent',
            'Right to privacy and confidentiality (HIPAA)',
            'Right to access your medical records',
            'Right to refuse treatment'
          ]
        }
      ]
    },
    {
      id: 'family',
      title: 'Family Rights',
      icon: <FamilyRestroomIcon />,
      color: 'warning',
      rights: [
        {
          title: 'Parental Rights',
          description: 'Parents have fundamental rights regarding their children.',
          details: [
            'Right to make decisions about child\'s education',
            'Right to make medical decisions for children',
            'Right to custody and visitation',
            'Right to child support'
          ]
        }
      ]
    },
    {
      id: 'consumer',
      title: 'Consumer Rights',
      icon: <ReceiptIcon />,
      color: 'info',
      rights: [
        {
          title: 'Consumer Protection',
          description: 'You have rights as a consumer when purchasing goods and services.',
          details: [
            'Right to accurate product information',
            'Right to return defective products',
            'Protection against deceptive advertising',
            'Right to dispute credit report errors'
          ]
        }
      ]
    }
  ];

  const quickResources = [
    {
      title: 'File a Complaint',
      description: 'Report violations of your rights',
      action: 'Report Now',
      color: 'error'
    },
    {
      title: 'Find Legal Help',
      description: 'Connect with legal aid organizations',
      action: 'Find Help',
      color: 'primary'
    },
    {
      title: 'Emergency Resources',
      description: 'Get immediate assistance',
      action: 'Get Help',
      color: 'warning'
    }
  ];

  return (
    <PageLayout>
      <Container maxWidth="lg" sx={{ py: 4 }}>
        {/* Hero Section */}
        <Box sx={{ textAlign: 'center', mb: 6 }}>
          <Typography variant="h2" component="h1" gutterBottom sx={{ fontWeight: 'bold' }}>
            Know Your Rights
          </Typography>
          <Typography variant="h5" color="text.secondary" sx={{ mb: 3 }}>
            Understanding your legal rights and protections
          </Typography>
          <Alert severity="info" sx={{ maxWidth: 800, mx: 'auto' }}>
            <Typography variant="body2">
              <strong>Important:</strong> This information is for educational purposes only and does not constitute legal advice. 
              For specific legal questions, consult with a qualified attorney.
            </Typography>
          </Alert>
        </Box>

        {/* Quick Resources */}
        <Grid container spacing={3} sx={{ mb: 6 }}>
          {quickResources.map((resource, index) => (
            <Grid item xs={12} md={4} key={index}>
              <Card sx={{ height: '100%', textAlign: 'center' }}>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    {resource.title}
                  </Typography>
                  <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                    {resource.description}
                  </Typography>
                  <Button
                    variant="contained"
                    color={resource.color}
                    fullWidth
                  >
                    {resource.action}
                  </Button>
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>

        {/* Rights Categories */}
        <Box sx={{ mb: 4 }}>
          <Typography variant="h4" gutterBottom sx={{ textAlign: 'center', mb: 4 }}>
            Your Rights by Category
          </Typography>
          
          {rightsCategories.map((category) => (
            <Accordion
              key={category.id}
              expanded={expandedCategory === category.id}
              onChange={() => handleCategoryChange(category.id)}
              sx={{ mb: 2 }}
            >
              <AccordionSummary
                expandIcon={<ExpandMoreIcon />}
                sx={{ bgcolor: `${category.color}.light`, color: `${category.color}.contrastText` }}
              >
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                  {category.icon}
                  <Typography variant="h6" sx={{ fontWeight: 'bold' }}>
                    {category.title}
                  </Typography>
                </Box>
              </AccordionSummary>
              <AccordionDetails>
                <Grid container spacing={3}>
                  {category.rights.map((right, index) => (
                    <Grid item xs={12} md={6} key={index}>
                      <Card variant="outlined">
                        <CardHeader
                          title={right.title}
                          subheader={right.description}
                        />
                        <CardContent>
                          <Typography variant="body2" color="text.secondary" gutterBottom>
                            Key Points:
                          </Typography>
                          <List dense>
                            {right.details.map((detail, detailIndex) => (
                              <ListItem key={detailIndex} sx={{ py: 0.5 }}>
                                <ListItemIcon sx={{ minWidth: 32 }}>
                                  <GavelIcon fontSize="small" color="primary" />
                                </ListItemIcon>
                                <ListItemText
                                  primary={detail}
                                  primaryTypographyProps={{ variant: 'body2' }}
                                />
                              </ListItem>
                            ))}
                          </List>
                        </CardContent>
                      </Card>
                    </Grid>
                  ))}
                </Grid>
              </AccordionDetails>
            </Accordion>
          ))}
        </Box>

        {/* Important Legal Information */}
        <Paper sx={{ p: 4, bgcolor: 'grey.50' }}>
          <Typography variant="h5" gutterBottom sx={{ textAlign: 'center' }}>
            Important Legal Information
          </Typography>
          <Grid container spacing={3}>
            <Grid item xs={12} md={6}>
              <Box>
                <Typography variant="h6" gutterBottom color="error">
                  ⚠️ Legal Disclaimer
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  The information provided on this page is for educational purposes only and does not constitute legal advice. 
                  Laws vary by state and jurisdiction, and this information may not be current or applicable to your specific situation.
                </Typography>
              </Box>
            </Grid>
            <Grid item xs={12} md={6}>
              <Box>
                <Typography variant="h6" gutterBottom color="primary">
                  📞 When to Seek Legal Help
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  You should consult with a qualified attorney if you believe your rights have been violated, 
                  if you need to file a lawsuit, or if you have complex legal questions that require professional guidance.
                </Typography>
              </Box>
            </Grid>
          </Grid>
        </Paper>

        {/* Emergency Resources */}
        <Box sx={{ mt: 6, textAlign: 'center' }}>
          <Typography variant="h5" gutterBottom>
            Need Immediate Help?
          </Typography>
          <Typography variant="body1" color="text.secondary" sx={{ mb: 3 }}>
            If you're in immediate danger or facing an emergency legal situation
          </Typography>
          <Box sx={{ display: 'flex', gap: 2, justifyContent: 'center', flexWrap: 'wrap' }}>
            <Button variant="contained" color="error" size="large">
              Call 911 (Emergency)
            </Button>
            <Button variant="contained" color="primary" size="large">
              Legal Aid Hotline
            </Button>
            <Button variant="outlined" color="primary" size="large">
              Find Local Attorney
            </Button>
          </Box>
        </Box>
      </Container>
    </PageLayout>
  );
};

export default KnowYourRightsPage;
