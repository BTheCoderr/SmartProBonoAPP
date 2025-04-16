import React, { useState } from 'react';
import {
  Box,
  Paper,
  Typography,
  TextField,
  Button,
  Rating,
  FormControl,
  FormLabel,
  RadioGroup,
  FormControlLabel,
  Radio,
  Snackbar,
  Alert,
  Chip,
} from '@mui/material';
import { useTranslation } from 'react-i18next';
import PropTypes from 'prop-types';

const FeedbackForm = ({ onSubmit, userType = 'user' }) => {
  const { t } = useTranslation();
  const [feedback, setFeedback] = useState({
    rating: 0,
    accuracy: '',
    helpfulness: '',
    clarity: '',
    suggestions: '',
    userType: userType,
  });
  const [submitted, setSubmitted] = useState(false);

  const handleSubmit = async e => {
    e.preventDefault();
    try {
      await onSubmit(feedback);
      setSubmitted(true);
      // Reset form after successful submission
      setFeedback({
        rating: 0,
        accuracy: '',
        helpfulness: '',
        clarity: '',
        suggestions: '',
        userType: userType,
      });
    } catch (error) {
      console.error('Error submitting feedback:', error);
    }
  };

  return (
    <Paper elevation={2} sx={{ p: 3, mt: 3 }}>
      <Box component="form" onSubmit={handleSubmit}>
        <Typography variant="h6" gutterBottom>
          {t('feedback.title')}
        </Typography>

        <Chip
          label={userType === 'lawyer' ? 'Legal Professional' : 'User'}
          color="primary"
          sx={{ mb: 2 }}
        />

        <Box sx={{ mb: 3 }}>
          <Typography component="legend">{t('feedback.overallRating')}</Typography>
          <Rating
            value={feedback.rating}
            onChange={(event, newValue) => {
              setFeedback(prev => ({ ...prev, rating: newValue }));
            }}
            size="large"
          />
        </Box>

        <FormControl component="fieldset" sx={{ mb: 3 }}>
          <FormLabel component="legend">{t('feedback.accuracy')}</FormLabel>
          <RadioGroup
            value={feedback.accuracy}
            onChange={e => setFeedback(prev => ({ ...prev, accuracy: e.target.value }))}
          >
            <FormControlLabel value="high" control={<Radio />} label={t('feedback.accuracyHigh')} />
            <FormControlLabel
              value="medium"
              control={<Radio />}
              label={t('feedback.accuracyMedium')}
            />
            <FormControlLabel value="low" control={<Radio />} label={t('feedback.accuracyLow')} />
          </RadioGroup>
        </FormControl>

        <FormControl component="fieldset" sx={{ mb: 3 }}>
          <FormLabel component="legend">{t('feedback.helpfulness')}</FormLabel>
          <RadioGroup
            value={feedback.helpfulness}
            onChange={e => setFeedback(prev => ({ ...prev, helpfulness: e.target.value }))}
          >
            <FormControlLabel
              value="very"
              control={<Radio />}
              label={t('feedback.helpfulnessVery')}
            />
            <FormControlLabel
              value="somewhat"
              control={<Radio />}
              label={t('feedback.helpfulnessSomewhat')}
            />
            <FormControlLabel
              value="not"
              control={<Radio />}
              label={t('feedback.helpfulnessNot')}
            />
          </RadioGroup>
        </FormControl>

        <FormControl component="fieldset" sx={{ mb: 3 }}>
          <FormLabel component="legend">{t('feedback.clarity')}</FormLabel>
          <RadioGroup
            value={feedback.clarity}
            onChange={e => setFeedback(prev => ({ ...prev, clarity: e.target.value }))}
          >
            <FormControlLabel value="clear" control={<Radio />} label={t('feedback.clarityHigh')} />
            <FormControlLabel
              value="moderate"
              control={<Radio />}
              label={t('feedback.clarityMedium')}
            />
            <FormControlLabel
              value="unclear"
              control={<Radio />}
              label={t('feedback.clarityLow')}
            />
          </RadioGroup>
        </FormControl>

        <TextField
          fullWidth
          multiline
          rows={4}
          label={t('feedback.suggestions')}
          value={feedback.suggestions}
          onChange={e => setFeedback(prev => ({ ...prev, suggestions: e.target.value }))}
          sx={{ mb: 3 }}
        />

        <Button type="submit" variant="contained" color="primary" fullWidth>
          {t('feedback.submit')}
        </Button>
      </Box>

      <Snackbar open={submitted} autoHideDuration={6000} onClose={() => setSubmitted(false)}>
        <Alert onClose={() => setSubmitted(false)} severity="success" sx={{ width: '100%' }}>
          {t('feedback.submitted')}
        </Alert>
      </Snackbar>
    </Paper>
  );
};


// Define PropTypes
FeedbackForm.propTypes = {
  /** TODO: Add description */
  onSubmit: PropTypes.any,
  /** TODO: Add description */
  userType: PropTypes.any,
};

export default FeedbackForm;
