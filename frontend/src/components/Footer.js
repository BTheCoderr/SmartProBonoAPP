import React from 'react';
import {
  Box,
  Container,
  Grid,
  Typography,
  Link,
  IconButton,
  useTheme,
  Divider,
  Stack,
  Chip,
  Tooltip,
} from '@mui/material';
import { Link as RouterLink } from 'react-router-dom';
import FacebookIcon from '@mui/icons-material/Facebook';
import TwitterIcon from '@mui/icons-material/Twitter';
import LinkedInIcon from '@mui/icons-material/LinkedIn';
import InstagramIcon from '@mui/icons-material/Instagram';
import YouTubeIcon from '@mui/icons-material/YouTube';
import EmailIcon from '@mui/icons-material/Email';
import PhoneIcon from '@mui/icons-material/Phone';
import LocationOnIcon from '@mui/icons-material/LocationOn';
import SecurityIcon from '@mui/icons-material/Security';
import VerifiedUserIcon from '@mui/icons-material/VerifiedUser';
import SupportIcon from '@mui/icons-material/Support';

const Footer = () => {
  const theme = useTheme();

  const footerSections = [
    {
      title: 'Services',
      links: [
        { text: 'AI Legal Assistant', path: '/legal-chat' },
        { text: 'Document Generation', path: '/services/contracts' },
        { text: 'Immigration Help', path: '/services/immigration' },
        { text: 'Virtual Paralegal', path: '/virtual-paralegal' },
        { text: 'Document Scanner', path: '/scan-document' },
        { text: 'Pro Bono Services', path: '/services' },
      ],
    },
    {
      title: 'Resources',
      links: [
        { text: 'Know Your Rights', path: '/resources/rights' },
        { text: 'Legal Templates', path: '/resources/templates' },
        { text: 'Educational Content', path: '/resources' },
        { text: 'Legal Glossary', path: '/resources/glossary' },
        { text: 'FAQ', path: '/faq' },
        { text: 'Blog', path: '/blog' },
      ],
    },
    {
      title: 'Company',
      links: [
        { text: 'About Us', path: '/about' },
        { text: 'Our Mission', path: '/mission' },
        { text: 'Team', path: '/team' },
        { text: 'Careers', path: '/careers' },
        { text: 'Press', path: '/press' },
        { text: 'Partners', path: '/partners' },
      ],
    },
    {
      title: 'Support',
      links: [
        { text: 'Help Center', path: '/help' },
        { text: 'Contact Us', path: '/contact' },
        { text: 'Live Chat', path: '/chat' },
        { text: 'Status Page', path: '/status' },
        { text: 'Bug Report', path: '/bug-report' },
        { text: 'Feature Request', path: '/feature-request' },
      ],
    },
  ];

  const socialLinks = [
    { icon: <FacebookIcon />, href: 'https://facebook.com/smartprobono', label: 'Facebook' },
    { icon: <TwitterIcon />, href: 'https://twitter.com/smartprobono', label: 'Twitter' },
    { icon: <LinkedInIcon />, href: 'https://linkedin.com/company/smartprobono', label: 'LinkedIn' },
    { icon: <InstagramIcon />, href: 'https://instagram.com/smartprobono', label: 'Instagram' },
    { icon: <YouTubeIcon />, href: 'https://youtube.com/smartprobono', label: 'YouTube' },
  ];

  const trustSignals = [
    { icon: <SecurityIcon />, text: 'Bank-Level Security', color: 'success' },
    { icon: <VerifiedUserIcon />, text: 'Licensed Attorneys', color: 'primary' },
    { icon: <SupportIcon />, text: '24/7 Support', color: 'info' },
  ];

  return (
    <Box
      sx={{
          background: 'linear-gradient(135deg, #f1f5f9 0%, #cbd5e1 100%)',
          color: '#1e293b',
          pt: { xs: 6, md: 8 },
          pb: { xs: 4, md: 6 },
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
          opacity: 0.05,
          background: `
            radial-gradient(circle at 20% 80%, rgba(255,255,255,0.3) 0%, transparent 50%),
            radial-gradient(circle at 80% 20%, rgba(255,255,255,0.3) 0%, transparent 50%)
          `,
        }}
      />

      <Container maxWidth="xl" sx={{ position: 'relative', zIndex: 1 }}>
        {/* Main Footer Content */}
        <Grid container spacing={4}>
          {/* Company Info */}
          <Grid item xs={12} md={4}>
            <Box sx={{ mb: 4 }}>
              <Typography
                variant="h4"
                sx={{
                  fontWeight: 800,
                  mb: 2,
                  background: 'linear-gradient(45deg, #ffffff 30%, #e2e8f0 90%)',
                  WebkitBackgroundClip: 'text',
                  WebkitTextFillColor: 'transparent',
                  backgroundClip: 'text',
                }}
              >
                SmartProBono
              </Typography>
              <Typography
                variant="body1"
                sx={{
                  mb: 3,
                  lineHeight: 1.6,
                  opacity: 0.9,
                  maxWidth: '400px',
                }}
              >
                Making legal help accessible, affordable, and easy to understand for everyone. 
                Our AI-powered platform connects you with the legal assistance you need.
              </Typography>

              {/* Trust Signals */}
              <Stack direction="row" spacing={2} sx={{ mb: 3 }}>
                {trustSignals.map((signal, index) => (
                  <Chip
                    key={index}
                    icon={signal.icon}
                    label={signal.text}
                    color={signal.color}
                    size="small"
                    sx={{
                      backgroundColor: 'rgba(255, 255, 255, 0.1)',
                      color: 'white',
                      border: '1px solid rgba(255, 255, 255, 0.2)',
                      '& .MuiChip-icon': {
                        color: theme.palette[signal.color].light,
                      },
                    }}
                  />
                ))}
              </Stack>

              {/* Contact Info */}
              <Stack spacing={2}>
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                  <EmailIcon sx={{ opacity: 0.7, fontSize: 20 }} />
                  <Typography variant="body2" sx={{ opacity: 0.9 }}>
                    support@smartprobono.org
                  </Typography>
                </Box>
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                  <PhoneIcon sx={{ opacity: 0.7, fontSize: 20 }} />
                  <Typography variant="body2" sx={{ opacity: 0.9 }}>
                    1-800-LEGAL-AID
                  </Typography>
                </Box>
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                  <LocationOnIcon sx={{ opacity: 0.7, fontSize: 20 }} />
                  <Typography variant="body2" sx={{ opacity: 0.9 }}>
                    New York, NY
                  </Typography>
                </Box>
              </Stack>
            </Box>
          </Grid>

          {/* Footer Links */}
          {footerSections.map((section) => (
            <Grid item xs={12} sm={6} md={2} key={section.title}>
              <Typography
                variant="h6"
                sx={{
                  fontWeight: 700,
                  mb: 3,
                  color: '#1e293b',
                  fontSize: '1.1rem',
                }}
              >
                {section.title}
              </Typography>
              <Stack spacing={2}>
                {section.links.map((link) => (
                  <Link
                    key={link.text}
                    component={RouterLink}
                    to={link.path}
                    sx={{
                      color: 'rgba(30, 41, 59, 0.8)',
                      textDecoration: 'none',
                      fontSize: '0.9rem',
                      transition: 'all 0.2s ease',
                      '&:hover': {
                        color: '#1e293b',
                        transform: 'translateX(4px)',
                      },
                    }}
                  >
                    {link.text}
                  </Link>
                ))}
              </Stack>
            </Grid>
          ))}
        </Grid>

        <Divider sx={{ my: 4, borderColor: 'rgba(30, 41, 59, 0.2)' }} />

        {/* Bottom Section */}
        <Grid container spacing={3} alignItems="center">
          <Grid item xs={12} md={6}>
            <Typography
              variant="body2"
              sx={{
                opacity: 0.8,
                textAlign: { xs: 'center', md: 'left' },
                color: '#475569',
              }}
            >
              © {new Date().getFullYear()} SmartProBono. All rights reserved. 
              Making legal help accessible to everyone.
          </Typography>
          </Grid>

          {/* Social Links */}
          <Grid item xs={12} md={6}>
            <Box
              sx={{
                display: 'flex',
                justifyContent: { xs: 'center', md: 'flex-end' },
                gap: 1,
              }}
            >
              {socialLinks.map((social) => (
                <Tooltip key={social.label} title={social.label}>
                  <IconButton
                    component="a"
                    href={social.href}
                    target="_blank"
                    rel="noopener noreferrer"
                    sx={{
                      color: 'rgba(30, 41, 59, 0.7)',
                      border: '1px solid rgba(30, 41, 59, 0.2)',
                      '&:hover': {
                        color: '#1e293b',
                        borderColor: 'rgba(30, 41, 59, 0.4)',
                        backgroundColor: 'rgba(30, 41, 59, 0.1)',
                        transform: 'translateY(-2px)',
                      },
                      transition: 'all 0.2s ease',
                    }}
                  >
                    {social.icon}
                  </IconButton>
                </Tooltip>
              ))}
            </Box>
          </Grid>
        </Grid>

        {/* Additional Links */}
        <Box
          sx={{
            mt: 4,
            pt: 3,
            borderTop: '1px solid rgba(30, 41, 59, 0.2)',
            textAlign: 'center',
          }}
        >
          <Stack
            direction={{ xs: 'column', sm: 'row' }}
            spacing={{ xs: 2, sm: 4 }}
            justifyContent="center"
            alignItems="center"
          >
            <Link
              component={RouterLink}
              to="/privacy"
              sx={{
                color: 'rgba(30, 41, 59, 0.7)',
                textDecoration: 'none',
                fontSize: '0.875rem',
                '&:hover': { color: '#1e293b' },
              }}
            >
              Privacy Policy
            </Link>
            <Link
              component={RouterLink}
              to="/terms"
              sx={{
                color: 'rgba(30, 41, 59, 0.7)',
                textDecoration: 'none',
                fontSize: '0.875rem',
                '&:hover': { color: '#1e293b' },
              }}
            >
              Terms of Service
            </Link>
            <Link
              component={RouterLink}
              to="/accessibility"
              sx={{
                color: 'rgba(30, 41, 59, 0.7)',
                textDecoration: 'none',
                fontSize: '0.875rem',
                '&:hover': { color: '#1e293b' },
              }}
            >
              Accessibility
            </Link>
            <Link
              component={RouterLink}
              to="/sitemap"
              sx={{
                color: 'rgba(30, 41, 59, 0.7)',
                textDecoration: 'none',
                fontSize: '0.875rem',
                '&:hover': { color: '#1e293b' },
              }}
            >
              Sitemap
            </Link>
          </Stack>
        </Box>
      </Container>
    </Box>
  );
};

export default Footer; 