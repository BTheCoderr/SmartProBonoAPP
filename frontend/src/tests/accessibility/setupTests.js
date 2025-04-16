/**
 * Jest setup file for accessibility testing
 * Configures axe-core for automated accessibility testing
 */

import '@testing-library/jest-dom';
import { toHaveNoViolations } from 'jest-axe';
import { configure } from '@testing-library/react';

// Add custom jest matchers from jest-axe
expect.extend(toHaveNoViolations);

// Configure testing-library
configure({
  // Wait for ui to settle before considering element queries complete
  asyncUtilTimeout: 5000,
  // Show more detailed info in testing-library error reports
  getElementError: (message, container) => {
    const error = new Error(message);
    error.container = container;
    error.name = 'TestingLibraryElementError';
    return error;
  },
});

// Mock scrollIntoView since it's not implemented in JSDOM
if (typeof window !== 'undefined') {
  window.HTMLElement.prototype.scrollIntoView = function () {};
  window.scrollTo = jest.fn();

  // Mock speechSynthesis API
  if (!window.speechSynthesis) {
    window.speechSynthesis = {
      speak: jest.fn(),
      cancel: jest.fn(),
      pause: jest.fn(),
      resume: jest.fn(),
      getVoices: jest.fn().mockReturnValue([]),
    };

    window.SpeechSynthesisUtterance = jest.fn().mockImplementation(text => ({
      text,
      lang: 'en-US',
      voice: null,
      volume: 1,
      rate: 1,
      pitch: 1,
    }));
  }

  // Mock ResizeObserver
  if (!window.ResizeObserver) {
    window.ResizeObserver = jest.fn().mockImplementation(() => ({
      observe: jest.fn(),
      unobserve: jest.fn(),
      disconnect: jest.fn(),
    }));
  }

  // Mock Intersection Observer
  if (!window.IntersectionObserver) {
    window.IntersectionObserver = jest.fn().mockImplementation(() => ({
      observe: jest.fn(),
      unobserve: jest.fn(),
      disconnect: jest.fn(),
    }));
  }
}

// Global constants for accessibility tests
global.AXE_TIMEOUT = 10000; // Timeout for axe tests in milliseconds

// Default axe configuration for all tests
global.axeConfig = {
  rules: {
    // Enable specific rules that might be disabled by default
    'color-contrast': { enabled: true },
    'document-title': { enabled: true },
    'html-has-lang': { enabled: true },
    'landmark-one-main': { enabled: true },
    'page-has-heading-one': { enabled: true },
    'scrollable-region-focusable': { enabled: true },
  },
  // Exclude certain components from specific tests if needed
  exclude: [
    // Format: [selector, selector, ...]
    // Example: Exclude code syntax highlighting which might have issues with color contrast
    '.prism-code',
    '[aria-hidden="true"]',
  ],
};

// Utility for checking if a test is running in CI environment
global.isCI = !!process.env.CI;

// Configure console to handle test logs
const originalError = console.error;
const originalWarn = console.warn;

// Filter out known issues to reduce noise in test output
console.error = (...args) => {
  // React 18 strict mode related warnings
  if (
    args[0] &&
    typeof args[0] === 'string' &&
    (args[0].includes('ReactDOM.render is no longer supported') ||
      args[0].includes('Warning: An update to') ||
      args[0].includes('Warning: validateDOMNesting'))
  ) {
    return;
  }
  originalError.apply(console, args);
};

console.warn = (...args) => {
  // Filter out react-axe warnings during test runs
  if (args[0] && typeof args[0] === 'string' && args[0].includes('react-axe')) {
    return;
  }
  originalWarn.apply(console, args);
};
