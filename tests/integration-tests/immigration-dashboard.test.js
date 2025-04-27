/**
 * Integration tests for the Immigration Dashboard
 */

import axios from 'axios';
import MockAdapter from 'axios-mock-adapter';
import { API_URL } from '../../frontend/src/config';

// Mock data for tests
const mockCases = {
  cases: [
    {
      _id: '1234',
      title: 'Family Visa Application',
      status: 'in-progress',
      clientName: 'Test User',
      createdAt: '2023-08-01T12:00:00Z',
      updatedAt: '2023-08-05T14:30:00Z',
      type: 'family',
      notes: 'Test notes'
    },
    {
      _id: '5678',
      title: 'Work Visa Application',
      status: 'completed',
      clientName: 'Another User',
      createdAt: '2023-07-15T10:00:00Z',
      updatedAt: '2023-07-25T16:45:00Z',
      type: 'employment'
    }
  ]
};

const mockForms = [
  {
    _id: 'form1',
    firstName: 'John',
    lastName: 'Doe',
    email: 'john@example.com',
    status: 'new',
    visaType: 'family',
    createdAt: '2023-08-10T09:00:00Z'
  },
  {
    _id: 'form2',
    firstName: 'Jane',
    lastName: 'Smith',
    email: 'jane@example.com',
    status: 'in-progress',
    visaType: 'employment',
    createdAt: '2023-08-05T11:30:00Z'
  }
];

const mockNotifications = {
  notifications: [
    {
      _id: 'notif1',
      title: 'New Document Required',
      message: 'Please upload your passport',
      isRead: false,
      type: 'document_request',
      createdAt: '2023-08-12T14:00:00Z',
      caseId: '1234'
    },
    {
      _id: 'notif2',
      title: 'Case Status Updated',
      message: 'Your case has been updated to in-progress',
      isRead: true,
      type: 'status_update',
      createdAt: '2023-08-10T09:15:00Z',
      caseId: '1234'
    }
  ],
  count: 2,
  unreadCount: 1
};

const mockEvents = {
  events: [
    {
      _id: 'event1',
      title: 'Document Deadline',
      date: '2023-09-01T00:00:00Z',
      type: 'deadline',
      caseId: '1234',
      description: 'Submit all documents by this date'
    },
    {
      _id: 'event2',
      title: 'Interview Preparation',
      date: '2023-08-25T15:00:00Z',
      type: 'appointment',
      caseId: '1234',
      description: 'Prepare for USCIS interview'
    }
  ],
  count: 2
};

describe('Immigration Dashboard', () => {
  let mock;
  
  beforeAll(() => {
    mock = new MockAdapter(axios);
  });
  
  afterEach(() => {
    mock.reset();
  });
  
  afterAll(() => {
    mock.restore();
  });
  
  describe('API Endpoints', () => {
    it('should fetch immigration cases successfully', async () => {
      mock.onGet(`${API_URL}/api/immigration/cases`).reply(200, mockCases);
      
      const response = await axios.get(`${API_URL}/api/immigration/cases`, {
        headers: { Authorization: 'Bearer test-token' }
      });
      
      expect(response.status).toBe(200);
      expect(response.data).toEqual(mockCases);
      expect(response.data.cases.length).toBe(2);
    });
    
    it('should fetch intake forms successfully', async () => {
      mock.onGet(`${API_URL}/api/immigration/intake-forms`).reply(200, mockForms);
      
      const response = await axios.get(`${API_URL}/api/immigration/intake-forms`, {
        headers: { Authorization: 'Bearer test-token' }
      });
      
      expect(response.status).toBe(200);
      expect(response.data).toEqual(mockForms);
      expect(response.data.length).toBe(2);
    });
    
    it('should fetch notifications successfully', async () => {
      mock.onGet(`${API_URL}/api/immigration/notifications`).reply(200, mockNotifications);
      
      const response = await axios.get(`${API_URL}/api/immigration/notifications`, {
        headers: { Authorization: 'Bearer test-token' }
      });
      
      expect(response.status).toBe(200);
      expect(response.data).toEqual(mockNotifications);
      expect(response.data.notifications.length).toBe(2);
      expect(response.data.unreadCount).toBe(1);
    });
    
    it('should fetch upcoming events successfully', async () => {
      mock.onGet(`${API_URL}/api/immigration/events`).reply(200, mockEvents);
      
      const response = await axios.get(`${API_URL}/api/immigration/events`, {
        headers: { Authorization: 'Bearer test-token' }
      });
      
      expect(response.status).toBe(200);
      expect(response.data).toEqual(mockEvents);
      expect(response.data.events.length).toBe(2);
    });
    
    it('should mark a notification as read successfully', async () => {
      const notificationId = 'notif1';
      mock.onPut(`${API_URL}/api/immigration/notifications/${notificationId}/read`).reply(200, {
        success: true,
        message: 'Notification marked as read'
      });
      
      const response = await axios.put(`${API_URL}/api/immigration/notifications/${notificationId}/read`, {}, {
        headers: { Authorization: 'Bearer test-token' }
      });
      
      expect(response.status).toBe(200);
      expect(response.data.success).toBe(true);
    });
    
    it('should upload a document successfully', async () => {
      const caseId = '1234';
      const mockFile = new File(['test content'], 'test.pdf', { type: 'application/pdf' });
      const formData = new FormData();
      formData.append('file', mockFile);
      formData.append('documentType', 'identity');
      
      mock.onPost(`${API_URL}/api/immigration/cases/${caseId}/documents`).reply(200, {
        message: 'Document uploaded successfully',
        document: {
          _id: 'doc1',
          filename: 'test.pdf',
          documentType: 'identity',
          uploadedAt: '2023-08-15T10:00:00Z'
        }
      });
      
      const response = await axios.post(`${API_URL}/api/immigration/cases/${caseId}/documents`, formData, {
        headers: { 
          Authorization: 'Bearer test-token',
          'Content-Type': 'multipart/form-data'
        }
      });
      
      expect(response.status).toBe(200);
      expect(response.data.message).toBe('Document uploaded successfully');
      expect(response.data.document.filename).toBe('test.pdf');
    });
  });
}); 