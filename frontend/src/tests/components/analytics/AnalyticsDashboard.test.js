import React from 'react';
import { render, screen } from '@testing-library/react';
import { renderWithProviders } from '../../setup/testUtils';
import AnalyticsDashboard from '../../../components/analytics/AnalyticsDashboard';
import useRealTimeAnalytics from '../../../hooks/useRealTimeAnalytics';

// Mock the hook
jest.mock('../../../hooks/useRealTimeAnalytics');

describe('AnalyticsDashboard', () => {
  const mockFormType = 'test_form';
  const mockRealTimeData = {
    activeUsers: 5,
    recentSubmissions: [
      {
        id: 'submission-1',
        timestamp: '2024-03-21T12:00:00.000Z'
      },
      {
        id: 'submission-2',
        timestamp: '2024-03-21T12:05:00.000Z'
      }
    ],
    fieldCompletionRates: {
      'field1': 80,
      'field2': 60
    },
    errorRates: {
      'validation': 5,
      'submission': 2
    },
    averageCompletionTime: 300000 // 5 minutes in milliseconds
  };

  beforeEach(() => {
    useRealTimeAnalytics.mockReturnValue({
      realTimeData: mockRealTimeData,
      isConnected: true
    });
  });

  it('renders loading state when not connected', () => {
    useRealTimeAnalytics.mockReturnValue({
      realTimeData: {},
      isConnected: false
    });

    renderWithProviders(<AnalyticsDashboard formType={mockFormType} />);
    
    expect(screen.getByRole('progressbar')).toBeInTheDocument();
  });

  it('renders all dashboard sections when connected', () => {
    renderWithProviders(<AnalyticsDashboard formType={mockFormType} />);

    // Check metric cards
    expect(screen.getByText('Active Users')).toBeInTheDocument();
    expect(screen.getByText('5')).toBeInTheDocument();
    expect(screen.getByText('Avg. Completion Time')).toBeInTheDocument();
    expect(screen.getByText('300s')).toBeInTheDocument();

    // Check chart titles
    expect(screen.getByText('Field Completion Rates')).toBeInTheDocument();
    expect(screen.getByText('Error Distribution')).toBeInTheDocument();
    expect(screen.getByText('Recent Submissions Timeline')).toBeInTheDocument();
  });

  it('formats data correctly for charts', () => {
    renderWithProviders(<AnalyticsDashboard formType={mockFormType} />);

    // Check field completion rates
    expect(screen.getByText('field1')).toBeInTheDocument();
    expect(screen.getByText('field2')).toBeInTheDocument();

    // Check error types
    expect(screen.getByText('validation')).toBeInTheDocument();
    expect(screen.getByText('submission')).toBeInTheDocument();
  });

  it('updates when real-time data changes', () => {
    const { rerender } = renderWithProviders(
      <AnalyticsDashboard formType={mockFormType} />
    );

    // Initial check
    expect(screen.getByText('5')).toBeInTheDocument();

    // Update mock data
    useRealTimeAnalytics.mockReturnValue({
      realTimeData: {
        ...mockRealTimeData,
        activeUsers: 10
      },
      isConnected: true
    });

    // Rerender with new data
    rerender(<AnalyticsDashboard formType={mockFormType} />);

    // Check if the display updated
    expect(screen.getByText('10')).toBeInTheDocument();
  });

  it('handles empty data gracefully', () => {
    useRealTimeAnalytics.mockReturnValue({
      realTimeData: {
        activeUsers: 0,
        recentSubmissions: [],
        fieldCompletionRates: {},
        errorRates: {},
        averageCompletionTime: 0
      },
      isConnected: true
    });

    renderWithProviders(<AnalyticsDashboard formType={mockFormType} />);

    // Check if empty states are handled
    expect(screen.getByText('0')).toBeInTheDocument();
    expect(screen.getByText('0s')).toBeInTheDocument();
  });
}); 