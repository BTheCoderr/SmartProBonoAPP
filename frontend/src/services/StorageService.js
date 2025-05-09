/**
 * StorageService.js
 * Utility service for managing local storage, session storage, and form progress tracking
 */

/**
 * Save form progress data to localStorage
 * @param {string} formId - Unique identifier for the form
 * @param {object|null} data - Form data to save or null to clear saved data
 */
export const saveFormProgress = (formId, data) => {
  try {
    if (data === null) {
      localStorage.removeItem(`form_progress_${formId}`);
      return;
    }
    
    const storageKey = `form_progress_${formId}`;
    localStorage.setItem(storageKey, JSON.stringify(data));
  } catch (error) {
    console.error('Error saving form progress:', error);
  }
};

/**
 * Retrieve saved form progress from localStorage
 * @param {string} formId - Unique identifier for the form
 * @returns {object|null} - The saved form data or null if not found
 */
export const getFormProgress = (formId) => {
  try {
    const storageKey = `form_progress_${formId}`;
    const savedData = localStorage.getItem(storageKey);
    
    if (!savedData) {
      return null;
    }
    
    return JSON.parse(savedData);
  } catch (error) {
    console.error('Error retrieving form progress:', error);
    return null;
  }
};

/**
 * Check if a form has any saved progress
 * @param {string} formId - Unique identifier for the form
 * @returns {boolean} - True if there is saved progress, false otherwise
 */
export const hasFormProgress = (formId) => {
  return getFormProgress(formId) !== null;
};

/**
 * Get completion percentage for all forms
 * @returns {Array} - Array of objects with formId and completion percentage
 */
export const getAllFormsProgress = () => {
  try {
    const forms = [];
    
    // Iterate through localStorage to find all form progress items
    for (let i = 0; i < localStorage.length; i++) {
      const key = localStorage.key(i);
      
      if (key.startsWith('form_progress_')) {
        try {
          const data = JSON.parse(localStorage.getItem(key));
          const formId = key.replace('form_progress_', '');
          
          forms.push({
            formId,
            progress: data.progress || 0,
            lastSaved: data.lastSaved || null,
            sessionId: data.sessionId || null
          });
        } catch (e) {
          console.error(`Error parsing data for key ${key}:`, e);
        }
      }
    }
    
    return forms;
  } catch (error) {
    console.error('Error getting all forms progress:', error);
    return [];
  }
};

/**
 * Clear all saved form progress data
 */
export const clearAllFormsProgress = () => {
  try {
    const keysToRemove = [];
    
    // Find all form progress keys
    for (let i = 0; i < localStorage.length; i++) {
      const key = localStorage.key(i);
      if (key.startsWith('form_progress_')) {
        keysToRemove.push(key);
      }
    }
    
    // Remove them all
    keysToRemove.forEach(key => localStorage.removeItem(key));
  } catch (error) {
    console.error('Error clearing all forms progress:', error);
  }
};

/**
 * Track form interaction analytics
 * @param {string} formId - Unique identifier for the form
 * @param {string} action - The interaction action
 * @param {object} data - Additional data about the interaction
 */
export const trackFormInteraction = (formId, action, data = {}) => {
  // This would typically send data to an analytics service
  // For now, we'll just log to console in development
  if (process.env.NODE_ENV === 'development') {
    console.log(`Form Interaction - ${formId} - ${action}`, data);
  }
  
  // Here you would implement actual analytics tracking
  // Example: trackEvent('form_interaction', { formId, action, ...data });
};

export default {
  saveFormProgress,
  getFormProgress,
  hasFormProgress,
  getAllFormsProgress,
  clearAllFormsProgress,
  trackFormInteraction
}; 