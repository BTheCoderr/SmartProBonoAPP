const rateLimit = require('express-rate-limit');
const helmet = require('helmet');
const hpp = require('hpp');
const mongoSanitize = require('express-mongo-sanitize');
const xss = require('xss-clean');
const { createLogger } = require('../utils/logger');

const logger = createLogger('security-middleware');

// Rate limiting configuration
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // Limit each IP to 100 requests per windowMs
  message: 'Too many requests from this IP, please try again later.',
  standardHeaders: true,
  legacyHeaders: false,
});

// API specific rate limiter
const apiLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 50,
  message: 'Too many API requests from this IP, please try again later.',
  standardHeaders: true,
  legacyHeaders: false,
});

// Document upload rate limiter
const uploadLimiter = rateLimit({
  windowMs: 60 * 60 * 1000, // 1 hour
  max: 10, // Limit each IP to 10 uploads per hour
  message: 'Too many document uploads from this IP, please try again later.',
});

// Security audit logging middleware
const auditLog = (req, res, next) => {
  const start = Date.now();
  res.on('finish', () => {
    const duration = Date.now() - start;
    logger.info({
      method: req.method,
      path: req.path,
      status: res.statusCode,
      duration,
      ip: req.ip,
      user: req.user ? req.user.id : 'anonymous'
    });
  });
  next();
};

// HTTPS enforcement middleware
const enforceHTTPS = (req, res, next) => {
  if (process.env.NODE_ENV === 'production' && !req.secure) {
    return res.redirect('https://' + req.headers.host + req.url);
  }
  next();
};

// Sensitive data sanitization
const sanitizeData = (req, res, next) => {
  // Remove any keys containing sensitive keywords
  const sensitiveKeys = ['ssn', 'password', 'secret', 'token'];
  
  const sanitizeObject = (obj) => {
    Object.keys(obj).forEach(key => {
      if (typeof obj[key] === 'object') {
        sanitizeObject(obj[key]);
      } else if (sensitiveKeys.some(sensitive => key.toLowerCase().includes(sensitive))) {
        obj[key] = '[REDACTED]';
      }
    });
  };

  if (req.body) sanitizeObject(req.body);
  if (req.params) sanitizeObject(req.params);
  if (req.query) sanitizeObject(req.query);

  next();
};

// Document access control middleware
const documentAccessControl = (req, res, next) => {
  const documentId = req.params.documentId || req.body.documentId;
  if (!documentId) return next();

  // Log document access
  logger.info({
    action: 'document_access',
    documentId,
    userId: req.user ? req.user.id : null,
    timestamp: new Date(),
    ip: req.ip
  });

  // TODO: Implement document access validation
  // This should check if the user has permission to access the document
  next();
};

module.exports = {
  // Apply basic security headers
  securityHeaders: helmet({
    contentSecurityPolicy: {
      directives: {
        defaultSrc: ["'self'"],
        styleSrc: ["'self'", "'unsafe-inline'"],
        scriptSrc: ["'self'"],
        imgSrc: ["'self'", "data:", "https:"],
        connectSrc: ["'self'", "https://api.openai.com"],
        frameSrc: ["'none'"],
        objectSrc: ["'none'"]
      }
    },
    crossOriginEmbedderPolicy: true,
    crossOriginOpenerPolicy: true,
    crossOriginResourcePolicy: { policy: "same-site" },
    dnsPrefetchControl: true,
    frameguard: { action: "deny" },
    hidePoweredBy: true,
    hsts: {
      maxAge: 31536000,
      includeSubDomains: true,
      preload: true
    },
    ieNoOpen: true,
    noSniff: true,
    referrerPolicy: { policy: "strict-origin-when-cross-origin" },
    xssFilter: true
  }),

  // Rate limiters
  limiter,
  apiLimiter,
  uploadLimiter,

  // MongoDB query sanitization
  mongoSanitize: mongoSanitize(),

  // XSS prevention
  xssProtection: xss(),

  // HTTP Parameter Pollution prevention
  hpp: hpp(),

  // Custom middleware
  auditLog,
  enforceHTTPS,
  sanitizeData,
  documentAccessControl
}; 