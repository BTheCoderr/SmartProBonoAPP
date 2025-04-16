import React, { createContext, useState, useContext, useCallback, useEffect } from 'react';
import PropTypes from 'prop-types';

// Create the context
const AuthContext = createContext();

// Custom hook to use the auth context
export function useAuth() {
  return useContext(AuthContext);
}

// Auth provider component
export function AuthProvider({ children }) {
  const [currentUser, setCurrentUser] = useState(null);
  const [token, setToken] = useState(localStorage.getItem('authToken') || null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const signup = async (email, password, name) => {
    try {
      const response = await fetch('/api/auth/signup', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password, name }),
      });

      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.message || 'Failed to sign up');
      }

      localStorage.setItem('authToken', data.token);
      setCurrentUser(data.user);
      setToken(data.token);
      return data;
    } catch (error) {
      setError(error.message);
      throw error;
    }
  };

  const login = async (email, password) => {
    try {
      const response = await fetch('/api/auth/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
      });

      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.message || 'Failed to login');
      }

      localStorage.setItem('authToken', data.token);
      setCurrentUser(data.user);
      setToken(data.token);
      return data;
    } catch (error) {
      setError(error.message);
      throw error;
    }
  };

  const logout = () => {
    localStorage.removeItem('authToken');
    setCurrentUser(null);
    setToken(null);
  };

  const resetPassword = async (email) => {
    try {
      const response = await fetch('/api/auth/reset-password', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email }),
      });

      if (!response.ok) {
        const data = await response.json();
        throw new Error(data.message || 'Failed to reset password');
      }

      return response.json();
    } catch (error) {
      setError(error.message);
      throw error;
    }
  };

  // Add a getToken method that returns the current token
  const getToken = useCallback(() => {
    return token;
  }, [token]);

  // Load user data on initialization
  useEffect(() => {
    const fetchUser = async () => {
      try {
        // Check if we have a token
        const storedToken = localStorage.getItem('authToken');
        if (!storedToken) {
          setLoading(false);
          return;
        }

        // Fetch user info using the token
        const response = await fetch('/api/auth/me', {
          headers: {
            'Authorization': `Bearer ${storedToken}`,
          },
        });

        if (response.ok) {
          const data = await response.json();
          if (data.user) {
            setCurrentUser(data.user);
            setToken(storedToken);
          } else {
            localStorage.removeItem('authToken');
            setToken(null);
          }
        } else {
          // Token is invalid or expired
          localStorage.removeItem('authToken');
          setToken(null);
        }
      } catch (error) {
        console.error('Error fetching user:', error);
        setError('Failed to authenticate');
      } finally {
        setLoading(false);
      }
    };

    fetchUser();
  }, []);

  const value = {
    user: currentUser,
    token,
    isAuthenticated: !!currentUser,
    isLoading: loading,
    error,
    login,
    signup,
    logout,
    resetPassword,
    getToken
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
}

AuthProvider.propTypes = {
  children: PropTypes.node.isRequired,
};

export default AuthProvider;
