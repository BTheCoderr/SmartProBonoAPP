import React, { createContext, useState, useEffect, useContext, useMemo, useCallback } from 'react';
import axios from 'axios';
import { API_URL } from '../config';
import { initializeSocket, disconnectSocket, addSocketEventHandler, removeSocketEventHandler } from '../services/socket';
import { useNavigate } from 'react-router-dom';
import ApiService from '../services/ApiService';

// Create the Auth Context
const AuthContext = createContext(null);

// Custom hook to use the Auth Context
export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

// Auth Provider Component
export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [accessToken, setAccessToken] = useState(localStorage.getItem('access_token'));
  const [refreshToken, setRefreshToken] = useState(localStorage.getItem('refresh_token'));
  const [isLoggingOut, setIsLoggingOut] = useState(false);
  const [isRefreshing, setIsRefreshing] = useState(false);
  const [refreshAttempts, setRefreshAttempts] = useState(0);
  const [notifications, setNotifications] = useState([]);
  const [authError, setAuthError] = useState(null);
  const MAX_REFRESH_ATTEMPTS = 3;
  const navigate = useNavigate();

  // Define isTestMode first
  const isTestMode = useMemo(() => {
    return window.location.href.includes('scanner-test') || 
           window.location.href.includes('test-mode') || 
           process.env.NODE_ENV === 'development';
  }, []);

  // Then define logout
  const logout = useCallback(async () => {
    if (isLoggingOut) return; // Prevent multiple logout attempts
    
    setIsLoggingOut(true);
    try {
      // Only make the API call if not in test mode
      if (!isTestMode && accessToken) {
        await ApiService.post('/api/auth/logout', {}, {
          headers: { Authorization: `Bearer ${accessToken}` }
        });
      }
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      // Clear all auth state
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      setAccessToken(null);
      setRefreshToken(null);
      setUser(null);
      setIsLoggingOut(false);
      setRefreshAttempts(0);
      
      // Disconnect socket
      disconnectSocket();
      
      // Navigate to home
      navigate('/', { replace: true });
    }
  }, [navigate, isTestMode, accessToken, isLoggingOut]);

  // Function to refresh the access token
  const refreshAccessToken = useCallback(async () => {
    if (!refreshToken || isRefreshing) return null;
    
    try {
      setIsRefreshing(true);
      const response = await axios.post(`${API_URL}/api/auth/refresh`, {}, {
        headers: { Authorization: `Bearer ${refreshToken}` }
      });
      
      const newAccessToken = response.data.access_token;
      setAccessToken(newAccessToken);
      localStorage.setItem('access_token', newAccessToken);
      setRefreshAttempts(0);
      return newAccessToken;
    } catch (error) {
      setRefreshAttempts(prev => prev + 1);
      console.error('Token refresh error:', error);
      
      // If too many refresh attempts, log out
      if (refreshAttempts >= MAX_REFRESH_ATTEMPTS) {
        console.warn('Maximum refresh attempts reached. Logging out.');
        await logout();
      }
      return null;
    } finally {
      setIsRefreshing(false);
    }
  }, [refreshToken, isRefreshing, refreshAttempts, logout]);

  // Check auth status on initial load
  useEffect(() => {
    const checkAuth = async () => {
      if (!accessToken) {
        setUser(null);
        setLoading(false);
        return;
      }
      
      try {
        const response = await axios.get(`${API_URL}/api/auth/me`, {
          headers: { Authorization: `Bearer ${accessToken}` }
        });
        
        setUser(response.data.user);
      } catch (error) {
        console.error('Auth check error:', error);
        
        // Try to refresh token if access token is expired
        if (error.response?.status === 401 && refreshToken) {
          const newToken = await refreshAccessToken();
          if (newToken) {
            // Try again with new token
            try {
              const retryResponse = await axios.get(`${API_URL}/api/auth/me`, {
                headers: { Authorization: `Bearer ${newToken}` }
              });
              setUser(retryResponse.data.user);
            } catch (retryError) {
              console.error('Auth retry error:', retryError);
              setUser(null);
            }
          } else {
            setUser(null);
          }
        } else {
          setUser(null);
        }
      } finally {
        setLoading(false);
      }
    };
    
    checkAuth();
  }, [accessToken, refreshToken, refreshAccessToken]);

  // Set up axios interceptor for authorization - memoized to prevent recreation on every render
  useEffect(() => {
    // Create axios instance for auth requests to avoid interceptor issues with other requests
    const authAxios = axios.create();
    
    const requestInterceptor = authAxios.interceptors.request.use(
      config => {
        if (accessToken) {
          config.headers.Authorization = `Bearer ${accessToken}`;
        }
        return config;
      },
      error => {
        return Promise.reject(error);
      }
    );

    // Handle token refresh on 401 errors
    const responseInterceptor = authAxios.interceptors.response.use(
      response => response,
      async error => {
        const originalRequest = error.config;
        
        // If the error is 401 and we have a refresh token
        if (error.response?.status === 401 && refreshToken && !originalRequest._retry) {
          originalRequest._retry = true;
          
          try {
            const newToken = await refreshAccessToken();
            if (newToken) {
              originalRequest.headers.Authorization = `Bearer ${newToken}`;
              return authAxios(originalRequest);
            }
          } catch (refreshError) {
            console.error('Token refresh failed:', refreshError);
            return Promise.reject(refreshError);
          }
        }
        
        return Promise.reject(error);
      }
    );

    // Clean up interceptors on unmount
    return () => {
      authAxios.interceptors.request.eject(requestInterceptor);
      authAxios.interceptors.response.eject(responseInterceptor);
    };
  }, [accessToken, refreshToken, refreshAccessToken]);

  // Connect to socket and subscribe to notifications
  useEffect(() => {
    const connectToSocket = async () => {
      if (user && accessToken) {
        try {
          const socket = await initializeSocket(accessToken);
          
          // Add notification handler
          const handleNotification = (notification) => {
            setNotifications(prev => [notification, ...prev]);
          };
          
          addSocketEventHandler('notification', handleNotification);
          
          // Clean up on unmount
          return () => {
            removeSocketEventHandler('notification', handleNotification);
            disconnectSocket();
          };
        } catch (error) {
          console.error('Socket connection error:', error);
        }
      }
    };
    
    connectToSocket();
  }, [user, accessToken]);

  // Login function with memoization
  const login = useCallback(async (email, password) => {
    try {
      const response = await axios.post(`${API_URL}/api/auth/login`, { email, password });
      const { access_token, refresh_token, user } = response.data;
      
      // Save tokens
      localStorage.setItem('access_token', access_token);
      localStorage.setItem('refresh_token', refresh_token);
      
      // Update state
      setAccessToken(access_token);
      setRefreshToken(refresh_token);
      setUser(user);
      
      return { success: true, user };
    } catch (error) {
      console.error('Login error:', error);
      throw error;
    }
  }, []);

  // Register function with memoization
  const register = useCallback(async (userData) => {
    try {
      const response = await axios.post(`${API_URL}/api/auth/register`, userData);
      const { access_token, refresh_token, user } = response.data;
      
      // Save tokens
      localStorage.setItem('access_token', access_token);
      localStorage.setItem('refresh_token', refresh_token);
      
      // Update state
      setAccessToken(access_token);
      setRefreshToken(refresh_token);
      setUser(user);
      
      return { success: true, user };
    } catch (error) {
      console.error('Registration error:', error);
      throw error;
    }
  }, []);

  // Memoize the context value to prevent unnecessary re-renders
  const value = useMemo(() => ({
    user,
    loading,
    login,
    register,
    logout,
    accessToken,
    refreshToken,
    notifications,
    isTestMode,
    isAuthenticated: !!user,
    clearNotifications: () => setNotifications([]),
    refreshAccessToken
  }), [user, loading, login, register, logout, accessToken, refreshToken, notifications, isTestMode, refreshAccessToken]);

  return (
    <AuthContext.Provider value={value}>
      {authError ? (
        <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', minHeight: '100vh', color: 'red' }}>
          <h2>Authentication Error</h2>
          <p>{authError}</p>
        </div>
      ) : loading ? (
        <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', minHeight: '100vh' }}>
          <h2>Loading authentication...</h2>
        </div>
      ) : (
        children
      )}
    </AuthContext.Provider>
  );
};

export default AuthContext; 