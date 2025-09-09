import React from 'react';
import { Container, Typography, Box } from '@mui/material';
import { useTranslation } from 'react-i18next';
import PageLayout from '../components/PageLayout';

const LegalTemplatesPage = () => {
  const { t } = useTranslation();
  
  return (
    <PageLayout
      title={t('templates.title')}
      description={t('templates.subtitle')}
    >
      <Container maxWidth="lg" sx={{ py: 4 }}>
        <Box sx={{ textAlign: 'center', mb: 4 }}>
          <Typography variant="h2" component="h1" gutterBottom sx={{ fontWeight: 'bold' }}>
            {t('templates.title')}
          </Typography>
          <Typography variant="body1" color="text.secondary">
            {t('templates.subtitle')}
          </Typography>
          <Typography variant="body1" color="text.secondary" sx={{ mt: 2 }}>
            {t('templates.description')}
          </Typography>
        </Box>
      </Container>
    </PageLayout>
  );
};

export default LegalTemplatesPage;
