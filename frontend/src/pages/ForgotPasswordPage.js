import React, { useState } from 'react';
import { 
  Container, 
  Box, 
  Typography, 
  TextField, 
  Button, 
  Paper,
  Link,
  Alert,
  Snackbar,
  CircularProgress
} from '@mui/material';
import { Formik, Form, Field } from 'formik';
import * as Yup from 'yup';
import { Link as RouterLink } from 'react-router-dom';
import axios from 'axios';
import { API_URL } from '../config';

// Validation schema
const ForgotPasswordSchema = Yup.object().shape({
  email: Yup.string()
    .email('Invalid email')
    .required('Email is required'),
});

const ForgotPasswordPage = () => {
  const [message, setMessage] = useState('');
  const [showAlert, setShowAlert] = useState(false);
  const [alertType, setAlertType] = useState('success');
  const [resetRequested, setResetRequested] = useState(false);

  const handleSubmit = async (values, { setSubmitting }) => {
    try {
      const response = await axios.post(`${API_URL}/api/auth/forgot-password`, {
        email: values.email
      });
      
      setAlertType('success');
      setMessage('If an account exists with that email, a password reset link has been sent.');
      setShowAlert(true);
      setResetRequested(true);
      
      // For development: display the reset link
      if (response.data.reset_link) {
        console.log('Reset link:', response.data.reset_link);
      }
    } catch (error) {
      setAlertType('error');
      setMessage(error.response?.data?.message || 'An error occurred. Please try again.');
      setShowAlert(true);
    } finally {
      setSubmitting(false);
    }
  };

  const handleCloseAlert = () => {
    setShowAlert(false);
  };

  return (
    <Container maxWidth="xs">
      <Box
        sx={{
          marginTop: 8,
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
        }}
      >
        <Paper
          elevation={3}
          sx={{
            padding: 4,
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            width: '100%',
          }}
        >
          <Typography component="h1" variant="h5" sx={{ mb: 3 }}>
            Forgot Password
          </Typography>
          
          {resetRequested ? (
            <Box textAlign="center">
              <Alert severity="success" sx={{ mb: 3 }}>
                Password reset link sent
              </Alert>
              <Typography variant="body1" paragraph>
                If an account exists with that email, a password reset link has been sent. 
                Please check your email inbox and follow the instructions to reset your password.
              </Typography>
              <Button
                component={RouterLink}
                to="/login"
                variant="contained"
                color="primary"
                sx={{ mt: 2 }}
              >
                Return to Login
              </Button>
            </Box>
          ) : (
            <>
              <Typography variant="body2" color="text.secondary" paragraph>
                Enter your email address and we'll send you a link to reset your password.
              </Typography>
              
              <Formik
                initialValues={{ email: '' }}
                validationSchema={ForgotPasswordSchema}
                onSubmit={handleSubmit}
              >
                {({ errors, touched, isSubmitting }) => (
                  <Form style={{ width: '100%' }}>
                    <Field
                      as={TextField}
                      margin="normal"
                      fullWidth
                      id="email"
                      label="Email Address"
                      name="email"
                      autoComplete="email"
                      autoFocus
                      error={touched.email && Boolean(errors.email)}
                      helperText={touched.email && errors.email}
                    />
                    
                    <Button
                      type="submit"
                      fullWidth
                      variant="contained"
                      color="primary"
                      disabled={isSubmitting}
                      sx={{ mt: 3, mb: 2 }}
                    >
                      {isSubmitting ? (
                        <CircularProgress size={24} color="inherit" />
                      ) : (
                        'Send Reset Link'
                      )}
                    </Button>
                    
                    <Box textAlign="center">
                      <Link component={RouterLink} to="/login" variant="body2">
                        Back to Login
                      </Link>
                    </Box>
                  </Form>
                )}
              </Formik>
            </>
          )}
        </Paper>
      </Box>
      
      <Snackbar 
        open={showAlert} 
        autoHideDuration={6000} 
        onClose={handleCloseAlert}
        anchorOrigin={{ vertical: 'top', horizontal: 'center' }}
      >
        <Alert 
          onClose={handleCloseAlert} 
          severity={alertType} 
          variant="filled"
          sx={{ width: '100%' }}
        >
          {message}
        </Alert>
      </Snackbar>
    </Container>
  );
};

export default ForgotPasswordPage; 