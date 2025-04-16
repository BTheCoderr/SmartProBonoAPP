import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { ChakraProvider } from '@chakra-ui/react';
import { BrowserRouter } from 'react-router-dom';
import CaseListPage from '../CaseListPage';
import { getAllCases } from '../../services/caseService';

// Mock the caseService
jest.mock('../../services/caseService');

const mockCases = [
  {
    id: '1',
    title: 'Test Case 1',
    status: 'NEW',
    priority: 'HIGH',
    assigned_to: { full_name: 'John Doe' },
    updated_at: '2024-05-29T12:00:00Z',
  },
  {
    id: '2',
    title: 'Test Case 2',
    status: 'IN_PROGRESS',
    priority: 'MEDIUM',
    assigned_to: null,
    updated_at: '2024-05-28T12:00:00Z',
  },
];

const renderWithProviders = component => {
  return render(
    <BrowserRouter>
      <ChakraProvider>{component}</ChakraProvider>
    </BrowserRouter>
  );
};

describe('CaseListPage', () => {
  beforeEach(() => {
    getAllCases.mockResolvedValue(mockCases);
  });

  afterEach(() => {
    jest.clearAllMocks();
  });

  it('renders the case list page with filters', async () => {
    renderWithProviders(<CaseListPage />);

    expect(screen.getByText('Cases')).toBeInTheDocument();
    expect(screen.getByPlaceholderText('Filter by status')).toBeInTheDocument();
    expect(screen.getByPlaceholderText('Filter by priority')).toBeInTheDocument();
    expect(screen.getByPlaceholderText('Search cases...')).toBeInTheDocument();

    await waitFor(() => {
      expect(getAllCases).toHaveBeenCalled();
    });
  });

  it('displays cases with correct formatting', async () => {
    renderWithProviders(<CaseListPage />);

    await waitFor(() => {
      expect(screen.getByText('Test Case 1')).toBeInTheDocument();
      expect(screen.getByText('Test Case 2')).toBeInTheDocument();
      expect(screen.getByText('John Doe')).toBeInTheDocument();
      expect(screen.getByText('Unassigned')).toBeInTheDocument();
    });

    const statusBadges = screen.getAllByText(/NEW|IN_PROGRESS/);
    expect(statusBadges).toHaveLength(2);

    const priorityBadges = screen.getAllByText(/HIGH|MEDIUM/);
    expect(priorityBadges).toHaveLength(2);
  });

  it('handles filter changes', async () => {
    renderWithProviders(<CaseListPage />);

    const statusFilter = screen.getByPlaceholderText('Filter by status');
    fireEvent.change(statusFilter, { target: { value: 'NEW' } });

    await waitFor(() => {
      expect(getAllCases).toHaveBeenCalledWith(
        expect.objectContaining({
          status: 'NEW',
        })
      );
    });

    const priorityFilter = screen.getByPlaceholderText('Filter by priority');
    fireEvent.change(priorityFilter, { target: { value: 'HIGH' } });

    await waitFor(() => {
      expect(getAllCases).toHaveBeenCalledWith(
        expect.objectContaining({
          status: 'NEW',
          priority: 'HIGH',
        })
      );
    });
  });

  it('handles search input', async () => {
    renderWithProviders(<CaseListPage />);

    const searchInput = screen.getByPlaceholderText('Search cases...');
    fireEvent.change(searchInput, { target: { value: 'test search' } });

    await waitFor(() => {
      expect(getAllCases).toHaveBeenCalledWith(
        expect.objectContaining({
          search: 'test search',
        })
      );
    });
  });

  it('clears filters when clear button is clicked', async () => {
    renderWithProviders(<CaseListPage />);

    const searchInput = screen.getByPlaceholderText('Search cases...');
    fireEvent.change(searchInput, { target: { value: 'test search' } });

    const clearButton = screen.getByText('Clear Filters');
    fireEvent.click(clearButton);

    await waitFor(() => {
      expect(getAllCases).toHaveBeenCalledWith(
        expect.objectContaining({
          status: '',
          priority: '',
          search: '',
        })
      );
    });
  });

  it('handles API errors gracefully', async () => {
    const error = new Error('Failed to fetch cases');
    getAllCases.mockRejectedValue(error);

    renderWithProviders(<CaseListPage />);

    await waitFor(() => {
      expect(screen.getByText('Error')).toBeInTheDocument();
      expect(screen.getByText('Failed to fetch cases')).toBeInTheDocument();
    });
  });
});
