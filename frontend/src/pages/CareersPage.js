import React from 'react';
import { Container, Typography } from '@mui/material';
import { useTranslation } from 'react-i18next';
import PageLayout from '../components/PageLayout';

const CareersPage = () => {
  const { t } = useTranslation();
  
  return (
    <PageLayout
      title={t('careers.title')}
      description={t('careers.subtitle')}
    >
      <Container maxWidth="lg" sx={{ py: 4 }}>
        <Typography variant="h2" component="h1" gutterBottom sx={{ fontWeight: 'bold' }}>
          {t('careers.title')}
        </Typography>
        <Typography variant="body1" color="text.secondary">
          {t('careers.subtitle')}
        </Typography>
        <Typography variant="body1" color="text.secondary" sx={{ mt: 2 }}>
          {t('careers.description')}
        </Typography>
      </Container>
    </PageLayout>
  );
};

export default CareersPage;
