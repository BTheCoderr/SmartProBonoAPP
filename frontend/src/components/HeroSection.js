import React from 'react';
import {
  Box,
  Container,
  Grid,
  Typography,
  Button,
  useTheme,
  Chip,
  Stack,
} from '@mui/material';
import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { useAuth } from '../context/AuthContext';
import ChatIcon from '@mui/icons-material/Chat';
import DocumentScannerIcon from '@mui/icons-material/DocumentScanner';
import OnboardingIcon from '@mui/icons-material/PlayArrow';
import SecurityIcon from '@mui/icons-material/Security';
import VerifiedUserIcon from '@mui/icons-material/VerifiedUser';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import SupportIcon from '@mui/icons-material/Support';

const HeroSection = () => {
  const { t } = useTranslation();
  const theme = useTheme();
  const navigate = useNavigate();
  const { mockLogin, isAuthenticated, currentUser } = useAuth();

  const itemVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: {
      opacity: 1,
      y: 0,
      transition: {
        duration: 0.5,
        ease: [0.25, 0.46, 0.45, 0.94],
      },
    },
  };

  const trustSignals = [
    {
      icon: <SecurityIcon sx={{ fontSize: 20, color: theme.palette.success.main }} />,
      text: t('hero.features.bankLevelSecurity'),
    },
    {
      icon: <VerifiedUserIcon sx={{ fontSize: 20, color: theme.palette.primary.main }} />,
      text: t('hero.features.licensedAttorneys'),
    },
    {
      icon: <CheckCircleIcon sx={{ fontSize: 20, color: theme.palette.warning.main }} />,
      text: t('hero.features.abaCompliant'),
    },
    {
      icon: <SupportIcon sx={{ fontSize: 20, color: theme.palette.info.main }} />,
      text: t('hero.features.expertSupport'),
    },
  ];

  return (
    <Box
      sx={{
        background: '#ffffff',
        color: 'text.primary',
        position: 'relative',
        pt: { xs: 10, md: 16 },
        pb: { xs: 8, md: 12 },
        borderBottom: '1px solid',
        borderColor: 'divider',
      }}
    >
      <Container maxWidth="lg">
        <Grid container spacing={6} alignItems="center">
          {/* Left Content */}
          <Grid item xs={12} md={7}>
            <motion.div
              initial="hidden"
              animate="visible"
              variants={itemVariants}
            >
              {/* Badge */}
              <Chip
                label={t('hero.badge')}
                sx={{
                  mb: 3,
                  backgroundColor: theme.palette.primary.main,
                  color: 'white',
                  fontWeight: 600,
                  fontSize: '0.75rem',
                  height: 28,
                }}
              />

              {/* Main Heading */}
              <Typography
                variant="h1"
                gutterBottom
                sx={{
                  fontWeight: 700,
                  fontSize: { xs: '2.5rem', sm: '3rem', md: '3.75rem' },
                  lineHeight: 1.1,
                  mb: 3,
                  color: '#0F172A',
                  letterSpacing: '-0.02em',
                }}
              >
                {t('hero.title')}
                <br />
                <Box
                  component="span"
                  sx={{
                    color: theme.palette.primary.main,
                  }}
                >
                  {t('hero.subtitle')}
                </Box>
              </Typography>

              {/* Subtitle */}
              <Typography
                variant="h6"
                paragraph
                sx={{
                  mb: 4,
                  maxWidth: '600px',
                  lineHeight: 1.7,
                  fontSize: { xs: '1rem', md: '1.125rem' },
                  fontWeight: 400,
                  color: '#64748B',
                }}
              >
                {t('hero.description')}
              </Typography>

              {/* CTA Buttons */}
              <Stack
                direction={{ xs: 'column', sm: 'row' }}
                spacing={2}
                sx={{ mb: 5 }}
              >
                {!isAuthenticated && (
                  <Button
                    variant="contained"
                    size="large"
                    onClick={mockLogin}
                    startIcon={<OnboardingIcon />}
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
                    {t('hero.getStarted')}
                  </Button>
                )}
                
                <Button
                  variant="outlined"
                  size="large"
                  startIcon={<DocumentScannerIcon />}
                  onClick={() => navigate('/scan-document')}
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
                  {t('hero.buttons.scanDocuments')}
                </Button>

                <Button
                  variant="outlined"
                  size="large"
                  startIcon={<ChatIcon />}
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
                  {t('hero.buttons.aiLegalChat')}
                </Button>
              </Stack>

              {/* Trust Signals */}
              <Box
                sx={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: 3,
                  flexWrap: 'wrap',
                }}
              >
                <Typography
                  variant="body2"
                  sx={{
                    fontWeight: 500,
                    color: '#64748B',
                    fontSize: '0.875rem',
                  }}
                >
                  Trusted by:
                </Typography>
                {trustSignals.map((signal, index) => (
                  <Box
                    key={signal.text}
                    sx={{
                      display: 'flex',
                      alignItems: 'center',
                      gap: 1,
                    }}
                  >
                    {signal.icon}
                    <Typography
                      variant="caption"
                      sx={{
                        fontWeight: 500,
                        fontSize: '0.75rem',
                        color: '#475569',
                      }}
                    >
                      {signal.text}
                    </Typography>
                  </Box>
                ))}
              </Box>
            </motion.div>
          </Grid>

          {/* Right Content */}
          <Grid item xs={12} md={5}>
            <motion.div
              initial="hidden"
              animate="visible"
              variants={itemVariants}
              transition={{ delay: 0.2 }}
            >
              <Box
                sx={{
                  p: 4,
                  backgroundColor: '#F8FAFC',
                  borderRadius: 3,
                  border: '1px solid',
                  borderColor: 'divider',
                }}
              >
                <Typography
                  variant="h6"
                  color="primary"
                  gutterBottom
                  sx={{
                    fontWeight: 600,
                    fontSize: '1.125rem',
                    mb: 3,
                    color: '#0F172A',
                  }}
                >
                  Why Choose SmartProBono?
                </Typography>
                <Box
                  component="ul"
                  sx={{
                    m: 0,
                    pl: 0,
                    listStyle: 'none',
                  }}
                >
                  {[
                    '24/7 AI-powered legal assistance',
                    'Free document generation & templates',
                    'Expert legal guidance & resources',
                    'Secure, confidential & compliant',
                  ].map((item, index) => (
                    <Box
                      key={index}
                      component="li"
                      sx={{
                        display: 'flex',
                        alignItems: 'flex-start',
                        mb: 2.5,
                        '&:last-child': { mb: 0 },
                      }}
                    >
                      <CheckCircleIcon
                        sx={{
                          fontSize: 20,
                          color: theme.palette.success.main,
                          mr: 1.5,
                          mt: 0.25,
                          flexShrink: 0,
                        }}
                      />
                      <Typography
                        sx={{
                          fontSize: '0.9375rem',
                          fontWeight: 500,
                          color: '#334155',
                          lineHeight: 1.6,
                        }}
                      >
                        {item}
                      </Typography>
                    </Box>
                  ))}
                </Box>
              </Box>
            </motion.div>
          </Grid>
        </Grid>
      </Container>
    </Box>
  );
};

export default HeroSection;
