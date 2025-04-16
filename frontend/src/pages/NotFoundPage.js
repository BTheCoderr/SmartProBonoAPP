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
        minHeight: 'calc(100vh - 64px)', // Adjust based on your navbar height
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
        <ErrorOutlineIcon sx={{ fontSize: 64, color: 'error.main', mb: 2 }} />
        <Typography variant="h4" gutterBottom>
          {t('errors.notFound.title')}
        </Typography>
        <Typography color="text.secondary" paragraph>
          {t('errors.notFound.message')}
        </Typography>
        <Box sx={{ mt: 4 }}>
          <Button variant="contained" onClick={() => navigate('/')} sx={{ mr: 2 }}>
            {t('common.backToHome')}
          </Button>
          <Button variant="outlined" onClick={() => navigate(-1)}>
            {t('common.goBack')}
          </Button>
        </Box>
      </Paper>
    </Box>
  );
};

export default NotFoundPage;
