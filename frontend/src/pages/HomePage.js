import React from 'react';
import { 
  Box, 
  Typography, 
  Paper, 
  Grid, 
  Button, 
  Container,
  Card,
  CardContent,
  CardActions,
  Divider,
  Chip,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Rating,
  Avatar
} from '@mui/material';
import { useNavigate } from 'react-router-dom';
import ChatIcon from '@mui/icons-material/Chat';
import GavelIcon from '@mui/icons-material/Gavel';
import DescriptionIcon from '@mui/icons-material/Description';
import ListAltIcon from '@mui/icons-material/ListAlt';
import FlightIcon from '@mui/icons-material/Flight';
import BuildIcon from '@mui/icons-material/Build';
import BalanceIcon from '@mui/icons-material/Balance';
import PersonIcon from '@mui/icons-material/Person';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import SecurityIcon from '@mui/icons-material/Security';
import VerifiedUserIcon from '@mui/icons-material/VerifiedUser';
import { useAuth } from '../context/AuthContext';

function HomePage() {
  const navigate = useNavigate();
  const { mockLogin, isAuthenticated, currentUser } = useAuth();

  const features = [
    {
      title: "Legal Documents",
      description: "Generate and review legal documents with AI assistance",
      icon: <DescriptionIcon sx={{ fontSize: 40, color: '#1976d2' }} />,
      path: '/services/contracts'
    },
    {
      title: "Know Your Rights",
      description: "Get instant information about your legal rights and protections",
      icon: <GavelIcon sx={{ fontSize: 40, color: '#1976d2' }} />,
      path: '/resources/rights'
    },
    {
      title: "Virtual Paralegal",
      description: "AI-powered paralegal assistance for attorneys and legal aid",
      icon: <PersonIcon sx={{ fontSize: 40, color: '#1976d2' }} />,
      path: '/virtual-paralegal'
    },
    {
      title: "Immigration Help",
      description: "Support for visa applications and immigration processes",
      icon: <FlightIcon sx={{ fontSize: 40, color: '#1976d2' }} />,
      path: '/services/immigration'
    },
    {
      title: "Pro Bono Services",
      description: "Connect with legal professionals offering free services",
      icon: <BuildIcon sx={{ fontSize: 40, color: '#1976d2' }} />,
      path: '/services'
    },
    {
      title: "Resources",
      description: "Access helpful legal resources and guides",
      icon: <ListAltIcon sx={{ fontSize: 40, color: '#1976d2' }} />,
      path: '/resources'
    },
    {
      title: "AI Legal Assistant",
      description: "Get instant answers to your legal questions 24/7",
      icon: <ChatIcon sx={{ fontSize: 40, color: '#1976d2' }} />,
      path: '/legal-chat'
    }
  ];

  const testimonials = [
    {
      name: "Sarah M.",
      role: "Immigration Client",
      rating: 5,
      text: "SmartProBono helped me understand my visa application process clearly. The AI guidance was incredibly helpful.",
      avatar: "S"
    },
    {
      name: "James R.",
      role: "Pro Bono Attorney",
      rating: 5,
      text: "This platform streamlines document preparation and client intake. It's a game-changer for pro bono work.",
      avatar: "J"
    },
    {
      name: "Maria L.",
      role: "Housing Rights Client",
      rating: 5,
      text: "The eviction defense tools helped me understand my rights and prepare my response. Thank you!",
      avatar: "M"
    }
  ];

  const trustSignals = [
    {
      icon: <SecurityIcon sx={{ fontSize: 40, color: '#1976d2' }} />,
      title: "Bank-Level Security",
      description: "Your data is protected with enterprise-grade encryption"
    },
    {
      icon: <VerifiedUserIcon sx={{ fontSize: 40, color: '#1976d2' }} />,
      title: "Licensed Attorneys",
      description: "All legal content reviewed by qualified professionals"
    },
    {
      icon: <CheckCircleIcon sx={{ fontSize: 40, color: '#1976d2' }} />,
      title: "ABA Guidelines",
      description: "Compliant with American Bar Association standards"
    }
  ];

  return (
    <Box>
      {/* Hero Section */}
      <Box 
        sx={{ 
          background: 'linear-gradient(45deg, #1976d2 30%, #2196f3 90%)',
          color: 'white',
          pt: { xs: 6, md: 8 },
          pb: { xs: 6, md: 8 },
          position: 'relative',
          overflow: 'hidden'
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
            background: `
              linear-gradient(45deg, transparent 45%, #ffffff 45%, #ffffff 55%, transparent 55%),
              linear-gradient(-45deg, transparent 45%, #ffffff 45%, #ffffff 55%, transparent 55%)
            `,
            backgroundSize: '20px 20px'
          }}
        />
        
        <Container maxWidth="lg">
          <Grid container spacing={4} alignItems="center">
            <Grid item xs={12} md={7}>
              <Typography 
                variant="h1" 
                gutterBottom 
                sx={{ 
                  fontWeight: 800,
                  fontSize: { xs: '2rem', md: '2.75rem' },
                  textShadow: '2px 2px 4px rgba(0,0,0,0.2)',
                  lineHeight: 1.2
                }}
              >
                Free Legal Help Made Simple
              </Typography>
              <Typography 
                variant="h5" 
                paragraph 
                sx={{ 
                  mb: 4, 
                  opacity: 0.9,
                  maxWidth: '600px',
                  lineHeight: 1.5,
                  fontSize: { xs: '1.1rem', md: '1.25rem' }
                }}
              >
                Get instant legal assistance, document generation, and professional guidance - all in one place.
              </Typography>
              <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap' }}>
                {!isAuthenticated && (
                  <Button 
                    variant="contained" 
                    color="secondary" 
                    onClick={mockLogin} 
                    sx={{ mr: 2 }}
                  >
                    TEST LOGIN
                  </Button>
                )}
                <Button
                  variant="contained"
                  color="primary"
                  onClick={() => navigate('/scan-document')}
                  sx={{ mr: 2 }}
                >
                  GO TO SCANNER
                </Button>
                {isAuthenticated && (
                  <Typography variant="body2" sx={{ mt: 2, color: 'success.main' }}>
                    Logged in as: {currentUser?.first_name} {currentUser?.last_name}
                  </Typography>
                )}
                <Button
                  variant="contained"
                  size="large"
                  onClick={() => navigate('/onboarding')}
                  sx={{ 
                    py: 1.5, 
                    px: 3,
                    fontSize: '1rem',
                    backgroundColor: 'white',
                    color: '#1976d2',
                    '&:hover': {
                      backgroundColor: 'rgba(255, 255, 255, 0.9)'
                    }
                  }}
                >
                  Get Started
                </Button>
                <Button
                  variant="outlined"
                  size="large"
                  startIcon={<ChatIcon />}
                  onClick={() => navigate('/legal-chat')}
                  sx={{ 
                    py: 1.5, 
                    px: 3,
                    fontSize: '1rem',
                    borderColor: 'white',
                    color: 'white',
                    '&:hover': {
                      borderColor: 'rgba(255, 255, 255, 0.9)',
                      backgroundColor: 'rgba(255, 255, 255, 0.1)'
                    }
                  }}
                >
                  Talk to AI Assistant
                </Button>
                <Button
                  variant="outlined"
                  size="large"
                  startIcon={<BalanceIcon />}
                  onClick={() => navigate('/services')}
                  sx={{ 
                    py: 1.5, 
                    px: 3,
                    fontSize: '1rem',
                    borderColor: 'white',
                    color: 'white',
                    '&:hover': {
                      borderColor: 'rgba(255, 255, 255, 0.9)',
                      backgroundColor: 'rgba(255, 255, 255, 0.1)'
                    }
                  }}
                >
                  Browse Services
                </Button>
              </Box>
            </Grid>
            <Grid 
              item 
              xs={12} 
              md={5} 
              sx={{ 
                display: 'flex', 
                justifyContent: 'center',
                alignItems: 'center'
              }}
            >
              <Box sx={{ 
                display: 'flex', 
                flexDirection: 'column', 
                gap: 2,
                width: '100%',
                maxWidth: 360,
                p: 2
              }}>
                <Paper 
                  elevation={6} 
                  sx={{ 
                    p: 3, 
                    bgcolor: 'rgba(255, 255, 255, 0.9)',
                    borderRadius: 2
                  }}
                >
                  <Typography variant="h6" color="primary" gutterBottom sx={{ fontSize: '1.1rem', fontWeight: 600 }}>
                    Why Choose Us?
                  </Typography>
                  <Box component="ul" sx={{ m: 0, pl: 2, color: 'text.primary' }}>
                    <Typography component="li" sx={{ mb: 1, fontSize: '0.95rem' }}>24/7 AI-powered legal assistance</Typography>
                    <Typography component="li" sx={{ mb: 1, fontSize: '0.95rem' }}>Free document generation</Typography>
                    <Typography component="li" sx={{ mb: 1, fontSize: '0.95rem' }}>Expert legal guidance</Typography>
                    <Typography component="li" sx={{ fontSize: '0.95rem' }}>Secure & confidential</Typography>
                  </Box>
                </Paper>
              </Box>
            </Grid>
          </Grid>
        </Container>
      </Box>

      {/* Trust Signals Section */}
      <Container maxWidth="lg" sx={{ py: 6 }}>
        <Grid container spacing={4}>
          {trustSignals.map((signal) => (
            <Grid item xs={12} md={4} key={signal.title}>
              <Paper 
                elevation={0} 
                sx={{ 
                  p: 3, 
                  textAlign: 'center',
                  backgroundColor: 'transparent'
                }}
              >
                {signal.icon}
                <Typography variant="h6" sx={{ mt: 2, mb: 1 }}>
                  {signal.title}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  {signal.description}
                </Typography>
              </Paper>
            </Grid>
          ))}
        </Grid>
      </Container>

      {/* Features Section */}
      <Container maxWidth="lg" sx={{ mb: 8, mt: 8 }}>
        <Typography variant="h4" align="center" gutterBottom fontWeight="bold">
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
                    boxShadow: 4
                  }
                }}
              >
                <CardContent sx={{ flexGrow: 1, textAlign: 'center', p: 3 }}>
                  <Box sx={{ mb: 2 }}>
                    {feature.icon}
                  </Box>
                  <Typography variant="h5" gutterBottom>
                    {feature.title}
                  </Typography>
                  <Typography color="text.secondary">
                    {feature.description}
                  </Typography>
                </CardContent>
                <Divider />
                <CardActions sx={{ justifyContent: 'center', p: 2 }}>
                  <Button
                    onClick={() => navigate(feature.path)}
                    variant="outlined"
                    size="large"
                  >
                    Learn More
                  </Button>
                </CardActions>
              </Card>
            </Grid>
          ))}
        </Grid>
      </Container>

      {/* Virtual Paralegal Assistant Highlight */}
      <Box sx={{ 
        bgcolor: 'secondary.light', 
        py: 6
      }}>
        <Container maxWidth="lg">
          <Grid container spacing={4} alignItems="center">
            <Grid item xs={12} md={6}>
              <Typography 
                variant="h4" 
                component="h2" 
                gutterBottom 
                fontWeight="bold"
                sx={{ color: 'primary.main' }}
              >
                Virtual Paralegal Assistant
              </Typography>
              <Typography variant="h6" paragraph sx={{ mb: 3 }}>
                Helping lawyers and legal aid organizations serve more clients efficiently
              </Typography>
              <Typography paragraph>
                Our AI-powered Virtual Paralegal Assistant automates client intake, document preparation, 
                and case screening - allowing legal professionals to focus on what matters most.
              </Typography>
              <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 2, mb: 3 }}>
                <Chip label="Client Intake" color="primary" />
                <Chip label="Document Automation" color="primary" />
                <Chip label="Case Screening" color="primary" />
                <Chip label="Self-Service Legal Help" color="primary" />
              </Box>
              <Button 
                variant="contained" 
                color="primary" 
                size="large" 
                onClick={() => navigate('/virtual-paralegal')}
                sx={{ mt: 2 }}
              >
                Learn More
              </Button>
            </Grid>
            <Grid item xs={12} md={6}>
              <Box 
                sx={{ 
                  p: 4, 
                  bgcolor: 'background.paper', 
                  borderRadius: 2,
                  boxShadow: 3
                }}
              >
                <Typography variant="h6" gutterBottom color="primary.main">
                  What Our Virtual Paralegal Can Do:
                </Typography>
                <List>
                  <ListItem>
                    <ListItemIcon>
                      <CheckCircleIcon color="primary" />
                    </ListItemIcon>
                    <ListItemText 
                      primary="Save 15+ hours per week on admin tasks" 
                      secondary="Automate routine document preparation and client communication"
                    />
                  </ListItem>
                  <ListItem>
                    <ListItemIcon>
                      <CheckCircleIcon color="primary" />
                    </ListItemIcon>
                    <ListItemText 
                      primary="Streamline client intake" 
                      secondary="Digital forms with automated data extraction and processing"
                    />
                  </ListItem>
                  <ListItem>
                    <ListItemIcon>
                      <CheckCircleIcon color="primary" />
                    </ListItemIcon>
                    <ListItemText 
                      primary="Pre-screen potential clients" 
                      secondary="Use customizable questionnaires to determine eligibility"
                    />
                  </ListItem>
                  <ListItem>
                    <ListItemIcon>
                      <CheckCircleIcon color="primary" />
                    </ListItemIcon>
                    <ListItemText 
                      primary="Help more clients with limited resources" 
                      secondary="Perfect for solo attorneys, small firms, and legal aid organizations"
                    />
                  </ListItem>
                </List>
              </Box>
            </Grid>
          </Grid>
        </Container>
      </Box>

      {/* Testimonials Section */}
      <Box sx={{ bgcolor: 'background.default', py: 6 }}>
        <Container maxWidth="lg">
          <Typography variant="h4" align="center" gutterBottom>
            What Our Users Say
          </Typography>
          <Grid container spacing={4} sx={{ mt: 2 }}>
            {testimonials.map((testimonial) => (
              <Grid item xs={12} md={4} key={testimonial.name}>
                <Card sx={{ height: '100%' }}>
                  <CardContent>
                    <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                      <Avatar sx={{ bgcolor: 'primary.main', mr: 2 }}>
                        {testimonial.avatar}
                      </Avatar>
                      <Box>
                        <Typography variant="h6">{testimonial.name}</Typography>
                        <Typography variant="body2" color="text.secondary">
                          {testimonial.role}
                        </Typography>
                      </Box>
                    </Box>
                    <Rating value={testimonial.rating} readOnly sx={{ mb: 2 }} />
                    <Typography variant="body1">
                      "{testimonial.text}"
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
            ))}
          </Grid>
        </Container>
      </Box>
    </Box>
  );
}

export default HomePage;