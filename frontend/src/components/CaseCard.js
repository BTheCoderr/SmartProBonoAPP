import React from 'react';
import PropTypes from 'prop-types';
import {
  Card,
  CardContent,
  CardActions,
  Typography,
  Chip,
  Box,
  Button,
  IconButton,
  Tooltip,
  LinearProgress,
  useTheme,
  useMediaQuery,
  Divider,
} from '@mui/material';
import { useNavigate } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { format, formatDistance } from 'date-fns';
// Icons
import DescriptionIcon from '@mui/icons-material/Description';
import AccessTimeIcon from '@mui/icons-material/AccessTime';
import PersonIcon from '@mui/icons-material/Person';
import PriorityHighIcon from '@mui/icons-material/PriorityHigh';
import ArrowForwardIcon from '@mui/icons-material/ArrowForward';
import HomeIcon from '@mui/icons-material/Home';
import WorkIcon from '@mui/icons-material/Work';
import FamilyRestroomIcon from '@mui/icons-material/FamilyRestroom';
import FlightIcon from '@mui/icons-material/Flight';
import MoneyOffIcon from '@mui/icons-material/MoneyOff';
import GavelIcon from '@mui/icons-material/Gavel';
import HelpIcon from '@mui/icons-material/Help';
import WarningIcon from '@mui/icons-material/Warning';
import {
  getStatusLabel,
  getCaseTypeLabel,
  getPriorityLabel,
  CASE_STATUS,
  CASE_TYPES,
  PRIORITY_LEVELS,
} from '../data/casesData';
// Helper function to get the appropriate icon for a case type
const getCaseTypeIcon = type => {
  switch (type) {
    case CASE_TYPES.HOUSING:
      return <HomeIcon />;
    case CASE_TYPES.EMPLOYMENT:
      return <WorkIcon />;
    case CASE_TYPES.FAMILY:
      return <FamilyRestroomIcon />;
    case CASE_TYPES.IMMIGRATION:
      return <FlightIcon />;
    case CASE_TYPES.DEBT:
      return <MoneyOffIcon />;
    case CASE_TYPES.CIVIL_RIGHTS:
      return <GavelIcon />;
    case CASE_TYPES.CRIMINAL:
      return <GavelIcon />;
    case CASE_TYPES.EMERGENCY:
      return <WarningIcon color="error" />;
    default:
      return <HelpIcon />;
  }
};
// Helper function to get colors for status and priority
const getStatusColor = status => {
  switch (status) {
    case CASE_STATUS.NEW:
      return 'info';
    case CASE_STATUS.IN_PROGRESS:
      return 'primary';
    case CASE_STATUS.PENDING_CLIENT:
    case CASE_STATUS.PENDING_COURT:
      return 'warning';
    case CASE_STATUS.RESOLVED:
      return 'success';
    case CASE_STATUS.CLOSED:
      return 'default';
    default:
      return 'default';
  }
};
const getPriorityColor = priority => {
  switch (priority) {
    case PRIORITY_LEVELS.LOW:
      return 'success';
    case PRIORITY_LEVELS.MEDIUM:
      return 'info';
    case PRIORITY_LEVELS.HIGH:
      return 'warning';
    case PRIORITY_LEVELS.URGENT:
      return 'error';
    default:
      return 'default';
  }
};
const CaseCard = ({ caseData, variant = 'default' }) => {
  const { t } = useTranslation();
  const navigate = useNavigate();
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('sm'));
  const isTablet = useMediaQuery(theme.breakpoints.down('md'));
  
  // Format dates
  const createdDate = new Date(caseData.created);
  const updatedDate = new Date(caseData.updated);
  const timeAgo = formatDistance(updatedDate, new Date(), { addSuffix: true });
  
  // Progress indicator (simplified version)
  const getProgressValue = status => {
    switch (status) {
      case CASE_STATUS.NEW:
        return 10;
      case CASE_STATUS.IN_PROGRESS:
        return 40;
      case CASE_STATUS.PENDING_CLIENT:
      case CASE_STATUS.PENDING_COURT:
        return 60;
      case CASE_STATUS.RESOLVED:
        return 90;
      case CASE_STATUS.CLOSED:
        return 100;
      default:
        return 0;
    }
  };
  
  const handleViewDetails = () => {
    navigate(`/cases/${caseData.id}`);
  };
  
  // Compact variant for dashboard
  if (variant === 'compact') {
    return (
      <Card
        sx={{
          mb: 2,
          borderLeft: 4,
          borderColor: theme.palette[getPriorityColor(caseData.priority)].main,
          transition: 'transform 0.2s',
          '&:hover': {
            transform: 'translateY(-4px)',
            boxShadow: 3,
          },
          width: '100%', // Make the card responsive to the container width
          borderRadius: { xs: 1, sm: 2 }, // Smaller border radius on mobile
        }}
      >
        <CardContent sx={{ p: { xs: 1.5, sm: 2 } }}> {/* Adjust padding for mobile */}
          <Box
            sx={{
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: { xs: 'flex-start', sm: 'center' }, // Stack on mobile for better readability
              flexDirection: { xs: 'column', sm: 'row' },
              mb: 1,
            }}
          >
            <Box sx={{ 
              display: 'flex', 
              alignItems: 'center',
              mb: { xs: 1, sm: 0 }, // Add margin when stacked vertically on mobile
              width: { xs: '100%', sm: 'auto' }
            }}>
              <Tooltip title={getCaseTypeLabel(caseData.type)}>
                <Box
                  sx={{
                    mr: 1.5,
                    color: theme.palette.text.secondary,
                    fontSize: { xs: '1.2rem', sm: '1.5rem' }, // Adjust icon size for mobile
                    display: 'flex',
                    alignItems: 'center',
                  }}
                >
                  {getCaseTypeIcon(caseData.type)}
                </Box>
              </Tooltip>
              <Typography 
                variant="h6" 
                component="h3" 
                noWrap 
                sx={{ 
                  maxWidth: { xs: '90%', sm: '180px' }, // Wider on mobile to use available space
                  fontSize: { xs: '0.95rem', sm: '1.1rem' }, // Slightly smaller on mobile
                  fontWeight: 'medium',
                }}
              >
                {caseData.title}
              </Typography>
            </Box>
            <Chip
              label={getStatusLabel(caseData.status)}
              size="small"
              color={getStatusColor(caseData.status)}
              sx={{ 
                alignSelf: { xs: 'flex-start', sm: 'center' }, // Align left on mobile
                fontSize: { xs: '0.7rem', sm: '0.75rem' }, // Adapt text size
                height: { xs: '22px', sm: '24px' }, // Slightly smaller height on mobile
              }}
            />
          </Box>
          
          <Typography 
            variant="body2" 
            color="text.secondary" 
            sx={{
              overflow: 'hidden',
              textOverflow: 'ellipsis',
              display: '-webkit-box',
              WebkitLineClamp: 2,
              WebkitBoxOrient: 'vertical',
              mb: 1,
              fontSize: { xs: '0.8rem', sm: '0.875rem' }, // Smaller font on mobile
              lineHeight: 1.4,
            }}
          >
            {caseData.description || t('No description provided')}
          </Typography>
          
          <Box sx={{ 
            mt: 2, 
            display: 'flex', 
            justifyContent: 'space-between', 
            alignItems: 'center',
            flexWrap: 'wrap',
            gap: { xs: 0.5, sm: 1 },
          }}>
            <Box sx={{ 
              display: 'flex', 
              alignItems: 'center', 
              fontSize: { xs: '0.7rem', sm: '0.75rem' },
              color: 'text.secondary',
              mr: { xs: 1, sm: 2 },
            }}>
              <AccessTimeIcon sx={{ fontSize: { xs: '0.9rem', sm: '1rem' }, mr: 0.5 }} />
              <Typography variant="caption" component="span">
                {timeAgo}
              </Typography>
            </Box>
            
            <Chip
              icon={<PriorityHighIcon fontSize="small" />}
              label={getPriorityLabel(caseData.priority)}
              size="small"
              color={getPriorityColor(caseData.priority)}
              sx={{ 
                height: { xs: '22px', sm: '24px' }, 
                fontSize: { xs: '0.7rem', sm: '0.75rem' },
                '& .MuiChip-icon': { 
                  fontSize: { xs: '0.9rem', sm: '1rem' } 
                } 
              }}
            />
          </Box>
        </CardContent>
        
        <Box sx={{ px: { xs: 1.5, sm: 2 }, pb: { xs: 1.5, sm: 2 } }}>
          <LinearProgress 
            variant="determinate" 
            value={getProgressValue(caseData.status)} 
            color={getStatusColor(caseData.status)}
            sx={{ 
              height: { xs: 4, sm: 6 }, 
              borderRadius: { xs: 1, sm: 2 } 
            }} 
          />
          
          <Box sx={{ 
            display: 'flex', 
            justifyContent: 'flex-end', 
            mt: 1.5 
          }}>
            <Button
              variant="text"
              color="primary"
              size={isMobile ? "small" : "medium"}
              onClick={handleViewDetails}
              endIcon={<ArrowForwardIcon />}
              sx={{ 
                minHeight: { xs: '32px', sm: '36px' },
                fontSize: { xs: '0.8rem', sm: '0.875rem' },
              }}
            >
              {t('View')}
            </Button>
          </Box>
        </Box>
      </Card>
    );
  }

  // Default variant
  return (
    <Card
      sx={{
        mb: 3,
        borderRadius: { xs: 1, sm: 2 },
        transition: 'all 0.2s ease-in-out',
        '&:hover': {
          transform: 'translateY(-4px)',
          boxShadow: 4,
        },
        overflow: 'visible', // For the priority indicator that extends beyond the card
        position: 'relative',
      }}
    >
      {/* Priority indicator */}
      <Box
        sx={{
          position: 'absolute',
          top: { xs: -8, sm: -10 },
          right: { xs: 8, sm: 16 },
          bgcolor: theme.palette[getPriorityColor(caseData.priority)].main,
          color: theme.palette[getPriorityColor(caseData.priority)].contrastText,
          borderRadius: '50%',
          width: { xs: 28, sm: 36 },
          height: { xs: 28, sm: 36 },
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          boxShadow: 2,
          zIndex: 1,
        }}
      >
        <Tooltip title={`${t('Priority')}: ${getPriorityLabel(caseData.priority)}`}>
          <PriorityHighIcon sx={{ fontSize: { xs: '1rem', sm: '1.25rem' } }} />
        </Tooltip>
      </Box>

      <CardContent sx={{ pt: { xs: 2, sm: 3 }, px: { xs: 2, sm: 3 } }}>
        <Box sx={{ 
          display: 'flex', 
          alignItems: { xs: 'flex-start', sm: 'center' },
          flexDirection: { xs: 'column', sm: 'row' },
          mb: 2 
        }}>
          <Box sx={{ 
            display: 'flex', 
            alignItems: 'center',
            mb: { xs: 1, sm: 0 },
            width: { xs: '100%', sm: 'auto' },
          }}>
            <Tooltip title={getCaseTypeLabel(caseData.type)}>
              <Box
                sx={{
                  mr: 1.5,
                  color: theme.palette.primary.main,
                  display: 'flex',
                }}
              >
                {getCaseTypeIcon(caseData.type)}
              </Box>
            </Tooltip>
            <Typography 
              variant="h5" 
              component="h2" 
              sx={{ 
                fontWeight: 'bold',
                fontSize: { xs: '1.15rem', sm: '1.4rem' },
                mr: { xs: 0, sm: 2 },
              }}
            >
              {caseData.title}
            </Typography>
          </Box>

          <Chip
            label={getStatusLabel(caseData.status)}
            color={getStatusColor(caseData.status)}
            sx={{ 
              alignSelf: { xs: 'flex-start', sm: 'flex-start' },
              height: { xs: '24px', sm: '28px' }, 
              fontSize: { xs: '0.75rem', sm: '0.8rem' },
            }}
          />
        </Box>

        <Typography 
          variant="body1" 
          color="text.secondary" 
          paragraph
          sx={{ 
            mb: 2,
            fontSize: { xs: '0.85rem', sm: '0.95rem' },
            lineHeight: 1.5,
          }}
        >
          {caseData.description || t('No description provided')}
        </Typography>

        <Box
          sx={{
            display: 'flex',
            flexWrap: 'wrap',
            gap: { xs: 1, sm: 2 },
            mb: 2,
          }}
        >
          <Box
            sx={{
              display: 'flex',
              alignItems: 'center',
              fontSize: { xs: '0.8rem', sm: '0.875rem' },
              color: 'text.secondary',
            }}
          >
            <PersonIcon sx={{ mr: 0.5, fontSize: { xs: '1rem', sm: '1.25rem' } }} />
            <Typography variant="body2" component="span">
              {caseData.client?.name || t('Unknown Client')}
            </Typography>
          </Box>

          <Box
            sx={{
              display: 'flex',
              alignItems: 'center',
              fontSize: { xs: '0.8rem', sm: '0.875rem' },
              color: 'text.secondary',
            }}
          >
            <AccessTimeIcon sx={{ mr: 0.5, fontSize: { xs: '1rem', sm: '1.25rem' } }} />
            <Typography variant="body2" component="span">
              {timeAgo}
            </Typography>
          </Box>

          <Box
            sx={{
              display: 'flex',
              alignItems: 'center',
              fontSize: { xs: '0.8rem', sm: '0.875rem' },
              color: 'text.secondary',
            }}
          >
            <DescriptionIcon sx={{ mr: 0.5, fontSize: { xs: '1rem', sm: '1.25rem' } }} />
            <Typography variant="body2" component="span">
              {caseData.documents?.length || 0} {t('documents')}
            </Typography>
          </Box>
        </Box>

        <Box sx={{ mt: 3 }}>
          <LinearProgress 
            variant="determinate" 
            value={getProgressValue(caseData.status)} 
            color={getStatusColor(caseData.status)}
            sx={{ 
              height: { xs: 5, sm: 8 }, 
              borderRadius: { xs: 1, sm: 2 } 
            }} 
          />
          <Typography 
            variant="caption" 
            color="text.secondary" 
            component="div" 
            sx={{ 
              mt: 0.5, 
              textAlign: 'right',
              fontSize: { xs: '0.7rem', sm: '0.75rem' },
            }}
          >
            {getProgressValue(caseData.status)}% {t('complete')}
          </Typography>
        </Box>
      </CardContent>

      <CardActions 
        sx={{ 
          justifyContent: 'space-between', 
          px: { xs: 2, sm: 3 }, 
          pb: { xs: 2, sm: 3 },
          pt: 0,
        }}
      >
        <Button
          variant="outlined"
          size={isMobile ? "small" : "medium"}
          startIcon={<DescriptionIcon />}
          sx={{ 
            minHeight: { xs: '36px', sm: '40px' },
            fontSize: { xs: '0.8rem', sm: '0.875rem' },
          }}
        >
          {t('Documents')}
        </Button>
        <Button
          variant="contained"
          color="primary"
          size={isMobile ? "small" : "medium"}
          onClick={handleViewDetails}
          endIcon={<ArrowForwardIcon />}
          sx={{ 
            minHeight: { xs: '36px', sm: '40px' },
            fontSize: { xs: '0.8rem', sm: '0.875rem' },
          }}
        >
          {t('Case Details')}
        </Button>
      </CardActions>
    </Card>
  );
};

CaseCard.propTypes = {
  caseData: PropTypes.shape({
    id: PropTypes.string.isRequired,
    title: PropTypes.string.isRequired,
    description: PropTypes.string,
    type: PropTypes.string.isRequired,
    status: PropTypes.string.isRequired,
    priority: PropTypes.string.isRequired,
    created: PropTypes.string.isRequired,
    updated: PropTypes.string.isRequired,
    client: PropTypes.shape({
      id: PropTypes.string,
      name: PropTypes.string,
    }),
    lawyer: PropTypes.shape({
      id: PropTypes.string,
      name: PropTypes.string,
    }),
  }).isRequired,
  variant: PropTypes.oneOf(['default', 'compact']),
};

export default CaseCard;