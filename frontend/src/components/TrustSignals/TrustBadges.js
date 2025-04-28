import React from 'react';
import { Box, Paper, Typography, Grid, Tooltip } from '@mui/material';
import VerifiedIcon from '@mui/icons-material/Verified';
import SecurityIcon from '@mui/icons-material/Security';
import GavelIcon from '@mui/icons-material/Gavel';
import AccessibilityIcon from '@mui/icons-material/Accessibility';
import ShieldIcon from '@mui/icons-material/Shield';

const badges = [
  {
    id: 'security',
    icon: SecurityIcon,
    title: 'Bank-Level Security',
    description: '256-bit encryption and SOC 2 Type II certified',
    color: '#2E7D32'
  },
  {
    id: 'legal',
    icon: GavelIcon,
    title: 'Bar Certified',
    description: 'Compliant with state bar requirements',
    color: '#1565C0'
  },
  {
    id: 'accessibility',
    icon: AccessibilityIcon,
    title: 'WCAG 2.1 Compliant',
    description: 'Accessible to users of all abilities',
    color: '#4527A0'
  },
  {
    id: 'privacy',
    icon: ShieldIcon,
    title: 'Privacy Guaranteed',
    description: 'GDPR and CCPA compliant data handling',
    color: '#283593'
  },
  {
    id: 'verified',
    icon: VerifiedIcon,
    title: 'Verified Provider',
    description: 'Vetted and approved legal service provider',
    color: '#00695C'
  }
];

const TrustBadge = ({ icon: Icon, title, description, color }) => (
  <Tooltip title={description} arrow placement="top">
    <Paper
      elevation={2}
      sx={{
        p: 2,
        height: '100%',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        textAlign: 'center',
        transition: 'transform 0.2s, box-shadow 0.2s',
        '&:hover': {
          transform: 'translateY(-4px)',
          boxShadow: 4
        },
        cursor: 'pointer'
      }}
    >
      <Icon
        sx={{
          fontSize: 40,
          color: color,
          mb: 1
        }}
      />
      <Typography
        variant="subtitle1"
        component="h3"
        sx={{
          fontWeight: 'bold',
          color: 'text.primary'
        }}
      >
        {title}
      </Typography>
      <Typography
        variant="body2"
        color="text.secondary"
        sx={{
          mt: 0.5,
          display: { xs: 'none', sm: 'block' }
        }}
      >
        {description}
      </Typography>
    </Paper>
  </Tooltip>
);

const TrustBadges = () => {
  return (
    <Box
      component="section"
      sx={{
        py: 4,
        px: 2
      }}
      aria-label="Trust and Security Certifications"
    >
      <Typography
        variant="h5"
        component="h2"
        align="center"
        gutterBottom
        sx={{ mb: 4 }}
      >
        Trusted & Secure Legal Services
      </Typography>

      <Grid
        container
        spacing={3}
        justifyContent="center"
        sx={{
          maxWidth: 1200,
          mx: 'auto'
        }}
      >
        {badges.map((badge) => (
          <Grid item xs={6} sm={4} md={2.4} key={badge.id}>
            <TrustBadge {...badge} />
          </Grid>
        ))}
      </Grid>

      <Typography
        variant="body2"
        align="center"
        color="text.secondary"
        sx={{ mt: 4 }}
      >
        Our platform adheres to the highest standards of security, privacy, and professional compliance
      </Typography>
    </Box>
  );
};

export default TrustBadges; 