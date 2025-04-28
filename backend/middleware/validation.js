const { createLogger } = require('../utils/logger');
const Joi = require('joi');

const logger = createLogger('validation-middleware');

// Base validation schemas
const schemas = {
  // Document generation validation
  document: Joi.object({
    // Common fields for all legal documents
    title: Joi.string().required(),
    description: Joi.string(),
    
    // Party information
    plaintiff: Joi.object({
      name: Joi.string().required(),
      address: Joi.string().required(),
      phone: Joi.string(),
      email: Joi.string().email()
    }).required(),
    
    defendant: Joi.object({
      name: Joi.string().required(),
      address: Joi.string().required(),
      phone: Joi.string(),
      email: Joi.string().email()
    }).required(),
    
    // Case information
    caseNumber: Joi.string(),
    court: Joi.object({
      name: Joi.string().required(),
      county: Joi.string().required(),
      state: Joi.string().required()
    }).required(),
    
    // Claim details
    claim: Joi.object({
      amount: Joi.number().positive().required(),
      description: Joi.string().required(),
      date: Joi.date().iso().required(),
      location: Joi.string().required()
    }).required(),
    
    // Supporting information
    facts: Joi.array().items(Joi.string()).min(1).required(),
    evidence: Joi.array().items(Joi.string()),
    witnesses: Joi.array().items(Joi.object({
      name: Joi.string().required(),
      relation: Joi.string(),
      testimony: Joi.string()
    })),
    
    // Filing information
    filingDate: Joi.date().iso().required(),
    filingFee: Joi.number().positive(),
    
    // Additional metadata
    tags: Joi.array().items(Joi.string()),
    priority: Joi.string().valid('low', 'medium', 'high'),
    status: Joi.string().valid('draft', 'final', 'filed'),
    
    // Document-specific fields can be added in template-specific schemas
    templateSpecific: Joi.object()
  }),

  // Template-specific validation schemas
  smallClaimComplaint: Joi.object({
    // Inherit from base document schema
    ...schemas.document,
    
    // Additional fields specific to small claims
    claimType: Joi.string().valid(
      'breach_of_contract',
      'property_damage',
      'personal_injury',
      'unpaid_debt',
      'consumer_dispute',
      'other'
    ).required(),
    
    settlementAttempts: Joi.array().items(Joi.object({
      date: Joi.date().iso(),
      method: Joi.string(),
      outcome: Joi.string()
    })),
    
    exhibits: Joi.array().items(Joi.object({
      name: Joi.string().required(),
      description: Joi.string(),
      type: Joi.string().valid('document', 'photo', 'receipt', 'contract', 'other')
    }))
  })
};

// Validation middleware
const validateDocument = async (req, res, next) => {
  try {
    const { templateName } = req.params;
    const documentData = req.body;
    
    // Get the appropriate schema based on template
    let schema = schemas.document; // Default to base schema
    if (schemas[templateName]) {
      schema = schemas[templateName];
    }
    
    // Validate the document data
    const { error, value } = schema.validate(documentData, {
      abortEarly: false,
      stripUnknown: true,
      presence: 'required'
    });
    
    if (error) {
      logger.warn('Document validation failed:', {
        template: templateName,
        errors: error.details.map(detail => ({
          field: detail.path.join('.'),
          message: detail.message
        }))
      });
      
      return res.status(400).json({
        error: 'Validation Error',
        details: error.details.map(detail => ({
          field: detail.path.join('.'),
          message: detail.message
        }))
      });
    }
    
    // Add validated data to request
    req.validatedData = value;
    next();
  } catch (error) {
    logger.error('Validation middleware error:', error);
    res.status(500).json({ error: 'Validation processing failed' });
  }
};

// Validation helper functions
const validateDateFormat = (date) => {
  return /^\d{4}-\d{2}-\d{2}$/.test(date);
};

const validateCurrency = (amount) => {
  return /^\d+(\.\d{2})?$/.test(amount);
};

const validatePhoneNumber = (phone) => {
  return /^\+?1?\d{10}$/.test(phone);
};

const validateZipCode = (zip) => {
  return /^\d{5}(-\d{4})?$/.test(zip);
};

const validateStateCode = (state) => {
  const states = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA',
                  'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD',
                  'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ',
                  'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC',
                  'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY'];
  return states.includes(state.toUpperCase());
};

module.exports = {
  validateDocument,
  validateDateFormat,
  validateCurrency,
  validatePhoneNumber,
  validateZipCode,
  validateStateCode,
  schemas
}; 