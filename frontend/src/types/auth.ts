export interface User {
  id: string;
  email: string;
  firstName: string;
  lastName: string;
  role: UserRole;
  createdAt: string;
  updatedAt: string;
}

export enum UserRole {
  CLIENT = 'CLIENT',
  LAWYER = 'LAWYER',
  ADMIN = 'ADMIN'
}

export interface AuthResponse {
  user: User;
  token: string;
  refreshToken: string;
}

export interface LoginCredentials {
  email: string;
  password: string;
}

export interface SignupCredentials extends LoginCredentials {
  firstName: string;
  lastName: string;
  role: UserRole;
}

export const AUTH_ERROR_CODES = {
  INVALID_CREDENTIALS: 'auth/invalid-credentials',
  TOKEN_EXPIRED: 'auth/token-expired',
  UNAUTHORIZED: 'auth/unauthorized',
  NETWORK_ERROR: 'auth/network-error',
  USER_NOT_FOUND: 'auth/user-not-found',
  EMAIL_IN_USE: 'auth/email-in-use',
  WEAK_PASSWORD: 'auth/weak-password',
  USER_EXISTS: 'auth/user-exists',
  VALIDATION_ERROR: 'auth/validation-error',
  UNKNOWN_ERROR: 'auth/unknown-error'
} as const;

export type AuthErrorCode = typeof AUTH_ERROR_CODES[keyof typeof AUTH_ERROR_CODES];

export class AuthError extends Error {
  constructor(
    message: string,
    public code: AuthErrorCode
  ) {
    super(message);
    this.name = 'AuthError';
  }
} 