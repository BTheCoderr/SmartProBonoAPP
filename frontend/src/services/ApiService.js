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
        const token = localStorage.getItem('auth_token');
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
        if (error.response?.status === 401) {
          // Handle token refresh or logout
          localStorage.removeItem('auth_token');
          window.location.href = '/login';
        }
        return Promise.reject(error);
      }
    );
  }

  // Auth methods
  async login(credentials) {
    const response = await this.client.post('/api/auth/login', credentials);
    return response.data;
  }

  async register(userData) {
    const response = await this.client.post('/api/auth/register', userData);
    return response.data;
  }

  async logout() {
    const response = await this.client.post('/api/auth/logout');
    localStorage.removeItem('auth_token');
    return response.data;
  }

  // User methods
  async getCurrentUser() {
    const response = await this.client.get('/api/users/me');
    return response.data;
  }

  async updateProfile(userData) {
    const response = await this.client.put('/api/users/profile', userData);
    return response.data;
  }

  // Document methods
  async uploadDocument(formData) {
    const response = await this.client.post('/api/documents/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  }

  async getDocuments() {
    const response = await this.client.get('/api/documents');
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

// Export singleton instance
const apiService = new ApiService();
export default apiService; 