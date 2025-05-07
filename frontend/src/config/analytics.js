// Google Analytics Configuration
export const GA4_CONFIG = {
  measurementId: process.env.REACT_APP_GA4_ID || 'G-JZGTHZLVVJ',
  streamId: process.env.REACT_APP_GA4_STREAM_ID || '11106122551',
  enabled: process.env.REACT_APP_ANALYTICS_ENABLED === 'true',
};

// Analytics Event Types
export const ANALYTICS_EVENTS = {
  FORM_VIEW: 'form_view',
  FORM_START: 'form_start',
  FORM_COMPLETION: 'form_completion',
  FORM_ABANDONMENT: 'form_abandonment',
  FIELD_INTERACTION: 'field_interaction',
  FIELD_TIMING: 'field_timing',
  FORM_ERROR: 'form_error',
};

// Analytics Dimensions
export const ANALYTICS_DIMENSIONS = {
  FORM_TYPE: 'form_type',
  FIELD_NAME: 'field_name',
  ERROR_TYPE: 'error_type',
  DEVICE_TYPE: 'device_type',
  USER_TYPE: 'user_type',
};

// Helper function to track GA4 events
export const trackGAEvent = (eventName, eventParams = {}) => {
  if (window.gtag && GA4_CONFIG.enabled) {
    window.gtag('event', eventName, {
      ...eventParams,
      send_to: GA4_CONFIG.measurementId
    });
  }
}; 