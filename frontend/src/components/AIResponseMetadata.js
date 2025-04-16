import React from 'react';
import {
  Box,
  LinearProgress,
  Typography,
  Chip,
  Card,
  CardContent,
  Tooltip,
  IconButton,
  Collapse,
  List,
  ListItem,
  ListItemText,
  Link,
} from '@mui/material';
import InfoIcon from '@mui/icons-material/Info';
import VerifiedIcon from '@mui/icons-material/Verified';
import WarningIcon from '@mui/icons-material/Warning';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import LibraryBooksIcon from '@mui/icons-material/LibraryBooks';
import { useTranslation } from 'react-i18next';
import PropTypes from 'prop-types';

const AIResponseMetadata = ({
  confidenceScore,
  citations = [],
  reasoningDetails = '',
  jurisdictions = [],
  lastUpdated = null,
}) => {
  const { t } = useTranslation();
  const [expanded, setExpanded] = React.useState(false);

  const getConfidenceMeta = (score) => {
    if (score >= 85) {
      return {
        color: 'success',
        label: t('High Confidence'),
        icon: <VerifiedIcon />,
        description: t('This response is based on well-established legal principles and sources.'),
      };
    } else if (score >= 60) {
      return {
        color: 'primary',
        label: t('Medium Confidence'),
        icon: <InfoIcon />,
        description: t(
          'This response is generally reliable but may have some limitations or ambiguities.'
        ),
      };
    } else {
      return {
        color: 'warning',
        label: t('Low Confidence'),
        icon: <WarningIcon />,
        description: t(
          'This response addresses complex or evolving legal issues. Consult an attorney.'
        ),
      };
    }
  };

  const confidenceMeta = getConfidenceMeta(confidenceScore);

  return (
    <Card variant="outlined" sx={{ mt: 2, mb: 2 }}>
      <CardContent>
        <Box display="flex" alignItems="center" justifyContent="space-between" mb={1}>
          <Box display="flex" alignItems="center">
            <Tooltip title={confidenceMeta.description}>
              <Chip
                icon={confidenceMeta.icon}
                label={confidenceMeta.label}
                color={confidenceMeta.color}
                size="small"
                sx={{ mr: 1 }}
              />
            </Tooltip>

            <Box sx={{ width: '100%', maxWidth: 180, ml: 1, mr: 1 }}>
              <LinearProgress
                variant="determinate"
                value={confidenceScore}
                color={confidenceMeta.color}
                sx={{ height: 8, borderRadius: 5 }}
              />
            </Box>

            <Typography variant="body2" color="text.secondary">
              {confidenceScore}%
            </Typography>
          </Box>

          {jurisdictions.length > 0 && (
            <Box>
              <Typography variant="caption" color="text.secondary" mr={1}>
                {t('Jurisdictions')}:
              </Typography>
              {jurisdictions.map((jurisdiction, index) => (
                <Chip
                  key={index}
                  label={jurisdiction}
                  size="small"
                  variant="outlined"
                  sx={{ ml: 0.5 }}
                />
              ))}
            </Box>
          )}

          <IconButton
            size="small"
            onClick={() => setExpanded(!expanded)}
            aria-expanded={expanded}
            aria-label="show more"
          >
            <ExpandMoreIcon
              sx={{ transform: expanded ? 'rotate(180deg)' : 'rotate(0deg)', transition: '0.3s' }}
            />
          </IconButton>
        </Box>

        {lastUpdated && (
          <Typography variant="caption" color="text.secondary" sx={{ display: 'block', mb: 1 }}>
            {t('Last updated')}: {new Date(lastUpdated).toLocaleDateString()}
          </Typography>
        )}

        <Collapse in={expanded} timeout="auto" unmountOnExit>
          {citations.length > 0 && (
            <Box mt={2}>
              <Box display="flex" alignItems="center" mb={1}>
                <LibraryBooksIcon fontSize="small" sx={{ mr: 1 }} color="primary" />
                <Typography variant="subtitle2">{t('Legal Citations')}</Typography>
              </Box>
              <List dense sx={{ bgcolor: 'background.paper', borderRadius: 1 }}>
                {citations.map((citation, index) => (
                  <ListItem key={index} divider={index !== citations.length - 1}>
                    <ListItemText
                      primary={
                        <Typography variant="body2">
                          {citation.text}
                          {citation.url && (
                            <Link href={citation.url} target="_blank" rel="noopener" sx={{ ml: 1 }}>
                              {t('View Source')}
                            </Link>
                          )}
                        </Typography>
                      }
                      secondary={
                        <Typography variant="caption" color="text.secondary">
                          {citation.type} • {citation.year}
                        </Typography>
                      }
                    />
                  </ListItem>
                ))}
              </List>
            </Box>
          )}

          {reasoningDetails && (
            <Box mt={2}>
              <Typography variant="subtitle2" gutterBottom>
                {t('AI Reasoning Details')}
              </Typography>
              <Typography variant="body2" color="text.secondary" sx={{ whiteSpace: 'pre-line' }}>
                {reasoningDetails}
              </Typography>
            </Box>
          )}
        </Collapse>
      </CardContent>
    </Card>
  );
};


// Define PropTypes
AIResponseMetadata.propTypes = {
  /** Confidence score percentage (0-100) indicating the AI's confidence in the response */
  confidenceScore: PropTypes.number.isRequired,
  /** Array of citation objects with source information */
  citations: PropTypes.arrayOf(
    PropTypes.shape({
      text: PropTypes.string.isRequired,
      url: PropTypes.string,
      type: PropTypes.string.isRequired,
      year: PropTypes.oneOfType([PropTypes.string, PropTypes.number]).isRequired
    })
  ),
  /** Detailed explanation of the AI's reasoning process */
  reasoningDetails: PropTypes.string,
  /** Array of relevant legal jurisdictions */
  jurisdictions: PropTypes.arrayOf(PropTypes.string),
  /** ISO date string of when the information was last updated */
  lastUpdated: PropTypes.string,
};

export default AIResponseMetadata;
