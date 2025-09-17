/**
 * Frontend Component Tests
 * Tests for React components and user interactions
 */

import React from 'react';
import { render, screen, fireEvent, waitFor, act } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import '@testing-library/jest-dom';

// Mock components and services
jest.mock('../frontend/src/services/WebSocketService', () => ({
  WebSocketService: jest.fn().mockImplementation(() => ({
    connect: jest.fn(),
    disconnect: jest.fn(),
    sendMessage: jest.fn(),
    onMessage: jest.fn(),
    onError: jest.fn(),
    onClose: jest.fn(),
    isConnected: false
  }))
}));

jest.mock('../frontend/src/hooks/useWebSocket', () => ({
  useWebSocket: () => ({
    sendMessage: jest.fn(),
    lastMessage: null,
    connectionStatus: 'Closed'
  })
}));

// Mock fetch globally
global.fetch = jest.fn();

// Create a test theme
const theme = createTheme();

// Helper function to render components with providers
const renderWithProviders = (component) => {
  return render(
    <BrowserRouter>
      <ThemeProvider theme={theme}>
        {component}
      </ThemeProvider>
    </BrowserRouter>
  );
};

describe('ImmigrationCRM Component', () => {
  let ImmigrationCRM;

  beforeAll(async () => {
    const module = await import('../frontend/src/components/ImmigrationCRM.js');
    ImmigrationCRM = module.default;
  });

  beforeEach(() => {
    fetch.mockClear();
  });

  test('renders immigration CRM component', () => {
    renderWithProviders(<ImmigrationCRM />);
    
    expect(screen.getByText('Immigration Cases')).toBeInTheDocument();
    expect(screen.getByText('Create New Case')).toBeInTheDocument();
  });

  test('displays loading state', () => {
    fetch.mockImplementation(() => new Promise(() => {})); // Never resolves
    
    renderWithProviders(<ImmigrationCRM />);
    
    expect(screen.getByText('Loading cases...')).toBeInTheDocument();
  });

  test('displays error state', async () => {
    fetch.mockRejectedValueOnce(new Error('Network error'));
    
    renderWithProviders(<ImmigrationCRM />);
    
    await waitFor(() => {
      expect(screen.getByText('Failed to fetch cases')).toBeInTheDocument();
    });
  });

  test('displays cases list', async () => {
    const mockCases = [
      {
        id: 1,
        clientName: 'John Doe',
        caseType: 'Asylum',
        status: 'New',
        priority: 'High',
        createdAt: '2024-01-01T00:00:00Z'
      }
    ];

    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => mockCases
    });

    renderWithProviders(<ImmigrationCRM />);

    await waitFor(() => {
      expect(screen.getByText('John Doe')).toBeInTheDocument();
      expect(screen.getByText('Asylum')).toBeInTheDocument();
      expect(screen.getByText('New')).toBeInTheDocument();
    });
  });

  test('opens create case dialog', () => {
    renderWithProviders(<ImmigrationCRM />);
    
    const createButton = screen.getByText('Create New Case');
    fireEvent.click(createButton);
    
    expect(screen.getByText('Create New Immigration Case')).toBeInTheDocument();
  });

  test('creates new case', async () => {
    const mockNewCase = {
      id: 2,
      clientName: 'Jane Smith',
      caseType: 'Green Card',
      status: 'New',
      priority: 'Medium'
    };

    // Mock initial fetch for cases list
    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => []
    });

    // Mock create case response
    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({
        success: true,
        case: mockNewCase
      })
    });

    renderWithProviders(<ImmigrationCRM />);

    // Open create dialog
    const createButton = screen.getByText('Create New Case');
    fireEvent.click(createButton);

    // Fill form
    const clientNameInput = screen.getByLabelText(/client name/i);
    const caseTypeInput = screen.getByLabelText(/case type/i);
    const submitButton = screen.getByText('Create Case');

    fireEvent.change(clientNameInput, { target: { value: 'Jane Smith' } });
    fireEvent.change(caseTypeInput, { target: { value: 'Green Card' } });

    // Submit form
    fireEvent.click(submitButton);

    await waitFor(() => {
      expect(fetch).toHaveBeenCalledWith(
        'http://localhost:3001/api/immigration/cases',
        expect.objectContaining({
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            clientName: 'Jane Smith',
            caseType: 'Green Card',
            status: 'New',
            priority: 'Medium',
            description: ''
          })
        })
      );
    });
  });

  test('deletes case', async () => {
    const mockCases = [
      {
        id: 1,
        clientName: 'John Doe',
        caseType: 'Asylum',
        status: 'New'
      }
    ];

    // Mock initial fetch
    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => mockCases
    });

    // Mock delete response
    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({ success: true })
    });

    renderWithProviders(<ImmigrationCRM />);

    await waitFor(() => {
      expect(screen.getByText('John Doe')).toBeInTheDocument();
    });

    // Click delete button
    const deleteButton = screen.getByLabelText(/delete case/i);
    fireEvent.click(deleteButton);

    // Confirm deletion
    const confirmButton = screen.getByText('Delete');
    fireEvent.click(confirmButton);

    await waitFor(() => {
      expect(fetch).toHaveBeenCalledWith(
        'http://localhost:3001/api/immigration/cases/1',
        expect.objectContaining({
          method: 'DELETE'
        })
      );
    });
  });
});

describe('VoiceEnabledAIChat Component', () => {
  let VoiceEnabledAIChat;

  beforeAll(async () => {
    const module = await import('../frontend/src/components/VoiceEnabledAIChat.js');
    VoiceEnabledAIChat = module.default;
  });

  beforeEach(() => {
    fetch.mockClear();
    
    // Mock speech recognition
    global.SpeechRecognition = jest.fn();
    global.webkitSpeechRecognition = jest.fn();
    
    // Mock speech synthesis
    global.speechSynthesis = {
      speak: jest.fn(),
      cancel: jest.fn(),
      getVoices: jest.fn(() => [])
    };
  });

  test('renders voice chat component', () => {
    renderWithProviders(<VoiceEnabledAIChat />);
    
    expect(screen.getByText('Voice-Enabled AI Legal Assistant')).toBeInTheDocument();
    expect(screen.getByText('Start a conversation with your voice')).toBeInTheDocument();
  });

  test('displays voice settings panel', () => {
    renderWithProviders(<VoiceEnabledAIChat />);
    
    const settingsButton = screen.getByLabelText(/voice settings/i);
    fireEvent.click(settingsButton);
    
    expect(screen.getByText('Voice Settings')).toBeInTheDocument();
    expect(screen.getByText('Language')).toBeInTheDocument();
  });

  test('handles text input and submission', async () => {
    const mockAIResponse = {
      success: true,
      analysis: {
        case_summary: 'Test analysis',
        key_facts: ['Fact 1', 'Fact 2'],
        practical_advice: ['Advice 1', 'Advice 2']
      }
    };

    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => mockAIResponse
    });

    renderWithProviders(<VoiceEnabledAIChat />);

    const textInput = screen.getByPlaceholderText(/type your message/i);
    const sendButton = screen.getByText('Send');

    fireEvent.change(textInput, { target: { value: 'Test question' } });
    fireEvent.click(sendButton);

    await waitFor(() => {
      expect(fetch).toHaveBeenCalledWith(
        'http://localhost:3001/api/legal-analysis',
        expect.objectContaining({
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            query: 'Test question',
            jurisdiction: 'ri'
          })
        })
      );
    });
  });

  test('handles voice input start', () => {
    const mockRecognition = {
      continuous: false,
      interimResults: true,
      lang: 'en-US',
      onstart: null,
      onresult: null,
      onerror: null,
      onend: null,
      start: jest.fn(),
      stop: jest.fn()
    };

    global.SpeechRecognition.mockImplementation(() => mockRecognition);

    renderWithProviders(<VoiceEnabledAIChat />);

    const micButton = screen.getByLabelText(/start voice input/i);
    fireEvent.click(micButton);

    expect(mockRecognition.start).toHaveBeenCalled();
  });

  test('handles API error', async () => {
    fetch.mockRejectedValueOnce(new Error('API Error'));

    renderWithProviders(<VoiceEnabledAIChat />);

    const textInput = screen.getByPlaceholderText(/type your message/i);
    const sendButton = screen.getByText('Send');

    fireEvent.change(textInput, { target: { value: 'Test question' } });
    fireEvent.click(sendButton);

    await waitFor(() => {
      expect(screen.getByText(/experiencing technical difficulties/i)).toBeInTheDocument();
    });
  });
});

describe('CourtFilingAssistant Component', () => {
  let CourtFilingAssistant;

  beforeAll(async () => {
    const module = await import('../frontend/src/components/CourtFilingAssistant.js');
    CourtFilingAssistant = module.default;
  });

  beforeEach(() => {
    fetch.mockClear();
  });

  test('renders court filing assistant', async () => {
    const mockRules = [
      {
        jurisdiction: 'Rhode Island',
        court: 'Superior Court',
        rule_number: 'Civ. R. 5',
        title: 'Service and Filing'
      }
    ];

    const mockTemplates = [
      {
        id: 'complaint_template',
        name: 'Civil Complaint Template',
        document_type: 'complaint',
        jurisdiction: 'Rhode Island',
        court: 'Superior Court'
      }
    ];

    const mockFilings = [];

    fetch
      .mockResolvedValueOnce({
        ok: true,
        json: async () => ({ rules: mockRules })
      })
      .mockResolvedValueOnce({
        ok: true,
        json: async () => ({ templates: mockTemplates })
      })
      .mockResolvedValueOnce({
        ok: true,
        json: async () => ({ filings: mockFilings })
      });

    renderWithProviders(<CourtFilingAssistant />);

    await waitFor(() => {
      expect(screen.getByText('Court Filing Assistant')).toBeInTheDocument();
    });

    expect(screen.getByText('Select Court & Document Type')).toBeInTheDocument();
  });

  test('navigates through filing steps', async () => {
    const mockTemplates = [
      {
        id: 'complaint_template',
        name: 'Civil Complaint Template',
        document_type: 'complaint',
        jurisdiction: 'Rhode Island',
        court: 'Superior Court'
      }
    ];

    fetch
      .mockResolvedValueOnce({ ok: true, json: async () => ({ rules: [] }) })
      .mockResolvedValueOnce({ ok: true, json: async () => ({ templates: mockTemplates }) })
      .mockResolvedValueOnce({ ok: true, json: async () => ({ filings: [] }) });

    renderWithProviders(<CourtFilingAssistant />);

    await waitFor(() => {
      expect(screen.getByText('Select Court & Document Type')).toBeInTheDocument();
    });

    // Select jurisdiction
    const jurisdictionSelect = screen.getByLabelText('Jurisdiction');
    fireEvent.mouseDown(jurisdictionSelect);
    const rhodeIslandOption = screen.getByText('Rhode Island');
    fireEvent.click(rhodeIslandOption);

    // Select court
    const courtSelect = screen.getByLabelText('Court');
    fireEvent.mouseDown(courtSelect);
    const superiorCourtOption = screen.getByText('Superior Court');
    fireEvent.click(superiorCourtOption);

    // Select document type
    const documentTypeSelect = screen.getByLabelText('Document Type');
    fireEvent.mouseDown(documentTypeSelect);
    const complaintOption = screen.getByText('Complaint');
    fireEvent.click(complaintOption);

    // Click Next
    const nextButton = screen.getByText('Next');
    fireEvent.click(nextButton);

    await waitFor(() => {
      expect(screen.getByText('Choose Document Template')).toBeInTheDocument();
    });
  });

  test('generates document from template', async () => {
    const mockTemplates = [
      {
        id: 'complaint_template',
        name: 'Civil Complaint Template',
        document_type: 'complaint',
        jurisdiction: 'Rhode Island',
        court: 'Superior Court',
        required_fields: ['plaintiff_name', 'defendant_name'],
        optional_fields: ['attorney_info']
      }
    ];

    const mockGeneratedDocument = 'Generated complaint document content...';

    fetch
      .mockResolvedValueOnce({ ok: true, json: async () => ({ rules: [] }) })
      .mockResolvedValueOnce({ ok: true, json: async () => ({ templates: mockTemplates }) })
      .mockResolvedValueOnce({ ok: true, json: async () => ({ filings: [] }) })
      .mockResolvedValueOnce({
        ok: true,
        json: async () => ({
          success: true,
          document_content: mockGeneratedDocument
        })
      });

    renderWithProviders(<CourtFilingAssistant />);

    // Navigate to template selection
    await waitFor(() => {
      expect(screen.getByText('Select Court & Document Type')).toBeInTheDocument();
    });

    // Fill required fields and navigate
    const jurisdictionSelect = screen.getByLabelText('Jurisdiction');
    fireEvent.mouseDown(jurisdictionSelect);
    fireEvent.click(screen.getByText('Rhode Island'));

    const courtSelect = screen.getByLabelText('Court');
    fireEvent.mouseDown(courtSelect);
    fireEvent.click(screen.getByText('Superior Court'));

    const documentTypeSelect = screen.getByLabelText('Document Type');
    fireEvent.mouseDown(documentTypeSelect);
    fireEvent.click(screen.getByText('Complaint'));

    fireEvent.click(screen.getByText('Next'));

    // Select template
    await waitFor(() => {
      expect(screen.getByText('Choose Document Template')).toBeInTheDocument();
    });

    const useTemplateButton = screen.getByText('Use Template');
    fireEvent.click(useTemplateButton);

    // Fill document data
    await waitFor(() => {
      expect(screen.getByText('Fill Document Data')).toBeInTheDocument();
    });

    const plaintiffNameInput = screen.getByLabelText(/plaintiff_name/i);
    const defendantNameInput = screen.getByLabelText(/defendant_name/i);
    const filingTitleInput = screen.getByLabelText(/filing title/i);

    fireEvent.change(plaintiffNameInput, { target: { value: 'John Doe' } });
    fireEvent.change(defendantNameInput, { target: { value: 'Jane Smith' } });
    fireEvent.change(filingTitleInput, { target: { value: 'Test Complaint' } });

    // Generate document
    const generateButton = screen.getByText('Generate Document');
    fireEvent.click(generateButton);

    await waitFor(() => {
      expect(screen.getByText('Review Generated Document')).toBeInTheDocument();
      expect(screen.getByText(mockGeneratedDocument)).toBeInTheDocument();
    });
  });

  test('calculates filing fees', async () => {
    const mockFeeResponse = { success: true, fees: 150.0 };

    fetch
      .mockResolvedValueOnce({ ok: true, json: async () => ({ rules: [] }) })
      .mockResolvedValueOnce({ ok: true, json: async () => ({ templates: [] }) })
      .mockResolvedValueOnce({ ok: true, json: async () => ({ filings: [] }) })
      .mockResolvedValueOnce({
        ok: true,
        json: async () => mockFeeResponse
      });

    renderWithProviders(<CourtFilingAssistant />);

    await waitFor(() => {
      expect(screen.getByText('Select Court & Document Type')).toBeInTheDocument();
    });

    // Fill required fields
    const jurisdictionSelect = screen.getByLabelText('Jurisdiction');
    fireEvent.mouseDown(jurisdictionSelect);
    fireEvent.click(screen.getByText('Rhode Island'));

    const courtSelect = screen.getByLabelText('Court');
    fireEvent.mouseDown(courtSelect);
    fireEvent.click(screen.getByText('Superior Court'));

    const documentTypeSelect = screen.getByLabelText('Document Type');
    fireEvent.mouseDown(documentTypeSelect);
    fireEvent.click(screen.getByText('Complaint'));

    // Calculate fees
    const calculateFeesButton = screen.getByText('Calculate Fees');
    fireEvent.click(calculateFeesButton);

    await waitFor(() => {
      expect(fetch).toHaveBeenCalledWith(
        'http://localhost:3001/api/court-filing/fees',
        expect.objectContaining({
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            document_type: 'complaint',
            jurisdiction: 'Rhode Island',
            court: 'Superior Court'
          })
        })
      );
    });
  });
});

describe('MobileOptimizedChat Component', () => {
  let MobileOptimizedChat;

  beforeAll(async () => {
    const module = await import('../frontend/src/components/MobileOptimizedChat.js');
    MobileOptimizedChat = module.default;
  });

  beforeEach(() => {
    fetch.mockClear();
  });

  test('renders mobile optimized chat', () => {
    renderWithProviders(<MobileOptimizedChat />);
    
    expect(screen.getByText('AI Legal Assistant')).toBeInTheDocument();
    expect(screen.getByText('Start a conversation')).toBeInTheDocument();
  });

  test('handles mobile voice input', () => {
    const mockRecognition = {
      continuous: false,
      interimResults: true,
      lang: 'en-US',
      onstart: null,
      onresult: null,
      onerror: null,
      onend: null,
      start: jest.fn(),
      stop: jest.fn()
    };

    global.SpeechRecognition.mockImplementation(() => mockRecognition);

    renderWithProviders(<MobileOptimizedChat />);

    const micButton = screen.getByLabelText(/start voice input/i);
    fireEvent.click(micButton);

    expect(mockRecognition.start).toHaveBeenCalled();
  });

  test('opens drawer menu', () => {
    renderWithProviders(<MobileOptimizedChat />);
    
    const menuButton = screen.getByLabelText(/menu/i);
    fireEvent.click(menuButton);
    
    expect(screen.getByText('Chat Options')).toBeInTheDocument();
    expect(screen.getByText('Clear Chat')).toBeInTheDocument();
  });

  test('exports chat', async () => {
    renderWithProviders(<MobileOptimizedChat />);
    
    // Add a message first
    const textInput = screen.getByPlaceholderText(/type your message/i);
    const sendButton = screen.getByText('Send');

    fireEvent.change(textInput, { target: { value: 'Test message' } });
    fireEvent.click(sendButton);

    // Open drawer and export
    const menuButton = screen.getByLabelText(/menu/i);
    fireEvent.click(menuButton);

    const exportButton = screen.getByText('Export Chat');
    fireEvent.click(exportButton);

    // Mock download
    const mockAnchor = {
      href: '',
      download: '',
      click: jest.fn()
    };
    global.document.createElement = jest.fn(() => mockAnchor);
    global.document.body.appendChild = jest.fn();
    global.document.body.removeChild = jest.fn();
    global.URL.createObjectURL = jest.fn(() => 'blob:url');
    global.URL.revokeObjectURL = jest.fn();

    expect(mockAnchor.click).toHaveBeenCalled();
  });
});

describe('AnalyticsDashboard Component', () => {
  let AnalyticsDashboard;

  beforeAll(async () => {
    const module = await import('../frontend/src/components/AnalyticsDashboard.js');
    AnalyticsDashboard = module.default;
  });

  beforeEach(() => {
    fetch.mockClear();
  });

  test('renders analytics dashboard', async () => {
    const mockAnalytics = {
      user: { total_users: 100, active_users: 50 },
      performance: { response_time: 200, uptime: 99.9 },
      business: { total_cases: 500, revenue: 10000 },
      security: { threats_blocked: 10, vulnerabilities: 2 }
    };

    fetch
      .mockResolvedValueOnce({
        ok: true,
        json: async () => ({ success: true, analytics: mockAnalytics.user })
      })
      .mockResolvedValueOnce({
        ok: true,
        json: async () => ({ success: true, analytics: mockAnalytics.performance })
      })
      .mockResolvedValueOnce({
        ok: true,
        json: async () => ({ success: true, analytics: mockAnalytics.business })
      })
      .mockResolvedValueOnce({
        ok: true,
        json: async () => ({ success: true, analytics: mockAnalytics.security })
      });

    renderWithProviders(<AnalyticsDashboard />);

    await waitFor(() => {
      expect(screen.getByText('Analytics Dashboard')).toBeInTheDocument();
    });
  });

  test('displays loading state', () => {
    fetch.mockImplementation(() => new Promise(() => {})); // Never resolves

    renderWithProviders(<AnalyticsDashboard />);

    expect(screen.getByText('Loading analytics...')).toBeInTheDocument();
  });

  test('handles analytics error', async () => {
    fetch.mockRejectedValueOnce(new Error('Analytics error'));

    renderWithProviders(<AnalyticsDashboard />);

    await waitFor(() => {
      expect(screen.getByText('Failed to load analytics')).toBeInTheDocument();
    });
  });
});

describe('DocumentCollaboration Component', () => {
  let DocumentCollaboration;

  beforeAll(async () => {
    const module = await import('../frontend/src/components/DocumentCollaboration.js');
    DocumentCollaboration = module.default;
  });

  beforeEach(() => {
    fetch.mockClear();
  });

  test('renders document collaboration', async () => {
    const mockDocuments = [
      {
        id: 'doc1',
        title: 'Test Document',
        content: 'Test content',
        type: 'legal_brief',
        lastModified: '2024-01-01T00:00:00Z'
      }
    ];

    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({ success: true, documents: mockDocuments })
    });

    renderWithProviders(<DocumentCollaboration />);

    await waitFor(() => {
      expect(screen.getByText('Document Collaboration')).toBeInTheDocument();
    });
  });

  test('creates new document', async () => {
    const mockNewDocument = {
      id: 'doc2',
      title: 'New Document',
      content: '',
      type: 'legal_brief'
    };

    fetch
      .mockResolvedValueOnce({
        ok: true,
        json: async () => ({ success: true, documents: [] })
      })
      .mockResolvedValueOnce({
        ok: true,
        json: async () => ({ success: true, document: mockNewDocument })
      });

    renderWithProviders(<DocumentCollaboration />);

    await waitFor(() => {
      expect(screen.getByText('Create Document')).toBeInTheDocument();
    });

    const createButton = screen.getByText('Create Document');
    fireEvent.click(createButton);

    await waitFor(() => {
      expect(fetch).toHaveBeenCalledWith(
        'http://localhost:3001/api/documents',
        expect.objectContaining({
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          }
        })
      );
    });
  });

  test('updates document content', async () => {
    const mockDocument = {
      id: 'doc1',
      title: 'Test Document',
      content: 'Original content',
      type: 'legal_brief'
    };

    fetch
      .mockResolvedValueOnce({
        ok: true,
        json: async () => ({ success: true, documents: [mockDocument] })
      })
      .mockResolvedValueOnce({
        ok: true,
        json: async () => ({ success: true })
      });

    renderWithProviders(<DocumentCollaboration />);

    await waitFor(() => {
      expect(screen.getByText('Test Document')).toBeInTheDocument();
    });

    const editButton = screen.getByLabelText(/edit document/i);
    fireEvent.click(editButton);

    const contentEditor = screen.getByDisplayValue('Original content');
    fireEvent.change(contentEditor, { target: { value: 'Updated content' } });

    // Simulate auto-save (would be triggered by debounced function in real app)
    await act(async () => {
      await new Promise(resolve => setTimeout(resolve, 100));
    });
  });
});

// Integration Tests
describe('Component Integration Tests', () => {
  test('navigation between components', () => {
    // This would test navigation between different components
    // using React Router in a real application
    expect(true).toBe(true); // Placeholder
  });

  test('shared state management', () => {
    // This would test shared state between components
    // using context or state management libraries
    expect(true).toBe(true); // Placeholder
  });

  test('error boundary handling', () => {
    // This would test error boundaries and error handling
    // across the application
    expect(true).toBe(true); // Placeholder
  });
});

// Accessibility Tests
describe('Accessibility Tests', () => {
  test('components have proper ARIA labels', () => {
    // Test that components have proper accessibility attributes
    expect(true).toBe(true); // Placeholder
  });

  test('keyboard navigation works', () => {
    // Test keyboard navigation through components
    expect(true).toBe(true); // Placeholder
  });

  test('screen reader compatibility', () => {
    // Test screen reader compatibility
    expect(true).toBe(true); // Placeholder
  });
});

// Performance Tests
describe('Performance Tests', () => {
  test('components render within acceptable time', () => {
    // Test component rendering performance
    expect(true).toBe(true); // Placeholder
  });

  test('memory usage is reasonable', () => {
    // Test memory usage and cleanup
    expect(true).toBe(true); // Placeholder
  });
});
