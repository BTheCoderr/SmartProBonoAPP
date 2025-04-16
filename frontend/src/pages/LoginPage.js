import React, { useState } from 'react';
import { useNavigate, Link, useLocation } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import {
  Box,
  Container,
  TextField,
  Button,
  Typography,
  Paper,
  InputAdornment,
  IconButton,
  Alert,
  Grid,
  useTheme,
  useMediaQuery,
} from '@mui/material';
import { Visibility, VisibilityOff, Email, Lock, Home } from '@mui/icons-material';
import Logo from '../components/Logo';

const LoginPage = () => {
  const { t } = useTranslation();
  const navigate = useNavigate();
  const location = useLocation();
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('sm'));

  // Check if we were redirected from a protected route
  const fromPath = location.state?.from || '/';
  const isRedirected = fromPath !== '/';

  const [formData, setFormData] = useState({
    email: '',
    password: '',
  });

  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleChange = e => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleTogglePassword = () => {
    setShowPassword(prev => !prev);
  };

  const handleSubmit = async e => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      // In a real app, we would connect to the backend
      // This is a mock implementation for demo purposes

      // Simulate successful login for any email/password combination
      const mockUser = {
        id: '12345',
        email: formData.email,
        firstName: 'Demo',
        lastName: 'User',
        role: 'user',
      };

      const mockToken = 'mock-jwt-token-' + Date.now();

      // Store token in localStorage
      localStorage.setItem('authToken', mockToken);

      // Store user data
      localStorage.setItem('user', JSON.stringify(mockUser));

      // Redirect to the original page the user was trying to access, or home
      navigate(fromPath);
    } catch (err) {
      setError(err.message || 'An error occurred during login');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container maxWidth="sm" sx={{ py: 8 }}>
      <Box sx={{ mb: 3, display: 'flex', justifyContent: 'space-between' }}>
        <Button startIcon={<Home />} component={Link} to="/" variant="text" color="primary">
          Back to Homepage
        </Button>
      </Box>

      <Paper
        elevation={3}
        sx={{
          p: 4,
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          borderRadius: 2,
          boxShadow: theme.shadows[3],
        }}
      >
        <Box sx={{ mb: 3, display: 'flex', justifyContent: 'center' }}>
          <Logo variant="light" size={isMobile ? "small" : "medium"} />
        </Box>

        <Typography
          component="h1"
          variant="h4"
          gutterBottom
          align="center"
          sx={{ fontWeight: 'bold' }}
        >
          {t('login.title')}
        </Typography>

        {isRedirected && (
          <Alert severity="info" sx={{ width: '100%', mb: 3 }}>
            Please log in to access this feature. Your free legal resources are still available on
            the homepage.
          </Alert>
        )}

        {!isRedirected && (
          <Typography variant="body1" color="text.secondary" align="center" sx={{ mb: 3 }}>
            {t('login.subtitle')}
          </Typography>
        )}

        {error && (
          <Alert severity="error" sx={{ width: '100%', mb: 3 }}>
            {error}
          </Alert>
        )}

        <Box component="form" onSubmit={handleSubmit} sx={{ width: '100%' }}>
          <TextField
            margin="normal"
            required
            fullWidth
            id="email"
            label={t('login.email')}
            name="email"
            autoComplete="email"
            autoFocus
            value={formData.email}
            onChange={handleChange}
            InputProps={{
              startAdornment: (
                <InputAdornment position="start">
                  <Email />
                </InputAdornment>
              ),
            }}
          />

          <TextField
            margin="normal"
            required
            fullWidth
            name="password"
            label={t('login.password')}
            type={showPassword ? 'text' : 'password'}
            id="password"
            autoComplete="current-password"
            value={formData.password}
            onChange={handleChange}
            InputProps={{
              startAdornment: (
                <InputAdornment position="start">
                  <Lock />
                </InputAdornment>
              ),
              endAdornment: (
                <InputAdornment position="end">
                  <IconButton
                    aria-label="toggle password visibility"
                    onClick={handleTogglePassword}
                    edge="end"
                  >
                    {showPassword ? <VisibilityOff /> : <Visibility />}
                  </IconButton>
                </InputAdornment>
              ),
            }}
          />

          <Button
            type="submit"
            fullWidth
            variant="contained"
            size="large"
            sx={{ mt: 3, mb: 2, py: 1.5 }}
            disabled={loading}
          >
            {loading ? t('login.loggingIn') : t('login.login')}
          </Button>

          <Grid container spacing={2}>
            <Grid item xs={12} sm={6}>
              <Link to="/forgot-password" style={{ textDecoration: 'none' }}>
                <Button color="primary" fullWidth>
                  {t('login.forgotPassword')}
                </Button>
              </Link>
            </Grid>
            <Grid item xs={12} sm={6}>
              <Link to="/register" style={{ textDecoration: 'none' }}>
                <Button color="primary" fullWidth>
                  {t('login.noAccount')}
                </Button>
              </Link>
            </Grid>
          </Grid>
        </Box>
      </Paper>

      <Box sx={{ mt: 4, textAlign: 'center' }}>
        <Typography variant="body2" color="text.secondary">
          For demo purposes, you can use any email and password to log in.
        </Typography>
      </Box>
    </Container>
  );
};

export default LoginPage;
