/**
 * Case Tracking Data Model
 *
 * This file defines the structure for legal cases and provides mock data
 * for development and testing of the case tracking feature.
 */

// Define case status options
export const CASE_STATUS = {
  NEW: 'new',
  IN_PROGRESS: 'in_progress',
  PENDING_CLIENT: 'pending_client',
  PENDING_COURT: 'pending_court',
  RESOLVED: 'resolved',
  CLOSED: 'closed',
};

// Define case types
export const CASE_TYPES = {
  HOUSING: 'housing',
  EMPLOYMENT: 'employment',
  FAMILY: 'family',
  IMMIGRATION: 'immigration',
  DEBT: 'debt',
  CIVIL_RIGHTS: 'civil_rights',
  CRIMINAL: 'criminal',
  EMERGENCY: 'emergency',
  OTHER: 'other',
};

// Define case priority levels
export const PRIORITY_LEVELS = {
  LOW: 'low',
  MEDIUM: 'medium',
  HIGH: 'high',
  URGENT: 'urgent',
};

// Sample mock cases data
export const mockCases = [
  {
    id: 'CASE-20240701-1234',
    title: 'Wrongful Eviction Dispute',
    type: CASE_TYPES.HOUSING,
    status: CASE_STATUS.IN_PROGRESS,
    priority: PRIORITY_LEVELS.HIGH,
    created: '2024-07-01T15:23:45Z',
    updated: '2024-07-05T10:12:30Z',
    description:
      'Client facing eviction without proper notice. Landlord claims non-payment of rent, client has proof of payment.',
    client: {
      id: 'C12345',
      name: 'Maria Rodriguez',
      email: 'maria.r@example.com',
      phone: '555-123-4567',
    },
    assignedTo: {
      id: 'A789',
      name: 'David Kim',
      role: 'Housing Attorney',
    },
    timeline: [
      {
        id: 'TL-1',
        date: '2024-07-01T15:23:45Z',
        type: 'case_created',
        description: 'Case opened through emergency support channel',
        user: 'System',
      },
      {
        id: 'TL-2',
        date: '2024-07-01T16:45:10Z',
        type: 'document_added',
        description: 'Client uploaded eviction notice',
        user: 'Maria Rodriguez',
      },
      {
        id: 'TL-3',
        date: '2024-07-02T09:30:00Z',
        type: 'attorney_assigned',
        description: 'Case assigned to David Kim',
        user: 'System',
      },
      {
        id: 'TL-4',
        date: '2024-07-03T14:15:20Z',
        type: 'consultation',
        description: 'Initial consultation conducted via video call',
        user: 'David Kim',
      },
      {
        id: 'TL-5',
        date: '2024-07-05T10:12:30Z',
        type: 'document_added',
        description: 'Response to eviction notice drafted and uploaded',
        user: 'David Kim',
      },
    ],
    nextSteps: [
      {
        id: 'NS-1',
        description: 'File response with local housing court',
        dueDate: '2024-07-08T17:00:00Z',
        completed: false,
        assignedTo: 'client',
      },
      {
        id: 'NS-2',
        description: 'Gather additional evidence of rent payments',
        dueDate: '2024-07-10T17:00:00Z',
        completed: false,
        assignedTo: 'client',
      },
      {
        id: 'NS-3',
        description: 'Follow-up consultation',
        dueDate: '2024-07-12T10:00:00Z',
        completed: false,
        assignedTo: 'attorney',
      },
    ],
    documents: [
      {
        id: 'DOC-1',
        title: 'Eviction Notice',
        type: 'received',
        dateAdded: '2024-07-01T16:45:10Z',
        addedBy: 'Maria Rodriguez',
      },
      {
        id: 'DOC-2',
        title: 'Rent Payment Records',
        type: 'evidence',
        dateAdded: '2024-07-02T11:30:15Z',
        addedBy: 'Maria Rodriguez',
      },
      {
        id: 'DOC-3',
        title: 'Response to Eviction Notice',
        type: 'generated',
        dateAdded: '2024-07-05T10:12:30Z',
        addedBy: 'David Kim',
      },
    ],
  },
  {
    id: 'CASE-20240625-5678',
    title: 'Unpaid Wages Claim',
    type: CASE_TYPES.EMPLOYMENT,
    status: CASE_STATUS.PENDING_CLIENT,
    priority: PRIORITY_LEVELS.MEDIUM,
    created: '2024-06-25T09:10:20Z',
    updated: '2024-07-03T16:45:20Z',
    description:
      'Client not paid for final two weeks of work after leaving job. Employer claims performance issues.',
    client: {
      id: 'C12346',
      name: 'James Wilson',
      email: 'james.w@example.com',
      phone: '555-222-3333',
    },
    assignedTo: {
      id: 'A456',
      name: 'Sarah Lee',
      role: 'Employment Attorney',
    },
    timeline: [
      {
        id: 'TL-1',
        date: '2024-06-25T09:10:20Z',
        type: 'case_created',
        description: 'Case opened through online portal',
        user: 'James Wilson',
      },
      {
        id: 'TL-2',
        date: '2024-06-26T13:45:10Z',
        type: 'attorney_assigned',
        description: 'Case assigned to Sarah Lee',
        user: 'System',
      },
      {
        id: 'TL-3',
        date: '2024-06-28T11:30:00Z',
        type: 'consultation',
        description: 'Initial consultation conducted via phone',
        user: 'Sarah Lee',
      },
      {
        id: 'TL-4',
        date: '2024-07-03T16:45:20Z',
        type: 'document_added',
        description: 'Demand letter to employer drafted',
        user: 'Sarah Lee',
      },
    ],
    nextSteps: [
      {
        id: 'NS-1',
        description: 'Review and approve demand letter',
        dueDate: '2024-07-07T17:00:00Z',
        completed: false,
        assignedTo: 'client',
      },
      {
        id: 'NS-2',
        description: 'Provide additional pay stubs',
        dueDate: '2024-07-08T17:00:00Z',
        completed: false,
        assignedTo: 'client',
      },
    ],
    documents: [
      {
        id: 'DOC-1',
        title: 'Employment Contract',
        type: 'evidence',
        dateAdded: '2024-06-25T09:15:10Z',
        addedBy: 'James Wilson',
      },
      {
        id: 'DOC-2',
        title: 'Final Pay Stub',
        type: 'evidence',
        dateAdded: '2024-06-26T10:20:15Z',
        addedBy: 'James Wilson',
      },
      {
        id: 'DOC-3',
        title: 'Demand Letter Draft',
        type: 'generated',
        dateAdded: '2024-07-03T16:45:20Z',
        addedBy: 'Sarah Lee',
      },
    ],
  },
  {
    id: 'CASE-20240710-9012',
    title: 'Emergency Police Encounter',
    type: CASE_TYPES.EMERGENCY,
    status: CASE_STATUS.NEW,
    priority: PRIORITY_LEVELS.URGENT,
    created: '2024-07-10T20:15:30Z',
    updated: '2024-07-10T20:15:30Z',
    description:
      'Client called emergency hotline during police stop. Concerned about rights violation.',
    client: {
      id: 'C12347',
      name: 'Jamal Thompson',
      email: 'jamal.t@example.com',
      phone: '555-444-5555',
    },
    assignedTo: null,
    timeline: [
      {
        id: 'TL-1',
        date: '2024-07-10T20:15:30Z',
        type: 'case_created',
        description: 'Case opened through emergency support call',
        user: 'System',
      },
    ],
    nextSteps: [
      {
        id: 'NS-1',
        description: 'Assign attorney to case',
        dueDate: '2024-07-10T21:00:00Z',
        completed: false,
        assignedTo: 'system',
      },
      {
        id: 'NS-2',
        description: 'Initial contact with client',
        dueDate: '2024-07-10T22:00:00Z',
        completed: false,
        assignedTo: 'system',
      },
    ],
    documents: [],
  },
];

/**
 * Get a case by ID
 * @param {string} caseId - The case ID
 * @returns {Object|null} - The case object or null if not found
 */
export const getCaseById = caseId => {
  return mockCases.find(c => c.id === caseId) || null;
};

/**
 * Get cases filtered by status, type, or priority
 * @param {Object} filters - Filters to apply
 * @param {string} [filters.status] - Filter by case status
 * @param {string} [filters.type] - Filter by case type
 * @param {string} [filters.priority] - Filter by priority level
 * @returns {Array} - Filtered array of cases
 */
export const filterCases = (filters = {}) => {
  return mockCases.filter(c => {
    let match = true;

    if (filters.status && c.status !== filters.status) {
      match = false;
    }

    if (filters.type && c.type !== filters.type) {
      match = false;
    }

    if (filters.priority && c.priority !== filters.priority) {
      match = false;
    }

    if (filters.clientId && c.client.id !== filters.clientId) {
      match = false;
    }

    if (filters.assignedToId && (!c.assignedTo || c.assignedTo.id !== filters.assignedToId)) {
      match = false;
    }

    return match;
  });
};

/**
 * Get cases for a specific client
 * @param {string} clientId - The client ID
 * @returns {Array} - Array of cases for the client
 */
export const getClientCases = clientId => {
  return filterCases({ clientId });
};

/**
 * Get a formatted status label for display
 * @param {string} status - The status code
 * @returns {string} - Formatted status label
 */
export const getStatusLabel = status => {
  const statusMap = {
    [CASE_STATUS.NEW]: 'New Case',
    [CASE_STATUS.IN_PROGRESS]: 'In Progress',
    [CASE_STATUS.PENDING_CLIENT]: 'Pending Client Action',
    [CASE_STATUS.PENDING_COURT]: 'Pending Court',
    [CASE_STATUS.RESOLVED]: 'Resolved',
    [CASE_STATUS.CLOSED]: 'Closed',
  };

  return statusMap[status] || status;
};

/**
 * Get a formatted case type label for display
 * @param {string} type - The case type code
 * @returns {string} - Formatted case type label
 */
export const getCaseTypeLabel = type => {
  const typeMap = {
    [CASE_TYPES.HOUSING]: 'Housing',
    [CASE_TYPES.EMPLOYMENT]: 'Employment',
    [CASE_TYPES.FAMILY]: 'Family',
    [CASE_TYPES.IMMIGRATION]: 'Immigration',
    [CASE_TYPES.DEBT]: 'Debt',
    [CASE_TYPES.CIVIL_RIGHTS]: 'Civil Rights',
    [CASE_TYPES.CRIMINAL]: 'Criminal',
    [CASE_TYPES.EMERGENCY]: 'Emergency',
    [CASE_TYPES.OTHER]: 'Other',
  };

  return typeMap[type] || type;
};

/**
 * Get a formatted priority level label for display
 * @param {string} priority - The priority level code
 * @returns {string} - Formatted priority level label
 */
export const getPriorityLabel = priority => {
  const priorityMap = {
    [PRIORITY_LEVELS.LOW]: 'Low',
    [PRIORITY_LEVELS.MEDIUM]: 'Medium',
    [PRIORITY_LEVELS.HIGH]: 'High',
    [PRIORITY_LEVELS.URGENT]: 'Urgent',
  };

  return priorityMap[priority] || priority;
};

export default mockCases;
