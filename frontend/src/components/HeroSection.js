import React from 'react';
import {
  Box,
  Container,
  Grid,
  Typography,
  Button,
  useTheme,
  Chip,
  Stack,
} from '@mui/material';
import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import ChatIcon from '@mui/icons-material/Chat';
import DocumentScannerIcon from '@mui/icons-material/DocumentScanner';
import OnboardingIcon from '@mui/icons-material/PlayArrow';
import TrendingUpIcon from '@mui/icons-material/TrendingUp';
import SecurityIcon from '@mui/icons-material/Security';
import VerifiedUserIcon from '@mui/icons-material/VerifiedUser';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';

const HeroSection = () => {
  const theme = useTheme();
  const navigate = useNavigate();
  const { mockLogin, isAuthenticated, currentUser } = useAuth();

  const heroVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        duration: 0.8,
        staggerChildren: 0.2,
      },
    },
  };

  const itemVariants = {
    hidden: { opacity: 0, y: 30 },
    visible: {
      opacity: 1,
      y: 0,
      transition: {
        duration: 0.6,
        ease: [0.25, 0.46, 0.45, 0.94],
      },
    },
  };

  const floatingAnimation = {
    y: [0, -10, 0],
    transition: {
      duration: 3,
      repeat: Infinity,
      ease: "easeInOut",
    },
  };

  const stats = [
    { label: 'Users Helped', value: '10K+', icon: '👥' },
    { label: 'Documents Generated', value: '50K+', icon: '📄' },
    { label: 'Success Rate', value: '95%', icon: '🎯' },
  ];

  const trustSignals = [
    {
      icon: <SecurityIcon sx={{ fontSize: 24, color: theme.palette.success.main }} />,
      text: 'Bank-Level Security',
    },
    {
      icon: <VerifiedUserIcon sx={{ fontSize: 24, color: theme.palette.primary.main }} />,
      text: 'Licensed Attorneys',
    },
    {
      icon: <CheckCircleIcon sx={{ fontSize: 24, color: theme.palette.warning.main }} />,
      text: 'ABA Compliant',
    },
  ];

  return (
    <Box
      component={motion.div}
      variants={heroVariants}
      initial="hidden"
      animate="visible"
              sx={{
          background: `linear-gradient(135deg, #1e40af 0%, #3b82f6 100%)`,
          color: 'white',
          position: 'relative',
          overflow: 'hidden',
          pt: { xs: 12, md: 16 },
          pb: { xs: 12, md: 16 },
          borderRadius: { xs: 0, md: '0 0 40px 40px' },
          mx: { xs: 0, md: 2 },
          mb: { xs: 0, md: 4 },
          boxShadow: '0 8px 32px rgba(30, 64, 175, 0.3)',
        }}
    >
              {/* Background Elements */}
        <Box
          sx={{
            position: 'absolute',
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            background: 'rgba(0, 0, 0, 0.4)',
            zIndex: 1,
          }}
        />
        <Box
          sx={{
            position: 'absolute',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          opacity: 0.1,
          background: `
            radial-gradient(circle at 20% 80%, rgba(255,255,255,0.3) 0%, transparent 50%),
            radial-gradient(circle at 80% 20%, rgba(255,255,255,0.3) 0%, transparent 50%),
            radial-gradient(circle at 40% 40%, rgba(255,255,255,0.2) 0%, transparent 50%)
          `,
        }}
      />
      
      {/* Floating Shapes */}
      <motion.div
        animate={floatingAnimation}
        style={{
          position: 'absolute',
          top: '20%',
          right: '10%',
          width: 60,
          height: 60,
          borderRadius: '50%',
          background: 'rgba(255, 255, 255, 0.1)',
        }}
      />
      <motion.div
        animate={{ ...floatingAnimation, delay: 1 }}
        style={{
          position: 'absolute',
          top: '60%',
          left: '5%',
          width: 40,
          height: 40,
          borderRadius: '50%',
          background: 'rgba(255, 255, 255, 0.1)',
        }}
      />

      <Container maxWidth="lg" sx={{ position: 'relative', zIndex: 3 }}>
        <Grid container spacing={4} alignItems="center">
          {/* Left Content */}
          <Grid item xs={12} md={7}>
            <motion.div variants={itemVariants}>
              {/* Badge */}
              <Chip
                label="🚀 Now with AI-Powered Legal Assistance"
                color="secondary"
                sx={{
                  mb: 3,
                  backgroundColor: 'rgba(255, 255, 255, 0.2)',
                  color: 'white',
                  fontWeight: 600,
                  fontSize: '0.875rem',
                  '&:hover': {
                    backgroundColor: 'rgba(255, 255, 255, 0.3)',
                  },
                }}
              />

              {/* Main Heading */}
              <Typography
                variant="h1"
                gutterBottom
                sx={{
                  fontWeight: 900,
                  fontSize: { xs: '2.5rem', sm: '3rem', md: '3.5rem' },
                  lineHeight: 1.1,
                  textShadow: '0 4px 12px rgba(0,0,0,0.5)',
                  mb: 3,
                  color: '#ffffff',
                }}
              >
                Free Legal Help
                <br />
                <Box
                  component="span"
                  sx={{
                    background: 'linear-gradient(45deg, #ffffff 30%, #f0f9ff 90%)',
                    WebkitBackgroundClip: 'text',
                    WebkitTextFillColor: 'transparent',
                    backgroundClip: 'text',
                  }}
                >
                  Made Simple
                </Box>
              </Typography>

              {/* Subtitle */}
              <Typography
                variant="h5"
                paragraph
                sx={{
                  mb: 4,
                  opacity: 1,
                  maxWidth: '600px',
                  lineHeight: 1.6,
                  fontSize: { xs: '1.1rem', md: '1.25rem' },
                  fontWeight: 500,
                  color: '#ffffff',
                  textShadow: '0 2px 8px rgba(0,0,0,0.4)',
                }}
              >
                Get instant legal assistance, AI-powered document generation, and professional guidance - all in one secure platform.
              </Typography>

              {/* Stats */}
              <Box
                sx={{
                  display: 'flex',
                  gap: 3,
                  mb: 4,
                  flexWrap: 'wrap',
                }}
              >
                {stats.map((stat, index) => (
                  <motion.div
                    key={stat.label}
                    variants={itemVariants}
                    initial="hidden"
                    animate="visible"
                    transition={{ delay: 0.5 + index * 0.1 }}
                  >
                    <Box sx={{ textAlign: 'center' }}>
                      <Typography
                        variant="h4"
                        sx={{
                          fontWeight: 800,
                          fontSize: '1.5rem',
                          mb: 0.5,
                          color: '#ffffff',
                          textShadow: '0 2px 6px rgba(0,0,0,0.4)',
                        }}
                      >
                        {stat.value}
                      </Typography>
                      <Typography
                        variant="caption"
                        sx={{
                          opacity: 1,
                          fontSize: '0.75rem',
                          fontWeight: 600,
                          color: '#ffffff',
                          textShadow: '0 1px 4px rgba(0,0,0,0.4)',
                        }}
                      >
                        {stat.label}
                      </Typography>
                    </Box>
                  </motion.div>
                ))}
              </Box>

              {/* CTA Buttons */}
              <Stack
                direction={{ xs: 'column', sm: 'row' }}
                spacing={2}
                sx={{ mb: 4 }}
              >
                {!isAuthenticated && (
                  <Button
                    variant="contained"
                    size="large"
                    onClick={mockLogin}
                    startIcon={<OnboardingIcon />}
                    sx={{
                      backgroundColor: 'white',
                      color: theme.palette.primary.main,
                      fontWeight: 700,
                      py: 1.5,
                      px: 3,
                      fontSize: '1rem',
                      '&:hover': {
                        backgroundColor: 'rgba(255, 255, 255, 0.9)',
                        transform: 'translateY(-2px)',
                        boxShadow: '0 8px 25px rgba(0, 0, 0, 0.2)',
                      },
                    }}
                  >
                    Get Started Free
                  </Button>
                )}
                
                <Button
                  variant="outlined"
                  size="large"
                  startIcon={<DocumentScannerIcon />}
                  onClick={() => navigate('/scan-document')}
                  sx={{
                    borderColor: 'rgba(255, 255, 255, 0.8)',
                    color: 'white',
                    fontWeight: 600,
                    py: 1.5,
                    px: 3,
                    fontSize: '1rem',
                    '&:hover': {
                      borderColor: 'white',
                      backgroundColor: 'rgba(255, 255, 255, 0.1)',
                      transform: 'translateY(-2px)',
                    },
                  }}
                >
                  Scan Documents
                </Button>

                <Button
                  variant="outlined"
                  size="large"
                  startIcon={<ChatIcon />}
                  onClick={() => navigate('/legal-chat')}
                  sx={{
                    borderColor: 'rgba(255, 255, 255, 0.8)',
                    color: 'white',
                    fontWeight: 600,
                    py: 1.5,
                    px: 3,
                    fontSize: '1rem',
                    '&:hover': {
                      borderColor: 'white',
                      backgroundColor: 'rgba(255, 255, 255, 0.1)',
                      transform: 'translateY(-2px)',
                    },
                  }}
                >
                  AI Legal Chat
                </Button>
              </Stack>

              {/* Trust Signals */}
              <Box
                sx={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: 3,
                  flexWrap: 'wrap',
                }}
              >
                <Typography
                  variant="body2"
                  sx={{
                    opacity: 1,
                    fontWeight: 600,
                    color: '#ffffff',
                    textShadow: '0 1px 4px rgba(0,0,0,0.4)',
                  }}
                >
                  Trusted by:
                </Typography>
                {trustSignals.map((signal, index) => (
                  <motion.div
                    key={signal.text}
                    variants={itemVariants}
                    initial="hidden"
                    animate="visible"
                    transition={{ delay: 0.8 + index * 0.1 }}
                  >
                    <Box
                      sx={{
                        display: 'flex',
                        alignItems: 'center',
                        gap: 1,
                        backgroundColor: 'rgba(255, 255, 255, 0.1)',
                        px: 2,
                        py: 1,
                        borderRadius: 2,
                        backdropFilter: 'blur(10px)',
                      }}
                    >
                      {signal.icon}
                      <Typography
                        variant="caption"
                        sx={{
                          fontWeight: 600,
                          fontSize: '0.75rem',
                          color: '#ffffff',
                          textShadow: '0 1px 4px rgba(0,0,0,0.4)',
                        }}
                      >
                        {signal.text}
                      </Typography>
                    </Box>
                  </motion.div>
                ))}
              </Box>
            </motion.div>
          </Grid>

          {/* Right Content */}
          <Grid item xs={12} md={5}>
            <motion.div
              variants={itemVariants}
              style={{
                display: 'flex',
                justifyContent: 'center',
                alignItems: 'center',
              }}
            >
              <Box
                sx={{
                  display: 'flex',
                  flexDirection: 'column',
                  gap: 3,
                  width: '100%',
                  maxWidth: 400,
                }}
              >
                {/* Feature Cards */}
                <motion.div
                  animate={floatingAnimation}
                  transition={{ delay: 0.5 }}
                >
                  <Box
                    sx={{
                      p: 3,
                      backgroundColor: 'rgba(255, 255, 255, 0.95)',
                      borderRadius: 3,
                      boxShadow: '0 20px 40px rgba(0, 0, 0, 0.1)',
                      backdropFilter: 'blur(20px)',
                      border: '1px solid rgba(255, 255, 255, 0.2)',
                    }}
                  >
                    <Typography
                      variant="h6"
                      color="primary"
                      gutterBottom
                      sx={{
                        fontWeight: 700,
                        fontSize: '1.1rem',
                        display: 'flex',
                        alignItems: 'center',
                        gap: 1,
                      }}
                    >
                      <TrendingUpIcon />
                      Why Choose SmartProBono?
                    </Typography>
                    <Box
                      component="ul"
                      sx={{
                        m: 0,
                        pl: 2,
                        color: 'text.primary',
                      }}
                    >
                      <Typography
                        component="li"
                        sx={{
                          mb: 1,
                          fontSize: '0.9rem',
                          fontWeight: 500,
                        }}
                      >
                        24/7 AI-powered legal assistance
                      </Typography>
                      <Typography
                        component="li"
                        sx={{
                          mb: 1,
                          fontSize: '0.9rem',
                          fontWeight: 500,
                        }}
                      >
                        Free document generation & templates
                      </Typography>
                      <Typography
                        component="li"
                        sx={{
                          mb: 1,
                          fontSize: '0.9rem',
                          fontWeight: 500,
                        }}
                      >
                        Expert legal guidance & resources
                      </Typography>
                      <Typography
                        component="li"
                        sx={{
                          fontSize: '0.9rem',
                          fontWeight: 500,
                        }}
                      >
                        Secure, confidential & compliant
                      </Typography>
                    </Box>
                  </Box>
                </motion.div>

                {/* User Status Card */}
                {isAuthenticated && (
                  <motion.div
                    initial={{ opacity: 0, scale: 0.9 }}
                    animate={{ opacity: 1, scale: 1 }}
                    transition={{ delay: 1 }}
                  >
                    <Box
                      sx={{
                        p: 2,
                        backgroundColor: 'rgba(255, 255, 255, 0.9)',
                        borderRadius: 2,
                        textAlign: 'center',
                        border: '1px solid rgba(255, 255, 255, 0.3)',
                      }}
                    >
                      <Typography
                        variant="body2"
                        sx={{
                          color: 'success.main',
                          fontWeight: 600,
                          mb: 1,
                        }}
                      >
                        ✅ Welcome back!
                      </Typography>
                      <Typography
                        variant="body2"
                        sx={{
                          color: 'text.primary',
                          fontWeight: 500,
                        }}
                      >
                        {currentUser?.first_name} {currentUser?.last_name}
                      </Typography>
                    </Box>
                  </motion.div>
                )}
              </Box>
            </motion.div>
          </Grid>
        </Grid>
      </Container>
    </Box>
  );
};

export default HeroSection;
