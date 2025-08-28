/**
 * Form Submission Workflow Test
 * This test validates the client intake form submission workflow.
 */

import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { MemoryRouter } from 'react-router-dom';
import ImmigrationIntakeForm from '../components/ImmigrationIntakeForm';
import { useAuth } from '../context/AuthContext';
import ApiService from '../services/ApiService';
import { SnackbarProvider } from 'notistack';

// Mock dependencies
jest.mock('../context/AuthContext', () => ({
  useAuth: jest.fn()
}));

jest.mock('../services/ApiService', () => ({
  post: jest.fn()
}));

jest.mock('react-router-dom', () => ({
  ...jest.requireActual('react-router-dom'),
  useNavigate: () => jest.fn()
}));

jest.mock('notistack', () => ({
  useSnackbar: () => ({
    enqueueSnackbar: jest.fn()
  }),
  SnackbarProvider: ({ children }) => <div>{children}</div>
}));

describe('ImmigrationIntakeForm Workflow', () => {
  const mockAuth = {
    accessToken: 'test-token',
    user: {
      id: '123',
      email: 'test@example.com',
      firstName: 'Test',
      lastName: 'User'
    }
  };

  beforeEach(() => {
    useAuth.mockReturnValue(mockAuth);
    ApiService.post.mockReset();
  });

  test('form can be filled and submitted with valid data', async () => {
    // Mock successful API response
    ApiService.post.mockResolvedValueOnce({
      success: true,
      id: 'intake-123',
      case_id: 'case-456'
    });

    render(
      <MemoryRouter>
        <SnackbarProvider>
          <ImmigrationIntakeForm />
        </SnackbarProvider>
      </MemoryRouter>
    );

    // Step 1: Personal Information
    await waitFor(() => screen.getByLabelText(/First Name/i));
    fireEvent.change(screen.getByLabelText(/First Name/i), { target: { value: 'John' } });
    fireEvent.change(screen.getByLabelText(/Last Name/i), { target: { value: 'Doe' } });
    fireEvent.change(screen.getByLabelText(/Email/i), { target: { value: 'john.doe@example.com' } });
    fireEvent.change(screen.getByLabelText(/Phone/i), { target: { value: '123-456-7890' } });
    
    // Click Next to move to Step 2
    fireEvent.click(screen.getByRole('button', { name: /Next/i }));

    // Step 2: Immigration Information
    await waitFor(() => screen.getByLabelText(/Current Immigration Status/i));
    fireEvent.change(screen.getByLabelText(/Current Immigration Status/i), { target: { value: 'H1B' } });
    fireEvent.change(screen.getByLabelText(/Country of Origin/i), { target: { value: 'Canada' } });
    
    // Click Next to move to Step 3
    fireEvent.click(screen.getByRole('button', { name: /Next/i }));

    // Step 3: Legal Issue
    await waitFor(() => screen.getByLabelText(/Describe Your Legal Issue/i));
    fireEvent.change(screen.getByLabelText(/Describe Your Legal Issue/i), { 
      target: { value: 'I need help with visa extension.' } 
    });
    
    // Select urgency
    const urgencySelect = screen.getByLabelText(/urgency/i);
    fireEvent.change(urgencySelect, { target: { value: 'high' } });
    
    // Submit the form
    fireEvent.click(screen.getByRole('button', { name: /Submit/i }));

    // Verify API was called with correct data
    await waitFor(() => {
      expect(ApiService.post).toHaveBeenCalledTimes(1);
      expect(ApiService.post).toHaveBeenCalledWith('/api/intake/immigration', expect.objectContaining({
        firstName: 'John',
        lastName: 'Doe',
        email: 'john.doe@example.com',
        urgency: 'high'
      }));
    });
  });

  test('form shows validation errors for required fields', async () => {
    render(
      <MemoryRouter>
        <SnackbarProvider>
          <ImmigrationIntakeForm />
        </SnackbarProvider>
      </MemoryRouter>
    );

    // Try to proceed without filling required fields
    fireEvent.click(screen.getByRole('button', { name: /Next/i }));

    // Check for validation errors
    await waitFor(() => {
      expect(screen.getByText(/first name is required/i)).toBeInTheDocument();
      expect(screen.getByText(/last name is required/i)).toBeInTheDocument();
      expect(screen.getByText(/email is required/i)).toBeInTheDocument();
    });
  });

  test('form handles API errors gracefully', async () => {
    // Mock API error
    ApiService.post.mockRejectedValueOnce({
      message: 'Server error processing form'
    });

    render(
      <MemoryRouter>
        <SnackbarProvider>
          <ImmigrationIntakeForm />
        </SnackbarProvider>
      </MemoryRouter>
    );

    // Fill out all steps
    // Step 1
    await waitFor(() => screen.getByLabelText(/First Name/i));
    fireEvent.change(screen.getByLabelText(/First Name/i), { target: { value: 'John' } });
    fireEvent.change(screen.getByLabelText(/Last Name/i), { target: { value: 'Doe' } });
    fireEvent.change(screen.getByLabelText(/Email/i), { target: { value: 'john.doe@example.com' } });
    fireEvent.change(screen.getByLabelText(/Phone/i), { target: { value: '123-456-7890' } });
    fireEvent.click(screen.getByRole('button', { name: /Next/i }));

    // Step 2
    await waitFor(() => screen.getByLabelText(/Current Immigration Status/i));
    fireEvent.change(screen.getByLabelText(/Current Immigration Status/i), { target: { value: 'H1B' } });
    fireEvent.change(screen.getByLabelText(/Country of Origin/i), { target: { value: 'Canada' } });
    fireEvent.click(screen.getByRole('button', { name: /Next/i }));

    // Step 3
    await waitFor(() => screen.getByLabelText(/Describe Your Legal Issue/i));
    fireEvent.change(screen.getByLabelText(/Describe Your Legal Issue/i), { 
      target: { value: 'I need help with visa extension.' } 
    });
    
    // Submit form
    fireEvent.click(screen.getByRole('button', { name: /Submit/i }));

    // Verify error was handled
    await waitFor(() => {
      expect(ApiService.post).toHaveBeenCalledTimes(1);
    });
  });
}); 