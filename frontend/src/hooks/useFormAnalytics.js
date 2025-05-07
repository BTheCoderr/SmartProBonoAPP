import { useState, useEffect, useRef } from 'react';
import AnalyticsService from '../services/AnalyticsService';

const useFormAnalytics = (formType) => {
  const [analytics, setAnalytics] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const startTimeRef = useRef(Date.now());
  const lastInteractionRef = useRef(Date.now());
  const interactionsRef = useRef([]);
  const fieldTimesRef = useRef({});

  // Load analytics data on mount
  useEffect(() => {
    const loadAnalytics = async () => {
      try {
        const data = await AnalyticsService.getFormAnalytics(formType);
        setAnalytics(data);
      } catch (err) {
        console.error('Error loading analytics:', err);
        setError('Failed to load analytics data');
      } finally {
        setLoading(false);
      }
    };

    loadAnalytics();
    trackFormView();

    return () => {
      // Track form abandonment if not completed
      if (!analytics?.completed) {
        trackFormAbandonment();
      }
    };
  }, [formType]);

  // Track form view
  const trackFormView = async () => {
    try {
      await AnalyticsService.trackFormView(formType);
    } catch (err) {
      console.error('Error tracking form view:', err);
    }
  };

  // Track form start
  const trackFormStart = async () => {
    try {
      await AnalyticsService.trackFormStart(formType);
      startTimeRef.current = Date.now();
    } catch (err) {
      console.error('Error tracking form start:', err);
    }
  };

  // Track form completion
  const trackFormCompletion = async () => {
    try {
      const completionTime = Date.now() - startTimeRef.current;
      await AnalyticsService.trackFormCompletion(formType, completionTime);
    } catch (err) {
      console.error('Error tracking form completion:', err);
    }
  };

  // Track form abandonment
  const trackFormAbandonment = async (lastStep, completionPercentage) => {
    try {
      await AnalyticsService.trackFormAbandonment(formType, lastStep, completionPercentage);
    } catch (err) {
      console.error('Error tracking form abandonment:', err);
    }
  };

  // Track field interaction
  const trackFieldInteraction = async (fieldName, value, interactionType = 'change') => {
    try {
      const now = Date.now();
      const timeSinceLastInteraction = now - lastInteractionRef.current;
      
      // Track field time
      if (!fieldTimesRef.current[fieldName]) {
        fieldTimesRef.current[fieldName] = 0;
      }
      fieldTimesRef.current[fieldName] += timeSinceLastInteraction;

      // Add to interactions list
      interactionsRef.current.push({
        timestamp: now,
        fieldName,
        interactionType,
        timeSinceLastInteraction
      });

      // Track field completion if value is valid
      if (value !== '' && value !== null && value !== undefined) {
        await AnalyticsService.trackFieldCompletion(formType, fieldName, value);
      }

      lastInteractionRef.current = now;
    } catch (err) {
      console.error('Error tracking field interaction:', err);
    }
  };

  // Track form error
  const trackFormError = async (errorType, errorMessage) => {
    try {
      await AnalyticsService.trackFormError(formType, errorType, errorMessage);
    } catch (err) {
      console.error('Error tracking form error:', err);
    }
  };

  // Get field completion rates
  const getFieldCompletionRates = async () => {
    try {
      return await AnalyticsService.getFieldCompletionRates(formType);
    } catch (err) {
      console.error('Error getting field completion rates:', err);
      return null;
    }
  };

  // Get form analytics summary
  const getAnalyticsSummary = () => {
    if (!analytics) return null;

    const totalTime = Date.now() - startTimeRef.current;
    const interactions = interactionsRef.current;
    const fieldTimes = fieldTimesRef.current;

    return {
      totalTime,
      averageTimePerField: Object.values(fieldTimes).reduce((a, b) => a + b, 0) / Object.keys(fieldTimes).length,
      totalInteractions: interactions.length,
      interactionsPerMinute: (interactions.length / (totalTime / 1000 / 60)).toFixed(2),
      mostTimeConsumingFields: Object.entries(fieldTimes)
        .sort(([, a], [, b]) => b - a)
        .slice(0, 5)
        .map(([field, time]) => ({ field, time })),
      fieldCompletionOrder: interactions
        .filter(i => i.interactionType === 'complete')
        .map(i => i.fieldName)
    };
  };

  return {
    analytics,
    loading,
    error,
    trackFormStart,
    trackFormCompletion,
    trackFormAbandonment,
    trackFieldInteraction,
    trackFormError,
    getFieldCompletionRates,
    getAnalyticsSummary
  };
};

export default useFormAnalytics; 