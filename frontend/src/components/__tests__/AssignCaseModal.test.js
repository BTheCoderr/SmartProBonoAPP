import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { ChakraProvider } from '@chakra-ui/react';
import AssignCaseModal from '../AssignCaseModal';
import { getAvailableAttorneys } from '../../services/userService';

// Mock the userService
jest.mock('../../services/userService');

const mockAttorneys = [
  { id: '1', full_name: 'John Doe', profile: { specialties: ['Criminal Law', 'Family Law'] } },
  { id: '2', full_name: 'Jane Smith', profile: { specialties: ['Immigration Law'] } },
];

describe('AssignCaseModal', () => {
  const mockOnClose = jest.fn();
  const mockOnAssign = jest.fn();

  beforeEach(() => {
    getAvailableAttorneys.mockResolvedValue(mockAttorneys);
  });

  afterEach(() => {
    jest.clearAllMocks();
  });

  it('renders the modal when isOpen is true', async () => {
    render(
      <ChakraProvider>
        <AssignCaseModal isOpen={true} onClose={mockOnClose} onAssign={mockOnAssign} />
      </ChakraProvider>
    );

    expect(screen.getByText('Assign Case')).toBeInTheDocument();
    await waitFor(() => {
      expect(getAvailableAttorneys).toHaveBeenCalled();
    });
  });

  it('loads and displays available attorneys', async () => {
    render(
      <ChakraProvider>
        <AssignCaseModal isOpen={true} onClose={mockOnClose} onAssign={mockOnAssign} />
      </ChakraProvider>
    );

    await waitFor(() => {
      expect(screen.getByText('John Doe - Criminal Law, Family Law')).toBeInTheDocument();
      expect(screen.getByText('Jane Smith - Immigration Law')).toBeInTheDocument();
    });
  });

  it('handles attorney selection and notes input', async () => {
    render(
      <ChakraProvider>
        <AssignCaseModal isOpen={true} onClose={mockOnClose} onAssign={mockOnAssign} />
      </ChakraProvider>
    );

    await waitFor(() => {
      expect(getAvailableAttorneys).toHaveBeenCalled();
    });

    const selectElement = screen.getByRole('combobox');
    fireEvent.change(selectElement, { target: { value: '1' } });

    const notesInput = screen.getByPlaceholderText('Add notes about this assignment...');
    fireEvent.change(notesInput, { target: { value: 'Test assignment notes' } });

    const assignButton = screen.getByText('Assign');
    fireEvent.click(assignButton);

    expect(mockOnAssign).toHaveBeenCalledWith('1', 'Test assignment notes');
  });

  it('disables the assign button when no attorney is selected', async () => {
    render(
      <ChakraProvider>
        <AssignCaseModal isOpen={true} onClose={mockOnClose} onAssign={mockOnAssign} />
      </ChakraProvider>
    );

    await waitFor(() => {
      expect(getAvailableAttorneys).toHaveBeenCalled();
    });

    const assignButton = screen.getByText('Assign');
    expect(assignButton).toBeDisabled();
  });

  it('handles API errors gracefully', async () => {
    const error = new Error('Failed to load attorneys');
    getAvailableAttorneys.mockRejectedValue(error);

    render(
      <ChakraProvider>
        <AssignCaseModal isOpen={true} onClose={mockOnClose} onAssign={mockOnAssign} />
      </ChakraProvider>
    );

    await waitFor(() => {
      expect(getAvailableAttorneys).toHaveBeenCalled();
    });
  });
});
