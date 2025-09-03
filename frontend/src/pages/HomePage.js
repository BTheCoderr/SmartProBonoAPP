import React from 'react';
import { PageLayout, Section } from '../design-system';
import HeroSection from '../components/HeroSection';
import FeaturesSection from '../components/FeaturesSection';
import TestimonialsSection from '../components/TestimonialsSection';
import Footer from '../components/Footer';
import TestPage from './TestPage';

function HomePage() {
  return (
    <PageLayout 
      background="light" 
      padding="none"
      sx={{ pt: { xs: 8, md: 10 } }} // Add top padding to account for fixed header
    >
      <HeroSection />
      <Section variant="default" background="white">
        <FeaturesSection />
      </Section>
      <Section variant="default" background="light">
        <TestimonialsSection />
      </Section>
      <Section variant="default" background="white">
        <TestPage />
      </Section>
      <Footer />
    </PageLayout>
  );
}

export default HomePage;