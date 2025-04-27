import React from 'react';
import { 
  Container, 
  Box, 
  Typography, 
  Button,
  Paper,
  Grid
} from '@mui/material';
import { Link } from 'react-router-dom';
import LockIcon from '@mui/icons-material/Lock';

const UnauthorizedPage = () => {
  return (
    <Container maxWidth="md">
      <Box
        sx={{
          marginTop: 8,
          marginBottom: 8,
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
        }}
      >
        <Paper
          elevation={3}
          sx={{
            padding: 4,
            borderRadius: 2,
            textAlign: 'center',
          }}
        >
          <Box 
            sx={{ 
              display: 'flex',
              justifyContent: 'center',
              mb: 3
            }}
          >
            <LockIcon
              color="error"
              sx={{ 
                fontSize: 100,
                p: 2,
                borderRadius: '50%',
                bgcolor: 'error.light',
                color: 'error.main'
              }}
            />
          </Box>

          <Typography component="h1" variant="h4" gutterBottom>
            Access Denied
          </Typography>
          
          <Typography variant="body1" color="text.secondary" paragraph>
            You don't have permission to access this page. This area may require different access rights or a subscription upgrade.
          </Typography>
          
          <Grid container spacing={2} justifyContent="center" sx={{ mt: 3 }}>
            <Grid item>
              <Button
                component={Link}
                to="/"
                variant="contained"
                color="primary"
              >
                Go to Home
              </Button>
            </Grid>
            <Grid item>
              <Button
                component={Link}
                to="/subscription"
                variant="outlined"
                color="primary"
              >
                View Subscription Plans
              </Button>
            </Grid>
          </Grid>
        </Paper>
      </Box>
    </Container>
  );
};

export default UnauthorizedPage; 