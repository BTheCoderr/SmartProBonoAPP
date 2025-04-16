/**
 * bandwidthDetection.js
 * Utility for detecting and managing low bandwidth conditions
 */

import { useState, useEffect } from 'react';

// Constants
const LOW_BANDWIDTH_THRESHOLD = 500; // kbps
const BANDWIDTH_TEST_URL = '/api/bandwidth-test'; // Small test file for bandwidth check
const BANDWIDTH_CHECK_INTERVAL = 60000; // Check every minute
const BANDWIDTH_LOCAL_STORAGE_KEY = 'appBandwidthMode';
const LOW_BANDWIDTH_SETTING_KEY = 'lowBandwidthMode';

/**
 * Measures the current network bandwidth by downloading a small test file
 * @returns {Promise<number>} Bandwidth in kbps
 */
export const measureBandwidth = async () => {
  try {
    const startTime = Date.now();
    const response = await fetch(BANDWIDTH_TEST_URL, {
      method: 'GET',
      cache: 'no-store', // Prevent caching
    });

    if (!response.ok) {
      throw new Error('Network response was not ok');
    }

    const blob = await response.blob();
    const endTime = Date.now();
    const duration = (endTime - startTime) / 1000; // seconds
    const fileSizeInBits = blob.size * 8; // Convert bytes to bits
    const bandwidthInKbps = fileSizeInBits / 1000 / duration; // kbps

    return bandwidthInKbps;
  } catch (error) {
    console.error('Error measuring bandwidth:', error);
    // Return -1 to indicate measurement error
    return -1;
  }
};

/**
 * Uses the Network Information API if available
 * @returns {Object} Network connection information or null if not supported
 */
export const getNetworkInformation = () => {
  if ('connection' in navigator) {
    const connection = navigator.connection;
    return {
      effectiveType: connection.effectiveType, // 'slow-2g', '2g', '3g', or '4g'
      downlink: connection.downlink, // Mbps
      rtt: connection.rtt, // ms
      saveData: connection.saveData, // true if data saver is enabled
    };
  }
  return null;
};

/**
 * Checks if the user is on a low bandwidth connection
 * @returns {Promise<boolean>} True if low bandwidth detected
 */
export const isLowBandwidth = async () => {
  // First check if user has manually set low bandwidth mode
  const userSetting = localStorage.getItem(LOW_BANDWIDTH_SETTING_KEY);
  if (userSetting === 'true') {
    return true;
  }
  if (userSetting === 'false') {
    return false;
  }

  // Then check Network Information API if available
  const networkInfo = getNetworkInformation();
  if (networkInfo) {
    // Consider 'slow-2g' and '2g' as low bandwidth
    if (['slow-2g', '2g'].includes(networkInfo.effectiveType)) {
      return true;
    }
    // Consider Save Data mode as low bandwidth
    if (networkInfo.saveData) {
      return true;
    }
    // Consider very slow connections as low bandwidth
    if (networkInfo.downlink < 0.5) {
      // Less than 0.5 Mbps
      return true;
    }
  }

  // Finally, measure actual bandwidth
  const bandwidth = await measureBandwidth();
  return bandwidth > 0 && bandwidth < LOW_BANDWIDTH_THRESHOLD;
};

/**
 * Sets the bandwidth mode preference
 * @param {boolean} isLowBandwidth - Whether to enable low bandwidth mode
 */
export const setBandwidthMode = isLowBandwidth => {
  localStorage.setItem(LOW_BANDWIDTH_SETTING_KEY, isLowBandwidth.toString());
  // Also store the mode for quick access without async checks
  localStorage.setItem(BANDWIDTH_LOCAL_STORAGE_KEY, isLowBandwidth.toString());

  // Dispatch an event so other components can react
  window.dispatchEvent(
    new CustomEvent('bandwidthmodechange', {
      detail: { isLowBandwidth },
    })
  );
};

/**
 * React hook for using bandwidth detection in components
 * @param {Object} options - Configuration options
 * @returns {Object} Bandwidth state and control functions
 */
export const useBandwidthDetection = (options = {}) => {
  const { autoDetect = true, checkInterval = BANDWIDTH_CHECK_INTERVAL } = options;

  const [isLowBandwidthMode, setIsLowBandwidthMode] = useState(() => {
    // Initialize from localStorage if available
    const storedMode = localStorage.getItem(BANDWIDTH_LOCAL_STORAGE_KEY);
    return storedMode === 'true';
  });

  const [isDetecting, setIsDetecting] = useState(false);
  const [lastChecked, setLastChecked] = useState(null);

  // Function to detect and update bandwidth mode
  const detectBandwidth = async () => {
    setIsDetecting(true);
    try {
      const lowBandwidth = await isLowBandwidth();
      setIsLowBandwidthMode(lowBandwidth);
      localStorage.setItem(BANDWIDTH_LOCAL_STORAGE_KEY, lowBandwidth.toString());
      setLastChecked(new Date());
    } catch (error) {
      console.error('Error detecting bandwidth:', error);
    } finally {
      setIsDetecting(false);
    }
  };

  // Function to manually set bandwidth mode
  const setLowBandwidthMode = value => {
    setIsLowBandwidthMode(value);
    setBandwidthMode(value);
    setLastChecked(new Date());
  };

  // Auto-detect on mount and at intervals if enabled
  useEffect(() => {
    if (autoDetect) {
      detectBandwidth();

      const intervalId = setInterval(detectBandwidth, checkInterval);

      // Listen for online status changes to re-check
      const handleOnline = () => detectBandwidth();
      window.addEventListener('online', handleOnline);

      return () => {
        clearInterval(intervalId);
        window.removeEventListener('online', handleOnline);
      };
    }
  }, [autoDetect, checkInterval]);

  // Listen for bandwidth mode changes from other components
  useEffect(() => {
    const handleBandwidthModeChange = event => {
      setIsLowBandwidthMode(event.detail.isLowBandwidth);
    };

    window.addEventListener('bandwidthmodechange', handleBandwidthModeChange);

    return () => {
      window.removeEventListener('bandwidthmodechange', handleBandwidthModeChange);
    };
  }, []);

  return {
    isLowBandwidthMode,
    setLowBandwidthMode,
    detectBandwidth,
    isDetecting,
    lastChecked,
  };
};

// Helper function to get optimized image quality based on bandwidth
export const getOptimizedImageQuality = () => {
  const isLowBandwidth = localStorage.getItem(BANDWIDTH_LOCAL_STORAGE_KEY) === 'true';
  return isLowBandwidth ? 'low' : 'high';
};

// Helper function to get appropriate asset URL based on bandwidth
export const getOptimizedAssetUrl = (highQualityUrl, lowQualityUrl) => {
  const isLowBandwidth = localStorage.getItem(BANDWIDTH_LOCAL_STORAGE_KEY) === 'true';
  return isLowBandwidth ? lowQualityUrl : highQualityUrl;
};

export default {
  measureBandwidth,
  isLowBandwidth,
  setBandwidthMode,
  useBandwidthDetection,
  getOptimizedImageQuality,
  getOptimizedAssetUrl,
};
