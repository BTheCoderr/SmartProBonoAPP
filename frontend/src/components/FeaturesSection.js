import React from 'react';
import {
  Box,
  Container,
  Grid,
  Typography,
  Card,
  CardContent,
  CardActions,
  Button,
  useTheme,
  Chip,
  Stack,
} from '@mui/material';
import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import ChatIcon from '@mui/icons-material/Chat';
import GavelIcon from '@mui/icons-material/Gavel';
import DescriptionIcon from '@mui/icons-material/Description';
import ListAltIcon from '@mui/icons-material/ListAlt';
import FlightIcon from '@mui/icons-material/Flight';
import BuildIcon from '@mui/icons-material/Build';
import PersonIcon from '@mui/icons-material/Person';

const FeaturesSection = () => {
  const theme = useTheme();
  const navigate = useNavigate();

  const features = [
    {
      title: "AI Legal Assistant",
      description: "Get instant answers to your legal questions 24/7 with our advanced AI-powered chat system",
      icon: <ChatIcon sx={{ fontSize: 48, color: theme.palette.primary.main }} />,
      path: '/legal-chat',
      color: 'primary',
      badge: "Most Popular",
      benefits: ["24/7 Availability", "Instant Responses", "Legal Expertise"],
      gradient: `linear-gradient(135deg, ${theme.palette.primary.light} 0%, ${theme.palette.primary.main} 100%)`,
    },
    {
      title: "Document Generation",
      description: "Create professional legal documents with AI assistance and customizable templates",
      icon: <DescriptionIcon sx={{ fontSize: 48, color: theme.palette.secondary.main }} />,
      path: '/services/contracts',
      color: 'secondary',
      badge: "New",
      benefits: ["AI-Powered", "Custom Templates", "Legal Compliance"],
      gradient: `linear-gradient(135deg, ${theme.palette.secondary.light} 0%, ${theme.palette.secondary.main} 100%)`,
    },
    {
      title: "Know Your Rights",
      description: "Get instant information about your legal rights and protections in various areas",
      icon: <GavelIcon sx={{ fontSize: 48, color: theme.palette.success.main }} />,
      path: '/resources/rights',
      color: 'success',
      benefits: ["Comprehensive Guide", "Easy to Understand", "Up-to-Date"],
      gradient: `linear-gradient(135deg, ${theme.palette.success.light} 0%, ${theme.palette.success.main} 100%)`,
    },
    {
      title: "Virtual Paralegal",
      description: "AI-powered paralegal assistance for attorneys and legal aid organizations",
      icon: <PersonIcon sx={{ fontSize: 48, color: theme.palette.info.main }} />,
      path: '/virtual-paralegal',
      color: 'info',
      badge: "Pro Feature",
      benefits: ["Time Saving", "Cost Effective", "Professional Grade"],
      gradient: `linear-gradient(135deg, ${theme.palette.info.light} 0%, ${theme.palette.info.main} 100%)`,
    },
    {
      title: "Immigration Help",
      description: "Comprehensive support for visa applications and immigration processes",
      icon: <FlightIcon sx={{ fontSize: 48, color: theme.palette.warning.main }} />,
      path: '/services/immigration',
      color: 'warning',
      benefits: ["Step-by-Step Guide", "Form Assistance", "Expert Tips"],
      gradient: `linear-gradient(135deg, ${theme.palette.warning.light} 0%, ${theme.palette.warning.main} 100%)`,
    },
    {
      title: "Pro Bono Services",
      description: "Connect with legal professionals offering free services and assistance",
      icon: <BuildIcon sx={{ fontSize: 48, color: theme.palette.error.main }} />,
      path: '/services',
      color: 'error',
      benefits: ["Free Services", "Expert Attorneys", "Local Support"],
      gradient: `linear-gradient(135deg, ${theme.palette.error.light} 0%, ${theme.palette.error.main} 100%)`,
    },
    {
      title: "Legal Resources",
      description: "Access helpful legal resources, guides, and educational materials",
      icon: <ListAltIcon sx={{ fontSize: 48, color: theme.palette.primary.main }} />,
      path: '/resources',
      color: 'primary',
      benefits: ["Educational Content", "Legal Updates", "Best Practices"],
      gradient: `linear-gradient(135deg, ${theme.palette.primary.light} 0%, ${theme.palette.primary.main} 100%)`,
    },
    {
      title: "Document Scanner",
      description: "AI-powered document analysis and legal document processing",
      icon: <DescriptionIcon sx={{ fontSize: 48, color: theme.palette.secondary.main }} />,
      path: '/scan-document',
      color: 'secondary',
      badge: "AI-Powered",
      benefits: ["OCR Technology", "Legal Analysis", "Smart Processing"],
      gradient: `linear-gradient(135deg, ${theme.palette.secondary.light} 0%, ${theme.palette.secondary.main} 100%)`,
    },
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

  const cardVariants = {
    hidden: { 
      opacity: 0, 
      y: 50,
      scale: 0.95
    },
    visible: { 
      opacity: 1, 
      y: 0,
      scale: 1,
      transition: {
        duration: 0.6,
        ease: [0.25, 0.46, 0.45, 0.94]
      }
    },
    hover: {
      y: -8,
      scale: 1.02,
      transition: {
        duration: 0.3,
        ease: "easeOut"
      }
    }
  };

  const getBadgeColor = (badge) => {
    const badgeColors = {
      "Most Popular": "primary",
      "New": "success",
      "Pro Feature": "warning",
      "AI-Powered": "secondary",
    };
    return badgeColors[badge] || "default";
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
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
        >
          <Box sx={{ textAlign: 'center', mb: { xs: 6, md: 8 } }}>
            <Chip
              label="🚀 Our Services"
              color="primary"
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
              Everything You Need for
              <br />
              Legal Assistance
            </Typography>
            <Typography
              variant="h5"
              sx={{
                maxWidth: '700px',
                mx: 'auto',
                lineHeight: 1.6,
                fontSize: { xs: '1.1rem', md: '1.25rem' },
                fontWeight: 400,
                color: '#475569',
              }}
            >
              Comprehensive legal tools and resources designed to make legal help accessible, 
              affordable, and easy to understand for everyone.
            </Typography>
          </Box>
        </motion.div>

        {/* Features Grid */}
        <motion.div
          variants={containerVariants}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true }}
        >
          <Grid container spacing={4}>
            {features.map((feature, index) => (
              <Grid item xs={12} sm={6} lg={4} key={index}>
                <motion.div variants={cardVariants}>
                  <Card
                    sx={{
                      height: '100%',
                      display: 'flex',
                      flexDirection: 'column',
                      position: 'relative',
                      overflow: 'hidden',
                      background: 'linear-gradient(135deg, #ffffff 0%, #f8fafc 100%)',
                      border: `1px solid ${theme.palette.divider}`,
                      '&:hover': {
                        '& .feature-icon': {
                          transform: 'scale(1.1) rotate(5deg)',
                        },
                        '& .feature-badge': {
                          transform: 'scale(1.05)',
                        },
                      },
                    }}
                  >
                    {/* Badge */}
                    {feature.badge && (
                      <Box
                        className="feature-badge"
                        sx={{
                          position: 'absolute',
                          top: 16,
                          right: 16,
                          zIndex: 1,
                          transition: 'transform 0.3s ease',
                        }}
                      >
                        <Chip
                          label={feature.badge}
                          color={getBadgeColor(feature.badge)}
                          size="small"
                          sx={{
                            fontWeight: 600,
                            fontSize: '0.75rem',
                            height: 24,
                          }}
                        />
                      </Box>
                    )}

                    {/* Icon Background */}
                    <Box
                      sx={{
                        position: 'absolute',
                        top: -20,
                        right: -20,
                        width: 120,
                        height: 120,
                        borderRadius: '50%',
                        background: feature.gradient,
                        opacity: 0.1,
                        zIndex: 0,
                      }}
                    />

                    <CardContent sx={{ flexGrow: 1, p: 3, position: 'relative', zIndex: 1 }}>
                      {/* Icon */}
                      <Box
                        className="feature-icon"
                        sx={{
                          mb: 2,
                          transition: 'transform 0.3s ease',
                          display: 'flex',
                          justifyContent: 'center',
                        }}
                      >
                        {feature.icon}
                      </Box>

                      {/* Title */}
                      <Typography
                        variant="h5"
                        gutterBottom
                        sx={{
                          fontWeight: 700,
                          fontSize: '1.25rem',
                          lineHeight: 1.3,
                          mb: 2,
                          textAlign: 'center',
                        }}
                      >
                        {feature.title}
                      </Typography>

                      {/* Description */}
                      <Typography
                        color="text.secondary"
                        sx={{
                          mb: 3,
                          lineHeight: 1.6,
                          textAlign: 'center',
                          fontSize: '0.95rem',
                        }}
                      >
                        {feature.description}
                      </Typography>

                      {/* Benefits */}
                      <Box sx={{ mb: 3 }}>
                        <Stack direction="row" spacing={1} flexWrap="wrap" justifyContent="center">
                          {feature.benefits.map((benefit, idx) => (
                            <Chip
                              key={idx}
                              label={benefit}
                              size="small"
                              variant="outlined"
                              sx={{
                                fontSize: '0.75rem',
                                height: 24,
                                fontWeight: 500,
                                borderColor: theme.palette.divider,
                                color: theme.palette.text.secondary,
                              }}
                            />
                          ))}
                        </Stack>
                      </Box>
                    </CardContent>

                    <CardActions sx={{ justifyContent: 'center', p: 3, pt: 0 }}>
                      <Button
                        onClick={() => navigate(feature.path)}
                        variant="contained"
                        size="large"
                        fullWidth
                        sx={{
                          background: feature.gradient,
                          color: 'white',
                          fontWeight: 600,
                          py: 1.5,
                          px: 3,
                          fontSize: '0.875rem',
                          '&:hover': {
                            background: feature.gradient,
                            transform: 'translateY(-2px)',
                            boxShadow: '0 8px 25px rgba(0, 0, 0, 0.2)',
                          },
                        }}
                      >
                        Learn More
                      </Button>
                    </CardActions>
                  </Card>
                </motion.div>
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

            <Typography
              variant="h4"
              gutterBottom
              sx={{
                fontWeight: 700,
                mb: 2,
                position: 'relative',
                zIndex: 1,
              }}
            >
              Ready to Get Started?
            </Typography>
            <Typography
              variant="h6"
              sx={{
                mb: 3,
                opacity: 0.9,
                maxWidth: '600px',
                mx: 'auto',
                position: 'relative',
                zIndex: 1,
              }}
            >
              Join thousands of users who have already found the legal help they need
            </Typography>
            <Stack
              direction={{ xs: 'column', sm: 'row' }}
              spacing={2}
              justifyContent="center"
              sx={{ position: 'relative', zIndex: 1 }}
            >
              <Button
                variant="contained"
                size="large"
                onClick={() => navigate('/onboarding')}
                sx={{
                  backgroundColor: 'white',
                  color: theme.palette.primary.main,
                  fontWeight: 700,
                  py: 1.5,
                  px: 4,
                  fontSize: '1rem',
                  '&:hover': {
                    backgroundColor: 'rgba(255, 255, 255, 0.9)',
                    transform: 'translateY(-2px)',
                    boxShadow: '0 8px 25px rgba(0, 0, 0, 0.2)',
                  },
                }}
              >
                Start Free Trial
              </Button>
              <Button
                variant="outlined"
                size="large"
                onClick={() => navigate('/legal-chat')}
                sx={{
                  borderColor: 'rgba(255, 255, 255, 0.8)',
                  color: 'white',
                  fontWeight: 600,
                  py: 1.5,
                  px: 4,
                  fontSize: '1rem',
                  '&:hover': {
                    borderColor: 'white',
                    backgroundColor: 'rgba(255, 255, 255, 0.1)',
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

export default FeaturesSection;
