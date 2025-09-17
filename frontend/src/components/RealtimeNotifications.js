/**
 * Real-Time Notifications Component
 * Displays live notifications and case updates
 */

import React, { useState, useEffect } from 'react';
import {
  Box,
  Paper,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Typography,
  Chip,
  IconButton,
  Badge,
  Collapse,
  Alert,
  Divider,
  Button,
  Tooltip
} from '@mui/material';
import {
  Notifications as NotificationsIcon,
  CaseIcon,
  Warning as WarningIcon,
  Info as InfoIcon,
  CheckCircle as CheckCircleIcon,
  ExpandMore as ExpandMoreIcon,
  ExpandLess as ExpandLessIcon,
  Clear as ClearIcon,
  MarkEmailRead as MarkReadIcon
} from '@mui/icons-material';
import { useNotifications } from '../hooks/useWebSocket';

const RealtimeNotifications = ({ 
  maxNotifications = 50,
  showBadge = true,
  autoExpand = false,
  onNotificationClick
}) => {
  const {
    notifications,
    unreadCount,
    markAsRead,
    markAllAsRead,
    clearNotifications
  } = useNotifications();

  const [expanded, setExpanded] = useState(autoExpand);
  const [filter, setFilter] = useState('all'); // 'all', 'unread', 'case_updates', 'notifications'

  // Auto-expand if there are urgent notifications
  useEffect(() => {
    const hasUrgent = notifications.some(n => 
      n.notification_type === 'urgent' || 
      n.urgency === 'high' || 
      n.urgency === 'critical'
    );
    if (hasUrgent && !expanded) {
      setExpanded(true);
    }
  }, [notifications, expanded]);

  const getNotificationIcon = (notification) => {
    if (notification.type === 'case_update') {
      return <CaseIcon color="primary" />;
    }
    
    switch (notification.notification_type) {
      case 'urgent':
      case 'warning':
        return <WarningIcon color="error" />;
      case 'success':
        return <CheckCircleIcon color="success" />;
      case 'info':
      default:
        return <InfoIcon color="info" />;
    }
  };

  const getNotificationColor = (notification) => {
    if (notification.type === 'case_update') {
      return 'primary';
    }
    
    switch (notification.notification_type) {
      case 'urgent':
        return 'error';
      case 'warning':
        return 'warning';
      case 'success':
        return 'success';
      case 'info':
      default:
        return 'info';
    }
  };

  const getUrgencyChip = (urgency) => {
    if (!urgency) return null;
    
    const colorMap = {
      'critical': 'error',
      'high': 'warning',
      'medium': 'info',
      'low': 'default'
    };
    
    return (
      <Chip 
        label={urgency.toUpperCase()} 
        size="small" 
        color={colorMap[urgency] || 'default'}
        sx={{ ml: 1 }}
      />
    );
  };

  const formatTimestamp = (timestamp) => {
    const date = new Date(timestamp);
    const now = new Date();
    const diffMs = now - date;
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMs / 3600000);
    const diffDays = Math.floor(diffMs / 86400000);

    if (diffMins < 1) return 'Just now';
    if (diffMins < 60) return `${diffMins}m ago`;
    if (diffHours < 24) return `${diffHours}h ago`;
    if (diffDays < 7) return `${diffDays}d ago`;
    return date.toLocaleDateString();
  };

  const filteredNotifications = notifications.filter(notification => {
    if (filter === 'unread') return !notification.read;
    if (filter === 'case_updates') return notification.type === 'case_update';
    if (filter === 'notifications') return notification.type === 'notification';
    return true;
  }).slice(0, maxNotifications);

  const handleNotificationClick = (notification) => {
    if (onNotificationClick) {
      onNotificationClick(notification);
    }
    
    if (!notification.read) {
      markAsRead(notification.id);
    }
  };

  const handleMarkAllRead = () => {
    markAllAsRead();
  };

  const handleClearAll = () => {
    clearNotifications();
  };

  return (
    <Box sx={{ width: '100%', maxWidth: 400 }}>
      {/* Header */}
      <Box sx={{ 
        display: 'flex', 
        alignItems: 'center', 
        justifyContent: 'space-between',
        p: 1,
        bgcolor: 'background.paper',
        borderBottom: 1,
        borderColor: 'divider'
      }}>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          <Badge badgeContent={showBadge ? unreadCount : 0} color="error">
            <NotificationsIcon />
          </Badge>
          <Typography variant="h6">
            Notifications
          </Typography>
          {unreadCount > 0 && (
            <Chip 
              label={`${unreadCount} unread`} 
              size="small" 
              color="error" 
            />
          )}
        </Box>
        
        <Box>
          <Tooltip title={expanded ? "Collapse" : "Expand"}>
            <IconButton 
              size="small" 
              onClick={() => setExpanded(!expanded)}
            >
              {expanded ? <ExpandLessIcon /> : <ExpandMoreIcon />}
            </IconButton>
          </Tooltip>
        </Box>
      </Box>

      {/* Actions */}
      {expanded && (
        <Box sx={{ 
          p: 1, 
          bgcolor: 'grey.50', 
          borderBottom: 1, 
          borderColor: 'divider',
          display: 'flex',
          gap: 1,
          flexWrap: 'wrap'
        }}>
          <Button 
            size="small" 
            onClick={handleMarkAllRead}
            disabled={unreadCount === 0}
            startIcon={<MarkReadIcon />}
          >
            Mark All Read
          </Button>
          <Button 
            size="small" 
            onClick={handleClearAll}
            disabled={notifications.length === 0}
            startIcon={<ClearIcon />}
          >
            Clear All
          </Button>
        </Box>
      )}

      {/* Notifications List */}
      <Collapse in={expanded}>
        <Paper variant="outlined" sx={{ maxHeight: 400, overflow: 'auto' }}>
          {filteredNotifications.length === 0 ? (
            <Box sx={{ 
              p: 3, 
              textAlign: 'center',
              color: 'text.secondary'
            }}>
              <NotificationsIcon sx={{ fontSize: 48, mb: 1, opacity: 0.5 }} />
              <Typography variant="body2">
                {filter === 'unread' ? 'No unread notifications' : 'No notifications'}
              </Typography>
            </Box>
          ) : (
            <List sx={{ p: 0 }}>
              {filteredNotifications.map((notification, index) => (
                <React.Fragment key={notification.id || index}>
                  <ListItem
                    button
                    onClick={() => handleNotificationClick(notification)}
                    sx={{
                      bgcolor: notification.read ? 'transparent' : 'action.hover',
                      '&:hover': {
                        bgcolor: 'action.selected'
                      }
                    }}
                  >
                    <ListItemIcon>
                      {getNotificationIcon(notification)}
                    </ListItemIcon>
                    <ListItemText
                      primary={
                        <Box sx={{ display: 'flex', alignItems: 'center', flexWrap: 'wrap' }}>
                          <Typography variant="body2" sx={{ fontWeight: notification.read ? 'normal' : 'bold' }}>
                            {notification.type === 'case_update' 
                              ? `Case Update: ${notification.case_id || 'Unknown Case'}`
                              : notification.data?.title || 'Notification'
                            }
                          </Typography>
                          {getUrgencyChip(notification.urgency)}
                          {!notification.read && (
                            <Chip label="NEW" size="small" color="error" sx={{ ml: 1 }} />
                          )}
                        </Box>
                      }
                      secondary={
                        <Box>
                          <Typography variant="caption" color="text.secondary">
                            {notification.type === 'case_update' 
                              ? notification.update?.description || 'Case status updated'
                              : notification.data?.message || 'New notification'
                            }
                          </Typography>
                          <Typography variant="caption" display="block" color="text.secondary">
                            {formatTimestamp(notification.timestamp)}
                          </Typography>
                        </Box>
                      }
                    />
                  </ListItem>
                  {index < filteredNotifications.length - 1 && <Divider />}
                </React.Fragment>
              ))}
            </List>
          )}
        </Paper>
      </Collapse>

      {/* Summary */}
      {expanded && notifications.length > 0 && (
        <Box sx={{ 
          p: 1, 
          bgcolor: 'grey.50', 
          borderTop: 1, 
          borderColor: 'divider',
          textAlign: 'center'
        }}>
          <Typography variant="caption" color="text.secondary">
            Showing {filteredNotifications.length} of {notifications.length} notifications
          </Typography>
        </Box>
      )}
    </Box>
  );
};

export default RealtimeNotifications;
