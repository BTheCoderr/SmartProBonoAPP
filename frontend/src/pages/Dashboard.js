import React from 'react';
import { Container, Typography, Box, Grid, Paper } from '@mui/material';
import { useAuth } from '../context/AuthContext';

const Dashboard = () => {
  const { user } = useAuth();

  return (
    <Container maxWidth="lg">
      <Box py={4}>
        <Typography variant="h2" component="h1" gutterBottom>
          Dashboard
        </Typography>
        <Typography variant="h6" gutterBottom>
          Welcome back, {user?.name || 'User'}
        </Typography>
        
        <Grid container spacing={3} mt={2}>
          <Grid item xs={12} md={6}>
            <Paper sx={{ p: 3 }}>
              <Typography variant="h6" gutterBottom>
                Recent Activity
              </Typography>
              <Typography variant="body1">
                No recent activity to display.
              </Typography>
            </Paper>
          </Grid>
          
          <Grid item xs={12} md={6}>
            <Paper sx={{ p: 3 }}>
              <Typography variant="h6" gutterBottom>
                Quick Actions
              </Typography>
              <Typography variant="body1">
                No actions available.
              </Typography>
            </Paper>
          </Grid>
        </Grid>
      </Box>
    </Container>
  );
};

export default Dashboard; 