import { useState } from 'react';
import axios from 'axios';
import config from '../config';
import { logInfo, logError } from '../utils/logger';

/**
 * Hook for sending test notifications
 * This is useful for testing the notification system in development
 */
const useTestNotification = () => {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(false);

  /**
   * Send a test notification
   * @param {Object} notificationData - The notification data
   * @param {string} notificationData.type - The notification type ('info', 'success', 'warning', 'error')
   * @param {string} notificationData.title - The notification title
   * @param {string} notificationData.message - The notification message
   * @param {number} [notificationData.user_id] - Optional user ID to send to specific user
   * @returns {Promise<Object>} - The notification response
   */
  const sendTestNotification = async (notificationData) => {
    setIsLoading(true);
    setError(null);
    setSuccess(false);

    try {
      // Validate the notification data
      const requiredFields = ['type', 'title', 'message'];
      const missingFields = requiredFields.filter(field => !notificationData[field]);
      
      if (missingFields.length > 0) {
        throw new Error(`Missing required fields: ${missingFields.join(', ')}`);
      }

      // Send the notification
      const response = await axios.post(
        `${config.api.baseUrl}/api/test-notification`,
        notificationData
      );

      logInfo('Test notification sent', { data: notificationData, response: response.data });
      setSuccess(true);
      return response.data;
    } catch (err) {
      const errorMessage = err.response?.data?.error || err.message || 'Failed to send test notification';
      logError('Failed to send test notification', { error: err, data: notificationData });
      setError(errorMessage);
      throw err;
    } finally {
      setIsLoading(false);
    }
  };

  /**
   * Send a preset test notification
   * @param {string} type - Preset type ('info', 'success', 'warning', 'error')
   * @param {number} [userId] - Optional user ID to send to specific user
   * @returns {Promise<Object>} - The notification response
   */
  const sendPresetNotification = async (type, userId = null) => {
    const presets = {
      info: {
        type: 'info',
        title: 'Information',
        message: 'This is a test information notification.',
      },
      success: {
        type: 'success',
        title: 'Success',
        message: 'Your action was completed successfully.',
      },
      warning: {
        type: 'warning',
        title: 'Warning',
        message: 'Please be cautious about this action.',
      },
      error: {
        type: 'error',
        title: 'Error',
        message: 'An error occurred. Please try again.',
      },
    };

    const preset = presets[type] || presets.info;
    if (userId) {
      preset.user_id = userId;
    }

    return sendTestNotification(preset);
  };

  return {
    isLoading,
    error,
    success,
    sendTestNotification,
    sendPresetNotification,
  };
};

export default useTestNotification; 