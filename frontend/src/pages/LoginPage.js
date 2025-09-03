import React, { useState } from 'react';
import { 
  Box, 
  Typography, 
  TextField, 
  Link,
  Grid,
  Alert,
  Snackbar,
  CircularProgress,
  Divider
} from '@mui/material';
import { Formik, Form, Field } from 'formik';
import * as Yup from 'yup';
import { useNavigate, Link as RouterLink } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { isSocketConnected } from '../services/socket';
import { motion } from 'framer-motion';
import { 
  PageLayout, 
  Section, 
  Button, 
  Card, 
  designTokens 
} from '../design-system';
import ErrorOutlineIcon from '@mui/icons-material/ErrorOutline';
import LoginIcon from '@mui/icons-material/Login';
import GoogleIcon from '@mui/icons-material/Google';
import FacebookIcon from '@mui/icons-material/Facebook';

// Validation schema
const LoginSchema = Yup.object().shape({
  email: Yup.string()
    .email('Invalid email')
    .required('Email is required'),
  password: Yup.string()
    .required('Password is required')
    .min(6, 'Password must be at least 6 characters'),
});

const LoginPage = () => {
  const navigate = useNavigate();
  const { login } = useAuth();
  const [, setError] = useState('');
  const [showAlert, setShowAlert] = useState(false);
  const [alertType, setAlertType] = useState('error');
  const [alertMessage, setAlertMessage] = useState('');
  const [isConnectingWebSocket, setIsConnectingWebSocket] = useState(false);

  const handleSubmit = async (values, { setSubmitting }) => {
    try {
      setError('');
      setShowAlert(false);
      
      const { success, error } = await login(values.email, values.password);
      
      if (success) {
        // Show connecting message
        setAlertType('info');
        setAlertMessage('Login successful! Establishing secure connection...');
        setShowAlert(true);
        setIsConnectingWebSocket(true);
        
        // Check WebSocket connection (with timeout)
        const checkSocketConnection = () => {
          // Check if socket is connected
          if (isSocketConnected()) {
            setAlertType('success');
            setAlertMessage('Connected successfully!');
            setShowAlert(true);
            setIsConnectingWebSocket(false);
            
            // Redirect after a brief delay to show the success message
            setTimeout(() => {
              navigate('/');
            }, 1000);
          } else {
            // If not connected yet, check again after a short delay (up to 10 attempts)
            let attemptCount = 0;
            const interval = setInterval(() => {
              attemptCount++;
              if (isSocketConnected()) {
                clearInterval(interval);
                setAlertType('success');
                setAlertMessage('Connected successfully!');
                setShowAlert(true);
                setIsConnectingWebSocket(false);
                
                // Redirect after a brief delay
                setTimeout(() => {
                  navigate('/');
                }, 1000);
              } else if (attemptCount >= 10) {
                // If still not connected after max attempts, continue anyway
                clearInterval(interval);
                setAlertType('warning');
                setAlertMessage('Connected with limited functionality. Real-time notifications may be delayed.');
                setShowAlert(true);
                setIsConnectingWebSocket(false);
                
                // Redirect after a brief delay
                setTimeout(() => {
                  navigate('/');
                }, 2000);
              }
            }, 300);
          }
        };
        
        // Allow a little time for the socket to connect before checking
        setTimeout(checkSocketConnection, 500);
      } else {
        setAlertType('error');
        setAlertMessage(error || 'Invalid email or password');
        setShowAlert(true);
      }
    } catch (error) {
      console.error('Login error:', error);
      setAlertType('error');
      setAlertMessage('An error occurred during login. Please try again.');
      setShowAlert(true);
    } finally {
      setSubmitting(false);
    }
  };

  const handleCloseAlert = () => {
    setShowAlert(false);
  };

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        duration: 0.6,
        staggerChildren: 0.1,
      },
    },
  };

  const itemVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: {
      opacity: 1,
      y: 0,
      transition: {
        duration: 0.5,
        ease: [0.25, 0.46, 0.45, 0.94],
      },
    },
  };

  return (
    <PageLayout background="light" padding="normal">
      <Section variant="hero" background="gradient" header={false}>
        <motion.div
          variants={containerVariants}
          initial="hidden"
          animate="visible"
        >
          <Box
            sx={{
              display: 'flex',
              justifyContent: 'center',
              alignItems: 'center',
              minHeight: '100vh',
              py: designTokens.spacing[12],
            }}
          >
            <motion.div variants={itemVariants}>
              <Card
                variant="elevated"
                sx={{
                  maxWidth: 480,
                  width: '100%',
                  p: designTokens.spacing[8],
                  background: 'rgba(255, 255, 255, 0.95)',
                  backdropFilter: 'blur(20px)',
                  border: '1px solid rgba(255, 255, 255, 0.2)',
                }}
              >
                {/* Header */}
                <motion.div variants={itemVariants}>
                  <Box sx={{ textAlign: 'center', mb: designTokens.spacing[8] }}>
                    <Box
                      sx={{
                        width: 80,
                        height: 80,
                        borderRadius: '50%',
                        background: designTokens.gradients.primary,
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        margin: '0 auto',
                        mb: designTokens.spacing[4],
                      }}
                    >
                      <LoginIcon sx={{ fontSize: 40, color: 'white' }} />
                    </Box>
                    <Typography
                      variant="h3"
                      sx={{
                        fontWeight: designTokens.typography.fontWeight.bold,
                        color: designTokens.colors.neutral[800],
                        mb: designTokens.spacing[2],
                      }}
                    >
                      Welcome Back
                    </Typography>
                    <Typography
                      variant="body1"
                      sx={{
                        color: designTokens.colors.neutral[500],
                        fontSize: designTokens.typography.fontSize.lg,
                      }}
                    >
                      Sign in to your SmartProBono account
                    </Typography>
                  </Box>
                </motion.div>

                {/* Alert */}
                {showAlert && (
                  <motion.div variants={itemVariants}>
                    <Alert 
                      severity={alertType} 
                      icon={<ErrorOutlineIcon />} 
                      sx={{ 
                        mb: designTokens.spacing[4],
                        borderRadius: designTokens.borderRadius.md,
                      }}
                    >
                      {alertMessage}
                    </Alert>
                  </motion.div>
                )}

                {/* Login Form */}
                <motion.div variants={itemVariants}>
                  <Formik
                    initialValues={{ email: '', password: '' }}
                    validationSchema={LoginSchema}
                    onSubmit={handleSubmit}
                  >
                    {({ errors, touched, isSubmitting }) => (
                      <Form>
                        <Box sx={{ mb: designTokens.spacing[6] }}>
                          <Field
                            as={TextField}
                            fullWidth
                            id="email"
                            label="Email Address"
                            name="email"
                            autoComplete="email"
                            autoFocus
                            error={touched.email && Boolean(errors.email)}
                            helperText={touched.email && errors.email}
                            disabled={isSubmitting || isConnectingWebSocket}
                            sx={{
                              mb: designTokens.spacing[4],
                              '& .MuiOutlinedInput-root': {
                                borderRadius: designTokens.borderRadius.md,
                              },
                            }}
                          />
                          
                          <Field
                            as={TextField}
                            fullWidth
                            name="password"
                            label="Password"
                            type="password"
                            id="password"
                            autoComplete="current-password"
                            error={touched.password && Boolean(errors.password)}
                            helperText={touched.password && errors.password}
                            disabled={isSubmitting || isConnectingWebSocket}
                            sx={{
                              '& .MuiOutlinedInput-root': {
                                borderRadius: designTokens.borderRadius.md,
                              },
                            }}
                          />
                        </Box>

                        <Button
                          type="submit"
                          fullWidth
                          variant="primary"
                          size="large"
                          startIcon={isSubmitting ? <CircularProgress size={20} color="inherit" /> : <LoginIcon />}
                          disabled={isSubmitting || isConnectingWebSocket}
                          sx={{ mb: designTokens.spacing[6] }}
                        >
                          {isSubmitting ? 'Signing In...' : 'Sign In'}
                        </Button>
                      </Form>
                    )}
                  </Formik>
                </motion.div>

                {/* Divider */}
                <motion.div variants={itemVariants}>
                  <Box sx={{ display: 'flex', alignItems: 'center', mb: designTokens.spacing[6] }}>
                    <Divider sx={{ flex: 1 }} />
                    <Typography
                      variant="body2"
                      sx={{
                        px: designTokens.spacing[4],
                        color: designTokens.colors.neutral[500],
                        fontWeight: designTokens.typography.fontWeight.medium,
                      }}
                    >
                      Or continue with
                    </Typography>
                    <Divider sx={{ flex: 1 }} />
                  </Box>
                </motion.div>

                {/* Social Login */}
                <motion.div variants={itemVariants}>
                  <Grid container spacing={designTokens.spacing[3]} sx={{ mb: designTokens.spacing[6] }}>
                    <Grid item xs={6}>
                      <Button
                        variant="ghost"
                        fullWidth
                        startIcon={<GoogleIcon />}
                        sx={{
                          border: `1px solid ${designTokens.colors.neutral[300]}`,
                          color: designTokens.colors.neutral[700],
                          '&:hover': {
                            backgroundColor: designTokens.colors.neutral[50],
                          },
                        }}
                      >
                        Google
                      </Button>
                    </Grid>
                    <Grid item xs={6}>
                      <Button
                        variant="ghost"
                        fullWidth
                        startIcon={<FacebookIcon />}
                        sx={{
                          border: `1px solid ${designTokens.colors.neutral[300]}`,
                          color: designTokens.colors.neutral[700],
                          '&:hover': {
                            backgroundColor: designTokens.colors.neutral[50],
                          },
                        }}
                      >
                        Facebook
                      </Button>
                    </Grid>
                  </Grid>
                </motion.div>

                {/* Links */}
                <motion.div variants={itemVariants}>
                  <Box sx={{ textAlign: 'center' }}>
                    <Link
                      component={RouterLink}
                      to="/forgot-password"
                      variant="body2"
                      sx={{
                        color: designTokens.colors.primary[600],
                        textDecoration: 'none',
                        fontWeight: designTokens.typography.fontWeight.medium,
                        '&:hover': {
                          textDecoration: 'underline',
                        },
                      }}
                    >
                      Forgot your password?
                    </Link>
                  </Box>
                </motion.div>

                <motion.div variants={itemVariants}>
                  <Box sx={{ textAlign: 'center', mt: designTokens.spacing[6] }}>
                    <Typography
                      variant="body2"
                      sx={{
                        color: designTokens.colors.neutral[500],
                        mb: designTokens.spacing[2],
                      }}
                    >
                      Don't have an account?
                    </Typography>
                    <Link
                      component={RouterLink}
                      to="/register"
                      variant="body2"
                      sx={{
                        color: designTokens.colors.primary[600],
                        textDecoration: 'none',
                        fontWeight: designTokens.typography.fontWeight.semibold,
                        '&:hover': {
                          textDecoration: 'underline',
                        },
                      }}
                    >
                      Sign up for free
                    </Link>
                  </Box>
                </motion.div>
              </Card>
            </motion.div>
          </Box>
        </motion.div>
      </Section>

      {/* Snackbar for alerts */}
      <Snackbar
        open={showAlert}
        autoHideDuration={6000}
        onClose={handleCloseAlert}
        anchorOrigin={{ vertical: 'top', horizontal: 'center' }}
      >
        <Alert
          onClose={handleCloseAlert}
          severity={alertType}
          sx={{ width: '100%' }}
        >
          {alertMessage}
        </Alert>
      </Snackbar>
    </PageLayout>
  );
};

export default LoginPage;