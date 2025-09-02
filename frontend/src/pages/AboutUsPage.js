import React from 'react';
import {
  Container,
  Typography,
  Box,
  Grid,
  Card,
  CardContent,
  Avatar,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Chip
} from '@mui/material';
import {
  Gavel as GavelIcon,
  Security as SecurityIcon,
  Public as PublicIcon,
  School as SchoolIcon,
  CheckCircle as CheckCircleIcon
} from '@mui/icons-material';
import PageLayout from '../components/PageLayout';

const AboutUsPage = () => {
  const teamMembers = [
    {
      name: 'Legal Team',
      role: 'Legal Experts',
      description: 'Experienced attorneys and legal professionals',
      avatar: <GavelIcon />
    },
    {
      name: 'Tech Team',
      role: 'Technology Experts',
      description: 'AI and software development specialists',
      avatar: <SecurityIcon />
    },
    {
      name: 'Support Team',
      role: 'User Support',
      description: 'Dedicated to helping users succeed',
      avatar: <PublicIcon />
    }
  ];

  const values = [
    {
      title: 'Accessibility',
      description: 'Making legal help available to everyone, regardless of financial situation',
      icon: <PublicIcon />
    },
    {
      title: 'Innovation',
      description: 'Using cutting-edge AI technology to improve legal services',
      icon: <SchoolIcon />
    },
    {
      title: 'Integrity',
      description: 'Maintaining the highest standards of legal and ethical practice',
      icon: <SecurityIcon />
    },
    {
      title: 'Empowerment',
      description: 'Giving people the tools and knowledge to understand their rights',
      icon: <GavelIcon />
    }
  ];

  return (
    <PageLayout>
      <Container maxWidth="lg" sx={{ py: 4 }}>
        {/* Hero Section */}
        <Box sx={{ textAlign: 'center', mb: 6 }}>
          <Typography variant="h2" component="h1" gutterBottom sx={{ fontWeight: 'bold' }}>
            About SmartProBono
          </Typography>
          <Typography variant="h5" color="text.secondary" sx={{ mb: 3 }}>
            Making legal help accessible, affordable, and easy to understand for everyone
          </Typography>
        </Box>

        {/* Mission Statement */}
        <Box sx={{ mb: 6, textAlign: 'center' }}>
          <Typography variant="h4" gutterBottom>
            Our Mission
          </Typography>
          <Typography variant="h6" color="text.secondary" sx={{ maxWidth: 800, mx: 'auto' }}>
            We believe that everyone deserves access to quality legal assistance, regardless of their financial situation. 
            SmartProBono combines the power of artificial intelligence with legal expertise to provide free, 
            accessible legal tools and resources to help people understand and protect their rights.
          </Typography>
        </Box>

        {/* Values */}
        <Box sx={{ mb: 6 }}>
          <Typography variant="h4" gutterBottom sx={{ textAlign: 'center', mb: 4 }}>
            Our Values
          </Typography>
          <Grid container spacing={3}>
            {values.map((value, index) => (
              <Grid item xs={12} md={6} key={index}>
                <Card sx={{ height: '100%', p: 2 }}>
                  <CardContent>
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 2 }}>
                      {value.icon}
                      <Typography variant="h6" sx={{ fontWeight: 'bold' }}>
                        {value.title}
                      </Typography>
                    </Box>
                    <Typography variant="body2" color="text.secondary">
                      {value.description}
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
            ))}
          </Grid>
        </Box>

        {/* What We Do */}
        <Box sx={{ mb: 6 }}>
          <Typography variant="h4" gutterBottom sx={{ textAlign: 'center', mb: 4 }}>
            What We Do
          </Typography>
          <Grid container spacing={3}>
            <Grid item xs={12} md={4}>
              <Card sx={{ height: '100%', textAlign: 'center', p: 2 }}>
                <CardContent>
                  <GavelIcon sx={{ fontSize: 48, color: 'primary.main', mb: 2 }} />
                  <Typography variant="h6" gutterBottom>
                    Document Generation
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Create professional legal documents using AI-powered templates and guidance
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
            <Grid item xs={12} md={4}>
              <Card sx={{ height: '100%', textAlign: 'center', p: 2 }}>
                <CardContent>
                  <SecurityIcon sx={{ fontSize: 48, color: 'success.main', mb: 2 }} />
                  <Typography variant="h6" gutterBottom>
                    Document Analysis
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Scan and analyze existing documents for legal issues and improvements
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
            <Grid item xs={12} md={4}>
              <Card sx={{ height: '100%', textAlign: 'center', p: 2 }}>
                <CardContent>
                  <PublicIcon sx={{ fontSize: 48, color: 'info.main', mb: 2 }} />
                  <Typography variant="h6" gutterBottom>
                    Legal Education
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Provide resources and guidance to help people understand their legal rights
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
          </Grid>
        </Box>

        {/* Team */}
        <Box sx={{ mb: 6 }}>
          <Typography variant="h4" gutterBottom sx={{ textAlign: 'center', mb: 4 }}>
            Our Team
          </Typography>
          <Grid container spacing={3}>
            {teamMembers.map((member, index) => (
              <Grid item xs={12} md={4} key={index}>
                <Card sx={{ height: '100%', textAlign: 'center', p: 2 }}>
                  <CardContent>
                    <Avatar sx={{ width: 80, height: 80, mx: 'auto', mb: 2, bgcolor: 'primary.main' }}>
                      {member.avatar}
                    </Avatar>
                    <Typography variant="h6" gutterBottom>
                      {member.name}
                    </Typography>
                    <Typography variant="subtitle1" color="primary" gutterBottom>
                      {member.role}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      {member.description}
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
            ))}
          </Grid>
        </Box>

        {/* Impact */}
        <Box sx={{ mb: 6, textAlign: 'center' }}>
          <Typography variant="h4" gutterBottom>
            Our Impact
          </Typography>
          <Grid container spacing={3} sx={{ mt: 2 }}>
            <Grid item xs={12} sm={4}>
              <Typography variant="h3" color="primary" sx={{ fontWeight: 'bold' }}>
                10K+
              </Typography>
              <Typography variant="h6" gutterBottom>
                Users Helped
              </Typography>
              <Typography variant="body2" color="text.secondary">
                People who have used our services to access legal help
              </Typography>
            </Grid>
            <Grid item xs={12} sm={4}>
              <Typography variant="h3" color="success.main" sx={{ fontWeight: 'bold' }}>
                50K+
              </Typography>
              <Typography variant="h6" gutterBottom>
                Documents Generated
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Legal documents created using our platform
              </Typography>
            </Grid>
            <Grid item xs={12} sm={4}>
              <Typography variant="h3" color="info.main" sx={{ fontWeight: 'bold' }}>
                95%
              </Typography>
              <Typography variant="h6" gutterBottom>
                Success Rate
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Users who successfully resolve their legal issues
              </Typography>
            </Grid>
          </Grid>
        </Box>

        {/* Contact */}
        <Box sx={{ textAlign: 'center', bgcolor: 'grey.50', p: 4, borderRadius: 2 }}>
          <Typography variant="h4" gutterBottom>
            Get in Touch
          </Typography>
          <Typography variant="body1" color="text.secondary" sx={{ mb: 3 }}>
            Have questions about our services or want to learn more? We'd love to hear from you.
          </Typography>
          <List sx={{ maxWidth: 400, mx: 'auto' }}>
            <ListItem>
              <ListItemIcon>
                <CheckCircleIcon color="primary" />
              </ListItemIcon>
              <ListItemText 
                primary="Email: support@smartprobono.org"
                secondary="We respond within 24 hours"
              />
            </ListItem>
            <ListItem>
              <ListItemIcon>
                <CheckCircleIcon color="primary" />
              </ListItemIcon>
              <ListItemText 
                primary="Phone: (401) 217-9799"
                secondary="Monday - Friday, 9 AM - 5 PM EST"
              />
            </ListItem>
            <ListItem>
              <ListItemIcon>
                <CheckCircleIcon color="primary" />
              </ListItemIcon>
              <ListItemText 
                primary="Location: Providence, RI"
                secondary="Serving clients nationwide"
              />
            </ListItem>
          </List>
        </Box>
      </Container>
    </PageLayout>
  );
};

export default AboutUsPage;
