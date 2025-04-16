import React, { useState } from 'react';
import {
  Badge,
  IconButton,
  Popover,
  List,
  ListItem,
  ListItemText,
  Typography,
  Divider,
  Button,
  Box,
  ListItemIcon,
  Tooltip,
  CircularProgress
} from '@mui/material';
import NotificationsIcon from '@mui/icons-material/Notifications';
import DeleteIcon from '@mui/icons-material/Delete';
import MarkEmailReadIcon from '@mui/icons-material/MarkEmailRead';
import InfoIcon from '@mui/icons-material/Info';
import WarningIcon from '@mui/icons-material/Warning';
import ErrorIcon from '@mui/icons-material/Error';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import { useNotification } from '../contexts/NotificationContext';
import { useTranslation } from 'react-i18next';
import { useNavigate } from 'react-router-dom';
import { logInfo } from '../utils/logger';

/**
 * NotificationBell component displays a bell icon with a badge for unread notifications
 * and a dropdown menu to view and manage notifications
 */
const NotificationBell = () => {
  const { t } = useTranslation();
  const navigate = useNavigate();
  const [anchorEl, setAnchorEl] = useState(null);
  const open = Boolean(anchorEl);
  
  const {
    notifications,
    unreadCount,
    isLoading,
    error,
    markAsRead,
    markAllAsRead,
    removeNotification,
    refreshNotifications
  } = useNotification();

  const handleClick = (event) => {
    setAnchorEl(event.currentTarget);
    
    // Refresh notifications when opening the menu
    if (!open) {
      refreshNotifications();
    }
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  const handleNotificationClick = (notification) => {
    // Mark as read when clicked
    markAsRead(notification.id);
    
    // Navigate to related URL if provided
    if (notification.action_url) {
      navigate(notification.action_url);
    }
    
    handleClose();
  };

  const handleMarkAllAsRead = () => {
    markAllAsRead();
  };

  const handleClearAll = () => {
    // Clear all notifications - warn the user this is permanent
    if (window.confirm(t('Are you sure you want to delete all notifications? This cannot be undone.'))) {
      notifications.forEach(notification => {
        removeNotification(notification.id);
      });
    }
  };

  const handleRequestPermission = async () => {
    if ('Notification' in window) {
      const permission = await Notification.requestPermission();
      logInfo('Browser notification permission:', permission);
      
      // Show a test notification if permission was granted
      if (permission === 'granted') {
        new Notification(t('Notifications Enabled'), {
          body: t('You will now receive notifications when important events occur.'),
          icon: '/logo192.png'
        });
      }
    }
  };

  // Get appropriate icon based on notification type
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

  // Format timestamp to readable format
  const formatTimestamp = (timestamp) => {
    if (!timestamp) return '';
    
    const date = new Date(timestamp);
    return date.toLocaleString();
  };

  return (
    <>
      <Tooltip title={t('Notifications')}>
        <IconButton 
          color="inherit" 
          onClick={handleClick} 
          aria-label={`${unreadCount} unread notifications`}
        >
          <Badge badgeContent={unreadCount} color="error">
            <NotificationsIcon />
          </Badge>
        </IconButton>
      </Tooltip>
      
      <Popover
        open={open}
        anchorEl={anchorEl}
        onClose={handleClose}
        anchorOrigin={{
          vertical: 'bottom',
          horizontal: 'right',
        }}
        transformOrigin={{
          vertical: 'top',
          horizontal: 'right',
        }}
        PaperProps={{
          sx: { 
            width: 360, 
            maxHeight: 500,
            overflow: 'auto'
          }
        }}
      >
        <Box sx={{ p: 2, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <Typography variant="h6">{t('Notifications')}</Typography>
          <Box>
            <Tooltip title={t('Mark all as read')}>
              <IconButton 
                size="small" 
                onClick={handleMarkAllAsRead}
                disabled={notifications.length === 0 || unreadCount === 0}
              >
                <MarkEmailReadIcon fontSize="small" />
              </IconButton>
            </Tooltip>
            <Tooltip title={t('Clear all')}>
              <IconButton 
                size="small" 
                onClick={handleClearAll}
                disabled={notifications.length === 0}
              >
                <DeleteIcon fontSize="small" />
              </IconButton>
            </Tooltip>
          </Box>
        </Box>
        
        <Divider />
        
        {isLoading ? (
          <Box sx={{ p: 4, textAlign: 'center' }}>
            <CircularProgress size={24} />
          </Box>
        ) : error ? (
          <Box sx={{ p: 2, textAlign: 'center' }}>
            <Typography color="error">
              {error}
            </Typography>
            <Button onClick={refreshNotifications} sx={{ mt: 1 }}>
              {t('Retry')}
            </Button>
          </Box>
        ) : notifications.length === 0 ? (
          <Box sx={{ p: 2, textAlign: 'center' }}>
            <Typography color="text.secondary">
              {t('No notifications')}
            </Typography>
          </Box>
        ) : (
          <List sx={{ width: '100%', p: 0 }}>
            {notifications.map((notification) => (
              <React.Fragment key={notification.id}>
                <ListItem
                  alignItems="flex-start"
                  button
                  onClick={() => handleNotificationClick(notification)}
                  sx={{
                    bgcolor: notification.is_read ? 'transparent' : 'action.hover',
                    '&:hover': {
                      bgcolor: 'action.selected',
                    },
                  }}
                >
                  <ListItemIcon sx={{ mt: 1, minWidth: 40 }}>
                    {getNotificationIcon(notification.type)}
                  </ListItemIcon>
                  <ListItemText
                    primary={
                      <Typography 
                        variant="subtitle2" 
                        fontWeight={notification.is_read ? 'normal' : 'bold'}
                      >
                        {notification.title}
                      </Typography>
                    }
                    secondary={
                      <>
                        <Typography
                          component="span"
                          variant="body2"
                          color="text.primary"
                          sx={{ display: 'block' }}
                        >
                          {notification.message}
                        </Typography>
                        <Typography
                          component="span"
                          variant="caption"
                          color="text.secondary"
                        >
                          {formatTimestamp(notification.created_at)}
                        </Typography>
                      </>
                    }
                  />
                  <Box sx={{ display: 'flex', alignItems: 'center' }}>
                    <Tooltip title={t('Delete')}>
                      <IconButton 
                        edge="end" 
                        aria-label="delete" 
                        onClick={(e) => {
                          e.stopPropagation();
                          removeNotification(notification.id);
                        }}
                        size="small"
                        sx={{ mr: 1 }}
                      >
                        <DeleteIcon fontSize="small" />
                      </IconButton>
                    </Tooltip>
                  </Box>
                </ListItem>
                <Divider component="li" />
              </React.Fragment>
            ))}
          </List>
        )}
        
        {/* Browser notifications permission section */}
        {'Notification' in window && Notification.permission !== 'granted' && (
          <Box sx={{ p: 2, textAlign: 'center', bgcolor: 'background.default' }}>
            <Typography variant="caption" color="text.secondary" paragraph>
              {t('Enable browser notifications to receive alerts even when the app is in the background.')}
            </Typography>
            <Button 
              size="small" 
              onClick={handleRequestPermission}
              variant="outlined"
            >
              {t('Enable notifications')}
            </Button>
          </Box>
        )}
      </Popover>
    </>
  );
};

export default NotificationBell; 