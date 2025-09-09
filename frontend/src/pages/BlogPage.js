import React from 'react';
import { Container, Typography, Box } from '@mui/material';
import { useTranslation } from 'react-i18next';
import PageLayout from '../components/PageLayout';

const BlogPage = () => {
  const { t } = useTranslation();
  
  return (
    <PageLayout
      title={t('blog.title')}
      description={t('blog.subtitle')}
    >
      <Container maxWidth="lg" sx={{ py: 4 }}>
        <Box sx={{ textAlign: 'center', mb: 4 }}>
          <Typography variant="h2" component="h1" gutterBottom sx={{ fontWeight: 'bold' }}>
            {t('blog.title')}
          </Typography>
          <Typography variant="body1" color="text.secondary">
            {t('blog.subtitle')}
          </Typography>
          <Typography variant="body1" color="text.secondary" sx={{ mt: 2 }}>
            {t('blog.description')}
          </Typography>
        </Box>
      </Container>
    </PageLayout>
  );
};

export default BlogPage;
