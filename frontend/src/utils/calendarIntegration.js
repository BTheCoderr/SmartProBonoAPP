/**
 * calendarIntegration.js
 * Utilities for integrating with external calendar services
 * Supports adding court dates, appointments, and deadlines to various calendar services
 */

import { logDataExport, logSecurityEvent } from './auditLogger';

// Supported calendar providers
export const CALENDAR_PROVIDERS = {
  GOOGLE: 'google_calendar',
  OUTLOOK: 'outlook_calendar',
  APPLE: 'apple_calendar',
  ICAL: 'ical', // Generic iCalendar format
};

// Calendar event types
export const EVENT_TYPES = {
  COURT_DATE: 'court_date',
  CLIENT_APPOINTMENT: 'client_appointment',
  FILING_DEADLINE: 'filing_deadline',
  DOCUMENT_DEADLINE: 'document_deadline',
  CONSULTATION: 'consultation',
  HEARING: 'hearing',
  DEPOSITION: 'deposition',
  STATUS_CONFERENCE: 'status_conference',
  TRIAL: 'trial',
  MEDIATION: 'mediation',
  REMINDER: 'reminder',
};

// Event importance/priority levels
export const PRIORITY_LEVELS = {
  HIGH: 'high',
  MEDIUM: 'medium',
  LOW: 'low',
};

/**
 * Format an event for Google Calendar
 * @param {Object} event - Event details
 * @returns {Object} - Google Calendar formatted event
 */
const formatGoogleCalendarEvent = event => {
  // Get reminder settings based on event type and priority
  const reminderSettings = getReminderSettings(event.type, event.priority);

  return {
    summary: event.title,
    description: formatEventDescription(event),
    location: event.location || '',
    start: {
      dateTime: event.startTime,
      timeZone: event.timeZone || Intl.DateTimeFormat().resolvedOptions().timeZone,
    },
    end: {
      dateTime:
        event.endTime ||
        new Date(new Date(event.startTime).getTime() + 60 * 60 * 1000).toISOString(), // Default to 1 hour
      timeZone: event.timeZone || Intl.DateTimeFormat().resolvedOptions().timeZone,
    },
    reminders: {
      useDefault: false,
      overrides: reminderSettings.map(reminder => ({
        method: 'popup',
        minutes: reminder,
      })),
    },
    // Add custom properties for Pro Bono App
    extendedProperties: {
      private: {
        eventType: event.type,
        caseId: event.caseId || '',
        priority: event.priority || PRIORITY_LEVELS.MEDIUM,
        createdBy: event.createdBy || 'system',
        appId: 'SmartProBonoApp',
      },
    },
    // Make high priority events visually distinct
    colorId:
      event.priority === PRIORITY_LEVELS.HIGH
        ? '11' // Red for high priority
        : event.priority === PRIORITY_LEVELS.MEDIUM
          ? '5' // Yellow for medium
          : '9', // Green for low
  };
};

/**
 * Format an event for Outlook Calendar
 * @param {Object} event - Event details
 * @returns {Object} - Outlook Calendar formatted event
 */
const formatOutlookCalendarEvent = event => {
  // Get reminder settings based on event type and priority
  const reminderMinutes = getReminderSettings(event.type, event.priority)[0] || 60; // Use first reminder

  return {
    subject: event.title,
    body: {
      contentType: 'HTML',
      content: formatEventDescription(event, 'html'),
    },
    start: {
      dateTime: event.startTime,
      timeZone: event.timeZone || Intl.DateTimeFormat().resolvedOptions().timeZone,
    },
    end: {
      dateTime:
        event.endTime ||
        new Date(new Date(event.startTime).getTime() + 60 * 60 * 1000).toISOString(),
      timeZone: event.timeZone || Intl.DateTimeFormat().resolvedOptions().timeZone,
    },
    location: {
      displayName: event.location || '',
    },
    importance:
      event.priority === PRIORITY_LEVELS.HIGH
        ? 'high'
        : event.priority === PRIORITY_LEVELS.LOW
          ? 'low'
          : 'normal',
    isReminderOn: true,
    reminderMinutesBeforeStart: reminderMinutes,
    categories: [getEventCategory(event.type)],
  };
};

/**
 * Generate an iCalendar (ICS) file content for an event
 * @param {Object} event - Event details
 * @returns {string} - iCalendar file content
 */
const generateICalendarContent = event => {
  const startDate = new Date(event.startTime);
  const endDate = event.endTime
    ? new Date(event.endTime)
    : new Date(startDate.getTime() + 60 * 60 * 1000);

  // Format dates to iCalendar format: YYYYMMDDTHHMMSSZ
  const formatDateForICal = date => {
    return date
      .toISOString()
      .replace(/[-:]/g, '')
      .replace(/\.\d{3}/, '');
  };

  // Get a unique ID for the event
  const getUid = () => {
    return `${Date.now()}-${Math.random().toString(36).substr(2, 9)}-smartprobono`;
  };

  // Create the iCalendar content
  let icsContent = [
    'BEGIN:VCALENDAR',
    'VERSION:2.0',
    'PRODID:-//SmartProBonoApp//EN',
    'CALSCALE:GREGORIAN',
    'METHOD:PUBLISH',
    'BEGIN:VEVENT',
    `UID:${getUid()}`,
    `DTSTAMP:${formatDateForICal(new Date())}`,
    `DTSTART:${formatDateForICal(startDate)}`,
    `DTEND:${formatDateForICal(endDate)}`,
    `SUMMARY:${event.title || 'Legal Appointment'}`,
    `DESCRIPTION:${formatEventDescription(event, 'plain').replace(/\n/g, '\\n')}`,
  ];

  if (event.location) {
    icsContent.push(`LOCATION:${event.location}`);
  }

  // Add appropriate status
  icsContent.push('STATUS:CONFIRMED');

  // Add a reminder alert (alarm)
  const reminderSettings = getReminderSettings(event.type, event.priority);
  if (reminderSettings.length > 0) {
    icsContent.push('BEGIN:VALARM');
    icsContent.push('ACTION:DISPLAY');
    icsContent.push(`DESCRIPTION:Reminder: ${event.title}`);
    // Convert minutes to negative duration in seconds: PT15M for 15 minutes
    icsContent.push(`TRIGGER:-PT${reminderSettings[0]}M`);
    icsContent.push('END:VALARM');
  }

  // Close the event and calendar
  icsContent.push('END:VEVENT');
  icsContent.push('END:VCALENDAR');

  return icsContent.join('\r\n');
};

/**
 * Format event description with relevant details
 * @param {Object} event - Event object
 * @param {string} format - 'plain' or 'html'
 * @returns {string} - Formatted description
 */
const formatEventDescription = (event, format = 'plain') => {
  const {
    description,
    caseId,
    caseName,
    clientName,
    location,
    type,
    notes,
    contactInfo,
    documentLinks,
  } = event;

  let formattedDescription;

  if (format === 'html') {
    formattedDescription = `<p>${description || `${getEventTypeLabel(type)} for case ${caseName || caseId}`}</p>`;

    // Add case and client info if available
    if (caseId || caseName) {
      formattedDescription += `<p><strong>Case:</strong> ${caseName || ''} ${caseId ? `(${caseId})` : ''}</p>`;
    }

    if (clientName) {
      formattedDescription += `<p><strong>Client:</strong> ${clientName}</p>`;
    }

    if (location) {
      formattedDescription += `<p><strong>Location:</strong> ${location}</p>`;
    }

    if (contactInfo) {
      formattedDescription += `<p><strong>Contact:</strong> ${contactInfo}</p>`;
    }

    if (notes) {
      formattedDescription += `<p><strong>Notes:</strong><br>${notes}</p>`;
    }

    // Add document links if any
    if (documentLinks && documentLinks.length > 0) {
      formattedDescription += '<p><strong>Related Documents:</strong></p><ul>';
      documentLinks.forEach(doc => {
        formattedDescription += `<li><a href="${doc.url}">${doc.title}</a></li>`;
      });
      formattedDescription += '</ul>';
    }

    formattedDescription += '<p><em>Created by SmartProBono App</em></p>';
  } else {
    // Plain text format
    formattedDescription =
      description || `${getEventTypeLabel(type)} for case ${caseName || caseId}`;

    // Add case and client info if available
    if (caseId || caseName) {
      formattedDescription += `\nCase: ${caseName || ''} ${caseId ? `(${caseId})` : ''}`;
    }

    if (clientName) {
      formattedDescription += `\nClient: ${clientName}`;
    }

    if (location) {
      formattedDescription += `\nLocation: ${location}`;
    }

    if (contactInfo) {
      formattedDescription += `\nContact: ${contactInfo}`;
    }

    if (notes) {
      formattedDescription += `\nNotes: ${notes}`;
    }

    // Add document links if any
    if (documentLinks && documentLinks.length > 0) {
      formattedDescription += '\nRelated Documents:';
      documentLinks.forEach(doc => {
        formattedDescription += `\n- ${doc.title}: ${doc.url}`;
      });
    }

    formattedDescription += '\nCreated by SmartProBono App';
  }

  return formattedDescription;
};

/**
 * Get reminder settings based on event type and priority
 * @param {string} eventType - Type of event
 * @param {string} priority - Priority level
 * @returns {Array<number>} - Array of reminder times in minutes before event
 */
const getReminderSettings = (eventType, priority) => {
  // Define default reminders
  const defaultReminders = [60]; // 1 hour

  // High priority events get more reminders
  if (priority === PRIORITY_LEVELS.HIGH) {
    return [1440, 720, 60, 30]; // 24 hours, 12 hours, 1 hour, 30 minutes
  }

  // Settings based on event type
  switch (eventType) {
    case EVENT_TYPES.COURT_DATE:
    case EVENT_TYPES.TRIAL:
      return [1440, 720, 120]; // 24 hours, 12 hours, 2 hours

    case EVENT_TYPES.FILING_DEADLINE:
    case EVENT_TYPES.DOCUMENT_DEADLINE:
      return [1440, 720, 360, 120]; // 24 hours, 12 hours, 6 hours, 2 hours

    case EVENT_TYPES.HEARING:
    case EVENT_TYPES.DEPOSITION:
      return [1440, 180, 60]; // 24 hours, 3 hours, 1 hour

    case EVENT_TYPES.CLIENT_APPOINTMENT:
    case EVENT_TYPES.CONSULTATION:
      return [360, 60]; // 6 hours, 1 hour

    case EVENT_TYPES.MEDIATION:
    case EVENT_TYPES.STATUS_CONFERENCE:
      return [720, 60]; // 12 hours, 1 hour

    default:
      return defaultReminders;
  }
};

/**
 * Get a human-readable label for an event type
 * @param {string} eventType - Type of event
 * @returns {string} - Human-readable label
 */
const getEventTypeLabel = eventType => {
  switch (eventType) {
    case EVENT_TYPES.COURT_DATE:
      return 'Court Date';
    case EVENT_TYPES.CLIENT_APPOINTMENT:
      return 'Client Appointment';
    case EVENT_TYPES.FILING_DEADLINE:
      return 'Filing Deadline';
    case EVENT_TYPES.DOCUMENT_DEADLINE:
      return 'Document Deadline';
    case EVENT_TYPES.CONSULTATION:
      return 'Consultation';
    case EVENT_TYPES.HEARING:
      return 'Hearing';
    case EVENT_TYPES.DEPOSITION:
      return 'Deposition';
    case EVENT_TYPES.STATUS_CONFERENCE:
      return 'Status Conference';
    case EVENT_TYPES.TRIAL:
      return 'Trial';
    case EVENT_TYPES.MEDIATION:
      return 'Mediation';
    case EVENT_TYPES.REMINDER:
      return 'Reminder';
    default:
      return 'Legal Appointment';
  }
};

/**
 * Get the category name for an event type
 * @param {string} eventType - Type of event
 * @returns {string} - Category name
 */
const getEventCategory = eventType => {
  switch (eventType) {
    case EVENT_TYPES.COURT_DATE:
    case EVENT_TYPES.HEARING:
    case EVENT_TYPES.TRIAL:
      return 'Court Events';

    case EVENT_TYPES.CLIENT_APPOINTMENT:
    case EVENT_TYPES.CONSULTATION:
      return 'Client Meetings';

    case EVENT_TYPES.FILING_DEADLINE:
    case EVENT_TYPES.DOCUMENT_DEADLINE:
      return 'Deadlines';

    case EVENT_TYPES.DEPOSITION:
    case EVENT_TYPES.STATUS_CONFERENCE:
    case EVENT_TYPES.MEDIATION:
      return 'Case Proceedings';

    default:
      return 'Legal Events';
  }
};

/**
 * Create an event in Google Calendar
 * @param {Object} event - Event details
 * @param {string} accessToken - Google API access token
 * @returns {Promise<Object>} - Created event data
 */
export const createGoogleCalendarEvent = async (event, accessToken) => {
  if (!accessToken) {
    throw new Error('Google Calendar access token is required');
  }

  try {
    const formattedEvent = formatGoogleCalendarEvent(event);

    const response = await fetch(
      'https://www.googleapis.com/calendar/v3/calendars/primary/events',
      {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${accessToken}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formattedEvent),
      }
    );

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(
        `Google Calendar API error: ${errorData.error?.message || response.statusText}`
      );
    }

    const createdEvent = await response.json();

    // Log the successful export
    logDataExport('calendar_event', event.caseId || 'unknown', 'google_calendar', {
      eventType: event.type,
      eventId: createdEvent.id,
      title: event.title,
    });

    return createdEvent;
  } catch (error) {
    // Log the error
    logSecurityEvent('calendar_integration_error', 'calendar_event', event.caseId || 'unknown', {
      error: error.message,
      provider: CALENDAR_PROVIDERS.GOOGLE,
    });
    throw error;
  }
};

/**
 * Create an event in Outlook Calendar
 * @param {Object} event - Event details
 * @param {string} accessToken - Microsoft Graph API access token
 * @returns {Promise<Object>} - Created event data
 */
export const createOutlookCalendarEvent = async (event, accessToken) => {
  if (!accessToken) {
    throw new Error('Outlook Calendar access token is required');
  }

  try {
    const formattedEvent = formatOutlookCalendarEvent(event);

    const response = await fetch('https://graph.microsoft.com/v1.0/me/events', {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${accessToken}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(formattedEvent),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(
        `Outlook Calendar API error: ${errorData.error?.message || response.statusText}`
      );
    }

    const createdEvent = await response.json();

    // Log the successful export
    logDataExport('calendar_event', event.caseId || 'unknown', 'outlook_calendar', {
      eventType: event.type,
      eventId: createdEvent.id,
      title: event.title,
    });

    return createdEvent;
  } catch (error) {
    // Log the error
    logSecurityEvent('calendar_integration_error', 'calendar_event', event.caseId || 'unknown', {
      error: error.message,
      provider: CALENDAR_PROVIDERS.OUTLOOK,
    });
    throw error;
  }
};

/**
 * Generate an iCalendar file for download
 * @param {Object} event - Event details
 * @returns {Blob} - iCalendar file as a Blob
 */
export const generateICalendarFile = event => {
  const icsContent = generateICalendarContent(event);

  // Create a Blob with the ICS content
  const blob = new Blob([icsContent], { type: 'text/calendar;charset=utf-8' });

  // Log the export
  logDataExport('calendar_event', event.caseId || 'unknown', 'ical_file', {
    eventType: event.type,
    title: event.title,
  });

  return blob;
};

/**
 * Download an event as an iCalendar file
 * @param {Object} event - Event details
 */
export const downloadICalendarFile = event => {
  const blob = generateICalendarFile(event);
  const fileName = `${event.title || 'Event'}_${new Date().toISOString().split('T')[0]}.ics`;

  // Create a URL for the Blob
  const url = URL.createObjectURL(blob);

  // Create an invisible link element and trigger download
  const link = document.createElement('a');
  link.href = url;
  link.download = fileName;
  document.body.appendChild(link);
  link.click();

  // Clean up
  setTimeout(() => {
    URL.revokeObjectURL(url);
    document.body.removeChild(link);
  }, 100);
};

/**
 * Create a calendar event using the specified provider
 * @param {Object} event - Event details
 * @param {string} provider - Calendar provider (use CALENDAR_PROVIDERS)
 * @param {Object} authData - Authentication data for the provider
 * @returns {Promise<Object>} - Result of the calendar operation
 */
export const createCalendarEvent = async (event, provider, authData = {}) => {
  switch (provider) {
    case CALENDAR_PROVIDERS.GOOGLE:
      return createGoogleCalendarEvent(event, authData.accessToken);

    case CALENDAR_PROVIDERS.OUTLOOK:
      return createOutlookCalendarEvent(event, authData.accessToken);

    case CALENDAR_PROVIDERS.ICAL:
      return { blob: generateICalendarFile(event) };

    case CALENDAR_PROVIDERS.APPLE:
      // For Apple Calendar, we generate an ICS file and the user can import it
      return { blob: generateICalendarFile(event) };

    default:
      throw new Error(`Unsupported calendar provider: ${provider}`);
  }
};

/**
 * Get auth URL for a calendar provider
 * @param {string} provider - Calendar provider
 * @returns {string} - Authorization URL
 */
export const getAuthorizationUrl = provider => {
  // These would typically be environment variables in a real app
  const clientIds = {
    [CALENDAR_PROVIDERS.GOOGLE]: process.env.REACT_APP_GOOGLE_CLIENT_ID,
    [CALENDAR_PROVIDERS.OUTLOOK]: process.env.REACT_APP_MICROSOFT_CLIENT_ID,
  };

  const redirectUri = window.location.origin + '/calendar-auth-callback';

  switch (provider) {
    case CALENDAR_PROVIDERS.GOOGLE:
      return `https://accounts.google.com/o/oauth2/v2/auth?client_id=${clientIds[provider]}&redirect_uri=${encodeURIComponent(redirectUri)}&response_type=token&scope=https://www.googleapis.com/auth/calendar.events`;

    case CALENDAR_PROVIDERS.OUTLOOK:
      return `https://login.microsoftonline.com/common/oauth2/v2.0/authorize?client_id=${clientIds[provider]}&redirect_uri=${encodeURIComponent(redirectUri)}&response_type=token&scope=Calendars.ReadWrite`;

    default:
      return null; // Other providers don't need OAuth
  }
};

export default {
  CALENDAR_PROVIDERS,
  EVENT_TYPES,
  PRIORITY_LEVELS,
  createCalendarEvent,
  createGoogleCalendarEvent,
  createOutlookCalendarEvent,
  generateICalendarFile,
  downloadICalendarFile,
  getAuthorizationUrl,
};
