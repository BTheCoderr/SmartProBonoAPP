import React from 'react';
import { Container, Typography, Box, Paper } from '@mui/material';

const AIVirtualParalegalTest = () => {
  return (
    <Container maxWidth="xl" sx={{ py: 4 }}>
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          AI Virtual Paralegal - Test Page
        </Typography>
        <Typography variant="body1" color="text.secondary">
          This is a test page to verify the route is working.
        </Typography>
      </Box>

      <Paper sx={{ p: 3 }}>
        <Typography variant="h6" gutterBottom>
          ✅ Route is working!
        </Typography>
        <Typography variant="body1">
          The AI Virtual Paralegal route is now accessible. 
          The full component will be loaded once we fix any import issues.
        </Typography>
      </Paper>
    </Container>
  );
};

export default AIVirtualParalegalTest;

