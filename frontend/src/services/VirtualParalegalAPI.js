/**
 * Virtual Paralegal CRM API Service
 * Handles all API calls for the Virtual Paralegal system
 */

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

class VirtualParalegalAPI {
  constructor() {
    this.baseURL = API_BASE_URL;
  }

  /**
   * Get authentication headers
   */
  getAuthHeaders() {
    const token = localStorage.getItem('accessToken');
    return {
      'Content-Type': 'application/json',
      'Authorization': token ? `Bearer ${token}` : '',
    };
  }

  /**
   * Make API request
   */
  async request(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`;
    const config = {
      headers: this.getAuthHeaders(),
      ...options,
    };

    try {
      const response = await fetch(url, config);
      
      if (!response.ok) {
        throw new Error(`API Error: ${response.status} ${response.statusText}`);
      }

      return await response.json();
    } catch (error) {
      console.error('API Request failed:', error);
      throw error;
    }
  }

  // ==================== CLIENT API ====================

  /**
   * Get client's cases
   */
  async getClientCases(clientId) {
    return this.request(`/api/v1/virtual-paralegal-crm/clients/${clientId}/cases`);
  }

  /**
   * Get client's documents
   */
  async getClientDocuments(clientId) {
    return this.request(`/api/v1/virtual-paralegal-crm/clients/${clientId}/documents`);
  }

  /**
   * Get client's notifications
   */
  async getClientNotifications(clientId) {
    return this.request(`/api/v1/virtual-paralegal-crm/clients/${clientId}/notifications`);
  }

  /**
   * Send message to lawyer
   */
  async sendMessageToLawyer(clientId, message) {
    return this.request(`/api/v1/virtual-paralegal-crm/clients/${clientId}/messages`, {
      method: 'POST',
      body: JSON.stringify({ message }),
    });
  }

  // ==================== LAWYER API ====================

  /**
   * Get all clients
   */
  async getClients() {
    return this.request('/api/v1/virtual-paralegal-crm/clients');
  }

  /**
   * Create new client
   */
  async createClient(clientData) {
    return this.request('/api/v1/virtual-paralegal-crm/clients', {
      method: 'POST',
      body: JSON.stringify(clientData),
    });
  }

  /**
   * Update client
   */
  async updateClient(clientId, clientData) {
    return this.request(`/api/v1/virtual-paralegal-crm/clients/${clientId}`, {
      method: 'PUT',
      body: JSON.stringify(clientData),
    });
  }

  /**
   * Get all cases
   */
  async getCases() {
    return this.request('/api/v1/virtual-paralegal-crm/cases');
  }

  /**
   * Create new case
   */
  async createCase(caseData) {
    return this.request('/api/v1/virtual-paralegal-crm/cases', {
      method: 'POST',
      body: JSON.stringify(caseData),
    });
  }

  /**
   * Update case
   */
  async updateCase(caseId, caseData) {
    return this.request(`/api/v1/virtual-paralegal-crm/cases/${caseId}`, {
      method: 'PUT',
      body: JSON.stringify(caseData),
    });
  }

  /**
   * Get case details
   */
  async getCaseDetails(caseId) {
    return this.request(`/api/v1/virtual-paralegal-crm/cases/${caseId}`);
  }

  /**
   * Get all tasks
   */
  async getTasks() {
    return this.request('/api/v1/virtual-paralegal-crm/tasks');
  }

  /**
   * Create new task
   */
  async createTask(taskData) {
    return this.request('/api/v1/virtual-paralegal-crm/tasks', {
      method: 'POST',
      body: JSON.stringify(taskData),
    });
  }

  /**
   * Update task
   */
  async updateTask(taskId, taskData) {
    return this.request(`/api/v1/virtual-paralegal-crm/tasks/${taskId}`, {
      method: 'PUT',
      body: JSON.stringify(taskData),
    });
  }

  // ==================== BONDSMAN API ====================

  /**
   * Get all bail bonds
   */
  async getBailBonds() {
    return this.request('/api/v1/bondsman/bonds');
  }

  /**
   * Create new bail bond
   */
  async createBailBond(bondData) {
    return this.request('/api/v1/bondsman/bonds', {
      method: 'POST',
      body: JSON.stringify(bondData),
    });
  }

  /**
   * Update bail bond
   */
  async updateBailBond(bondId, bondData) {
    return this.request(`/api/v1/bondsman/bonds/${bondId}`, {
      method: 'PUT',
      body: JSON.stringify(bondData),
    });
  }

  /**
   * Get bond clients
   */
  async getBondClients() {
    return this.request('/api/v1/bondsman/clients');
  }

  /**
   * Get payments
   */
  async getPayments() {
    return this.request('/api/v1/bondsman/payments');
  }

  /**
   * Record payment
   */
  async recordPayment(paymentData) {
    return this.request('/api/v1/bondsman/payments', {
      method: 'POST',
      body: JSON.stringify(paymentData),
    });
  }

  /**
   * Get court dates
   */
  async getCourtDates() {
    return this.request('/api/v1/bondsman/court-dates');
  }

  // ==================== DOCUMENT API ====================

  /**
   * Upload document
   */
  async uploadDocument(file, caseId) {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('caseId', caseId);

    const response = await fetch(`${this.baseURL}/api/v1/documents/upload`, {
      method: 'POST',
      headers: {
        'Authorization': localStorage.getItem('accessToken') ? `Bearer ${localStorage.getItem('accessToken')}` : '',
      },
      body: formData,
    });

    if (!response.ok) {
      throw new Error(`Upload failed: ${response.statusText}`);
    }

    return await response.json();
  }

  /**
   * Download document
   */
  async downloadDocument(documentId) {
    const response = await fetch(`${this.baseURL}/api/v1/documents/${documentId}/download`, {
      headers: this.getAuthHeaders(),
    });

    if (!response.ok) {
      throw new Error(`Download failed: ${response.statusText}`);
    }

    return response.blob();
  }

  /**
   * Get document list
   */
  async getDocuments(caseId = null) {
    const endpoint = caseId 
      ? `/api/v1/documents?caseId=${caseId}`
      : '/api/v1/documents';
    return this.request(endpoint);
  }

  // ==================== NOTIFICATION API ====================

  /**
   * Get notifications
   */
  async getNotifications(userId) {
    return this.request(`/api/v1/notifications/${userId}`);
  }

  /**
   * Mark notification as read
   */
  async markNotificationAsRead(notificationId) {
    return this.request(`/api/v1/notifications/${notificationId}/read`, {
      method: 'PUT',
    });
  }

  /**
   * Mark all notifications as read
   */
  async markAllNotificationsAsRead(userId) {
    return this.request(`/api/v1/notifications/${userId}/read-all`, {
      method: 'PUT',
    });
  }

  // ==================== ANALYTICS API ====================

  /**
   * Get dashboard analytics
   */
  async getDashboardAnalytics(userRole) {
    return this.request(`/api/v1/analytics/dashboard/${userRole}`);
  }

  /**
   * Get case statistics
   */
  async getCaseStatistics() {
    return this.request('/api/v1/analytics/cases');
  }

  /**
   * Get client statistics
   */
  async getClientStatistics() {
    return this.request('/api/v1/analytics/clients');
  }

  // ==================== HEALTH CHECK ====================

  /**
   * Check API health
   */
  async healthCheck() {
    try {
      const response = await fetch(`${this.baseURL}/api/v1/health`);
      return response.ok;
    } catch (error) {
      return false;
    }
  }
}

// Create singleton instance
const virtualParalegalAPI = new VirtualParalegalAPI();

export default virtualParalegalAPI;
