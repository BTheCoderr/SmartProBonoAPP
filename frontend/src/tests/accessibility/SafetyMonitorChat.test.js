import React from 'react';
import { render, screen, fireEvent, act, waitFor } from '@testing-library/react';
import { axe } from 'jest-axe';
import SafetyMonitorChat from '../../components/SafetyMonitorChat';
import axios from 'axios';

// Mock axios
jest.mock('axios');

// Mock the Web Crypto API for encryption tests
const mockGenerateKey = jest.fn();
const mockExportKey = jest.fn();
const mockImportKey = jest.fn();
const mockEncrypt = jest.fn();
const mockDecrypt = jest.fn();

Object.defineProperty(window, 'crypto', {
  value: {
    subtle: {
      generateKey: mockGenerateKey,
      exportKey: mockExportKey,
      importKey: mockImportKey,
      encrypt: mockEncrypt,
      decrypt: mockDecrypt,
    },
    getRandomValues: jest.fn(arr => arr),
  },
});

// Mock localStorage
const localStorageMock = (() => {
  let store = {};
  return {
    getItem: jest.fn(key => store[key] || null),
    setItem: jest.fn((key, value) => {
      store[key] = value;
    }),
    removeItem: jest.fn(key => {
      delete store[key];
    }),
    clear: jest.fn(() => {
      store = {};
    }),
  };
})();
Object.defineProperty(window, 'localStorage', { value: localStorageMock });

// Mock data for tests
const mockMessages = [
  {
    text: 'Hello, how can I help you today?',
    sender: 'lawyer',
    senderId: 'lawyer123',
    senderName: 'Jane Smith',
    timestamp: '2023-05-15T14:30:00Z',
  },
  {
    text: 'I need help with my case.',
    sender: 'client',
    senderId: 'client456',
    senderName: 'John Doe',
    timestamp: '2023-05-15T14:31:00Z',
  },
  {
    text: 'Location sharing is now active.',
    sender: 'system',
    timestamp: '2023-05-15T14:32:00Z',
    isLocationUpdate: true,
  },
];

const mockClientInfo = {
  id: 'client456',
  name: 'John Doe',
  email: 'john@example.com',
};

const mockLawyerInfo = {
  id: 'lawyer123',
  name: 'Jane Smith',
  email: 'jane@example.com',
};

// Setup for each test
beforeEach(() => {
  jest.clearAllMocks();

  // Mock axios responses
  axios.get.mockImplementation(url => {
    if (url.includes('/api/safety-monitor/chat/')) {
      return Promise.resolve({ data: { messages: mockMessages } });
    }
    if (url.includes('/api/safety-monitor/status/')) {
      return Promise.resolve({
        data: {
          active_sos: false,
          location_sharing: false,
          safety_level: 'NORMAL',
        },
      });
    }
    if (url.includes('/api/safety-monitor/companion/')) {
      return Promise.resolve({ data: { companions: [] } });
    }
    return Promise.reject(new Error('Not found'));
  });

  // Mock crypto API functions
  const mockKey = { type: 'secret' };
  mockGenerateKey.mockResolvedValue(mockKey);
  mockExportKey.mockResolvedValue(new Uint8Array(32));
  mockImportKey.mockResolvedValue(mockKey);
  mockEncrypt.mockResolvedValue(new Uint8Array(32));
  mockDecrypt.mockImplementation(() => {
    const encoder = new TextEncoder();
    return Promise.resolve(encoder.encode(JSON.stringify({ text: 'Decrypted message' })));
  });
});

describe('SafetyMonitorChat Accessibility', () => {
  // Test for accessibility violations
  test('should have no accessibility violations', async () => {
    const { container } = render(
      <SafetyMonitorChat
        caseId="case123"
        clientInfo={mockClientInfo}
        onSendSOS={jest.fn()}
        onLocationShare={jest.fn()}
        onAddCompanion={jest.fn()}
      />
    );

    // Wait for messages to load
    await waitFor(() => {
      expect(screen.getByRole('log')).toBeInTheDocument();
    });

    // Run axe
    const results = await axe(container, global.axeConfig);
    expect(results).toHaveNoViolations();
  });

  // Test for keyboard navigation within the chat
  test('should support keyboard navigation', async () => {
    render(
      <SafetyMonitorChat
        caseId="case123"
        clientInfo={mockClientInfo}
        onSendSOS={jest.fn()}
        onLocationShare={jest.fn()}
        onAddCompanion={jest.fn()}
      />
    );

    // Wait for messages to load
    await waitFor(() => {
      expect(screen.getByRole('log')).toBeInTheDocument();
    });

    // Tab through the interactive elements
    const elementsInTabOrder = [
      screen.getByLabelText('Share your location'),
      screen.getByLabelText('Add emergency contacts'),
      screen.getByLabelText('Send SOS emergency alert'),
      screen.getByLabelText('Message text'),
      screen.getByLabelText('Send message'),
    ];

    // Check if tab navigation works as expected
    let currentFocus = document.activeElement;
    for (const element of elementsInTabOrder) {
      fireEvent.keyDown(currentFocus, { key: 'Tab' });
      currentFocus = document.activeElement;
      expect(currentFocus).toBeVisible();
    }

    // Test that enter key can be used to activate buttons
    const locationButton = screen.getByLabelText('Share your location');
    locationButton.focus();
    fireEvent.keyDown(locationButton, { key: 'Enter' });

    // Check if location request is made
    await waitFor(() => {
      expect(axios.post).toHaveBeenCalled();
    });
  });

  // Test screen reader announcements
  test('should make appropriate screen reader announcements', async () => {
    render(
      <SafetyMonitorChat
        caseId="case123"
        clientInfo={mockClientInfo}
        onSendSOS={jest.fn()}
        onLocationShare={jest.fn()}
        onAddCompanion={jest.fn()}
      />
    );

    // Wait for initial load announcement
    await waitFor(() => {
      const announcement = screen.getByTestId('screen-reader-announcement');
      expect(announcement).toBeInTheDocument();
    });

    // Test sending message announcement
    const inputField = screen.getByLabelText('Message text');
    const sendButton = screen.getByLabelText('Send message');

    fireEvent.change(inputField, { target: { value: 'Test message' } });
    fireEvent.click(sendButton);

    await waitFor(() => {
      const announcement = screen.getByTestId('screen-reader-announcement');
      expect(announcement).toHaveTextContent(/message sent/i);
    });
  });

  // Test for proper ARIA attributes
  test('should have proper ARIA attributes', async () => {
    render(
      <SafetyMonitorChat
        caseId="case123"
        clientInfo={mockClientInfo}
        onSendSOS={jest.fn()}
        onLocationShare={jest.fn()}
        onAddCompanion={jest.fn()}
      />
    );

    await waitFor(() => {
      expect(screen.getByRole('log')).toBeInTheDocument();
    });

    // Check for proper role assignments
    expect(screen.getByRole('region')).toHaveAttribute('aria-label', 'Safety Monitor Chat');
    expect(screen.getByRole('log')).toHaveAttribute('aria-label', 'Chat messages');
    expect(screen.getByRole('form')).toHaveAttribute('aria-label', 'Message input form');

    // Check that buttons have proper ARIA labels
    expect(screen.getByLabelText('Share your location')).toBeInTheDocument();
    expect(screen.getByLabelText('Add emergency contacts')).toBeInTheDocument();
    expect(screen.getByLabelText('Send SOS emergency alert')).toBeInTheDocument();

    // Check status elements
    const statusElements = screen.getAllByRole('status');
    expect(statusElements.length).toBeGreaterThan(0);
  });

  // Test SOS flow accessibility
  test('should maintain accessibility during SOS flow', async () => {
    render(
      <SafetyMonitorChat
        caseId="case123"
        clientInfo={mockClientInfo}
        onSendSOS={jest.fn()}
        onLocationShare={jest.fn()}
        onAddCompanion={jest.fn()}
      />
    );

    await waitFor(() => {
      expect(screen.getByRole('log')).toBeInTheDocument();
    });

    // Trigger SOS dialog
    const sosButton = screen.getByLabelText('Send SOS emergency alert');
    fireEvent.click(sosButton);

    // Check if dialog is accessible
    await waitFor(() => {
      expect(screen.getByRole('dialog')).toBeInTheDocument();
    });

    const dialog = screen.getByRole('dialog');

    // Check dialog accessibility attributes
    expect(dialog).toHaveAttribute('aria-labelledby');
    expect(dialog).toHaveAttribute('aria-describedby');

    // Dialog should trap focus - test focus trap
    const elementsInDialog = [
      screen.getByLabelText('Cancel SOS request'),
      screen.getByLabelText('Confirm and send SOS alert'),
    ];

    // Check that all interactive elements are focusable
    for (const element of elementsInDialog) {
      expect(element).toBeVisible();
      element.focus();
      expect(document.activeElement).toBe(element);
    }

    // Escape key should close dialog
    fireEvent.keyDown(dialog, { key: 'Escape' });
    await waitFor(() => {
      expect(screen.queryByRole('dialog')).not.toBeInTheDocument();
    });
  });

  // Test focus management after actions
  test('should maintain focus after operations', async () => {
    render(
      <SafetyMonitorChat
        caseId="case123"
        clientInfo={mockClientInfo}
        onSendSOS={jest.fn()}
        onLocationShare={jest.fn()}
        onAddCompanion={jest.fn()}
      />
    );

    await waitFor(() => {
      expect(screen.getByRole('log')).toBeInTheDocument();
    });

    // Test focus management after sending a message
    const inputField = screen.getByLabelText('Message text');
    const sendButton = screen.getByLabelText('Send message');

    inputField.focus();
    fireEvent.change(inputField, { target: { value: 'Test message' } });
    fireEvent.click(sendButton);

    // Focus should return to input field after sending
    await waitFor(() => {
      expect(document.activeElement).toBe(inputField);
    });
  });

  // Test with encryption enabled
  test('should maintain accessibility with encryption', async () => {
    // Mock localStorage to contain an encryption key
    localStorageMock.getItem.mockImplementation(key => {
      if (key.startsWith('chat_key_')) {
        return 'mockEncryptionKey';
      }
      return null;
    });

    const { container } = render(
      <SafetyMonitorChat
        caseId="case123"
        clientInfo={mockClientInfo}
        onSendSOS={jest.fn()}
        onLocationShare={jest.fn()}
        onAddCompanion={jest.fn()}
      />
    );

    await waitFor(() => {
      expect(screen.getByRole('log')).toBeInTheDocument();
    });

    // Check that encryption status is correctly displayed
    await waitFor(() => {
      const secureChat = screen.getByText(/secure chat/i);
      expect(secureChat).toBeInTheDocument();
    });

    // Test sending an encrypted message
    const inputField = screen.getByLabelText('Message text');
    const sendButton = screen.getByLabelText('Send message');

    fireEvent.change(inputField, { target: { value: 'Encrypted message' } });
    fireEvent.click(sendButton);

    // Should still be able to interact with the UI after sending encrypted message
    await waitFor(() => {
      expect(inputField).toHaveValue('');
    });

    // Run axe to check for accessibility violations
    const results = await axe(container, global.axeConfig);
    expect(results).toHaveNoViolations();
  });
});
