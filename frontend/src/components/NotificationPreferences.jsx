import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  FormGroup,
  FormControlLabel,
  Switch,
  Card,
  CardContent,
  CardHeader,
  Divider,
  Button,
  Alert,
  Snackbar,
  Grid,
  CircularProgress
} from '@mui/material';
import { useNotification } from '../contexts/NotificationContext';
import { useAuth } from '../contexts/AuthContext';
import axios from 'axios';
import config from '../config';

const NotificationPreferences = () => {
  const { isAuthenticated, getToken } = useAuth();
  const [preferences, setPreferences] = useState({
    email: {
      caseUpdates: true,
      documentUpdates: true,
      appointmentReminders: true,
      newMessages: true,
      legalAIResponses: true,
      systemAnnouncements: true
    },
    inApp: {
      caseUpdates: true,
      documentUpdates: true,
      appointmentReminders: true,
      newMessages: true,
      legalAIResponses: true,
      systemAnnouncements: true
    },
    browser: {
      caseUpdates: true,
      documentUpdates: true,
      appointmentReminders: true,
      newMessages: true,
      legalAIResponses: true,
      systemAnnouncements: false
    }
  });
  
  const [browserPermissionGranted, setBrowserPermissionGranted] = useState(false);
  const [loading, setLoading] = useState(true);
  const [success, setSuccess] = useState(false);
  const [error, setError] = useState(null);
  
  // Fetch preferences on mount if authenticated
  useEffect(() => {
    if (isAuthenticated) {
      fetchPreferences();
      checkBrowserPermission();
    } else {
      setLoading(false);
    }
  }, [isAuthenticated]);
  
  // Check notification permissions
  const checkBrowserPermission = async () => {
    if ('Notification' in window) {
      const permission = Notification.permission;
      if (permission === 'granted') {
        setBrowserPermissionGranted(true);
      }
    }
  };
  
  // Fetch preferences from the API
  const fetchPreferences = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const token = await getToken();
      
      const response = await axios.get(
        `${config.apiUrl}/api/notifications/preferences`,
        {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        }
      );
      
      // Update state with fetched preferences
      if (response.data) {
        setPreferences(response.data);
      }
      
      setLoading(false);
    } catch (err) {
      setError('Error fetching notification preferences: ' + err.message);
      setLoading(false);
    }
  };
  
  // Handle toggling a preference
  const handleTogglePreference = (category, prefName) => (event) => {
    setPreferences(prev => ({
      ...prev,
      [category]: {
        ...prev[category],
        [prefName]: event.target.checked
      }
    }));
  };
  
  // Request browser notification permission
  const requestBrowserPermission = async () => {
    if (!('Notification' in window)) {
      setError('Browser notifications are not supported in your browser');
      return;
    }
    
    try {
      setError(null);
      const permission = await Notification.requestPermission();
      
      if (permission === 'granted') {
        setBrowserPermissionGranted(true);
        
        try {
          // Update permission status on server
          const token = await getToken();
          await axios.post(
            `${config.apiUrl}/api/notifications/browser-permission`,
            { granted: true },
            {
              headers: {
                'Authorization': `Bearer ${token}`
              }
            }
          );
          
          setSuccess('Browser notification permission granted');
          
          // Enable default browser notification settings
          const updatedPreferences = {
            ...preferences,
            browser: {
              ...preferences.browser,
              caseUpdates: true,
              documentUpdates: true,
              appointmentReminders: true,
              newMessages: true
            }
          };
          
          setPreferences(updatedPreferences);
        } catch (err) {
          console.error('Error updating browser permission on server:', err);
        }
      } else {
        setError('Browser notification permission denied');
        
        try {
          // Update permission status on server
          const token = await getToken();
          await axios.post(
            `${config.apiUrl}/api/notifications/browser-permission`,
            { granted: false },
            {
              headers: {
                'Authorization': `Bearer ${token}`
              }
            }
          );
          
          // Disable all browser notifications
          const updatedPreferences = {
            ...preferences,
            browser: {
              ...preferences.browser,
              caseUpdates: false,
              documentUpdates: false,
              appointmentReminders: false,
              newMessages: false,
              legalAIResponses: false,
              systemAnnouncements: false
            }
          };
          
          setPreferences(updatedPreferences);
        } catch (err) {
          console.error('Error updating browser permission on server:', err);
        }
      }
    } catch (err) {
      console.error('Error requesting notification permission:', err);
      setError('Error requesting notification permission: ' + err.message);
    }
  };
  
  // Save preferences to the server
  const savePreferences = async () => {
    if (!isAuthenticated) {
      setError('You must be logged in to save preferences.');
      return;
    }
    
    try {
      setLoading(true);
      setError(null);
      
      const token = await getToken();
      
      const response = await axios.post(
        `${config.apiUrl}/api/notifications/preferences`,
        preferences,
        {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        }
      );
      
      if (response.data && response.data.message) {
        setSuccess(response.data.message);
      } else {
        setSuccess('Notification preferences saved successfully');
      }
      
      setLoading(false);
    } catch (err) {
      setError(`Error saving preferences: ${err.response?.data?.error || err.message}`);
      setLoading(false);
    }
  };
  
  // Reset preferences to default
  const resetPreferences = () => {
    setPreferences({
      email: {
        caseUpdates: true,
        documentUpdates: true,
        appointmentReminders: true,
        newMessages: true,
        legalAIResponses: true,
        systemAnnouncements: true
      },
      inApp: {
        caseUpdates: true,
        documentUpdates: true,
        appointmentReminders: true,
        newMessages: true,
        legalAIResponses: true,
        systemAnnouncements: true
      },
      browser: {
        caseUpdates: true,
        documentUpdates: true,
        appointmentReminders: true,
        newMessages: true,
        legalAIResponses: false,
        systemAnnouncements: false
      }
    });
  };
  
  // Close success snackbar
  const handleCloseSuccess = () => {
    setSuccess(null);
  };
  
  // Close error snackbar
  const handleCloseError = () => {
    setError(null);
  };
  
  if (!isAuthenticated) {
    return (
      <Box mt={4}>
        <Alert severity="warning">
          You need to be logged in to manage notification preferences.
        </Alert>
      </Box>
    );
  }
  
  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', my: 4 }}>
        <CircularProgress />
      </Box>
    );
  }
  
  return (
    <Box>
      <Typography variant="h5" gutterBottom>
        Notification Preferences
      </Typography>
      
      <Typography variant="body2" color="text.secondary" paragraph>
        Manage how you receive notifications from the Smart Pro Bono platform.
      </Typography>
      
      <Grid container spacing={3} mt={1}>
        {/* In-App Notifications */}
        <Grid item xs={12} md={4}>
          <Card>
            <CardHeader title="In-App Notifications" />
            <Divider />
            <CardContent>
              <Typography variant="body2" color="text.secondary" paragraph>
                These notifications appear in the notification center within the application.
              </Typography>
              
              <FormGroup>
                <FormControlLabel
                  control={<Switch checked={preferences.inApp.caseUpdates} onChange={handleTogglePreference('inApp', 'caseUpdates')} />}
                  label="Case Updates"
                />
                <FormControlLabel
                  control={<Switch checked={preferences.inApp.documentUpdates} onChange={handleTogglePreference('inApp', 'documentUpdates')} />}
                  label="Document Updates"
                />
                <FormControlLabel
                  control={<Switch checked={preferences.inApp.appointmentReminders} onChange={handleTogglePreference('inApp', 'appointmentReminders')} />}
                  label="Appointment Reminders"
                />
                <FormControlLabel
                  control={<Switch checked={preferences.inApp.newMessages} onChange={handleTogglePreference('inApp', 'newMessages')} />}
                  label="New Messages"
                />
                <FormControlLabel
                  control={<Switch checked={preferences.inApp.legalAIResponses} onChange={handleTogglePreference('inApp', 'legalAIResponses')} />}
                  label="Legal AI Responses"
                />
                <FormControlLabel
                  control={<Switch checked={preferences.inApp.systemAnnouncements} onChange={handleTogglePreference('inApp', 'systemAnnouncements')} />}
                  label="System Announcements"
                />
              </FormGroup>
            </CardContent>
          </Card>
        </Grid>
        
        {/* Email Notifications */}
        <Grid item xs={12} md={4}>
          <Card>
            <CardHeader title="Email Notifications" />
            <Divider />
            <CardContent>
              <Typography variant="body2" color="text.secondary" paragraph>
                These notifications are sent to your email address.
              </Typography>
              
              <FormGroup>
                <FormControlLabel
                  control={<Switch checked={preferences.email.caseUpdates} onChange={handleTogglePreference('email', 'caseUpdates')} />}
                  label="Case Updates"
                />
                <FormControlLabel
                  control={<Switch checked={preferences.email.documentUpdates} onChange={handleTogglePreference('email', 'documentUpdates')} />}
                  label="Document Updates"
                />
                <FormControlLabel
                  control={<Switch checked={preferences.email.appointmentReminders} onChange={handleTogglePreference('email', 'appointmentReminders')} />}
                  label="Appointment Reminders"
                />
                <FormControlLabel
                  control={<Switch checked={preferences.email.newMessages} onChange={handleTogglePreference('email', 'newMessages')} />}
                  label="New Messages"
                />
                <FormControlLabel
                  control={<Switch checked={preferences.email.legalAIResponses} onChange={handleTogglePreference('email', 'legalAIResponses')} />}
                  label="Legal AI Responses"
                />
                <FormControlLabel
                  control={<Switch checked={preferences.email.systemAnnouncements} onChange={handleTogglePreference('email', 'systemAnnouncements')} />}
                  label="System Announcements"
                />
              </FormGroup>
            </CardContent>
          </Card>
        </Grid>
        
        {/* Browser Notifications */}
        <Grid item xs={12} md={4}>
          <Card>
            <CardHeader 
              title="Browser Notifications" 
              action={
                !browserPermissionGranted && (
                  <Button 
                    size="small" 
                    variant="outlined" 
                    onClick={requestBrowserPermission}
                    sx={{ mt: 1 }}
                  >
                    Enable
                  </Button>
                )
              }
            />
            <Divider />
            <CardContent>
              <Typography variant="body2" color="text.secondary" paragraph>
                These notifications appear as desktop notifications when the browser is open.
              </Typography>
              
              {!browserPermissionGranted ? (
                <Alert severity="info" sx={{ mb: 2 }}>
                  Browser notifications are not enabled. Click "Enable" to grant permission.
                </Alert>
              ) : null}
              
              <FormGroup>
                <FormControlLabel
                  control={
                    <Switch 
                      checked={preferences.browser.caseUpdates} 
                      onChange={handleTogglePreference('browser', 'caseUpdates')} 
                      disabled={!browserPermissionGranted}
                    />
                  }
                  label="Case Updates"
                />
                <FormControlLabel
                  control={
                    <Switch 
                      checked={preferences.browser.documentUpdates} 
                      onChange={handleTogglePreference('browser', 'documentUpdates')} 
                      disabled={!browserPermissionGranted}
                    />
                  }
                  label="Document Updates"
                />
                <FormControlLabel
                  control={
                    <Switch 
                      checked={preferences.browser.appointmentReminders} 
                      onChange={handleTogglePreference('browser', 'appointmentReminders')} 
                      disabled={!browserPermissionGranted}
                    />
                  }
                  label="Appointment Reminders"
                />
                <FormControlLabel
                  control={
                    <Switch 
                      checked={preferences.browser.newMessages} 
                      onChange={handleTogglePreference('browser', 'newMessages')} 
                      disabled={!browserPermissionGranted}
                    />
                  }
                  label="New Messages"
                />
                <FormControlLabel
                  control={
                    <Switch 
                      checked={preferences.browser.legalAIResponses} 
                      onChange={handleTogglePreference('browser', 'legalAIResponses')} 
                      disabled={!browserPermissionGranted}
                    />
                  }
                  label="Legal AI Responses"
                />
                <FormControlLabel
                  control={
                    <Switch 
                      checked={preferences.browser.systemAnnouncements} 
                      onChange={handleTogglePreference('browser', 'systemAnnouncements')} 
                      disabled={!browserPermissionGranted}
                    />
                  }
                  label="System Announcements"
                />
              </FormGroup>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
      
      <Box mt={3} display="flex" justifyContent="flex-end">
        <Button 
          variant="outlined" 
          onClick={resetPreferences} 
          sx={{ mr: 2 }}
          disabled={loading}
        >
          Reset to Default
        </Button>
        <Button 
          variant="contained" 
          onClick={savePreferences}
          disabled={loading}
        >
          {loading ? <CircularProgress size={24} /> : "Save Preferences"}
        </Button>
      </Box>
      
      <Snackbar 
        open={!!success} 
        autoHideDuration={6000} 
        onClose={handleCloseSuccess}
      >
        <Alert onClose={handleCloseSuccess} severity="success">
          {success}
        </Alert>
      </Snackbar>
      
      <Snackbar 
        open={!!error} 
        autoHideDuration={6000} 
        onClose={handleCloseError}
      >
        <Alert onClose={handleCloseError} severity="error">
          {error}
        </Alert>
      </Snackbar>
    </Box>
  );
};

export default NotificationPreferences; 