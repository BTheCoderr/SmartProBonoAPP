import React from 'react';
import { Container, Typography, Box } from '@mui/material';

const Home = () => {
  return (
    <Container maxWidth="lg">
      <Box py={4}>
        <Typography variant="h1" component="h1" gutterBottom>
          Welcome to SmartProBono
        </Typography>
        <Typography variant="h5" component="h2" gutterBottom>
          Empowering access to justice through technology
        </Typography>
      </Box>
    </Container>
  );
};

export default Home; 