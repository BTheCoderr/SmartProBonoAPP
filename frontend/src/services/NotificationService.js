/**
 * Real-time notification service for the Virtual Paralegal CRM
 * Handles WebSocket connections and real-time updates
 */

class NotificationService {
  constructor() {
    this.ws = null;
    this.listeners = new Map();
    this.reconnectAttempts = 0;
    this.maxReconnectAttempts = 5;
    this.reconnectDelay = 1000;
    this.isConnected = false;
  }

  /**
   * Connect to WebSocket server
   */
  connect(userId, userRole) {
    try {
      // In production, this would connect to a real WebSocket server
      // For now, we'll simulate real-time updates with intervals
      console.log(`Connecting to notification service for ${userRole} user: ${userId}`);
      
      this.userId = userId;
      this.userRole = userRole;
      this.isConnected = true;
      
      // Simulate real-time updates
      this.startSimulatedUpdates();
      
      return true;
    } catch (error) {
      console.error('Failed to connect to notification service:', error);
      return false;
    }
  }

  /**
   * Disconnect from WebSocket server
   */
  disconnect() {
    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }
    this.isConnected = false;
    this.stopSimulatedUpdates();
  }

  /**
   * Subscribe to notifications for a specific type
   */
  subscribe(type, callback) {
    if (!this.listeners.has(type)) {
      this.listeners.set(type, new Set());
    }
    this.listeners.get(type).add(callback);
  }

  /**
   * Unsubscribe from notifications
   */
  unsubscribe(type, callback) {
    if (this.listeners.has(type)) {
      this.listeners.get(type).delete(callback);
    }
  }

  /**
   * Emit notification to all subscribers
   */
  emit(type, data) {
    if (this.listeners.has(type)) {
      this.listeners.get(type).forEach(callback => {
        try {
          callback(data);
        } catch (error) {
          console.error('Error in notification callback:', error);
        }
      });
    }
  }

  /**
   * Start simulated real-time updates
   */
  startSimulatedUpdates() {
    // Simulate case updates
    this.caseUpdateInterval = setInterval(() => {
      this.simulateCaseUpdate();
    }, 30000); // Every 30 seconds

    // Simulate court date reminders
    this.courtDateInterval = setInterval(() => {
      this.simulateCourtDateReminder();
    }, 60000); // Every minute

    // Simulate document updates
    this.documentInterval = setInterval(() => {
      this.simulateDocumentUpdate();
    }, 45000); // Every 45 seconds

    // Simulate payment updates (for bondsman)
    if (this.userRole === 'bondsman') {
      this.paymentInterval = setInterval(() => {
        this.simulatePaymentUpdate();
      }, 90000); // Every 90 seconds
    }
  }

  /**
   * Stop simulated updates
   */
  stopSimulatedUpdates() {
    if (this.caseUpdateInterval) {
      clearInterval(this.caseUpdateInterval);
    }
    if (this.courtDateInterval) {
      clearInterval(this.courtDateInterval);
    }
    if (this.documentInterval) {
      clearInterval(this.documentInterval);
    }
    if (this.paymentInterval) {
      clearInterval(this.paymentInterval);
    }
  }

  /**
   * Simulate case status updates
   */
  simulateCaseUpdate() {
    const updates = [
      {
        type: 'case_update',
        data: {
          id: Math.floor(Math.random() * 1000),
          title: 'Case Status Updated',
          message: 'Your immigration case has been updated to "Under Review"',
          timestamp: new Date().toISOString(),
          priority: 'info'
        }
      },
      {
        type: 'case_update',
        data: {
          id: Math.floor(Math.random() * 1000),
          title: 'New Document Available',
          message: 'A new document has been uploaded to your case file',
          timestamp: new Date().toISOString(),
          priority: 'info'
        }
      }
    ];

    const randomUpdate = updates[Math.floor(Math.random() * updates.length)];
    this.emit('case_update', randomUpdate.data);
  }

  /**
   * Simulate court date reminders
   */
  simulateCourtDateReminder() {
    const reminders = [
      {
        type: 'court_reminder',
        data: {
          id: Math.floor(Math.random() * 1000),
          title: 'Court Date Reminder',
          message: 'You have a court hearing tomorrow at 2:00 PM',
          timestamp: new Date().toISOString(),
          priority: 'warning',
          courtDate: new Date(Date.now() + 24 * 60 * 60 * 1000).toISOString()
        }
      },
      {
        type: 'court_reminder',
        data: {
          id: Math.floor(Math.random() * 1000),
          title: 'Biometrics Appointment',
          message: 'Your biometrics appointment is scheduled for next week',
          timestamp: new Date().toISOString(),
          priority: 'info',
          appointmentDate: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000).toISOString()
        }
      }
    ];

    const randomReminder = reminders[Math.floor(Math.random() * reminders.length)];
    this.emit('court_reminder', randomReminder.data);
  }

  /**
   * Simulate document updates
   */
  simulateDocumentUpdate() {
    const updates = [
      {
        type: 'document_update',
        data: {
          id: Math.floor(Math.random() * 1000),
          title: 'Document Status Changed',
          message: 'Your I-485 form has been approved and is ready for download',
          timestamp: new Date().toISOString(),
          priority: 'success',
          documentId: Math.floor(Math.random() * 100)
        }
      },
      {
        type: 'document_update',
        data: {
          id: Math.floor(Math.random() * 1000),
          title: 'New Document Required',
          message: 'Please upload your financial disclosure documents',
          timestamp: new Date().toISOString(),
          priority: 'warning',
          dueDate: new Date(Date.now() + 3 * 24 * 60 * 60 * 1000).toISOString()
        }
      }
    ];

    const randomUpdate = updates[Math.floor(Math.random() * updates.length)];
    this.emit('document_update', randomUpdate.data);
  }

  /**
   * Simulate payment updates (for bondsman)
   */
  simulatePaymentUpdate() {
    const updates = [
      {
        type: 'payment_update',
        data: {
          id: Math.floor(Math.random() * 1000),
          title: 'Payment Received',
          message: 'Premium payment of $2,500 received from John Smith',
          timestamp: new Date().toISOString(),
          priority: 'success',
          amount: 2500,
          clientName: 'John Smith'
        }
      },
      {
        type: 'payment_update',
        data: {
          id: Math.floor(Math.random() * 1000),
          title: 'Payment Overdue',
          message: 'Premium payment is 5 days overdue for Maria Garcia',
          timestamp: new Date().toISOString(),
          priority: 'error',
          amount: 5000,
          clientName: 'Maria Garcia'
        }
      }
    ];

    const randomUpdate = updates[Math.floor(Math.random() * updates.length)];
    this.emit('payment_update', randomUpdate.data);
  }

  /**
   * Send a notification to a specific user
   */
  sendNotification(userId, type, data) {
    // In a real implementation, this would send via WebSocket
    console.log(`Sending notification to user ${userId}:`, { type, data });
    this.emit(type, { ...data, userId });
  }

  /**
   * Get connection status
   */
  getConnectionStatus() {
    return {
      isConnected: this.isConnected,
      userId: this.userId,
      userRole: this.userRole
    };
  }
}

// Create singleton instance
const notificationService = new NotificationService();

export default notificationService;
