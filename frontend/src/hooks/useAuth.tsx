import React, { useState, useEffect, useContext, createContext, ReactNode } from 'react';
import axios, { AxiosError } from 'axios';

interface User {
  id: string;
  email: string;
  role: string;
  name?: string;
}

interface AuthResponse {
  token: string;
  user: User;
}

interface AuthContextType {
  user: User | null;
  loading: boolean;
  error: string | null;
  login: (email: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
  signup: (email: string, password: string, name: string) => Promise<void>;
}

const AuthContext = createContext<AuthContextType | null>(null);

interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider = ({ children }: AuthProviderProps): React.ReactElement => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    checkAuth();
  }, []);

  const checkAuth = async (): Promise<void> => {
    try {
      const token = localStorage.getItem('token');
      if (!token) {
        setLoading(false);
        return;
      }

      const response = await axios.get<User>('/api/auth/me', {
        headers: { Authorization: `Bearer ${token}` }
      });

      setUser(response.data);
    } catch (err) {
      localStorage.removeItem('token');
      if (err instanceof AxiosError) {
        setError(err.response?.data?.message || 'Authentication failed');
      }
    } finally {
      setLoading(false);
    }
  };

  const login = async (email: string, password: string): Promise<void> => {
    try {
      setError(null);
      const response = await axios.post<AuthResponse>('/api/auth/login', { email, password });
      localStorage.setItem('token', response.data.token);
      setUser(response.data.user);
    } catch (err) {
      if (err instanceof AxiosError) {
        setError(err.response?.data?.message || 'Invalid email or password');
      } else {
        setError('An unexpected error occurred');
      }
      throw err;
    }
  };

  const logout = async (): Promise<void> => {
    try {
      await axios.post('/api/auth/logout');
    } catch (err) {
      if (err instanceof AxiosError) {
        console.error('Logout error:', err.response?.data);
      }
    } finally {
      localStorage.removeItem('token');
      setUser(null);
    }
  };

  const signup = async (email: string, password: string, name: string): Promise<void> => {
    try {
      setError(null);
      const response = await axios.post<AuthResponse>('/api/auth/signup', { email, password, name });
      localStorage.setItem('token', response.data.token);
      setUser(response.data.user);
    } catch (err) {
      if (err instanceof AxiosError) {
        setError(err.response?.data?.message || 'Signup failed. Please try again.');
      } else {
        setError('An unexpected error occurred during signup');
      }
      throw err;
    }
  };

  return (
    <AuthContext.Provider 
      value={{
        user,
        loading,
        error,
        login,
        logout,
        signup
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = (): AuthContextType => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}; 