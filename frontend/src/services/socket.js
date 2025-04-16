import { io } from 'socket.io-client';
import config from '../config';
import { logger } from '../utils/logger';

/**
 * WebSocket service for handling Socket.IO connections
 */
class WebSocketService {
  constructor() {
    this.socket = null;
    this.isConnected = false;
    this.events = new Map();
    this.defaultOptions = {
      transports: ['websocket', 'polling'],
      reconnection: true,
      reconnectionAttempts: 5,
      reconnectionDelay: 1000,
      reconnectionDelayMax: 5000,
      timeout: 20000,
      autoConnect: true,
      forceNew: true,
    };
  }

  /**
   * Initialize the Socket.IO connection
   * @param {Object} options - Optional connection options
   * @returns {boolean} - Whether the initialization was successful
   */
  initSocket(options = {}) {
    if (!config.features.enableWebSocket) {
      logger.info('WebSocket feature is disabled');
      return false;
    }

    if (this.socket) {
      logger.info('Socket already initialized, closing existing connection');
      this.close();
    }

    try {
      // Close any existing connection
      if (this.socket) {
        this.close();
      }

      // Determine the URL to connect to
      const url = config.apiUrl;
      
      // Merge default options with provided options
      const connectionOptions = { 
        ...this.defaultOptions,
        ...options 
      };
      
      // Add auth token if provided
      if (options.token) {
        connectionOptions.auth = { token: options.token };
        logger.info('Using authentication token for WebSocket connection');
      } else {
        // For unauthenticated connections, use the public flag
        connectionOptions.query = { public: 'true' };
        logger.info('Using public WebSocket connection (no auth)');
      }
      
      // Create new Socket.IO connection
      this.socket = io(url, connectionOptions);
      
      // Set up internal handlers for connection events
      this.socket.on('connect', () => {
        this.isConnected = true;
        logger.info('WebSocket connected successfully');
        this._triggerEvent('connect', { connected: true });
      });
      
      this.socket.on('disconnect', (reason) => {
        this.isConnected = false;
        logger.info('WebSocket disconnected:', reason);
        this._triggerEvent('disconnect', { reason });
      });
      
      this.socket.on('connect_error', (error) => {
        this.isConnected = false;
        logger.error('WebSocket connection error:', error.message);
        this._triggerEvent('connect_error', { message: error.message });
      });
      
      this.socket.on('connection_error', (data) => {
        logger.error('Authentication error:', data.message);
        this._triggerEvent('auth_error', { message: data.message });
      });
      
      return true;
    } catch (error) {
      logger.error('Error initializing socket:', error);
      return false;
    }
  }

  /**
   * Set up a handler for connection open event
   * @param {Function} callback - Function to call when connection opens
   */
  onOpen(callback) {
    if (!this.socket) {
      logger.warn('Socket not initialized');
      return null;
    }
    
    return this.on('connect', callback);
  }
  
  /**
   * Set up a handler for connection error event
   * @param {Function} callback - Function to call when connection error occurs
   */
  onError(callback) {
    if (!this.socket) {
      logger.warn('Socket not initialized');
      return null;
    }
    
    return this.on('connect_error', callback);
  }
  
  /**
   * Set up a handler for connection close event
   * @param {Function} callback - Function to call when connection closes
   */
  onClose(callback) {
    if (!this.socket) {
      logger.warn('Socket not initialized');
      return null;
    }
    
    return this.on('disconnect', callback);
  }

  /**
   * Trigger a saved event callback
   * @param {string} eventType - Event type to trigger
   * @param {any} data - Data to pass to the callback
   */
  _triggerEvent(eventType, data) {
    if (this.events.has(eventType)) {
      const callbacks = this.events.get(eventType);
      callbacks.forEach(callback => {
        try {
          callback(data);
        } catch (error) {
          logger.error(`Error in ${eventType} handler:`, error);
        }
      });
    }
  }

  /**
   * Register an event listener
   * @param {string} eventType - Event type to listen for
   * @param {Function} callback - Callback function to execute when event occurs
   * @returns {Function|null} - Function to remove the listener or null if error
   */
  on(eventType, callback) {
    if (!this.socket) {
      logger.warn('Socket not initialized');
      return null;
    }
    
    try {
      // Store callback in our event map
      if (!this.events.has(eventType)) {
        this.events.set(eventType, new Set());
      }
      this.events.get(eventType).add(callback);
      
      // Register with Socket.IO
      this.socket.on(eventType, (data) => {
        this._triggerEvent(eventType, data);
      });
      
      // Return function to remove this specific listener
      return () => this.off(eventType, callback);
    } catch (error) {
      logger.error(`Error registering ${eventType} listener:`, error);
      return null;
    }
  }

  /**
   * Remove an event listener
   * @param {string} eventType - Event type to remove listener for
   * @param {Function} callback - Callback function to remove
   */
  off(eventType, callback) {
    if (!this.socket) {
      logger.warn('Socket not initialized');
      return;
    }
    
    try {
      // If we have this event type stored
      if (this.events.has(eventType)) {
        const callbacks = this.events.get(eventType);
        
        if (callback) {
          // Remove specific callback
          callbacks.delete(callback);
        } else {
          // Remove all callbacks for this event
          this.events.delete(eventType);
        }
      }
      
      // If no callback provided, remove all listeners for this event
      if (!callback) {
        this.socket.off(eventType);
      }
    } catch (error) {
      logger.error(`Error removing ${eventType} listener:`, error);
    }
  }

  /**
   * Send a message through the socket
   * @param {Object} message - Message to send
   * @returns {boolean} - Whether the message was sent successfully
   */
  sendMessage(message) {
    if (!this.socket) {
      logger.warn('Socket not initialized');
      return false;
    }
    
    try {
      if (typeof message === 'string') {
        // Simple string message
        this.socket.emit('message', message);
      } else if (typeof message === 'object') {
        // Object with type and data
        const { type, data } = message;
        if (!type) {
          logger.error('Message object must have a type property');
          return false;
        }
        this.socket.emit(type, data || {});
      } else {
        logger.error('Invalid message format');
        return false;
      }
      return true;
    } catch (error) {
      logger.error('Error sending message:', error);
      return false;
    }
  }

  /**
   * Close the socket connection
   */
  close() {
    if (this.socket) {
      try {
        this.socket.disconnect();
        this.socket = null;
        this.isConnected = false;
        
        // Clear all events
        this.events.clear();
      } catch (error) {
        logger.error('Error closing socket:', error);
      }
    }
  }

  /**
   * Check if socket is connected
   * @returns {boolean} - Whether the socket is connected
   */
  isSocketConnected() {
    return this.socket && this.socket.connected;
  }

  /**
   * Reconnect to the server with the same URL and options
   * @returns {boolean} - Whether reconnection was successful
   */
  reconnect() {
    if (this.socket) {
      try {
        this.socket.connect();
        return true;
      } catch (error) {
        logger.error('Error reconnecting socket:', error);
        return false;
      }
    }
    return false;
  }
}

// Export the WebSocketService class instead of a singleton instance
export default WebSocketService;
