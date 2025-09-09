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
import { useTranslation } from 'react-i18next';
import FacebookIcon from '@mui/icons-material/Facebook';
import TwitterIcon from '@mui/icons-material/Twitter';
import LinkedInIcon from '@mui/icons-material/LinkedIn';
import InstagramIcon from '@mui/icons-material/Instagram';
import YouTubeIcon from '@mui/icons-material/YouTube';
import EmailIcon from '@mui/icons-material/Email';
import PhoneIcon from '@mui/icons-material/Phone';
import LocationOnIcon from '@mui/icons-material/LocationOn';


const Footer = () => {
  const { t } = useTranslation();
  const theme = useTheme();

  const footerSections = [
    {
      title: t('footer.services'),
      links: [
        { text: t('footer.aiLegalAssistant'), path: '/legal-chat' },
        { text: t('footer.documentGeneration'), path: '/services/contracts' },
        { text: t('footer.immigrationHelp'), path: '/services/immigration' },
        { text: t('footer.virtualParalegal'), path: '/virtual-paralegal' },
        { text: t('footer.documentScanner'), path: '/scan-document' },
        { text: t('footer.proBonoServices'), path: '/services' },
      ],
    },
    {
      title: t('footer.resources'),
      links: [
        { text: t('footer.knowYourRights'), path: '/resources/rights' },
        { text: t('footer.legalTemplates'), path: '/resources/templates' },
        { text: t('footer.educationalContent'), path: '/resources' },
        { text: t('footer.legalGlossary'), path: '/resources/glossary' },
        { text: t('footer.faq'), path: '/faq' },
        { text: t('footer.blog'), path: '/blog' },
      ],
    },
    {
      title: t('footer.company'),
      links: [
        { text: t('footer.aboutUs'), path: '/about' },
        { text: t('footer.ourMission'), path: '/mission' },
        { text: t('footer.team'), path: '/team' },
        { text: t('footer.careers'), path: '/careers' },
        { text: t('footer.press'), path: '/press' },
        { text: t('footer.partners'), path: '/partners' },
      ],
    },
    {
      title: t('footer.support'),
      links: [
        { text: t('footer.helpCenter'), path: '/help' },
        { text: t('footer.contactUs'), path: '/contact' },
        { text: t('footer.liveChat'), path: '/chat' },
        { text: t('footer.statusPage'), path: '/status' },
        { text: t('footer.bugReport'), path: '/bug-report' },
        { text: t('footer.featureRequest'), path: '/feature-request' },
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



  return (
    <Box
      sx={{
          background: 'linear-gradient(135deg, #0F3D5E 0%, #1FB6A6 100%)',
          color: '#ffffff',
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
            radial-gradient(circle at 20% 80%, ${theme.palette.primary.light}20 0%, transparent 50%),
            radial-gradient(circle at 80% 20%, ${theme.palette.secondary.light}20 0%, transparent 50%)
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
                  color: '#ffffff',
                  textShadow: '0 2px 4px rgba(0,0,0,0.3)',
                }}
              >
                SmartProBono
              </Typography>
              <Chip 
                label="Beta" 
                size="small" 
                sx={{ 
                  backgroundColor: 'rgba(255, 255, 255, 0.2)', 
                  color: '#ffffff',
                  fontWeight: 'bold',
                  ml: 2
                }} 
              />
              <Typography
                variant="body1"
                sx={{
                  mb: 3,
                  lineHeight: 1.6,
                  opacity: 0.9,
                  maxWidth: '400px',
                }}
              >
                {t('company.description')}
              </Typography>



              {/* Contact Info */}
              <Stack spacing={2}>
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                  <EmailIcon sx={{ opacity: 0.7, fontSize: 20 }} />
                  <Typography variant="body2" sx={{ opacity: 0.9 }}>
                    bferrell@smartprobono.org
                  </Typography>
                </Box>
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                  <PhoneIcon sx={{ opacity: 0.7, fontSize: 20 }} />
                  <Typography variant="body2" sx={{ opacity: 0.9 }}>
                    (401) 217-9799
                  </Typography>
                </Box>
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                  <LocationOnIcon sx={{ opacity: 0.7, fontSize: 20 }} />
                  <Typography variant="body2" sx={{ opacity: 0.9 }}>
                    Providence, RI
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
                  color: '#ffffff',
                  fontSize: '1.1rem',
                  textShadow: '0 1px 2px rgba(0,0,0,0.3)',
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
                      color: 'rgba(255, 255, 255, 0.8)',
                      textDecoration: 'none',
                      fontSize: '0.9rem',
                      transition: 'all 0.2s ease',
                      '&:hover': {
                        color: '#ffffff',
                        transform: 'translateX(4px)',
                        textShadow: '0 1px 2px rgba(0,0,0,0.3)',
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

        <Divider sx={{ my: 4, borderColor: 'rgba(255, 255, 255, 0.2)' }} />

        {/* Bottom Section */}
        <Grid container spacing={3} alignItems="center">
          <Grid item xs={12} md={6}>
            <Typography
              variant="body2"
              sx={{
                opacity: 0.9,
                textAlign: { xs: 'center', md: 'left' },
                color: 'rgba(255, 255, 255, 0.8)',
                textShadow: '0 1px 2px rgba(0,0,0,0.3)',
              }}
            >
              © {new Date().getFullYear()} SmartProBono. {t('footer.allRightsReserved')} 
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
                      color: 'rgba(255, 255, 255, 0.8)',
                      border: '1px solid rgba(255, 255, 255, 0.3)',
                      '&:hover': {
                        color: '#ffffff',
                        borderColor: 'rgba(255, 255, 255, 0.6)',
                        backgroundColor: 'rgba(255, 255, 255, 0.1)',
                        transform: 'translateY(-2px)',
                        boxShadow: '0 4px 12px rgba(0,0,0,0.2)',
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
            borderTop: '1px solid rgba(255, 255, 255, 0.2)',
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
                color: 'rgba(255, 255, 255, 0.7)',
                textDecoration: 'none',
                fontSize: '0.875rem',
                '&:hover': { color: '#ffffff' },
              }}
            >
              {t('footer.privacyPolicy')}
            </Link>
            <Link
              component={RouterLink}
              to="/terms"
              sx={{
                color: 'rgba(255, 255, 255, 0.7)',
                textDecoration: 'none',
                fontSize: '0.875rem',
                '&:hover': { color: '#ffffff' },
              }}
            >
              {t('footer.termsOfService')}
            </Link>
            <Link
              component={RouterLink}
              to="/accessibility"
              sx={{
                color: 'rgba(255, 255, 255, 0.7)',
                textDecoration: 'none',
                fontSize: '0.875rem',
                '&:hover': { color: '#ffffff' },
              }}
            >
              {t('footer.accessibility')}
            </Link>
            <Link
              component={RouterLink}
              to="/sitemap"
              sx={{
                color: 'rgba(255, 255, 255, 0.7)',
                textDecoration: 'none',
                fontSize: '0.875rem',
                '&:hover': { color: '#ffffff' },
              }}
            >
              {t('footer.sitemap')}
            </Link>
          </Stack>
        </Box>
      </Container>
    </Box>
  );
};

export default Footer; 