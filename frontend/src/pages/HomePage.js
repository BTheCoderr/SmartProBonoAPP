import React, { useState, useEffect } from 'react';
import {
  Box,
  Container,
  Typography,
  Button,
  Grid,
  Card,
  CardContent,
  CardActions,
  Paper,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Chip,
} from '@mui/material';
import { useNavigate } from 'react-router-dom';
import ChatIcon from '@mui/icons-material/Chat';
import DescriptionIcon from '@mui/icons-material/Description';
import GavelIcon from '@mui/icons-material/Gavel';
import FlightIcon from '@mui/icons-material/Flight';
import BuildIcon from '@mui/icons-material/Build';
import ListAltIcon from '@mui/icons-material/ListAlt';
import ArrowForwardIcon from '@mui/icons-material/ArrowForward';
import LockIcon from '@mui/icons-material/Lock';
import BalanceIcon from '@mui/icons-material/Balance';

function HomePage() {
  const navigate = useNavigate();
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  // Check authentication status when component mounts
  useEffect(() => {
    const authToken = localStorage.getItem('authToken');
    setIsAuthenticated(!!authToken);
  }, []);

  // All features - some require auth
  const features = [
    {
      title: 'Legal Documents',
      description: 'Generate and review legal documents with AI assistance',
      icon: <DescriptionIcon sx={{ fontSize: 40, color: '#1976d2' }} />,
      path: '/document-templates',
      requiresAuth: true,
    },
    {
      title: 'Know Your Rights',
      description: 'Get instant information about your legal rights and protections',
      icon: <GavelIcon sx={{ fontSize: 40, color: '#1976d2' }} />,
      path: '/resources/rights',
      requiresAuth: false,
    },
    {
      title: 'Immigration Help',
      description: 'Support for visa applications and immigration processes',
      icon: <FlightIcon sx={{ fontSize: 40, color: '#1976d2' }} />,
      path: '/services/immigration',
      requiresAuth: false,
    },
    {
      title: 'Pro Bono Services',
      description: 'Connect with legal professionals offering free services',
      icon: <BuildIcon sx={{ fontSize: 40, color: '#1976d2' }} />,
      path: '/services',
      requiresAuth: false,
    },
    {
      title: 'Resources',
      description: 'Access helpful legal resources and guides',
      icon: <ListAltIcon sx={{ fontSize: 40, color: '#1976d2' }} />,
      path: '/resources',
      requiresAuth: false,
    },
    {
      title: 'AI Legal Assistant',
      description: 'Get instant answers to your legal questions 24/7',
      icon: <ChatIcon sx={{ fontSize: 40, color: '#1976d2' }} />,
      path: '/legal-chat',
      requiresAuth: true,
    },
  ];

  // Helper function to handle navigation with auth redirection
  const handleFeatureClick = feature => {
    if (feature.requiresAuth && !isAuthenticated) {
      navigate('/login', { state: { from: feature.path } });
    } else {
      navigate(feature.path);
    }
  };

  return (
    <Box sx={{ minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>
      {/* Hero Section with Blue Pattern Background */}
      <Box
        sx={{
          background: 'linear-gradient(45deg, #1976d2 30%, #2196f3 90%)',
          position: 'relative',
          color: 'white',
          pt: 8,
          pb: 8,
          overflow: 'hidden',
        }}
      >
        {/* Background Pattern */}
        <Box
          sx={{
            position: 'absolute',
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            opacity: 0.1,
            backgroundImage: `repeating-linear-gradient(45deg, #ffffff 0, #ffffff 1px, transparent 1px, transparent 50%)`,
            backgroundSize: '20px 20px',
          }}
        />

        <Container maxWidth="lg" sx={{ position: 'relative' }}>
          <Grid container spacing={4} alignItems="center">
            <Grid item xs={12} md={7}>
              <Typography
                variant="h1"
                sx={{
                  fontSize: { xs: '2.5rem', md: '3.5rem' },
                  fontWeight: 'bold',
                  mb: 3,
                }}
              >
                Free Legal Help Made Simple
              </Typography>
              <Typography
                variant="h5"
                sx={{ mb: 4, opacity: 0.9 }}
              >
                Get instant legal assistance, document generation, and professional guidance - all in one place.
              </Typography>
              <Box sx={{ display: 'flex', gap: 2 }}>
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
                  startIcon={<ChatIcon />}
                >
                  START LEGAL CHAT
                </Button>
                <Button
                  variant="outlined"
                  size="large"
                  sx={{
                    color: 'white',
                    borderColor: 'white',
                    '&:hover': {
                      borderColor: 'rgba(255, 255, 255, 0.9)',
                      bgcolor: 'rgba(255, 255, 255, 0.1)',
                    },
                  }}
                  startIcon={<BalanceIcon />}
                >
                  BROWSE SERVICES
                </Button>
              </Box>
            </Grid>
            <Grid item xs={12} md={5}>
              <Paper
                elevation={6}
                sx={{
                  p: 3,
                  bgcolor: 'rgba(255, 255, 255, 0.95)',
                  borderRadius: 2,
                }}
              >
                <Typography
                  variant="h6"
                  color="primary"
                  gutterBottom
                  sx={{ fontWeight: 600 }}
                >
                  Why Choose Us?
                </Typography>
                <List>
                  <ListItem>
                    <ListItemIcon>
                      <ChatIcon color="primary" />
                    </ListItemIcon>
                    <ListItemText primary="24/7 AI-powered legal assistance" />
                  </ListItem>
                  <ListItem>
                    <ListItemIcon>
                      <DescriptionIcon color="primary" />
                    </ListItemIcon>
                    <ListItemText primary="Free document generation" />
                  </ListItem>
                  <ListItem>
                    <ListItemIcon>
                      <GavelIcon color="primary" />
                    </ListItemIcon>
                    <ListItemText primary="Expert legal guidance" />
                  </ListItem>
                  <ListItem>
                    <ListItemIcon>
                      <LockIcon color="primary" />
                    </ListItemIcon>
                    <ListItemText primary="Secure & confidential" />
                  </ListItem>
                </List>
              </Paper>
            </Grid>
          </Grid>
        </Container>
      </Box>

      {/* Services Section */}
      <Container maxWidth="lg" sx={{ py: 8 }}>
        <Typography variant="h3" component="h2" align="center" gutterBottom>
          Our Services
        </Typography>
        <Typography variant="h6" align="center" color="text.secondary" sx={{ mb: 6 }}>
          Everything you need for legal assistance in one place
        </Typography>

        <Grid container spacing={4}>
          {features.map((feature, index) => (
            <Grid item xs={12} sm={6} md={4} key={index}>
              <Card
                sx={{
                  height: '100%',
                  display: 'flex',
                  flexDirection: 'column',
                  transition: 'transform 0.2s',
                  '&:hover': {
                    transform: 'translateY(-4px)',
                  },
                }}
                onClick={() => handleFeatureClick(feature)}
              >
                <CardContent sx={{ flexGrow: 1 }}>
                  <Box
                    sx={{
                      display: 'flex',
                      flexDirection: 'column',
                      alignItems: 'center',
                      textAlign: 'center',
                      mb: 2,
                    }}
                  >
                    {feature.icon}
                    <Typography variant="h6" component="h3" sx={{ mt: 2 }}>
                      {feature.title}
                    </Typography>
                  </Box>
                  <Typography variant="body1" color="text.secondary" align="center">
                    {feature.description}
                  </Typography>
                </CardContent>
                <CardActions sx={{ justifyContent: 'center', pb: 2 }}>
                  <Button
                    variant="outlined"
                    color="primary"
                    endIcon={<ArrowForwardIcon />}
                  >
                    Learn More
                  </Button>
                  {feature.requiresAuth && !isAuthenticated && (
                    <Chip
                      label="Login Required"
                      size="small"
                      color="primary"
                      variant="outlined"
                      sx={{ ml: 1 }}
                    />
                  )}
                </CardActions>
              </Card>
            </Grid>
          ))}
        </Grid>

        {/* Need Legal Assistance Section */}
        <Box sx={{ mt: 8, mb: 8, textAlign: 'center' }}>
          <Typography variant="h3" component="h2" gutterBottom>
            Need Legal Assistance?
          </Typography>
          <Typography variant="h6" color="text.secondary" paragraph>
            Our AI-powered legal assistant is available 24/7 to help you with your legal questions.
          </Typography>
          <Button
            variant="contained"
            size="large"
            onClick={() => handleFeatureClick(features.find(f => f.title === 'AI Legal Assistant'))}
            sx={{ mt: 2 }}
          >
            Get Started Now
          </Button>
        </Box>

        {/* Additional Resources Section */}
        <Box sx={{ mt: 8, mb: 8 }}>
          <Typography variant="h4" component="h2" gutterBottom align="center">
            Additional Resources
          </Typography>
          <Grid container spacing={4} sx={{ mt: 2 }}>
            <Grid item xs={12} md={4}>
              <Card sx={{ height: '100%' }}>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    Emergency Support
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Get immediate assistance for urgent legal matters
                  </Typography>
                  <Button
                    variant="outlined"
                    color="error"
                    sx={{ mt: 2 }}
                    onClick={() => navigate('/emergency-support')}
                  >
                    Get Help Now
                  </Button>
                </CardContent>
              </Card>
            </Grid>
            <Grid item xs={12} md={4}>
              <Card sx={{ height: '100%' }}>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    Legal Education
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Access free legal education resources and guides
                  </Typography>
                  <Button
                    variant="outlined"
                    sx={{ mt: 2 }}
                    onClick={() => navigate('/resources/education')}
                  >
                    Start Learning
                  </Button>
                </CardContent>
              </Card>
            </Grid>
            <Grid item xs={12} md={4}>
              <Card sx={{ height: '100%' }}>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    Find a Lawyer
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Connect with pro bono lawyers in your area
                  </Typography>
                  <Button
                    variant="outlined"
                    sx={{ mt: 2 }}
                    onClick={() => navigate('/find-lawyer')}
                  >
                    Find Now
                  </Button>
                </CardContent>
              </Card>
            </Grid>
          </Grid>
        </Box>
      </Container>

      {/* Footer CTA */}
      <Box
        sx={{
          bgcolor: 'primary.main',
          color: 'white',
          py: 6,
          mt: 'auto',
        }}
      >
        <Container maxWidth="lg">
          <Typography variant="h4" align="center" gutterBottom>
            Ready to Get Started?
          </Typography>
          <Typography variant="h6" align="center" paragraph>
            Join thousands of people getting free legal assistance
          </Typography>
          <Box sx={{ display: 'flex', justifyContent: 'center', gap: 2 }}>
            <Button
              variant="contained"
              size="large"
              color="secondary"
              onClick={() => navigate('/register')}
            >
              Create Free Account
            </Button>
            <Button
              variant="outlined"
              size="large"
              sx={{ color: 'white', borderColor: 'white' }}
              onClick={() => navigate('/about')}
            >
              Learn More
            </Button>
          </Box>
        </Container>
      </Box>
    </Box>
  );
}

export default HomePage;
