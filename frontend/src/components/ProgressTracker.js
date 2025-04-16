import React from 'react';
import {
  Box,
  Paper,
  Typography,
  LinearProgress,
  Chip,
  Grid,
  Card,
  CardContent,
  Badge,
  IconButton,
  Tooltip,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
} from '@mui/material';
import {
  EmojiEvents as TrophyIcon,
  Share as ShareIcon,
  Star as StarIcon,
  CheckCircle as CheckCircleIcon,
  Lock as LockIcon,
} from '@mui/icons-material';
import { useTranslation } from 'react-i18next';
import PropTypes from 'prop-types';

const ProgressTracker = ({ progress, achievements = [], isPremium = false, onUpgradeClick }) => {
  const { t } = useTranslation();
  const [showBadgeDialog, setShowBadgeDialog] = React.useState(false);
  const [selectedBadge, setSelectedBadge] = React.useState(null);

  const badges = [
    {
      id: 'first_doc',
      title: t('progress.badges.firstDoc'),
      description: t('progress.badges.firstDocDesc'),
      icon: <StarIcon />,
      unlocked: progress >= 20,
    },
    {
      id: 'expert',
      title: t('progress.badges.expert'),
      description: t('progress.badges.expertDesc'),
      icon: <TrophyIcon />,
      unlocked: progress >= 50,
      premium: true,
    },
    // Add more badges as needed
  ];

  const handleBadgeClick = badge => {
    if (badge.premium && !isPremium) {
      onUpgradeClick();
      return;
    }
    setSelectedBadge(badge);
    setShowBadgeDialog(true);
  };

  const handleShare = async achievement => {
    try {
      await navigator.share({
        title: 'My Legal Achievement',
        text: `I just earned the ${achievement.title} badge on ProBono App!`,
        url: window.location.href,
      });
    } catch (err) {
      console.error('Error sharing:', err);
    }
  };

  return (
    <Box sx={{ mb: 4 }}>
      <Paper elevation={3} sx={{ p: 3 }}>
        <Typography variant="h5" gutterBottom>
          {t('progress.title')}
        </Typography>

        <Box sx={{ mb: 3 }}>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
            <Typography variant="body2" color="text.secondary">
              {t('progress.overall')}
            </Typography>
            <Typography variant="body2" color="text.secondary">
              {progress}%
            </Typography>
          </Box>
          <LinearProgress
            variant="determinate"
            value={progress}
            sx={{ height: 10, borderRadius: 5 }}
          />
        </Box>

        <Grid container spacing={2} sx={{ mb: 3 }}>
          {badges.map(badge => (
            <Grid item key={badge.id}>
              <Tooltip
                title={badge.premium && !isPremium ? t('progress.premiumFeature') : badge.title}
              >
                <Badge
                  badgeContent={badge.premium && !isPremium ? <LockIcon /> : null}
                  color="primary"
                >
                  <Chip
                    icon={badge.icon}
                    label={badge.title}
                    color={badge.unlocked ? 'primary' : 'default'}
                    onClick={() => handleBadgeClick(badge)}
                    sx={{
                      opacity: badge.unlocked ? 1 : 0.6,
                      cursor: 'pointer',
                    }}
                  />
                </Badge>
              </Tooltip>
            </Grid>
          ))}
        </Grid>

        <Typography variant="h6" gutterBottom>
          {t('progress.recentAchievements')}
        </Typography>

        <Grid container spacing={2}>
          {achievements.map(achievement => (
            <Grid item xs={12} sm={6} md={4} key={achievement.id}>
              <Card>
                <CardContent>
                  <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                    <CheckCircleIcon color="success" sx={{ mr: 1 }} />
                    <Typography variant="subtitle1">{achievement.title}</Typography>
                  </Box>
                  <Typography variant="body2" color="text.secondary">
                    {achievement.description}
                  </Typography>
                  <Box sx={{ display: 'flex', justifyContent: 'flex-end', mt: 1 }}>
                    <IconButton
                      size="small"
                      onClick={() => handleShare(achievement)}
                      aria-label="share achievement"
                    >
                      <ShareIcon />
                    </IconButton>
                  </Box>
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>

        <Dialog open={showBadgeDialog} onClose={() => setShowBadgeDialog(false)}>
          <DialogTitle>{selectedBadge?.title}</DialogTitle>
          <DialogContent>
            <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
              {selectedBadge?.icon}
              <Typography sx={{ ml: 1 }}>{selectedBadge?.description}</Typography>
            </Box>
            {selectedBadge?.unlocked ? (
              <Button
                startIcon={<ShareIcon />}
                onClick={() => handleShare(selectedBadge)}
                fullWidth
              >
                {t('common.share')}
              </Button>
            ) : (
              <Typography color="text.secondary">{t('progress.lockedBadgeMessage')}</Typography>
            )}
          </DialogContent>
          <DialogActions>
            <Button onClick={() => setShowBadgeDialog(false)}>{t('common.close')}</Button>
          </DialogActions>
        </Dialog>
      </Paper>
    </Box>
  );
};


// Define PropTypes
ProgressTracker.propTypes = {
  /** TODO: Add description */
  progress: PropTypes.any,
  /** TODO: Add description */
  achievements: PropTypes.any,
  /** TODO: Add description */
  isPremium: PropTypes.any,
  /** TODO: Add description */
  onUpgradeClick: PropTypes.any,
};

export default ProgressTracker;
