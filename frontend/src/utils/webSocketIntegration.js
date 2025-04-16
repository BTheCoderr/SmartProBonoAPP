import { useEffect, useState } from 'react';
import socketService from '../services/socket';
import { logInfo, logError } from './logger';

/**
 * Custom hook to integrate WebSocket functionality in React components.
 * 
 * @param {Object} options - Configuration options
 * @param {string[]} options.events - Array of event names to listen for
 * @param {Function} options.onMessage - Callback function for all messages
 * @param {Object} options.eventHandlers - Object mapping event names to handler functions
 * @param {boolean} options.autoConnect - Whether to connect automatically (default: true)
 * @param {Function} options.onConnected - Callback when connection is established
 * @param {Function} options.onDisconnected - Callback when connection is lost
 * @param {Function} options.onError - Callback when connection error occurs
 * @returns {Object} WebSocket utilities and state
 */
export const useWebSocket = ({
  events = [],
  onMessage,
  eventHandlers = {},
  autoConnect = true,
  onConnected,
  onDisconnected,
  onError
}) => {
  const [isConnected, setIsConnected] = useState(false);
  const [isConnecting, setIsConnecting] = useState(false);
  const [error, setError] = useState(null);
  const [lastMessage, setLastMessage] = useState(null);

  // Initialize the socket connection on component mount
  useEffect(() => {
    if (autoConnect) {
      connect();
    }

    // Clean up the socket connection on component unmount
    return () => {
      disconnect();
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  // Connect to the WebSocket server
  const connect = () => {
    try {
      setIsConnecting(true);
      setError(null);
      
      // Initialize the socket connection
      socketService.initSocket();
      
      // Set up connection event handlers
      socketService.on('connect', () => {
        setIsConnected(true);
        setIsConnecting(false);
        logInfo('WebSocket connected');
        if (onConnected) onConnected();
      });
      
      socketService.on('connect_error', (err) => {
        setError(err);
        setIsConnected(false);
        setIsConnecting(false);
        logError('WebSocket connection error:', err);
        if (onError) onError(err);
      });
      
      socketService.on('disconnect', (reason) => {
        setIsConnected(false);
        logInfo(`WebSocket disconnected: ${reason}`);
        if (onDisconnected) onDisconnected(reason);
      });
      
      // Set up event handlers for specific events
      events.forEach(event => {
        socketService.on(event, (data) => {
          setLastMessage({ event, data });
          if (onMessage) onMessage(event, data);
          if (eventHandlers[event]) eventHandlers[event](data);
        });
      });
      
    } catch (err) {
      setError(err);
      setIsConnecting(false);
      logError('Error initializing WebSocket:', err);
      if (onError) onError(err);
    }
  };

  // Disconnect from the WebSocket server
  const disconnect = () => {
    try {
      // Remove all event listeners
      events.forEach(event => {
        socketService.off(event);
      });
      
      // Special events
      socketService.off('connect');
      socketService.off('connect_error');
      socketService.off('disconnect');
      
      // Close the connection
      socketService.close();
      
      setIsConnected(false);
    } catch (err) {
      logError('Error disconnecting WebSocket:', err);
    }
  };

  // Send a message through the WebSocket connection
  const sendMessage = (event, data) => {
    if (!isConnected) {
      setError(new Error('Cannot send message: WebSocket is not connected'));
      return false;
    }
    
    try {
      return socketService.sendMessage({
        type: event,
        data: data
      });
    } catch (err) {
      setError(err);
      logError('Error sending WebSocket message:', err);
      return false;
    }
  };

  return {
    isConnected,
    isConnecting,
    error,
    lastMessage,
    connect,
    disconnect,
    sendMessage
  };
};

/**
 * Add WebSocket functionality to a React component
 * This is a HOC (Higher Order Component) that wraps a component with WebSocket functionality
 * 
 * @param {React.Component} Component - The component to wrap
 * @param {Object} options - WebSocket configuration options
 * @returns {React.Component} Enhanced component with WebSocket functionality
 */
export const withWebSocket = (Component, options = {}) => {
  const WithWebSocket = (props) => {
    const webSocket = useWebSocket(options);
    return <Component {...props} webSocket={webSocket} />;
  };
  
  // Set display name for debugging
  WithWebSocket.displayName = `WithWebSocket(${Component.displayName || Component.name || 'Component'})`;
  
  return WithWebSocket;
};

export default {
  useWebSocket,
  withWebSocket
}; 