/**
 * Protected Routes Test
 * This test file verifies the functionality of protected routes and role-based access.
 */

import React from 'react';
import { render, screen } from '@testing-library/react';
import { MemoryRouter, Route, Routes } from 'react-router-dom';
import ProtectedRoute from '../components/ProtectedRoute';
import { AuthProvider } from '../context/AuthContext';

// Mock components
const MockDashboard = () => <div>Dashboard Content</div>;
const MockLogin = () => <div>Login Page</div>;
const MockUnauthorized = () => <div>Unauthorized Page</div>;

// Mock AuthContext
jest.mock('../context/AuthContext', () => ({
  useAuth: jest.fn(),
  AuthProvider: ({ children }) => <div>{children}</div>
}));

describe('Protected Routes', () => {
  const mockUseAuth = require('../context/AuthContext').useAuth;
  
  afterEach(() => {
    jest.clearAllMocks();
  });
  
  test('redirects to login when user is not authenticated', () => {
    // Mock unauthenticated user
    mockUseAuth.mockReturnValue({
      user: null,
      isAuthenticated: false,
      loading: false
    });
    
    render(
      <MemoryRouter initialEntries={['/dashboard']}>
        <Routes>
          <Route path="/login" element={<MockLogin />} />
          <Route element={<ProtectedRoute />}>
            <Route path="/dashboard" element={<MockDashboard />} />
          </Route>
        </Routes>
      </MemoryRouter>
    );
    
    // Should redirect to login
    expect(screen.getByText('Login Page')).toBeInTheDocument();
  });
  
  test('allows access to protected route when user is authenticated', () => {
    // Mock authenticated user
    mockUseAuth.mockReturnValue({
      user: { id: '123', role: 'user' },
      isAuthenticated: true,
      loading: false
    });
    
    render(
      <MemoryRouter initialEntries={['/dashboard']}>
        <Routes>
          <Route path="/login" element={<MockLogin />} />
          <Route element={<ProtectedRoute />}>
            <Route path="/dashboard" element={<MockDashboard />} />
          </Route>
        </Routes>
      </MemoryRouter>
    );
    
    // Should show dashboard content
    expect(screen.getByText('Dashboard Content')).toBeInTheDocument();
  });
  
  test('shows loading indicator while checking auth status', () => {
    // Mock loading state
    mockUseAuth.mockReturnValue({
      user: null,
      isAuthenticated: false,
      loading: true
    });
    
    render(
      <MemoryRouter initialEntries={['/dashboard']}>
        <Routes>
          <Route path="/login" element={<MockLogin />} />
          <Route element={<ProtectedRoute />}>
            <Route path="/dashboard" element={<MockDashboard />} />
          </Route>
        </Routes>
      </MemoryRouter>
    );
    
    // Should show loading indicator
    expect(screen.getByText('Verifying Authentication...')).toBeInTheDocument();
  });
  
  test('redirects to unauthorized page when user does not have required role', () => {
    // Mock authenticated user with insufficient role
    mockUseAuth.mockReturnValue({
      user: { id: '123', role: 'user' },
      isAuthenticated: true,
      loading: false
    });
    
    render(
      <MemoryRouter initialEntries={['/admin']}>
        <Routes>
          <Route path="/unauthorized" element={<MockUnauthorized />} />
          <Route element={<ProtectedRoute requiredRole="admin" />}>
            <Route path="/admin" element={<div>Admin Dashboard</div>} />
          </Route>
        </Routes>
      </MemoryRouter>
    );
    
    // Should redirect to unauthorized page
    expect(screen.getByText('Unauthorized Page')).toBeInTheDocument();
  });
  
  test('allows access when user has required role', () => {
    // Mock authenticated user with correct role
    mockUseAuth.mockReturnValue({
      user: { id: '123', role: 'admin' },
      isAuthenticated: true,
      loading: false
    });
    
    render(
      <MemoryRouter initialEntries={['/admin']}>
        <Routes>
          <Route path="/unauthorized" element={<MockUnauthorized />} />
          <Route element={<ProtectedRoute requiredRole="admin" />}>
            <Route path="/admin" element={<div>Admin Dashboard</div>} />
          </Route>
        </Routes>
      </MemoryRouter>
    );
    
    // Should show admin dashboard
    expect(screen.getByText('Admin Dashboard')).toBeInTheDocument();
  });
}); 