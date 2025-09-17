/**
 * React Hook for WebSocket functionality
 * Provides easy integration with WebSocket service in React components
 */

import { useState, useEffect, useCallback, useRef } from 'react';
import webSocketService from '../services/WebSocketService';

export const useWebSocket = (autoConnect = true) => {
  const [isConnected, setIsConnected] = useState(false);
  const [clientId, setClientId] = useState(null);
  const [rooms, setRooms] = useState(new Set());
  const [messages, setMessages] = useState([]);
  const [notifications, setNotifications] = useState([]);
  const [error, setError] = useState(null);
  
  const messageHandlersRef = useRef(new Map());

  // Connect to WebSocket
  const connect = useCallback((serverUrl) => {
    webSocketService.connect(serverUrl);
  }, []);

  // Disconnect from WebSocket
  const disconnect = useCallback(() => {
    webSocketService.disconnect();
  }, []);

  // Join a room
  const joinRoom = useCallback((roomId) => {
    webSocketService.joinRoom(roomId);
  }, []);

  // Leave a room
  const leaveRoom = useCallback((roomId) => {
    webSocketService.leaveRoom(roomId);
  }, []);

  // Send chat message
  const sendChatMessage = useCallback((roomId, message, sender) => {
    webSocketService.sendChatMessage(roomId, message, sender);
  }, []);

  // Send document update
  const sendDocumentUpdate = useCallback((roomId, documentId, changes) => {
    webSocketService.sendDocumentUpdate(roomId, documentId, changes);
  }, []);

  // Get room history
  const getRoomHistory = useCallback((roomId, limit) => {
    webSocketService.getRoomHistory(roomId, limit);
  }, []);

  // Add message handler
  const addMessageHandler = useCallback((event, handler) => {
    webSocketService.on(event, handler);
    messageHandlersRef.current.set(event, handler);
  }, []);

  // Remove message handler
  const removeMessageHandler = useCallback((event, handler) => {
    webSocketService.off(event, handler);
    messageHandlersRef.current.delete(event);
  }, []);

  // Clear all message handlers
  const clearMessageHandlers = useCallback(() => {
    messageHandlersRef.current.forEach((handler, event) => {
      webSocketService.off(event, handler);
    });
    messageHandlersRef.current.clear();
  }, []);

  // Set up event listeners
  useEffect(() => {
    const handleConnection = (data) => {
      setIsConnected(true);
      setClientId(data.client_id);
      setError(null);
    };

    const handleDisconnection = () => {
      setIsConnected(false);
      setClientId(null);
    };

    const handleError = (data) => {
      setError(data.error);
    };

    const handleRoomJoined = (data) => {
      setRooms(prev => new Set([...prev, data.room_id]));
    };

    const handleRoomLeft = (data) => {
      setRooms(prev => {
        const newRooms = new Set(prev);
        newRooms.delete(data.room_id);
        return newRooms;
      });
    };

    const handleChatMessage = (data) => {
      setMessages(prev => [...prev, {
        id: Date.now(),
        type: 'chat',
        ...data,
        timestamp: new Date().toISOString()
      }]);
    };

    const handleNotification = (data) => {
      setNotifications(prev => [...prev, {
        id: Date.now(),
        type: 'notification',
        ...data,
        timestamp: new Date().toISOString()
      }]);
    };

    const handleCaseUpdate = (data) => {
      setNotifications(prev => [...prev, {
        id: Date.now(),
        type: 'case_update',
        ...data,
        timestamp: new Date().toISOString()
      }]);
    };

    // Add event listeners
    addMessageHandler('connected', handleConnection);
    addMessageHandler('disconnected', handleDisconnection);
    addMessageHandler('error', handleError);
    addMessageHandler('room_joined', handleRoomJoined);
    addMessageHandler('room_left', handleRoomLeft);
    addMessageHandler('chat_message', handleChatMessage);
    addMessageHandler('notification_received', handleNotification);
    addMessageHandler('case_updated', handleCaseUpdate);

    // Auto-connect if enabled
    if (autoConnect && !isConnected) {
      connect();
    }

    // Cleanup on unmount
    return () => {
      clearMessageHandlers();
      if (autoConnect) {
        disconnect();
      }
    };
  }, [autoConnect, connect, disconnect, addMessageHandler, clearMessageHandlers, isConnected]);

  return {
    // Connection state
    isConnected,
    clientId,
    rooms: Array.from(rooms),
    error,
    
    // Messages and notifications
    messages,
    notifications,
    
    // Connection methods
    connect,
    disconnect,
    
    // Room methods
    joinRoom,
    leaveRoom,
    isInRoom: (roomId) => rooms.has(roomId),
    
    // Messaging methods
    sendChatMessage,
    sendDocumentUpdate,
    getRoomHistory,
    
    // Event handling
    addMessageHandler,
    removeMessageHandler,
    clearMessageHandlers,
    
    // Utility methods
    clearMessages: () => setMessages([]),
    clearNotifications: () => setNotifications([]),
    clearError: () => setError(null)
  };
};

export const useChat = (roomId) => {
  const { 
    isConnected, 
    messages, 
    sendChatMessage, 
    joinRoom, 
    leaveRoom, 
    isInRoom,
    getRoomHistory 
  } = useWebSocket();

  const [isJoined, setIsJoined] = useState(false);

  // Auto-join room when roomId changes
  useEffect(() => {
    if (roomId && isConnected && !isInRoom(roomId)) {
      joinRoom(roomId);
      setIsJoined(true);
    } else if (!roomId && isJoined) {
      leaveRoom(roomId);
      setIsJoined(false);
    }
  }, [roomId, isConnected, isInRoom, joinRoom, leaveRoom, isJoined]);

  // Filter messages for this room
  const roomMessages = messages.filter(msg => msg.room_id === roomId);

  const sendMessage = useCallback((message, sender) => {
    if (roomId && isConnected) {
      sendChatMessage(roomId, message, sender);
    }
  }, [roomId, isConnected, sendChatMessage]);

  const loadHistory = useCallback((limit = 50) => {
    if (roomId && isConnected) {
      getRoomHistory(roomId, limit);
    }
  }, [roomId, isConnected, getRoomHistory]);

  return {
    isConnected,
    isJoined,
    messages: roomMessages,
    sendMessage,
    loadHistory
  };
};

export const useNotifications = () => {
  const { notifications, clearNotifications } = useWebSocket();

  const unreadCount = notifications.filter(n => !n.read).length;

  const markAsRead = useCallback((notificationId) => {
    // This would typically update the notification in a backend
    console.log('Mark notification as read:', notificationId);
  }, []);

  const markAllAsRead = useCallback(() => {
    // This would typically update all notifications in a backend
    console.log('Mark all notifications as read');
  }, []);

  return {
    notifications,
    unreadCount,
    markAsRead,
    markAllAsRead,
    clearNotifications
  };
};

export const useDocumentCollaboration = (documentId, roomId) => {
  const { 
    isConnected, 
    sendDocumentUpdate, 
    addMessageHandler, 
    removeMessageHandler 
  } = useWebSocket();

  const [documentChanges, setDocumentChanges] = useState([]);
  const [isCollaborating, setIsCollaborating] = useState(false);

  // Handle document updates
  useEffect(() => {
    const handleDocumentUpdate = (data) => {
      if (data.document_id === documentId) {
        setDocumentChanges(prev => [...prev, {
          id: Date.now(),
          ...data,
          timestamp: new Date().toISOString()
        }]);
      }
    };

    addMessageHandler('document_updated', handleDocumentUpdate);

    return () => {
      removeMessageHandler('document_updated', handleDocumentUpdate);
    };
  }, [documentId, addMessageHandler, removeMessageHandler]);

  const sendChanges = useCallback((changes) => {
    if (roomId && documentId && isConnected) {
      sendDocumentUpdate(roomId, documentId, changes);
    }
  }, [roomId, documentId, isConnected, sendDocumentUpdate]);

  const startCollaboration = useCallback(() => {
    setIsCollaborating(true);
  }, []);

  const stopCollaboration = useCallback(() => {
    setIsCollaborating(false);
  }, []);

  return {
    isConnected,
    isCollaborating,
    documentChanges,
    sendChanges,
    startCollaboration,
    stopCollaboration
  };
};

export default useWebSocket;
