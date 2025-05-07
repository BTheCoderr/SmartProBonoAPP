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
        await ApiService.post('/api/auth/logout');
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

  // Handle navigation errors
  useEffect(() => {
    if (navigate && window.location.pathname === '/dashboard' && !user) {
      const navigateToHome = async () => {
        try {
          await navigate('/', { replace: true });
        } catch (error) {
          console.error('Navigation error:', error);
          // Fallback to window.location if navigation fails
          if (error.message.includes('history')) {
            window.location.href = '/';
          }
        }
      };
      navigateToHome();
    }
  }, [navigate, user]);

  // Handle notifications from socket
  const handleNotification = useCallback((data) => {
    setNotifications(prev => [data, ...prev].slice(0, 10)); // Keep only the 10 most recent notifications
    // You can also show a toast/snackbar here to alert the user
    console.log('New notification received:', data);
  }, []);

  // Initialize socket when user is authenticated
  useEffect(() => {
    let mounted = true;

    const initSocket = async () => {
      if (user && user.id) {
        try {
          console.log('Initializing socket for user:', user.id);
          await initializeSocket(user.id);
          if (mounted) {
            console.log('Socket initialized and registered successfully');
            // Set up notification handler
            addSocketEventHandler('notification', handleNotification);
          }
        } catch (error) {
          console.error('Failed to initialize socket:', error);
          // If socket initialization fails, log out the user
          await logout();
        }
      }
    };

    initSocket();
    
    // Cleanup function
    return () => {
      mounted = false;
      removeSocketEventHandler('notification', handleNotification);
      disconnectSocket();
    };
  }, [user, handleNotification, logout]);

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
          // If already refreshing, wait until it's done
          if (isRefreshing) {
            return new Promise(resolve => {
              setTimeout(() => {
                originalRequest.headers.Authorization = `Bearer ${accessToken}`;
                resolve(authAxios(originalRequest));
              }, 1000); // Wait 1 second and retry with the new token
            });
          }
          
          // Check if we've exceeded max refresh attempts
          if (refreshAttempts >= MAX_REFRESH_ATTEMPTS) {
            console.log('Max refresh attempts reached, logging out');
            logout();
            return Promise.reject(error);
          }
          
          originalRequest._retry = true;
          setIsRefreshing(true);
          
          try {
            // Attempt to refresh the token
            const refreshResponse = await axios.post(`${API_URL}/api/auth/refresh`, {}, {
              headers: {
                'Authorization': `Bearer ${refreshToken}`
              },
              timeout: 5000 // Add timeout to prevent hanging requests
            });
            
            const { access_token } = refreshResponse.data;
            
            // Update tokens
            localStorage.setItem('access_token', access_token);
            setAccessToken(access_token);
            
            // Reset refresh state
            setRefreshAttempts(0);
            setIsRefreshing(false);
            
            // Update authorization header and retry
            originalRequest.headers.Authorization = `Bearer ${access_token}`;
            return authAxios(originalRequest);
          } catch (refreshError) {
            // Handle rate limiting (429)
            if (refreshError.response?.status === 429) {
              console.log('Rate limited during token refresh, will retry later');
              setIsRefreshing(false);
              // Increment attempts counter
              setRefreshAttempts(prevAttempts => prevAttempts + 1);
              return Promise.reject(refreshError);
            }
            
            // If refresh fails, logout user
            console.error('Token refresh failed:', refreshError);
            setIsRefreshing(false);
            logout();
            return Promise.reject(refreshError);
          }
        }
        
        return Promise.reject(error);
      }
    );

    // Make auth instance available
    window.authAxios = authAxios;
    
    return () => {
      authAxios.interceptors.request.eject(requestInterceptor);
      authAxios.interceptors.response.eject(responseInterceptor);
    };
  }, [accessToken, refreshToken, isRefreshing, refreshAttempts]);

  // Load user from token on mount
  useEffect(() => {
    const loadUser = async () => {
      if (!accessToken) {
        setLoading(false);
        return;
      }

      // Skip actual auth API calls when in test mode
      if (isTestMode) {
        console.log('🧪 Test mode detected - skipping real authentication API calls');
        setLoading(false);
        return;
      }

      try {
        const response = await ApiService.get('/api/auth/profile');
        setUser(response.data);
        setAuthError(null);
      } catch (error) {
        console.error('Error loading user:', error);
        setAuthError('Authentication failed. Please log in again or contact support.');
        if (error.response?.status !== 401 || !refreshToken) {
          await logout();
        }
      } finally {
        setLoading(false);
      }
    };

    loadUser();
  }, [accessToken, isTestMode, refreshToken, logout]);

  // Login function with memoization
  const login = useCallback(async (email, password) => {
    try {
      const response = await ApiService.post('/api/auth/login', { email, password });
      setUser(response.data);
      return response.data;
    } catch (error) {
      throw error;
    }
  }, []);

  // Register function with memoization
  const register = useCallback(async (userData) => {
    try {
      const response = await ApiService.post('/api/auth/register', userData);
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
    isTestMode
  }), [user, loading, login, register, logout, accessToken, refreshToken, notifications, isTestMode]);

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