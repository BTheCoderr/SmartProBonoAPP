import React, { useState, useEffect } from 'react';
import {
  Container,
  Typography,
  Paper,
  Box,
  TextField,
  Button,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Grid,
  Alert,
  Divider,
  Card,
  CardContent,
  CardActions,
  Chip,
  Snackbar,
  CircularProgress
} from '@mui/material';
import { useNotification } from '../contexts/NotificationContext';
import { useAuth } from '../contexts/AuthContext';
import notificationService from '../services/notificationService';
import useTestNotification from '../hooks/useTestNotification';

// Generate a unique ID for test notifications
const generateId = () => {
  return `test-${Date.now()}-${Math.floor(Math.random() * 1000)}`;
};

const NotificationTestPage = () => {
  const { notifications, markAsRead, removeNotification } = useNotification();
  const { user } = useAuth();
  const { 
    isLoading, 
    error: hookError, 
    success: hookSuccess, 
    sendTestNotification, 
    sendPresetNotification 
  } = useTestNotification();
  
  // Socket connection status
  const [isConnected, setIsConnected] = useState(false);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  
  // State for form fields
  const [notificationType, setNotificationType] = useState('info');
  const [title, setTitle] = useState('Test Notification');
  const [message, setMessage] = useState('This is a test notification message');
  const [success, setSuccess] = useState(null);
  const [error, setError] = useState(null);
  
  // Check connection status
  useEffect(() => {
    const checkConnection = () => {
      setIsConnected(notificationService.isConnected());
      setIsAuthenticated(notificationService.isAuthenticated());
    };
    
    // Check initial state
    checkConnection();
    
    // Set up listeners
    const unsubscribeConnect = notificationService.onConnect(() => {
      setIsConnected(true);
    });
    
    const unsubscribeDisconnect = notificationService.onDisconnect(() => {
      setIsConnected(false);
      setIsAuthenticated(false);
    });
    
    const unsubscribeAuthenticated = notificationService.onAuthenticated(() => {
      setIsAuthenticated(true);
    });
    
    // Clean up listeners
    return () => {
      unsubscribeConnect();
      unsubscribeDisconnect();
      unsubscribeAuthenticated();
    };
  }, []);
  
  // Effect to show error/success messages from the hook
  useEffect(() => {
    if (hookError) {
      setError(hookError);
      setTimeout(() => setError(null), 5000);
    }
    
    if (hookSuccess) {
      setSuccess('Test notification sent successfully!');
      setTimeout(() => setSuccess(null), 3000);
    }
  }, [hookError, hookSuccess]);
  
  // Handle sending a test notification
  const handleSendNotification = async () => {
    if (!isConnected) {
      setError('WebSocket is not connected. Please connect first.');
      return;
    }
    
    try {
      await sendTestNotification({
        type: notificationType,
        title: title,
        message: message,
        user_id: user?.id
      });
    } catch (err) {
      // Error is handled in the hook and set via useEffect
    }
  };
  
  // Handle connecting to the WebSocket
  const handleConnect = async () => {
    try {
      setError(null);
      await notificationService.connect();
      if (user?.id) {
        await notificationService.authenticate(user.id);
      }
    } catch (err) {
      setError(`Failed to connect: ${err.message}`);
    }
  };
  
  // Handle preset notification types
  const handlePresetNotification = (type) => {
    switch (type) {
      case 'info':
        setNotificationType('info');
        setTitle('Information');
        setMessage('This is an informational notification.');
        break;
      case 'success':
        setNotificationType('success');
        setTitle('Success');
        setMessage('The operation completed successfully.');
        break;
      case 'warning':
        setNotificationType('warning');
        setTitle('Warning');
        setMessage('This action might have consequences.');
        break;
      case 'error':
        setNotificationType('error');
        setTitle('Error');
        setMessage('An error occurred during the operation.');
        break;
      case 'case':
        setNotificationType('info');
        setTitle('Case Status Update');
        setMessage('Your case #12345 status has been updated to "In Progress"');
        break;
      case 'document':
        setNotificationType('success');
        setTitle('Document Ready');
        setMessage('Your requested document "Tenant Rights" is now ready for download');
        break;
      case 'appointment':
        setNotificationType('warning');
        setTitle('Appointment Reminder');
        setMessage('Reminder: You have an appointment with Atty. Smith tomorrow at 10:00 AM');
        break;
      default:
        setNotificationType('info');
        setTitle('System Notification');
        setMessage('This is a system notification');
    }
  };
  
  // Handle quick sending a preset notification
  const handleQuickSend = async (type) => {
    if (!isConnected) {
      setError('WebSocket is not connected. Please connect first.');
      return;
    }
    
    try {
      await sendPresetNotification(type, user?.id);
    } catch (err) {
      // Error is handled in the hook
    }
  };
  
  return (
    <Container maxWidth="lg" sx={{ mt: 12, mb: 4 }}>
      <Typography variant="h4" gutterBottom>
        Notification System Test
      </Typography>
      
      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3, mb: 3 }}>
            <Typography variant="h6" gutterBottom>
              Send Test Notification
            </Typography>
            
            <Box sx={{ display: 'flex', mb: 2, flexWrap: 'wrap', gap: 1 }}>
              <Chip 
                label="Info" 
                onClick={() => handlePresetNotification('info')}
                color={notificationType === 'info' ? 'primary' : 'default'}
              />
              <Chip 
                label="Success" 
                onClick={() => handlePresetNotification('success')}
                color={notificationType === 'success' ? 'primary' : 'default'}
              />
              <Chip 
                label="Warning" 
                onClick={() => handlePresetNotification('warning')}
                color={notificationType === 'warning' ? 'primary' : 'default'}
              />
              <Chip 
                label="Error" 
                onClick={() => handlePresetNotification('error')}
                color={notificationType === 'error' ? 'primary' : 'default'}
              />
              <Chip 
                label="Case Update" 
                onClick={() => handlePresetNotification('case')}
                color={notificationType === 'case' ? 'primary' : 'default'}
              />
              <Chip 
                label="Document" 
                onClick={() => handlePresetNotification('document')}
                color={notificationType === 'document' ? 'primary' : 'default'}
              />
              <Chip 
                label="Appointment" 
                onClick={() => handlePresetNotification('appointment')}
                color={notificationType === 'appointment' ? 'primary' : 'default'}
              />
            </Box>
            
            <FormControl fullWidth margin="normal">
              <InputLabel id="notification-type-label">Notification Type</InputLabel>
              <Select
                labelId="notification-type-label"
                id="notification-type"
                value={notificationType}
                label="Notification Type"
                onChange={(e) => setNotificationType(e.target.value)}
              >
                <MenuItem value="info">Info</MenuItem>
                <MenuItem value="success">Success</MenuItem>
                <MenuItem value="warning">Warning</MenuItem>
                <MenuItem value="error">Error</MenuItem>
              </Select>
            </FormControl>
            
            <TextField
              fullWidth
              label="Notification Title"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              margin="normal"
            />
            
            <TextField
              fullWidth
              label="Notification Message"
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              margin="normal"
              multiline
              rows={3}
            />
            
            <Button 
              variant="contained" 
              color="primary" 
              fullWidth 
              sx={{ mt: 2 }}
              onClick={handleSendNotification}
              disabled={!isConnected || isLoading}
            >
              {isLoading ? <CircularProgress size={24} /> : 'Send Test Notification'}
            </Button>
            
            {!isConnected && (
              <Alert severity="warning" sx={{ mt: 2 }}>
                WebSocket is not connected. Please connect to use this feature.
                <Button 
                  size="small" 
                  onClick={handleConnect} 
                  sx={{ ml: 1 }}
                >
                  Connect
                </Button>
              </Alert>
            )}
          </Paper>
          
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Quick Send
            </Typography>
            
            <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1, mb: 2 }}>
              <Button 
                variant="outlined" 
                onClick={() => handleQuickSend('info')}
                disabled={!isConnected || isLoading}
              >
                Info
              </Button>
              <Button 
                variant="outlined" 
                color="success"
                onClick={() => handleQuickSend('success')}
                disabled={!isConnected || isLoading}
              >
                Success
              </Button>
              <Button 
                variant="outlined" 
                color="warning"
                onClick={() => handleQuickSend('warning')}
                disabled={!isConnected || isLoading}
              >
                Warning
              </Button>
              <Button 
                variant="outlined" 
                color="error"
                onClick={() => handleQuickSend('error')}
                disabled={!isConnected || isLoading}
              >
                Error
              </Button>
            </Box>
            
            <Divider sx={{ my: 2 }} />
            
            <Typography variant="h6" gutterBottom>
              Connection Status
            </Typography>
            
            <Box sx={{ display: 'flex', gap: 1, mb: 2 }}>
              <Alert severity={isConnected ? "success" : "error"} sx={{ flex: 1 }}>
                WebSocket: {isConnected ? "Connected" : "Disconnected"}
              </Alert>
              <Alert severity={isAuthenticated ? "success" : "warning"} sx={{ flex: 1 }}>
                Auth: {isAuthenticated ? "Authenticated" : "Not Authenticated"}
              </Alert>
            </Box>
            
            <Typography variant="body2" color="text.secondary">
              To test notifications, make sure you are logged in and the WebSocket is connected. 
              The notification will appear in the notification center in the top navigation bar.
            </Typography>
          </Paper>
        </Grid>
        
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Recent Notifications ({notifications.length})
            </Typography>
            
            {notifications.length === 0 ? (
              <Alert severity="info">No notifications to display</Alert>
            ) : (
              <Box sx={{ maxHeight: 400, overflow: 'auto' }}>
                {notifications.map((notification) => (
                  <Card key={notification.id} sx={{ mb: 2 }}>
                    <CardContent>
                      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 1 }}>
                        <Typography variant="subtitle1" component="div" fontWeight={notification.is_read ? 'normal' : 'bold'}>
                          {notification.title}
                        </Typography>
                        <Chip 
                          label={notification.type} 
                          size="small"
                          color={
                            notification.type === 'success' ? 'success' :
                            notification.type === 'warning' ? 'warning' :
                            notification.type === 'error' ? 'error' :
                            'info'
                          }
                        />
                      </Box>
                      <Typography variant="body2">
                        {notification.message}
                      </Typography>
                      <Typography variant="caption" color="text.secondary" sx={{ mt: 1, display: 'block' }}>
                        {new Date(notification.created_at).toLocaleString()}
                      </Typography>
                    </CardContent>
                    <CardActions>
                      <Button 
                        size="small" 
                        onClick={() => markAsRead(notification.id)}
                        disabled={notification.is_read}
                      >
                        {notification.is_read ? "Read" : "Mark as Read"}
                      </Button>
                      <Button 
                        size="small" 
                        color="error"
                        onClick={() => removeNotification(notification.id)}
                      >
                        Delete
                      </Button>
                    </CardActions>
                  </Card>
                ))}
              </Box>
            )}
          </Paper>
        </Grid>
      </Grid>
      
      <Snackbar 
        open={!!success} 
        autoHideDuration={3000} 
        onClose={() => setSuccess(null)}
        message={success}
      />
      
      <Snackbar 
        open={!!error} 
        autoHideDuration={5000} 
        onClose={() => setError(null)}
      >
        <Alert severity="error">{error}</Alert>
      </Snackbar>
    </Container>
  );
};

export default NotificationTestPage; 