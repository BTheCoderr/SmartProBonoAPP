import React, { createContext, useContext, useState, useEffect, useCallback } from 'react';
import PropTypes from 'prop-types';
import { io } from 'socket.io-client';
import { logInfo, logError, logWarn as logWarning } from '../utils/logger';
import { useAuth } from './AuthContext';
import config from '../config';

// Create context
const WebSocketContext = createContext(null);

// Custom hook to use the WebSocket context
export const useWebSocket = () => useContext(WebSocketContext);

export const WebSocketProvider = ({ children }) => {
  const { isAuthenticated, token, user } = useAuth();
  const [socket, setSocket] = useState(null);
  const [isConnected, setIsConnected] = useState(false);
  const [lastMessage, setLastMessage] = useState(null);
  const [caseUpdates, setCaseUpdates] = useState([]);
  
  // Event listeners map
  const [eventListeners, setEventListeners] = useState({});

  // Initialize the socket connection
  const initSocket = useCallback(() => {
    if (!isAuthenticated || !token) return;

    // Close existing socket if any
    if (socket) {
      socket.disconnect();
    }

    // Create new socket connection
    const newSocket = io(config.apiUrl, {
      transports: ['websocket', 'polling'],
      reconnection: true,
      reconnectionAttempts: 5,
      reconnectionDelay: 1000,
      reconnectionDelayMax: 5000,
      timeout: 20000,
      auth: {
        token
      }
    });

    // Set up event handlers
    newSocket.on('connect', () => {
      console.log('WebSocket connected');
      setIsConnected(true);
      
      // Join the user's personal channel for updates
      if (user && user.id) {
        newSocket.emit('join_user_channel', { user_id: user.id });
      }
    });

    newSocket.on('disconnect', () => {
      console.log('WebSocket disconnected');
      setIsConnected(false);
    });

    newSocket.on('error', (error) => {
      console.error('WebSocket error:', error);
    });

    newSocket.on('message', (message) => {
      console.log('Received message:', message);
      setLastMessage(message);
    });
    
    // Handle case specific events
    newSocket.on('case_updated', (data) => {
      console.log('Case updated:', data);
      setCaseUpdates((prevUpdates) => [data, ...prevUpdates].slice(0, 10));
      triggerEventListeners('case_updated', data);
    });
    
    newSocket.on('case_created', (data) => {
      console.log('Case created:', data);
      setCaseUpdates((prevUpdates) => [data, ...prevUpdates].slice(0, 10));
      triggerEventListeners('case_created', data);
    });
    
    newSocket.on('case_status_changed', (data) => {
      console.log('Case status changed:', data);
      setCaseUpdates((prevUpdates) => [data, ...prevUpdates].slice(0, 10));
      triggerEventListeners('case_status_changed', data);
    });
    
    newSocket.on('case_priority_changed', (data) => {
      console.log('Case priority changed:', data);
      setCaseUpdates((prevUpdates) => [data, ...prevUpdates].slice(0, 10));
      triggerEventListeners('case_priority_changed', data);
    });
    
    newSocket.on('case_assigned', (data) => {
      console.log('Case assigned:', data);
      setCaseUpdates((prevUpdates) => [data, ...prevUpdates].slice(0, 10));
      triggerEventListeners('case_assigned', data);
    });

    setSocket(newSocket);
    
    // Cleanup function
    return () => {
      if (newSocket) {
        newSocket.disconnect();
      }
    };
  }, [isAuthenticated, token, user]);

  // Call initSocket when auth state changes
  useEffect(() => {
    if (isAuthenticated && token) {
      initSocket();
    }
    
    return () => {
      if (socket) {
        socket.disconnect();
        setSocket(null);
      }
    };
  }, [isAuthenticated, token, initSocket]);

  // Function to add event listeners
  const addEventListener = useCallback((event, callback) => {
    setEventListeners((prevListeners) => {
      const existingListeners = prevListeners[event] || [];
      return {
        ...prevListeners,
        [event]: [...existingListeners, callback]
      };
    });
    
    // Cleanup function to remove the listener
    return () => {
      setEventListeners((prevListeners) => {
        const existingListeners = prevListeners[event] || [];
        return {
          ...prevListeners,
          [event]: existingListeners.filter(cb => cb !== callback)
        };
      });
    };
  }, []);
  
  // Function to trigger event listeners
  const triggerEventListeners = useCallback((event, data) => {
    if (eventListeners[event]) {
      eventListeners[event].forEach(callback => {
        try {
          callback(data);
        } catch (error) {
          console.error(`Error in ${event} event listener:`, error);
        }
      });
    }
  }, [eventListeners]);

  // Function to send a message over socket
  const sendMessage = useCallback((event, data) => {
    if (socket && isConnected) {
      socket.emit(event, data);
        return true;
      }
    return false;
  }, [socket, isConnected]);
  
  // Function to join a specific case room for updates
  const joinCaseRoom = useCallback((caseId) => {
    if (socket && isConnected && caseId) {
      socket.emit('join_case_room', { case_id: caseId });
      console.log(`Joined case room for case ${caseId}`);
      return true;
    }
    return false;
  }, [socket, isConnected]);
  
  // Function to leave a specific case room
  const leaveCaseRoom = useCallback((caseId) => {
    if (socket && isConnected && caseId) {
      socket.emit('leave_case_room', { case_id: caseId });
      console.log(`Left case room for case ${caseId}`);
      return true;
    }
    return false;
  }, [socket, isConnected]);
  
  // Clear case updates
  const clearCaseUpdates = useCallback(() => {
    setCaseUpdates([]);
  }, []);
  
  const value = {
    socket,
    isConnected,
    lastMessage,
    caseUpdates,
    addEventListener,
    sendMessage,
    joinCaseRoom,
    leaveCaseRoom,
    clearCaseUpdates
  };

  return <WebSocketContext.Provider value={value}>{children}</WebSocketContext.Provider>;
};

WebSocketProvider.propTypes = {
  children: PropTypes.node.isRequired
};

export default WebSocketContext; 