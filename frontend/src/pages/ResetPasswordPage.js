import React, { useState, useEffect } from 'react';
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
  CircularProgress,
  InputAdornment,
  IconButton
} from '@mui/material';
import { Formik, Form, Field } from 'formik';
import * as Yup from 'yup';
import { Link as RouterLink, useParams, useNavigate } from 'react-router-dom';
import axios from 'axios';
import Visibility from '@mui/icons-material/Visibility';
import VisibilityOff from '@mui/icons-material/VisibilityOff';
import { API_URL } from '../config';

// Validation schema
const ResetPasswordSchema = Yup.object().shape({
  password: Yup.string()
    .min(8, 'Password must be at least 8 characters')
    .required('Password is required')
    .matches(
      /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]/,
      'Password must contain at least one uppercase letter, one lowercase letter, one number, and one special character'
    ),
  confirmPassword: Yup.string()
    .oneOf([Yup.ref('password'), null], 'Passwords must match')
    .required('Confirm password is required'),
});

const ResetPasswordPage = () => {
  const { token } = useParams();
  const navigate = useNavigate();
  const [message, setMessage] = useState('');
  const [showAlert, setShowAlert] = useState(false);
  const [alertType, setAlertType] = useState('success');
  const [resetCompleted, setResetCompleted] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [tokenValid, setTokenValid] = useState(true);

  useEffect(() => {
    // Check if token exists in URL
    if (!token) {
      setTokenValid(false);
      setAlertType('error');
      setMessage('No reset token provided. Please request a new password reset.');
      setShowAlert(true);
    }
  }, [token]);

  const handleClickShowPassword = () => {
    setShowPassword(!showPassword);
  };

  const handleClickShowConfirmPassword = () => {
    setShowConfirmPassword(!showConfirmPassword);
  };

  const handleSubmit = async (values, { setSubmitting }) => {
    try {
      await axios.post(`${API_URL}/api/auth/reset-password`, {
        token: token,
        password: values.password
      });
      
      setAlertType('success');
      setMessage('Your password has been successfully reset.');
      setShowAlert(true);
      setResetCompleted(true);
      
      // Redirect to login after 3 seconds
      setTimeout(() => {
        navigate('/login');
      }, 3000);
    } catch (error) {
      setAlertType('error');
      setMessage(error.response?.data?.message || 'An error occurred. Please try again or request a new password reset.');
      setShowAlert(true);
      if (error.response?.status === 400 && error.response?.data?.error === 'Invalid or expired token') {
        setTokenValid(false);
      }
    } finally {
      setSubmitting(false);
    }
  };

  const handleCloseAlert = () => {
    setShowAlert(false);
  };

  if (!tokenValid) {
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
              Invalid Reset Link
            </Typography>
            <Alert severity="error" sx={{ mb: 3, width: '100%' }}>
              This password reset link is invalid or has expired.
            </Alert>
            <Typography variant="body1" paragraph>
              Please request a new password reset link.
            </Typography>
            <Button
              component={RouterLink}
              to="/forgot-password"
              variant="contained"
              color="primary"
              sx={{ mt: 2 }}
            >
              Request New Link
            </Button>
          </Paper>
        </Box>
      </Container>
    );
  }

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
            Reset Your Password
          </Typography>
          
          {resetCompleted ? (
            <Box textAlign="center">
              <Alert severity="success" sx={{ mb: 3 }}>
                Password reset successful!
              </Alert>
              <Typography variant="body1" paragraph>
                Your password has been successfully reset. You will be redirected to the login page shortly.
              </Typography>
              <Button
                component={RouterLink}
                to="/login"
                variant="contained"
                color="primary"
                sx={{ mt: 2 }}
              >
                Go to Login
              </Button>
            </Box>
          ) : (
            <>
              <Typography variant="body2" color="text.secondary" paragraph>
                Please enter your new password below.
              </Typography>
              
              <Formik
                initialValues={{ password: '', confirmPassword: '' }}
                validationSchema={ResetPasswordSchema}
                onSubmit={handleSubmit}
              >
                {({ errors, touched, isSubmitting }) => (
                  <Form style={{ width: '100%' }}>
                    <Field
                      as={TextField}
                      margin="normal"
                      fullWidth
                      id="password"
                      label="New Password"
                      name="password"
                      type={showPassword ? 'text' : 'password'}
                      autoComplete="new-password"
                      error={touched.password && Boolean(errors.password)}
                      helperText={touched.password && errors.password}
                      InputProps={{
                        endAdornment: (
                          <InputAdornment position="end">
                            <IconButton
                              aria-label="toggle password visibility"
                              onClick={handleClickShowPassword}
                              edge="end"
                            >
                              {showPassword ? <VisibilityOff /> : <Visibility />}
                            </IconButton>
                          </InputAdornment>
                        ),
                      }}
                    />
                    
                    <Field
                      as={TextField}
                      margin="normal"
                      fullWidth
                      id="confirmPassword"
                      label="Confirm New Password"
                      name="confirmPassword"
                      type={showConfirmPassword ? 'text' : 'password'}
                      autoComplete="new-password"
                      error={touched.confirmPassword && Boolean(errors.confirmPassword)}
                      helperText={touched.confirmPassword && errors.confirmPassword}
                      InputProps={{
                        endAdornment: (
                          <InputAdornment position="end">
                            <IconButton
                              aria-label="toggle password visibility"
                              onClick={handleClickShowConfirmPassword}
                              edge="end"
                            >
                              {showConfirmPassword ? <VisibilityOff /> : <Visibility />}
                            </IconButton>
                          </InputAdornment>
                        ),
                      }}
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
                        'Reset Password'
                      )}
                    </Button>
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

export default ResetPasswordPage; 