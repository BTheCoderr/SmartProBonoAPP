import { useState, useEffect, useCallback } from 'react';
import WebSocketService from '../services/WebSocketService';
import AnalyticsService from '../services/AnalyticsService';

const useRealTimeAnalytics = (formType) => {
  const [realTimeData, setRealTimeData] = useState({
    activeUsers: 0,
    recentSubmissions: [],
    fieldCompletionRates: {},
    errorRates: {},
    averageCompletionTime: null
  });

  const [isConnected, setIsConnected] = useState(false);

  const handleAnalyticsUpdate = useCallback((data) => {
    if (data.formType === formType) {
      setRealTimeData(prev => ({
        ...prev,
        ...data.metrics
      }));
    }
  }, [formType]);

  const handleFormActivity = useCallback((data) => {
    if (data.formType === formType) {
      setRealTimeData(prev => ({
        ...prev,
        activeUsers: data.activeUsers,
        recentSubmissions: [data.submission, ...prev.recentSubmissions].slice(0, 10)
      }));
    }
  }, [formType]);

  useEffect(() => {
    // Initialize WebSocket connection
    WebSocketService.connect();
    setIsConnected(true);

    // Subscribe to real-time updates
    const analyticsUnsubscribe = WebSocketService.subscribe(
      'analytics_update',
      handleAnalyticsUpdate
    );

    const activityUnsubscribe = WebSocketService.subscribe(
      'form_activity',
      handleFormActivity
    );

    // Load initial analytics data
    const loadInitialData = async () => {
      try {
        const [analytics, completionRates] = await Promise.all([
          AnalyticsService.getFormAnalytics(formType),
          AnalyticsService.getFieldCompletionRates(formType)
        ]);

        setRealTimeData(prev => ({
          ...prev,
          fieldCompletionRates: completionRates,
          averageCompletionTime: analytics.averageCompletionTime,
          errorRates: analytics.errorRates
        }));
      } catch (error) {
        console.error('Error loading initial analytics data:', error);
      }
    };

    loadInitialData();

    // Cleanup subscriptions
    return () => {
      analyticsUnsubscribe();
      activityUnsubscribe();
      WebSocketService.disconnect();
      setIsConnected(false);
    };
  }, [formType, handleAnalyticsUpdate, handleFormActivity]);

  const refreshAnalytics = useCallback(async () => {
    try {
      const analytics = await AnalyticsService.getFormAnalytics(formType);
      setRealTimeData(prev => ({
        ...prev,
        ...analytics
      }));
    } catch (error) {
      console.error('Error refreshing analytics:', error);
    }
  }, [formType]);

  return {
    realTimeData,
    isConnected,
    refreshAnalytics
  };
};

export default useRealTimeAnalytics; 