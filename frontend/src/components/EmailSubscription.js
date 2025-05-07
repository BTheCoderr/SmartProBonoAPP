import React, { useState } from 'react';
import {
  Box,
  Typography,
  TextField,
  Button,
  Checkbox,
  FormControlLabel,
  Paper,
  Snackbar,
  Alert,
  CircularProgress,
  useTheme
} from '@mui/material';
import { motion } from 'framer-motion';
import MailOutlineIcon from '@mui/icons-material/MailOutline';
import axios from 'axios';

const EmailSubscription = ({ prefilledEmail = '' }) => {
  const [email, setEmail] = useState(prefilledEmail);
  const [preferences, setPreferences] = useState({
    productUpdates: true,
    legalNews: false,
    tips: true
  });
  const [loading, setLoading] = useState(false);
  const [snackbar, setSnackbar] = useState({ open: false, message: '', severity: 'success' });
  const theme = useTheme();

  const handleSubscribe = async (event) => {
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
      const response = await axios.post('/api/beta/subscribe', {
        email,
        preferences
      });
      
      console.log('Subscription response:', response.data);
      
      setSnackbar({
        open: true,
        message: 'Successfully subscribed to updates!',
        severity: 'success'
      });
      
    } catch (error) {
      // If the API fails, fall back to localStorage
      console.warn('API call failed, using localStorage fallback:', error);
      
      try {
        // In a real app, this would call an API endpoint
        console.log('Email subscription:', {
          email,
          preferences
        });

        // Store in localStorage for demo purposes
        localStorage.setItem('emailSubscription', JSON.stringify({
          email,
          preferences,
          subscribedAt: new Date().toISOString()
        }));

        setSnackbar({
          open: true,
          message: 'Successfully subscribed to updates!',
          severity: 'success'
        });
      } catch (fallbackError) {
        console.error('Subscription error:', fallbackError);
        setSnackbar({
          open: true,
          message: 'Failed to subscribe. Please try again.',
          severity: 'error'
        });
      }
    } finally {
      setLoading(false);
    }
  };

  const handlePreferenceChange = (event) => {
    setPreferences({
      ...preferences,
      [event.target.name]: event.target.checked
    });
  };

  return (
    <Paper 
      component={motion.div}
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      elevation={2} 
      sx={{ 
        p: 3, 
        borderRadius: 2,
        backgroundColor: 'rgba(255, 255, 255, 0.95)',
        backdropFilter: 'blur(10px)',
        border: `1px solid ${theme.palette.divider}`,
      }}
    >
      <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
        <MailOutlineIcon color="primary" sx={{ mr: 1 }} />
        <Typography variant="h5" fontWeight="bold">
          Stay Updated
        </Typography>
      </Box>
      
      <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
        Subscribe to our newsletter to receive important updates, legal insights, and helpful resources.
      </Typography>
      
      <Box component="form" onSubmit={handleSubscribe}>
        <TextField
          fullWidth
          placeholder="Your email address"
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
          variant="outlined"
          disabled={loading}
          sx={{ mb: 2 }}
        />
        
        <Typography variant="subtitle2" sx={{ mb: 1 }}>
          I'd like to receive:
        </Typography>
        
        <Box sx={{ mb: 3 }}>
          <FormControlLabel
            control={
              <Checkbox 
                checked={preferences.productUpdates} 
                onChange={handlePreferenceChange}
                name="productUpdates"
                color="primary"
              />
            }
            label="Product updates and new features"
          />
          
          <FormControlLabel
            control={
              <Checkbox 
                checked={preferences.legalNews} 
                onChange={handlePreferenceChange}
                name="legalNews"
                color="primary"
              />
            }
            label="Legal news and insights"
          />
          
          <FormControlLabel
            control={
              <Checkbox 
                checked={preferences.tips} 
                onChange={handlePreferenceChange}
                name="tips"
                color="primary"
              />
            }
            label="Tips and best practices"
          />
        </Box>
        
        <Button
          type="submit"
          variant="contained"
          color="primary"
          fullWidth
          disabled={loading}
          sx={{ py: 1.5 }}
        >
          {loading ? <CircularProgress size={24} color="inherit" /> : 'Subscribe'}
        </Button>
        
        <Typography variant="caption" color="text.secondary" sx={{ mt: 2, display: 'block', textAlign: 'center' }}>
          We respect your privacy and will never share your information.
          You can unsubscribe at any time.
        </Typography>
      </Box>
      
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
    </Paper>
  );
};

export default EmailSubscription; 