/**
 * auditLogger.js
 * Comprehensive audit logging system for sensitive operations in legal applications
 * Tracks user actions, system events, data access, and compliance-related activities
 */

import { DATA_CATEGORIES, PRIVACY_JURISDICTIONS } from './dataRetentionPolicy';

// Audit log event severity levels
export const SEVERITY_LEVELS = {
  INFO: 'info', // Normal operations, routine actions
  WARNING: 'warning', // Unusual but not critical events
  ERROR: 'error', // Errors and exceptions
  CRITICAL: 'critical', // Serious security or integrity issues
  DEBUG: 'debug', // Development/troubleshooting only
};

// Audit event categories
export const EVENT_CATEGORIES = {
  AUTH: 'authentication', // Login/logout events
  ACCESS: 'data_access', // Data viewing/retrieval
  MODIFICATION: 'data_modification', // Data updates/changes
  DELETION: 'data_deletion', // Data removal
  EXPORT: 'data_export', // Data exports/downloads
  SHARING: 'data_sharing', // Data sharing with others
  ADMIN: 'administrative', // System administration
  COMPLIANCE: 'compliance', // Compliance-related activities
  SECURITY: 'security', // Security events
  SYSTEM: 'system', // System events
};

// Types of operations that require auditing
export const OPERATION_TYPES = {
  VIEW: 'view',
  CREATE: 'create',
  UPDATE: 'update',
  DELETE: 'delete',
  EXPORT: 'export',
  DOWNLOAD: 'download',
  SHARE: 'share',
  LOGIN: 'login',
  LOGOUT: 'logout',
  GRANT_ACCESS: 'grant_access',
  REVOKE_ACCESS: 'revoke_access',
  ENCRYPT: 'encrypt',
  DECRYPT: 'decrypt',
};

// Local cache to temporarily store logs if API is unavailable
let localAuditCache = [];
const MAX_CACHE_SIZE = 100;

/**
 * Create a new audit log entry
 * @param {string} eventCategory - Category of the event (use EVENT_CATEGORIES)
 * @param {string} operationType - Type of operation (use OPERATION_TYPES)
 * @param {string} resourceType - Type of resource affected (e.g., 'case', 'document')
 * @param {string} resourceId - ID of the affected resource
 * @param {Object} details - Additional event details
 * @param {string} [severityLevel=SEVERITY_LEVELS.INFO] - Severity level of the event
 * @returns {Object} - The created audit log entry
 */
export const createAuditLog = (
  eventCategory,
  operationType,
  resourceType,
  resourceId,
  details = {},
  severityLevel = SEVERITY_LEVELS.INFO
) => {
  // Get user information if available
  const user = getCurrentUser();

  // Build the audit log entry
  const logEntry = {
    id: generateLogId(),
    timestamp: new Date().toISOString(),
    eventCategory,
    operationType,
    resourceType,
    resourceId,
    severityLevel,
    user: {
      id: user?.id || 'anonymous',
      name: user?.name || 'Anonymous User',
      role: user?.role || 'unknown',
    },
    sessionId: getSessionId(),
    ipAddress: '[Collected on server]', // Will be filled by server
    userAgent: navigator.userAgent,
    details: {
      ...details,
      location: getLocation(),
      application: {
        name: 'SmartProBono',
        version: process.env.REACT_APP_VERSION || 'unknown',
      },
    },
    metadata: {
      privacyCategory: details.privacyCategory || null,
      jurisdiction: details.jurisdiction || null,
      isEncrypted: !!details.isEncrypted,
      relatedAuditIds: details.relatedAuditIds || [],
    },
  };

  // Send log to server, or cache if that fails
  logToServer(logEntry).catch(() => {
    // Store locally if server logging fails
    cacheLogLocally(logEntry);
  });

  return logEntry;
};

/**
 * Generate a unique ID for the log entry
 * @returns {string} Unique log ID
 */
const generateLogId = () => {
  return Date.now().toString(36) + Math.random().toString(36).substr(2, 5).toUpperCase();
};

/**
 * Get current user from the application context
 * @returns {Object|null} Current user object or null
 */
const getCurrentUser = () => {
  // In a real application, this would retrieve user from context/state
  // This is a placeholder implementation
  try {
    const userStr = localStorage.getItem('currentUser');
    return userStr ? JSON.parse(userStr) : null;
  } catch (e) {
    console.error('Error getting current user for audit log', e);
    return null;
  }
};

/**
 * Get the current session ID
 * @returns {string} Session ID
 */
const getSessionId = () => {
  let sessionId = sessionStorage.getItem('sessionId');

  if (!sessionId) {
    sessionId = Date.now().toString(36) + Math.random().toString(36).substr(2, 5);
    sessionStorage.setItem('sessionId', sessionId);
  }

  return sessionId;
};

/**
 * Get the user's general location (if available)
 * @returns {Object} Location information or null
 */
const getLocation = () => {
  // This would be filled by the server with approximate location based on IP
  // We'll just use a placeholder here
  return { approximateLocation: 'Not available client-side' };
};

/**
 * Send the log entry to the server
 * @param {Object} logEntry - The log entry to send
 * @returns {Promise} - Promise that resolves when log is sent
 */
const logToServer = async logEntry => {
  try {
    // Check for cached logs and try to send them first
    await sendCachedLogs();

    // Send the current log
    const response = await fetch('/api/audit-logs', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(logEntry),
    });

    if (!response.ok) {
      throw new Error(`Server returned ${response.status}`);
    }

    return response.json();
  } catch (error) {
    console.error('Failed to send audit log to server', error);
    throw error;
  }
};

/**
 * Cache a log entry locally when server is unavailable
 * @param {Object} logEntry - The log entry to cache
 */
const cacheLogLocally = logEntry => {
  // Add to cache
  localAuditCache.push({
    ...logEntry,
    cached: true,
    cacheTimestamp: new Date().toISOString(),
  });

  // Limit cache size
  if (localAuditCache.length > MAX_CACHE_SIZE) {
    localAuditCache = localAuditCache.slice(localAuditCache.length - MAX_CACHE_SIZE);
  }

  // Store in localStorage as backup (encrypted in a real app)
  try {
    localStorage.setItem('auditLogCache', JSON.stringify(localAuditCache));
  } catch (e) {
    console.error('Error caching audit logs locally', e);
  }
};

/**
 * Send any cached logs to the server
 * @returns {Promise} - Promise that resolves when cached logs are sent
 */
const sendCachedLogs = async () => {
  if (localAuditCache.length === 0) return;

  // Try to recover logs from localStorage if available
  try {
    const storedLogs = localStorage.getItem('auditLogCache');
    if (storedLogs) {
      const parsedLogs = JSON.parse(storedLogs);
      localAuditCache = [...localAuditCache, ...parsedLogs];
      // Remove duplicates
      const uniqueIds = new Set();
      localAuditCache = localAuditCache.filter(log => {
        if (uniqueIds.has(log.id)) return false;
        uniqueIds.add(log.id);
        return true;
      });
    }
  } catch (e) {
    console.error('Error recovering cached logs', e);
  }

  if (localAuditCache.length === 0) return;

  try {
    const response = await fetch('/api/audit-logs/batch', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ logs: localAuditCache }),
    });

    if (response.ok) {
      // Clear cache on successful send
      localAuditCache = [];
      localStorage.removeItem('auditLogCache');
    }
  } catch (error) {
    console.error('Failed to send cached audit logs', error);
  }
};

/**
 * Log user authentication events
 * @param {string} operationType - 'login', 'logout', 'failed_login', etc.
 * @param {string} userId - User ID
 * @param {Object} details - Additional details
 * @param {string} [severityLevel=SEVERITY_LEVELS.INFO] - Severity level
 * @returns {Object} - The created audit log
 */
export const logAuthEvent = (
  operationType,
  userId,
  details = {},
  severityLevel = SEVERITY_LEVELS.INFO
) => {
  return createAuditLog(
    EVENT_CATEGORIES.AUTH,
    operationType,
    'user',
    userId,
    details,
    severityLevel
  );
};

/**
 * Log data access events
 * @param {string} resourceType - Type of resource accessed
 * @param {string} resourceId - ID of resource accessed
 * @param {Object} details - Additional details
 * @returns {Object} - The created audit log
 */
export const logDataAccess = (resourceType, resourceId, details = {}) => {
  return createAuditLog(EVENT_CATEGORIES.ACCESS, OPERATION_TYPES.VIEW, resourceType, resourceId, {
    ...details,
    privacyCategory: details.privacyCategory || DATA_CATEGORIES.LEGAL_CASE,
  });
};

/**
 * Log data modification events
 * @param {string} operationType - Type of modification operation
 * @param {string} resourceType - Type of resource modified
 * @param {string} resourceId - ID of resource modified
 * @param {Object} details - Additional details
 * @returns {Object} - The created audit log
 */
export const logDataModification = (operationType, resourceType, resourceId, details = {}) => {
  return createAuditLog(EVENT_CATEGORIES.MODIFICATION, operationType, resourceType, resourceId, {
    ...details,
    changes: details.changes || 'Not specified',
    previousState: details.previousState,
    newState: details.newState,
  });
};

/**
 * Log data deletion events
 * @param {string} resourceType - Type of resource deleted
 * @param {string} resourceId - ID of resource deleted
 * @param {Object} details - Additional details
 * @returns {Object} - The created audit log
 */
export const logDataDeletion = (resourceType, resourceId, details = {}) => {
  return createAuditLog(
    EVENT_CATEGORIES.DELETION,
    OPERATION_TYPES.DELETE,
    resourceType,
    resourceId,
    {
      ...details,
      reason: details.reason || 'User requested deletion',
      permanentDeletion: details.permanentDeletion || false,
    },
    SEVERITY_LEVELS.WARNING // Deletions are always at least warnings
  );
};

/**
 * Log data export/download events
 * @param {string} resourceType - Type of resource exported
 * @param {string} resourceId - ID of resource exported
 * @param {string} exportFormat - Format of the export (PDF, CSV, etc.)
 * @param {Object} details - Additional details
 * @returns {Object} - The created audit log
 */
export const logDataExport = (resourceType, resourceId, exportFormat, details = {}) => {
  return createAuditLog(EVENT_CATEGORIES.EXPORT, OPERATION_TYPES.EXPORT, resourceType, resourceId, {
    ...details,
    exportFormat,
    dataSize: details.dataSize,
    destinationType: details.destinationType || 'local_download',
  });
};

/**
 * Log data sharing events
 * @param {string} resourceType - Type of resource shared
 * @param {string} resourceId - ID of resource shared
 * @param {string} recipientId - ID of the recipient
 * @param {Object} details - Additional details
 * @returns {Object} - The created audit log
 */
export const logDataSharing = (resourceType, resourceId, recipientId, details = {}) => {
  return createAuditLog(EVENT_CATEGORIES.SHARING, OPERATION_TYPES.SHARE, resourceType, resourceId, {
    ...details,
    recipientId,
    recipientType: details.recipientType || 'user',
    sharingMethod: details.sharingMethod || 'internal',
    permissionLevel: details.permissionLevel || 'read',
    expirationDate: details.expirationDate,
  });
};

/**
 * Log security-related events
 * @param {string} operationType - Type of security operation
 * @param {string} resourceType - Type of resource affected
 * @param {string} resourceId - ID of resource affected
 * @param {Object} details - Additional details
 * @param {string} severityLevel - Severity level
 * @returns {Object} - The created audit log
 */
export const logSecurityEvent = (
  operationType,
  resourceType,
  resourceId,
  details = {},
  severityLevel = SEVERITY_LEVELS.WARNING
) => {
  return createAuditLog(
    EVENT_CATEGORIES.SECURITY,
    operationType,
    resourceType,
    resourceId,
    details,
    severityLevel
  );
};

/**
 * Log compliance-related events
 * @param {string} operationType - Type of compliance operation
 * @param {string} resourceType - Type of resource affected
 * @param {string} resourceId - ID of resource affected
 * @param {Object} details - Additional details
 * @returns {Object} - The created audit log
 */
export const logComplianceEvent = (operationType, resourceType, resourceId, details = {}) => {
  return createAuditLog(EVENT_CATEGORIES.COMPLIANCE, operationType, resourceType, resourceId, {
    ...details,
    complianceType: details.complianceType || 'privacy',
    jurisdiction: details.jurisdiction || PRIVACY_JURISDICTIONS.GENERAL,
  });
};

/**
 * Export audit logs for a specified date range and filters
 * @param {Date} startDate - Start date for logs
 * @param {Date} endDate - End date for logs
 * @param {Object} filters - Filters to apply
 * @param {string} format - Export format (CSV, JSON, PDF)
 * @returns {Promise<Blob>} - Blob containing the exported data
 */
export const exportAuditLogs = async (startDate, endDate, filters = {}, format = 'CSV') => {
  try {
    // Prepare query parameters
    const params = new URLSearchParams({
      startDate: startDate.toISOString(),
      endDate: endDate.toISOString(),
      format: format,
      ...filters,
    });

    // Log the export attempt
    logDataExport('audit_logs', 'system', format, {
      dateRange: `${startDate.toISOString()} to ${endDate.toISOString()}`,
      filters,
    });

    // Fetch the logs from server
    const response = await fetch(`/api/audit-logs/export?${params.toString()}`, {
      method: 'GET',
      headers: {
        Accept: format === 'JSON' ? 'application/json' : 'text/csv',
      },
    });

    if (!response.ok) {
      throw new Error(`Server returned ${response.status}`);
    }

    // Get the blob from the response
    const blob = await response.blob();
    return blob;
  } catch (error) {
    console.error('Failed to export audit logs', error);
    throw error;
  }
};

/**
 * Initialize the audit logger
 * This should be called when the application starts
 */
export const initAuditLogger = () => {
  // Try to send any cached logs
  sendCachedLogs().catch(console.error);

  // Log application start
  createAuditLog(EVENT_CATEGORIES.SYSTEM, 'application_start', 'application', 'main', {
    startReason: 'user_initiated',
    url: window.location.href,
    referrer: document.referrer,
  });

  // Set up window unload handler
  window.addEventListener('unload', () => {
    // Attempt to log application exit, but this must be synchronous
    try {
      const logEntry = {
        eventCategory: EVENT_CATEGORIES.SYSTEM,
        operationType: 'application_exit',
        resourceType: 'application',
        resourceId: 'main',
        timestamp: new Date().toISOString(),
        user: getCurrentUser() || { id: 'anonymous' },
        sessionId: getSessionId(),
      };

      // Use synchronous XHR since we're in unload
      const xhr = new XMLHttpRequest();
      xhr.open('POST', '/api/audit-logs/sync', false); // Synchronous request
      xhr.setRequestHeader('Content-Type', 'application/json');
      xhr.send(JSON.stringify(logEntry));
    } catch (e) {
      // No way to report errors during unload
    }
  });
};

export default {
  SEVERITY_LEVELS,
  EVENT_CATEGORIES,
  OPERATION_TYPES,
  createAuditLog,
  logAuthEvent,
  logDataAccess,
  logDataModification,
  logDataDeletion,
  logDataExport,
  logDataSharing,
  logSecurityEvent,
  logComplianceEvent,
  exportAuditLogs,
  initAuditLogger,
};
