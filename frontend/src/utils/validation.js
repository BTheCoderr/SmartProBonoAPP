import * as Yup from 'yup';

// Common validation patterns
const PHONE_REGEX = /^(\+\d{1,2}\s?)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}$/;
const ZIP_REGEX = /^\d{5}(-\d{4})?$/;
const CURRENCY_REGEX = /^\$?\d+(,\d{3})*(\.\d{2})?$/;

// Client Information Schema
export const clientInfoSchema = Yup.object().shape({
  firstName: Yup.string()
    .min(2, 'First name must be at least 2 characters')
    .max(50, 'First name must be less than 50 characters')
    .required('First name is required'),
  lastName: Yup.string()
    .min(2, 'Last name must be at least 2 characters')
    .max(50, 'Last name must be less than 50 characters')
    .required('Last name is required'),
  email: Yup.string()
    .email('Invalid email address')
    .required('Email is required'),
  phone: Yup.string()
    .matches(PHONE_REGEX, 'Invalid phone number')
    .required('Phone number is required'),
  address: Yup.object().shape({
    street: Yup.string().required('Street address is required'),
    city: Yup.string().required('City is required'),
    state: Yup.string().required('State is required'),
    zipCode: Yup.string()
      .matches(ZIP_REGEX, 'Invalid ZIP code')
      .required('ZIP code is required')
  })
});

// Legal Document Schema
export const legalDocumentSchema = Yup.object().shape({
  documentType: Yup.string().required('Document type is required'),
  caseNumber: Yup.string().when('documentType', {
    is: (type) => ['court_filing', 'legal_response'].includes(type),
    then: Yup.string().required('Case number is required')
  }),
  filingDate: Yup.date()
    .min(new Date(), 'Filing date cannot be in the past')
    .required('Filing date is required'),
  claimAmount: Yup.string()
    .matches(CURRENCY_REGEX, 'Invalid currency format')
    .when('documentType', {
      is: 'small_claims',
      then: Yup.string().required('Claim amount is required')
    }),
  description: Yup.string()
    .min(50, 'Description must be at least 50 characters')
    .max(5000, 'Description must be less than 5000 characters')
    .required('Description is required')
});

// Digital Signature Schema
export const signatureSchema = Yup.object().shape({
  signatureType: Yup.string()
    .oneOf(['drawn', 'typed'], 'Invalid signature type')
    .required('Signature type is required'),
  signatureData: Yup.string().required('Signature is required'),
  dateTime: Yup.date().required('Signature date is required'),
  ipAddress: Yup.string().required('IP address is required'),
  consent: Yup.boolean()
    .oneOf([true], 'You must agree to the terms')
    .required('Consent is required')
});

// Form Progress Schema
export const formProgressSchema = Yup.object().shape({
  currentStep: Yup.number().min(0).required(),
  completedSteps: Yup.array().of(Yup.number()),
  savedData: Yup.object(),
  lastUpdated: Yup.date().required()
});

// Custom validation functions
export const validateFormProgress = (values, schema) => {
  try {
    schema.validateSync(values, { abortEarly: false });
    return { isValid: true, errors: {} };
  } catch (err) {
    const errors = err.inner.reduce((acc, error) => {
      acc[error.path] = error.message;
      return acc;
    }, {});
    return { isValid: false, errors };
  }
};

export const validateSignature = async (signatureData) => {
  try {
    await signatureSchema.validate(signatureData, { abortEarly: false });
    return { isValid: true };
  } catch (err) {
    return { 
      isValid: false, 
      errors: err.inner.reduce((acc, error) => {
        acc[error.path] = error.message;
        return acc;
      }, {})
    };
  }
}; 