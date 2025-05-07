import React from 'react';
import { Container, Typography, Box } from '@mui/material';

const About = () => {
  return (
    <Container maxWidth="lg">
      <Box py={4}>
        <Typography variant="h2" component="h1" gutterBottom>
          About SmartProBono
        </Typography>
        <Typography variant="body1" paragraph>
          SmartProBono is a platform dedicated to making legal services more accessible
          to those who need it most. We leverage technology to connect clients with
          pro bono legal services and resources.
        </Typography>
      </Box>
    </Container>
  );
};

export default About; 