import axios from 'axios';
import { API_BASE_URL, API_HEADERS } from '../config/api';

// Helper function to handle API errors
const handleApiError = error => {
  if (error.response) {
    throw new Error(error.response.data.error || 'An error occurred');
  }
  throw error;
};

// Upload document
export const uploadDocument = async (caseId, file, metadata = {}) => {
  try {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('metadata', JSON.stringify(metadata));

    const response = await axios.post(`${API_BASE_URL}/cases/${caseId}/documents`, formData, {
      headers: {
        ...API_HEADERS,
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  } catch (error) {
    handleApiError(error);
  }
};

// Get documents for a case
export const getCaseDocuments = async caseId => {
  try {
    const response = await axios.get(`${API_BASE_URL}/cases/${caseId}/documents`, {
      headers: API_HEADERS,
    });
    return response.data;
  } catch (error) {
    handleApiError(error);
  }
};

// Download document
export const downloadDocument = async (caseId, documentId) => {
  try {
    const response = await axios.get(
      `${API_BASE_URL}/cases/${caseId}/documents/${documentId}/download`,
      {
        headers: API_HEADERS,
        responseType: 'blob',
      }
    );
    return response.data;
  } catch (error) {
    handleApiError(error);
  }
};

// Update document metadata
export const updateDocumentMetadata = async (caseId, documentId, metadata) => {
  try {
    const response = await axios.put(
      `${API_BASE_URL}/cases/${caseId}/documents/${documentId}/metadata`,
      metadata,
      { headers: API_HEADERS }
    );
    return response.data;
  } catch (error) {
    handleApiError(error);
  }
};

// Delete document
export const deleteDocument = async (caseId, documentId) => {
  try {
    await axios.delete(`${API_BASE_URL}/cases/${caseId}/documents/${documentId}`, {
      headers: API_HEADERS,
    });
  } catch (error) {
    handleApiError(error);
  }
};

// Share document
export const shareDocument = async (caseId, documentId, shareData) => {
  try {
    const response = await axios.post(
      `${API_BASE_URL}/cases/${caseId}/documents/${documentId}/share`,
      shareData,
      { headers: API_HEADERS }
    );
    return response.data;
  } catch (error) {
    handleApiError(error);
  }
};

// Get document versions
export const getDocumentVersions = async (caseId, documentId) => {
  try {
    const response = await axios.get(
      `${API_BASE_URL}/cases/${caseId}/documents/${documentId}/versions`,
      { headers: API_HEADERS }
    );
    return response.data;
  } catch (error) {
    handleApiError(error);
  }
};

// Restore document version
export const restoreDocumentVersion = async (caseId, documentId, versionId) => {
  try {
    const response = await axios.post(
      `${API_BASE_URL}/cases/${caseId}/documents/${documentId}/versions/${versionId}/restore`,
      {},
      { headers: API_HEADERS }
    );
    return response.data;
  } catch (error) {
    handleApiError(error);
  }
};

// Mock form schema data - in a real app, this would come from an API
const formSchemas = {
  'lease-agreement': {
    sections: [
      {
        title: 'Basic Information',
        fields: [
          { id: 'landlordName', label: 'Landlord Name', type: 'text', required: true },
          { id: 'tenantName', label: 'Tenant Name', type: 'text', required: true },
          { id: 'propertyAddress', label: 'Property Address', type: 'textarea', required: true },
        ],
      },
      {
        title: 'Lease Terms',
        fields: [
          { id: 'startDate', label: 'Start Date', type: 'date', required: true },
          { id: 'endDate', label: 'End Date', type: 'date', required: true },
          { id: 'monthlyRent', label: 'Monthly Rent', type: 'number', required: true },
          { id: 'securityDeposit', label: 'Security Deposit', type: 'number', required: true },
        ],
      },
    ],
  },
  // Add more templates as needed
};

export const getTemplateFormSchema = (templateId) => {
  return formSchemas[templateId] || {
    sections: [
      {
        title: 'Default Section',
        fields: [
          { id: 'defaultField', label: 'Default Field', type: 'text', required: true },
        ],
      },
    ],
  };
};

export const generateDocument = async (templateId, formData) => {
  const response = await fetch(`${process.env.REACT_APP_API_URL}/api/documents/generate`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${localStorage.getItem('authToken')}`,
    },
    body: JSON.stringify({
      templateId,
      formData,
    }),
  });

  if (!response.ok) {
    const data = await response.json();
    throw new Error(data.message || 'Failed to generate document');
  }

  return response.json();
};
