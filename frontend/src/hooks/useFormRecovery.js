import { useState, useEffect } from 'react';
import ApiService from '../services/ApiService';

const useFormRecovery = (formType, initialValues) => {
  const [recoveredData, setRecoveredData] = useState(null);
  const [isRecovering, setIsRecovering] = useState(true);
  const [lastAutoSave, setLastAutoSave] = useState(null);

  useEffect(() => {
    const recoverForm = async () => {
      try {
        // Check localStorage first
        const localDraft = localStorage.getItem(`${formType}FormDraft`);
        if (localDraft) {
          const parsed = JSON.parse(localDraft);
          if (parsed.timestamp > (lastAutoSave?.timestamp || 0)) {
            setRecoveredData(parsed);
            setLastAutoSave(parsed);
            setIsRecovering(false);
            return;
          }
        }

        // Check server-side drafts
        const response = await ApiService.get(`/api/drafts/${formType}/latest`);
        if (response.data && (!lastAutoSave || response.data.timestamp > lastAutoSave.timestamp)) {
          setRecoveredData(response.data);
          setLastAutoSave(response.data);
        }
      } catch (err) {
        console.error('Error recovering form:', err);
      } finally {
        setIsRecovering(false);
      }
    };

    recoverForm();
  }, [formType]);

  const saveRecoveryPoint = async (values) => {
    try {
      const timestamp = Date.now();
      const recoveryData = { values, timestamp };
      
      // Save locally
      localStorage.setItem(
        `${formType}FormDraft`,
        JSON.stringify(recoveryData)
      );

      // Save to server
      await ApiService.post(`/api/drafts/${formType}`, recoveryData);
      
      setLastAutoSave(recoveryData);
    } catch (err) {
      console.error('Error saving recovery point:', err);
    }
  };

  const clearRecoveryData = async () => {
    try {
      localStorage.removeItem(`${formType}FormDraft`);
      await ApiService.delete(`/api/drafts/${formType}`);
      setRecoveredData(null);
      setLastAutoSave(null);
    } catch (err) {
      console.error('Error clearing recovery data:', err);
    }
  };

  return {
    recoveredData,
    isRecovering,
    lastAutoSave,
    saveRecoveryPoint,
    clearRecoveryData
  };
};

export default useFormRecovery; 