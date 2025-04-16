import React, { useEffect } from 'react';
import socketService from '../services/socket';
import config from '../config';
const WebSocketClient = () => {
  useEffect(() => {
    // Only initialize if WebSocket feature is enabled
    if (config.features.enableWebSocket) {
      socketService.initSocket();
      // Cleanup on unmount
      return () => {
        socketService.close();
      };
    }
  }, []);
  // No need to render anything
  return null;
};
export default WebSocketClient;