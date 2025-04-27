import React, { useState, useEffect } from 'react';
import { 
  Container, 
  Box, 
  Typography, 
  TextField, 
  Button, 
  Paper,
  Grid,
  Alert,
  Snackbar,
  Divider,
  Avatar,
  Tabs,
  Tab,
  Switch,
  FormGroup,
  FormControlLabel,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  IconButton,
  List,
  ListItem,
  ListItemText,
  ListItemSecondaryAction,
  ListItemIcon,
  Chip
} from '@mui/material';
import { Formik, Form, Field } from 'formik';
import * as Yup from 'yup';
import { useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import PersonIcon from '@mui/icons-material/Person';
import LockIcon from '@mui/icons-material/Lock';
import NotificationsIcon from '@mui/icons-material/Notifications';
import DeleteIcon from '@mui/icons-material/Delete';
import SecurityIcon from '@mui/icons-material/Security';
import EmailIcon from '@mui/icons-material/Email';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import InfoIcon from '@mui/icons-material/Info';
import WarningIcon from '@mui/icons-material/Warning';
import ErrorIcon from '@mui/icons-material/Error';
import axios from 'axios';
import { API_URL } from '../config';

// Validation schema for profile update
const ProfileSchema = Yup.object().shape({
  username: Yup.string()
    .required('Username is required')
    .min(3, 'Username must be at least 3 characters')
    .max(50, 'Username must be less than 50 characters'),
  email: Yup.string()
    .email('Invalid email')
    .required('Email is required'),
  firstName: Yup.string(),
  lastName: Yup.string(),
});

// Validation schema for password change
const PasswordSchema = Yup.object().shape({
  currentPassword: Yup.string()
    .required('Current password is required'),
  newPassword: Yup.string()
    .required('New password is required')
    .min(8, 'Password must be at least 8 characters')
    .matches(
      /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]/,
      'Password must contain at least one uppercase letter, one lowercase letter, one number, and one special character'
    ),
  confirmPassword: Yup.string()
    .oneOf([Yup.ref('newPassword'), null], 'Passwords must match')
    .required('Confirm password is required'),
});

// TabPanel component for displaying tab content
function TabPanel(props) {
  const { children, value, index, ...other } = props;

  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`profile-tabpanel-${index}`}
      aria-labelledby={`profile-tab-${index}`}
      {...other}
    >
      {value === index && (
        <Box sx={{ pt: 3 }}>
          {children}
        </Box>
      )}
    </div>
  );
}

// Get notification icon based on type
const getNotificationIcon = (type) => {
  switch (type) {
    case 'success':
      return <CheckCircleIcon color="success" />;
    case 'warning':
      return <WarningIcon color="warning" />;
    case 'error':
      return <ErrorIcon color="error" />;
    case 'info':
    default:
      return <InfoIcon color="info" />;
  }
};

const formatNotificationTime = (timestamp) => {
  if (!timestamp) return 'Unknown time';
  
  try {
    const date = new Date(timestamp);
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  } catch (e) {
    return 'Unknown time';
  }
};

const ProfilePage = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { currentUser, updateProfile, logout } = useAuth();
  const [error, setError] = useState('');
  const [message, setMessage] = useState('');
  const [showAlert, setShowAlert] = useState(false);
  const [alertType, setAlertType] = useState('success');
  const [tabValue, setTabValue] = useState(0);
  const [notificationSettings, setNotificationSettings] = useState({
    emailNotifications: true,
    pushNotifications: true,
    caseUpdates: true,
    formSubmissions: true,
    documentRequests: true,
    appointments: true,
    messages: true
  });
  const [notifications, setNotifications] = useState([]);
  const [loadingNotifications, setLoadingNotifications] = useState(false);

  useEffect(() => {
    // Check for tab param in URL
    const params = new URLSearchParams(location.search);
    const tab = params.get('tab');
    if (tab === 'notifications') {
      setTabValue(2);
    }
    
    // Fetch notification settings
    const fetchNotificationSettings = async () => {
      try {
        const response = await axios.get(`${API_URL}/api/users/notification-settings`, {
          headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` }
        });
        
        if (response.data && response.data.settings) {
          setNotificationSettings(response.data.settings);
        }
      } catch (error) {
        console.error('Error fetching notification settings:', error);
        // Use default settings if fetch fails
      }
    };
    
    // Fetch notifications
    const fetchNotifications = async () => {
      try {
        setLoadingNotifications(true);
        const response = await axios.get(`${API_URL}/api/notifications`, {
          headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` }
        });
        
        if (response.data && Array.isArray(response.data.notifications)) {
          setNotifications(response.data.notifications);
        } else {
          // Use fallback data for development/demo purposes
          setNotifications([
            {
              _id: '1',
              title: 'Form Submitted',
              message: 'Your immigration form has been submitted successfully.',
              type: 'success',
              isRead: true,
              createdAt: new Date(Date.now() - 2 * 86400000).toISOString()
            },
            {
              _id: '2',
              title: 'Documents Required',
              message: 'Please upload your identification documents for your immigration case.',
              type: 'warning',
              isRead: true,
              createdAt: new Date(Date.now() - 3 * 86400000).toISOString()
            },
            {
              _id: '3',
              title: 'Case Status Updated',
              message: 'Your case status has been updated to "In Progress".',
              type: 'info',
              isRead: true,
              createdAt: new Date(Date.now() - 5 * 86400000).toISOString()
            }
          ]);
        }
      } catch (error) {
        console.error('Error fetching notifications:', error);
        // Use fallback data
        setNotifications([]);
      } finally {
        setLoadingNotifications(false);
      }
    };
    
    if (currentUser) {
      fetchNotificationSettings();
      fetchNotifications();
    }
  }, [currentUser, location.search]);

  if (!currentUser) {
    navigate('/login');
    return null;
  }

  const handleProfileUpdate = async (values, { setSubmitting }) => {
    try {
      const { success, error } = await updateProfile(values);
      
      if (success) {
        setMessage('Profile updated successfully');
        setAlertType('success');
      } else {
        setMessage(error);
        setAlertType('error');
      }
      
      setShowAlert(true);
    } catch (error) {
      setMessage('An error occurred. Please try again.');
      setAlertType('error');
      setShowAlert(true);
    } finally {
      setSubmitting(false);
    }
  };

  const handlePasswordChange = async (values, { setSubmitting, resetForm }) => {
    try {
      const { currentPassword, newPassword } = values;
      const { success, error } = await updateProfile({
        current_password: currentPassword,
        password: newPassword
      });
      
      if (success) {
        setMessage('Password updated successfully');
        setAlertType('success');
        resetForm();
      } else {
        setMessage(error);
        setAlertType('error');
      }
      
      setShowAlert(true);
    } catch (error) {
      setMessage('An error occurred. Please try again.');
      setAlertType('error');
      setShowAlert(true);
    } finally {
      setSubmitting(false);
    }
  };

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const handleCloseAlert = () => {
    setShowAlert(false);
  };

  const getInitials = () => {
    if (!currentUser) return '?';
    
    if (currentUser.first_name && currentUser.last_name) {
      return `${currentUser.first_name.charAt(0)}${currentUser.last_name.charAt(0)}`;
    } else if (currentUser.username) {
      return currentUser.username.charAt(0).toUpperCase();
    } else {
      return '?';
    }
  };

  const handleTabChange = (event, newValue) => {
    setTabValue(newValue);
  };

  const handleNotificationSettingChange = async (event) => {
    const { name, checked } = event.target;
    
    // Update UI immediately for better UX
    setNotificationSettings(prev => ({
      ...prev,
      [name]: checked
    }));
    
    // Save to server
    try {
      await axios.put(`${API_URL}/api/users/notification-settings`, 
        { [name]: checked },
        { headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` } }
      );
    } catch (error) {
      console.error('Error updating notification settings:', error);
      // Revert the setting if server update fails
      setNotificationSettings(prev => ({
        ...prev,
        [name]: !checked
      }));
      setMessage('Failed to update notification settings');
      setAlertType('error');
      setShowAlert(true);
    }
  };

  const clearAllNotifications = async () => {
    try {
      await axios.delete(`${API_URL}/api/notifications/clear-all`, {
        headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` }
      });
      
      setNotifications([]);
      setMessage('All notifications cleared');
      setAlertType('success');
      setShowAlert(true);
    } catch (error) {
      console.error('Error clearing notifications:', error);
      setMessage('Failed to clear notifications');
      setAlertType('error');
      setShowAlert(true);
    }
  };

  const deleteNotification = async (notificationId) => {
    try {
      await axios.delete(`${API_URL}/api/notifications/${notificationId}`, {
        headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` }
      });
      
      // Update UI
      setNotifications(prev => prev.filter(n => n._id !== notificationId));
    } catch (error) {
      console.error('Error deleting notification:', error);
      setMessage('Failed to delete notification');
      setAlertType('error');
      setShowAlert(true);
    }
  };

  return (
    <Container maxWidth="md">
      <Box
        sx={{
          marginTop: 4,
          marginBottom: 8,
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
        }}
      >
        <Paper
          elevation={3}
          sx={{
            padding: 4,
            width: '100%',
          }}
        >
          <Box 
            sx={{ 
              display: 'flex', 
              alignItems: 'center', 
              justifyContent: 'center',
              flexDirection: 'column',
              mb: 4 
            }}
          >
            <Avatar 
              sx={{ 
                width: 100, 
                height: 100, 
                bgcolor: 'primary.main',
                fontSize: '2.5rem',
                mb: 2
              }}
            >
              {getInitials()}
            </Avatar>
            <Typography component="h1" variant="h4">
              {currentUser.first_name && currentUser.last_name 
                ? `${currentUser.first_name} ${currentUser.last_name}` 
                : currentUser.username}
            </Typography>
            <Typography color="textSecondary">
              {currentUser.role && (currentUser.role.charAt(0).toUpperCase() + currentUser.role.slice(1))}
            </Typography>
          </Box>

          <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
            <Tabs 
              value={tabValue} 
              onChange={handleTabChange} 
              aria-label="profile tabs"
              variant="scrollable"
              scrollButtons="auto"
            >
              <Tab 
                label="Profile Information" 
                icon={<PersonIcon />} 
                iconPosition="start"
              />
              <Tab 
                label="Security" 
                icon={<LockIcon />} 
                iconPosition="start"
              />
              <Tab 
                label="Notifications" 
                icon={<NotificationsIcon />} 
                iconPosition="start"
              />
            </Tabs>
          </Box>

          <TabPanel value={tabValue} index={0}>
            <Typography component="h2" variant="h6" gutterBottom>
              Profile Information
            </Typography>
            
            <Formik
              initialValues={{ 
                username: currentUser.username || '',
                email: currentUser.email || '',
                firstName: currentUser.first_name || '',
                lastName: currentUser.last_name || ''
              }}
              validationSchema={ProfileSchema}
              onSubmit={handleProfileUpdate}
            >
              {({ errors, touched, isSubmitting }) => (
                <Form>
                  <Grid container spacing={2}>
                    <Grid item xs={12} sm={6}>
                      <Field
                        as={TextField}
                        margin="normal"
                        fullWidth
                        id="firstName"
                        label="First Name"
                        name="firstName"
                        autoComplete="given-name"
                        error={touched.firstName && Boolean(errors.firstName)}
                        helperText={touched.firstName && errors.firstName}
                      />
                    </Grid>
                    <Grid item xs={12} sm={6}>
                      <Field
                        as={TextField}
                        margin="normal"
                        fullWidth
                        id="lastName"
                        label="Last Name"
                        name="lastName"
                        autoComplete="family-name"
                        error={touched.lastName && Boolean(errors.lastName)}
                        helperText={touched.lastName && errors.lastName}
                      />
                    </Grid>
                  </Grid>
                  
                  <Field
                    as={TextField}
                    margin="normal"
                    fullWidth
                    id="username"
                    label="Username"
                    name="username"
                    autoComplete="username"
                    error={touched.username && Boolean(errors.username)}
                    helperText={touched.username && errors.username}
                  />
                  
                  <Field
                    as={TextField}
                    margin="normal"
                    fullWidth
                    id="email"
                    label="Email Address"
                    name="email"
                    autoComplete="email"
                    error={touched.email && Boolean(errors.email)}
                    helperText={touched.email && errors.email}
                  />
                  
                  <Button
                    type="submit"
                    variant="contained"
                    color="primary"
                    disabled={isSubmitting}
                    sx={{ mt: 3, mb: 2 }}
                  >
                    {isSubmitting ? 'Updating...' : 'Update Profile'}
                  </Button>
                </Form>
              )}
            </Formik>
          </TabPanel>

          <TabPanel value={tabValue} index={1}>
            <Typography component="h2" variant="h6" gutterBottom>
              Change Password
            </Typography>
            
            <Formik
              initialValues={{ 
                currentPassword: '',
                newPassword: '',
                confirmPassword: ''
              }}
              validationSchema={PasswordSchema}
              onSubmit={handlePasswordChange}
            >
              {({ errors, touched, isSubmitting }) => (
                <Form>
                  <Field
                    as={TextField}
                    margin="normal"
                    fullWidth
                    name="currentPassword"
                    label="Current Password"
                    type="password"
                    id="currentPassword"
                    error={touched.currentPassword && Boolean(errors.currentPassword)}
                    helperText={touched.currentPassword && errors.currentPassword}
                  />
                  
                  <Field
                    as={TextField}
                    margin="normal"
                    fullWidth
                    name="newPassword"
                    label="New Password"
                    type="password"
                    id="newPassword"
                    error={touched.newPassword && Boolean(errors.newPassword)}
                    helperText={touched.newPassword && errors.newPassword}
                  />
                  
                  <Field
                    as={TextField}
                    margin="normal"
                    fullWidth
                    name="confirmPassword"
                    label="Confirm New Password"
                    type="password"
                    id="confirmPassword"
                    error={touched.confirmPassword && Boolean(errors.confirmPassword)}
                    helperText={touched.confirmPassword && errors.confirmPassword}
                  />
                  
                  <Button
                    type="submit"
                    variant="contained"
                    color="primary"
                    disabled={isSubmitting}
                    sx={{ mt: 3, mb: 2 }}
                  >
                    {isSubmitting ? 'Updating...' : 'Change Password'}
                  </Button>
                </Form>
              )}
            </Formik>
          </TabPanel>

          <TabPanel value={tabValue} index={2}>
            <Box sx={{ mb: 4 }}>
              <Typography component="h2" variant="h6" gutterBottom>
                Notification Preferences
              </Typography>
              
              <FormGroup>
                <Grid container spacing={2}>
                  <Grid item xs={12} sm={6}>
                    <FormControlLabel
                      control={
                        <Switch
                          checked={notificationSettings.emailNotifications}
                          onChange={handleNotificationSettingChange}
                          name="emailNotifications"
                          color="primary"
                        />
                      }
                      label="Email Notifications"
                    />
                    <Typography variant="caption" color="text.secondary" sx={{ display: 'block', ml: 2 }}>
                      Receive notifications via email
                    </Typography>
                  </Grid>
                  
                  <Grid item xs={12} sm={6}>
                    <FormControlLabel
                      control={
                        <Switch
                          checked={notificationSettings.pushNotifications}
                          onChange={handleNotificationSettingChange}
                          name="pushNotifications"
                          color="primary"
                        />
                      }
                      label="In-App Notifications"
                      sx={{ mb: 1 }}
                    />
                    <Typography variant="caption" color="text.secondary" sx={{ display: 'block', ml: 2 }}>
                      Receive notifications in the app
                    </Typography>
                  </Grid>
                </Grid>
                
                <Divider sx={{ my: 3 }} />
                <Typography variant="subtitle1" gutterBottom>
                  Notification Types
                </Typography>
                
                <Grid container spacing={2}>
                  <Grid item xs={12} sm={6}>
                    <FormControlLabel
                      control={
                        <Switch
                          checked={notificationSettings.caseUpdates}
                          onChange={handleNotificationSettingChange}
                          name="caseUpdates"
                          color="primary"
                        />
                      }
                      label="Case Updates"
                    />
                  </Grid>
                  
                  <Grid item xs={12} sm={6}>
                    <FormControlLabel
                      control={
                        <Switch
                          checked={notificationSettings.formSubmissions}
                          onChange={handleNotificationSettingChange}
                          name="formSubmissions"
                          color="primary"
                        />
                      }
                      label="Form Submissions"
                    />
                  </Grid>
                  
                  <Grid item xs={12} sm={6}>
                    <FormControlLabel
                      control={
                        <Switch
                          checked={notificationSettings.documentRequests}
                          onChange={handleNotificationSettingChange}
                          name="documentRequests"
                          color="primary"
                        />
                      }
                      label="Document Requests"
                    />
                  </Grid>
                  
                  <Grid item xs={12} sm={6}>
                    <FormControlLabel
                      control={
                        <Switch
                          checked={notificationSettings.appointments}
                          onChange={handleNotificationSettingChange}
                          name="appointments"
                          color="primary"
                        />
                      }
                      label="Appointments & Deadlines"
                    />
                  </Grid>
                  
                  <Grid item xs={12} sm={6}>
                    <FormControlLabel
                      control={
                        <Switch
                          checked={notificationSettings.messages}
                          onChange={handleNotificationSettingChange}
                          name="messages"
                          color="primary"
                        />
                      }
                      label="Messages"
                    />
                  </Grid>
                </Grid>
              </FormGroup>
            </Box>
            
            <Divider sx={{ my: 4 }} />
            
            <Box sx={{ mb: 2, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <Typography component="h2" variant="h6">
                Notification History
              </Typography>
              
              {notifications.length > 0 && (
                <Button 
                  variant="outlined" 
                  size="small" 
                  color="error"
                  onClick={clearAllNotifications}
                >
                  Clear All
                </Button>
              )}
            </Box>
            
            {notifications.length === 0 ? (
              <Box sx={{ py: 3, textAlign: 'center' }}>
                <NotificationsIcon sx={{ fontSize: 48, color: 'text.secondary', mb: 1 }} />
                <Typography color="text.secondary">
                  No notifications in your history
                </Typography>
              </Box>
            ) : (
              <List>
                {notifications.map((notification) => (
                  <ListItem
                    key={notification._id}
                    sx={{
                      mb: 1,
                      borderLeft: '4px solid',
                      borderColor: 
                        notification.type === 'success' ? 'success.main' :
                        notification.type === 'warning' ? 'warning.main' :
                        notification.type === 'error' ? 'error.main' : 'info.main',
                      bgcolor: 'background.paper',
                      boxShadow: 1
                    }}
                  >
                    <ListItemIcon>
                      {getNotificationIcon(notification.type)}
                    </ListItemIcon>
                    <ListItemText
                      primary={
                        <Box sx={{ display: 'flex', alignItems: 'center' }}>
                          <Typography variant="subtitle1">
                            {notification.title}
                          </Typography>
                          {!notification.isRead && (
                            <Chip 
                              label="Unread" 
                              color="error" 
                              size="small" 
                              sx={{ ml: 1, height: 20 }}
                            />
                          )}
                        </Box>
                      }
                      secondary={
                        <>
                          <Typography variant="body2">
                            {notification.message}
                          </Typography>
                          <Typography variant="caption" color="text.secondary">
                            {formatNotificationTime(notification.createdAt)}
                          </Typography>
                        </>
                      }
                    />
                    <ListItemSecondaryAction>
                      <IconButton 
                        edge="end" 
                        aria-label="delete"
                        onClick={() => deleteNotification(notification._id)}
                      >
                        <DeleteIcon fontSize="small" />
                      </IconButton>
                    </ListItemSecondaryAction>
                  </ListItem>
                ))}
              </List>
            )}
          </TabPanel>
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
          sx={{ width: '100%' }}
        >
          {message}
        </Alert>
      </Snackbar>
    </Container>
  );
};

export default ProfilePage; 