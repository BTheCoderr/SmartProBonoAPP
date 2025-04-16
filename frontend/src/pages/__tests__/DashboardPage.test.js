import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { ChakraProvider } from '@chakra-ui/react';
import DashboardPage from '../DashboardPage';

// Mock the recharts components
jest.mock('recharts', () => ({
  ResponsiveContainer: ({ children }) => <div>{children}</div>,
  BarChart: ({ children }) => <div>{children}</div>,
  Bar: () => <div>Bar</div>,
  XAxis: () => <div>XAxis</div>,
  YAxis: () => <div>YAxis</div>,
  CartesianGrid: () => <div>CartesianGrid</div>,
  Tooltip: () => <div>Tooltip</div>,
  Legend: () => <div>Legend</div>,
  PieChart: ({ children }) => <div>{children}</div>,
  Pie: () => <div>Pie</div>,
  Cell: () => <div>Cell</div>,
}));

describe('DashboardPage', () => {
  beforeEach(() => {
    // Reset any mocks if needed
  });

  afterEach(() => {
    jest.clearAllMocks();
  });

  it('renders dashboard with metrics', async () => {
    render(
      <ChakraProvider>
        <DashboardPage />
      </ChakraProvider>
    );

    await waitFor(() => {
      expect(screen.getByText('Dashboard')).toBeInTheDocument();
      expect(screen.getByText('Total Cases')).toBeInTheDocument();
      expect(screen.getByText('Active Cases')).toBeInTheDocument();
      expect(screen.getByText('Closed Cases')).toBeInTheDocument();
      expect(screen.getByText('Avg. Resolution Time')).toBeInTheDocument();
    });

    // Check if metrics are displayed
    expect(screen.getByText('150')).toBeInTheDocument(); // Total Cases
    expect(screen.getByText('45')).toBeInTheDocument(); // Active Cases
    expect(screen.getByText('105')).toBeInTheDocument(); // Closed Cases
    expect(screen.getByText('15 days')).toBeInTheDocument(); // Avg Resolution Time
  });

  it('handles time range changes', async () => {
    render(
      <ChakraProvider>
        <DashboardPage />
      </ChakraProvider>
    );

    const timeRangeSelect = screen.getByRole('combobox');
    fireEvent.change(timeRangeSelect, { target: { value: 'week' } });

    await waitFor(() => {
      expect(timeRangeSelect.value).toBe('week');
    });
  });

  it('displays charts and tables', async () => {
    render(
      <ChakraProvider>
        <DashboardPage />
      </ChakraProvider>
    );

    await waitFor(() => {
      expect(screen.getByText('Cases by Type')).toBeInTheDocument();
      expect(screen.getByText('Cases by Status')).toBeInTheDocument();
      expect(screen.getByText('Case Trend')).toBeInTheDocument();
      expect(screen.getByText('Top Performing Attorneys')).toBeInTheDocument();
    });

    // Check if attorney data is displayed
    expect(screen.getByText('John Doe')).toBeInTheDocument();
    expect(screen.getByText('92%')).toBeInTheDocument();
  });

  it('calculates trends correctly', async () => {
    render(
      <ChakraProvider>
        <DashboardPage />
      </ChakraProvider>
    );

    await waitFor(() => {
      // Total Cases trend: (150 - 140) / 140 * 100 = 7.1%
      expect(screen.getByText('7.1%')).toBeInTheDocument();
    });
  });

  it('displays loading state', () => {
    render(
      <ChakraProvider>
        <DashboardPage />
      </ChakraProvider>
    );

    expect(screen.getByText('Loading...')).toBeInTheDocument();
  });

  it('handles error state', async () => {
    // Mock console.error to prevent error logging during test
    const originalError = console.error;
    console.error = jest.fn();

    // Force an error state
    jest.spyOn(global, 'fetch').mockRejectedValueOnce(new Error('Failed to fetch'));

    render(
      <ChakraProvider>
        <DashboardPage />
      </ChakraProvider>
    );

    await waitFor(() => {
      expect(screen.getByText('Error')).toBeInTheDocument();
      expect(screen.getByText('Failed to fetch dashboard data')).toBeInTheDocument();
    });

    // Restore console.error
    console.error = originalError;
  });

  it('displays correct badge colors for success rates', async () => {
    render(
      <ChakraProvider>
        <DashboardPage />
      </ChakraProvider>
    );

    await waitFor(() => {
      const badges = screen.getAllByText(/%/);
      expect(badges[0]).toHaveStyle({ backgroundColor: expect.stringContaining('green') });
      expect(badges[1]).toHaveStyle({ backgroundColor: expect.stringContaining('orange') });
    });
  });
});
