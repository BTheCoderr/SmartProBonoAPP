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
import { useTranslation } from 'react-i18next';
import ChatIcon from '@mui/icons-material/Chat';
import GavelIcon from '@mui/icons-material/Gavel';
import DescriptionIcon from '@mui/icons-material/Description';
import ListAltIcon from '@mui/icons-material/ListAlt';
import FlightIcon from '@mui/icons-material/Flight';
import BuildIcon from '@mui/icons-material/Build';
import PersonIcon from '@mui/icons-material/Person';

const FeaturesSection = () => {
  const { t } = useTranslation();
  const theme = useTheme();
  const navigate = useNavigate();

  const features = [
    {
      title: t('features.items.aiLegalAssistant.title'),
      description: t('features.items.aiLegalAssistant.description'),
      icon: <ChatIcon sx={{ fontSize: 48, color: theme.palette.primary.main }} />,
      path: '/legal-chat',
      color: 'primary',
      badge: t('features.items.aiLegalAssistant.badge'),
      benefits: t('features.items.aiLegalAssistant.benefits'),
      gradient: `linear-gradient(135deg, ${theme.palette.primary.light} 0%, ${theme.palette.primary.main} 100%)`,
    },
    {
      title: t('features.items.documentGeneration.title'),
      description: t('features.items.documentGeneration.description'),
      icon: <DescriptionIcon sx={{ fontSize: 48, color: theme.palette.secondary.main }} />,
      path: '/services/contracts',
      color: 'secondary',
      badge: t('features.items.documentGeneration.badge'),
      benefits: t('features.items.documentGeneration.benefits'),
      gradient: `linear-gradient(135deg, ${theme.palette.secondary.light} 0%, ${theme.palette.secondary.main} 100%)`,
    },
    {
      title: t('features.items.knowYourRights.title'),
      description: t('features.items.knowYourRights.description'),
      icon: <GavelIcon sx={{ fontSize: 48, color: theme.palette.success.main }} />,
      path: '/resources/rights',
      color: 'success',
      benefits: t('features.items.knowYourRights.benefits'),
      gradient: `linear-gradient(135deg, ${theme.palette.success.light} 0%, ${theme.palette.success.main} 100%)`,
    },
    {
      title: t('features.items.virtualParalegal.title'),
      description: t('features.items.virtualParalegal.description'),
      icon: <PersonIcon sx={{ fontSize: 48, color: theme.palette.info.main }} />,
      path: '/virtual-paralegal',
      color: 'info',
      badge: t('features.items.virtualParalegal.badge'),
      benefits: t('features.items.virtualParalegal.benefits'),
      gradient: `linear-gradient(135deg, ${theme.palette.info.light} 0%, ${theme.palette.info.main} 100%)`,
    },
    {
      title: t('features.items.immigrationHelp.title'),
      description: t('features.items.immigrationHelp.description'),
      icon: <FlightIcon sx={{ fontSize: 48, color: theme.palette.warning.main }} />,
      path: '/services/immigration',
      color: 'warning',
      benefits: t('features.items.immigrationHelp.benefits'),
      gradient: `linear-gradient(135deg, ${theme.palette.warning.light} 0%, ${theme.palette.warning.main} 100%)`,
    },
    {
      title: t('features.items.proBonoServices.title'),
      description: t('features.items.proBonoServices.description'),
      icon: <BuildIcon sx={{ fontSize: 48, color: theme.palette.error.main }} />,
      path: '/services',
      color: 'error',
      benefits: t('features.items.proBonoServices.benefits'),
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
      title: t('features.items.documentScanner.title'),
      description: t('features.items.documentScanner.description'),
      icon: <DescriptionIcon sx={{ fontSize: 48, color: theme.palette.secondary.main }} />,
      path: '/scan-document',
      color: 'secondary',
      badge: t('features.items.documentScanner.badge'),
      benefits: t('features.items.documentScanner.benefits'),
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
      bgcolor: '#FAFBFC',
      borderTop: '1px solid',
      borderColor: 'divider',
    }}>
      <Container maxWidth="lg">
        {/* Section Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.5 }}
        >
          <Box sx={{ textAlign: 'center', mb: { xs: 6, md: 8 } }}>
            <Chip
              label={t('features.badge')}
              sx={{
                mb: 2,
                fontSize: '0.75rem',
                fontWeight: 600,
                height: 28,
                backgroundColor: theme.palette.primary.main,
                color: 'white',
              }}
            />
            <Typography
              variant="h2"
              gutterBottom
              sx={{
                fontWeight: 700,
                fontSize: { xs: '2.25rem', md: '2.75rem' },
                lineHeight: 1.2,
                mb: 2,
                color: '#0F172A',
                letterSpacing: '-0.02em',
              }}
            >
              {t('features.title')}
            </Typography>
            <Typography
              variant="h6"
              sx={{
                maxWidth: '600px',
                mx: 'auto',
                lineHeight: 1.7,
                fontSize: { xs: '1rem', md: '1.125rem' },
                fontWeight: 400,
                color: '#64748B',
              }}
            >
              {t('features.subtitle')}
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
                      background: '#ffffff',
                      border: `1px solid ${theme.palette.divider}`,
                      borderRadius: 2,
                      transition: 'all 0.2s ease',
                      '&:hover': {
                        borderColor: theme.palette.primary.main,
                        boxShadow: '0 4px 12px rgba(15, 61, 94, 0.08)',
                        transform: 'translateY(-2px)',
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


                    <CardContent sx={{ flexGrow: 1, p: 3, position: 'relative', zIndex: 1 }}>
                      {/* Icon */}
                      <Box
                        sx={{
                          mb: 2,
                          display: 'flex',
                          justifyContent: 'center',
                        }}
                      >
                        <Box
                          sx={{
                            p: 2,
                            borderRadius: 2,
                            backgroundColor: '#F8FAFC',
                            display: 'inline-flex',
                          }}
                        >
                          {feature.icon}
                        </Box>
                      </Box>

                      {/* Title */}
                      <Typography
                        variant="h6"
                        gutterBottom
                        sx={{
                          fontWeight: 600,
                          fontSize: '1.125rem',
                          lineHeight: 1.3,
                          mb: 1.5,
                          textAlign: 'center',
                          color: '#0F172A',
                        }}
                      >
                        {feature.title}
                      </Typography>

                      {/* Description */}
                      <Typography
                        sx={{
                          mb: 3,
                          lineHeight: 1.6,
                          textAlign: 'center',
                          fontSize: '0.9375rem',
                          color: '#64748B',
                        }}
                      >
                        {feature.description}
                      </Typography>

                      {/* Benefits */}
                      <Box sx={{ mb: 3 }}>
                        <Stack direction="row" spacing={1} flexWrap="wrap" justifyContent="center">
                          {(Array.isArray(feature.benefits) ? feature.benefits : []).map((benefit, idx) => (
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
                        variant="outlined"
                        size="medium"
                        fullWidth
                        sx={{
                          borderColor: theme.palette.divider,
                          color: 'text.primary',
                          fontWeight: 600,
                          py: 1.25,
                          px: 3,
                          fontSize: '0.875rem',
                          borderRadius: 2,
                          textTransform: 'none',
                          '&:hover': {
                            borderColor: theme.palette.primary.main,
                            backgroundColor: 'rgba(15, 61, 94, 0.04)',
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
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.5, delay: 0.2 }}
        >
          <Box
            sx={{
              textAlign: 'center',
              mt: { xs: 8, md: 10 },
              p: 5,
              background: '#ffffff',
              borderRadius: 3,
              border: '1px solid',
              borderColor: 'divider',
            }}
          >
            <Typography
              variant="h4"
              gutterBottom
              sx={{
                fontWeight: 700,
                mb: 2,
                color: '#0F172A',
                fontSize: { xs: '1.75rem', md: '2rem' },
              }}
            >
              Ready to Get Started?
            </Typography>
            <Typography
              variant="h6"
              sx={{
                mb: 4,
                maxWidth: '600px',
                mx: 'auto',
                color: '#64748B',
                fontSize: { xs: '1rem', md: '1.125rem' },
                fontWeight: 400,
              }}
            >
              Join thousands of users who have already found the legal help they need
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
                  backgroundColor: theme.palette.primary.main,
                  color: 'white',
                  fontWeight: 600,
                  py: 1.5,
                  px: 4,
                  fontSize: '1rem',
                  borderRadius: 2,
                  textTransform: 'none',
                  '&:hover': {
                    backgroundColor: theme.palette.primary.dark,
                    transform: 'translateY(-1px)',
                    boxShadow: '0 4px 12px rgba(15, 61, 94, 0.3)',
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
                  borderColor: theme.palette.divider,
                  color: 'text.primary',
                  fontWeight: 600,
                  py: 1.5,
                  px: 4,
                  fontSize: '1rem',
                  borderRadius: 2,
                  textTransform: 'none',
                  '&:hover': {
                    borderColor: theme.palette.primary.main,
                    backgroundColor: 'rgba(15, 61, 94, 0.04)',
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
