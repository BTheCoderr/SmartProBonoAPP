import io from 'socket.io-client';
import config from '../config';
import { logInfo, logError, logDebug } from '../utils/logger';

class NotificationService {
  constructor() {
    this.socket = null;
    this.connected = false;
    this.authenticated = false;
    this.callbacks = {
      onNotification: [],
      onConnect: [],
      onDisconnect: [],
      onAuthenticated: [],
      onError: []
    };
  }

  connect() {
    if (this.socket) {
      return Promise.resolve(this.socket);
    }

    return new Promise((resolve, reject) => {
      try {
        logInfo('Connecting to WebSocket server', { url: config.apiUrl });
        
        this.socket = io(config.apiUrl, {
          transports: ['websocket', 'polling'],
          reconnection: true,
          reconnectionDelay: 1000,
          reconnectionDelayMax: 5000,
          reconnectionAttempts: 5
        });

        this.socket.on('connect', () => {
          this.connected = true;
          logInfo('WebSocket connected');
          this._triggerCallbacks('onConnect');
          resolve(this.socket);
        });

        this.socket.on('disconnect', () => {
          this.connected = false;
          this.authenticated = false;
          logInfo('WebSocket disconnected');
          this._triggerCallbacks('onDisconnect');
        });

        this.socket.on('connection_success', (data) => {
          logDebug('Connection success', data);
        });
        
        this.socket.on('auth_success', (data) => {
          this.authenticated = true;
          logInfo('WebSocket authenticated', data);
          this._triggerCallbacks('onAuthenticated', data);
        });
        
        this.socket.on('auth_error', (data) => {
          this.authenticated = false;
          logError('WebSocket authentication error', data);
          this._triggerCallbacks('onError', data);
        });
        
        this.socket.on('notification', (notification) => {
          logDebug('Received notification', notification);
          this._triggerCallbacks('onNotification', notification);
        });
        
        this.socket.on('error', (error) => {
          logError('WebSocket error', error);
          this._triggerCallbacks('onError', error);
        });

      } catch (error) {
        logError('Failed to connect to WebSocket', error);
        reject(error);
      }
    });
  }

  authenticate(userId) {
    if (!this.connected || !this.socket) {
      return Promise.reject(new Error('Socket not connected'));
    }

    return new Promise((resolve, reject) => {
      logInfo('Authenticating with WebSocket', { userId });
      
      // Set up a one-time auth success handler
      const onSuccess = (data) => {
        this.socket.off('auth_success', onSuccess);
        this.socket.off('auth_error', onError);
        resolve(data);
      };
      
      // Set up a one-time auth error handler
      const onError = (error) => {
        this.socket.off('auth_success', onSuccess);
        this.socket.off('auth_error', onError);
        reject(error);
      };
      
      this.socket.once('auth_success', onSuccess);
      this.socket.once('auth_error', onError);
      
      // Send authentication event
      this.socket.emit('authenticate', { user_id: userId });
    });
  }

  disconnect() {
    if (this.socket) {
      this.socket.disconnect();
      this.socket = null;
      this.connected = false;
      this.authenticated = false;
    }
  }

  onNotification(callback) {
    this._addCallback('onNotification', callback);
    return () => this._removeCallback('onNotification', callback);
  }

  onConnect(callback) {
    this._addCallback('onConnect', callback);
    return () => this._removeCallback('onConnect', callback);
  }

  onDisconnect(callback) {
    this._addCallback('onDisconnect', callback);
    return () => this._removeCallback('onDisconnect', callback);
  }

  onAuthenticated(callback) {
    this._addCallback('onAuthenticated', callback);
    return () => this._removeCallback('onAuthenticated', callback);
  }

  onError(callback) {
    this._addCallback('onError', callback);
    return () => this._removeCallback('onError', callback);
  }

  isConnected() {
    return this.connected;
  }

  isAuthenticated() {
    return this.authenticated;
  }

  // Private methods
  _addCallback(event, callback) {
    if (typeof callback === 'function' && this.callbacks[event]) {
      this.callbacks[event].push(callback);
    }
  }

  _removeCallback(event, callback) {
    if (this.callbacks[event]) {
      this.callbacks[event] = this.callbacks[event].filter(cb => cb !== callback);
    }
  }

  _triggerCallbacks(event, data) {
    if (this.callbacks[event]) {
      this.callbacks[event].forEach(callback => {
        try {
          callback(data);
        } catch (error) {
          logError(`Error in ${event} callback`, error);
        }
      });
    }
  }
}

// Singleton instance
const notificationService = new NotificationService();

export default notificationService; 