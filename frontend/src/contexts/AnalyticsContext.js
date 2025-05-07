import React, { createContext, useContext } from 'react';
import ReactGA from 'react-ga4';

const AnalyticsContext = createContext();

export const useAnalytics = () => {
  const context = useContext(AnalyticsContext);
  if (!context) {
    throw new Error('useAnalytics must be used within an AnalyticsProvider');
  }
  return context;
};

export const AnalyticsProvider = ({ children }) => {
  const trackEvent = (category, action, label, value) => {
    ReactGA.event({
      category,
      action,
      label,
      value
    });
  };

  const trackPageView = (path) => {
    ReactGA.send({ hitType: "pageview", page: path });
  };

  const trackError = (error, component) => {
    ReactGA.event({
      category: 'error',
      action: 'error_occurred',
      label: `${component}: ${error.message}`,
      value: 1
    });
  };

  const trackUserAction = (action, details) => {
    ReactGA.event({
      category: 'user_action',
      action,
      label: JSON.stringify(details),
      value: 1
    });
  };

  const value = {
    trackEvent,
    trackPageView,
    trackError,
    trackUserAction
  };

  return (
    <AnalyticsContext.Provider value={value}>
      {children}
    </AnalyticsContext.Provider>
  );
};

export default AnalyticsContext; 