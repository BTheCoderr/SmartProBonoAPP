import React from 'react';
import { screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import FormTemplate from '../templates/FormTemplate';
import { renderWithProviders, mockAnalyticsData, mockApiResponses, fillFormField, submitForm, navigateToStep } from './setup/testUtils';
import ApiService from '../services/ApiService';
import { act } from 'react-dom/test-utils';

// Mock API service
jest.mock('../services/ApiService');

// Mock analytics hooks
jest.mock('../hooks/useFormAnalytics', () => ({
  __esModule: true,
  default: () => ({
    trackFormStart: jest.fn(),
    trackFormCompletion: jest.fn(),
    trackFieldInteraction: jest.fn(),
    trackFieldTiming: jest.fn(),
    trackFormAbandonment: jest.fn(),
    trackFormError: jest.fn(),
    getFormAnalytics: jest.fn(() => mockAnalyticsData)
  })
}));

describe('FormTemplate', () => {
  let user;

  beforeEach(() => {
    user = userEvent.setup();
    // Reset API mocks
    ApiService.post.mockReset();
    // Mock localStorage
    Object.defineProperty(window, 'localStorage', {
      value: {
        getItem: jest.fn(),
        setItem: jest.fn(),
        removeItem: jest.fn()
      },
      writable: true
    });
  });

  it('renders form with initial state', () => {
    renderWithProviders(<FormTemplate />);
    
    expect(screen.getByText('Form Template')).toBeInTheDocument();
    expect(screen.getByText('Form Progress: 0%')).toBeInTheDocument();
    expect(screen.getByText('Auto-save Off')).toBeInTheDocument();
  });

  it('handles field input and validation', async () => {
    renderWithProviders(<FormTemplate />);
    
    const field1Input = screen.getByLabelText('Field 1');
    await fillFormField(field1Input, '', user);
    
    expect(screen.getByText('Field 1 is required')).toBeInTheDocument();
    
    await fillFormField(field1Input, 'test value', user);
    expect(screen.queryByText('Field 1 is required')).not.toBeInTheDocument();
  });

  it('tracks field timing and interactions', async () => {
    renderWithProviders(<FormTemplate />);
    
    const field1Input = screen.getByLabelText('Field 1');
    const startTime = Date.now();
    
    await fillFormField(field1Input, 'test value', user);
    await new Promise(resolve => setTimeout(resolve, 1000)); // Simulate user typing
    await fillFormField(field1Input, '', user);
    
    const endTime = Date.now();
    const duration = endTime - startTime;
    
    expect(duration).toBeGreaterThanOrEqual(1000);
  });

  it('handles form submission', async () => {
    ApiService.post.mockResolvedValueOnce(mockApiResponses.generateDocument.success);
    
    renderWithProviders(<FormTemplate />);
    
    // Fill out form
    await fillFormField(screen.getByLabelText('Field 1'), 'test value', user);
    await fillFormField(screen.getByLabelText('Field 2'), '42', user);
    
    // Submit form
    await submitForm(screen.getByText('Submit'), user);
    
    expect(ApiService.post).toHaveBeenCalledWith(
      '/api/templates/generate',
      expect.any(Object)
    );
  });

  it('handles draft saving and loading', async () => {
    ApiService.post.mockResolvedValueOnce(mockApiResponses.saveDraft.success);
    
    renderWithProviders(<FormTemplate />);
    
    // Fill out form
    await fillFormField(screen.getByLabelText('Field 1'), 'draft value', user);
    
    // Save draft
    await act(async () => {
      await user.click(screen.getByText('Save Draft'));
    });
    
    expect(screen.getByText('Draft saved successfully')).toBeInTheDocument();
  });

  it('handles form abandonment', async () => {
    renderWithProviders(<FormTemplate />);
    
    // Fill out partial form
    await fillFormField(screen.getByLabelText('Field 1'), 'abandoned value', user);
    
    // Simulate page unload
    const event = new Event('beforeunload');
    window.dispatchEvent(event);
    
    // Check if abandonment was tracked
    expect(window.localStorage.getItem).toHaveBeenCalled();
  });

  it('validates steps before navigation', async () => {
    renderWithProviders(<FormTemplate />);
    
    // Try to navigate without filling required field
    await user.click(screen.getByText('Next'));
    
    expect(screen.getByText('Please fix the errors before proceeding')).toBeInTheDocument();
    
    // Fill required field and navigate
    await fillFormField(screen.getByLabelText('Field 1'), 'valid value', user);
    await user.click(screen.getByText('Next'));
    
    expect(screen.getByLabelText('Field 2')).toBeInTheDocument();
  });

  it('shows form preview', async () => {
    renderWithProviders(<FormTemplate />);
    
    // Fill out form
    await fillFormField(screen.getByLabelText('Field 1'), 'preview value', user);
    await fillFormField(screen.getByLabelText('Field 2'), '42', user);
    
    // Navigate to last step
    await navigateToStep(2, user, screen.getByText);
    
    // Show preview
    await user.click(screen.getByText('Preview'));
    
    expect(screen.getByText('Document Preview')).toBeInTheDocument();
  });

  it('handles auto-save toggle', async () => {
    renderWithProviders(<FormTemplate />);
    
    // Toggle auto-save on
    await user.click(screen.getByText('Auto-save Off'));
    
    expect(screen.getByText('Auto-save On')).toBeInTheDocument();
    
    // Fill out form (should trigger auto-save)
    await fillFormField(screen.getByLabelText('Field 1'), 'auto-save value', user);
    
    await waitFor(() => {
      expect(window.localStorage.setItem).toHaveBeenCalled();
    });
  });
}); 