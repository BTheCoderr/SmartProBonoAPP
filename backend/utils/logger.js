const winston = require('winston');
const path = require('path');

// Define log levels
const levels = {
  error: 0,
  warn: 1,
  info: 2,
  http: 3,
  debug: 4,
};

// Define colors for each level
const colors = {
  error: 'red',
  warn: 'yellow',
  info: 'green',
  http: 'magenta',
  debug: 'white',
};

// Tell winston about these colors
winston.addColors(colors);

// Custom format for logging
const format = winston.format.combine(
  winston.format.timestamp({ format: 'YYYY-MM-DD HH:mm:ss:ms' }),
  winston.format.colorize({ all: true }),
  winston.format.printf(
    (info) => `${info.timestamp} ${info.level}: ${info.message}`
  )
);

// Define which transports the logger must use
const transports = [
  // Console transport
  new winston.transports.Console(),
  
  // Write all logs with level 'error' and below to error.log
  new winston.transports.File({
    filename: path.join(__dirname, '../logs/error.log'),
    level: 'error',
  }),
  
  // Write all logs with level 'info' and below to combined.log
  new winston.transports.File({
    filename: path.join(__dirname, '../logs/combined.log'),
  }),
  
  // Separate security audit log
  new winston.transports.File({
    filename: path.join(__dirname, '../logs/audit.log'),
    level: 'info',
  }),
];

// Create a logger instance
const createLogger = (service) => {
  return winston.createLogger({
    level: process.env.NODE_ENV === 'development' ? 'debug' : 'info',
    levels,
    format: winston.format.combine(
      winston.format.label({ label: service }),
      winston.format.timestamp(),
      winston.format.metadata({
        fillExcept: ['message', 'level', 'timestamp', 'label']
      }),
      winston.format.json()
    ),
    defaultMeta: { service },
    transports,
    // Handle exceptions and rejections
    exceptionHandlers: [
      new winston.transports.File({ 
        filename: path.join(__dirname, '../logs/exceptions.log')
      })
    ],
    rejectionHandlers: [
      new winston.transports.File({ 
        filename: path.join(__dirname, '../logs/rejections.log')
      })
    ]
  });
};

// Create a stream object with a write function that will be used by morgan
const stream = {
  write: (message) => {
    const logger = createLogger('http');
    logger.http(message.trim());
  },
};

module.exports = {
  createLogger,
  stream,
}; 