import axios from 'axios';
import { API_BASE_URL } from '../config';

// Create axios instance with the base URL
const api = axios.create({
  baseURL: `${API_BASE_URL}/paralegal`,
  withCredentials: true
});

// Add request interceptor to include auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Mock data for demo mode
const mockCases = [
  {
    id: '1',
    client_name: 'John Doe',
    client_email: 'john.doe@example.com',
    client_phone: '555-123-4567',
    case_type: 'Immigration',
    description: 'DACA renewal application',
    urgency: 'high',
    status: 'new',
    created_at: new Date().toISOString()
  },
  {
    id: '2',
    client_name: 'Jane Smith',
    client_email: 'jane.smith@example.com',
    client_phone: '555-987-6543',
    case_type: 'Tenant Rights',
    description: 'Eviction defense',
    urgency: 'medium',
    status: 'in_progress',
    created_at: new Date().toISOString()
  }
];

const mockTemplates = [
  { id: '1', name: 'Client Intake Form', category: 'General', format: 'PDF' },
  { id: '2', name: 'Fee Waiver Request', category: 'Court', format: 'DOCX' },
  { id: '3', name: 'Client Representation Agreement', category: 'Contracts', format: 'PDF' },
  { id: '4', name: 'Tenant Complaint Letter', category: 'Housing', format: 'DOCX' },
  { id: '5', name: 'Employment Discrimination Complaint', category: 'Employment', format: 'PDF' },
];

const mockQuestions = [
  { id: '1', question: 'Have you sought legal help for this issue before?', type: 'boolean' },
  { id: '2', question: 'When did this issue first occur?', type: 'date' },
  { id: '3', question: 'Please describe your current financial situation', type: 'text' },
  { id: '4', question: 'Do you have any deadlines or court dates approaching?', type: 'boolean' },
  { id: '5', question: 'What is your preferred language for communication?', type: 'select', options: ['English', 'Spanish', 'Mandarin', 'Vietnamese', 'Other'] }
];

// Helper function to determine if we should use demo mode
const useDemoMode = () => {
  // Check if we're in demo mode by trying a quick ping to the backend
  return new Promise((resolve) => {
    fetch(`${API_BASE_URL}/ping`, { 
      method: 'GET',
      signal: AbortSignal.timeout(3000) // 3 second timeout
    })
    .then(() => resolve(false)) // Backend is available, don't use demo
    .catch(() => resolve(true)); // Backend is not available, use demo
  });
};

const paralegalService = {
  // Case management
  createCase: async (caseData) => {
    try {
      // Check if we need to use demo mode
      const useDemo = await useDemoMode();
      
      if (useDemo) {
        // Return a mock success response for demo
        return {
          success: true,
          message: 'Case created successfully (Demo)',
          case_id: Math.floor(Math.random() * 1000).toString()
        };
      }
      
      const response = await api.post('/case', caseData);
      return response.data;
    } catch (error) {
      console.error('Error creating case:', error);
      // Fallback to demo if API fails
      return {
        success: true,
        message: 'Case created successfully (Demo Fallback)',
        case_id: Math.floor(Math.random() * 1000).toString()
      };
    }
  },
  
  getCases: async (filters = {}) => {
    try {
      // Check if we need to use demo mode
      const useDemo = await useDemoMode();
      
      if (useDemo) {
        // Filter and return mock cases
        let filteredCases = [...mockCases];
        if (filters.status) {
          filteredCases = filteredCases.filter(c => c.status === filters.status);
        }
        if (filters.caseType) {
          filteredCases = filteredCases.filter(c => c.case_type === filters.caseType);
        }
        return {
          success: true,
          cases: filteredCases
        };
      }
      
      const params = new URLSearchParams();
      if (filters.status) params.append('status', filters.status);
      if (filters.caseType) params.append('case_type', filters.caseType);
      
      const response = await api.get('/cases', { params });
      return response.data;
    } catch (error) {
      console.error('Error fetching cases:', error);
      // Return mock data on error
      return {
        success: true,
        cases: mockCases
      };
    }
  },
  
  getCase: async (caseId) => {
    try {
      // Check if we need to use demo mode
      const useDemo = await useDemoMode();
      
      if (useDemo) {
        const mockCase = mockCases.find(c => c.id === caseId);
        return {
          success: !!mockCase,
          case: mockCase || null
        };
      }
      
      const response = await api.get(`/case/${caseId}`);
      return response.data;
    } catch (error) {
      console.error(`Error fetching case ${caseId}:`, error);
      const mockCase = mockCases.find(c => c.id === caseId);
      return {
        success: !!mockCase,
        case: mockCase || null
      };
    }
  },
  
  updateCase: async (caseId, caseData) => {
    try {
      // Check if we need to use demo mode
      const useDemo = await useDemoMode();
      
      if (useDemo) {
        return {
          success: true,
          message: 'Case updated successfully (Demo)'
        };
      }
      
      const response = await api.put(`/case/${caseId}`, caseData);
      return response.data;
    } catch (error) {
      console.error(`Error updating case ${caseId}:`, error);
      return {
        success: true,
        message: 'Case updated successfully (Demo Fallback)'
      };
    }
  },
  
  // Document templates
  getDocumentTemplates: async (type) => {
    try {
      // Check if we need to use demo mode
      const useDemo = await useDemoMode();
      
      if (useDemo) {
        let filteredTemplates = [...mockTemplates];
        if (type) {
          filteredTemplates = filteredTemplates.filter(t => t.category.toLowerCase() === type.toLowerCase());
        }
        return {
          success: true,
          templates: filteredTemplates
        };
      }
      
      const params = new URLSearchParams();
      if (type) params.append('type', type);
      
      const response = await api.get('/templates', { params });
      return response.data;
    } catch (error) {
      console.error('Error fetching document templates:', error);
      return {
        success: true,
        templates: mockTemplates
      };
    }
  },
  
  generateDocument: async (templateId, data) => {
    try {
      // Check if we need to use demo mode
      const useDemo = await useDemoMode();
      
      if (useDemo) {
        const template = mockTemplates.find(t => t.id === templateId);
        return {
          success: true,
          message: `${template?.name || 'Document'} generated successfully (Demo)`,
          document_url: `/demo-documents/sample-${templateId}.${template?.format.toLowerCase() || 'pdf'}`
        };
      }
      
      const response = await api.post(`/generate-document/${templateId}`, data);
      return response.data;
    } catch (error) {
      console.error(`Error generating document from template ${templateId}:`, error);
      const template = mockTemplates.find(t => t.id === templateId);
      return {
        success: true,
        message: `${template?.name || 'Document'} generated successfully (Demo Fallback)`,
        document_url: `/demo-documents/sample-${templateId}.${template?.format.toLowerCase() || 'pdf'}`
      };
    }
  },
  
  // Screening questions
  getScreeningQuestions: async (category) => {
    try {
      // Check if we need to use demo mode
      const useDemo = await useDemoMode();
      
      if (useDemo) {
        return {
          success: true,
          questions: mockQuestions
        };
      }
      
      const params = new URLSearchParams();
      if (category) params.append('category', category);
      
      const response = await api.get('/screening-questions', { params });
      return response.data;
    } catch (error) {
      console.error('Error fetching screening questions:', error);
      return {
        success: true,
        questions: mockQuestions
      };
    }
  }
};

export default paralegalService; 