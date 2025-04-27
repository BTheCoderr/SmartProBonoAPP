import React, { useState, useEffect } from 'react';
import {
  Container,
  Typography,
  Box,
  Paper,
  Grid,
  Card,
  CardContent,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Button,
  Alert,
  CircularProgress,
  Chip
} from '@mui/material';
import PersonIcon from '@mui/icons-material/Person';
import SecurityIcon from '@mui/icons-material/Security';
import GroupIcon from '@mui/icons-material/Group';
import GavelIcon from '@mui/icons-material/Gavel';
import DescriptionIcon from '@mui/icons-material/Description';
import axios from 'axios';
import { useAuth } from '../context/AuthContext';

// Mock data for users - in a real app this would come from an API
const mockUsers = [
  { id: 1, username: 'johnsmith', email: 'john@example.com', role: 'client', active: true, created_at: '2023-08-15T12:00:00Z' },
  { id: 2, username: 'sarahjones', email: 'sarah@example.com', role: 'lawyer', active: true, created_at: '2023-09-20T10:30:00Z' },
  { id: 3, username: 'mikebrown', email: 'mike@example.com', role: 'client', active: false, created_at: '2023-07-05T09:15:00Z' },
  { id: 4, username: 'emilydavis', email: 'emily@example.com', role: 'admin', active: true, created_at: '2023-06-10T14:45:00Z' },
  { id: 5, username: 'alexwilson', email: 'alex@example.com', role: 'client', active: true, created_at: '2023-10-25T11:20:00Z' }
];

// Stats cards data
const statsCardsData = [
  { title: 'Total Users', value: 153, icon: <PersonIcon fontSize="large" color="primary" /> },
  { title: 'Active Lawyers', value: 28, icon: <GavelIcon fontSize="large" color="success" /> },
  { title: 'Active Cases', value: 47, icon: <DescriptionIcon fontSize="large" color="warning" /> },
  { title: 'New Users (Last 30d)', value: 21, icon: <GroupIcon fontSize="large" color="info" /> }
];

const AdminDashboard = () => {
  const { currentUser } = useAuth();
  const [users, setUsers] = useState(mockUsers);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // In a real application, you would fetch users from your API
  useEffect(() => {
    // Simulating API call
    setLoading(true);
    setTimeout(() => {
      setUsers(mockUsers);
      setLoading(false);
    }, 1000);

    // Real API call would look like:
    // const fetchUsers = async () => {
    //   try {
    //     setLoading(true);
    //     const response = await axios.get('/api/admin/users');
    //     setUsers(response.data.users);
    //   } catch (error) {
    //     setError('Failed to load users');
    //     console.error(error);
    //   } finally {
    //     setLoading(false);
    //   }
    // };
    // fetchUsers();
  }, []);

  const formatDate = (dateString) => {
    const options = { year: 'numeric', month: 'short', day: 'numeric' };
    return new Date(dateString).toLocaleDateString(undefined, options);
  };

  if (!currentUser || currentUser.role !== 'admin') {
    return (
      <Container maxWidth="md" sx={{ mt: 4 }}>
        <Alert severity="error">
          You do not have permission to access this page. This area is restricted to administrators.
        </Alert>
      </Container>
    );
  }

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          Admin Dashboard
        </Typography>
        <Typography variant="subtitle1" color="text.secondary">
          Welcome back, {currentUser.first_name || currentUser.username}! Here's what's happening with your system.
        </Typography>
      </Box>

      {/* Stats Cards */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        {statsCardsData.map((stat, index) => (
          <Grid item xs={12} sm={6} md={3} key={index}>
            <Card elevation={2}>
              <CardContent sx={{ textAlign: 'center', py: 3 }}>
                <Box sx={{ mb: 2 }}>
                  {stat.icon}
                </Box>
                <Typography variant="h5" component="div">
                  {stat.value}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  {stat.title}
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      {/* User Management */}
      <Paper elevation={2} sx={{ p: 3, mb: 4 }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
          <Typography variant="h5" component="h2">
            <SecurityIcon sx={{ mr: 1, verticalAlign: 'middle' }} />
            User Management
          </Typography>
          <Button variant="contained" color="primary">
            Add New User
          </Button>
        </Box>

        {error && (
          <Alert severity="error" sx={{ mb: 3 }}>
            {error}
          </Alert>
        )}

        {loading ? (
          <Box sx={{ display: 'flex', justifyContent: 'center', p: 3 }}>
            <CircularProgress />
          </Box>
        ) : (
          <TableContainer>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>Username</TableCell>
                  <TableCell>Email</TableCell>
                  <TableCell>Role</TableCell>
                  <TableCell>Status</TableCell>
                  <TableCell>Created</TableCell>
                  <TableCell>Actions</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {users.map((user) => (
                  <TableRow key={user.id}>
                    <TableCell>{user.username}</TableCell>
                    <TableCell>{user.email}</TableCell>
                    <TableCell>
                      <Chip 
                        label={user.role.charAt(0).toUpperCase() + user.role.slice(1)} 
                        color={
                          user.role === 'admin' 
                            ? 'error' 
                            : user.role === 'lawyer' 
                              ? 'success' 
                              : 'primary'
                        }
                        size="small"
                      />
                    </TableCell>
                    <TableCell>
                      <Chip 
                        label={user.active ? 'Active' : 'Inactive'} 
                        color={user.active ? 'success' : 'default'}
                        size="small"
                      />
                    </TableCell>
                    <TableCell>{formatDate(user.created_at)}</TableCell>
                    <TableCell>
                      <Button size="small" sx={{ mr: 1 }}>Edit</Button>
                      <Button size="small" color="error">
                        {user.active ? 'Deactivate' : 'Activate'}
                      </Button>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        )}
      </Paper>

      {/* System Information */}
      <Paper elevation={2} sx={{ p: 3 }}>
        <Typography variant="h5" component="h2" gutterBottom>
          System Information
        </Typography>
        <Grid container spacing={2}>
          <Grid item xs={12} md={4}>
            <Typography variant="subtitle2">Application Version</Typography>
            <Typography variant="body1">1.0.0 (Build 124)</Typography>
          </Grid>
          <Grid item xs={12} md={4}>
            <Typography variant="subtitle2">Last Database Backup</Typography>
            <Typography variant="body1">Today at 03:00 AM</Typography>
          </Grid>
          <Grid item xs={12} md={4}>
            <Typography variant="subtitle2">Server Status</Typography>
            <Chip label="Online" color="success" size="small" />
          </Grid>
        </Grid>
      </Paper>
    </Container>
  );
};

export default AdminDashboard; 