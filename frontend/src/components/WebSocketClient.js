import React, { useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { initializeSocket, disconnectSocket } from '../services/socket';
import config from '../config';

const WebSocketClient = () => {
  const { currentUser, isAuthenticated } = useAuth();

  useEffect(() => {
    // Only initialize if WebSocket feature is enabled AND user is authenticated
    if (config.features.enableWebSocket && isAuthenticated && currentUser?.id) {
      console.log('WebSocketClient: Initializing socket for user', currentUser.id);
      
      // Initialize socket with user ID
      initializeSocket(currentUser.id)
        .then(() => {
          console.log('WebSocketClient: Socket connection established successfully');
        })
        .catch(error => {
          console.error('WebSocketClient: Failed to initialize socket connection:', error);
        });
      
      // Cleanup on unmount
      return () => {
        console.log('WebSocketClient: Disconnecting socket');
        disconnectSocket();
      };
    }
  }, [currentUser, isAuthenticated]);

  // No need to render anything
  return null;
};

export default WebSocketClient; 