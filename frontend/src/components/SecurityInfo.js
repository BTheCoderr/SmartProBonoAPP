import React from 'react';
import {
  Box,
  Paper,
  Typography,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Divider,
  Alert,
} from '@mui/material';
import SecurityIcon from '@mui/icons-material/Security';
import LockIcon from '@mui/icons-material/Lock';
import VerifiedUserIcon from '@mui/icons-material/VerifiedUser';
import GavelIcon from '@mui/icons-material/Gavel';
import { useTranslation } from 'react-i18next';

const SecurityInfo = () => {
  const { t } = useTranslation();

  const securityFeatures = [
    {
      icon: <LockIcon />,
      title: t('security.features.encryption.title'),
      description: t('security.features.encryption.description'),
    },
    {
      icon: <SecurityIcon />,
      title: t('security.features.audits.title'),
      description: t('security.features.audits.description'),
    },
    {
      icon: <VerifiedUserIcon />,
      title: t('security.features.dataProtection.title'),
      description: t('security.features.dataProtection.description'),
    },
    {
      icon: <GavelIcon />,
      title: t('security.features.compliance.title'),
      description: t('security.features.compliance.description'),
    },
  ];

  return (
    <Box sx={{ maxWidth: 800, mx: 'auto', p: 3 }}>
      <Paper elevation={3} sx={{ p: 4 }}>
        <Typography variant="h4" gutterBottom>
          {t('security.title')}
        </Typography>

        <Alert severity="info" sx={{ mb: 4 }}>
          {t('security.subtitle')}
        </Alert>

        <List>
          {securityFeatures.map((feature, index) => (
            <React.Fragment key={feature.title}>
              <ListItem alignItems="flex-start">
                <ListItemIcon>{feature.icon}</ListItemIcon>
                <ListItemText
                  primary={feature.title}
                  secondary={feature.description}
                  primaryTypographyProps={{
                    variant: 'h6',
                    gutterBottom: true,
                  }}
                  secondaryTypographyProps={{
                    variant: 'body1',
                  }}
                />
              </ListItem>
              {index < securityFeatures.length - 1 && <Divider variant="inset" component="li" />}
            </React.Fragment>
          ))}
        </List>

        <Box sx={{ mt: 4 }}>
          <Typography variant="h5" gutterBottom>
            {t('security.dataProtection.title')}
          </Typography>
          <List>
            <ListItem>
              <ListItemText
                primary={t('security.dataProtection.encryption.title')}
                secondary={t('security.dataProtection.encryption.description')}
              />
            </ListItem>
            <ListItem>
              <ListItemText
                primary={t('security.dataProtection.transfer.title')}
                secondary={t('security.dataProtection.transfer.description')}
              />
            </ListItem>
            <ListItem>
              <ListItemText
                primary={t('security.dataProtection.access.title')}
                secondary={t('security.dataProtection.access.description')}
              />
            </ListItem>
            <ListItem>
              <ListItemText
                primary={t('security.dataProtection.backups.title')}
                secondary={t('security.dataProtection.backups.description')}
              />
            </ListItem>
          </List>
        </Box>

        <Box sx={{ mt: 4 }}>
          <Typography variant="h5" gutterBottom>
            {t('security.certifications.title')}
          </Typography>
          <List>
            <ListItem>
              <ListItemText
                primary={t('security.certifications.gdpr.title')}
                secondary={t('security.certifications.gdpr.description')}
              />
            </ListItem>
            <ListItem>
              <ListItemText
                primary={t('security.certifications.ccpa.title')}
                secondary={t('security.certifications.ccpa.description')}
              />
            </ListItem>
            <ListItem>
              <ListItemText
                primary={t('security.certifications.hipaa.title')}
                secondary={t('security.certifications.hipaa.description')}
              />
            </ListItem>
          </List>
        </Box>

        <Alert severity="success" sx={{ mt: 4 }}>
          {t('security.updateMessage')}
        </Alert>
      </Paper>
    </Box>
  );
};

export default SecurityInfo;
