import axios from 'axios';
import config from '../config';

// Create axios instance with default config
const api = axios.create({
  baseURL: config.apiUrl,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Legal Rights API
export const legalRightsApi = {
  getRights: async category => {
    try {
      const response = await api.get(`/api/legal/rights/${category}`);
      return response.data;
    } catch (error) {
      console.error('Error fetching legal rights:', error);
      throw error;
    }
  },
};

// Legal Chat API
export const legalChatApi = {
  sendMessage: async (message, taskType = 'chat') => {
    try {
      const response = await fetch(`${config.apiUrl}/api/legal/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message,
          task_type: taskType,
          include_model_info: true,
        }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Failed to send message');
      }

      const data = await response.json();
      return {
        response: data.response,
        model: data.model,
        provider: data.provider,
        tokens: data.tokens,
        confidenceScore: data.confidence_score,
        confidenceFactors: data.confidence_factors,
        reasoningDetails: data.reasoning_details,
        citations: data.citations || [],
        jurisdictions: data.jurisdictions || [],
        lastUpdated: data.last_updated,
        status: data.status,
      };
    } catch (error) {
      console.error('Error sending message:', error);
      throw error;
    }
  },

  // Add specialized endpoints for different tasks
  generateDocument: async (prompt, documentType) => {
    try {
      const response = await fetch(`${config.apiUrl}/api/legal/draft`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          prompt,
          document_type: documentType,
          task_type: 'document_drafting',
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to generate document');
      }

      const data = await response.json();
      return {
        document: data.document,
        model: data.model,
        confidenceScore: data.confidence_score,
        citations: data.citations || [],
        status: data.status,
      };
    } catch (error) {
      console.error('Error generating document:', error);
      throw error;
    }
  },

  researchRights: async (query, jurisdiction = null) => {
    try {
      const response = await fetch(`${config.apiUrl}/api/legal/rights`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          topic: query,
          jurisdiction: jurisdiction,
          task_type: 'rights_research',
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to research rights');
      }

      const data = await response.json();
      return {
        explanation: data.explanation,
        model: data.model,
        confidenceScore: data.confidence_score,
        citations: data.citations || [],
        jurisdictions: data.jurisdictions || [],
        reasoningDetails: data.reasoning_details,
        status: data.status,
      };
    } catch (error) {
      console.error('Error researching rights:', error);
      throw error;
    }
  },

  analyzeLegal: async (query, analysisType = 'legal_research') => {
    try {
      const response = await fetch(`${config.apiUrl}/api/legal/analyze`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          document: query,
          analysis_type: analysisType,
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to analyze legal text');
      }

      const data = await response.json();
      return {
        analysis: data.analysis,
        model: data.model,
        confidenceScore: data.confidence_score,
        citations: data.citations || [],
        jurisdictions: data.jurisdictions || [],
        reasoningDetails: data.reasoning_details,
        status: data.status,
      };
    } catch (error) {
      console.error('Error analyzing legal text:', error);
      throw error;
    }
  },

  explainProcedure: async (procedureType, jurisdiction = null) => {
    try {
      const response = await fetch(`${config.apiUrl}/api/legal/procedure`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          procedure_type: procedureType,
          jurisdiction: jurisdiction,
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to explain procedure');
      }

      const data = await response.json();
      return {
        guidance: data.guidance,
        model: data.model,
        confidenceScore: data.confidence_score,
        citations: data.citations || [],
        jurisdictions: data.jurisdictions || [],
        reasoningDetails: data.reasoning_details,
        status: data.status,
      };
    } catch (error) {
      console.error('Error explaining procedure:', error);
      throw error;
    }
  },
};

// Documents API
export const documentsApi = {
  generateDocument: async (template, data) => {
    try {
      const response = await api.post('/api/documents/generate', {
        template,
        data,
      });
      return response.data;
    } catch (error) {
      console.error('Error generating document:', error);
      throw error;
    }
  },

  getTemplates: async () => {
    try {
      const response = await api.get('/api/documents/templates');
      return response.data;
    } catch (error) {
      console.error('Error fetching templates:', error);
      throw error;
    }
  },

  // New document endpoints
  saveDocument: async documentData => {
    try {
      const response = await api.post('/api/documents/save', documentData);
      return response.data;
    } catch (error) {
      console.error('Error saving document:', error);
      throw error;
    }
  },

  getDocumentHistory: async () => {
    try {
      const response = await api.get('/api/documents/history');
      return response.data;
    } catch (error) {
      console.error('Error fetching document history:', error);
      throw error;
    }
  },

  submitToEFiling: async (documentId, courtInfo) => {
    try {
      const response = await api.post(`/api/documents/${documentId}/efile`, courtInfo);
      return response.data;
    } catch (error) {
      console.error('Error submitting to e-filing:', error);
      throw error;
    }
  },
};

// Immigration Services API
export const immigrationApi = {
  getVisaRequirements: async visaType => {
    try {
      const response = await api.get(`/api/immigration/visa-requirements/${visaType}`);
      return response.data;
    } catch (error) {
      console.error('Error fetching visa requirements:', error);
      throw error;
    }
  },

  submitVisaApplication: async applicationData => {
    try {
      const response = await api.post('/api/immigration/apply', applicationData);
      return response.data;
    } catch (error) {
      console.error('Error submitting visa application:', error);
      throw error;
    }
  },
};

// Expungement Services API
export const expungementApi = {
  checkEligibility: async caseData => {
    try {
      const response = await api.post('/api/expungement/check-eligibility', caseData);
      return response.data;
    } catch (error) {
      console.error('Error checking expungement eligibility:', error);
      throw error;
    }
  },

  getStateRules: async state => {
    try {
      const response = await api.get(`/api/expungement/rules/${state}`);
      return response.data;
    } catch (error) {
      console.error('Error fetching state rules:', error);
      throw error;
    }
  },

  startExpungementProcess: async caseData => {
    try {
      const response = await api.post('/api/expungement/start', caseData);
      return response.data;
    } catch (error) {
      console.error('Error starting expungement process:', error);
      throw error;
    }
  },

  saveProgress: async (caseId, progressData) => {
    try {
      const response = await api.put(`/api/expungement/${caseId}/progress`, progressData);
      return response.data;
    } catch (error) {
      console.error('Error saving progress:', error);
      throw error;
    }
  },

  getRequiredDocuments: async (state, caseType) => {
    try {
      const response = await api.get(`/api/expungement/documents/${state}/${caseType}`);
      return response.data;
    } catch (error) {
      console.error('Error fetching required documents:', error);
      throw error;
    }
  },
};

// Feedback API
export const feedbackApi = {
  submit: async feedbackData => {
    try {
      const response = await fetch(`${config.apiUrl}/api/feedback`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(feedbackData),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Failed to submit feedback');
      }

      return response.json();
    } catch (error) {
      console.error('Error submitting feedback:', error);
      throw error;
    }
  },

  getAnalytics: async () => {
    try {
      const response = await fetch(`${config.apiUrl}/api/feedback/analytics`);

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Failed to fetch feedback analytics');
      }

      return response.json();
    } catch (error) {
      console.error('Error fetching analytics:', error);
      throw error;
    }
  },
};

// Conversation API
export const conversationApi = {
  save: async conversationData => {
    try {
      const response = await fetch(`${config.apiUrl}/api/conversations`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(conversationData),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Failed to save conversation');
      }

      return response.json();
    } catch (error) {
      console.error('Error saving conversation:', error);
      throw error;
    }
  },

  getByUserId: async userId => {
    try {
      const response = await fetch(`${config.apiUrl}/api/conversations/${userId}`);

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Failed to fetch conversations');
      }

      return response.json();
    } catch (error) {
      console.error('Error fetching conversations:', error);
      throw error;
    }
  },
};

// Contracts API
export const contractsApi = {
  generate: async (templateName, formData, language) => {
    try {
      const response = await fetch(`${config.apiUrl}/api/contracts/generate`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          template: templateName.toLowerCase().replace(/\s+/g, '_'),
          data: formData,
          language: language,
        }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Failed to generate contract');
      }

      // Get the blob from the response
      const blob = await response.blob();

      // Create a download link
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `${templateName.toLowerCase().replace(/\s+/g, '-')}-${new Date().toISOString().split('T')[0]}.pdf`;

      // Trigger download
      document.body.appendChild(link);
      link.click();

      // Cleanup
      link.remove();
      window.URL.revokeObjectURL(url);
    } catch (error) {
      console.error('Error generating contract:', error);
      throw error;
    }
  },

  getTemplates: async () => {
    try {
      const response = await fetch(`${config.apiUrl}/api/contracts/templates`);
      if (!response.ok) {
        throw new Error('Failed to fetch templates');
      }
      return response.json();
    } catch (error) {
      console.error('Error fetching templates:', error);
      throw error;
    }
  },
};

// Error interceptor
api.interceptors.response.use(
  response => response,
  error => {
    if (error.response) {
      // Handle specific error status codes
      switch (error.response.status) {
        case 401:
          // Handle unauthorized
          console.error('Unauthorized access');
          break;
        case 403:
          // Handle forbidden
          console.error('Forbidden access');
          break;
        case 404:
          // Handle not found
          console.error('Resource not found');
          break;
        case 500:
          // Handle server error
          console.error('Server error');
          break;
        default:
          console.error('API error:', error.response.data);
      }
    }
    return Promise.reject(error);
  }
);

export default api;
