import { useState, useEffect, useRef } from 'react';
import { useSnackbar } from 'notistack';
import AnalyticsService from '../services/AnalyticsService';

const useFormAutoSave = (formType, values, initialValues) => {
  const { enqueueSnackbar } = useSnackbar();
  const [lastSaved, setLastSaved] = useState(null);
  const [isSaving, setIsSaving] = useState(false);
  const [autoSaveEnabled, setAutoSaveEnabled] = useState(true);
  const autoSaveTimeoutRef = useRef(null);
  const lastSavedValuesRef = useRef(null);

  // Load draft on mount
  useEffect(() => {
    const loadDraft = () => {
      try {
        const savedDraft = localStorage.getItem(`${formType}FormDraft`);
        if (savedDraft) {
          const parsedDraft = JSON.parse(savedDraft);
          lastSavedValuesRef.current = parsedDraft.values;
          setLastSaved(new Date(parsedDraft.timestamp));
          return parsedDraft.values;
        }
      } catch (err) {
        console.error('Error loading draft:', err);
        enqueueSnackbar('Failed to load saved draft', { variant: 'error' });
      }
      return null;
    };

    const draft = loadDraft();
    if (draft) {
      // Track draft loaded
      AnalyticsService.trackFormStart(formType, 'draft_loaded');
    }

    return () => {
      if (autoSaveTimeoutRef.current) {
        clearTimeout(autoSaveTimeoutRef.current);
      }
    };
  }, [formType]);

  // Auto-save when values change
  useEffect(() => {
    if (!autoSaveEnabled || isSaving) return;

    // Clear any existing timeout
    if (autoSaveTimeoutRef.current) {
      clearTimeout(autoSaveTimeoutRef.current);
    }

    // Set new timeout for auto-save
    autoSaveTimeoutRef.current = setTimeout(() => {
      if (hasChanges()) {
        saveDraft(values);
      }
    }, 2000); // Auto-save after 2 seconds of no changes

    return () => {
      if (autoSaveTimeoutRef.current) {
        clearTimeout(autoSaveTimeoutRef.current);
      }
    };
  }, [values, autoSaveEnabled]);

  // Check if there are unsaved changes
  const hasChanges = () => {
    if (!lastSavedValuesRef.current) return true;
    return JSON.stringify(values) !== JSON.stringify(lastSavedValuesRef.current);
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

  // Save draft
  const saveDraft = async (valuesToSave = values) => {
    if (isSaving) return;
    
    setIsSaving(true);
    try {
      const completionPercentage = calculateCompletion();
      const draftData = {
        values: valuesToSave,
        timestamp: new Date().toISOString(),
        formType,
        completionPercentage
      };

      localStorage.setItem(`${formType}FormDraft`, JSON.stringify(draftData));
      lastSavedValuesRef.current = valuesToSave;
      setLastSaved(new Date());

      // Track draft saved
      await AnalyticsService.trackFormProgress(formType, 'draft_saved', completionPercentage);

      enqueueSnackbar('Draft saved', { 
        variant: 'success',
        autoHideDuration: 2000
      });
    } catch (err) {
      console.error('Error saving draft:', err);
      enqueueSnackbar('Failed to save draft', { variant: 'error' });
    } finally {
      setIsSaving(false);
    }
  };

  // Clear draft
  const clearDraft = async () => {
    try {
      localStorage.removeItem(`${formType}FormDraft`);
      lastSavedValuesRef.current = null;
      setLastSaved(null);

      // Track draft cleared
      await AnalyticsService.trackFormProgress(formType, 'draft_cleared');

      enqueueSnackbar('Draft cleared', { variant: 'success' });
    } catch (err) {
      console.error('Error clearing draft:', err);
      enqueueSnackbar('Failed to clear draft', { variant: 'error' });
    }
  };

  // Toggle auto-save
  const toggleAutoSave = () => {
    setAutoSaveEnabled(!autoSaveEnabled);
    enqueueSnackbar(`Auto-save ${!autoSaveEnabled ? 'enabled' : 'disabled'}`, {
      variant: 'info'
    });
  };

  return {
    lastSaved,
    isSaving,
    autoSaveEnabled,
    hasChanges,
    saveDraft,
    clearDraft,
    toggleAutoSave,
    calculateCompletion
  };
};

export default useFormAutoSave; 