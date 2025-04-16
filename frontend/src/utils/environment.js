// Environment detection
export const isDevelopment = process.env.NODE_ENV === 'development';
export const isProduction = process.env.NODE_ENV === 'production';
export const isTest = process.env.NODE_ENV === 'test';

// API configuration
export const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:5003/api';

// Feature flags
export const FEATURES = {
  enableAnalytics: isProduction,
  enableErrorReporting: isProduction,
  enableDebugLogging: isDevelopment,
  enablePerformanceMonitoring: isProduction,
};

// Environment-specific settings
export const ENV_CONFIG = {
  maxRetries: isProduction ? 3 : 1,
  cacheTimeout: isProduction ? 3600000 : 0, // 1 hour in production, disabled in development
  apiTimeout: isProduction ? 30000 : 5000, // 30 seconds in production, 5 seconds in development
};

export default {
  isDevelopment,
  isProduction,
  isTest,
  API_BASE_URL,
  FEATURES,
  ENV_CONFIG,
}; 