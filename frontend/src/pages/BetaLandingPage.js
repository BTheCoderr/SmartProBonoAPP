import React, { useState } from 'react';
import {
  Box,
  Container,
  Typography,
  Button,
  Grid,
  Paper,
  TextField,
  Card,
  CardContent,
  Avatar,
  Rating,
  Snackbar,
  Alert,
  useTheme,
  useMediaQuery,
  IconButton,
  CircularProgress,
} from '@mui/material';
import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import ChatIcon from '@mui/icons-material/Chat';
import GavelIcon from '@mui/icons-material/Gavel';
import DescriptionIcon from '@mui/icons-material/Description';
import ArrowForwardIcon from '@mui/icons-material/ArrowForward';
import SecurityIcon from '@mui/icons-material/Security';
import AccessTimeIcon from '@mui/icons-material/AccessTime';
import SupportIcon from '@mui/icons-material/Support';
import axios from 'axios';

const BetaLandingPage = () => {
  const [email, setEmail] = useState('');
  const [loading, setLoading] = useState(false);
  const [snackbar, setSnackbar] = useState({ open: false, message: '', severity: 'success' });
  const navigate = useNavigate();
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('sm'));

  const handleError = (error) => {
    console.error('Error:', error);
    setSnackbar({
      open: true,
      message: error.response?.data?.message || 'An unexpected error occurred. Please try again.',
      severity: 'error'
    });
  };

  const handleJoinBeta = async (event) => {
    event.preventDefault();
    if (!email) {
      setSnackbar({
        open: true,
        message: 'Please enter your email address',
        severity: 'error'
      });
      return;
    }
    setLoading(true);

    try {
      // Try to use the backend API
      const response = await axios.post('/api/beta/signup', {
        email,
        source: 'landing_page'
      });
      
      console.log('Beta signup response:', response.data);
      
      setSnackbar({
        open: true,
        message: 'Thanks for joining! Please check your email for a confirmation link.',
        severity: 'success'
      });
      setEmail('');
      
    } catch (error) {
      // If the API fails, fall back to localStorage approach
      console.warn('API call failed, using localStorage fallback:', error);
      
      try {
        // Generate a mock confirmation token for testing
        const mockToken = btoa(email).replace(/=/g, '').slice(0, 20);
        console.log(`Generated confirmation token: ${mockToken}`);
        
        // Store in localStorage for testing confirmation flow
        localStorage.setItem('pendingConfirmation', JSON.stringify({
          email,
          token: mockToken,
          createdAt: new Date().toISOString()
        }));
        
        // Create confirmation URL
        const confirmationUrl = `/beta/confirm/${mockToken}`;
        
        setSnackbar({
          open: true,
          message: (
            <span>
              Thanks for joining! In a real app, you would receive a confirmation email. 
              For testing, <a href={confirmationUrl} style={{color: 'white', textDecoration: 'underline'}}>click here</a> to confirm.
            </span>
          ),
          severity: 'success'
        });
        setEmail('');
      } catch (fallbackError) {
        handleError(fallbackError);
      }
    } finally {
      setLoading(false);
    }
  };

  const isSubmitDisabled = loading || !email;

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

  const partners = [
    {
      name: "Legal Aid Society",
      logo: "/partners/legal-aid.png"
    },
    {
      name: "Pro Bono Net",
      logo: "/partners/pbn.png"
    },
    {
      name: "American Bar Association",
      logo: "/partners/aba.png"
    }
  ];

  const features = [
    {
      icon: <ChatIcon sx={{ fontSize: 40, color: theme.palette.primary.main }} />,
      title: "AI Legal Assistant",
      description: "Get instant answers to your legal questions 24/7",
      color: '#2196f3',
      onClick: () => navigate('/legal-chat')
    },
    {
      icon: <DescriptionIcon sx={{ fontSize: 40, color: theme.palette.primary.main }} />,
      title: "Document Generation",
      description: "Create legal documents automatically based on your needs",
      color: '#4caf50',
      onClick: () => navigate('/documents')
    },
    {
      icon: <GavelIcon sx={{ fontSize: 40, color: theme.palette.primary.main }} />,
      title: "Expert Guidance",
      description: "Connect with pro bono lawyers when needed",
      color: '#ff9800',
      onClick: () => navigate('/expert-help')
    }
  ];

  const benefits = [
    {
      icon: <SecurityIcon />,
      title: "Secure & Confidential",
      description: "Bank-level encryption for your data"
    },
    {
      icon: <AccessTimeIcon />,
      title: "24/7 Availability",
      description: "Get help whenever you need it"
    },
    {
      icon: <SupportIcon />,
      title: "Expert Support",
      description: "Access to legal professionals"
    }
  ];

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        delayChildren: 0.3,
        staggerChildren: 0.2
      }
    }
  };

  const itemVariants = {
    hidden: { y: 20, opacity: 0 },
    visible: {
      y: 0,
      opacity: 1
    }
  };

  return (
    <Box>
      {/* Hero Section */}
      <Box
        sx={{
          background: `linear-gradient(135deg, 
            ${theme.palette.primary.main} 0%, 
            ${theme.palette.primary.dark} 100%)`,
          color: 'white',
          pt: { xs: 8, md: 12 },
          pb: { xs: 8, md: 12 },
          position: 'relative',
          overflow: 'hidden',
        }}
      >
        {/* Animated background pattern */}
        <Box
          component={motion.div}
          animate={{
            backgroundPosition: ['0% 0%', '100% 100%'],
          }}
          transition={{
            duration: 20,
            repeat: Infinity,
            repeatType: 'reverse',
          }}
          sx={{
            position: 'absolute',
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            opacity: 0.1,
            backgroundImage: `linear-gradient(45deg, #fff 25%, transparent 25%),
              linear-gradient(-45deg, #fff 25%, transparent 25%),
              linear-gradient(45deg, transparent 75%, #fff 75%),
              linear-gradient(-45deg, transparent 75%, #fff 75%)`,
            backgroundSize: '20px 20px',
          }}
        />

        <Container maxWidth="lg">
          <Grid container spacing={4} alignItems="center">
            <Grid item xs={12} md={6}>
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.8 }}
              >
                <Typography
                  variant="h1"
                  gutterBottom
                  sx={{
                    fontWeight: 800,
                    fontSize: { xs: '2.5rem', md: '3.5rem' },
                    lineHeight: 1.2,
                    mb: 3,
                  }}
                >
                  Legal Help Made Simple
                </Typography>
                <Typography
                  variant="h5"
                  paragraph
                  sx={{
                    mb: 4,
                    opacity: 0.9,
                    fontSize: { xs: '1.1rem', md: '1.25rem' },
                    fontWeight: 300,
                  }}
                >
                  Join the beta and be among the first to experience AI-powered legal assistance.
                </Typography>

                {/* Beta Signup Form */}
                <Paper
                  component="form"
                  onSubmit={handleJoinBeta}
                  sx={{
                    p: '2px 4px',
                    display: 'flex',
                    alignItems: 'center',
                    maxWidth: 500,
                    backgroundColor: 'rgba(255, 255, 255, 0.1)',
                    backdropFilter: 'blur(10px)',
                    border: '1px solid rgba(255, 255, 255, 0.2)',
                  }}
                >
                  <TextField
                    fullWidth
                    placeholder="Enter your email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    disabled={loading}
                    sx={{
                      '& .MuiInputBase-input': {
                        color: 'white',
                      },
                      '& .MuiInputBase-root': {
                        backgroundColor: 'transparent',
                      },
                    }}
                    InputProps={{
                      disableUnderline: true,
                      sx: { px: 2, py: 1 },
                    }}
                  />
                  <IconButton
                    type="submit"
                    disabled={isSubmitDisabled}
                    sx={{
                      p: '10px',
                      color: 'white',
                      '&:hover': {
                        backgroundColor: 'rgba(255, 255, 255, 0.1)',
                      },
                    }}
                  >
                    {loading ? (
                      <CircularProgress size={24} color="inherit" />
                    ) : (
                      <ArrowForwardIcon />
                    )}
                  </IconButton>
                </Paper>
              </motion.div>
            </Grid>

            <Grid item xs={12} md={6}>
              <motion.div
                variants={containerVariants}
                initial="hidden"
                animate="visible"
                style={{
                  display: 'flex',
                  flexDirection: 'column',
                  gap: '20px',
                  alignItems: isMobile ? 'center' : 'flex-start'
                }}
              >
                {features.map((feature, index) => (
                  <motion.div
                    key={feature.title}
                    variants={itemVariants}
                    whileHover={{ scale: 1.05, translateX: 10 }}
                    style={{
                      width: '100%',
                      maxWidth: 350,
                      transform: `translateX(${isMobile ? 0 : index * 20}px)`
                    }}
                  >
                    <Card
                      sx={{
                        backgroundColor: 'rgba(255, 255, 255, 0.9)',
                        backdropFilter: 'blur(10px)',
                        boxShadow: 3,
                        borderLeft: 4,
                        borderColor: feature.color,
                        cursor: 'pointer',
                        '&:hover': {
                          boxShadow: 6,
                          backgroundColor: 'rgba(255, 255, 255, 0.95)',
                        }
                      }}
                      onClick={feature.onClick}
                    >
                      <CardContent>
                        <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                          {feature.icon}
                          <Typography variant="h6" sx={{ ml: 2 }}>
                            {feature.title}
                          </Typography>
                        </Box>
                        <Typography variant="body2" color="text.secondary">
                          {feature.description}
                        </Typography>
                      </CardContent>
                    </Card>
                  </motion.div>
                ))}
              </motion.div>
            </Grid>
          </Grid>
        </Container>
      </Box>

      {/* Benefits Section */}
      <Container maxWidth="lg" sx={{ py: 8 }}>
        <Typography
          variant="h4"
          align="center"
          gutterBottom
          sx={{ fontWeight: 700, mb: 6 }}
        >
          Why Choose SmartProBono?
        </Typography>
        <Grid container spacing={4}>
          {benefits.map((benefit, index) => (
            <Grid item xs={12} md={4} key={benefit.title}>
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.2 }}
              >
                <Paper
                  elevation={0}
                  sx={{
                    p: 3,
                    height: '100%',
                    backgroundColor: 'transparent',
                    border: '1px solid',
                    borderColor: 'divider',
                    transition: 'transform 0.3s ease-in-out',
                    '&:hover': {
                      transform: 'translateY(-8px)',
                    },
                  }}
                >
                  <Box sx={{ mb: 2, color: 'primary.main' }}>
                    {benefit.icon}
                  </Box>
                  <Typography variant="h6" gutterBottom>
                    {benefit.title}
                  </Typography>
                  <Typography color="text.secondary">
                    {benefit.description}
                  </Typography>
                </Paper>
              </motion.div>
            </Grid>
          ))}
        </Grid>
      </Container>

      {/* Partner Logos */}
      <Container maxWidth="lg" sx={{ py: 6 }}>
        <Typography variant="h6" align="center" color="text.secondary" gutterBottom>
          Trusted By Leading Organizations
        </Typography>
        <Grid container spacing={4} justifyContent="center" alignItems="center">
          {partners.map((partner) => (
            <Grid item key={partner.name}>
              <Box
                component="img"
                src={partner.logo}
                alt={partner.name}
                sx={{
                  height: 60,
                  filter: 'grayscale(100%)',
                  opacity: 0.7,
                  transition: '0.3s',
                  '&:hover': {
                    filter: 'grayscale(0%)',
                    opacity: 1,
                  },
                }}
              />
            </Grid>
          ))}
        </Grid>
      </Container>

      {/* Features Section */}
      <Container maxWidth="lg" sx={{ py: 8 }}>
        <Grid container spacing={4}>
          <Grid item xs={12} md={4}>
            <Card sx={{ height: '100%' }}>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  AI-Powered Legal Assistance
                </Typography>
                <Typography color="text.secondary">
                  Get instant answers to your legal questions and guidance on your specific situation.
                </Typography>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} md={4}>
            <Card sx={{ height: '100%' }}>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Document Generation
                </Typography>
                <Typography color="text.secondary">
                  Create legal documents automatically based on your information and needs.
                </Typography>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} md={4}>
            <Card sx={{ height: '100%' }}>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Expert Guidance
                </Typography>
                <Typography color="text.secondary">
                  Connect with pro bono lawyers and get professional legal advice when needed.
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      </Container>

      {/* Testimonials */}
      <Box sx={{ bgcolor: 'grey.50', py: 8 }}>
        <Container maxWidth="lg">
          <Typography variant="h4" align="center" gutterBottom fontWeight="bold">
            What People Are Saying
          </Typography>
          <motion.div
            variants={containerVariants}
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true }}
          >
            <Grid container spacing={4} sx={{ mt: 2 }}>
              {testimonials.map((testimonial, index) => (
                <Grid item xs={12} md={4} key={testimonial.name}>
                  <motion.div
                    variants={itemVariants}
                    whileHover={{ scale: 1.03 }}
                  >
                    <Card 
                      sx={{ 
                        height: '100%',
                        position: 'relative',
                        '&::before': {
                          content: '""',
                          position: 'absolute',
                          top: 0,
                          left: 0,
                          right: 0,
                          height: 4,
                          backgroundColor: 'primary.main',
                          borderTopLeftRadius: 4,
                          borderTopRightRadius: 4,
                        }
                      }}
                    >
                      <CardContent>
                        <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                          <Avatar 
                            sx={{ 
                              bgcolor: 'primary.main', 
                              mr: 2,
                              width: 56,
                              height: 56
                            }}
                          >
                            {testimonial.avatar}
                          </Avatar>
                          <Box>
                            <Typography variant="subtitle1" fontWeight="bold">
                              {testimonial.name}
                            </Typography>
                            <Typography variant="body2" color="text.secondary">
                              {testimonial.role}
                            </Typography>
                          </Box>
                        </Box>
                        <Rating value={testimonial.rating} readOnly sx={{ mb: 2 }} />
                        <Typography 
                          variant="body1" 
                          color="text.secondary"
                          sx={{ 
                            fontStyle: 'italic',
                            position: 'relative',
                            '&::before': {
                              content: '"""',
                              fontSize: '2rem',
                              color: 'primary.main',
                              opacity: 0.3,
                              position: 'absolute',
                              left: -16,
                              top: -8
                            }
                          }}
                        >
                          {testimonial.text}
                        </Typography>
                      </CardContent>
                    </Card>
                  </motion.div>
                </Grid>
              ))}
            </Grid>
          </motion.div>
        </Container>
      </Box>

      {/* New FAQ Section */}
      <Box sx={{ bgcolor: 'background.default', py: 8 }}>
        <Container maxWidth="lg">
          <Typography
            variant="h4"
            align="center"
            gutterBottom
            sx={{ fontWeight: 700, mb: 6 }}
          >
            Frequently Asked Questions
          </Typography>
          <Grid container spacing={4}>
            {[
              {
                question: "How does the AI legal assistant work?",
                answer: "Our AI assistant uses advanced natural language processing to understand your legal questions and provide accurate, relevant information based on current laws and regulations."
              },
              {
                question: "Is my information secure?",
                answer: "Yes, we use bank-level encryption and follow strict data protection protocols to ensure your information remains confidential and secure."
              },
              {
                question: "How can I connect with a pro bono lawyer?",
                answer: "After completing our intake form, our system matches you with available pro bono attorneys based on your legal needs and their expertise."
              },
              {
                question: "What types of legal documents can I generate?",
                answer: "You can generate various documents including contracts, legal letters, court forms, and immigration paperwork - all customized to your specific situation."
              }
            ].map((faq, index) => (
              <Grid item xs={12} md={6} key={index}>
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  transition={{ delay: index * 0.1 }}
                  viewport={{ once: true }}
                >
                  <Card sx={{ height: '100%' }}>
                    <CardContent>
                      <Typography variant="h6" gutterBottom color="primary">
                        {faq.question}
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        {faq.answer}
                      </Typography>
                    </CardContent>
                  </Card>
                </motion.div>
              </Grid>
            ))}
          </Grid>
        </Container>
      </Box>

      {/* Add Help Widget */}
      <Box
        component={motion.div}
        initial={{ scale: 0 }}
        animate={{ scale: 1 }}
        sx={{
          position: 'fixed',
          bottom: 20,
          right: 20,
          zIndex: 1000
        }}
      >
        <Button
          variant="contained"
          color="primary"
          startIcon={<ChatIcon />}
          onClick={() => {
            if (email) {
              handleJoinBeta();
            } else {
              navigate('/legal-chat');
            }
          }}
          sx={{
            borderRadius: 30,
            px: 3,
            py: 1.5,
            boxShadow: 4
          }}
        >
          {email ? 'Join Beta' : 'Need Help?'}
        </Button>
      </Box>

      {/* Snackbar for notifications */}
      <Snackbar
        open={snackbar.open}
        autoHideDuration={6000}
        onClose={() => setSnackbar({ ...snackbar, open: false })}
        anchorOrigin={{ vertical: 'bottom', horizontal: 'center' }}
      >
        <Alert
          onClose={() => setSnackbar({ ...snackbar, open: false })}
          severity={snackbar.severity}
          variant="filled"
          sx={{ width: '100%' }}
        >
          {snackbar.message}
        </Alert>
      </Snackbar>
    </Box>
  );
};

export default BetaLandingPage; 