/**
 * WebSocket Service for Real-Time Features
 * Handles real-time notifications, live chat, and document collaboration
 */

class WebSocketService {
  constructor() {
    this.ws = null;
    this.clientId = null;
    this.rooms = new Set();
    this.messageHandlers = new Map();
    this.reconnectAttempts = 0;
    this.maxReconnectAttempts = 5;
    this.reconnectDelay = 1000;
    this.isConnected = false;
  }

  /**
   * Connect to WebSocket server
   */
  connect(serverUrl = 'ws://localhost:8765') {
    try {
      this.ws = new WebSocket(serverUrl);
      
      this.ws.onopen = (event) => {
        console.log('WebSocket connected');
        this.isConnected = true;
        this.reconnectAttempts = 0;
        this.emit('connected', { event });
      };

      this.ws.onmessage = (event) => {
        try {
          const message = JSON.parse(event.data);
          this.handleMessage(message);
        } catch (error) {
          console.error('Error parsing WebSocket message:', error);
        }
      };

      this.ws.onclose = (event) => {
        console.log('WebSocket disconnected');
        this.isConnected = false;
        this.emit('disconnected', { event });
        
        // Attempt to reconnect
        if (this.reconnectAttempts < this.maxReconnectAttempts) {
          this.reconnectAttempts++;
          console.log(`Attempting to reconnect (${this.reconnectAttempts}/${this.maxReconnectAttempts})...`);
          setTimeout(() => this.connect(serverUrl), this.reconnectDelay * this.reconnectAttempts);
        }
      };

      this.ws.onerror = (error) => {
        console.error('WebSocket error:', error);
        this.emit('error', { error });
      };

    } catch (error) {
      console.error('Error connecting to WebSocket:', error);
      this.emit('error', { error });
    }
  }

  /**
   * Disconnect from WebSocket server
   */
  disconnect() {
    if (this.ws) {
      this.ws.close();
      this.ws = null;
      this.isConnected = false;
    }
  }

  /**
   * Send message to server
   */
  send(type, data = {}) {
    if (this.ws && this.isConnected) {
      const message = {
        type,
        ...data,
        timestamp: new Date().toISOString()
      };
      this.ws.send(JSON.stringify(message));
    } else {
      console.warn('WebSocket not connected. Cannot send message.');
    }
  }

  /**
   * Handle incoming messages
   */
  handleMessage(message) {
    const { message_type, data } = message;
    
    // Update client ID if provided
    if (data.client_id) {
      this.clientId = data.client_id;
    }

    // Emit message to handlers
    this.emit(message_type, data);

    // Handle specific message types
    switch (message_type) {
      case 'connection':
        this.clientId = data.client_id;
        this.emit('connection_established', data);
        break;
      
      case 'room_joined':
        this.rooms.add(data.room_id);
        this.emit('room_joined', data);
        break;
      
      case 'room_left':
        this.rooms.delete(data.room_id);
        this.emit('room_left', data);
        break;
      
      case 'chat':
        this.emit('chat_message', data);
        break;
      
      case 'document_update':
        this.emit('document_updated', data);
        break;
      
      case 'notification':
        this.emit('notification_received', data);
        break;
      
      case 'case_update':
        this.emit('case_updated', data);
        break;
      
      case 'error':
        this.emit('server_error', data);
        break;
      
      default:
        console.log('Unknown message type:', message_type, data);
    }
  }

  /**
   * Join a room
   */
  joinRoom(roomId) {
    this.send('join_room', { room_id: roomId });
  }

  /**
   * Leave a room
   */
  leaveRoom(roomId) {
    this.send('leave_room', { room_id: roomId });
  }

  /**
   * Send chat message
   */
  sendChatMessage(roomId, message, sender = 'Anonymous') {
    this.send('chat_message', {
      room_id: roomId,
      message,
      sender
    });
  }

  /**
   * Send document update
   */
  sendDocumentUpdate(roomId, documentId, changes) {
    this.send('document_update', {
      room_id: roomId,
      document_id: documentId,
      document_data: changes
    });
  }

  /**
   * Get room history
   */
  getRoomHistory(roomId, limit = 50) {
    this.send('get_history', {
      room_id: roomId,
      limit
    });
  }

  /**
   * Get server statistics
   */
  getStats() {
    this.send('get_stats');
  }

  /**
   * Event handling
   */
  on(event, handler) {
    if (!this.messageHandlers.has(event)) {
      this.messageHandlers.set(event, []);
    }
    this.messageHandlers.get(event).push(handler);
  }

  off(event, handler) {
    if (this.messageHandlers.has(event)) {
      const handlers = this.messageHandlers.get(event);
      const index = handlers.indexOf(handler);
      if (index > -1) {
        handlers.splice(index, 1);
      }
    }
  }

  emit(event, data) {
    if (this.messageHandlers.has(event)) {
      this.messageHandlers.get(event).forEach(handler => {
        try {
          handler(data);
        } catch (error) {
          console.error('Error in message handler:', error);
        }
      });
    }
  }

  /**
   * Utility methods
   */
  isConnectedToRoom(roomId) {
    return this.rooms.has(roomId);
  }

  getConnectedRooms() {
    return Array.from(this.rooms);
  }

  getClientId() {
    return this.clientId;
  }

  getConnectionStatus() {
    return this.isConnected;
  }
}

// Create singleton instance
const webSocketService = new WebSocketService();

export default webSocketService;