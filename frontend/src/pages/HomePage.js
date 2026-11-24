import React from 'react';
import { PageLayout, Section } from '../design-system';
import HeroSection from '../components/HeroSection';
import FeaturesSection from '../components/FeaturesSection';
import TestimonialsSection from '../components/TestimonialsSection';

function HomePage() {
  return (
    <PageLayout 
      background="light" 
      padding="none"
      sx={{ pt: { xs: 0, md: 1 } }}
    >
      <HeroSection />
      <Section variant="default" background="white">
        <FeaturesSection />
      </Section>
      <Section variant="default" background="light">
        <TestimonialsSection />
      </Section>
    </PageLayout>
  );
}

export default HomePage;