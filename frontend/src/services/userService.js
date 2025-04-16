import axios from 'axios';
import { API_BASE_URL, API_HEADERS } from '../config/api';

// Helper function to handle API errors
const handleApiError = error => {
  if (error.response) {
    throw new Error(error.response.data.error || 'An error occurred');
  }
  throw error;
};

// Get all users with optional filters (e.g., role, availability)
export const getAllUsers = async (filters = {}) => {
  try {
    const queryParams = new URLSearchParams();
    Object.entries(filters).forEach(([key, value]) => {
      if (value) queryParams.append(key, value);
    });

    const response = await axios.get(`${API_BASE_URL}/users?${queryParams.toString()}`, {
      headers: API_HEADERS,
    });
    return response.data;
  } catch (error) {
    handleApiError(error);
  }
};

// Get user by ID
export const getUserById = async userId => {
  try {
    const response = await axios.get(`${API_BASE_URL}/users/${userId}`, { headers: API_HEADERS });
    return response.data;
  } catch (error) {
    handleApiError(error);
  }
};

/**
 * Get available attorneys for case assignment
 * @param {Object} filters - Optional filters for attorneys
 * @param {string} filters.availability - Filter by availability (e.g., 'weekdays', 'weekends')
 * @param {Array<string>} filters.specialties - Filter by specialties
 * @returns {Promise<Array>} List of available attorneys
 */
export const getAvailableAttorneys = async (filters = {}) => {
  try {
    const queryParams = new URLSearchParams();
    if (filters.availability) {
      queryParams.append('availability', filters.availability);
    }
    if (filters.specialties) {
      filters.specialties.forEach(specialty => queryParams.append('specialties', specialty));
    }

    const response = await axios.get(
      `${API_BASE_URL}/api/users/attorneys/available?${queryParams.toString()}`,
      { headers: API_HEADERS }
    );
    return response.data;
  } catch (error) {
    handleApiError(error);
  }
};

/**
 * Get user profile by ID
 * @param {string} userId - User ID
 * @returns {Promise<Object>} User profile data
 */
export const getUserProfile = async userId => {
  try {
    const response = await axios.get(`${API_BASE_URL}/api/users/${userId}/profile`, {
      headers: API_HEADERS,
    });
    return response.data;
  } catch (error) {
    handleApiError(error);
  }
};

/**
 * Update user profile
 * @param {string} userId - User ID
 * @param {Object} profileData - Profile data to update
 * @returns {Promise<Object>} Updated user profile
 */
export const updateUserProfile = async (userId, profileData) => {
  try {
    const response = await axios.put(`${API_BASE_URL}/api/users/${userId}/profile`, profileData, {
      headers: API_HEADERS,
    });
    return response.data;
  } catch (error) {
    handleApiError(error);
  }
};

/**
 * Update user availability
 * @param {string} userId - User ID
 * @param {Object} availabilityData - Availability settings
 * @returns {Promise<Object>} Updated user data
 */
export const updateUserAvailability = async (userId, availabilityData) => {
  try {
    const response = await axios.put(
      `${API_BASE_URL}/api/users/${userId}/availability`,
      availabilityData,
      { headers: API_HEADERS }
    );
    return response.data;
  } catch (error) {
    handleApiError(error);
  }
};
