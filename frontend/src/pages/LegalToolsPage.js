import React from 'react';
import {
  Box,
  Container,
  Typography,
  Grid,
  Card,
  CardActionArea,
  Button,
  Chip,
  Paper
} from '@mui/material';
import {
  DocumentScanner as ScannerIcon,
  Chat as ChatIcon,
  Security as SecurityIcon,
  Gavel as GavelIcon,
  Description as PDFIcon,
  Assessment as AssessmentIcon
} from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import { useTranslation } from 'react-i18next';

const LegalToolsPage = () => {
  const { t } = useTranslation();
  const navigate = useNavigate();

  const tools = [
    {
      title: t('legalTools.tools.documentScanner.title'),
      description: t('legalTools.tools.documentScanner.description'),
      icon: <ScannerIcon sx={{ fontSize: 40, color: 'primary.main' }} />,
      path: '/scan-document',
      badge: 'AI',
      color: 'primary'
    },
    {
      title: t('legalTools.tools.pdfGenerator.title'),
      description: t('legalTools.tools.pdfGenerator.description'),
      icon: <PDFIcon sx={{ fontSize: 40, color: 'success.main' }} />,
      path: '/generate-document',
      badge: 'New',
      color: 'success'
    },
    {
      title: t('legalTools.tools.aiLegalChat.title'),
      description: t('legalTools.tools.aiLegalChat.description'),
      icon: <ChatIcon sx={{ fontSize: 40, color: 'info.main' }} />,
      path: '/legal-chat',
      badge: 'AI',
      color: 'info'
    },
    {
      title: t('legalTools.tools.safetyCheck.title'),
      description: t('legalTools.tools.safetyCheck.description'),
      icon: <SecurityIcon sx={{ fontSize: 40, color: 'warning.main' }} />,
      path: '/safety-check',
      badge: 'New',
      color: 'warning'
    },
    {
      title: 'Legal Assessment',
      description: 'Comprehensive legal needs assessment and recommendations',
      icon: <AssessmentIcon sx={{ fontSize: 40, color: 'secondary.main' }} />,
      path: '/legal-assessment',
      badge: 'Coming Soon',
      color: 'default'
    },
    {
      title: 'Contract Review',
      description: 'AI-powered contract analysis and risk assessment',
      icon: <GavelIcon sx={{ fontSize: 40, color: 'error.main' }} />,
      path: '/contract-review',
      badge: 'Coming Soon',
      color: 'default'
    }
  ];

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Paper sx={{ p: 4, mb: 4, textAlign: 'center' }}>
        <Typography variant="h3" component="h1" gutterBottom>
          {t('legalTools.title')}
        </Typography>
        <Typography variant="h6" color="text.secondary" paragraph>
          {t('legalTools.subtitle')}
        </Typography>
      </Paper>

      <Grid container spacing={3}>
        {tools.map((tool, index) => (
          <Grid item xs={12} sm={6} md={4} key={index}>
            <Card 
              sx={{ 
                height: '100%',
                display: 'flex',
                flexDirection: 'column',
                transition: 'transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out',
                '&:hover': {
                  transform: 'translateY(-4px)',
                  boxShadow: 4
                }
              }}
            >
              <CardActionArea 
                onClick={() => navigate(tool.path)}
                sx={{ 
                  flex: 1,
                  display: 'flex',
                  flexDirection: 'column',
                  alignItems: 'center',
                  p: 3,
                  textAlign: 'center'
                }}
                disabled={tool.badge === 'Coming Soon'}
              >
                <Box sx={{ mb: 2 }}>
                  {tool.icon}
                </Box>
                
                <Typography variant="h6" component="h2" gutterBottom>
                  {tool.title}
                </Typography>
                
                <Typography variant="body2" color="text.secondary" paragraph>
                  {tool.description}
                </Typography>

                <Chip 
                  label={tool.badge}
                  color={tool.color}
                  size="small"
                  sx={{ mt: 'auto' }}
                />
              </CardActionArea>
            </Card>
          </Grid>
        ))}
      </Grid>

      <Box sx={{ mt: 6, textAlign: 'center' }}>
        <Typography variant="h5" gutterBottom>
          Need Help Getting Started?
        </Typography>
        <Typography variant="body1" color="text.secondary" paragraph>
          Our tools are designed to be user-friendly, but we're here to help if you need assistance.
        </Typography>
        <Button 
          variant="contained" 
          size="large"
          onClick={() => navigate('/legal-chat')}
          startIcon={<ChatIcon />}
        >
          Get Help from AI Assistant
        </Button>
      </Box>
    </Container>
  );
};

export default LegalToolsPage;