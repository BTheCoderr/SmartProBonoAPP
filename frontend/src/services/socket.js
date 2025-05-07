import { io } from 'socket.io-client';
import config from '../config';

let socket = null;
let isConnected = false;
let reconnectAttempts = 0;
const MAX_RECONNECT_ATTEMPTS = 5;
let heartbeatInterval = null;
const HEARTBEAT_INTERVAL = 30000; // 30 seconds

// Event handlers store
const eventHandlers = {
  'notification': [],
  'direct_message': [],
  'connect': [],
  'disconnect': [],
  'connect_error': [],
  'reconnecting': [],
  'reconnect_failed': []
};

/**
 * Start heartbeat to detect disconnections
 */
const startHeartbeat = () => {
  if (heartbeatInterval) {
    clearInterval(heartbeatInterval);
  }
  
  heartbeatInterval = setInterval(() => {
    if (socket && isConnected) {
      // Use a timeout to handle unresponsive pings
      const timeoutId = setTimeout(() => {
        console.warn('Heartbeat timeout - no response received');
        if (socket) {
          socket.disconnect().connect();
        }
      }, 5000); // 5 second timeout

      socket.emit('ping', {}, (response) => {
        clearTimeout(timeoutId);
        if (!response) {
          console.warn('Invalid heartbeat response');
          if (socket) {
            socket.disconnect().connect();
          }
        }
      });
    }
  }, HEARTBEAT_INTERVAL);
};

/**
 * Stop heartbeat
 */
const stopHeartbeat = () => {
  if (heartbeatInterval) {
    clearInterval(heartbeatInterval);
    heartbeatInterval = null;
  }
};

/**
 * Initialize the Socket.IO connection
 * @param {string} userId - The user ID to register with the server
 * @returns {Promise} - Resolves when connected and registered, rejects on error
 */
export const initializeSocket = (userId) => {
  return new Promise((resolve, reject) => {
    if (!config.features.enableWebSocket) {
      console.log('WebSocket is disabled in config');
      return reject(new Error('WebSocket is disabled'));
    }

    // Don't initialize again if already connected
    if (isConnected && socket) {
      console.log('Socket already connected');
      return resolve(socket);
    }

    console.log(`Initializing Socket.IO connection to ${config.wsUrl}`);
    
    // Cleanup any existing socket
    if (socket) {
      socket.disconnect();
      socket = null;
    }
    
    // Create new socket connection
    socket = io(config.wsUrl, {
      transports: ['websocket'],
      reconnection: true,
      reconnectionDelay: 1000,
      reconnectionDelayMax: 5000,
      reconnectionAttempts: MAX_RECONNECT_ATTEMPTS,
      timeout: 10000, // Increased timeout for slow connections
    });

    // Setup connect handler
    socket.on('connect', () => {
      console.log('Socket connected!');
      isConnected = true;
      reconnectAttempts = 0;
      
      // Start heartbeat
      startHeartbeat();
      
      // Register the user if userId is provided
      if (userId) {
        registerUser(userId)
          .then(() => {
            console.log(`User ${userId} registered with socket server`);
            // Notify all connect handlers
            eventHandlers.connect.forEach(handler => {
              try {
                handler();
              } catch (error) {
                console.error('Error in connect handler:', error);
              }
            });
            resolve(socket);
          })
          .catch(error => {
            console.error('Failed to register user with socket:', error);
            reject(error);
          });
      } else {
        // If no userId provided, just resolve with the socket
        eventHandlers.connect.forEach(handler => {
          try {
            handler();
          } catch (error) {
            console.error('Error in connect handler:', error);
          }
        });
        resolve(socket);
      }
    });

    // Setup disconnect handler
    socket.on('disconnect', (reason) => {
      console.log(`Socket disconnected: ${reason}`);
      isConnected = false;
      
      // Stop heartbeat
      stopHeartbeat();
      
      // Notify all disconnect handlers
      eventHandlers.disconnect.forEach(handler => {
        try {
          handler(reason);
        } catch (error) {
          console.error('Error in disconnect handler:', error);
        }
      });
    });

    // Setup reconnecting handler
    socket.io.on('reconnect_attempt', (attempt) => {
      console.log(`Socket reconnection attempt ${attempt}`);
      // Notify all reconnecting handlers
      eventHandlers.reconnecting.forEach(handler => {
        try {
          handler(attempt);
        } catch (error) {
          console.error('Error in reconnecting handler:', error);
        }
      });
    });
    
    // Setup reconnect failure handler
    socket.io.on('reconnect_failed', () => {
      console.error('Socket reconnection failed after all attempts');
      // Notify all reconnect failed handlers
      eventHandlers.reconnect_failed.forEach(handler => {
        try {
          handler();
        } catch (error) {
          console.error('Error in reconnect_failed handler:', error);
        }
      });
    });

    // Setup error handler
    socket.on('connect_error', (error) => {
      console.error('Socket connection error:', error);
      reconnectAttempts++;
      
      // Notify all error handlers
      eventHandlers.connect_error.forEach(handler => {
        try {
          handler(error);
        } catch (handlerError) {
          console.error('Error in connect_error handler:', handlerError);
        }
      });
      
      // If exceeded max attempts, stop trying
      if (reconnectAttempts >= MAX_RECONNECT_ATTEMPTS) {
        console.error('Max reconnect attempts reached');
        socket.disconnect();
        reject(new Error('Failed to connect after maximum attempts'));
      }
    });

    // Setup notification handler
    socket.on('notification', (data) => {
      console.log('Received notification:', data);
      eventHandlers.notification.forEach(handler => {
        try {
          handler(data);
        } catch (error) {
          console.error('Error in notification handler:', error);
        }
      });
    });

    // Setup direct message handler
    socket.on('direct_message', (data) => {
      console.log('Received direct message:', data);
      eventHandlers.direct_message.forEach(handler => {
        try {
          handler(data);
        } catch (error) {
          console.error('Error in direct_message handler:', error);
        }
      });
    });
    
    // Setup ping handler for heartbeat
    socket.on('pong', () => {
      // Server responded to our ping
      console.debug('Received heartbeat pong from server');
    });
  });
};

/**
 * Register the user with the socket server
 * @param {string} userId - The user ID to register
 * @returns {Promise} - Resolves when registered, rejects on error
 */
export const registerUser = (userId) => {
  return new Promise((resolve, reject) => {
    if (!socket) {
      return reject(new Error('Socket not initialized'));
    }
    
    if (!isConnected) {
      return reject(new Error('Socket not connected'));
    }

    // Add timeout for registration
    const timeoutId = setTimeout(() => {
      reject(new Error('Registration timeout'));
    }, 10000); // 10 second timeout

    socket.emit('register', { user_id: userId }, (response) => {
      clearTimeout(timeoutId);
      if (response && response.status === 'success') {
        resolve(response);
      } else {
        reject(new Error('Registration failed: ' + (response?.error || 'Unknown error')));
      }
    });
  });
};

/**
 * Add event handler with timeout protection
 */
export const addSocketEventHandler = (event, handler) => {
  if (!eventHandlers[event]) {
    eventHandlers[event] = [];
  }
  
  // Wrap handler with timeout and error protection
  const wrappedHandler = async (...args) => {
    try {
      const result = handler(...args);
      if (result && typeof result.then === 'function') {
        // If handler returns a promise, add timeout
        const timeoutPromise = new Promise((_, reject) => {
          setTimeout(() => reject(new Error('Handler timeout')), 5000);
        });
        await Promise.race([result, timeoutPromise]);
      }
    } catch (error) {
      console.error(`Error in ${event} handler:`, error);
    }
  };
  
  eventHandlers[event].push(wrappedHandler);
};

/**
 * Remove an event handler for a specific event
 * @param {string} event - The event to remove the handler from
 * @param {Function} handler - The handler function to remove
 */
export const removeSocketEventHandler = (event, handler) => {
  if (!eventHandlers[event]) {
      return;
    }
  
  const index = eventHandlers[event].indexOf(handler);
  if (index !== -1) {
    eventHandlers[event].splice(index, 1);
  }
};

/**
 * Disconnect the socket
 */
export const disconnectSocket = () => {
  if (socket) {
    // Stop heartbeat
    stopHeartbeat();
    
    socket.disconnect();
    isConnected = false;
    socket = null;
  }
};

/**
 * Check if socket is connected
 * @returns {boolean} - Whether the socket is connected
 */
export const isSocketConnected = () => {
  return isConnected && socket && socket.connected;
};

/**
 * Get the socket instance
 * @returns {Object|null} - The socket instance or null if not connected
 */
export const getSocket = () => {
  return socket;
};

/**
 * Mark notifications as read
 * @param {string|string[]} notificationIds - The ID(s) of the notification(s) to mark as read
 * @returns {Promise} - Resolves when marked as read, rejects on error
 */
export const markNotificationsAsRead = (notificationIds) => {
  return new Promise((resolve, reject) => {
    if (!socket || !isConnected) {
      return reject(new Error('Socket not connected'));
    }

    const payload = Array.isArray(notificationIds) 
      ? { notification_ids: notificationIds }
      : { notification_id: notificationIds };
    
    socket.emit('mark_read', payload, (response) => {
      if (response && response.status === 'success') {
        resolve(response);
      } else {
        reject(new Error(response?.message || 'Failed to mark as read'));
      }
    });
  });
};

/**
 * Get user notifications
 * @param {Object} options - Options for fetching notifications
 * @param {number} options.limit - Maximum number of notifications to fetch
 * @param {boolean} options.unreadOnly - Whether to fetch only unread notifications
 * @returns {Promise} - Resolves with notifications, rejects on error
 */
export const getUserNotifications = (options = {}) => {
  return new Promise((resolve, reject) => {
    if (!socket || !isConnected) {
      return reject(new Error('Socket not connected'));
    }

    socket.emit('get_notifications', options, (response) => {
      if (response && response.status === 'success') {
        resolve(response.notifications || []);
      } else {
        reject(new Error(response?.message || 'Failed to get notifications'));
      }
    });
  });
}; 