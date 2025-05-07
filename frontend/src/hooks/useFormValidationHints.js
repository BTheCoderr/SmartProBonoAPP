import { useState, useEffect } from 'react';

const useFormValidationHints = (formik, validationSchema) => {
  const [fieldHints, setFieldHints] = useState({});
  const [estimatedTime, setEstimatedTime] = useState(0);
  const [fieldTimes, setFieldTimes] = useState({});

  // Generate field hints based on validation schema
  useEffect(() => {
    const hints = {};
    if (validationSchema) {
      Object.keys(validationSchema.fields).forEach(field => {
        const tests = validationSchema.fields[field].tests;
        hints[field] = tests.map(test => {
          switch (test.name) {
            case 'required':
              return 'This field is required';
            case 'min':
              return `Minimum ${test.params.min} characters`;
            case 'max':
              return `Maximum ${test.params.max} characters`;
            case 'email':
              return 'Must be a valid email address';
            case 'matches':
              return 'Must match the required format';
            case 'positive':
              return 'Must be a positive number';
            default:
              return test.message;
          }
        });
      });
    }
    setFieldHints(hints);
  }, [validationSchema]);

  // Track field completion times
  useEffect(() => {
    const startTimes = {};
    const completionTimes = {};
    let totalEstimatedTime = 0;

    const handleFieldFocus = (fieldName) => {
      startTimes[fieldName] = Date.now();
    };

    const handleFieldBlur = (fieldName) => {
      if (startTimes[fieldName] && formik.values[fieldName]) {
        const completionTime = Date.now() - startTimes[fieldName];
        completionTimes[fieldName] = completionTime;
        setFieldTimes(prev => ({
          ...prev,
          [fieldName]: completionTime
        }));

        // Update estimated time for remaining fields
        const remainingFields = Object.keys(formik.values).filter(
          field => !formik.values[field] && formik.touched[field]
        );
        
        const avgCompletionTime = Object.values(completionTimes).reduce(
          (sum, time) => sum + time, 0
        ) / Object.keys(completionTimes).length;

        totalEstimatedTime = remainingFields.length * avgCompletionTime;
        setEstimatedTime(totalEstimatedTime);
      }
    };

    // Add event listeners to form fields
    Object.keys(formik.values).forEach(fieldName => {
      const element = document.querySelector(`[name="${fieldName}"]`);
      if (element) {
        element.addEventListener('focus', () => handleFieldFocus(fieldName));
        element.addEventListener('blur', () => handleFieldBlur(fieldName));
      }
    });

    return () => {
      // Clean up event listeners
      Object.keys(formik.values).forEach(fieldName => {
        const element = document.querySelector(`[name="${fieldName}"]`);
        if (element) {
          element.removeEventListener('focus', () => handleFieldFocus(fieldName));
          element.removeEventListener('blur', () => handleFieldBlur(fieldName));
        }
      });
    };
  }, [formik.values, formik.touched]);

  const getFieldHint = (fieldName) => {
    if (!fieldHints[fieldName]) return [];
    
    const hints = fieldHints[fieldName];
    const value = formik.values[fieldName];
    const errors = formik.errors[fieldName];
    
    return hints.filter(hint => {
      // Only show relevant hints based on current value and errors
      if (!value && errors) return true;
      if (hint.includes('required') && !value) return true;
      if (hint.includes('minimum') && value && value.length < parseInt(hint.match(/\d+/)[0])) return true;
      if (hint.includes('maximum') && value && value.length > parseInt(hint.match(/\d+/)[0])) return true;
      return false;
    });
  };

  const getEstimatedTimeForField = (fieldName) => {
    return fieldTimes[fieldName] || 0;
  };

  const getFormattedEstimatedTime = () => {
    const minutes = Math.ceil(estimatedTime / 60000);
    return minutes <= 1 ? '1 minute' : `${minutes} minutes`;
  };

  return {
    getFieldHint,
    getEstimatedTimeForField,
    getFormattedEstimatedTime,
    estimatedTime
  };
};

export default useFormValidationHints; 