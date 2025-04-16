import config from '../config';

export const documentApi = {
  // Get a document by ID
  getDocument: async documentId => {
    try {
      const response = await fetch(`${config.apiUrl}/api/documents/${documentId}`);
      if (!response.ok) {
        throw new Error('Failed to fetch document');
      }
      return response.json();
    } catch (error) {
      console.error('Error fetching document:', error);
      throw error;
    }
  },

  // Create a new document
  createDocument: async documentData => {
    try {
      const response = await fetch(`${config.apiUrl}/api/documents`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(documentData),
      });
      if (!response.ok) {
        throw new Error('Failed to create document');
      }
      return response.json();
    } catch (error) {
      console.error('Error creating document:', error);
      throw error;
    }
  },

  // Update a document
  updateDocument: async (documentId, documentData) => {
    try {
      const response = await fetch(`${config.apiUrl}/api/documents/${documentId}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(documentData),
      });
      if (!response.ok) {
        throw new Error('Failed to update document');
      }
      return response.json();
    } catch (error) {
      console.error('Error updating document:', error);
      throw error;
    }
  },

  // Get document versions
  getDocumentVersions: async documentId => {
    try {
      const response = await fetch(`${config.apiUrl}/api/documents/${documentId}/versions`);
      if (!response.ok) {
        throw new Error('Failed to fetch document versions');
      }
      return response.json();
    } catch (error) {
      console.error('Error fetching document versions:', error);
      throw error;
    }
  },

  // Revert to a specific version
  revertToVersion: async (documentId, version) => {
    try {
      const response = await fetch(
        `${config.apiUrl}/api/documents/${documentId}/versions/${version}`,
        {
          method: 'POST',
        }
      );
      if (!response.ok) {
        throw new Error('Failed to revert document');
      }
      return response.json();
    } catch (error) {
      console.error('Error reverting document:', error);
      throw error;
    }
  },

  // Share a document with users
  shareDocument: async (documentId, users) => {
    try {
      const response = await fetch(`${config.apiUrl}/api/documents/${documentId}/share`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ users }),
      });
      if (!response.ok) {
        throw new Error('Failed to share document');
      }
      return response.json();
    } catch (error) {
      console.error('Error sharing document:', error);
      throw error;
    }
  },

  // Generate a document from a template
  generateFromTemplate: async (templateId, formData) => {
    try {
      const response = await fetch(`${config.apiUrl}/api/documents/generate`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          templateId,
          formData,
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to generate document');
      }

      // Get the blob from the response
      const blob = await response.blob();

      // Create a download link
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `generated-document-${new Date().toISOString().split('T')[0]}.pdf`;

      // Trigger download
      document.body.appendChild(link);
      link.click();

      // Cleanup
      link.remove();
      window.URL.revokeObjectURL(url);
    } catch (error) {
      console.error('Error generating document:', error);
      throw error;
    }
  },

  // Save document as template
  saveAsTemplate: async (documentId, templateData) => {
    try {
      const response = await fetch(
        `${config.apiUrl}/api/documents/${documentId}/save-as-template`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(templateData),
        }
      );
      if (!response.ok) {
        throw new Error('Failed to save document as template');
      }
      return response.json();
    } catch (error) {
      console.error('Error saving document as template:', error);
      throw error;
    }
  },
};
