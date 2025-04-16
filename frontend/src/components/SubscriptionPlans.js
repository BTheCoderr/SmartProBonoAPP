import React from 'react';
import {
  Box,
  Paper,
  Typography,
  Button,
  Grid,
  Card,
  CardContent,
  CardActions,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Divider,
  Chip,
} from '@mui/material';
import {
  Check as CheckIcon,
  Star as StarIcon,
  Business as BusinessIcon,
  Person as PersonIcon,
} from '@mui/icons-material';
import { useTranslation } from 'react-i18next';
import PropTypes from 'prop-types';
const SubscriptionPlans = ({ onSubscribe, currentPlan = 'free' }) => {
  const { t } = useTranslation();
  const plans = [
    {
      id: 'free',
      title: t('subscription.plans.free.title'),
      description: t('subscription.plans.free.description'),
      price: '$0',
      icon: <PersonIcon fontSize="large" />,
      features: [
        t('subscription.plans.free.features.templates'),
        t('subscription.plans.free.features.chat'),
        t('subscription.plans.free.features.resources'),
      ],
      buttonText: t('subscription.current'),
      recommended: false,
    },
    {
      id: 'pro',
      title: t('subscription.plans.pro.title'),
      description: t('subscription.plans.pro.description'),
      price: '$9.99',
      period: t('subscription.monthly'),
      icon: <StarIcon fontSize="large" />,
      features: [
        t('subscription.plans.pro.features.all'),
        t('subscription.plans.pro.features.advanced'),
        t('subscription.plans.pro.features.priority'),
        t('subscription.plans.pro.features.customization'),
      ],
      buttonText: currentPlan === 'pro' ? t('subscription.current') : t('subscription.upgrade'),
      recommended: true,
    },
    {
      id: 'team',
      title: t('subscription.plans.team.title'),
      description: t('subscription.plans.team.description'),
      price: t('subscription.plans.team.price'),
      icon: <BusinessIcon fontSize="large" />,
      features: [
        t('subscription.plans.team.features.all'),
        t('subscription.plans.team.features.team'),
        t('subscription.plans.team.features.analytics'),
        t('subscription.plans.team.features.support'),
      ],
      buttonText: t('subscription.contact'),
      recommended: false,
    },
  ];
  const handleSubscribe = planId => {
    if (planId === currentPlan) return;
    onSubscribe(planId);
  };
  return (
    <Box sx={{ py: 4 }}>
      <Typography variant="h4" align="center" gutterBottom>
        {t('subscription.title')}
      </Typography>
      <Typography variant="subtitle1" align="center" color="text.secondary" sx={{ mb: 6 }}>
        {t('subscription.subtitle')}
      </Typography>
      <Grid container spacing={4} justifyContent="center">
        {plans.map(plan => (
          <Grid item xs={12} sm={6} md={4} key={plan.id}>
            <Card
              elevation={plan.recommended ? 8 : 1}
              sx={{
                height: '100%',
                display: 'flex',
                flexDirection: 'column',
                position: 'relative',
                border: plan.recommended ? 2 : 0,
                borderColor: 'primary.main',
              }}
            >
              {plan.recommended && (
                <Chip
                  label={t('subscription.recommended')}
                  color="primary"
                  sx={{
                    position: 'absolute',
                    top: -12,
                    right: 20,
                  }}
                />
              )}
              <CardContent sx={{ flexGrow: 1 }}>
                <Box sx={{ textAlign: 'center', mb: 2 }}>
                  {plan.icon}
                  <Typography variant="h5" component="div" gutterBottom>
                    {plan.title}
                  </Typography>
                  <Typography variant="subtitle1" color="text.secondary" paragraph>
                    {plan.description}
                  </Typography>
                  <Box
                    sx={{
                      display: 'flex',
                      justifyContent: 'center',
                      alignItems: 'baseline',
                      mb: 2,
                    }}
                  >
                    <Typography variant="h4" component="span">
                      {plan.price}
                    </Typography>
                    {plan.period && (
                      <Typography variant="subtitle1" color="text.secondary" sx={{ ml: 1 }}>
                        /{plan.period}
                      </Typography>
                    )}
                  </Box>
                </Box>
                <Divider sx={{ my: 2 }} />
                <List dense>
                  {plan.features.map((feature, index) => (
                    <ListItem key={index}>
                      <ListItemIcon>
                        <CheckIcon color="primary" />
                      </ListItemIcon>
                      <ListItemText primary={feature} />
                    </ListItem>
                  ))}
                </List>
              </CardContent>
              <CardActions sx={{ p: 2, pt: 0 }}>
                <Button
                  fullWidth
                  variant={plan.recommended ? 'contained' : 'outlined'}
                  onClick={() => handleSubscribe(plan.id)}
                  disabled={plan.id === currentPlan}
                >
                  {plan.buttonText}
                </Button>
              </CardActions>
            </Card>
          </Grid>
        ))}
      </Grid>
      <Box sx={{ mt: 6, textAlign: 'center' }}>
        <Typography variant="body2" color="text.secondary">
          {t('subscription.nonprofit')}
        </Typography>
        <Button color="primary" sx={{ mt: 1 }}>
          {t('subscription.contactSales')}
        </Button>
      </Box>
    </Box>
  );
};

// Define PropTypes
SubscriptionPlans.propTypes = {
  /** TODO: Add description */
  onSubscribe: PropTypes.any,
  /** TODO: Add description */
  currentPlan: PropTypes.any,
};

export default SubscriptionPlans;