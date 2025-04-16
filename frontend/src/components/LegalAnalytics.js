import React, { useState, useEffect } from 'react';
import {
  Box,
  Paper,
  Typography,
  CircularProgress,
  Grid,
  Card,
  CardContent,
  LinearProgress,
  Chip,
  Alert,
  Button,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
} from '@mui/material';
import {
  TrendingUp as TrendingUpIcon,
  Gavel as GavelIcon,
  Assignment as AssignmentIcon,
  Timeline as TimelineIcon,
} from '@mui/icons-material';
import { useTranslation } from 'react-i18next';
import PropTypes from 'prop-types';
const LegalAnalytics = ({ caseData, onRecommendation }) => {
  const { t } = useTranslation();
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(false);
  const [showDetails, setShowDetails] = useState(false);
  const [selectedFactor, setSelectedFactor] = useState(null);
  useEffect(() => {
    if (caseData) {
      analyzeCaseData();
    }
  }, [caseData, analyzeCaseData]);
  const analyzeCaseData = async () => {
    setLoading(true);
    try {
      const response = await fetch('/api/legal/analyze', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(caseData),
      });
      const data = await response.json();
      setAnalysis(data);
    } catch (error) {
      console.error('Analysis error:', error);
    } finally {
      setLoading(false);
    }
  };
  const getSuccessRateColor = rate => {
    if (rate >= 75) return 'success';
    if (rate >= 50) return 'warning';
    return 'error';
  };
  const renderSuccessFactors = () => {
    if (!analysis?.factors) return null;
    return analysis.factors.map((factor, index) => (
      <Grid item xs={12} md={6} key={index}>
        <Card>
          <CardContent>
            <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
              <GavelIcon sx={{ mr: 1 }} />
              <Typography variant="h6">{factor.name}</Typography>
            </Box>
            <LinearProgress
              variant="determinate"
              value={factor.impact}
              color={factor.impact >= 70 ? 'success' : 'warning'}
              sx={{ mb: 1, height: 8, borderRadius: 4 }}
            />
            <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
              <Typography variant="body2" color="text.secondary">
                {t('analytics.impact')}
              </Typography>
              <Typography variant="body2" color="text.secondary">
                {factor.impact}%
              </Typography>
            </Box>
            <Button
              size="small"
              onClick={() => {
                setSelectedFactor(factor);
                setShowDetails(true);
              }}
              sx={{ mt: 1 }}
            >
              {t('common.learnMore')}
            </Button>
          </CardContent>
        </Card>
      </Grid>
    ));
  };
  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', p: 4 }}>
        <CircularProgress />
      </Box>
    );
  }
  return (
    <Box sx={{ mb: 4 }}>
      <Paper elevation={3} sx={{ p: 3 }}>
        {analysis && (
          <>
            <Box sx={{ mb: 4, textAlign: 'center' }}>
              <Typography variant="h4" gutterBottom>
                {t('analytics.caseAnalysis')}
              </Typography>
              <Box sx={{ display: 'flex', justifyContent: 'center', gap: 2, mb: 3 }}>
                <Chip
                  icon={<TrendingUpIcon />}
                  label={`${analysis.successRate}% ${t('analytics.successRate')}`}
                  color={getSuccessRateColor(analysis.successRate)}
                />
                <Chip
                  icon={<TimelineIcon />}
                  label={`${analysis.timeEstimate} ${t('analytics.estimatedTime')}`}
                />
              </Box>
              {analysis.recommendation && (
                <Alert severity="info" sx={{ mb: 3 }}>
                  {analysis.recommendation}
                </Alert>
              )}
            </Box>
            <Typography variant="h5" gutterBottom>
              {t('analytics.keyFactors')}
            </Typography>
            <Grid container spacing={3}>
              {renderSuccessFactors()}
            </Grid>
            {analysis.similarCases && (
              <Box sx={{ mt: 4 }}>
                <Typography variant="h5" gutterBottom>
                  {t('analytics.similarCases')}
                </Typography>
                <Grid container spacing={2}>
                  {analysis.similarCases.map((caseRef, index) => (
                    <Grid item xs={12} key={index}>
                      <Card variant="outlined">
                        <CardContent>
                          <Typography variant="subtitle1">{caseRef.title}</Typography>
                          <Typography variant="body2" color="text.secondary">
                            {caseRef.outcome}
                          </Typography>
                        </CardContent>
                      </Card>
                    </Grid>
                  ))}
                </Grid>
              </Box>
            )}
          </>
        )}
        <Dialog open={showDetails} onClose={() => setShowDetails(false)}>
          <DialogTitle>{selectedFactor?.name}</DialogTitle>
          <DialogContent>
            <Typography paragraph>{selectedFactor?.description}</Typography>
            {selectedFactor?.recommendations?.map((rec, index) => (
              <Alert severity="info" sx={{ mt: 1 }} key={index}>
                {rec}
              </Alert>
            ))}
          </DialogContent>
          <DialogActions>
            <Button onClick={() => setShowDetails(false)}>{t('common.close')}</Button>
          </DialogActions>
        </Dialog>
      </Paper>
    </Box>
  );
};

// Define PropTypes
LegalAnalytics.propTypes = {
  /** TODO: Add description */
  caseData: PropTypes.any,
  /** TODO: Add description */
  onRecommendation: PropTypes.any,
};

export default LegalAnalytics;