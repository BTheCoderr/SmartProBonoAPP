import React from 'react';
import { Box } from '@mui/material';
import HeroSection from '../components/HeroSection';
import FeaturesSection from '../components/FeaturesSection';
import TestimonialsSection from '../components/TestimonialsSection';
import Footer from '../components/Footer';

function HomePage() {
  return (
    <Box sx={{ 
      minHeight: '100vh',
      backgroundColor: '#fafafa',
      pt: { xs: 8, md: 10 } // Add top padding to account for fixed header
    }}>
      <HeroSection />
      <Box sx={{ py: { xs: 6, md: 8 } }}>
        <FeaturesSection />
      </Box>
      <Box sx={{ py: { xs: 6, md: 8 } }}>
        <TestimonialsSection />
      </Box>
      <Footer />
    </Box>
  );
}

export default HomePage;