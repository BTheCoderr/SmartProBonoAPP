import React, { useEffect } from 'react';
import { Navigate, Outlet, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { Box, CircularProgress, Typography } from '@mui/material';

const ProtectedRoute = ({ requiredRole }) => {
  const { currentUser, isAuthenticated, loading } = useAuth();
  const location = useLocation();

  // Add debug logging
  useEffect(() => {
    console.log('ProtectedRoute check for path:', location.pathname);
    console.log('isAuthenticated:', isAuthenticated);
    console.log('loading:', loading);
    console.log('currentUser:', currentUser);
  }, [isAuthenticated, loading, currentUser, location]);

  // Show loading spinner while checking authentication
  if (loading) {
    console.log('ProtectedRoute is loading...');
    return (
      <Box 
        sx={{
          display: 'flex', 
          justifyContent: 'center', 
          alignItems: 'center',
          flexDirection: 'column',
          height: '100vh',
          bgcolor: '#f5f5f5'
        }}
      >
        <CircularProgress size={60} />
        <Typography variant="h6" sx={{ mt: 2 }}>
          Checking Authentication...
        </Typography>
      </Box>
    );
  }

  // Check if user is authenticated
  if (!isAuthenticated) {
    console.log('ProtectedRoute - Not authenticated, redirecting to login');
    return <Navigate to="/login" state={{ from: location.pathname }} replace />;
  }

  // If a specific role is required, check if user has that role
  if (requiredRole && currentUser?.role !== requiredRole) {
    console.log(`ProtectedRoute - User does not have required role: ${requiredRole}`);
    return <Navigate to="/unauthorized" replace />;
  }

  // User is authenticated and has the required role (if specified)
  console.log('ProtectedRoute - Access granted');
  return <Outlet />;
};

export default ProtectedRoute; 