/**
 * dataRetentionPolicy.js
 * Utilities for enforcing data retention policies, tracking data lifespans,
 * and handling privacy compliance requirements
 */

// Data retention periods in days
export const RETENTION_PERIODS = {
  // Client personal information
  CLIENT_PERSONAL_DATA: 365 * 2, // 2 years

  // Case data
  ACTIVE_CASE: 365 * 7, // 7 years
  CLOSED_CASE: 365 * 3, // 3 years
  DECLINED_CASE: 365 * 1, // 1 year

  // Communication records
  CHAT_MESSAGES: 365 * 2, // 2 years
  EMAIL_CORRESPONDENCE: 365 * 3, // 3 years
  VOICE_RECORDINGS: 90, // 90 days

  // Documents
  LEGAL_DOCUMENTS: 365 * 7, // 7 years
  DRAFT_DOCUMENTS: 180, // 180 days
  SYSTEM_LOGS: 30, // 30 days

  // Security data
  SECURITY_INCIDENT_LOGS: 365 * 2, // 2 years
  ACCESS_LOGS: 90, // 90 days

  // Consent records - kept longer for compliance purposes
  CONSENT_RECORDS: 365 * 10, // 10 years
};

// Data categories for privacy laws
export const DATA_CATEGORIES = {
  PERSONAL_IDENTIFIABLE: 'personal_identifiable', // Name, email, phone, address
  SENSITIVE_PERSONAL: 'sensitive_personal', // Health, religion, biometric
  FINANCIAL: 'financial', // Financial information
  COMMUNICATIONS: 'communications', // Messages, emails
  LEGAL_CASE: 'legal_case', // Case information
  DOCUMENTS: 'documents', // Legal documents
  SECURITY: 'security', // Security-related data
  SYSTEM: 'system', // System logs, usage data
};

// Data privacy jurisdictions
export const PRIVACY_JURISDICTIONS = {
  GDPR: 'gdpr', // European Union
  CCPA: 'ccpa', // California
  LGPD: 'lgpd', // Brazil
  PIPEDA: 'pipeda', // Canada
  GENERAL: 'general', // General policy
};

/**
 * Calculate the expiration date for a piece of data
 * @param {string} dataType - Type of data (use constants)
 * @param {Date} creationDate - When the data was created
 * @param {string} [jurisdiction=PRIVACY_JURISDICTIONS.GENERAL] - Privacy jurisdiction
 * @returns {Date} - Expiration date
 */
export const calculateExpirationDate = (
  dataType,
  creationDate,
  jurisdiction = PRIVACY_JURISDICTIONS.GENERAL
) => {
  if (!creationDate) {
    creationDate = new Date();
  } else if (typeof creationDate === 'string') {
    creationDate = new Date(creationDate);
  }

  // Get retention period, adjusting for jurisdiction if needed
  let retentionDays = RETENTION_PERIODS[dataType] || 365; // Default to 1 year

  // Adjust retention period based on jurisdiction
  // For example, GDPR might require shorter retention for some data
  if (jurisdiction === PRIVACY_JURISDICTIONS.GDPR) {
    if (dataType === 'SECURITY_INCIDENT_LOGS') {
      retentionDays = 365; // Only 1 year for GDPR
    }
  }

  // Calculate expiration date
  const expirationDate = new Date(creationDate);
  expirationDate.setDate(expirationDate.getDate() + retentionDays);

  return expirationDate;
};

/**
 * Check if a data item has expired
 * @param {Object} dataItem - Data item with metadata
 * @returns {boolean} - Whether the data has expired
 */
export const isDataExpired = dataItem => {
  if (!dataItem || !dataItem.metadata || !dataItem.metadata.expirationDate) {
    return false; // Can't determine if missing metadata
  }

  const expirationDate = new Date(dataItem.metadata.expirationDate);
  return expirationDate < new Date();
};

/**
 * Tag data with retention metadata
 * @param {Object} data - The data object to tag
 * @param {string} dataType - Type of data (use constants)
 * @param {string} category - Data category (use constants)
 * @param {string} [jurisdiction=PRIVACY_JURISDICTIONS.GENERAL] - Privacy jurisdiction
 * @returns {Object} - Data with retention metadata
 */
export const tagDataWithRetentionMetadata = (
  data,
  dataType,
  category,
  jurisdiction = PRIVACY_JURISDICTIONS.GENERAL
) => {
  if (!data) return data;

  const creationDate = new Date();
  const expirationDate = calculateExpirationDate(dataType, creationDate, jurisdiction);

  return {
    ...data,
    metadata: {
      ...data.metadata,
      dataType,
      category,
      jurisdiction,
      creationDate: creationDate.toISOString(),
      expirationDate: expirationDate.toISOString(),
      retentionPeriodDays: RETENTION_PERIODS[dataType] || 365,
    },
  };
};

/**
 * Generate a data retention report for items approaching expiration
 * @param {Array} dataItems - Array of data items with metadata
 * @param {number} daysThreshold - Days threshold for approaching expiration
 * @returns {Object} - Report of items approaching expiration
 */
export const generateRetentionReport = (dataItems, daysThreshold = 30) => {
  if (!dataItems || !Array.isArray(dataItems)) {
    return { expiringSoon: [], expired: [], totalItems: 0 };
  }

  const now = new Date();
  const thresholdDate = new Date();
  thresholdDate.setDate(thresholdDate.getDate() + daysThreshold);

  const expiringSoon = [];
  const expired = [];

  dataItems.forEach(item => {
    if (!item.metadata || !item.metadata.expirationDate) return;

    const expirationDate = new Date(item.metadata.expirationDate);

    if (expirationDate < now) {
      expired.push({
        id: item.id,
        dataType: item.metadata.dataType,
        category: item.metadata.category,
        expirationDate: item.metadata.expirationDate,
        daysExpired: Math.floor((now - expirationDate) / (1000 * 60 * 60 * 24)),
      });
    } else if (expirationDate < thresholdDate) {
      expiringSoon.push({
        id: item.id,
        dataType: item.metadata.dataType,
        category: item.metadata.category,
        expirationDate: item.metadata.expirationDate,
        daysUntilExpiration: Math.floor((expirationDate - now) / (1000 * 60 * 60 * 24)),
      });
    }
  });

  return {
    expiringSoon,
    expired,
    totalItems: dataItems.length,
    reportGeneratedAt: now.toISOString(),
    daysThreshold,
  };
};

/**
 * Create a data retention audit log entry
 * @param {string} action - Action performed (e.g., 'delete', 'extend', 'archive')
 * @param {Object} dataItem - The data item affected
 * @param {string} performedBy - User or system that performed the action
 * @param {string} reason - Reason for the action
 * @returns {Object} - Audit log entry
 */
export const createRetentionAuditLog = (action, dataItem, performedBy, reason) => {
  return {
    timestamp: new Date().toISOString(),
    action,
    dataItemId: dataItem.id,
    dataType: dataItem.metadata?.dataType || 'unknown',
    category: dataItem.metadata?.category || 'unknown',
    originalExpirationDate: dataItem.metadata?.expirationDate,
    performedBy,
    reason,
    systemInfo: {
      userAgent: navigator.userAgent,
      ipAddress: '[Collected on server]', // Placeholder, actual IP would be added server-side
    },
  };
};

/**
 * Process data deletion
 * @param {Array} dataItems - Array of data items to check
 * @param {Function} deleteCallback - Function to call for deleting data
 * @param {Function} logCallback - Function to log deletion
 * @returns {Promise<Object>} - Results of deletion operations
 */
export const processDataDeletion = async (dataItems, deleteCallback, logCallback) => {
  if (!dataItems || !Array.isArray(dataItems) || !deleteCallback) {
    return { success: false, deleted: 0, errors: ['Invalid parameters'] };
  }

  const results = { success: true, deleted: 0, errors: [] };
  const now = new Date();

  for (const item of dataItems) {
    if (!item.metadata || !item.metadata.expirationDate) continue;

    const expirationDate = new Date(item.metadata.expirationDate);

    if (expirationDate < now) {
      try {
        // Delete the expired item
        await deleteCallback(item);
        results.deleted++;

        // Log the deletion if a log callback is provided
        if (logCallback) {
          const logEntry = createRetentionAuditLog(
            'delete',
            item,
            'system-retention-policy',
            'Data retention period expired'
          );
          await logCallback(logEntry);
        }
      } catch (error) {
        results.errors.push(`Failed to delete item ${item.id}: ${error.message}`);
        results.success = false;
      }
    }
  }

  return results;
};

/**
 * Extend retention period for a data item
 * @param {Object} dataItem - Data item to extend
 * @param {number} additionalDays - Days to extend
 * @param {string} reason - Reason for extension
 * @param {string} extendedBy - User who extended the retention
 * @returns {Object} - Updated data item
 */
export const extendRetentionPeriod = (dataItem, additionalDays, reason, extendedBy) => {
  if (!dataItem || !dataItem.metadata || !dataItem.metadata.expirationDate) {
    throw new Error('Invalid data item or missing metadata');
  }

  const currentExpiration = new Date(dataItem.metadata.expirationDate);
  const newExpiration = new Date(currentExpiration);
  newExpiration.setDate(newExpiration.getDate() + additionalDays);

  // Update the metadata
  const updatedItem = {
    ...dataItem,
    metadata: {
      ...dataItem.metadata,
      originalExpirationDate: dataItem.metadata.expirationDate,
      expirationDate: newExpiration.toISOString(),
      retentionExtensions: [
        ...(dataItem.metadata.retentionExtensions || []),
        {
          extendedAt: new Date().toISOString(),
          additionalDays,
          reason,
          extendedBy,
        },
      ],
    },
  };

  return updatedItem;
};

/**
 * Generate a privacy compliance report
 * @param {Array} dataItems - Array of data items
 * @returns {Object} - Compliance report
 */
export const generatePrivacyComplianceReport = dataItems => {
  if (!dataItems || !Array.isArray(dataItems)) {
    return { categories: {}, jurisdictions: {}, totalItems: 0 };
  }

  const report = {
    categories: {},
    jurisdictions: {},
    retentionStatus: {
      current: 0,
      expiringSoon: 0,
      expired: 0,
    },
    totalItems: dataItems.length,
    reportGeneratedAt: new Date().toISOString(),
  };

  // Initialize categories
  Object.values(DATA_CATEGORIES).forEach(category => {
    report.categories[category] = 0;
  });

  // Initialize jurisdictions
  Object.values(PRIVACY_JURISDICTIONS).forEach(jurisdiction => {
    report.jurisdictions[jurisdiction] = 0;
  });

  const now = new Date();
  const thirtyDaysFromNow = new Date();
  thirtyDaysFromNow.setDate(thirtyDaysFromNow.getDate() + 30);

  // Process each data item
  dataItems.forEach(item => {
    // Count by category
    const category = item.metadata?.category || 'unknown';
    report.categories[category] = (report.categories[category] || 0) + 1;

    // Count by jurisdiction
    const jurisdiction = item.metadata?.jurisdiction || PRIVACY_JURISDICTIONS.GENERAL;
    report.jurisdictions[jurisdiction] = (report.jurisdictions[jurisdiction] || 0) + 1;

    // Check retention status
    if (item.metadata?.expirationDate) {
      const expirationDate = new Date(item.metadata.expirationDate);

      if (expirationDate < now) {
        report.retentionStatus.expired++;
      } else if (expirationDate < thirtyDaysFromNow) {
        report.retentionStatus.expiringSoon++;
      } else {
        report.retentionStatus.current++;
      }
    } else {
      // Items without expiration dates are considered current
      report.retentionStatus.current++;
    }
  });

  return report;
};

export default {
  RETENTION_PERIODS,
  DATA_CATEGORIES,
  PRIVACY_JURISDICTIONS,
  calculateExpirationDate,
  isDataExpired,
  tagDataWithRetentionMetadata,
  generateRetentionReport,
  createRetentionAuditLog,
  processDataDeletion,
  extendRetentionPeriod,
  generatePrivacyComplianceReport,
};
