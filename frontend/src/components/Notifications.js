import React, { useState, useEffect, useCallback } from 'react';
import {
  Badge,
  IconButton,
  Tooltip,
  Menu,
  MenuItem,
  Typography,
  Box,
  Divider,
  Button,
  ListItemText,
  ListItemIcon,
  CircularProgress,
  Paper,
  Alert,
  Chip,
  Snackbar
} from '@mui/material';
import {
  Notifications as NotificationsIcon,
  CheckCircle as CheckCircleIcon,
  Info as InfoIcon,
  Warning as WarningIcon,
  Error as ErrorIcon,
  MoreHoriz as MoreHorizIcon,
  Done as DoneIcon,
  WifiOff as WifiOffIcon,
  Refresh as RefreshIcon,
  SignalWifiConnectedNoInternet4 as RetryingIcon
} from '@mui/icons-material';
import { useAuth } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { API_URL } from '../config';
import { 
  isSocketConnected, 
  addSocketEventHandler, 
  removeSocketEventHandler, 
  initializeSocket,
  markNotificationsAsRead,
  getUserNotifications 
} from '../services/socket';

// Function to format notification timestamp
const formatNotificationTime = (timestamp) => {
  if (!timestamp) return 'Unknown time';
  
  const now = new Date();
  const notificationTime = new Date(timestamp);
  const diffMs = now - notificationTime;
  const diffMins = Math.round(diffMs / 60000);
  const diffHours = Math.round(diffMs / 3600000);
  const diffDays = Math.round(diffMs / 86400000);

  if (diffMins < 1) return 'Just now';
  if (diffMins < 60) return `${diffMins} minute${diffMins !== 1 ? 's' : ''} ago`;
  if (diffHours < 24) return `${diffHours} hour${diffHours !== 1 ? 's' : ''} ago`;
  if (diffDays < 7) return `${diffDays} day${diffDays !== 1 ? 's' : ''} ago`;
  
  return notificationTime.toLocaleDateString();
};

// Select icon based on notification type
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

const Notifications = () => {
  const [anchorEl, setAnchorEl] = useState(null);
  const [notifications, setNotifications] = useState([]);
  const [loading, setLoading] = useState(false);
  const [connectionStatus, setConnectionStatus] = useState('checking');
  const [error, setError] = useState(null);
  const [reconnectAttempt, setReconnectAttempt] = useState(0);
  const [statusMessage, setStatusMessage] = useState(null);
  const { currentUser, accessToken, isAuthenticated } = useAuth();
  const navigate = useNavigate();
  
  const open = Boolean(anchorEl);
  
  // Memoized fetch notifications function
  const fetchNotifications = useCallback(async () => {
    if (!accessToken) return;
    
    try {
      setLoading(true);
      setError(null);
      
      // Try to get notifications from WebSocket first
      if (isSocketConnected()) {
        try {
          const socketNotifications = await getUserNotifications({ limit: 20 });
          setNotifications(socketNotifications);
          return;
        } catch (socketError) {
          console.error('Failed to get notifications via WebSocket, falling back to API:', socketError);
          // Fall back to REST API
        }
      }
      
      // Fallback to REST API
      const response = await axios.get(`${API_URL}/api/notifications`, {
        headers: { Authorization: `Bearer ${accessToken}` }
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
            isRead: false,
            createdAt: new Date(Date.now() - 30 * 60000).toISOString() // 30 minutes ago
          },
          {
            _id: '2',
            title: 'Documents Required',
            message: 'Please upload your identification documents for your immigration case.',
            type: 'warning',
            isRead: false,
            createdAt: new Date(Date.now() - 3 * 3600000).toISOString() // 3 hours ago
          },
          {
            _id: '3',
            title: 'Case Status Updated',
            message: 'Your case status has been updated to "In Progress".',
            type: 'info',
            isRead: true,
            createdAt: new Date(Date.now() - 2 * 86400000).toISOString() // 2 days ago
          }
        ]);
      }
    } catch (error) {
      console.error('Error fetching notifications:', error);
      setError('Failed to load notifications. Please try again.');
      
      // Use fallback data in case of error
      setNotifications([
        {
          _id: '1',
          title: 'Form Submitted',
          message: 'Your immigration form has been submitted successfully.',
          type: 'success',
          isRead: false,
          createdAt: new Date(Date.now() - 30 * 60000).toISOString()
        }
      ]);
    } finally {
      setLoading(false);
    }
  }, [accessToken]);
  
  // Handle socket connection status
  useEffect(() => {
    const checkConnection = () => {
      setConnectionStatus(isSocketConnected() ? 'connected' : 'disconnected');
    };
    
    // Check connection immediately
    checkConnection();
    
    // Set up connection event handlers
    const handleConnect = () => {
      setConnectionStatus('connected');
      setError(null);
      setStatusMessage({ type: 'success', text: 'Connected to real-time notifications' });
      setReconnectAttempt(0);
      // Refresh notifications when connection is restored
      fetchNotifications();
    };
    
    const handleDisconnect = (reason) => {
      setConnectionStatus('disconnected');
      if (reason === 'io server disconnect') {
        // The server has forcefully disconnected the socket
        setStatusMessage({ type: 'error', text: 'Server disconnected the connection' });
      } else {
        setStatusMessage({ type: 'warning', text: 'Connection lost. Attempting to reconnect...' });
      }
    };
    
    const handleError = (err) => {
      setConnectionStatus('error');
      setError(`Connection error: ${err.message || 'Unknown error'}`);
      setStatusMessage({ type: 'error', text: `Connection error: ${err.message || 'Unknown error'}` });
    };
    
    const handleReconnecting = (attempt) => {
      setConnectionStatus('reconnecting');
      setReconnectAttempt(attempt);
      setStatusMessage({ type: 'info', text: `Reconnecting (attempt ${attempt})...` });
    };
    
    const handleReconnectFailed = () => {
      setConnectionStatus('reconnect_failed');
      setError('Failed to reconnect after multiple attempts');
      setStatusMessage({ type: 'error', text: 'Failed to reconnect. Please try manually.' });
    };
    
    // Add event handlers
    addSocketEventHandler('connect', handleConnect);
    addSocketEventHandler('disconnect', handleDisconnect);
    addSocketEventHandler('connect_error', handleError);
    addSocketEventHandler('reconnecting', handleReconnecting);
    addSocketEventHandler('reconnect_failed', handleReconnectFailed);
    
    // Clean up
    return () => {
      removeSocketEventHandler('connect', handleConnect);
      removeSocketEventHandler('disconnect', handleDisconnect);
      removeSocketEventHandler('connect_error', handleError);
      removeSocketEventHandler('reconnecting', handleReconnecting);
      removeSocketEventHandler('reconnect_failed', handleReconnectFailed);
    };
  }, [fetchNotifications]);
  
  // Handle new notifications from socket
  useEffect(() => {
    const handleNotification = (data) => {
      // Add the new notification to the list
      setNotifications(prev => {
        // Check if notification already exists
        const exists = prev.some(n => n._id === data._id || n.id === data.id);
        if (exists) return prev;
        
        // Show a status message for the new notification
        setStatusMessage({
          type: 'info',
          text: `New notification: ${data.title || data.message}`,
        });
        
        // Add to the beginning of the list
        return [data, ...prev];
      });
    };
    
    // Add notification handler
    addSocketEventHandler('notification', handleNotification);
    
    // Clean up
    return () => {
      removeSocketEventHandler('notification', handleNotification);
    };
  }, []);
  
  // Fetch notifications when component mounts or when user logs in
  useEffect(() => {
    if (isAuthenticated && accessToken) {
      fetchNotifications();
      
      // Try to initialize socket if not connected
      if (connectionStatus !== 'connected' && currentUser?.id) {
        setConnectionStatus('connecting');
        
        initializeSocket(currentUser.id)
          .then(() => {
            setConnectionStatus('connected');
            setError(null);
          })
          .catch(err => {
            setConnectionStatus('error');
            setError(`Failed to connect: ${err.message}`);
          });
      }
    } else {
      setNotifications([]);
    }
  }, [isAuthenticated, accessToken, currentUser, connectionStatus, fetchNotifications]);
  
  const handleRetryConnection = () => {
    if (!currentUser?.id) return;
    
    setConnectionStatus('connecting');
    setError(null);
    
    initializeSocket(currentUser.id)
      .then(() => {
        setConnectionStatus('connected');
        fetchNotifications();
      })
      .catch(err => {
        setConnectionStatus('error');
        setError(`Failed to connect: ${err.message}`);
      });
  };
  
  const handleClick = (event) => {
    setAnchorEl(event.currentTarget);
  };
  
  const handleClose = () => {
    setAnchorEl(null);
  };
  
  const markAsRead = async (notificationId) => {
    if (!accessToken) return;
    
    try {
      // Update in UI first for responsiveness
      setNotifications(prev => 
        prev.map(notification => 
          (notification._id === notificationId || notification.id === notificationId) 
            ? { ...notification, isRead: true } 
            : notification
        )
      );
      
      // Try WebSocket first
      if (isSocketConnected()) {
        try {
          await markNotificationsAsRead(notificationId);
          return;
        } catch (socketError) {
          console.error('Failed to mark notification as read via WebSocket, falling back to API:', socketError);
          // Fall back to REST API
        }
      }
      
      // Fallback to REST API
      await axios.post(`${API_URL}/api/notifications/${notificationId}/read`, {}, {
        headers: { Authorization: `Bearer ${accessToken}` }
      });
    } catch (error) {
      console.error('Error marking notification as read:', error);
      // Revert the UI change if the server update failed
      fetchNotifications();
    }
  };
  
  const markAllAsRead = async () => {
    if (!accessToken) return;
    
    try {
      // Get IDs of all unread notifications
      const unreadIds = notifications
        .filter(n => !n.isRead)
        .map(n => n._id || n.id);
        
      if (unreadIds.length === 0) return;
      
      // Update in UI first for responsiveness
      setNotifications(prev => 
        prev.map(notification => ({ ...notification, isRead: true }))
      );
      
      // Try WebSocket first
      if (isSocketConnected()) {
        try {
          await markNotificationsAsRead(unreadIds);
          return;
        } catch (socketError) {
          console.error('Failed to mark all as read via WebSocket, falling back to API:', socketError);
          // Fall back to REST API
        }
      }
      
      // Fallback to REST API
      await axios.post(`${API_URL}/api/notifications/mark-all-read`, {}, {
        headers: { Authorization: `Bearer ${accessToken}` }
      });
    } catch (error) {
      console.error('Error marking all notifications as read:', error);
      // Revert the UI change if the server update failed
      fetchNotifications();
    }
  };
  
  const handleNotificationClick = (notification) => {
    // Mark as read
    markAsRead(notification._id || notification.id);
    
    // Handle navigation based on notification type
    if (notification.category === 'immigration' && notification.caseId) {
      navigate(`/case/${notification.caseId}`);
    } else if (notification.category === 'immigration') {
      navigate('/immigration-dashboard');
    } else if (notification.formId) {
      navigate(`/forms/${notification.formId}`);
    }
    
    handleClose();
  };
  
  // Don't render if user is not authenticated
  if (!isAuthenticated) {
    return null;
  }
  
  // Close status message after 3 seconds
  const handleStatusClose = () => {
    setStatusMessage(null);
  };
  
  // Determine icon color based on connection status
  const getConnectionColor = () => {
    switch (connectionStatus) {
      case 'connected':
        return 'default';
      case 'disconnected':
      case 'error':
      case 'reconnect_failed':
        return 'error';
      case 'connecting':
      case 'reconnecting':
      case 'checking':
        return 'disabled';
      default:
        return 'default';
    }
  };
  
  // Determine connection icon based on status
  const getConnectionIcon = () => {
    switch (connectionStatus) {
      case 'reconnecting':
        return <RetryingIcon sx={{ 
          position: 'absolute', 
          right: -5, 
          bottom: -5, 
          fontSize: '0.8rem', 
          color: 'info.main',
          backgroundColor: 'background.paper',
          borderRadius: '50%',
          animation: 'pulse 1.5s infinite'
        }} />;
      case 'disconnected':
      case 'error':
      case 'reconnect_failed':
        return <WifiOffIcon sx={{ 
          position: 'absolute', 
          right: -5, 
          bottom: -5, 
          fontSize: '0.8rem', 
          color: 'error.main',
          backgroundColor: 'background.paper',
          borderRadius: '50%'
        }} />;
      default:
        return null;
    }
  };
  
  // Get unread count
  const unreadCount = notifications.filter(n => !n.isRead).length;
  
  return (
    <>
      <Tooltip title={
        connectionStatus === 'connected' ? "Notifications" : 
        connectionStatus === 'disconnected' ? "Disconnected - Click to reconnect" : 
        connectionStatus === 'reconnecting' ? `Reconnecting (attempt ${reconnectAttempt})...` :
        connectionStatus === 'error' ? "Connection error - Click to retry" :
        "Connecting..."
      }>
        <IconButton
          onClick={handleClick}
          size="large"
          color={getConnectionColor()}
          aria-label="notifications"
          aria-controls={open ? 'notifications-menu' : undefined}
          aria-haspopup="true"
          aria-expanded={open ? 'true' : undefined}
          sx={{ ml: 1, position: 'relative' }}
        >
          <Badge badgeContent={unreadCount} color="error">
            <NotificationsIcon />
          </Badge>
          {getConnectionIcon()}
        </IconButton>
      </Tooltip>
      
      <Menu
        id="notifications-menu"
        anchorEl={anchorEl}
        open={open}
        onClose={handleClose}
        PaperProps={{
          sx: {
            width: { xs: '90%', sm: 350, md: 400 },
            maxHeight: 500,
            maxWidth: '100%',
            overflow: 'auto'
          }
        }}
        transformOrigin={{ horizontal: 'right', vertical: 'top' }}
        anchorOrigin={{ horizontal: 'right', vertical: 'bottom' }}
      >
        <Box sx={{ p: 2, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <Typography variant="h6">Notifications</Typography>
          {connectionStatus !== 'connected' && (
            <Chip 
              icon={
                connectionStatus === 'connecting' || connectionStatus === 'reconnecting' 
                  ? <CircularProgress size={16} /> 
                  : <WifiOffIcon />
              }
              label={
                connectionStatus === 'connecting' ? "Connecting..." : 
                connectionStatus === 'reconnecting' ? `Reconnecting (${reconnectAttempt})` : 
                "Offline"
              }
              color={
                connectionStatus === 'connecting' || connectionStatus === 'reconnecting' 
                  ? "default" 
                  : "error"
              }
              size="small"
            />
          )}
        </Box>
        
        {error && (
          <Alert severity="error" sx={{ mx: 2, mb: 1 }}>
            {error}
            <Button 
              size="small" 
              startIcon={<RefreshIcon />} 
              onClick={handleRetryConnection}
              sx={{ ml: 1 }}
            >
              Retry
            </Button>
          </Alert>
        )}
        
        {loading ? (
          <Box sx={{ display: 'flex', justifyContent: 'center', p: 3 }}>
            <CircularProgress size={30} />
          </Box>
        ) : notifications.length === 0 ? (
          <Box sx={{ p: 3, textAlign: 'center' }}>
            <Typography color="textSecondary">No notifications</Typography>
          </Box>
        ) : (
          <>
            {unreadCount > 0 && (
              <Box sx={{ px: 2, display: 'flex', justifyContent: 'flex-end' }}>
                <Button
                  size="small"
                  startIcon={<DoneIcon />}
                  onClick={markAllAsRead}
                >
                  Mark all as read
                </Button>
              </Box>
            )}
            
            {/* Notifications list */}
            {notifications.map((notification) => (
              <MenuItem
                key={notification._id || notification.id}
                onClick={() => handleNotificationClick(notification)}
                sx={{
                  py: 1.5,
                  px: 2,
                  borderLeft: notification.isRead ? 'none' : '4px solid',
                  borderLeftColor: `${notification.type}.main`,
                  bgcolor: notification.isRead ? 'inherit' : 'action.hover',
                  '&:hover': {
                    bgcolor: 'action.selected'
                  }
                }}
              >
                <ListItemIcon>
                  {getNotificationIcon(notification.type)}
                </ListItemIcon>
                <ListItemText
                  primary={
                    <Typography variant="subtitle2" noWrap>
                      {notification.title || 'Notification'}
                    </Typography>
                  }
                  secondary={
                    <>
                      <Typography variant="body2" color="textPrimary" noWrap>
                        {notification.message}
                      </Typography>
                      <Typography variant="caption" color="textSecondary">
                        {formatNotificationTime(notification.createdAt || notification.timestamp)}
                      </Typography>
                    </>
                  }
                />
              </MenuItem>
            ))}
          </>
        )}
        
        <Divider />
        <Box sx={{ p: 1, display: 'flex', justifyContent: 'space-between' }}>
          <Button size="small" onClick={fetchNotifications} startIcon={<RefreshIcon />}>
            Refresh
          </Button>
          <Button size="small" onClick={() => navigate('/notifications')}>
            View All
          </Button>
        </Box>
      </Menu>
      
      {/* Status message snackbar */}
      <Snackbar
        open={Boolean(statusMessage)}
        autoHideDuration={statusMessage?.type === 'error' ? 6000 : 3000}
        onClose={handleStatusClose}
        anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}
      >
        {statusMessage && (
          <Alert 
            onClose={handleStatusClose} 
            severity={statusMessage.type} 
            sx={{ width: '100%' }}
          >
            {statusMessage.text}
          </Alert>
        )}
      </Snackbar>
    </>
  );
};

export default Notifications; 