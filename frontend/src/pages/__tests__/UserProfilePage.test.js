import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { ChakraProvider } from '@chakra-ui/react';
import UserProfilePage from '../UserProfilePage';
import { getUserById, updateUserProfile, updateUserAvailability } from '../../services/userService';

// Mock the userService
jest.mock('../../services/userService');

const mockUser = {
  id: '123',
  full_name: 'John Doe',
  email: 'john@example.com',
  phone: '123-456-7890',
  role: 'ATTORNEY',
  profile: {
    specialties: ['CRIMINAL_LAW', 'FAMILY_LAW'],
    bio: 'Test bio',
  },
  availability: {
    monday: { available: true, hours: '9:00-17:00' },
    tuesday: { available: true, hours: '9:00-17:00' },
    wednesday: { available: false, hours: '9:00-17:00' },
    thursday: { available: true, hours: '9:00-17:00' },
    friday: { available: true, hours: '9:00-17:00' },
  },
  case_load: {
    active_cases: 5,
    cases_this_month: 8,
    total_cases: 25,
  },
};

describe('UserProfilePage', () => {
  beforeEach(() => {
    getUserById.mockResolvedValue(mockUser);
    updateUserProfile.mockResolvedValue({});
    updateUserAvailability.mockResolvedValue({});
  });

  afterEach(() => {
    jest.clearAllMocks();
  });

  it('renders user profile data', async () => {
    render(
      <ChakraProvider>
        <UserProfilePage />
      </ChakraProvider>
    );

    await waitFor(() => {
      expect(getUserById).toHaveBeenCalledWith('123');
    });

    expect(screen.getByDisplayValue('John Doe')).toBeInTheDocument();
    expect(screen.getByDisplayValue('john@example.com')).toBeInTheDocument();
    expect(screen.getByDisplayValue('123-456-7890')).toBeInTheDocument();
    expect(screen.getByDisplayValue('ATTORNEY')).toBeInTheDocument();
    expect(screen.getByDisplayValue('Test bio')).toBeInTheDocument();
  });

  it('handles profile updates', async () => {
    render(
      <ChakraProvider>
        <UserProfilePage />
      </ChakraProvider>
    );

    await waitFor(() => {
      expect(getUserById).toHaveBeenCalled();
    });

    const nameInput = screen.getByLabelText('Full Name');
    fireEvent.change(nameInput, { target: { value: 'Jane Doe' } });

    const emailInput = screen.getByLabelText('Email');
    fireEvent.change(emailInput, { target: { value: 'jane@example.com' } });

    const saveButton = screen.getByText('Save Profile');
    fireEvent.click(saveButton);

    await waitFor(() => {
      expect(updateUserProfile).toHaveBeenCalledWith(
        '123',
        expect.objectContaining({
          full_name: 'Jane Doe',
          email: 'jane@example.com',
        })
      );
    });

    expect(screen.getByText('Success')).toBeInTheDocument();
    expect(screen.getByText('Profile updated successfully')).toBeInTheDocument();
  });

  it('handles specialty toggles', async () => {
    render(
      <ChakraProvider>
        <UserProfilePage />
      </ChakraProvider>
    );

    await waitFor(() => {
      expect(getUserById).toHaveBeenCalled();
    });

    const civilRightsSwitch = screen.getByText('CIVIL RIGHTS').previousSibling;
    fireEvent.click(civilRightsSwitch);

    const saveButton = screen.getByText('Save Profile');
    fireEvent.click(saveButton);

    await waitFor(() => {
      expect(updateUserProfile).toHaveBeenCalledWith(
        '123',
        expect.objectContaining({
          specialties: ['CRIMINAL_LAW', 'FAMILY_LAW', 'CIVIL_RIGHTS'],
        })
      );
    });
  });

  it('handles availability updates', async () => {
    render(
      <ChakraProvider>
        <UserProfilePage />
      </ChakraProvider>
    );

    await waitFor(() => {
      expect(getUserById).toHaveBeenCalled();
    });

    const wednesdaySwitch = screen.getAllByRole('switch')[7]; // Wednesday's switch
    fireEvent.click(wednesdaySwitch);

    const hoursInput = screen.getAllByPlaceholderText('9:00-17:00')[2]; // Wednesday's hours
    fireEvent.change(hoursInput, { target: { value: '10:00-18:00' } });

    const saveButton = screen.getByText('Save Availability');
    fireEvent.click(saveButton);

    await waitFor(() => {
      expect(updateUserAvailability).toHaveBeenCalledWith(
        '123',
        expect.objectContaining({
          wednesday: { available: true, hours: '10:00-18:00' },
        })
      );
    });

    expect(screen.getByText('Success')).toBeInTheDocument();
    expect(screen.getByText('Availability updated successfully')).toBeInTheDocument();
  });

  it('displays case load information', async () => {
    render(
      <ChakraProvider>
        <UserProfilePage />
      </ChakraProvider>
    );

    await waitFor(() => {
      expect(getUserById).toHaveBeenCalled();
    });

    expect(screen.getByText('5')).toBeInTheDocument();
    expect(screen.getByText('8')).toBeInTheDocument();
    expect(screen.getByText('25')).toBeInTheDocument();
  });

  it('handles API errors gracefully', async () => {
    const error = new Error('Failed to fetch user data');
    getUserById.mockRejectedValue(error);

    render(
      <ChakraProvider>
        <UserProfilePage />
      </ChakraProvider>
    );

    await waitFor(() => {
      expect(screen.getByText('Error')).toBeInTheDocument();
      expect(screen.getByText('Failed to fetch user data')).toBeInTheDocument();
    });
  });

  it('handles profile update errors', async () => {
    const error = new Error('Failed to update profile');
    updateUserProfile.mockRejectedValue(error);

    render(
      <ChakraProvider>
        <UserProfilePage />
      </ChakraProvider>
    );

    await waitFor(() => {
      expect(getUserById).toHaveBeenCalled();
    });

    const saveButton = screen.getByText('Save Profile');
    fireEvent.click(saveButton);

    await waitFor(() => {
      expect(screen.getByText('Error')).toBeInTheDocument();
      expect(screen.getByText('Failed to update profile')).toBeInTheDocument();
    });
  });

  it('handles availability update errors', async () => {
    const error = new Error('Failed to update availability');
    updateUserAvailability.mockRejectedValue(error);

    render(
      <ChakraProvider>
        <UserProfilePage />
      </ChakraProvider>
    );

    await waitFor(() => {
      expect(getUserById).toHaveBeenCalled();
    });

    const saveButton = screen.getByText('Save Availability');
    fireEvent.click(saveButton);

    await waitFor(() => {
      expect(screen.getByText('Error')).toBeInTheDocument();
      expect(screen.getByText('Failed to update availability')).toBeInTheDocument();
    });
  });
});
