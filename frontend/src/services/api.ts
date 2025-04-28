import axios, { AxiosInstance, AxiosError, AxiosRequestConfig } from 'axios';
import config from '../config';

class ApiService {
  private static instance: ApiService;
  private api: AxiosInstance;
  private requestCount: number = 0;
  private lastWindowStart: number = Date.now();

  private constructor() {
    this.api = axios.create({
      baseURL: config.api.baseURL,
      timeout: config.api.timeout,
      headers: config.api.headers,
      withCredentials: config.api.withCredentials,
    });

    this.setupInterceptors();
  }

  public static getInstance(): ApiService {
    if (!ApiService.instance) {
      ApiService.instance = new ApiService();
    }
    return ApiService.instance;
  }

  private setupInterceptors(): void {
    // Request Interceptor
    this.api.interceptors.request.use(
      async (axiosConfig) => {
        // Rate Limiting
        if (!this.checkRateLimit()) {
          throw new Error('Rate limit exceeded. Please try again later.');
        }

        // Add Auth Token
        const token = localStorage.getItem(config.security.tokenKey);
        if (token) {
          axiosConfig.headers = axiosConfig.headers || {};
          axiosConfig.headers.Authorization = `${config.security.tokenPrefix} ${token}`;
        }

        // Add CSRF Token if available
        const csrfToken = document.querySelector('meta[name="csrf-token"]')?.getAttribute('content');
        if (csrfToken) {
          axiosConfig.headers = axiosConfig.headers || {};
          axiosConfig.headers[config.security.csrfHeaderName] = csrfToken;
        }

        return axiosConfig;
      },
      (error) => Promise.reject(this.handleError(error))
    );

    // Response Interceptor
    this.api.interceptors.response.use(
      (response) => response,
      async (error) => {
        const originalRequest = error.config;

        // Handle token refresh
        if (error.response?.status === 401 && !originalRequest._retry) {
          originalRequest._retry = true;
          try {
            const refreshToken = localStorage.getItem(config.security.refreshTokenKey);
            const response = await this.api.post('/auth/refresh', { refreshToken });
            const { token } = response.data;
            localStorage.setItem(config.security.tokenKey, token);
            originalRequest.headers = originalRequest.headers || {};
            originalRequest.headers.Authorization = `${config.security.tokenPrefix} ${token}`;
            return this.api(originalRequest);
          } catch (refreshError) {
            return Promise.reject(this.handleError(refreshError));
          }
        }

        return Promise.reject(this.handleError(error));
      }
    );
  }

  private checkRateLimit(): boolean {
    const now = Date.now();
    if (now - this.lastWindowStart >= config.rateLimit.perWindow) {
      this.requestCount = 0;
      this.lastWindowStart = now;
    }

    this.requestCount++;
    return this.requestCount <= config.rateLimit.maxRequests;
  }

  private handleError(error: AxiosError): Error {
    if (error.response) {
      switch (error.response.status) {
        case 401:
          return new Error(config.errors.unauthorized);
        case 403:
          return new Error(config.errors.forbidden);
        case 404:
          return new Error(config.errors.notFound);
        case 422:
          return new Error(config.errors.validation);
        default:
          return new Error(config.errors.server);
      }
    }

    if (error.request) {
      if (error.code === 'ECONNABORTED') {
        return new Error(config.errors.timeout);
      }
      return new Error(config.errors.network);
    }

    return error;
  }

  // API Methods
  public async get<T>(url: string, config?: AxiosRequestConfig): Promise<T> {
    try {
      const response = await this.api.get<T>(url, config);
      return response.data;
    } catch (error) {
      throw this.handleError(error as AxiosError);
    }
  }

  public async post<T>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> {
    try {
      const response = await this.api.post<T>(url, data, config);
      return response.data;
    } catch (error) {
      throw this.handleError(error as AxiosError);
    }
  }

  public async put<T>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> {
    try {
      const response = await this.api.put<T>(url, data, config);
      return response.data;
    } catch (error) {
      throw this.handleError(error as AxiosError);
    }
  }

  public async delete<T>(url: string, config?: AxiosRequestConfig): Promise<T> {
    try {
      const response = await this.api.delete<T>(url, config);
      return response.data;
    } catch (error) {
      throw this.handleError(error as AxiosError);
    }
  }

  // Specialized API Methods for Legal Services
  public async generateLegalDocument(templateId: string, data: any): Promise<string> {
    try {
      const response = await this.post<{ documentUrl: string }>('/api/documents/generate', {
        templateId,
        data,
      });
      return response.documentUrl;
    } catch (error) {
      throw this.handleError(error as AxiosError);
    }
  }

  public async getLegalAdvice(query: string): Promise<any> {
    try {
      const response = await this.post<any>('/api/legal-chat/advice', { query });
      return response;
    } catch (error) {
      throw this.handleError(error as AxiosError);
    }
  }

  public async uploadDocument(file: File, metadata: any): Promise<any> {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('metadata', JSON.stringify(metadata));

    try {
      const response = await this.post<any>('/api/documents/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      return response;
    } catch (error) {
      throw this.handleError(error as AxiosError);
    }
  }
}

export default ApiService.getInstance(); 