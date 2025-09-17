import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:3001';

class CRMService {
  constructor() {
    this.api = axios.create({
      baseURL: API_BASE_URL,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Add auth token to requests
    this.api.interceptors.request.use((config) => {
      const token = localStorage.getItem('access_token') || localStorage.getItem('token');
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
      return config;
    });
  }

  // Client Portal APIs
  async createClientIntake(data) {
    try {
      const response = await this.api.post('/api/v1/crm/client/intake', data);
      return response.data;
    } catch (error) {
      console.error('Error creating client intake:', error);
      throw error;
    }
  }

  async getClientCases(clientId) {
    try {
      const response = await this.api.get(`/api/v1/crm/client/${clientId}/cases`);
      return response.data;
    } catch (error) {
      console.error('Error getting client cases:', error);
      throw error;
    }
  }

  async getClientDocuments(clientId) {
    try {
      const response = await this.api.get(`/api/v1/crm/client/${clientId}/documents`);
      return response.data;
    } catch (error) {
      console.error('Error getting client documents:', error);
      throw error;
    }
  }

  async getClientCourtDates(clientId) {
    try {
      const response = await this.api.get(`/api/v1/crm/client/${clientId}/court-dates`);
      return response.data;
    } catch (error) {
      console.error('Error getting client court dates:', error);
      throw error;
    }
  }

  async getClientNotifications(clientId) {
    try {
      const response = await this.api.get(`/api/v1/crm/client/${clientId}/notifications`);
      return response.data;
    } catch (error) {
      console.error('Error getting client notifications:', error);
      throw error;
    }
  }

  // Lawyer Dashboard APIs
  async getLawyerClients() {
    try {
      const response = await this.api.get('/api/v1/crm/lawyer/clients');
      return response.data;
    } catch (error) {
      console.error('Error getting lawyer clients:', error);
      throw error;
    }
  }

  async getLawyerCases() {
    try {
      const response = await this.api.get('/api/v1/crm/lawyer/cases');
      return response.data;
    } catch (error) {
      console.error('Error getting lawyer cases:', error);
      throw error;
    }
  }

  async createCase(data) {
    try {
      const response = await this.api.post('/api/v1/crm/lawyer/cases', data);
      return response.data;
    } catch (error) {
      console.error('Error creating case:', error);
      throw error;
    }
  }

  async getLawyerTasks() {
    try {
      const response = await this.api.get('/api/v1/crm/lawyer/tasks');
      return response.data;
    } catch (error) {
      console.error('Error getting lawyer tasks:', error);
      throw error;
    }
  }

  async createTask(data) {
    try {
      const response = await this.api.post('/api/v1/crm/lawyer/tasks', data);
      return response.data;
    } catch (error) {
      console.error('Error creating task:', error);
      throw error;
    }
  }

  // Bondsman Dashboard APIs
  async getBondsmanBonds() {
    try {
      const response = await this.api.get('/api/v1/crm/bondsman/bonds');
      return response.data;
    } catch (error) {
      console.error('Error getting bondsman bonds:', error);
      throw error;
    }
  }

  async createBailBond(data) {
    try {
      const response = await this.api.post('/api/v1/crm/bondsman/bonds', data);
      return response.data;
    } catch (error) {
      console.error('Error creating bail bond:', error);
      throw error;
    }
  }

  async getBondsmanPayments() {
    try {
      const response = await this.api.get('/api/v1/crm/bondsman/payments');
      return response.data;
    } catch (error) {
      console.error('Error getting bondsman payments:', error);
      throw error;
    }
  }

  async createPayment(data) {
    try {
      const response = await this.api.post('/api/v1/crm/bondsman/payments', data);
      return response.data;
    } catch (error) {
      console.error('Error creating payment:', error);
      throw error;
    }
  }

  // Shared APIs
  async createCourtDate(data) {
    try {
      const response = await this.api.post('/api/v1/crm/court-dates', data);
      return response.data;
    } catch (error) {
      console.error('Error creating court date:', error);
      throw error;
    }
  }

  async getUpcomingCourtDates(daysAhead = 30) {
    try {
      const response = await this.api.get(`/api/v1/crm/court-dates/upcoming?days=${daysAhead}`);
      return response.data;
    } catch (error) {
      console.error('Error getting upcoming court dates:', error);
      throw error;
    }
  }

  async createNotification(data) {
    try {
      const response = await this.api.post('/api/v1/crm/notifications', data);
      return response.data;
    } catch (error) {
      console.error('Error creating notification:', error);
      throw error;
    }
  }

  async markNotificationRead(notificationId) {
    try {
      const response = await this.api.put(`/api/v1/crm/notifications/${notificationId}/read`);
      return response.data;
    } catch (error) {
      console.error('Error marking notification as read:', error);
      throw error;
    }
  }

  async getDashboardAnalytics() {
    try {
      const response = await this.api.get('/api/v1/crm/dashboard/analytics');
      return response.data;
    } catch (error) {
      console.error('Error getting dashboard analytics:', error);
      throw error;
    }
  }

  // Health check
  async healthCheck() {
    try {
      const response = await this.api.get('/api/health');
      return response.data;
    } catch (error) {
      console.error('Error checking server health:', error);
      throw error;
    }
  }
}

// Export singleton instance
export default new CRMService();
