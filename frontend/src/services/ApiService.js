import axios from 'axios';
import config from '../config';

class ApiService {
  constructor() {
    this.client = axios.create({
      baseURL: config.baseURL,
      timeout: config.timeout,
      headers: config.headers,
      withCredentials: config.withCredentials
    });

    // Add request interceptor for auth token
    this.client.interceptors.request.use(
      (config) => {
        const token = localStorage.getItem('access_token');
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      },
      (error) => Promise.reject(error)
    );

    // Add response interceptor for error handling
    this.client.interceptors.response.use(
      (response) => response,
      async (error) => {
        // If the error doesn't have a response, pass it through
        if (!error.response) {
          return Promise.reject(error);
        }
        
        // If the error is related to authorization and we're not on the auth routes
        if (error.response.status === 401 && 
            !error.config.url.includes('/api/auth/login') && 
            !error.config.url.includes('/api/auth/refresh')) {
          
          // Dispatch an event for the auth provider to handle
          const authErrorEvent = new CustomEvent('auth:error', { 
            detail: { 
              status: error.response.status,
              message: error.response.data?.message || 'Authentication required'
            } 
          });
          window.dispatchEvent(authErrorEvent);
        }
        
        return Promise.reject(error);
      }
    );
  }

  // HTTP methods
  async get(url, config = {}) {
    return this.client.get(url, config);
  }

  async post(url, data = {}, config = {}) {
    return this.client.post(url, data, config);
  }

  async put(url, data = {}, config = {}) {
    return this.client.put(url, data, config);
  }

  async patch(url, data = {}, config = {}) {
    return this.client.patch(url, data, config);
  }

  async delete(url, config = {}) {
    return this.client.delete(url, config);
  }

  // Auth specific methods
  async login(credentials) {
    try {
      const response = await this.post('/api/auth/login', credentials);
      this.handleAuthResponse(response.data);
      return response.data;
    } catch (error) {
      throw error;
    }
  }

  async register(userData) {
    try {
      const response = await this.post('/api/auth/register', userData);
      this.handleAuthResponse(response.data);
      return response.data;
    } catch (error) {
      throw error;
    }
  }

  async logout() {
    try {
      await this.post('/api/auth/logout');
      this.clearAuth();
    } catch (error) {
      // Still clear auth data locally even if server request fails
      this.clearAuth();
      throw error;
    }
  }

  async refreshToken() {
    try {
      const refreshToken = localStorage.getItem('refresh_token');
      if (!refreshToken) {
        throw new Error('No refresh token available');
      }
      
      // Create a separate axios instance to avoid interceptors
      const refreshClient = axios.create({
        baseURL: config.baseURL,
        timeout: config.timeout
      });
      
      const response = await refreshClient.post('/api/auth/refresh', {}, {
        headers: { Authorization: `Bearer ${refreshToken}` }
      });
      
      // Update stored token
      localStorage.setItem('access_token', response.data.access_token);
      
      return response.data.access_token;
    } catch (error) {
      this.clearAuth();
      throw error;
    }
  }

  // Helper methods
  handleAuthResponse(data) {
    if (data.access_token) {
      localStorage.setItem('access_token', data.access_token);
    }
    
    if (data.refresh_token) {
      localStorage.setItem('refresh_token', data.refresh_token);
    }
  }

  clearAuth() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
  }

  // User methods
  async getCurrentUser() {
    const response = await this.get('/api/users/me');
    return response.data;
  }

  async updateProfile(userData) {
    const response = await this.put('/api/users/profile', userData);
    return response.data;
  }

  // Document methods
  async uploadDocument(formData) {
    const response = await this.post('/api/documents/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  }

  async getDocuments() {
    const response = await this.get('/api/documents');
    return response.data;
  }

  // Form submission methods
  async submitForm(formType, formData) {
    const response = await this.post(`/api/forms/${formType}/submit`, formData);
    return response.data;
  }

  async saveDraft(formType, draftData) {
    const response = await this.post(`/api/forms/${formType}/draft`, draftData);
    return response.data;
  }

  async getDraft(formType) {
    const response = await this.get(`/api/forms/${formType}/draft`);
    return response.data;
  }

  async generateDocument(formType, formData) {
    const response = await this.post(`/api/forms/${formType}/generate`, formData);
    return response.data;
  }

  // PDF methods
  async generatePDF(templateId, data) {
    const response = await this.post('/api/documents/generate', {
      template_id: templateId,
      data: data
    }, { responseType: 'blob' });
    return response.data;
  }

  async downloadPDF(documentId) {
    const response = await this.get(`/api/documents/${documentId}/download`, {
      responseType: 'blob'
    });
    return response.data;
  }

  async previewPDF(templateId, data) {
    const response = await this.post('/api/documents/preview', {
      template_id: templateId,
      data: data
    }, { responseType: 'blob' });
    return response.data;
  }

  // Error handler
  handleError(error) {
    if (error.response) {
      // Server responded with error
      return error.response.data.message || config.errors.server;
    } else if (error.request) {
      // No response received
      return config.errors.network;
    } else {
      // Request setup error
      return config.errors.server;
    }
  }
}

// Create and export a singleton instance
export default new ApiService(); 