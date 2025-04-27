const config = {
  apiUrl: process.env.REACT_APP_API_URL || 'http://localhost:5003',
  wsUrl: process.env.REACT_APP_WS_URL || 'ws://localhost:5003',
  env: process.env.NODE_ENV || 'development',
  support: {
    email: 'support@smartprobono.org',
    phone: '+1 (800) PRO-BONO',
    hours: '9:00 AM - 5:00 PM EST',
    responseTime: '24-48 hours'
  },
  features: {
    enableWebSocket: true, // Enable WebSocket to use the notification system
    enableAnalytics: true,
    enableFeedback: true,
  }
};

// Export the API_URL for files that import it directly
export const API_URL = config.apiUrl;
export const API_BASE_URL = config.apiUrl;

export default config; 