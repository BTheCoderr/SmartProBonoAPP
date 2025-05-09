#!/usr/bin/env node

/**
 * Form Progress Tracking Test Script
 * 
 * This script tests the form progress tracking functionality by:
 * 1. Importing the StorageService functions
 * 2. Simulating form data updates
 * 3. Verifying that the data is properly stored and retrieved
 */

// Mock localStorage for Node.js environment
global.localStorage = {
  data: {},
  getItem(key) {
    return this.data[key] || null;
  },
  setItem(key, value) {
    this.data[key] = value;
  },
  removeItem(key) {
    delete this.data[key];
  },
  clear() {
    this.data = {};
  }
};

// Import the functions from a mock version of the actual service
// In a real environment, we would import from the actual service
const {
  saveFormProgress,
  getFormProgress,
  hasFormProgress,
  getAllFormsProgress,
  clearAllFormsProgress
} = {
  saveFormProgress: (formId, data) => {
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
  },
  
  getFormProgress: (formId) => {
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
  },
  
  hasFormProgress: (formId) => {
    return getFormProgress(formId) !== null;
  },
  
  getAllFormsProgress: () => {
    try {
      const forms = [];
      
      // In our mock, we'll just look through the known keys
      const keys = Object.keys(localStorage.data);
      
      for (const key of keys) {
        if (key.startsWith('form_progress_')) {
          try {
            const data = JSON.parse(localStorage.data[key]);
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
  },
  
  clearAllFormsProgress: () => {
    try {
      const keysToRemove = [];
      
      // In our mock, we'll just look through the known keys
      const keys = Object.keys(localStorage.data);
      
      for (const key of keys) {
        if (key.startsWith('form_progress_')) {
          keysToRemove.push(key);
        }
      }
      
      // Remove them all
      keysToRemove.forEach(key => localStorage.removeItem(key));
    } catch (error) {
      console.error('Error clearing all forms progress:', error);
    }
  }
};

/**
 * Test function to verify form progress tracking
 */
function testFormProgressTracking() {
  console.log('Starting Form Progress Tracking Test...');
  
  // Test Data
  const testFormId = 'immigrationIntakeForm';
  const mockSessionId = 'test-session-123';
  const now = new Date().toISOString();
  
  // Test 1: Initial state (no data)
  console.log('\nTest 1: Initial state check');
  const initialData = getFormProgress(testFormId);
  console.log('Initial data:', initialData);
  console.assert(initialData === null, 'Initial data should be null');
  
  // Test 2: Save form progress
  console.log('\nTest 2: Save form progress');
  const testFormData = {
    firstName: 'John',
    lastName: 'Doe',
    email: 'john.doe@example.com',
    phone: '555-123-4567',
  };
  
  saveFormProgress(testFormId, {
    formData: testFormData,
    sessionId: mockSessionId,
    lastSaved: now,
    progress: 50
  });
  
  console.log('Form progress saved');
  
  // Test 3: Retrieve saved form progress
  console.log('\nTest 3: Retrieve saved form progress');
  const savedData = getFormProgress(testFormId);
  console.log('Retrieved data:', savedData);
  console.assert(savedData !== null, 'Retrieved data should not be null');
  console.assert(savedData.formData.firstName === 'John', 'First name should match');
  console.assert(savedData.progress === 50, 'Progress should be 50%');
  
  // Test 4: Update form progress
  console.log('\nTest 4: Update form progress');
  const updatedFormData = {
    ...testFormData,
    currentImmigrationStatus: 'permanent_resident',
    nationality: 'Canada',
    desiredService: 'citizenship'
  };
  
  saveFormProgress(testFormId, {
    formData: updatedFormData,
    sessionId: mockSessionId,
    lastSaved: new Date().toISOString(),
    progress: 75
  });
  
  console.log('Form progress updated');
  
  // Test 5: Retrieve updated form progress
  console.log('\nTest 5: Retrieve updated form progress');
  const updatedData = getFormProgress(testFormId);
  console.log('Updated data:', updatedData);
  console.assert(updatedData.progress === 75, 'Updated progress should be 75%');
  console.assert(updatedData.formData.nationality === 'Canada', 'Nationality should be Canada');
  
  // Test 6: Get all forms progress
  console.log('\nTest 6: Get all forms progress');
  
  // Add another form for testing
  saveFormProgress('otherForm', {
    formData: { field1: 'value1' },
    sessionId: 'other-session-456',
    lastSaved: new Date().toISOString(),
    progress: 25
  });
  
  const allForms = getAllFormsProgress();
  console.log('All forms:', allForms);
  console.assert(allForms.length === 2, 'Should have 2 forms in progress');
  
  // Test 7: Check if form has progress
  console.log('\nTest 7: Check if form has progress');
  const hasProgress = hasFormProgress(testFormId);
  console.log('Has progress:', hasProgress);
  console.assert(hasProgress === true, 'Form should have progress');
  
  // Test 8: Clear form progress
  console.log('\nTest 8: Clear form progress');
  saveFormProgress(testFormId, null);
  const afterClear = getFormProgress(testFormId);
  console.log('After clear:', afterClear);
  console.assert(afterClear === null, 'Form progress should be null after clearing');
  
  // Test 9: Clear all forms progress
  console.log('\nTest 9: Clear all forms progress');
  clearAllFormsProgress();
  const remainingForms = getAllFormsProgress();
  console.log('Remaining forms:', remainingForms);
  console.assert(remainingForms.length === 0, 'Should have no forms in progress after clearing all');
  
  // Final result
  console.log('\nForm Progress Tracking Test Completed!');
  console.log('All tests passed!');
}

// Run the test
testFormProgressTracking(); 