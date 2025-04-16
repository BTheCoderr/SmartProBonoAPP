import { isDevelopment } from './environment';

// Log levels
export const LogLevel = {
  ERROR: 'error',
  WARN: 'warn',
  INFO: 'info',
  DEBUG: 'debug',
};

// Default configuration
const config = {
  level: isDevelopment ? LogLevel.DEBUG : LogLevel.ERROR,
  enableConsole: isDevelopment,
  // Add more configuration options as needed
};

// Helper to check if we should log at this level
const shouldLog = (messageLevel) => {
  const levels = Object.values(LogLevel);
  const configLevelIndex = levels.indexOf(config.level);
  const messageLevelIndex = levels.indexOf(messageLevel);
  return messageLevelIndex <= configLevelIndex;
};

// Format the log message
const formatMessage = (level, message, data) => {
  const timestamp = new Date().toISOString();
  return {
    timestamp,
    level,
    message,
    data,
  };
};

// Main logging functions
/* eslint-disable no-console */
const logToConsole = (level, formattedLog) => {
  if (!config.enableConsole) return;

  const { timestamp, message, data } = formattedLog;
  const prefix = `[${timestamp}] ${level.toUpperCase()}:`;

  switch (level) {
    case LogLevel.ERROR:
      // Using function form to satisfy ESLint
      if (data) {
        console.error(prefix, message, data);
      } else {
        console.error(prefix, message);
      }
      break;
    case LogLevel.WARN:
      if (data) {
        console.warn(prefix, message, data);
      } else {
        console.warn(prefix, message);
      }
      break;
    case LogLevel.INFO:
      if (data) {
        console.info(prefix, message, data);
      } else {
        console.info(prefix, message);
      }
      break;
    case LogLevel.DEBUG:
      if (data) {
        console.debug(prefix, message, data);
      } else {
        console.debug(prefix, message);
      }
      break;
    default:
      if (data) {
        console.log(prefix, message, data);
      } else {
        console.log(prefix, message);
      }
  }
};
/* eslint-enable no-console */

// Export logging functions
export const logger = {
  error: (message, data) => {
    if (shouldLog(LogLevel.ERROR)) {
      const formattedLog = formatMessage(LogLevel.ERROR, message, data);
      logToConsole(LogLevel.ERROR, formattedLog);
      // Here you could add additional logging destinations (e.g., error monitoring service)
    }
  },

  warn: (message, data) => {
    if (shouldLog(LogLevel.WARN)) {
      const formattedLog = formatMessage(LogLevel.WARN, message, data);
      logToConsole(LogLevel.WARN, formattedLog);
    }
  },

  info: (message, data) => {
    if (shouldLog(LogLevel.INFO)) {
      const formattedLog = formatMessage(LogLevel.INFO, message, data);
      logToConsole(LogLevel.INFO, formattedLog);
    }
  },

  debug: (message, data) => {
    if (shouldLog(LogLevel.DEBUG)) {
      const formattedLog = formatMessage(LogLevel.DEBUG, message, data);
      logToConsole(LogLevel.DEBUG, formattedLog);
    }
  },

  // Configure logger settings
  configure: (options) => {
    Object.assign(config, options);
  },
};

// Simple export aliases for direct use in other files
export const logError = (message, data) => logger.error(message, data);
export const logWarn = (message, data) => logger.warn(message, data);
export const logInfo = (message, data) => logger.info(message, data);
export const logDebug = (message, data) => logger.debug(message, data);

export default logger;