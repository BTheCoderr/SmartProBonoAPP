import React from 'react';
import { render, screen, fireEvent, act } from '@testing-library/react';
import { axe } from 'jest-axe';
import BandwidthModeSelector from '../../components/BandwidthModeSelector';
import { I18nextProvider } from 'react-i18next';
import i18n from '../../i18n';

// Mock the bandwidth detection hook
jest.mock('../../utils/bandwidthDetection', () => ({
  useBandwidthDetection: () => ({
    isLowBandwidthMode: false,
    setLowBandwidthMode: jest.fn(),
    detectBandwidth: jest.fn(),
    isDetecting: false,
    lastChecked: new Date(),
  }),
  getOptimizedImageQuality: jest.fn().mockReturnValue('high'),
}));

describe('BandwidthModeSelector Accessibility', () => {
  // Basic setup before each test
  beforeEach(() => {
    jest.clearAllMocks();
  });

  // Test for accessibility violations
  it('should have no accessibility violations', async () => {
    const { container } = render(
      <I18nextProvider i18n={i18n}>
        <BandwidthModeSelector />
      </I18nextProvider>
    );

    // Run axe on the rendered component
    const results = await axe(container, global.axeConfig);
    expect(results).toHaveNoViolations();
  });

  // Test for keyboard navigation
  it('should be navigable with keyboard', () => {
    render(
      <I18nextProvider i18n={i18n}>
        <BandwidthModeSelector />
      </I18nextProvider>
    );

    // Find the toggle button
    const toggle = screen.getByRole('switch');

    // Check if it can receive focus
    toggle.focus();
    expect(document.activeElement).toBe(toggle);

    // Test toggle with keyboard
    fireEvent.keyDown(toggle, { key: 'Enter', code: 'Enter' });
  });

  // Test screen reader announcements
  it('should make screen reader announcements when toggle changes', () => {
    render(
      <I18nextProvider i18n={i18n}>
        <BandwidthModeSelector />
      </I18nextProvider>
    );

    // Find the announcement element
    const announcement = screen.getByRole('status', { hidden: true });
    expect(announcement).toBeInTheDocument();

    // Toggle the switch and verify announcement
    const toggle = screen.getByRole('switch');
    fireEvent.click(toggle);

    // There should be an announcement
    expect(announcement).toBeInTheDocument();
  });

  // Test focus management during operations
  it('should maintain focus during bandwidth detection', async () => {
    // Mock bandwidth detection function
    const detectBandwidthMock = jest.fn(
      () =>
        new Promise(resolve => {
          setTimeout(resolve, 100);
        })
    );

    jest.mock('../../utils/bandwidthDetection', () => ({
      ...jest.requireActual('../../utils/bandwidthDetection'),
      useBandwidthDetection: () => ({
        isLowBandwidthMode: false,
        setLowBandwidthMode: jest.fn(),
        detectBandwidth: detectBandwidthMock,
        isDetecting: false,
        lastChecked: new Date(),
      }),
    }));

    render(
      <I18nextProvider i18n={i18n}>
        <BandwidthModeSelector />
      </I18nextProvider>
    );

    // Find the detect button
    const detectButton = screen.getByText(/check connection speed/i);
    detectButton.focus();

    // Verify initial focus
    expect(document.activeElement).toBe(detectButton);

    // Click the button
    fireEvent.click(detectButton);

    // After completion, focus should be maintained
    await act(async () => {
      await new Promise(r => setTimeout(r, 150));
    });

    // Focus should return to the button
    expect(document.activeElement).toBe(detectButton);
  });

  // Test for proper ARIA attributes
  it('should have proper ARIA attributes', () => {
    render(
      <I18nextProvider i18n={i18n}>
        <BandwidthModeSelector />
      </I18nextProvider>
    );

    // Check toggle has proper aria attributes
    const toggle = screen.getByRole('switch');
    expect(toggle).toHaveAttribute('aria-checked', 'false');
    expect(toggle).toHaveAttribute('aria-describedby');

    // Check heading is properly labeled
    const heading = screen.getByRole('heading', { level: 2, hidden: true });
    expect(heading).toHaveTextContent(/bandwidth settings/i);

    // Check the features list has proper aria attributes
    const featuresList = screen.getByRole('list');
    expect(featuresList).toHaveAttribute('aria-label');
  });

  // Test compact mode accessibility
  it('should maintain accessibility in compact mode', async () => {
    const { container } = render(
      <I18nextProvider i18n={i18n}>
        <BandwidthModeSelector isCompact={true} />
      </I18nextProvider>
    );

    // Should still have a toggle with proper attributes
    const toggle = screen.getByRole('switch');
    expect(toggle).toBeInTheDocument();

    // Should not have features list in compact mode
    const featuresList = screen.queryByRole('list');
    expect(featuresList).not.toBeInTheDocument();

    // Run axe on the rendered component
    const results = await axe(container, global.axeConfig);
    expect(results).toHaveNoViolations();
  });
});
