import { useState, useEffect } from 'react';
import * as yup from 'yup';
import { useFormik } from 'formik';
import AnalyticsService from '../services/AnalyticsService';

const useFormValidation = (formType, initialValues, validationSchema, onSubmit) => {
  const [fieldErrors, setFieldErrors] = useState({});
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitError, setSubmitError] = useState(null);
  const [validationHistory, setValidationHistory] = useState([]);
  const [lastValidated, setLastValidated] = useState(null);

  // Initialize formik
  const formik = useFormik({
    initialValues,
    validationSchema,
    onSubmit: async (values, { setSubmitting }) => {
      setIsSubmitting(true);
      setSubmitError(null);

      try {
        // Track form submission attempt
        await AnalyticsService.trackFormCompletion(formType, Date.now() - lastValidated);
        
        // Call the provided onSubmit function
        await onSubmit(values);
        
        // Clear validation history on successful submit
        setValidationHistory([]);
      } catch (error) {
        setSubmitError(error.message || 'An error occurred while submitting the form');
        
        // Track form error
        await AnalyticsService.trackFormError(formType, 'submit', error.message);
        
        // Add to validation history
        setValidationHistory(prev => [...prev, {
          timestamp: new Date(),
          type: 'submit',
          error: error.message
        }]);
      } finally {
        setSubmitting(false);
        setIsSubmitting(false);
      }
    }
  });

  // Enhanced field-level validation
  const validateField = async (fieldName, value) => {
    try {
      // Create a schema for just this field
      const fieldSchema = yup.reach(validationSchema, fieldName);
      await fieldSchema.validate(value);
      
      // Clear error for this field
      setFieldErrors(prev => ({
        ...prev,
        [fieldName]: undefined
      }));

      // Track successful field completion
      await AnalyticsService.trackFieldCompletion(formType, fieldName, value);

      return true;
    } catch (error) {
      // Set error for this field
      setFieldErrors(prev => ({
        ...prev,
        [fieldName]: error.message
      }));

      // Track field error
      await AnalyticsService.trackFormError(formType, 'field', {
        field: fieldName,
        error: error.message
      });

      // Add to validation history
      setValidationHistory(prev => [...prev, {
        timestamp: new Date(),
        type: 'field',
        field: fieldName,
        error: error.message
      }]);

      return false;
    }
  };

  // Enhanced form-level validation
  const validateForm = async (values = formik.values) => {
    setLastValidated(Date.now());
    
    try {
      await validationSchema.validate(values, { abortEarly: false });
      setFieldErrors({});
      return true;
    } catch (error) {
      const newErrors = {};
      
      if (error.inner) {
        error.inner.forEach(err => {
          newErrors[err.path] = err.message;
        });
      }
      
      setFieldErrors(newErrors);

      // Track validation errors
      Object.entries(newErrors).forEach(async ([field, error]) => {
        await AnalyticsService.trackFormError(formType, 'validation', {
          field,
          error
        });
      });

      return false;
    }
  };

  // Auto-validate on mount and value changes
  useEffect(() => {
    const validate = async () => {
      if (Object.keys(formik.touched).length > 0) {
        await validateForm();
      }
    };

    validate();
  }, [formik.values]);

  // Helper to get field error message
  const getFieldError = (fieldName) => {
    return fieldErrors[fieldName] || formik.errors[fieldName];
  };

  // Helper to check if a field has been touched and has an error
  const hasFieldError = (fieldName) => {
    return formik.touched[fieldName] && Boolean(getFieldError(fieldName));
  };

  // Get validation history for a specific field
  const getFieldValidationHistory = (fieldName) => {
    return validationHistory.filter(entry => 
      entry.type === 'field' && entry.field === fieldName
    );
  };

  // Get overall form validation status
  const getFormValidationStatus = () => {
    const totalFields = Object.keys(initialValues).length;
    const validFields = Object.keys(formik.values).filter(field => 
      !getFieldError(field) && formik.touched[field]
    ).length;

    return {
      progress: Math.round((validFields / totalFields) * 100),
      validFields,
      totalFields,
      hasErrors: Object.keys(fieldErrors).length > 0,
      isValid: Object.keys(fieldErrors).length === 0 && formik.isValid
    };
  };

  return {
    formik,
    fieldErrors,
    isSubmitting,
    submitError,
    validationHistory,
    validateField,
    validateForm,
    getFieldError,
    hasFieldError,
    getFieldValidationHistory,
    getFormValidationStatus
  };
};

export default useFormValidation; 