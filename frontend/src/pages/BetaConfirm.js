import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  Box,
  Container,
  Typography,
  CircularProgress,
  Button,
  Paper,
  Divider
} from '@mui/material';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import ErrorIcon from '@mui/icons-material/Error';
import EmailSubscription from '../components/EmailSubscription';
import axios from 'axios';

const BetaConfirm = () => {
  const { token } = useParams();
  const navigate = useNavigate();
  const [status, setStatus] = useState('loading'); // loading, success, error
  const [confirmedEmail, setConfirmedEmail] = useState('');

  useEffect(() => {
    const confirmEmail = async () => {
      try {
        // First try to use the backend API
        try {
          const response = await axios.get(`/api/beta/confirm/${token}`);
          console.log('Confirmation response:', response.data);
          
          // Extract email from response if available
          if (response.data && response.data.email) {
            setConfirmedEmail(response.data.email);
          } else {
            // Try to find email in localStorage as a fallback
            const pendingConfirmation = JSON.parse(localStorage.getItem('pendingConfirmation'));
            if (pendingConfirmation && pendingConfirmation.email) {
              setConfirmedEmail(pendingConfirmation.email);
            }
          }
          
          setStatus('success');
          return;
        } catch (apiError) {
          console.warn('API confirmation failed, using localStorage fallback:', apiError);
          
          // Fall back to localStorage approach
          // Mock API response for testing
          // Simulate API delay
          await new Promise(resolve => setTimeout(resolve, 800));
          
          console.log(`Confirming email with token: ${token}`);
          
          // Check localStorage for pending confirmation
          const pendingConfirmation = JSON.parse(localStorage.getItem('pendingConfirmation'));
          
          if (pendingConfirmation && pendingConfirmation.token === token) {
            // Confirmation successful
            console.log(`Confirmed email: ${pendingConfirmation.email}`);
            
            // Store in localStorage as confirmed
            localStorage.setItem('confirmedUser', JSON.stringify({
              ...pendingConfirmation,
              confirmedAt: new Date().toISOString()
            }));
            
            // Save email for subscription form
            setConfirmedEmail(pendingConfirmation.email);
            
            // Remove pending confirmation
            localStorage.removeItem('pendingConfirmation');
            
            setStatus('success');
          } else {
            console.error('Invalid or expired token');
            setStatus('error');
          }
        }
      } catch (error) {
        console.error('Confirmation error:', error);
        setStatus('error');
      }
    };

    confirmEmail();
  }, [token]);

  return (
    <Box
      sx={{
        minHeight: '100vh',
        display: 'flex',
        alignItems: 'center',
        bgcolor: 'background.default',
        py: 4
      }}
    >
      <Container maxWidth="md">
        {status === 'loading' && (
          <Paper
            elevation={3}
            sx={{
              p: 4,
              textAlign: 'center',
              borderRadius: 2
            }}
          >
            <CircularProgress size={60} sx={{ mb: 3 }} />
            <Typography variant="h5" gutterBottom>
              Confirming your email...
            </Typography>
          </Paper>
        )}

        {status === 'success' && (
          <Box>
            <Paper
              elevation={3}
              sx={{
                p: 4,
                textAlign: 'center',
                borderRadius: 2,
                mb: 4
              }}
            >
              <CheckCircleIcon
                color="success"
                sx={{ fontSize: 60, mb: 3 }}
              />
              <Typography variant="h5" gutterBottom>
                Email Confirmed!
              </Typography>
              <Typography color="text.secondary" paragraph>
                Thank you for confirming your email. You'll be among the first to know when the beta is ready.
              </Typography>
              <Button
                variant="contained"
                onClick={() => navigate('/')}
                sx={{ mt: 2 }}
              >
                Return to Home
              </Button>
            </Paper>
            
            <Divider sx={{ my: 4 }} />
            
            {/* Email Subscription Component */}
            <Typography variant="h5" align="center" gutterBottom>
              Stay in the loop!
            </Typography>
            <Typography variant="body1" align="center" color="text.secondary" paragraph>
              Choose what updates you'd like to receive from us
            </Typography>
            <EmailSubscription prefilledEmail={confirmedEmail} />
          </Box>
        )}

        {status === 'error' && (
          <Paper
            elevation={3}
            sx={{
              p: 4,
              textAlign: 'center',
              borderRadius: 2
            }}
          >
            <ErrorIcon
              color="error"
              sx={{ fontSize: 60, mb: 3 }}
            />
            <Typography variant="h5" gutterBottom>
              Confirmation Failed
            </Typography>
            <Typography color="text.secondary" paragraph>
              The confirmation link appears to be invalid or has expired.
            </Typography>
            <Button
              variant="contained"
              onClick={() => navigate('/')}
              sx={{ mt: 2 }}
            >
              Return to Home
            </Button>
          </Paper>
        )}
      </Container>
    </Box>
  );
};

export default BetaConfirm; 