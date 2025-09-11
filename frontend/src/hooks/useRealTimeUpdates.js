import { useState, useEffect, useCallback } from 'react';
import notificationService from '../services/NotificationService';
import { useAuth } from '../context/AuthContext';

/**
 * Custom hook for real-time updates across the Virtual Paralegal CRM
 */
export const useRealTimeUpdates = () => {
  const { currentUser } = useAuth();
  const [notifications, setNotifications] = useState([]);
  const [isConnected, setIsConnected] = useState(false);
  const [lastUpdate, setLastUpdate] = useState(null);

  // Connect to notification service when component mounts
  useEffect(() => {
    if (currentUser) {
      const connected = notificationService.connect(
        currentUser.id || currentUser.user_id,
        currentUser.role || 'client'
      );
      setIsConnected(connected);
    }

    return () => {
      notificationService.disconnect();
      setIsConnected(false);
    };
  }, [currentUser]);

  // Subscribe to different types of notifications
  useEffect(() => {
    if (!isConnected) return;

    const handleCaseUpdate = (data) => {
      setNotifications(prev => [{
        id: data.id,
        type: 'case_update',
        title: data.title,
        message: data.message,
        timestamp: data.timestamp,
        priority: data.priority,
        read: false
      }, ...prev.slice(0, 49)]); // Keep only last 50 notifications
      setLastUpdate(new Date());
    };

    const handleCourtReminder = (data) => {
      setNotifications(prev => [{
        id: data.id,
        type: 'court_reminder',
        title: data.title,
        message: data.message,
        timestamp: data.timestamp,
        priority: data.priority,
        read: false,
        courtDate: data.courtDate,
        appointmentDate: data.appointmentDate
      }, ...prev.slice(0, 49)]);
      setLastUpdate(new Date());
    };

    const handleDocumentUpdate = (data) => {
      setNotifications(prev => [{
        id: data.id,
        type: 'document_update',
        title: data.title,
        message: data.message,
        timestamp: data.timestamp,
        priority: data.priority,
        read: false,
        documentId: data.documentId,
        dueDate: data.dueDate
      }, ...prev.slice(0, 49)]);
      setLastUpdate(new Date());
    };

    const handlePaymentUpdate = (data) => {
      setNotifications(prev => [{
        id: data.id,
        type: 'payment_update',
        title: data.title,
        message: data.message,
        timestamp: data.timestamp,
        priority: data.priority,
        read: false,
        amount: data.amount,
        clientName: data.clientName
      }, ...prev.slice(0, 49)]);
      setLastUpdate(new Date());
    };

    // Subscribe to notification types
    notificationService.subscribe('case_update', handleCaseUpdate);
    notificationService.subscribe('court_reminder', handleCourtReminder);
    notificationService.subscribe('document_update', handleDocumentUpdate);
    notificationService.subscribe('payment_update', handlePaymentUpdate);

    return () => {
      notificationService.unsubscribe('case_update', handleCaseUpdate);
      notificationService.unsubscribe('court_reminder', handleCourtReminder);
      notificationService.unsubscribe('document_update', handleDocumentUpdate);
      notificationService.unsubscribe('payment_update', handlePaymentUpdate);
    };
  }, [isConnected]);

  // Mark notification as read
  const markAsRead = useCallback((notificationId) => {
    setNotifications(prev => 
      prev.map(notification => 
        notification.id === notificationId 
          ? { ...notification, read: true }
          : notification
      )
    );
  }, []);

  // Mark all notifications as read
  const markAllAsRead = useCallback(() => {
    setNotifications(prev => 
      prev.map(notification => ({ ...notification, read: true }))
    );
  }, []);

  // Clear all notifications
  const clearAll = useCallback(() => {
    setNotifications([]);
  }, []);

  // Get unread count
  const unreadCount = notifications.filter(n => !n.read).length;

  // Get notifications by type
  const getNotificationsByType = useCallback((type) => {
    return notifications.filter(n => n.type === type);
  }, [notifications]);

  // Get notifications by priority
  const getNotificationsByPriority = useCallback((priority) => {
    return notifications.filter(n => n.priority === priority);
  }, [notifications]);

  return {
    notifications,
    isConnected,
    lastUpdate,
    unreadCount,
    markAsRead,
    markAllAsRead,
    clearAll,
    getNotificationsByType,
    getNotificationsByPriority
  };
};

export default useRealTimeUpdates;
