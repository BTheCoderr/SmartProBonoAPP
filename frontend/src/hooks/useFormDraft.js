import { useState, useEffect } from 'react';

const useFormDraft = (formType, initialValues) => {
  const [values, setValues] = useState(initialValues);
  const [lastSaved, setLastSaved] = useState(null);
  const [isSaving, setIsSaving] = useState(false);
  const [error, setError] = useState(null);

  // Load draft on mount
  useEffect(() => {
    const loadDraft = () => {
      try {
        const savedDraft = localStorage.getItem(`${formType}FormDraft`);
        if (savedDraft) {
          const parsedDraft = JSON.parse(savedDraft);
          setValues(parsedDraft.values);
          setLastSaved(new Date(parsedDraft.timestamp));
        }
      } catch (err) {
        console.error('Error loading draft:', err);
        setError('Failed to load draft');
      }
    };

    loadDraft();
  }, [formType]);

  // Save draft
  const saveDraft = async () => {
    setIsSaving(true);
    setError(null);

    try {
      const draftData = {
        values,
        timestamp: new Date().toISOString(),
        formType
      };

      localStorage.setItem(`${formType}FormDraft`, JSON.stringify(draftData));
      setLastSaved(new Date());
    } catch (err) {
      console.error('Error saving draft:', err);
      setError('Failed to save draft');
    } finally {
      setIsSaving(false);
    }
  };

  // Clear draft
  const clearDraft = () => {
    try {
      localStorage.removeItem(`${formType}FormDraft`);
      setValues(initialValues);
      setLastSaved(null);
    } catch (err) {
      console.error('Error clearing draft:', err);
      setError('Failed to clear draft');
    }
  };

  // Auto-save functionality
  const autoSave = () => {
    if (!isSaving) {
      saveDraft();
    }
  };

  // Calculate completion percentage
  const calculateCompletion = () => {
    const totalFields = Object.keys(initialValues).length;
    const filledFields = Object.entries(values).filter(([_, value]) => {
      if (Array.isArray(value)) {
        return value.length > 0;
      }
      if (typeof value === 'boolean') {
        return true;
      }
      return value !== '' && value !== null && value !== undefined;
    }).length;

    return Math.round((filledFields / totalFields) * 100);
  };

  return {
    values,
    setValues,
    lastSaved,
    isSaving,
    error,
    saveDraft,
    clearDraft,
    autoSave,
    calculateCompletion
  };
};

export default useFormDraft; 