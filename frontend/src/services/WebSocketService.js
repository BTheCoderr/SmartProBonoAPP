import { io } from 'socket.io-client';

class WebSocketService {
  static instance = null;
  socket = null;
  listeners = new Map();

  static getInstance() {
    if (!WebSocketService.instance) {
      WebSocketService.instance = new WebSocketService();
    }
    return WebSocketService.instance;
  }

  connect(url = process.env.REACT_APP_WS_URL || 'ws://localhost:3001') {
    if (!this.socket) {
      this.socket = io(url, {
        transports: ['websocket'],
        autoConnect: true
      });

      this.socket.on('connect', () => {
        console.log('WebSocket connected');
      });

      this.socket.on('analytics_update', (data) => {
        this.notifyListeners('analytics_update', data);
      });

      this.socket.on('form_activity', (data) => {
        this.notifyListeners('form_activity', data);
      });

      this.socket.on('error', (error) => {
        console.error('WebSocket error:', error);
        this.notifyListeners('error', error);
      });
    }
  }

  disconnect() {
    if (this.socket) {
      this.socket.disconnect();
      this.socket = null;
    }
  }

  subscribe(event, callback) {
    if (!this.listeners.has(event)) {
      this.listeners.set(event, new Set());
    }
    this.listeners.get(event).add(callback);

    return () => {
      const eventListeners = this.listeners.get(event);
      if (eventListeners) {
        eventListeners.delete(callback);
      }
    };
  }

  notifyListeners(event, data) {
    const eventListeners = this.listeners.get(event);
    if (eventListeners) {
      eventListeners.forEach(callback => callback(data));
    }
  }

  emit(event, data) {
    if (this.socket) {
      this.socket.emit(event, data);
    }
  }
}

export default WebSocketService.getInstance(); 