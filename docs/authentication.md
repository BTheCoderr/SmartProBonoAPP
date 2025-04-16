# Authentication System Documentation

The Smart Pro Bono application implements a secure JWT-based authentication system to manage user identity, access control, and session management. This document outlines the architecture, implementation details, and usage guidelines for the authentication system.

## Architecture Overview

The authentication system is built on the following key components:

1. **JWT Authentication**: JSON Web Tokens for stateless authentication
2. **Role-Based Access Control (RBAC)**: Different permissions for attorneys, clients, and administrators
3. **Token Management**: Securely storing, refreshing, and validating tokens
4. **Authentication Context**: Frontend state management for auth status
5. **Protected Routes**: Components that restrict access based on authentication status
6. **User Profile Management**: Features for managing user information

## Backend Implementation

### JWT Configuration

The JWT authentication is configured using the Flask-JWT-Extended library:

```python
from flask import Flask
from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'dev-key-never-use-in-prod')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30)

jwt = JWTManager(app)
```

### User Authentication Endpoints

The backend provides several endpoints for user authentication:

```python
@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email', '')
    password = data.get('password', '')
    
    user = User.query.filter_by(email=email).first()
    
    if not user or not user.check_password(password):
        return jsonify({'message': 'Invalid credentials'}), 401
    
    # Create tokens
    access_token = create_access_token(identity=user.id)
    refresh_token = create_refresh_token(identity=user.id)
    
    return jsonify({
        'access_token': access_token,
        'refresh_token': refresh_token,
        'user': {
            'id': user.id,
            'email': user.email,
            'name': user.name,
            'role': user.role,
            'profile_pic': user.profile_pic
        }
    })

@app.route('/api/auth/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    current_user_id = get_jwt_identity()
    access_token = create_access_token(identity=current_user_id)
    
    return jsonify({
        'access_token': access_token
    })

@app.route('/api/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    
    # Check if user already exists
    existing_user = User.query.filter_by(email=data.get('email')).first()
    if existing_user:
        return jsonify({'message': 'User already exists'}), 409
    
    # Create new user
    new_user = User(
        email=data.get('email'),
        name=data.get('name'),
        role=data.get('role', 'client')  # Default role is client
    )
    new_user.set_password(data.get('password'))
    
    db.session.add(new_user)
    db.session.commit()
    
    # Create tokens
    access_token = create_access_token(identity=new_user.id)
    refresh_token = create_refresh_token(identity=new_user.id)
    
    return jsonify({
        'message': 'User registered successfully',
        'access_token': access_token,
        'refresh_token': refresh_token,
        'user': {
            'id': new_user.id,
            'email': new_user.email,
            'name': new_user.name,
            'role': new_user.role
        }
    }), 201

@app.route('/api/auth/logout', methods=['POST'])
@jwt_required()
def logout():
    # Add token to blocklist (not implemented in this example)
    # jwt_redis.set(get_jwt()['jti'], '', ex=ACCESS_EXPIRES)
    
    return jsonify({'message': 'Successfully logged out'})

@app.route('/api/auth/me', methods=['GET'])
@jwt_required()
def get_user_info():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    return jsonify({
        'id': user.id,
        'email': user.email,
        'name': user.name,
        'role': user.role,
        'profile_pic': user.profile_pic,
        'created_at': user.created_at.isoformat()
    })
```

### User Model

The User model stores authentication information and user details:

```python
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), default='client')  # client, attorney, admin
    profile_pic = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    # Methods for password hashing and verification
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
```

### Role-Based Access Control

Custom decorators for restricting access based on user roles:

```python
from functools import wraps
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request

def attorney_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user or user.role != 'attorney':
            return jsonify({'message': 'Attorney role required'}), 403
        
        return fn(*args, **kwargs)
    return wrapper

def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user or user.role != 'admin':
            return jsonify({'message': 'Admin role required'}), 403
        
        return fn(*args, **kwargs)
    return wrapper
```

## Frontend Implementation

### Authentication Context

The `AuthContext` provides authentication state and functions throughout the application:

```jsx
import React, { createContext, useState, useEffect, useContext } from 'react';
import axios from 'axios';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(localStorage.getItem('token'));
  const [refreshToken, setRefreshToken] = useState(localStorage.getItem('refreshToken'));
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  // Set up axios defaults
  axios.defaults.headers.common['Authorization'] = token ? `Bearer ${token}` : '';
  
  // Initialize auth state from tokens
  useEffect(() => {
    const initializeAuth = async () => {
      if (token) {
        try {
          const response = await axios.get('/api/auth/me');
          setUser(response.data);
        } catch (err) {
          // If token is invalid, try to refresh
          if (refreshToken) {
            try {
              const refreshResponse = await axios.post('/api/auth/refresh', {
                refresh_token: refreshToken
              });
              
              const newToken = refreshResponse.data.access_token;
              setToken(newToken);
              localStorage.setItem('token', newToken);
              
              // Retry getting user info with new token
              axios.defaults.headers.common['Authorization'] = `Bearer ${newToken}`;
              const userResponse = await axios.get('/api/auth/me');
              setUser(userResponse.data);
            } catch (refreshErr) {
              // Both tokens are invalid, log out
              logout();
              setError('Session expired. Please log in again.');
            }
          } else {
            logout();
          }
        } finally {
          setLoading(false);
        }
      } else {
        setLoading(false);
      }
    };
    
    initializeAuth();
  }, [token, refreshToken]);
  
  // Login function
  const login = async (email, password) => {
    try {
      setLoading(true);
      setError(null);
      
      const response = await axios.post('/api/auth/login', { email, password });
      
      const { access_token, refresh_token, user: userData } = response.data;
      
      setToken(access_token);
      setRefreshToken(refresh_token);
      setUser(userData);
      
      localStorage.setItem('token', access_token);
      localStorage.setItem('refreshToken', refresh_token);
      
      axios.defaults.headers.common['Authorization'] = `Bearer ${access_token}`;
      
      return true;
    } catch (err) {
      const message = err.response?.data?.message || 'Login failed. Please try again.';
      setError(message);
      return false;
    } finally {
      setLoading(false);
    }
  };
  
  // Register function
  const register = async (userData) => {
    try {
      setLoading(true);
      setError(null);
      
      const response = await axios.post('/api/auth/register', userData);
      
      const { access_token, refresh_token, user: newUser } = response.data;
      
      setToken(access_token);
      setRefreshToken(refresh_token);
      setUser(newUser);
      
      localStorage.setItem('token', access_token);
      localStorage.setItem('refreshToken', refresh_token);
      
      axios.defaults.headers.common['Authorization'] = `Bearer ${access_token}`;
      
      return true;
    } catch (err) {
      const message = err.response?.data?.message || 'Registration failed. Please try again.';
      setError(message);
      return false;
    } finally {
      setLoading(false);
    }
  };
  
  // Logout function
  const logout = () => {
    // Call logout endpoint if user is logged in
    if (token) {
      axios.post('/api/auth/logout').catch(() => {
        // Silent catch - we still want to clear local state even if the API call fails
      });
    }
    
    // Clear local state
    setUser(null);
    setToken(null);
    setRefreshToken(null);
    
    // Remove from localStorage
    localStorage.removeItem('token');
    localStorage.removeItem('refreshToken');
    
    // Clear Authorization header
    axios.defaults.headers.common['Authorization'] = '';
  };
  
  // Check if user has a specific role
  const hasRole = (requiredRole) => {
    if (!user) return false;
    return user.role === requiredRole;
  };
  
  // Update user profile
  const updateProfile = async (profileData) => {
    try {
      setLoading(true);
      setError(null);
      
      const response = await axios.put('/api/users/profile', profileData);
      
      setUser(prev => ({ ...prev, ...response.data }));
      
      return true;
    } catch (err) {
      const message = err.response?.data?.message || 'Failed to update profile. Please try again.';
      setError(message);
      return false;
    } finally {
      setLoading(false);
    }
  };
  
  // Auth context value
  const value = {
    user,
    token,
    isAuthenticated: !!user,
    isAttorney: user?.role === 'attorney',
    isAdmin: user?.role === 'admin',
    isClient: user?.role === 'client',
    loading,
    error,
    login,
    register,
    logout,
    hasRole,
    updateProfile
  };
  
  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = () => useContext(AuthContext);
```

### Protected Route Component

A component that restricts access to routes based on authentication status and roles:

```jsx
import React from 'react';
import { Navigate, Outlet } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

const ProtectedRoute = ({ 
  requiredAuth = true, 
  requiredRoles = [], 
  redirectPath = '/' 
}) => {
  const { isAuthenticated, user, loading } = useAuth();
  
  // Show loading state while auth is being checked
  if (loading) {
    return <div>Loading...</div>;
  }
  
  // Check if authentication is required but user is not authenticated
  if (requiredAuth && !isAuthenticated) {
    return <Navigate to="/login" replace />;
  }
  
  // Check if authentication is NOT required but user IS authenticated
  if (!requiredAuth && isAuthenticated) {
    return <Navigate to={redirectPath} replace />;
  }
  
  // Check if specific roles are required
  if (
    requiredRoles.length > 0 &&
    isAuthenticated &&
    !requiredRoles.includes(user.role)
  ) {
    return <Navigate to="/unauthorized" replace />;
  }
  
  // Render the protected content
  return <Outlet />;
};

export default ProtectedRoute;
```

### Login and Registration Forms

Example login form component:

```jsx
import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import {
  Box,
  Button,
  TextField,
  Typography,
  Paper,
  Alert,
  CircularProgress
} from '@mui/material';

const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [formError, setFormError] = useState('');
  const { login, loading, error } = useAuth();
  const navigate = useNavigate();
  
  const handleSubmit = async (e) => {
    e.preventDefault();
    setFormError('');
    
    // Simple validation
    if (!email.trim()) {
      setFormError('Email is required');
      return;
    }
    
    if (!password) {
      setFormError('Password is required');
      return;
    }
    
    const success = await login(email, password);
    if (success) {
      navigate('/dashboard');
    }
  };
  
  return (
    <Box
      sx={{
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        minHeight: '100vh',
        backgroundColor: 'background.default'
      }}
    >
      <Paper
        elevation={3}
        sx={{
          p: 4,
          maxWidth: 400,
          width: '100%'
        }}
      >
        <Typography variant="h4" component="h1" gutterBottom align="center">
          Log In
        </Typography>
        
        {(error || formError) && (
          <Alert severity="error" sx={{ mb: 2 }}>
            {formError || error}
          </Alert>
        )}
        
        <form onSubmit={handleSubmit}>
          <TextField
            label="Email"
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            fullWidth
            margin="normal"
            required
            autoFocus
          />
          
          <TextField
            label="Password"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            fullWidth
            margin="normal"
            required
          />
          
          <Button
            type="submit"
            variant="contained"
            color="primary"
            fullWidth
            size="large"
            sx={{ mt: 3, mb: 2 }}
            disabled={loading}
          >
            {loading ? <CircularProgress size={24} /> : 'Log In'}
          </Button>
          
          <Typography variant="body2" align="center">
            Don't have an account?{' '}
            <Link to="/register">Sign up here</Link>
          </Typography>
        </form>
      </Paper>
    </Box>
  );
};

export default Login;
```

## Usage Guidelines

### Protecting Routes

In the application's routing configuration:

```jsx
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import ProtectedRoute from './components/ProtectedRoute';
import Home from './pages/Home';
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import AdminDashboard from './pages/AdminDashboard';
import Profile from './pages/Profile';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Public routes */}
        <Route path="/" element={<Home />} />
        
        {/* Auth routes - only accessible when NOT logged in */}
        <Route element={<ProtectedRoute requiredAuth={false} redirectPath="/dashboard" />}>
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
        </Route>
        
        {/* Protected routes - require authentication */}
        <Route element={<ProtectedRoute />}>
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/profile" element={<Profile />} />
        </Route>
        
        {/* Admin-only routes */}
        <Route element={<ProtectedRoute requiredRoles={['admin']} />}>
          <Route path="/admin" element={<AdminDashboard />} />
        </Route>
        
        {/* Attorney-only routes */}
        <Route element={<ProtectedRoute requiredRoles={['attorney']} />}>
          <Route path="/cases" element={<CaseManagement />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}
```

### Accessing Auth Information in Components

```jsx
import { useAuth } from '../contexts/AuthContext';

const UserGreeting = () => {
  const { user, isAuthenticated, isAttorney } = useAuth();
  
  if (!isAuthenticated) {
    return <p>Please log in to continue</p>;
  }
  
  return (
    <div>
      <h2>Welcome, {user.name}!</h2>
      {isAttorney && <p>You have attorney privileges</p>}
    </div>
  );
};
```

### Making Authenticated API Requests

```jsx
import axios from 'axios';
import { useAuth } from '../contexts/AuthContext';

const UserProfile = () => {
  const { token } = useAuth();
  const [profile, setProfile] = useState(null);
  
  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const response = await axios.get('/api/users/profile', {
          headers: {
            Authorization: `Bearer ${token}`
          }
        });
        setProfile(response.data);
      } catch (error) {
        console.error('Failed to fetch profile:', error);
      }
    };
    
    fetchProfile();
  }, [token]);
  
  // Render profile data...
};
```

## Security Considerations

### Token Storage

The application stores authentication tokens in localStorage, which provides persistence across browser sessions but is vulnerable to XSS attacks. For highest security, consider:

1. Using HttpOnly cookies for refresh tokens
2. Keeping access tokens in memory only (not localStorage)
3. Implementing CSRF protection measures

### Token Expiration

Access tokens are short-lived (1 hour) while refresh tokens last longer (30 days). This provides a balance between security and user experience:

- If an access token is compromised, it has limited validity
- The refresh mechanism allows sustained sessions without requiring frequent logins

### Password Security

Password security measures:

1. Passwords are never stored in plain text
2. Werkzeug's `generate_password_hash` uses secure hashing (PBKDF2 + SHA256)
3. Frontend prevents submission of weak passwords (min 8 chars, mixed case, numbers)

## Future Enhancements

1. **Multi-factor Authentication**: Add SMS or authenticator app verification
2. **OAuth Integration**: Support login via Google, Facebook, LinkedIn
3. **Session Management**: Allow users to view and terminate active sessions
4. **Password Recovery**: Implement secure password reset functionality
5. **Audit Logging**: Track authentication events for security monitoring
6. **Device Fingerprinting**: Enhance security by detecting suspicious logins
7. **Account Lockout**: Protect against brute force attacks
8. **JWT Token Revocation**: Enable immediate token invalidation when needed

## Troubleshooting

### Common Auth Issues

1. **"Invalid Token" Errors**
   - Check that the token is not expired
   - Verify the token is being sent correctly in the Authorization header
   - Ensure the JWT secret key is consistent between auth and validation

2. **Authentication Loop**
   - Often caused by refresh token issues
   - Check for proper handling of token refresh failures
   - Verify that new tokens are being stored correctly

3. **"User not found" After Login**
   - Check that the user ID stored in the token exists in the database
   - Verify that the token payload contains the correct identity claims

4. **CORS Issues with Auth Headers**
   - Ensure the server is configured to accept the Authorization header
   - Check that preflight OPTIONS requests are handled correctly

## API Reference

### Authentication Endpoints

| Endpoint | Method | Description | Request Body | Response |
|----------|--------|-------------|--------------|----------|
| `/api/auth/login` | POST | Log in a user | `{ email, password }` | `{ access_token, refresh_token, user }` |
| `/api/auth/register` | POST | Register a new user | `{ email, password, name, role }` | `{ access_token, refresh_token, user }` |
| `/api/auth/refresh` | POST | Refresh the access token | `{ refresh_token }` | `{ access_token }` |
| `/api/auth/logout` | POST | Log out a user | None | `{ message }` |
| `/api/auth/me` | GET | Get current user info | None | User object | 