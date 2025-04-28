import * as yup from 'yup';

// Regular expressions for validation
const PHONE_REGEX = /^\+?1?\d{10}$/;
const ZIP_CODE_REGEX = /^\d{5}(-\d{4})?$/;
const CURRENCY_REGEX = /^\d+(\.\d{2})?$/;
const DATE_REGEX = /^\d{4}-\d{2}-\d{2}$/;

// List of US state codes
const STATE_CODES = [
  'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA',
  'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD',
  'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ',
  'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC',
  'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY'
];

// Validation schemas for different sections
const partySchema = yup.object().shape({
  name: yup.string()
    .required('Name is required')
    .min(2, 'Name must be at least 2 characters')
    .max(100, 'Name must be less than 100 characters'),
  
  address: yup.string()
    .required('Address is required')
    .min(5, 'Address must be at least 5 characters'),
  
  phone: yup.string()
    .matches(PHONE_REGEX, 'Invalid phone number format')
    .nullable(),
  
  email: yup.string()
    .email('Invalid email address')
    .nullable()
});

const courtSchema = yup.object().shape({
  name: yup.string()
    .required('Court name is required')
    .min(3, 'Court name must be at least 3 characters'),
  
  county: yup.string()
    .required('County is required')
    .min(2, 'County must be at least 2 characters'),
  
  state: yup.string()
    .required('State is required')
    .oneOf(STATE_CODES, 'Invalid state code')
});

const claimSchema = yup.object().shape({
  amount: yup.string()
    .required('Claim amount is required')
    .matches(CURRENCY_REGEX, 'Invalid currency format'),
  
  description: yup.string()
    .required('Claim description is required')
    .min(10, 'Description must be at least 10 characters'),
  
  date: yup.string()
    .required('Date is required')
    .matches(DATE_REGEX, 'Date must be in YYYY-MM-DD format'),
  
  location: yup.string()
    .required('Location is required')
    .min(2, 'Location must be at least 2 characters')
});

const witnessSchema = yup.object().shape({
  name: yup.string()
    .required('Witness name is required')
    .min(2, 'Name must be at least 2 characters'),
  
  relation: yup.string()
    .required('Relation is required'),
  
  testimony: yup.string()
    .nullable()
});

const exhibitSchema = yup.object().shape({
  name: yup.string()
    .required('Exhibit name is required'),
  
  description: yup.string()
    .required('Description is required'),
  
  type: yup.string()
    .required('Type is required')
    .oneOf(['document', 'photo', 'receipt', 'contract', 'other'], 'Invalid exhibit type')
});

// Main validation schema for small claims form
export const smallClaimsSchema = yup.object().shape({
  title: yup.string()
    .required('Title is required'),
  
  description: yup.string()
    .nullable(),
  
  plaintiff: partySchema,
  defendant: partySchema,
  
  caseNumber: yup.string()
    .nullable(),
  
  court: courtSchema,
  claim: claimSchema,
  
  claimType: yup.string()
    .required('Claim type is required')
    .oneOf([
      'breach_of_contract',
      'property_damage',
      'personal_injury',
      'unpaid_debt',
      'consumer_dispute',
      'other'
    ], 'Invalid claim type'),
  
  facts: yup.array()
    .of(yup.string().required('Fact statement is required'))
    .min(1, 'At least one fact is required'),
  
  evidence: yup.array()
    .of(yup.string())
    .nullable(),
  
  witnesses: yup.array()
    .of(witnessSchema)
    .nullable(),
  
  settlementAttempts: yup.array()
    .of(yup.object().shape({
      date: yup.string()
        .required('Date is required')
        .matches(DATE_REGEX, 'Date must be in YYYY-MM-DD format'),
      method: yup.string()
        .required('Method is required'),
      outcome: yup.string()
        .required('Outcome is required')
    }))
    .nullable(),
  
  filingDate: yup.string()
    .required('Filing date is required')
    .matches(DATE_REGEX, 'Date must be in YYYY-MM-DD format'),
  
  filingFee: yup.string()
    .required('Filing fee is required')
    .matches(CURRENCY_REGEX, 'Invalid currency format'),
  
  exhibits: yup.array()
    .of(exhibitSchema)
    .nullable()
});

// Helper function to validate form data
export const validateFormData = async (schema, data) => {
  try {
    await schema.validate(data, { abortEarly: false });
    return { isValid: true, errors: null };
  } catch (err) {
    const errors = err.inner.reduce((acc, error) => {
      acc[error.path] = error.message;
      return acc;
    }, {});
    return { isValid: false, errors };
  }
};

// Helper function to format validation errors for display
export const formatValidationErrors = (errors) => {
  if (!errors) return [];
  
  return Object.entries(errors).map(([field, message]) => ({
    field,
    message,
    path: field.split('.')
  }));
};

// Helper function to check if a section is valid
export const isSectionValid = async (schema, data) => {
  try {
    await schema.validate(data);
    return true;
  } catch (err) {
    return false;
  }
}; 