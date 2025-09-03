import React from 'react';
import { Navigate, useLocation } from 'react-router-dom';
import { Box, Paper, Typography, Button } from '@mui/material';
import LockIcon from '@mui/icons-material/Lock';
import { useTranslation } from 'react-i18next';

const PremiumRouteGuard = ({ children, isPremium = false }) => {
  const { t } = useTranslation();
  const location = useLocation();

  if (!isPremium) {
    return (
      <Box
        sx={{
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
          minHeight: 'calc(100vh - 64px)',
          p: 2,
        }}
      >
        <Paper
          elevation={3}
          sx={{
            p: 4,
            textAlign: 'center',
            maxWidth: 400,
          }}
        >
          <LockIcon sx={{ fontSize: 64, color: 'primary.main', mb: 2 }} />
          <Typography variant="h5" gutterBottom>
            {t('premium.accessDenied.title')}
          </Typography>
          <Typography color="text.secondary" paragraph>
            {t('premium.accessDenied.message')}
          </Typography>
          <Box sx={{ mt: 3 }}>
            <Button
              variant="contained"
              color="primary"
              href="/subscription"
              sx={{ mr: 2 }}
            >
              {t('premium.upgrade')}
            </Button>
            <Button
              variant="outlined"
              onClick={() => window.history.back()}
            >
              {t('common.goBack')}
            </Button>
            <Button
              variant="text"
              onClick={() => {
                // Use Navigate to redirect to login with current location as state
                return <Navigate to="/login" state={{ from: location }} replace />;
              }}
              sx={{ ml: 1 }}
            >
              Login
            </Button>
          </Box>
        </Paper>
      </Box>
    );
  }

  return children;
};

export default PremiumRouteGuard; 