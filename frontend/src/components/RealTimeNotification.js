import React, { useState, useEffect } from 'react';
import {
  Snackbar,
  Alert,
  IconButton,
  Badge,
  Menu,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Typography,
  Box,
  Divider,
  Button,
  Chip
} from '@mui/material';
import {
  Notifications as NotificationsIcon,
  CheckCircle as CheckCircleIcon,
  Warning as WarningIcon,
  Info as InfoIcon,
  Error as ErrorIcon,
  Assignment as AssignmentIcon,
  Schedule as ScheduleIcon,
  Description as DescriptionIcon,
  Payment as PaymentIcon,
  MarkAsUnread as MarkAsUnreadIcon
} from '@mui/icons-material';
import { useRealTimeUpdates } from '../hooks/useRealTimeUpdates';

const RealTimeNotification = () => {
  const {
    notifications,
    isConnected,
    unreadCount,
    markAsRead,
    markAllAsRead,
    clearAll
  } = useRealTimeUpdates();

  const [anchorEl, setAnchorEl] = useState(null);
  const [currentNotification, setCurrentNotification] = useState(null);
  const [showSnackbar, setShowSnackbar] = useState(false);

  // Show snackbar for new notifications
  useEffect(() => {
    if (notifications.length > 0 && !notifications[0].read) {
      setCurrentNotification(notifications[0]);
      setShowSnackbar(true);
    }
  }, [notifications]);

  const handleMenuOpen = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleMenuClose = () => {
    setAnchorEl(null);
  };

  const handleSnackbarClose = (event, reason) => {
    if (reason === 'clickaway') {
      return;
    }
    setShowSnackbar(false);
    if (currentNotification) {
      markAsRead(currentNotification.id);
    }
  };

  const handleNotificationClick = (notification) => {
    markAsRead(notification.id);
    setCurrentNotification(notification);
    setShowSnackbar(true);
  };

  const getNotificationIcon = (type, priority) => {
    const iconProps = { fontSize: 'small' };
    
    switch (type) {
      case 'case_update':
        return <AssignmentIcon {...iconProps} />;
      case 'court_reminder':
        return <ScheduleIcon {...iconProps} />;
      case 'document_update':
        return <DescriptionIcon {...iconProps} />;
      case 'payment_update':
        return <PaymentIcon {...iconProps} />;
      default:
        return <NotificationsIcon {...iconProps} />;
    }
  };

  const getPriorityColor = (priority) => {
    switch (priority) {
      case 'success': return 'success';
      case 'warning': return 'warning';
      case 'error': return 'error';
      case 'info': return 'info';
      default: return 'info';
    }
  };

  const getPriorityIcon = (priority) => {
    switch (priority) {
      case 'success': return <CheckCircleIcon fontSize="small" />;
      case 'warning': return <WarningIcon fontSize="small" />;
      case 'error': return <ErrorIcon fontSize="small" />;
      case 'info': return <InfoIcon fontSize="small" />;
      default: return <InfoIcon fontSize="small" />;
    }
  };

  const formatTimestamp = (timestamp) => {
    const date = new Date(timestamp);
    const now = new Date();
    const diffInMinutes = Math.floor((now - date) / (1000 * 60));
    
    if (diffInMinutes < 1) return 'Just now';
    if (diffInMinutes < 60) return `${diffInMinutes}m ago`;
    if (diffInMinutes < 1440) return `${Math.floor(diffInMinutes / 60)}h ago`;
    return date.toLocaleDateString();
  };

  return (
    <>
      {/* Notification Bell */}
      <IconButton
        color="inherit"
        onClick={handleMenuOpen}
        disabled={!isConnected}
      >
        <Badge badgeContent={unreadCount} color="error">
          <NotificationsIcon />
        </Badge>
      </IconButton>

      {/* Notification Menu */}
      <Menu
        anchorEl={anchorEl}
        open={Boolean(anchorEl)}
        onClose={handleMenuClose}
        PaperProps={{
          sx: { width: 400, maxHeight: 500 }
        }}
      >
        <Box sx={{ p: 2, borderBottom: 1, borderColor: 'divider' }}>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <Typography variant="h6">
              Notifications
              {unreadCount > 0 && (
                <Chip 
                  label={unreadCount} 
                  size="small" 
                  color="error" 
                  sx={{ ml: 1 }}
                />
              )}
            </Typography>
            <Box>
              {unreadCount > 0 && (
                <Button
                  size="small"
                  startIcon={<MarkAsUnreadIcon />}
                  onClick={markAllAsRead}
                  sx={{ mr: 1 }}
                >
                  Mark All Read
                </Button>
              )}
              <Button
                size="small"
                onClick={clearAll}
              >
                Clear All
              </Button>
            </Box>
          </Box>
          <Typography variant="body2" color="text.secondary">
            {isConnected ? 'Real-time updates active' : 'Connecting...'}
          </Typography>
        </Box>

        {notifications.length === 0 ? (
          <Box sx={{ p: 3, textAlign: 'center' }}>
            <Typography variant="body2" color="text.secondary">
              No notifications yet
            </Typography>
          </Box>
        ) : (
          <List sx={{ maxHeight: 400, overflow: 'auto' }}>
            {notifications.map((notification, index) => (
              <React.Fragment key={notification.id}>
                <ListItem
                  button
                  onClick={() => handleNotificationClick(notification)}
                  sx={{
                    bgcolor: notification.read ? 'transparent' : 'action.hover',
                    '&:hover': { bgcolor: 'action.selected' }
                  }}
                >
                  <ListItemIcon>
                    <Box sx={{ position: 'relative' }}>
                      {getNotificationIcon(notification.type, notification.priority)}
                      {!notification.read && (
                        <Box
                          sx={{
                            position: 'absolute',
                            top: -2,
                            right: -2,
                            width: 8,
                            height: 8,
                            borderRadius: '50%',
                            bgcolor: 'error.main'
                          }}
                        />
                      )}
                    </Box>
                  </ListItemIcon>
                  <ListItemText
                    primary={
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                        <Typography variant="subtitle2">
                          {notification.title}
                        </Typography>
                        {getPriorityIcon(notification.priority)}
                      </Box>
                    }
                    secondary={
                      <Box>
                        <Typography variant="body2" color="text.secondary">
                          {notification.message}
                        </Typography>
                        <Typography variant="caption" color="text.secondary">
                          {formatTimestamp(notification.timestamp)}
                        </Typography>
                      </Box>
                    }
                  />
                </ListItem>
                {index < notifications.length - 1 && <Divider />}
              </React.Fragment>
            ))}
          </List>
        )}
      </Menu>

      {/* Snackbar for new notifications */}
      <Snackbar
        open={showSnackbar}
        autoHideDuration={6000}
        onClose={handleSnackbarClose}
        anchorOrigin={{ vertical: 'top', horizontal: 'right' }}
      >
        <Alert
          onClose={handleSnackbarClose}
          severity={getPriorityColor(currentNotification?.priority)}
          sx={{ width: '100%' }}
          icon={getPriorityIcon(currentNotification?.priority)}
        >
          <Typography variant="subtitle2" gutterBottom>
            {currentNotification?.title}
          </Typography>
          <Typography variant="body2">
            {currentNotification?.message}
          </Typography>
        </Alert>
      </Snackbar>
    </>
  );
};

export default RealTimeNotification;
