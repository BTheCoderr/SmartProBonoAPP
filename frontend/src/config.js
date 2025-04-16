const config = {
  apiUrl: process.env.REACT_APP_API_URL || 'http://localhost:5002',
  // Socket.IO client will handle the connection path
  env: process.env.NODE_ENV || 'development',
  api: {
    baseUrl: process.env.REACT_APP_API_URL || 'http://localhost:5002',
    timeout: 30000, // 30 seconds
    retryAttempts: 3,
    endpoints: {
      legal: '/api/legal',
      documents: '/api/documents',
      auth: '/api/auth',
      cases: '/api/cases'
    }
  },
  support: {
    email: 'support@smartprobono.org',
    phone: '+1 (800) PRO-BONO',
    hours: '9:00 AM - 5:00 PM EST',
    responseTime: '24-48 hours',
  },
  features: {
    enableWebSocket: true, // Enable WebSocket for real-time chat
    enableAnalytics: process.env.NODE_ENV === 'production',
    enableFeedback: true,
  },
  security: {
    sessionTimeout: 3600000, // 1 hour
    refreshTokenInterval: 300000, // 5 minutes
    maxLoginAttempts: 5
  }
};

export default config;
