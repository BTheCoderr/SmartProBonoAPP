import React from 'react';
import {
  Box,
  Grid,
  Card,
  CardContent,
  Typography,
  Button,
  Paper,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Chip,
  Container,
} from '@mui/material';
import PageLayout from '../components/PageLayout';
import GavelIcon from '@mui/icons-material/Gavel';
import DescriptionIcon from '@mui/icons-material/Description';
import SupportAgentIcon from '@mui/icons-material/SupportAgent';
import SchoolIcon from '@mui/icons-material/School';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import TranslateIcon from '@mui/icons-material/Translate';
import AccountBalanceIcon from '@mui/icons-material/AccountBalance';
import HandshakeIcon from '@mui/icons-material/Handshake';
import { useNavigate } from 'react-router-dom';

const services = [
  {
    title: 'Legal Consultation',
    icon: <GavelIcon sx={{ fontSize: 40, color: '#1976d2' }} />,
    description: 'Professional legal advice and consultation services.',
    features: ['One-on-one consultation', 'Case evaluation', 'Legal strategy planning'],
    color: '#1976d2',
    path: '/legal-chat',
  },
  {
    title: 'Document Review',
    icon: <DescriptionIcon sx={{ fontSize: 40, color: '#2e7d32' }} />,
    description: 'Expert review of legal documents and contracts.',
    features: ['Contract analysis', 'Document verification', 'Legal compliance check'],
    color: '#2e7d32',
    path: '/contracts',
  },
  {
    title: 'Legal Representation',
    icon: <AccountBalanceIcon sx={{ fontSize: 40, color: '#ed6c02' }} />,
    description: 'Professional representation for your legal matters.',
    features: ['Court representation', 'Case management', 'Legal advocacy'],
    color: '#ed6c02',
    path: '/legal-chat',
  },
  {
    title: 'Educational Resources',
    icon: <SchoolIcon sx={{ fontSize: 40, color: '#9c27b0' }} />,
    description: 'Learn about your legal rights and responsibilities.',
    features: ['Legal guides', 'Educational materials', 'Rights information'],
    color: '#9c27b0',
    path: '/resources',
  },
  {
    title: 'Translation Services',
    icon: <TranslateIcon sx={{ fontSize: 40, color: '#0288d1' }} />,
    description: 'Legal document translation and interpretation.',
    features: ['Document translation', 'Live interpretation', 'Multi-language support'],
    color: '#0288d1',
    path: '/legal-chat',
  },
  {
    title: 'Support Services',
    icon: <SupportAgentIcon sx={{ fontSize: 40, color: '#7b1fa2' }} />,
    description: 'Ongoing support throughout your legal journey.',
    features: ['24/7 assistance', 'Case tracking', 'Status updates'],
    color: '#7b1fa2',
    path: '/legal-chat',
  },
];

function Services() {
  const navigate = useNavigate();

  return (
    <PageLayout
      title="Our Services"
      description="Comprehensive legal services to support your needs"
    >
      {/* Services Grid */}
      <Grid container spacing={4} sx={{ mb: 8 }}>
        {services.map((service, index) => (
          <Grid item xs={12} sm={6} md={4} key={index}>
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
                  {service.features.map((feature, i) => (
                    <Chip
                      key={i}
                      label={feature}
                      size="small"
                      icon={<CheckCircleIcon />}
                      sx={{ bgcolor: `${service.color}15` }}
                    />
                  ))}
                </Box>
              </CardContent>
              <Box sx={{ p: 2, pt: 0 }}>
                <Button
                  variant="outlined"
                  fullWidth
                  onClick={() => navigate(service.path)}
                  sx={{
                    borderColor: service.color,
                    color: service.color,
                    '&:hover': {
                      borderColor: service.color,
                      bgcolor: `${service.color}08`,
                    },
                  }}
                >
                  Learn More
                </Button>
              </Box>
            </Card>
          </Grid>
        ))}
      </Grid>

      {/* Pro Bono Commitment */}
      <Paper sx={{ p: 4, mb: 4, bgcolor: 'primary.main', color: 'white' }}>
        <Grid container spacing={4} alignItems="center">
          <Grid item xs={12} md={8}>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 2 }}>
              <HandshakeIcon sx={{ fontSize: 40 }} />
              <Typography variant="h5">Our Pro Bono Commitment</Typography>
            </Box>
            <Typography paragraph>
              We believe everyone deserves access to quality legal services. Our pro bono program
              provides free legal assistance to those who need it most.
            </Typography>
            <List>
              <ListItem>
                <ListItemIcon>
                  <CheckCircleIcon sx={{ color: 'white' }} />
                </ListItemIcon>
                <ListItemText primary="Free legal consultations for qualifying individuals" />
              </ListItem>
              <ListItem>
                <ListItemIcon>
                  <CheckCircleIcon sx={{ color: 'white' }} />
                </ListItemIcon>
                <ListItemText primary="Document preparation assistance" />
              </ListItem>
              <ListItem>
                <ListItemIcon>
                  <CheckCircleIcon sx={{ color: 'white' }} />
                </ListItemIcon>
                <ListItemText primary="Access to legal resources and education" />
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
              Get Started Now
            </Button>
          </Grid>
        </Grid>
      </Paper>
    </PageLayout>
  );
}

export default Services;
