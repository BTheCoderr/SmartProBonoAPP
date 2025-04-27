import React, { createContext, useState, useEffect, useContext, useMemo, useCallback } from 'react';
import axios from 'axios';
import { API_URL } from '../config';
import { initializeSocket, disconnectSocket, addSocketEventHandler, removeSocketEventHandler } from '../services/socket';

// Create the Auth Context
const AuthContext = createContext();

// Custom hook to use the Auth Context
export const useAuth = () => {
  return useContext(AuthContext);
};

// Auth Provider Component
export const AuthProvider = ({ children }) => {
  const [currentUser, setCurrentUser] = useState(null);
  const [accessToken, setAccessToken] = useState(localStorage.getItem('access_token'));
  const [refreshToken, setRefreshToken] = useState(localStorage.getItem('refresh_token'));
  const [loading, setLoading] = useState(true);
  const [isLoggingOut, setIsLoggingOut] = useState(false);
  const [isRefreshing, setIsRefreshing] = useState(false);
  const [refreshAttempts, setRefreshAttempts] = useState(0);
  const [notifications, setNotifications] = useState([]);
  const MAX_REFRESH_ATTEMPTS = 3;

  // Add this at the top of the AuthProvider component
  const isTestMode = window.location.href.includes('scanner-test') || 
                    window.location.href.includes('test-mode') || 
                    process.env.NODE_ENV === 'development';

  // Handle notifications from socket
  const handleNotification = useCallback((data) => {
    setNotifications(prev => [data, ...prev].slice(0, 10)); // Keep only the 10 most recent notifications
    // You can also show a toast/snackbar here to alert the user
    console.log('New notification received:', data);
  }, []);

  // Initialize socket when user is authenticated
  useEffect(() => {
    if (currentUser && currentUser.id) {
      console.log('Initializing socket for user:', currentUser.id);
      initializeSocket(currentUser.id)
        .then(() => {
          console.log('Socket initialized and registered successfully');
          // Set up notification handler
          addSocketEventHandler('notification', handleNotification);
        })
        .catch(error => {
          console.error('Failed to initialize socket:', error);
        });
      
      // Cleanup function
      return () => {
        removeSocketEventHandler('notification', handleNotification);
      };
    }
  }, [currentUser, handleNotification]);

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

  // Load user from token on mount - use memoization to prevent unnecessary API calls
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
        const response = await axios.get(`${API_URL}/api/auth/me`, {
          headers: {
            Authorization: `Bearer ${accessToken}`
          },
          // Add cache control to prevent duplicate requests
          cache: {
            maxAge: 15 * 60 * 1000, // 15 minutes
            excludeFromCache: false,
          }
        });
        setCurrentUser(response.data.user);
      } catch (error) {
        // Token might be expired or invalid
        console.error('Error loading user:', error);
        // Don't logout here - let the interceptor handle token refresh
        if (error.response?.status !== 401 || !refreshToken) {
          logout();
        }
      } finally {
        setLoading(false);
      }
    };

    loadUser();
  }, [accessToken, isTestMode]); // Only dependency is accessToken

  // Mock login function for testing purposes without backend
  const mockLogin = useCallback(() => {
    // Create a mock user and token
    const mockUser = {
      id: 1,
      username: 'testuser',
      email: 'test@example.com',
      first_name: 'Test',
      last_name: 'User',
      role: 'user'
    };
    
    const mockToken = 'mock-jwt-token-for-testing-purposes';
    
    // Save to localStorage and state
    localStorage.setItem('access_token', mockToken);
    localStorage.setItem('refresh_token', mockToken);
    setAccessToken(mockToken);
    setRefreshToken(mockToken);
    setCurrentUser(mockUser);
    
    return { success: true, user: mockUser };
  }, []);

  // Login function with memoization
  const login = useCallback(async (email, password) => {
    try {
      const response = await axios.post(`${API_URL}/api/auth/login`, {
        email,
        password
      });

      const { access_token, refresh_token, user } = response.data;
      
      // Save tokens to localStorage and state
      localStorage.setItem('access_token', access_token);
      localStorage.setItem('refresh_token', refresh_token);
      setAccessToken(access_token);
      setRefreshToken(refresh_token);
      setCurrentUser(user);
      
      return { success: true, user };
    } catch (error) {
      console.error('Login error:', error);
      return { 
        success: false, 
        error: error.response?.data?.message || 'Login failed'
      };
    }
  }, []);

  // Register function with memoization
  const register = useCallback(async (userData) => {
    try {
      const response = await axios.post(`${API_URL}/api/auth/register`, userData);
      return { success: true, data: response.data };
    } catch (error) {
      console.error('Registration error:', error);
      return { 
        success: false, 
        error: error.response?.data?.message || 'Registration failed'
      };
    }
  }, []);

  // Update profile function with memoization
  const updateProfile = useCallback(async (userData) => {
    try {
      const response = await axios.put(`${API_URL}/api/auth/update`, userData, {
        headers: {
          Authorization: `Bearer ${accessToken}`
        }
      });
      setCurrentUser(response.data.user);
      return { success: true, user: response.data.user };
    } catch (error) {
      console.error('Update profile error:', error);
      return { 
        success: false, 
        error: error.response?.data?.message || 'Profile update failed'
      };
    }
  }, [accessToken]);

  // Logout function with debounce
  const logout = useCallback(async () => {
    // Prevent multiple logout attempts in succession
    if (isLoggingOut) return;
    
    setIsLoggingOut(true);
    
    // Disconnect socket
    disconnectSocket();
    
    if (accessToken) {
      try {
        // Call the logout endpoint to invalidate the token
        await axios.post(`${API_URL}/api/auth/logout`, {}, {
          headers: {
            Authorization: `Bearer ${accessToken}`
          },
          // Add timeout to prevent hanging requests
          timeout: 5000
        });
      } catch (error) {
        // Just log the error, but continue with local logout
        console.error('Logout API error:', error);
        // Don't retry the API call if it fails
      }
    }
    
    // Clear tokens and user state regardless of API success
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('token'); // Remove old token format as well
    setAccessToken(null);
    setRefreshToken(null);
    setCurrentUser(null);
    
    // Reset logout status after a short delay
    setTimeout(() => {
      setIsLoggingOut(false);
    }, 1000);
  }, [accessToken, isLoggingOut]);

  // Memoize the context value to prevent unnecessary re-renders
  const value = useMemo(() => ({
    currentUser,
    isAuthenticated: !!currentUser,
    login,
    register,
    logout,
    updateProfile,
    mockLogin,
    loading,
    notifications
  }), [currentUser, login, register, logout, updateProfile, mockLogin, loading, notifications]);

  // Return Provider with context value
  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};

export default AuthContext; 