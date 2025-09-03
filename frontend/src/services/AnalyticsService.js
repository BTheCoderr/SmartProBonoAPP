import { trackGAEvent, ANALYTICS_EVENTS } from '../config/analytics';

class AnalyticsService {
  static sessionData = {
    startTime: null,
    interactions: [],
    fieldTimings: {},
    errors: [],
    formProgress: {}
  };

  static initializeSession(formType) {
    this.sessionData = {
      startTime: new Date(),
      interactions: [],
      fieldTimings: {},
      errors: [],
      formProgress: {}
    };
    localStorage.setItem(`${formType}_session`, JSON.stringify(this.sessionData));
  }

  static async trackFormView(formType) {
    try {
      const data = {
        formType,
        timestamp: new Date().toISOString(),
        referrer: document.referrer,
        userAgent: navigator.userAgent,
        deviceInfo: {
          screenSize: `${window.screen.width}x${window.screen.height}`,
          viewport: `${window.innerWidth}x${window.innerHeight}`,
          devicePixelRatio: window.devicePixelRatio,
          platform: navigator.platform
        }
      };
      

      
      // Track in GA4
      trackGAEvent(ANALYTICS_EVENTS.FORM_VIEW, {
        form_type: formType,
        device_info: data.deviceInfo
      });
    } catch (error) {
      console.error('Error tracking form view:', error);
    }
  }

  static async trackFormStart(formType) {
    try {
      this.initializeSession(formType);
      const data = { 
        formType, 
        timestamp: new Date().toISOString(),
        userAgent: navigator.userAgent,
        screenSize: {
          width: window.innerWidth,
          height: window.innerHeight
        },
        sessionId: this.generateSessionId(),
        previousAttempts: this.getPreviousAttempts(formType)
      };
      

      
      // Track in GA4
      trackGAEvent(ANALYTICS_EVENTS.FORM_START, {
        form_type: formType,
        session_id: data.sessionId,
        previous_attempts: data.previousAttempts.length
      });
    } catch (error) {
      console.error('Error tracking form start:', error);
    }
  }

  static async trackFormCompletion(formType, completionData) {
    try {
      const sessionData = this.getSessionData(formType);
      const data = {
        formType,
        completionTime: new Date() - sessionData.startTime,
        timestamp: new Date().toISOString(),
        formMetrics: this.getFormMetrics(formType),
        fieldTimings: sessionData.fieldTimings,
        interactionCount: sessionData.interactions.length,
        errorCount: sessionData.errors.length,
        completionPath: this.getCompletionPath(formType),
        validationAttempts: this.getValidationAttempts(formType),
        ...completionData
      };
      

      
      // Track in GA4
      trackGAEvent(ANALYTICS_EVENTS.FORM_COMPLETION, {
        form_type: formType,
        completion_time: data.completionTime,
        interaction_count: data.interactionCount,
        error_count: data.errorCount
      });
      
      this.clearSessionData(formType);
    } catch (error) {
      console.error('Error tracking form completion:', error);
    }
  }

  static async trackFormAbandonment(formType, lastStep, completionPercentage) {
    try {
      const sessionData = this.getSessionData(formType);
      const data = {
        formType,
        lastStep,
        completionPercentage,
        timestamp: new Date().toISOString(),
        timeSpent: new Date() - sessionData.startTime,
        lastInteraction: sessionData.interactions[sessionData.interactions.length - 1],
        abandonmentReason: this.getAbandonmentReason(formType),
        incompleteFields: this.getIncompleteFields(formType),
        formProgress: sessionData.formProgress
      };

      // Log the data for debugging
      console.log('Form abandonment data:', data);

    } catch (error) {
      console.error('Error tracking form abandonment:', error);
    }
  }

  static async trackFieldInteraction(formType, fieldName, value, interactionType = 'change') {
    try {
      const interaction = {
        fieldName,
        interactionType,
        timestamp: new Date().toISOString(),
        valueLength: typeof value === 'string' ? value.length : null,
        isValid: this.validateField(fieldName, value),
        validationErrors: this.getFieldValidationErrors(fieldName, value),
        timeSpent: this.getFieldTimeSpent(formType, fieldName)
      };
      
      this.updateSessionInteractions(formType, interaction);
      

    } catch (error) {
      console.error('Error tracking field interaction:', error);
    }
  }

  static async trackFieldTiming(formType, fieldName, duration) {
    try {
      const timing = {
        formType,
        fieldName,
        duration,
        timestamp: new Date().toISOString(),
        interactionCount: this.getFieldInteractionCount(formType, fieldName),
        validationAttempts: this.getFieldValidationAttempts(formType, fieldName)
      };
      
      // Log the timing for debugging
      console.log('Field timing data:', timing);
      
      this.updateFieldTiming(formType, fieldName, duration);
      

    } catch (error) {
      console.error('Error tracking field timing:', error);
    }
  }

  static async trackFormError(formType, errorType, errorDetails) {
    try {
      const error = {
        formType,
        errorType,
        errorDetails,
        timestamp: new Date().toISOString(),
        stackTrace: new Error().stack,
        currentStep: this.getCurrentStep(formType),
        formState: this.getFormState(formType),
        browserInfo: {
          userAgent: navigator.userAgent,
          platform: navigator.platform,
          language: navigator.language
        }
      };
      
      this.updateSessionErrors(formType, error);
      

    } catch (error) {
      console.error('Error tracking form error:', error);
    }
  }

  // Analytics Retrieval Methods












  // Helper Methods
  static generateSessionId() {
    return `${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
  }

  static getSessionData(formType) {
    const data = localStorage.getItem(`${formType}_session`);
    return data ? JSON.parse(data) : this.sessionData;
  }

  static updateSessionInteractions(formType, interaction) {
    const sessionData = this.getSessionData(formType);
    sessionData.interactions.push(interaction);
    localStorage.setItem(`${formType}_session`, JSON.stringify(sessionData));
  }

  static updateFieldTiming(formType, fieldName, duration) {
    const sessionData = this.getSessionData(formType);
    if (!sessionData.fieldTimings[fieldName]) {
      sessionData.fieldTimings[fieldName] = [];
    }
    sessionData.fieldTimings[fieldName].push(duration);
    localStorage.setItem(`${formType}_session`, JSON.stringify(sessionData));
  }

  static updateSessionErrors(formType, error) {
    const sessionData = this.getSessionData(formType);
    sessionData.errors.push(error);
    localStorage.setItem(`${formType}_session`, JSON.stringify(sessionData));
  }

  static clearSessionData(formType) {
    localStorage.removeItem(`${formType}_session`);
  }

  static getFieldTimeSpent(formType, fieldName) {
    const sessionData = this.getSessionData(formType);
    const timings = sessionData.fieldTimings[fieldName] || [];
    return timings.reduce((sum, time) => sum + time, 0);
  }

  static getFieldInteractionCount(formType, fieldName) {
    const sessionData = this.getSessionData(formType);
    return sessionData.interactions.filter(i => i.fieldName === fieldName).length;
  }

  static getFieldValidationAttempts(formType, fieldName) {
    const sessionData = this.getSessionData(formType);
    return sessionData.interactions.filter(
      i => i.fieldName === fieldName && i.validationErrors
    ).length;
  }

  static getPreviousAttempts(formType) {
    const attempts = localStorage.getItem(`${formType}_attempts`);
    return attempts ? JSON.parse(attempts) : [];
  }

  static getCompletionPath(formType) {
    const sessionData = this.getSessionData(formType);
    return sessionData.interactions.map(i => ({
      fieldName: i.fieldName,
      timestamp: i.timestamp
    }));
  }

  static getAbandonmentReason(formType) {
    const sessionData = this.getSessionData(formType);
    const lastError = sessionData.errors[sessionData.errors.length - 1];
    const lastInteraction = sessionData.interactions[sessionData.interactions.length - 1];
    
    if (lastError) {
      return { type: 'error', details: lastError };
    }
    
    if (lastInteraction && !lastInteraction.isValid) {
      return { type: 'validation', details: lastInteraction };
    }
    
    return { type: 'unknown' };
  }

  static getIncompleteFields(formType) {
    const sessionData = this.getSessionData(formType);
    // Log the session data for debugging
    console.log('Session data for incomplete fields:', sessionData);
    const formState = this.getFormState(formType);
    
    return Object.entries(formState)
      .filter(([_, value]) => !value || value.length === 0)
      .map(([field]) => field);
  }

  static getFormState(formType) {
    const draft = localStorage.getItem(`${formType}FormDraft`);
    return draft ? JSON.parse(draft).values : {};
  }

  static getCurrentStep(formType) {
    const sessionData = this.getSessionData(formType);
    return sessionData.formProgress.currentStep;
  }

  static validateField(fieldName, value) {
    // Enhanced validation logic can be implemented here
    return value !== null && value !== undefined && value !== '';
  }

  static getFieldValidationErrors(fieldName, value) {
    // Implement field-specific validation logic
    const errors = [];
    if (!value) errors.push('required');
    return errors;
  }

  static getFormMetrics(formType) {
    const draft = localStorage.getItem(`${formType}FormDraft`);
    if (!draft) return null;

    const { values, timestamp } = JSON.parse(draft);
    return {
      fieldCount: Object.keys(values).length,
      filledFields: Object.values(values).filter(v => v !== '' && v !== null).length,
      lastModified: timestamp
    };
  }

  static getTimeSpent(formType) {
    const start = localStorage.getItem(`${formType}StartTime`);
    return start ? Date.now() - new Date(start).getTime() : 0;
  }

  static getLastInteraction(formType) {
    const interactions = JSON.parse(localStorage.getItem(`${formType}Interactions`) || '[]');
    return interactions[interactions.length - 1] || null;
  }
}

export default AnalyticsService; 