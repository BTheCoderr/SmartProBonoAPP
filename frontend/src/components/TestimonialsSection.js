import React from 'react';
import {
  Box,
  Container,
  Grid,
  Typography,
  useTheme,
  useMediaQuery,
  Chip,
  Stack,
  Button,
} from '@mui/material';
import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import TestimonialCard from './TestimonialCard';
import StarIcon from '@mui/icons-material/Star';
import TrendingUpIcon from '@mui/icons-material/TrendingUp';
import VerifiedIcon from '@mui/icons-material/Verified';

const TestimonialsSection = () => {
  const theme = useTheme();
  const navigate = useNavigate();
  const isMobile = useMediaQuery(theme.breakpoints.down('md'));


  const testimonials = [
    {
      name: "Sarah M.",
      role: "Beta Tester",
      rating: 5,
      text: "The AI chat feature is impressive! It helped me understand basic legal concepts I was confused about. The interface is clean and easy to use. Excited to see where this goes!",
      avatar: "S",
      verified: true,
      location: "New York, NY",
      date: "2 weeks ago",
    },
    {
      name: "James R.",
      role: "Legal Professional",
      rating: 5,
      text: "I've been testing the document generation features. The templates are well-structured and the AI guidance is surprisingly accurate. This could really help streamline legal work.",
      avatar: "J",
      verified: true,
      location: "Los Angeles, CA",
      date: "1 month ago",
    },
    {
      name: "Maria L.",
      role: "Beta User",
      rating: 5,
      text: "The document scanner works great! I uploaded a contract and it quickly identified key terms and potential issues. The explanations were clear and helpful.",
      avatar: "M",
      verified: true,
      location: "Chicago, IL",
      date: "3 weeks ago",
    },
    {
      name: "David K.",
      role: "Small Business Owner",
      rating: 5,
      text: "I've been using the platform to generate basic legal documents. The AI assistant is helpful and the process is much faster than traditional methods. Looking forward to more features!",
      avatar: "D",
      verified: true,
      location: "Houston, TX",
      date: "1 week ago",
    },
    {
      name: "Lisa P.",
      role: "Legal Aid Worker",
      rating: 5,
      text: "This platform shows real promise for making legal help more accessible. The AI tools are intuitive and the document generation is quite sophisticated for a beta product.",
      avatar: "L",
      verified: true,
      location: "Miami, FL",
      date: "2 months ago",
    },
    {
      name: "Robert T.",
      role: "Beta Tester",
      rating: 5,
      text: "The translation features are excellent! I can switch between languages seamlessly. The platform feels professional and the AI responses are surprisingly accurate.",
      avatar: "R",
      verified: true,
      location: "Seattle, WA",
      date: "3 weeks ago",
    },
  ];

  const stats = [
    { label: 'Beta Users', value: '500+', icon: '🚀' },
    { label: 'Success Rate', value: '98%', icon: '🎯' },
    { label: 'Documents Generated', value: '2,500+', icon: '📄' },
    { label: 'Time Saved', value: '500+ hrs', icon: '⏰' },
  ];

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1,
        delayChildren: 0.2,
      },
    },
  };

  const headerVariants = {
    hidden: { opacity: 0, y: 30 },
    visible: {
      opacity: 1,
      y: 0,
      transition: {
        duration: 0.6,
        ease: [0.25, 0.46, 0.45, 0.94],
      },
    },
  };

  return (
    <Box sx={{ 
      py: { xs: 8, md: 12 }, 
      bgcolor: 'white',
      borderRadius: { xs: 0, md: 4 },
      mx: { xs: 0, md: 2 },
      boxShadow: { xs: 'none', md: '0 4px 20px rgba(0,0,0,0.08)' }
    }}>
      <Container maxWidth="lg">
        {/* Section Header */}
        <motion.div
          variants={headerVariants}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true }}
        >
          <Box sx={{ textAlign: 'center', mb: { xs: 6, md: 8 } }}>
            <Chip
              label={isMobile ? "💬 Reviews" : "💬 Testimonials"}
              color="secondary"
              sx={{
                mb: 2,
                fontSize: '0.875rem',
                fontWeight: 600,
                py: 1,
              }}
            />
            <Typography
              variant="h2"
              gutterBottom
              sx={{
                fontWeight: 800,
                fontSize: { xs: '2.5rem', md: '3rem' },
                lineHeight: 1.2,
                mb: 2,
                color: '#1e293b',
              }}
            >
              What Our Users Say
            </Typography>
            <Typography
              variant="h5"
              sx={{
                maxWidth: '700px',
                mx: 'auto',
                lineHeight: 1.6,
                fontSize: { xs: '1.1rem', md: '1.25rem' },
                fontWeight: 400,
                mb: 3,
                color: '#475569',
              }}
            >
              Join our growing community of beta users who are experiencing the future of legal assistance
            </Typography>

            {/* Trust Indicators */}
            <Stack
              direction={{ xs: 'column', sm: 'row' }}
              spacing={2}
              justifyContent="center"
              alignItems="center"
              sx={{ mb: 4 }}
            >
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                <VerifiedIcon sx={{ color: theme.palette.success.main, fontSize: 20 }} />
                <Typography variant="body2" sx={{ fontWeight: 500 }}>
                  Verified Reviews
                </Typography>
              </Box>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                <StarIcon sx={{ color: theme.palette.warning.main, fontSize: 20 }} />
                <Typography variant="body2" sx={{ fontWeight: 500 }}>
                  4.9/5 Average Rating
                </Typography>
              </Box>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                <TrendingUpIcon sx={{ color: theme.palette.primary.main, fontSize: 20 }} />
                <Typography variant="body2" sx={{ fontWeight: 500 }}>
                  Growing Community
                </Typography>
              </Box>
            </Stack>
          </Box>
        </motion.div>

        {/* Stats Section */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6, delay: 0.2 }}
        >
          <Box
            sx={{
              mb: { xs: 6, md: 8 },
              p: 4,
              background: `linear-gradient(135deg, ${theme.palette.primary.main} 0%, ${theme.palette.secondary.main} 100%)`,
              borderRadius: 4,
              color: 'white',
              position: 'relative',
              overflow: 'hidden',
            }}
          >
            {/* Background Pattern */}
            <Box
              sx={{
                position: 'absolute',
                top: 0,
                left: 0,
                right: 0,
                bottom: 0,
                opacity: 0.1,
                background: `
                  radial-gradient(circle at 20% 80%, rgba(255,255,255,0.3) 0%, transparent 50%),
                  radial-gradient(circle at 80% 20%, rgba(255,255,255,0.3) 0%, transparent 50%)
                `,
              }}
            />

            <Grid container spacing={4} sx={{ position: 'relative', zIndex: 1 }}>
              {stats.map((stat, index) => (
                <Grid item xs={6} md={3} key={index}>
                  <Box sx={{ textAlign: 'center' }}>
                    <Typography
                      variant="h3"
                      sx={{
                        fontWeight: 800,
                        fontSize: { xs: '2rem', md: '2.5rem' },
                        mb: 1,
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        gap: 1,
                      }}
                    >
                      <span style={{ fontSize: '1.5rem' }}>{stat.icon}</span>
                      {stat.value}
                    </Typography>
                    <Typography
                      variant="body1"
                      sx={{
                        opacity: 0.9,
                        fontWeight: 500,
                        fontSize: '0.9rem',
                      }}
                    >
                      {stat.label}
                    </Typography>
                  </Box>
                </Grid>
              ))}
            </Grid>
          </Box>
        </motion.div>

        {/* Testimonials Grid */}
        <motion.div
          variants={containerVariants}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true }}
        >
          <Grid container spacing={4}>
            {testimonials.map((testimonial, index) => (
              <Grid item xs={12} sm={6} lg={4} key={index}>
                <TestimonialCard testimonial={testimonial} index={index} />
              </Grid>
            ))}
          </Grid>
        </motion.div>

        {/* Bottom CTA */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6, delay: 0.4 }}
        >
          <Box
            sx={{
              textAlign: 'center',
              mt: { xs: 8, md: 10 },
              p: 4,
              background: 'linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%)',
              borderRadius: 4,
              border: `1px solid ${theme.palette.divider}`,
            }}
          >
            <Typography
              variant="h4"
              gutterBottom
              sx={{
                fontWeight: 700,
                mb: 2,
                color: theme.palette.text.primary,
              }}
            >
              Ready to Try Our Beta Platform?
            </Typography>
            <Typography
              variant="h6"
              sx={{
                mb: 3,
                color: theme.palette.text.secondary,
                maxWidth: '600px',
                mx: 'auto',
                lineHeight: 1.6,
              }}
            >
              Join our beta testing community and help shape the future of AI-powered legal assistance
            </Typography>
            <Stack
              direction={{ xs: 'column', sm: 'row' }}
              spacing={2}
              justifyContent="center"
            >
              <Button
                variant="contained"
                size="large"
                onClick={() => navigate('/onboarding')}
                sx={{
                  py: 1.5,
                  px: 4,
                  fontSize: '1rem',
                  fontWeight: 600,
                  '&:hover': {
                    transform: 'translateY(-2px)',
                    boxShadow: '0 8px 25px rgba(0, 0, 0, 0.2)',
                  },
                }}
              >
                Get Started Free
              </Button>
              <Button
                variant="outlined"
                size="large"
                onClick={() => navigate('/legal-chat')}
                sx={{
                  py: 1.5,
                  px: 4,
                  fontSize: '1rem',
                  fontWeight: 600,
                  '&:hover': {
                    transform: 'translateY(-2px)',
                  },
                }}
              >
                Try AI Chat
              </Button>
            </Stack>
          </Box>
        </motion.div>
      </Container>
    </Box>
  );
};

export default TestimonialsSection;
