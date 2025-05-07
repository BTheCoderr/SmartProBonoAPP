import React from 'react';
import { render } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import { ThemeProvider } from '@mui/material/styles';
import theme from '../../theme';

// Custom render function that includes providers
export const renderWithProviders = (ui, options = {}) => {
  const Wrapper = ({ children }) => (
    <BrowserRouter>
      <ThemeProvider theme={theme}>
        {children}
      </ThemeProvider>
    </BrowserRouter>
  );

  return render(ui, { wrapper: Wrapper, ...options });
};

// Mock form analytics data
export const mockAnalyticsData = {
  formStart: new Date(),
  fieldInteractions: {},
  fieldTiming: {},
  errors: [],
  completion: 0
};

// Mock API responses
export const mockApiResponses = {
  generateDocument: {
    success: {
      document_id: 'test-doc-123',
      url: 'http://example.com/test.pdf'
    },
    error: {
      message: 'Failed to generate document'
    }
  },
  saveDraft: {
    success: {
      draft_id: 'draft-123',
      timestamp: new Date().toISOString()
    },
    error: {
      message: 'Failed to save draft'
    }
  }
};

// Form test helpers
export const fillFormField = async (field, value, user) => {
  await user.type(field, value);
  await user.tab(); // Trigger blur event
};

export const submitForm = async (submitButton, user) => {
  await user.click(submitButton);
};

export const navigateToStep = async (stepNumber, user, getByText) => {
  const steps = Array.from({ length: stepNumber });
  for (let i = 0; i < steps.length; i++) {
    await user.click(getByText('Next'));
  }
}; 