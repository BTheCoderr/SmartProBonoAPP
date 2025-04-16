import React from 'react';
import {
  Card,
  CardContent,
  CardActions,
  Typography,
  Box,
  Chip,
  Button,
  Tooltip,
  Avatar,
  Divider,
} from '@mui/material';
import { useTranslation } from 'react-i18next';
import { useNavigate } from 'react-router-dom';
import LockIcon from '@mui/icons-material/Lock';
import AccessTimeIcon from '@mui/icons-material/AccessTime';
import LocalOfferIcon from '@mui/icons-material/LocalOffer';
import VerifiedUserIcon from '@mui/icons-material/VerifiedUser';
import NewReleasesIcon from '@mui/icons-material/NewReleases';

// Import Material-UI icons dynamically
import * as MuiIcons from '@mui/icons-material';
import PropTypes from 'prop-types';

const DocumentTemplateCard = ({ template, userAccessLevel = 'free' }) => {
  const { t } = useTranslation();
  const navigate = useNavigate();

  // Determine if the user has access to this template
  const hasAccess = () => {
    const accessLevels = {
      free: 0,
      registered: 1,
      premium: 2,
    };

    return accessLevels[userAccessLevel] >= accessLevels[template.accessLevel];
  };

  // Dynamically get icon component
  const IconComponent =
    template.icon && MuiIcons[template.icon] ? MuiIcons[template.icon] : MuiIcons.Description;

  // Get access level display elements
  const getAccessLevelDisplay = () => {
    switch (template.accessLevel) {
      case 'free':
        return {
          label: t('Free'),
          color: 'success',
          icon: <VerifiedUserIcon fontSize="small" />,
        };
      case 'registered':
        return {
          label: t('Account Required'),
          color: 'primary',
          icon: <LockIcon fontSize="small" />,
        };
      case 'premium':
        return {
          label: t('Premium'),
          color: 'secondary',
          icon: <NewReleasesIcon fontSize="small" />,
        };
      default:
        return {
          label: t('Free'),
          color: 'success',
          icon: <VerifiedUserIcon fontSize="small" />,
        };
    }
  };

  const accessDisplay = getAccessLevelDisplay();

  const handleTemplateSelect = () => {
    if (hasAccess()) {
      navigate(`/document-templates/form/${template.id}`);
    } else {
      if (template.accessLevel === 'registered') {
        // Instead of forcing login, offer a limited preview or explain benefits
        // Show a dialog or provide a preview option
        const useAnyway = window.confirm(
          `This template typically requires a free account for tracking purposes. \n\nWould you like to use it anyway? (Click OK to continue, or Cancel to create an account for save & tracking features)`
        );

        if (useAnyway) {
          // Allow them to use it anyway
          navigate(`/document-templates/form/${template.id}?demo=true`);
        } else {
          // They chose to register
          navigate(
            '/login?redirect=' + encodeURIComponent(`/document-templates/form/${template.id}`)
          );
        }
      } else if (template.accessLevel === 'premium') {
        // For premium content, show subscription options
        navigate('/subscription?template=' + template.id);
      }
    }
  };

  return (
    <Card
      sx={{
        height: '100%',
        display: 'flex',
        flexDirection: 'column',
        transition: 'transform 0.2s, box-shadow 0.2s',
        '&:hover': {
          transform: 'translateY(-4px)',
          boxShadow: 3,
        },
        position: 'relative',
        ...(template.featured && {
          border: '1px solid',
          borderColor: 'primary.main',
        }),
      }}
    >
      {template.featured && (
        <Box
          sx={{
            position: 'absolute',
            top: 0,
            right: 0,
            bgcolor: 'primary.main',
            color: 'white',
            px: 1,
            py: 0.5,
            borderBottomLeftRadius: 4,
          }}
        >
          <Typography variant="caption" fontWeight="bold">
            {t('Featured')}
          </Typography>
        </Box>
      )}

      {template.isNew && (
        <Box
          sx={{
            position: 'absolute',
            top: template.featured ? 24 : 0,
            right: 0,
            bgcolor: 'secondary.main',
            color: 'white',
            px: 1,
            py: 0.5,
            borderBottomLeftRadius: 4,
            display: 'flex',
            alignItems: 'center',
          }}
        >
          <NewReleasesIcon fontSize="small" sx={{ mr: 0.5 }} />
          <Typography variant="caption" fontWeight="bold">
            {t('NEW')}
          </Typography>
        </Box>
      )}

      <CardContent sx={{ pt: 3, pb: 1, flexGrow: 1 }}>
        <Box display="flex" alignItems="center" mb={2}>
          <Avatar
            sx={{
              bgcolor: template.isNew
                ? 'secondary.main'
                : template.featured
                  ? 'primary.main'
                  : 'grey.200',
              color: template.isNew || template.featured ? 'white' : 'text.primary',
              mr: 1.5,
            }}
          >
            <IconComponent />
          </Avatar>
          <Typography variant="h6" component="h3" noWrap>
            {template.name}
          </Typography>
        </Box>

        <Chip
          size="small"
          icon={accessDisplay.icon}
          label={accessDisplay.label}
          color={accessDisplay.color}
          sx={{ mb: 2 }}
        />

        <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
          {template.description}
        </Typography>

        <Box display="flex" flexWrap="wrap" gap={0.5} mb={2}>
          {template.tags &&
            template.tags.map(tag => (
              <Chip
                key={tag}
                label={tag}
                size="small"
                variant="outlined"
                icon={<LocalOfferIcon fontSize="small" />}
                sx={{ fontSize: '0.7rem' }}
              />
            ))}
        </Box>
      </CardContent>

      <Divider />

      <CardActions sx={{ display: 'flex', justifyContent: 'space-between', px: 2, py: 1.5 }}>
        <Tooltip title={t('Estimated completion time')}>
          <Box display="flex" alignItems="center">
            <AccessTimeIcon fontSize="small" color="action" sx={{ mr: 0.5 }} />
            <Typography variant="caption" color="text.secondary">
              {template.estimatedCompletionTime}
            </Typography>
          </Box>
        </Tooltip>

        <Button
          variant={hasAccess() ? 'contained' : 'outlined'}
          size="small"
          onClick={handleTemplateSelect}
          startIcon={hasAccess() ? null : <LockIcon fontSize="small" />}
          color={template.isNew ? 'secondary' : 'primary'}
        >
          {hasAccess() ? t('Use Template') : t('Unlock')}
        </Button>
      </CardActions>
    </Card>
  );
};


// Define PropTypes
DocumentTemplateCard.propTypes = {
  /** TODO: Add description */
  template: PropTypes.any,
  /** TODO: Add description */
  userAccessLevel: PropTypes.any,
};

export default DocumentTemplateCard;
