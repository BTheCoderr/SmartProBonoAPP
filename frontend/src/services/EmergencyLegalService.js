import axios from 'axios';
import config from '../config';
import { logInfo, logError } from '../utils/logger';

const EmergencyLegalService = {
  /**
   * Get the current availability of legal advocates
   * @returns {Promise} Promise with availability data
   */
  getAvailability: async () => {
    try {
      const response = await axios.get(`${config.apiUrl}/api/emergency-legal/availability`);
      return response.data;
    } catch (error) {
      logError('Error fetching advocate availability:', error);
      throw error;
    }
  },

  /**
   * Submit triage information to get connected with a legal advocate
   * @param {Object} triageData - Information about the legal emergency
   * @returns {Promise} Promise with connection details
   */
  submitTriage: async triageData => {
    try {
      const response = await axios.post(`${config.apiUrl}/api/emergency-legal/triage`, triageData);
      return response.data;
    } catch (error) {
      logError('Error submitting triage information:', error);
      throw error;
    }
  },

  /**
   * Get the status of an ongoing or completed call
   * @param {string} caseId - The unique case ID
   * @returns {Promise} Promise with call status information
   */
  getCallStatus: async caseId => {
    try {
      const response = await axios.get(
        `${config.apiUrl}/api/emergency-legal/call/${caseId}/status`
      );
      return response.data;
    } catch (error) {
      logError(`Error fetching call status for case ${caseId}:`, error);
      throw error;
    }
  },

  /**
   * End an ongoing call
   * @param {string} caseId - The unique case ID
   * @returns {Promise} Promise with call end confirmation
   */
  endCall: async caseId => {
    try {
      const response = await axios.post(`${config.apiUrl}/api/emergency-legal/call/${caseId}/end`);
      return response.data;
    } catch (error) {
      logError(`Error ending call for case ${caseId}:`, error);
      throw error;
    }
  },

  /**
   * Toggle recording for a call
   * @param {string} caseId - The unique case ID
   * @param {string} action - Either "start" or "stop"
   * @returns {Promise} Promise with recording status update
   */
  toggleRecording: async (caseId, action) => {
    try {
      const response = await axios.post(
        `${config.apiUrl}/api/emergency-legal/call/${caseId}/recording`,
        { recording_action: action }
      );
      return response.data;
    } catch (error) {
      logError(`Error toggling recording for case ${caseId}:`, error);
      throw error;
    }
  },

  /**
   * Initialize a Jitsi Meet conference
   * @param {string} roomName - The name of the Jitsi room (usually case ID)
   * @param {HTMLElement} parentNode - The DOM element to place the conference
   * @param {Object} options - Additional options for the conference
   * @returns {Object} The Jitsi Meet API instance
   */
  initializeJitsiMeet: (roomName, parentNode, options = {}) => {
    // This is a facade for the actual Jitsi Meet implementation
    // In production, this would interact with the Jitsi Meet External API

    logInfo('Initializing Jitsi Meet with:', { roomName, options });

    // Check if JitsiMeetExternalAPI is available
    if (typeof window.JitsiMeetExternalAPI === 'undefined') {
      logError(
        'Jitsi Meet External API not loaded. Make sure to include the script in your HTML.'
      );
      return null;
    }

    try {
      // Default domain for Jitsi Meet
      const domain = options.domain || 'meet.jit.si';

      // Default configuration options
      const defaultOptions = {
        roomName,
        width: '100%',
        height: '100%',
        parentNode,
        userInfo: {
          displayName: options.displayName || 'Legal Support User',
        },
        configOverwrite: {
          startWithAudioMuted: options.startMuted?.audio || false,
          startWithVideoMuted: options.startMuted?.video || true,
          enableClosePage: false,
          prejoinPageEnabled: false,
          disableDeepLinking: true,
          ...options.configOverwrite,
        },
        interfaceConfigOverwrite: {
          TOOLBAR_BUTTONS: [
            'microphone',
            'camera',
            'closedcaptions',
            'desktop',
            'fullscreen',
            'fodeviceselection',
            'hangup',
            'chat',
            'settings',
            'raisehand',
            'videoquality',
            'filmstrip',
            'tileview',
          ],
          ...options.interfaceConfigOverwrite,
        },
      };

      // Create and return the API instance
      return new window.JitsiMeetExternalAPI(domain, defaultOptions);
    } catch (error) {
      logError('Error initializing Jitsi Meet:', error);
      return null;
    }
  },
};

export default EmergencyLegalService;
