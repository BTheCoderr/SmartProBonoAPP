import axios from 'axios';
import config from '../config';

const API_URL = `${config.apiUrl}/api/cases`;

// Case status constants
export const CaseStatus = {
  NEW: 'new',
  IN_PROGRESS: 'in_progress',
  PENDING_REVIEW: 'pending_review',
  COMPLETED: 'completed',
  CLOSED: 'closed',
};

// Case priority constants
export const CasePriority = {
  URGENT: 'urgent',
  HIGH: 'high',
  MEDIUM: 'medium',
  LOW: 'low',
};

// Get all cases with optional filters
export const getAllCases = async (filters = {}) => {
  try {
    const { status, priority, search, sort_by, sort_direction } = filters;
    
    let url = API_URL;
    const params = new URLSearchParams();
    
    if (status) params.append('status', status);
    if (priority) params.append('priority', priority);
    if (search) params.append('search', search);
    if (sort_by) params.append('sort_by', sort_by);
    if (sort_direction) params.append('sort_direction', sort_direction);
    
    if (params.toString()) {
      url += `?${params.toString()}`;
    }
    
    const response = await axios.get(url);
    return response.data;
  } catch (error) {
    console.error('Error fetching cases:', error);
    throw error;
  }
};

// Get a case by ID
export const getCaseById = async (caseId) => {
  try {
    const response = await axios.get(`${API_URL}/${caseId}`);
    return response.data;
  } catch (error) {
    console.error(`Error fetching case ${caseId}:`, error);
    throw error;
  }
};

// Create a new case
export const createCase = async (caseData) => {
  try {
    const response = await axios.post(API_URL, caseData);
    return response.data;
  } catch (error) {
    console.error('Error creating case:', error);
    throw error;
  }
};

// Update an existing case
export const updateCase = async (caseId, updateData) => {
  try {
    const response = await axios.put(`${API_URL}/${caseId}`, updateData);
    return response.data;
  } catch (error) {
    console.error(`Error updating case ${caseId}:`, error);
    throw error;
  }
};

// Delete a case
export const deleteCase = async (caseId) => {
  try {
    await axios.delete(`${API_URL}/${caseId}`);
    return true;
  } catch (error) {
    console.error(`Error deleting case ${caseId}:`, error);
    throw error;
  }
};

// Assign a case to a user
export const assignCase = async (caseId, userId) => {
  try {
    const response = await axios.post(`${API_URL}/${caseId}/assign`, { user_id: userId });
    return response.data;
  } catch (error) {
    console.error(`Error assigning case ${caseId}:`, error);
    throw error;
  }
};

// Update a case's priority
export const updatePriority = async (caseId, priority) => {
  try {
    const response = await axios.put(`${API_URL}/${caseId}/priority`, { priority });
    return response.data;
  } catch (error) {
    console.error(`Error updating priority for case ${caseId}:`, error);
    throw error;
  }
};

// Get case history
export const getCaseHistory = async (caseId) => {
  try {
    const response = await axios.get(`${API_URL}/${caseId}/history`);
    return response.data;
  } catch (error) {
    console.error(`Error fetching history for case ${caseId}:`, error);
    throw error;
  }
};

// Add a timeline event
export const addTimelineEvent = async (caseId, eventData) => {
  try {
    const response = await axios.post(`${API_URL}/${caseId}/timeline`, eventData);
    return response.data;
  } catch (error) {
    console.error(`Error adding timeline event for case ${caseId}:`, error);
    throw error;
  }
};

// Get timeline events
export const getCaseTimeline = async (caseId) => {
  try {
    const response = await axios.get(`${API_URL}/${caseId}/timeline`);
    return response.data;
  } catch (error) {
    console.error(`Error fetching timeline for case ${caseId}:`, error);
    throw error;
  }
};

// Add a document to a case
export const addDocument = async (caseId, documentData) => {
  try {
    const response = await axios.post(`${API_URL}/${caseId}/documents`, documentData);
    return response.data;
  } catch (error) {
    console.error(`Error adding document to case ${caseId}:`, error);
    throw error;
  }
};

// Get case documents
export const getCaseDocuments = async (caseId) => {
  try {
    const response = await axios.get(`${API_URL}/${caseId}/documents`);
    return response.data;
  } catch (error) {
    console.error(`Error fetching documents for case ${caseId}:`, error);
    throw error;
  }
};

// Batch Operations

// Update multiple cases at once
export const updateCasesBatch = async (caseIds, updateData) => {
  try {
    const response = await axios.put(`${API_URL}/batch`, {
      case_ids: caseIds,
      ...updateData
    });
    return response.data;
  } catch (error) {
    console.error('Error updating cases in batch:', error);
    throw error;
  }
};

// Delete multiple cases at once
export const deleteCasesBatch = async (caseIds) => {
  try {
    const response = await axios.delete(`${API_URL}/batch`, {
      data: { case_ids: caseIds }
    });
    return response.data;
  } catch (error) {
    console.error('Error deleting cases in batch:', error);
    throw error;
  }
};

// Assign multiple cases to a user
export const assignCasesBatch = async (caseIds, userId) => {
  try {
    const response = await axios.post(`${API_URL}/batch/assign`, {
      case_ids: caseIds,
      user_id: userId
    });
    return response.data;
  } catch (error) {
    console.error('Error assigning cases in batch:', error);
    throw error;
  }
};

// Update priority for multiple cases
export const updatePriorityBatch = async (caseIds, priority) => {
  try {
    const response = await axios.put(`${API_URL}/batch/priority`, {
      case_ids: caseIds,
      priority
    });
    return response.data;
  } catch (error) {
    console.error('Error updating priority for cases in batch:', error);
    throw error;
  }
};
