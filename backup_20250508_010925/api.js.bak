import axios from 'axios';
import config from '../config';

// Helper function to get JWT token from local storage
const getToken = () => {
  return localStorage.getItem('access_token') || localStorage.getItem('token') || '';
};

// Create axios instance with default config
const api = axios.create({
  baseURL: config.baseURL || '',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Legal Rights API
export const legalRightsApi = {
  getRights: async (category) => {
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
  sendMessage: async (params, taskType) => {
    try {
      // Handle both old and new parameter formats for backward compatibility
      let message, task_type;
      
      if (typeof params === 'object') {
        // New format: {message: '...', task_type: '...'}
        message = params.message;
        task_type = params.task_type || 'chat';
      } else {
        // Old format: (message, taskType)
        message = params;
        task_type = taskType || 'chat';
      }
      
      const response = await fetch('/api/legal/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
          message,
          task_type,
          include_model_info: true
        }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Failed to send message');
      }

      return response.json();
    } catch (error) {
      console.error('Error sending message:', error);
      throw error;
    }
  },

  // Add specialized endpoints for different tasks
  generateDocument: async (prompt, documentType) => {
    try {
      const response = await fetch('/api/legal/draft', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
          prompt,
          document_type: documentType,
          task_type: 'document_drafting'
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to generate document');
      }

      return response.json();
    } catch (error) {
      console.error('Error generating document:', error);
      throw error;
    }
  },

  researchRights: async (query) => {
    try {
      const response = await fetch('/api/legal/research', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
          query,
          task_type: 'rights_research'
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to research rights');
      }

      return response.json();
    } catch (error) {
      console.error('Error researching rights:', error);
      throw error;
    }
  },

  analyzeLegal: async (query) => {
    try {
      const response = await fetch('/api/legal/analyze', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
          query,
          task_type: 'complex_analysis'
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to analyze legal text');
      }

      return response.json();
    } catch (error) {
      console.error('Error analyzing legal text:', error);
      throw error;
    }
  }
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
  
  getDocumentById: async (documentId) => {
    try {
      const response = await api.get(`/api/documents/${documentId}`);
      return response.data;
    } catch (error) {
      console.error('Error fetching document by ID:', error);
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
  saveDocument: async (documentData) => {
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
  
  // New delete document method
  deleteDocument: async (documentId) => {
    try {
      const response = await api.delete(`/api/documents/${documentId}`);
      return response.data;
    } catch (error) {
      console.error('Error deleting document:', error);
      throw error;
    }
  },

  // New endpoints for document versioning
  getDocumentVersions: async (documentId) => {
    try {
      const response = await api.get(`/api/documents/${documentId}/versions`);
      return response.data;
    } catch (error) {
      console.error('Error fetching document versions:', error);
      throw error;
    }
  },
  
  revertToVersion: async (documentId, versionNumber) => {
    try {
      const response = await api.post(`/api/documents/${documentId}/versions/${versionNumber}`);
      return response.data;
    } catch (error) {
      console.error('Error reverting document to version:', error);
      throw error;
    }
  },
  
  // New endpoints for document templates
  saveTemplate: async (templateData) => {
    try {
      const response = await api.post('/api/documents/templates', templateData);
      return response.data;
    } catch (error) {
      console.error('Error saving template:', error);
      throw error;
    }
  },
  
  getTemplateById: async (templateId) => {
    try {
      const response = await api.get(`/api/documents/templates/${templateId}`);
      return response.data;
    } catch (error) {
      console.error('Error fetching template:', error);
      throw error;
    }
  },
  
  // New endpoint for document editing
  updateDocument: async (documentId, documentData) => {
    try {
      const response = await api.put(`/api/documents/${documentId}`, documentData);
      return response.data;
    } catch (error) {
      console.error('Error updating document:', error);
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

  // New endpoint for document tagging
  updateDocumentTags: async (documentId, tags) => {
    try {
      const response = await api.put(`/api/documents/${documentId}/tags`, { tags });
      return response.data;
    } catch (error) {
      console.error('Error updating document tags:', error);
      throw error;
    }
  },
  
  // New endpoint for categorizing documents
  updateDocumentCategory: async (documentId, category) => {
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

  // Get common tags
  getCommonTags: async () => {
    try {
      const response = await api.get('/api/documents/tags/common');
      return response.data;
    } catch (error) {
      console.error('Error fetching common tags:', error);
      throw error;
    }
  },

  // Share document via email
  shareDocumentViaEmail: async (documentId, emailDetails) => {
    try {
      const response = await api.post(`/api/documents/${documentId}/share`, emailDetails);
      return response.data;
    } catch (error) {
      console.error('Error sharing document via email:', error);
      throw error;
    }
  },

  async scanDocument(file, documentType = 'general') {
    try {
      const formData = new FormData();
      formData.append('file', file);
      formData.append('documentType', documentType);
      
      console.log('Attempting to scan document:', file.name, 'type:', documentType);
      
      // Add a test mode that bypasses the backend for testing
      if (process.env.NODE_ENV === 'development' || window.location.href.includes('scanner-test')) {
        console.log('TEST MODE: Simulating document scanning...');
        
        // Simulate processing delay
        await new Promise(resolve => setTimeout(resolve, 1500));
        
        // Create a FileReader to read the image
        const reader = new FileReader();
        
        // Return a promise that resolves when the file is read
        return new Promise((resolve, reject) => {
          reader.onload = () => {
            let mockExtractedText = '';
            let mockExtractedData = {};
            
            // Generate different mock responses based on document type
            switch(documentType) {
              case 'identification':
                mockExtractedText = "NAME: JOHN DOE\nDOB: 01/15/1985\nADDRESS: 123 MAIN ST, ANYTOWN, CA 94000\nID#: DL12345678\nISSUE DATE: 01/20/2020\nEXPIRY DATE: 01/15/2025";
                mockExtractedData = {
                  documentType: 'identification',
                  documentClass: 'drivers_license',
                  personalInfo: {
                    fullName: 'John Doe',
                    dateOfBirth: '01/15/1985',
                    address: '123 Main St, Anytown, CA 94000',
                  },
                  idDetails: {
                    idNumber: 'DL12345678',
                    issueDate: '01/20/2020',
                    expiryDate: '01/15/2025',
                    isValid: true
                  }
                };
                break;
                
              case 'immigration':
                mockExtractedText = "USCIS FORM I-94\nAdmission Number: 123456789012\nLast Name: SMITH\nFirst Name: JANE\nBirth Date: 02/23/1990\nCountry of Citizenship: CANADA\nDate of Entry: 10/15/2022\nClass of Admission: B-2\nAdmitted Until: 04/14/2023";
                mockExtractedData = {
                  documentType: 'immigration',
                  documentClass: 'i94',
                  personalInfo: {
                    lastName: 'Smith',
                    firstName: 'Jane',
                    dateOfBirth: '02/23/1990',
                    citizenship: 'Canada'
                  },
                  immigrationDetails: {
                    admissionNumber: '123456789012',
                    entryDate: '10/15/2022',
                    admissionClass: 'B-2',
                    admittedUntil: '04/14/2023',
                    status: 'Valid'
                  }
                };
                break;
                
              case 'legal':
                mockExtractedText = "CONTRACT OF EMPLOYMENT\nBETWEEN: ABC Company Inc. (\"Employer\")\nAND: Sarah Johnson (\"Employee\")\nTITLE: Marketing Manager\nSTART DATE: March 1, 2023\nSALARY: $75,000 per annum\nTERM: Indefinite, Full-time employment\nPROBATION PERIOD: 90 days\nSIGNED: ____________\nDATE: February 15, 2023";
                mockExtractedData = {
                  documentType: 'legal',
                  documentClass: 'employment_contract',
                  parties: {
                    employer: 'ABC Company Inc.',
                    employee: 'Sarah Johnson'
                  },
                  terms: {
                    position: 'Marketing Manager',
                    startDate: 'March 1, 2023',
                    compensation: '$75,000 per annum',
                    employmentType: 'Indefinite, Full-time',
                    probationPeriod: '90 days'
                  },
                  execution: {
                    signatureDate: 'February 15, 2023',
                    isFullyExecuted: false
                  }
                };
                break;
                
              default:
                mockExtractedText = "This is simulated OCR text for testing purposes. The actual OCR would extract real text from your document. This appears to be a general document with various paragraphs of information. The quality of the document will affect OCR accuracy.";
                mockExtractedData = {
                  documentType: documentType,
                  fileType: file.type,
                  fileName: file.name,
                  fileSize: file.size,
                  dateScanned: new Date().toISOString(),
                  testMode: true,
                  contentSummary: 'General document with text content'
                };
            }
            
            // Create mock OCR results
            const mockResult = {
              success: true,
              extractedText: mockExtractedText,
              extractedData: mockExtractedData,
              fileUrl: reader.result,
              confidence: 0.92,
              processingTimestamp: new Date().toISOString(),
              processingTimeMs: 1253,
              pageCount: 1
            };
            
            console.log('Mock scan result:', mockResult);
            resolve(mockResult);
          };
          
          reader.onerror = () => {
            reject(new Error('Failed to read the file'));
          };
          
          // Read the file as a data URL
          reader.readAsDataURL(file);
        });
      }
      
      // If not in test mode, use the real API
      const response = await fetch('/api/documents/scan', {
        method: 'POST',
        body: formData,
      });
      
      if (!response.ok) {
        const errorData = await response.json();
        console.error('Error scanning document:', errorData);
        throw new Error(errorData.error || 'Failed to scan document');
      }
      
      return await response.json();
    } catch (error) {
      console.error('Error in scanDocument API call:', error);
      throw error;
    }
  },
};

// Immigration Services API
export const immigrationApi = {
  async getVisaRequirements(visaType, accessToken) {
    try {
      const token = accessToken || getToken();
      const response = await fetch('/api/immigration/visa-requirements?type=' + visaType, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + token
        }
      });
      
      if (!response.ok) {
        throw new Error(`Error fetching visa requirements: ${response.statusText}`);
      }
      
      return await response.json();
    } catch (error) {
      console.error('Error in getVisaRequirements:', error);
      throw error;
    }
  },

  async submitApplication(applicationData, accessToken) {
    try {
      const token = accessToken || getToken();
      const response = await fetch('/api/immigration/submit-application', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + token
        },
        body: JSON.stringify(applicationData)
      });
      
      if (!response.ok) {
        throw new Error(`Error submitting immigration application: ${response.statusText}`);
      }
      
      return await response.json();
    } catch (error) {
      console.error('Error in submitApplication:', error);
      throw error;
    }
  },
  
  async submitImmigrationForm(formData, accessToken) {
    try {
      const token = accessToken || getToken();
      const response = await fetch('/api/immigration/intake-form', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + token
        },
        body: JSON.stringify(formData)
      });
      
      if (!response.ok) {
        throw new Error(`Error submitting immigration form: ${response.statusText}`);
      }
      
      return await response.json();
    } catch (error) {
      console.error('Error in submitImmigrationForm:', error);
      throw error;
    }
  },

  // New methods for managing immigration intake forms
  async getIntakeForms(accessToken) {
    try {
      const token = accessToken || getToken();
      const response = await fetch('/api/immigration/intake-forms', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + token
        }
      });
      
      if (!response.ok) {
        throw new Error(`Error fetching immigration forms: ${response.statusText}`);
      }
      
      return await response.json();
    } catch (error) {
      console.error('Error in getIntakeForms:', error);
      throw error;
    }
  },

  async getIntakeFormById(formId, accessToken) {
    try {
      const token = accessToken || getToken();
      const response = await fetch('/api/immigration/intake-forms/' + formId, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + token
        }
      });
      
      if (!response.ok) {
        throw new Error(`Error fetching immigration form: ${response.statusText}`);
      }
      
      return await response.json();
    } catch (error) {
      console.error('Error in getIntakeFormById:', error);
      throw error;
    }
  },

  async updateFormStatus(formId, status, accessToken) {
    try {
      const token = accessToken || getToken();
      const response = await fetch('/api/immigration/intake-forms/' + formId + '/status', {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + token
        },
        body: JSON.stringify({ status })
      });
      
      if (!response.ok) {
        throw new Error(`Error updating form status: ${response.statusText}`);
      }
      
      return await response.json();
    } catch (error) {
      console.error('Error in updateFormStatus:', error);
      throw error;
    }
  },

  // New methods for the Immigration Dashboard
  async getCases(accessToken) {
    try {
      const token = accessToken || getToken();
      const response = await fetch('/api/immigration/cases', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + token
        }
      });
      
      if (!response.ok) {
        throw new Error(`Error fetching immigration cases: ${response.statusText}`);
      }
      
      return await response.json();
    } catch (error) {
      console.error('Error in getCases:', error);
      throw error;
    }
  },

  async getCaseById(caseId, accessToken) {
    try {
      const token = accessToken || getToken();
      const response = await fetch('/api/immigration/cases/' + caseId, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + token
        }
      });
      
      if (!response.ok) {
        throw new Error(`Error fetching immigration case: ${response.statusText}`);
      }
      
      return await response.json();
    } catch (error) {
      console.error('Error in getCaseById:', error);
      throw error;
    }
  },

  async updateCaseStatus(caseId, status, accessToken) {
    try {
      const token = accessToken || getToken();
      const response = await fetch('/api/immigration/cases/' + caseId + '/status', {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + token
        },
        body: JSON.stringify({ status })
      });
      
      if (!response.ok) {
        throw new Error(`Error updating case status: ${response.statusText}`);
      }
      
      return await response.json();
    } catch (error) {
      console.error('Error in updateCaseStatus:', error);
      throw error;
    }
  },

  async uploadCaseDocument(caseId, file, documentType, accessToken) {
    try {
      const token = accessToken || getToken();
      const formData = new FormData();
      formData.append('file', file);
      formData.append('documentType', documentType);
      
      const response = await fetch('/api/immigration/cases/' + caseId + '/documents', {
        method: 'POST',
        headers: {
          'Authorization': 'Bearer ' + token
        },
        body: formData
      });
      
      if (!response.ok) {
        throw new Error(`Error uploading document: ${response.statusText}`);
      }
      
      return await response.json();
    } catch (error) {
      console.error('Error in uploadCaseDocument:', error);
      throw error;
    }
  },

  async getCaseDocuments(caseId, accessToken) {
    try {
      const token = accessToken || getToken();
      const response = await fetch('/api/immigration/cases/' + caseId + '/documents', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + token
        }
      });
      
      if (!response.ok) {
        throw new Error(`Error fetching case documents: ${response.statusText}`);
      }
      
      return await response.json();
    } catch (error) {
      console.error('Error in getCaseDocuments:', error);
      throw error;
    }
  },

  async getNotifications(accessToken) {
    try {
      const token = accessToken || getToken();
      const response = await fetch('/api/immigration/notifications', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + token
        }
      });
      
      if (!response.ok) {
        throw new Error(`Error fetching notifications: ${response.statusText}`);
      }
      
      return await response.json();
    } catch (error) {
      console.error('Error in getNotifications:', error);
      throw error;
    }
  },

  async markNotificationAsRead(notificationId, accessToken) {
    try {
      const token = accessToken || getToken();
      const response = await fetch('/api/immigration/notifications/' + notificationId + '/read', {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + token
        }
      });
      
      if (!response.ok) {
        throw new Error(`Error marking notification as read: ${response.statusText}`);
      }
      
      return await response.json();
    } catch (error) {
      console.error('Error in markNotificationAsRead:', error);
      throw error;
    }
  },

  async getUpcomingEvents(accessToken) {
    try {
      const token = accessToken || getToken();
      const response = await fetch('/api/immigration/events', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + token
        }
      });
      
      if (!response.ok) {
        throw new Error(`Error fetching upcoming events: ${response.statusText}`);
      }
      
      return await response.json();
    } catch (error) {
      console.error('Error in getUpcomingEvents:', error);
      throw error;
    }
  }
};

// Expungement Services API
export const expungementApi = {
  checkEligibility: async (caseData) => {
    try {
      const response = await api.post('/api/expungement/check-eligibility', caseData);
      return response.data;
    } catch (error) {
      console.error('Error checking expungement eligibility:', error);
      throw error;
    }
  },

  getStateRules: async (state) => {
    try {
      const response = await api.get('/api/expungement/rules/' + state);
      return response.data;
    } catch (error) {
      console.error('Error fetching state rules:', error);
      throw error;
    }
  },

  startExpungementProcess: async (caseData) => {
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
      const response = await api.put('/api/expungement/' + caseId + '/progress', progressData);
      return response.data;
    } catch (error) {
      console.error('Error saving progress:', error);
      throw error;
    }
  },

  getRequiredDocuments: async (state, caseType) => {
    try {
      const response = await api.get('/api/expungement/documents/' + state + '/' + caseType);
      return response.data;
    } catch (error) {
      console.error('Error fetching required documents:', error);
      throw error;
    }
  }
};

// Feedback API
export const feedbackApi = {
  submit: async (feedbackData) => {
    try {
      const response = await fetch('/api/feedback', {
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
      const response = await fetch('/api/feedback/analytics');
      
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
  save: async (conversationData) => {
    try {
      const response = await fetch('/api/conversations', {
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

  getByUserId: async (userId) => {
    try {
      const response = await fetch('/api/conversations/' + userId);
      
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
      const response = await fetch('/api/contracts/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          template: templateName.toLowerCase().replace(/\s+/g, '_'),
          data: formData,
          language: language
        })
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
      const response = await fetch('/api/contracts/templates');
      if (!response.ok) {
        throw new Error('Failed to fetch templates');
      }
      return response.json();
    } catch (error) {
      console.error('Error fetching templates:', error);
      throw error;
    }
  }
};

// Error interceptor
api.interceptors.response.use(
  (response) => response,
  (error) => {
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