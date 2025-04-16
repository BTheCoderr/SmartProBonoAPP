import config from '../config';

export const immigrationApi = {
  // Get all cases
  getCases: async () => {
    try {
      const response = await fetch(`${config.apiUrl}/api/immigration/cases`);
      if (!response.ok) {
        throw new Error('Failed to fetch cases');
      }
      return response.json();
    } catch (error) {
      console.error('Error fetching cases:', error);
      throw error;
    }
  },

  // Create a new case
  createCase: async caseData => {
    try {
      const response = await fetch(`${config.apiUrl}/api/immigration/cases`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(caseData),
      });
      if (!response.ok) {
        throw new Error('Failed to create case');
      }
      return response.json();
    } catch (error) {
      console.error('Error creating case:', error);
      throw error;
    }
  },

  // Update an existing case
  updateCase: async (caseId, caseData) => {
    try {
      const response = await fetch(`${config.apiUrl}/api/immigration/cases/${caseId}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(caseData),
      });
      if (!response.ok) {
        throw new Error('Failed to update case');
      }
      return response.json();
    } catch (error) {
      console.error('Error updating case:', error);
      throw error;
    }
  },

  // Delete a case
  deleteCase: async caseId => {
    try {
      const response = await fetch(`${config.apiUrl}/api/immigration/cases/${caseId}`, {
        method: 'DELETE',
      });
      if (!response.ok) {
        throw new Error('Failed to delete case');
      }
      return response.json();
    } catch (error) {
      console.error('Error deleting case:', error);
      throw error;
    }
  },

  // Upload a document for a case
  uploadDocument: async (caseId, file) => {
    try {
      const formData = new FormData();
      formData.append('file', file);
      formData.append('caseId', caseId);

      const response = await fetch(`${config.apiUrl}/api/immigration/cases/${caseId}/documents`, {
        method: 'POST',
        body: formData,
      });
      if (!response.ok) {
        throw new Error('Failed to upload document');
      }
      return response.json();
    } catch (error) {
      console.error('Error uploading document:', error);
      throw error;
    }
  },

  // Get documents for a case
  getDocuments: async caseId => {
    try {
      const response = await fetch(`${config.apiUrl}/api/immigration/cases/${caseId}/documents`);
      if (!response.ok) {
        throw new Error('Failed to fetch documents');
      }
      return response.json();
    } catch (error) {
      console.error('Error fetching documents:', error);
      throw error;
    }
  },

  // Generate immigration forms
  generateForm: async (formType, formData) => {
    try {
      const response = await fetch(`${config.apiUrl}/api/immigration/forms/generate`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          formType,
          formData,
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to generate form');
      }

      // Get the blob from the response
      const blob = await response.blob();

      // Create a download link
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `${formType.toLowerCase().replace(/\s+/g, '-')}-${new Date().toISOString().split('T')[0]}.pdf`;

      // Trigger download
      document.body.appendChild(link);
      link.click();

      // Cleanup
      link.remove();
      window.URL.revokeObjectURL(url);
    } catch (error) {
      console.error('Error generating form:', error);
      throw error;
    }
  },
};
