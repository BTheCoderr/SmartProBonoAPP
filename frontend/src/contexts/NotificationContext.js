import React, { createContext, useContext, useState, useEffect } from 'react';
import PropTypes from 'prop-types';
import { useAuth } from './AuthContext';
import { logInfo, logError, logDebug } from '../utils/logger';
import notificationService from '../services/notificationService';
import axios from 'axios';
import config from '../config';

// Create the notification context
const NotificationContext = createContext();

// Custom hook to use the notification context
export const useNotification = () => {
  return useContext(NotificationContext);
};

export const NotificationProvider = ({ children }) => {
  // State for notifications
  const [notifications, setNotifications] = useState([]);
  const [unreadCount, setUnreadCount] = useState(0);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  
  // Get access to Auth context
  const { isAuthenticated, user } = useAuth();
  
  // Effect to initialize WebSocket and fetch existing notifications
  useEffect(() => {
    if (isAuthenticated && user?.id) {
      setIsLoading(true);
      
      // Connect to WebSocket
      notificationService.connect()
        .then(() => {
          logInfo('WebSocket connected in NotificationContext');
          return notificationService.authenticate(user.id);
        })
        .then(() => {
          logInfo('WebSocket authenticated in NotificationContext');
          // Fetch existing notifications
          return fetchNotifications();
        })
        .catch(err => {
          logError('Failed to initialize notifications', err);
          setError('Failed to connect to notification service');
        })
        .finally(() => {
          setIsLoading(false);
        });
        
      // Set up listener for new notifications
      const unsubscribe = notificationService.onNotification(handleNewNotification);
      
      return () => {
        // Clean up
        unsubscribe();
        notificationService.disconnect();
      };
    }
  }, [isAuthenticated, user]);
  
  // Function to fetch existing notifications
  const fetchNotifications = async () => {
    try {
      const response = await axios.get(`${config.api.baseUrl}/api/notifications`);
      const fetchedNotifications = response.data.notifications || [];
      
      setNotifications(fetchedNotifications);
      const unreadNotifications = fetchedNotifications.filter(n => !n.is_read);
      setUnreadCount(unreadNotifications.length);
      
      return fetchedNotifications;
    } catch (error) {
      logError('Failed to fetch notifications', error);
      setError('Failed to load notifications');
      throw error;
    }
  };
  
  // Handler for receiving new notifications
  const handleNewNotification = (notification) => {
    logDebug('Received notification in context', notification);
    
    setNotifications(prev => {
      // Check if this notification already exists (by id)
      const exists = prev.some(n => n.id === notification.id);
      if (exists) return prev;
      
      // Add the new notification to the beginning of the array
      const newNotifications = [{...notification, is_read: false}, ...prev];
      
      // Update unread count
      setUnreadCount(count => count + 1);
      
      // Show browser notification if supported
      showBrowserNotification(notification);
      
      return newNotifications;
    });
  };
  
  // Function to show browser notification if permitted
  const showBrowserNotification = (notification) => {
    if ('Notification' in window && Notification.permission === 'granted') {
      new Notification(notification.title, {
        body: notification.message,
        icon: '/logo192.png', // Adjust path to your app's icon
      });
    } else if ('Notification' in window && Notification.permission !== 'denied') {
      // Request permission
      Notification.requestPermission().then(permission => {
        if (permission === 'granted') {
          new Notification(notification.title, {
            body: notification.message,
            icon: '/logo192.png',
          });
        }
      });
    }
  };
  
  // Function to mark a notification as read
  const markAsRead = async (notificationId) => {
    try {
      setNotifications(prev => {
        const updated = prev.map(notification => {
          if (notification.id === notificationId && !notification.is_read) {
            // Mark as read and decrement unread count
            setUnreadCount(count => Math.max(0, count - 1));
            return { ...notification, is_read: true };
          }
          return notification;
        });
        return updated;
      });
      
      // Send API request to mark as read on the server
      await axios.post(`${config.api.baseUrl}/api/notifications/${notificationId}/read`);
      
      logInfo('Notification marked as read', { notificationId });
    } catch (error) {
      logError('Failed to mark notification as read', error);
      // Revert the UI change on error
      fetchNotifications();
    }
  };
  
  // Function to mark all notifications as read
  const markAllAsRead = async () => {
    try {
      setNotifications(prev => {
        const updated = prev.map(notification => {
          return { ...notification, is_read: true };
        });
        setUnreadCount(0);
        return updated;
      });
      
      // Send API request to mark all as read on the server
      await axios.post(`${config.api.baseUrl}/api/notifications/read-all`);
      
      logInfo('All notifications marked as read');
    } catch (error) {
      logError('Failed to mark all notifications as read', error);
      // Revert the UI change on error
      fetchNotifications();
    }
  };
  
  // Function to remove a notification
  const removeNotification = async (notificationId) => {
    try {
      setNotifications(prev => {
        // Find the notification to check if it's unread
        const notification = prev.find(n => n.id === notificationId);
        if (notification && !notification.is_read) {
          setUnreadCount(count => Math.max(0, count - 1));
        }
        
        // Filter out the notification
        return prev.filter(n => n.id !== notificationId);
      });
      
      // Send API request to delete notification on the server
      await axios.delete(`${config.api.baseUrl}/api/notifications/${notificationId}`);
      
      logInfo('Notification removed', { notificationId });
    } catch (error) {
      logError('Failed to remove notification', error);
      // Revert the UI change on error
      fetchNotifications();
    }
  };
  
  // Create the context value object
  const value = {
    notifications,
    unreadCount,
    isLoading,
    error,
    markAsRead,
    markAllAsRead,
    removeNotification,
    refreshNotifications: fetchNotifications
  };
  
  return (
    <NotificationContext.Provider value={value}>
      {children}
    </NotificationContext.Provider>
  );
};

NotificationProvider.propTypes = {
  children: PropTypes.node.isRequired
};

export default NotificationContext; 