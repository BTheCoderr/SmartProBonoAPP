import api from './api';
import config from '../config';

const documentsApi = {
  // Get a document by ID
  getById: async (id) => {
    try {
      const response = await api.get(`/api/documents/${id}`);
      return response.data;
    } catch (error) {
      console.error('Error fetching document:', error);
      throw error;
    }
  },

  // Get all documents history
  getHistory: async () => {
    try {
      const response = await api.get('/api/documents/history');
      return response.data;
    } catch (error) {
      console.error('Error fetching document history:', error);
      throw error;
    }
  },

  // Delete a document
  deleteDocument: async (id) => {
    try {
      const response = await api.delete(`/api/documents/${id}`);
      return response.data;
    } catch (error) {
      console.error('Error deleting document:', error);
      throw error;
    }
  },

  // Get available templates
  getTemplates: async () => {
    try {
      const response = await api.get('/api/documents/templates');
      return response.data;
    } catch (error) {
      console.error('Error fetching templates:', error);
      throw error;
    }
  },

  // Generate a document from a template
  generateDocument: async (template, data) => {
    try {
      const response = await api.post('/api/documents/generate', {
        template,
        data,
      }, {
        responseType: 'blob',
      });
      
      // Create download link for the PDF
      const blob = new Blob([response.data], { type: 'application/pdf' });
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `${template.toLowerCase().replace(/\s+/g, '_')}.pdf`;
      document.body.appendChild(link);
      link.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(link);
      
      return true;
    } catch (error) {
      console.error('Error generating document:', error);
      throw error;
    }
  },
  
  // Generate a document directly using the document_service (for testing)
  generateDocumentDirect: async (template, data) => {
    try {
      const backendUrl = config.apiUrl;
      const response = await fetch(`${backendUrl}/api/contracts/generate`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          template: template,
          data: data,
          language: 'en'
        })
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
      link.download = `${template.toLowerCase().replace(/\s+/g, '-')}-${new Date().toISOString().split('T')[0]}.pdf`;
      
      // Trigger download
      document.body.appendChild(link);
      link.click();
      
      // Cleanup
      link.remove();
      window.URL.revokeObjectURL(url);
      
      return true;
    } catch (error) {
      console.error('Error generating document directly:', error);
      throw error;
    }
  },
  
  // Save a document
  saveDocument: async (documentData) => {
    try {
      const response = await api.post('/api/documents', documentData);
      return response.data;
    } catch (error) {
      console.error('Error saving document:', error);
      throw error;
    }
  },
  
  // Update document tags
  updateTags: async (documentId, tags) => {
    try {
      const response = await api.put(`/api/documents/${documentId}/tags`, { tags });
      return response.data;
    } catch (error) {
      console.error('Error updating document tags:', error);
      throw error;
    }
  },
  
  // Update document category
  updateCategory: async (documentId, category) => {
    try {
      const response = await api.put(`/api/documents/${documentId}/category`, { category });
      return response.data;
    } catch (error) {
      console.error('Error updating document category:', error);
      throw error;
    }
  },
  
  // Get document categories
  getCategories: async () => {
    try {
      const response = await api.get('/api/documents/categories');
      return response.data;
    } catch (error) {
      console.error('Error fetching document categories:', error);
      throw error;
    }
  },
  
  // Search documents by tags
  searchByTags: async (tags) => {
    try {
      const response = await api.post('/api/documents/search/tags', { tags });
      return response.data;
    } catch (error) {
      console.error('Error searching documents by tags:', error);
      throw error;
    }
  },
  
  // Share document via email
  shareViaEmail: async (documentId, emailDetails) => {
    try {
      const response = await api.post(`/api/documents/${documentId}/share-via-email`, emailDetails);
      return response.data;
    } catch (error) {
      console.error('Error sharing document via email:', error);
      throw error;
    }
  }
};

export default documentsApi; 