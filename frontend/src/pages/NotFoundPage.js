import React from 'react';
import { Box, Typography, Button, Paper } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import ErrorOutlineIcon from '@mui/icons-material/ErrorOutline';

const NotFoundPage = () => {
  const navigate = useNavigate();
  const { t } = useTranslation();

  return (
    <Box
      sx={{
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        minHeight: '60vh',
        px: 2
      }}
    >
      <Paper
        elevation={3}
        sx={{
          p: { xs: 2, sm: 4 },
          width: '100%',
          textAlign: 'center',
          maxWidth: 400,
        }}
      >
        <ErrorOutlineIcon sx={{ fontSize: 64, color: 'error.main', mb: 2 }} />
        <Typography variant="h4" gutterBottom>
          {t('errors.notFound.title', { defaultValue: 'Page not found' })}
        </Typography>
        <Typography color="text.secondary" paragraph>
          {t('errors.notFound.message', { defaultValue: 'This page is not available in the legacy prototype.' })}
        </Typography>
        <Box sx={{ mt: 4, display: 'flex', flexWrap: 'wrap', justifyContent: 'center', gap: 1 }}>
          <Button
            variant="contained"
            onClick={() => navigate('/')}
            sx={{ maxWidth: '100%' }}
          >
            {t('common.backToHome')}
          </Button>
          <Button
            variant="outlined"
            onClick={() => navigate(-1)}
          >
            {t('common.goBack')}
          </Button>
        </Box>
      </Paper>
    </Box>
  );
};

export default NotFoundPage; 