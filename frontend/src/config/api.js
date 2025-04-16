// API Configuration
// This file contains API-related configuration settings

// Base URL for API calls
export const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5002';

// Default headers for API requests
export const API_HEADERS = {
  'Content-Type': 'application/json',
  Accept: 'application/json',
};

// API timeout in milliseconds
export const API_TIMEOUT = 30000;

// API endpoints
export const API_ENDPOINTS = {
  // Authentication
  LOGIN: '/api/auth/login',
  REGISTER: '/api/auth/register',
  LOGOUT: '/api/auth/logout',

  // Cases
  CASES: '/api/cases',
  CASE_DETAIL: id => `/api/cases/${id}`,
  CASE_TIMELINE: id => `/api/cases/${id}/timeline`,
  CASE_DOCUMENTS: id => `/api/cases/${id}/documents`,
  CASE_NEXT_STEPS: id => `/api/cases/${id}/next-steps`,

  // Legal AI
  LEGAL_AI_CHAT: '/api/legal-ai/chat',
  LEGAL_AI_ANALYZE: '/api/legal-ai/analyze',

  // Documents
  DOCUMENT_ANALYSIS: '/api/document-analysis/analyze',
  DOCUMENT_GENERATION: '/api/document-generator',

  // Emergency Legal Support
  EMERGENCY_AVAILABILITY: '/api/emergency-legal/availability',
  EMERGENCY_TRIAGE: '/api/emergency-legal/triage',
};

export default {
  API_BASE_URL,
  API_HEADERS,
  API_TIMEOUT,
  API_ENDPOINTS,
};
