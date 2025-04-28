import React, { useState } from 'react';
import { 
  Container, 
  Box, 
  Typography, 
  TextField, 
  Button, 
  Paper,
  Link,
  Grid,
  Alert,
  Snackbar,
  CircularProgress
} from '@mui/material';
import { Formik, Form, Field } from 'formik';
import * as Yup from 'yup';
import { useNavigate, Link as RouterLink } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { isSocketConnected } from '../services/socket';
import ErrorOutlineIcon from '@mui/icons-material/ErrorOutline';

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
  const [error, setError] = useState('');
  const [showAlert, setShowAlert] = useState(false);
  const [alertType, setAlertType] = useState('error');
  const [alertMessage, setAlertMessage] = useState('');
  const [isConnectingWebSocket, setIsConnectingWebSocket] = useState(false);

  const handleSubmit = async (values, { setSubmitting }) => {
    try {
      setError('');
      setShowAlert(false);
      
      const { success, error, user } = await login(values.email, values.password);
      
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
            Sign In
          </Typography>
          
          <Formik
            initialValues={{ email: '', password: '' }}
            validationSchema={LoginSchema}
            onSubmit={handleSubmit}
          >
            {({ errors, touched, isSubmitting }) => (
              <Form style={{ width: '100%' }}>
                {showAlert && (
                  <Alert severity={alertType} icon={<ErrorOutlineIcon />} sx={{ width: '100%', mb: 2 }}>
                    {alertMessage}
                  </Alert>
                )}
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
                  helperText={touched.email && errors.email ? (
                    <span style={{ color: 'red', display: 'flex', alignItems: 'center' }}><ErrorOutlineIcon fontSize="small" style={{ marginRight: 4 }} />{errors.email}</span>
                  ) : ''}
                  disabled={isSubmitting || isConnectingWebSocket}
                />
                
                <Field
                  as={TextField}
                  margin="normal"
                  fullWidth
                  name="password"
                  label="Password"
                  type="password"
                  id="password"
                  autoComplete="current-password"
                  error={touched.password && Boolean(errors.password)}
                  helperText={touched.password && errors.password ? (
                    <span style={{ color: 'red', display: 'flex', alignItems: 'center' }}><ErrorOutlineIcon fontSize="small" style={{ marginRight: 4 }} />{errors.password}</span>
                  ) : ''}
                  disabled={isSubmitting || isConnectingWebSocket}
                />
                
                <Button
                  type="submit"
                  fullWidth
                  variant="contained"
                  color="primary"
                  disabled={isSubmitting || isConnectingWebSocket}
                  sx={{ mt: 3, mb: 2 }}
                >
                  {isSubmitting ? (
                    <CircularProgress size={24} color="inherit" />
                  ) : isConnectingWebSocket ? (
                    <>
                      <CircularProgress size={24} color="inherit" sx={{ mr: 1 }} />
                      Connecting...
                    </>
                  ) : (
                    'Sign In'
                  )}
                </Button>
                
                <Grid container>
                  <Grid item xs>
                    <Link component={RouterLink} to="/forgot-password" variant="body2">
                      Forgot password?
                    </Link>
                  </Grid>
                  <Grid item>
                    <Link component={RouterLink} to="/register" variant="body2">
                      {"Don't have an account? Sign Up"}
                    </Link>
                  </Grid>
                </Grid>
              </Form>
            )}
          </Formik>
        </Paper>
      </Box>
      
      <Snackbar 
        open={showAlert} 
        autoHideDuration={alertType === 'error' ? 6000 : alertType === 'success' ? 2000 : null}
        onClose={handleCloseAlert}
        anchorOrigin={{ vertical: 'top', horizontal: 'center' }}
      >
        <Alert 
          onClose={handleCloseAlert} 
          severity={alertType}
          variant="filled"
          sx={{ width: '100%' }}
        >
          {alertMessage}
        </Alert>
      </Snackbar>
    </Container>
  );
};

export default LoginPage; 