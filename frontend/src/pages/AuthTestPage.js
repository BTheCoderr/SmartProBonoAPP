import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import {
  Box,
  Container,
  Typography,
  Button,
  Paper,
  Divider,
  CircularProgress,
  TextField,
  Alert,
  Grid
} from '@mui/material';
import ApiService from '../services/ApiService';

/**
 * Test page to verify JWT authentication functionality
 */
const AuthTestPage = () => {
  const { user, accessToken, refreshToken, refreshAccessToken, logout } = useAuth();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [result, setResult] = useState(null);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [registerData, setRegisterData] = useState({
    email: '',
    password: '',
    firstName: '',
    lastName: '',
    role: 'user'
  });
  
  // Basic test that just fetches the /api/auth/test-auth endpoint
  const testAuthEndpoint = async () => {
    setLoading(true);
    setError(null);
    setResult(null);
    
    try {
      const response = await ApiService.get('/api/auth/test-auth');
      setResult(response.data);
    } catch (err) {
      setError(err.response?.data?.error || err.message);
    } finally {
      setLoading(false);
    }
  };
  
  // Test login functionality
  const testLogin = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResult(null);
    
    try {
      const response = await ApiService.login({ email, password });
      setResult(response);
    } catch (err) {
      setError(err.response?.data?.error || err.message);
    } finally {
      setLoading(false);
    }
  };
  
  // Test refresh token functionality
  const testRefreshToken = async () => {
    setLoading(true);
    setError(null);
    setResult(null);
    
    try {
      const newToken = await refreshAccessToken();
      setResult({ message: 'Token refreshed successfully', token: newToken });
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };
  
  // Test logout functionality
  const testLogout = async () => {
    setLoading(true);
    setError(null);
    setResult(null);
    
    try {
      await logout();
      setResult({ message: 'Logged out successfully' });
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };
  
  // Handle register form data changes
  const handleRegisterChange = (e) => {
    const { name, value } = e.target;
    setRegisterData(prev => ({ ...prev, [name]: value }));
  };
  
  // Test registration functionality
  const testRegister = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResult(null);
    
    try {
      const response = await ApiService.register(registerData);
      setResult(response);
    } catch (err) {
      setError(err.response?.data?.error || err.message);
    } finally {
      setLoading(false);
    }
  };
  
  return (
    <Container maxWidth="md" sx={{ py: 4 }}>
      <Typography variant="h4" gutterBottom>
        JWT Authentication Test Page
      </Typography>
      
      <Box sx={{ mb: 3 }}>
        <Typography variant="h6">Current Authentication State</Typography>
        <Paper sx={{ p: 2, mb: 2 }}>
          <Typography variant="body1">
            <strong>User:</strong> {user ? JSON.stringify(user, null, 2) : 'Not logged in'}
          </Typography>
          <Typography variant="body1">
            <strong>Access Token:</strong> {accessToken ? `${accessToken.substring(0, 15)}...` : 'None'}
          </Typography>
          <Typography variant="body1">
            <strong>Refresh Token:</strong> {refreshToken ? `${refreshToken.substring(0, 15)}...` : 'None'}
          </Typography>
        </Paper>
      </Box>
      
      <Divider sx={{ my: 3 }} />
      
      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <Typography variant="h6" gutterBottom>Login Test</Typography>
          <Paper sx={{ p: 2 }}>
            <form onSubmit={testLogin}>
              <TextField
                label="Email"
                variant="outlined"
                fullWidth
                margin="normal"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
              />
              <TextField
                label="Password"
                variant="outlined"
                fullWidth
                margin="normal"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
              <Button 
                variant="contained" 
                color="primary" 
                type="submit"
                disabled={loading}
                sx={{ mt: 2 }}
              >
                {loading ? <CircularProgress size={24} /> : 'Login'}
              </Button>
            </form>
          </Paper>
        </Grid>
        
        <Grid item xs={12} md={6}>
          <Typography variant="h6" gutterBottom>Register Test</Typography>
          <Paper sx={{ p: 2 }}>
            <form onSubmit={testRegister}>
              <TextField
                label="Email"
                variant="outlined"
                fullWidth
                margin="normal"
                name="email"
                value={registerData.email}
                onChange={handleRegisterChange}
                required
              />
              <TextField
                label="Password"
                variant="outlined"
                fullWidth
                margin="normal"
                type="password"
                name="password"
                value={registerData.password}
                onChange={handleRegisterChange}
                required
              />
              <TextField
                label="First Name"
                variant="outlined"
                fullWidth
                margin="normal"
                name="firstName"
                value={registerData.firstName}
                onChange={handleRegisterChange}
                required
              />
              <TextField
                label="Last Name"
                variant="outlined"
                fullWidth
                margin="normal"
                name="lastName"
                value={registerData.lastName}
                onChange={handleRegisterChange}
                required
              />
              <Button 
                variant="contained" 
                color="primary" 
                type="submit"
                disabled={loading}
                sx={{ mt: 2 }}
              >
                {loading ? <CircularProgress size={24} /> : 'Register'}
              </Button>
            </form>
          </Paper>
        </Grid>
      </Grid>
      
      <Box sx={{ mt: 3 }}>
        <Typography variant="h6" gutterBottom>API Tests</Typography>
        <Paper sx={{ p: 2 }}>
          <Button 
            variant="contained" 
            onClick={testAuthEndpoint}
            disabled={loading}
            sx={{ mr: 2, mb: 2 }}
          >
            Test Auth Endpoint
          </Button>
          
          <Button 
            variant="contained" 
            onClick={testRefreshToken}
            disabled={loading || !refreshToken}
            sx={{ mr: 2, mb: 2 }}
          >
            Test Refresh Token
          </Button>
          
          <Button 
            variant="contained" 
            color="error"
            onClick={testLogout}
            disabled={loading || !accessToken}
            sx={{ mb: 2 }}
          >
            Test Logout
          </Button>
        </Paper>
      </Box>
      
      {error && (
        <Alert severity="error" sx={{ mt: 3 }}>
          {error}
        </Alert>
      )}
      
      {result && (
        <Box sx={{ mt: 3 }}>
          <Typography variant="h6">Result:</Typography>
          <Paper sx={{ p: 2, bgcolor: '#f5f5f5' }}>
            <pre>{JSON.stringify(result, null, 2)}</pre>
          </Paper>
        </Box>
      )}
    </Container>
  );
};

export default AuthTestPage; 