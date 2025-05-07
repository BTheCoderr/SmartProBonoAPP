import axios from 'axios';
import { 
  AuthResponse, 
  LoginCredentials, 
  SignupCredentials, 
  AuthError,
  AUTH_ERROR_CODES 
} from '../types/auth';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

const handleAuthError = (error: any): never => {
  if (axios.isAxiosError(error)) {
    const status = error.response?.status;
    const message = error.response?.data?.message || error.message;

    switch (status) {
      case 401:
        throw new AuthError(message, AUTH_ERROR_CODES.INVALID_CREDENTIALS);
      case 409:
        throw new AuthError(message, AUTH_ERROR_CODES.USER_EXISTS);
      case 422:
        throw new AuthError(message, AUTH_ERROR_CODES.VALIDATION_ERROR);
      default:
        throw new AuthError(message, AUTH_ERROR_CODES.NETWORK_ERROR);
    }
  }
  throw new AuthError('An unexpected error occurred', AUTH_ERROR_CODES.UNKNOWN_ERROR);
};

export const login = async (credentials: LoginCredentials): Promise<AuthResponse> => {
  try {
    const response = await axios.post<AuthResponse>(
      `${API_URL}/api/auth/login`,
      credentials
    );
    return response.data;
  } catch (error) {
    throw handleAuthError(error);
  }
};

export const signup = async (credentials: SignupCredentials): Promise<AuthResponse> => {
  try {
    const response = await axios.post<AuthResponse>(
      `${API_URL}/api/auth/signup`,
      credentials
    );
    return response.data;
  } catch (error) {
    throw handleAuthError(error);
  }
};

export const logout = async (): Promise<void> => {
  try {
    const token = localStorage.getItem('token');
    await axios.post(
      `${API_URL}/api/auth/logout`,
      {},
      {
        headers: {
          Authorization: `Bearer ${token}`
        }
      }
    );
  } catch (error) {
    throw handleAuthError(error);
  }
};

export const refreshToken = async (): Promise<AuthResponse> => {
  try {
    const refreshToken = localStorage.getItem('refreshToken');
    const response = await axios.post<AuthResponse>(
      `${API_URL}/api/auth/refresh`,
      { refreshToken }
    );
    return response.data;
  } catch (error) {
    throw handleAuthError(error);
  }
}; 