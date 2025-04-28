const config = {
  // API Configuration
  API_URL: process.env.REACT_APP_API_URL || 'https://smartprobonoapp.onrender.com',
  baseURL: process.env.REACT_APP_API_URL || 'https://smartprobonoapp.onrender.com',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
    'X-Requested-With': 'XMLHttpRequest',
    'X-Client-Version': '1.0.0',
  },
  withCredentials: true,
  
  // Security Configuration
  security: {
    tokenKey: 'auth_token',
    refreshTokenKey: 'refresh_token',
    tokenPrefix: 'Bearer',
    secureCookie: process.env.NODE_ENV === 'production',
    csrfHeaderName: 'X-CSRF-Token',
  },
  
  // Rate Limiting
  rateLimit: {
    maxRequests: 100,
    perWindow: 60000, // 1 minute
  },
  
  // Error Messages
  errors: {
    network: 'Network error. Please check your connection.',
    unauthorized: 'Please log in to access this feature.',
    forbidden: 'You do not have permission to access this resource.',
    notFound: 'The requested resource was not found.',
    validation: 'Please check your input and try again.',
    server: 'An unexpected error occurred. Please try again later.',
    timeout: 'The request timed out. Please try again.',
  },
  
  // Feature Flags
  features: {
    enableAI: true,
    enablePDFGeneration: true,
    enableWebSocket: true,
    enableAnalytics: process.env.NODE_ENV === 'production',
  },
  
  // Analytics
  analytics: {
    enabled: process.env.NODE_ENV === 'production',
    trackingId: process.env.REACT_APP_ANALYTICS_ID,
  },
  
  // Websocket
  websocket: {
    url: process.env.REACT_APP_WEBSOCKET_URL || 'wss://smartprobonoapp.onrender.com',
    reconnectInterval: 3000,
    maxReconnectAttempts: 5,
  },
};

// Export both the default config and named exports
export const { API_URL, baseURL, security, features, websocket } = config;
export default config; 