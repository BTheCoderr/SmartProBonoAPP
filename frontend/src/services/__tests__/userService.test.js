import axios from 'axios';
import {
  getAllUsers,
  getUserById,
  getAvailableAttorneys,
  getUserProfile,
  updateUserProfile,
  updateUserAvailability,
} from '../userService';
import { API_BASE_URL, API_HEADERS } from '../../config/api';

// Mock axios
jest.mock('axios');

describe('userService', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe('getAllUsers', () => {
    it('fetches users with no filters', async () => {
      const mockUsers = [
        { id: '1', name: 'User 1' },
        { id: '2', name: 'User 2' },
      ];
      axios.get.mockResolvedValueOnce({ data: mockUsers });

      const result = await getAllUsers();
      expect(result).toEqual(mockUsers);
      expect(axios.get).toHaveBeenCalledWith(`${API_BASE_URL}/users?`, { headers: API_HEADERS });
    });

    it('fetches users with filters', async () => {
      const mockUsers = [{ id: '1', name: 'User 1' }];
      const filters = { role: 'attorney', availability: 'weekends' };
      axios.get.mockResolvedValueOnce({ data: mockUsers });

      const result = await getAllUsers(filters);
      expect(result).toEqual(mockUsers);
      expect(axios.get).toHaveBeenCalledWith(
        `${API_BASE_URL}/users?role=attorney&availability=weekends`,
        { headers: API_HEADERS }
      );
    });

    it('handles errors appropriately', async () => {
      const errorMessage = 'Network error';
      axios.get.mockRejectedValueOnce({ response: { data: { error: errorMessage } } });

      await expect(getAllUsers()).rejects.toThrow(errorMessage);
    });
  });

  describe('getAvailableAttorneys', () => {
    it('fetches available attorneys with no filters', async () => {
      const mockAttorneys = [
        { id: '1', name: 'Attorney 1' },
        { id: '2', name: 'Attorney 2' },
      ];
      axios.get.mockResolvedValueOnce({ data: mockAttorneys });

      const result = await getAvailableAttorneys();
      expect(result).toEqual(mockAttorneys);
      expect(axios.get).toHaveBeenCalledWith(`${API_BASE_URL}/api/users/attorneys/available?`, {
        headers: API_HEADERS,
      });
    });

    it('fetches attorneys with availability and specialty filters', async () => {
      const mockAttorneys = [{ id: '1', name: 'Attorney 1' }];
      const filters = {
        availability: 'weekdays',
        specialties: ['immigration', 'family'],
      };
      axios.get.mockResolvedValueOnce({ data: mockAttorneys });

      const result = await getAvailableAttorneys(filters);
      expect(result).toEqual(mockAttorneys);
      expect(axios.get).toHaveBeenCalledWith(
        `${API_BASE_URL}/api/users/attorneys/available?availability=weekdays&specialties=immigration&specialties=family`,
        { headers: API_HEADERS }
      );
    });

    it('handles errors appropriately', async () => {
      const errorMessage = 'Failed to fetch attorneys';
      axios.get.mockRejectedValueOnce({ response: { data: { error: errorMessage } } });

      await expect(getAvailableAttorneys()).rejects.toThrow(errorMessage);
    });
  });

  describe('getUserProfile', () => {
    it('fetches user profile successfully', async () => {
      const mockProfile = { id: '1', name: 'Test User', role: 'attorney' };
      axios.get.mockResolvedValueOnce({ data: mockProfile });

      const result = await getUserProfile('1');
      expect(result).toEqual(mockProfile);
      expect(axios.get).toHaveBeenCalledWith(`${API_BASE_URL}/api/users/1/profile`, {
        headers: API_HEADERS,
      });
    });

    it('handles errors appropriately', async () => {
      const errorMessage = 'Profile not found';
      axios.get.mockRejectedValueOnce({ response: { data: { error: errorMessage } } });

      await expect(getUserProfile('1')).rejects.toThrow(errorMessage);
    });
  });

  describe('updateUserProfile', () => {
    it('updates user profile successfully', async () => {
      const mockUpdatedProfile = {
        id: '1',
        profile: {
          full_name: 'Updated Name',
          specialties: ['immigration'],
        },
      };
      axios.put.mockResolvedValueOnce({ data: mockUpdatedProfile });

      const profileData = {
        full_name: 'Updated Name',
        specialties: ['immigration'],
      };

      const result = await updateUserProfile('1', profileData);
      expect(result).toEqual(mockUpdatedProfile);
      expect(axios.put).toHaveBeenCalledWith(`${API_BASE_URL}/api/users/1/profile`, profileData, {
        headers: API_HEADERS,
      });
    });

    it('handles errors appropriately', async () => {
      const errorMessage = 'Failed to update profile';
      axios.put.mockRejectedValueOnce({ response: { data: { error: errorMessage } } });

      await expect(updateUserProfile('1', {})).rejects.toThrow(errorMessage);
    });
  });

  describe('updateUserAvailability', () => {
    it('updates user availability successfully', async () => {
      const mockUpdatedUser = {
        id: '1',
        profile: {
          availability: { weekdays: true, weekends: false },
        },
      };
      axios.put.mockResolvedValueOnce({ data: mockUpdatedUser });

      const availabilityData = { weekdays: true, weekends: false };

      const result = await updateUserAvailability('1', availabilityData);
      expect(result).toEqual(mockUpdatedUser);
      expect(axios.put).toHaveBeenCalledWith(
        `${API_BASE_URL}/api/users/1/availability`,
        availabilityData,
        { headers: API_HEADERS }
      );
    });

    it('handles errors appropriately', async () => {
      const errorMessage = 'Failed to update availability';
      axios.put.mockRejectedValueOnce({ response: { data: { error: errorMessage } } });

      await expect(updateUserAvailability('1', {})).rejects.toThrow(errorMessage);
    });
  });
});
