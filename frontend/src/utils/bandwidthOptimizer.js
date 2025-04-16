/**
 * bandwidthOptimizer.js
 * Utility for optimizing application performance in low-bandwidth environments
 */

import { getOptimizedImageQuality } from './bandwidthDetection';

// Constants for optimization settings
const IMAGE_QUALITY = {
  high: 0.9,
  medium: 0.6,
  low: 0.4,
  ultraLow: 0.2,
};

const MAX_IMAGE_SIZES = {
  high: 1600,
  medium: 1200,
  low: 800,
  ultraLow: 400,
};

/**
 * Compresses an image file to reduce size based on bandwidth availability
 * @param {File} imageFile - The original image file
 * @param {string} quality - Image quality level ('high', 'medium', 'low', 'ultraLow')
 * @returns {Promise<Blob>} - Compressed image blob
 */
export const compressImage = async (imageFile, quality = null) => {
  // Use detected quality if not explicitly specified
  const qualityLevel = quality || getOptimizedImageQuality();
  const qualityFactor = IMAGE_QUALITY[qualityLevel];
  const maxSize = MAX_IMAGE_SIZES[qualityLevel];

  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.readAsDataURL(imageFile);

    reader.onload = event => {
      const img = new Image();
      img.src = event.target.result;

      img.onload = () => {
        // Determine if resizing is needed
        let width = img.width;
        let height = img.height;

        if (width > maxSize || height > maxSize) {
          if (width > height) {
            height = Math.round((height * maxSize) / width);
            width = maxSize;
          } else {
            width = Math.round((width * maxSize) / height);
            height = maxSize;
          }
        }

        // Create canvas for resizing and compression
        const canvas = document.createElement('canvas');
        canvas.width = width;
        canvas.height = height;

        const ctx = canvas.getContext('2d');
        ctx.drawImage(img, 0, 0, width, height);

        // Convert to blob with appropriate quality
        canvas.toBlob(blob => resolve(blob), imageFile.type || 'image/jpeg', qualityFactor);
      };

      img.onerror = () => reject(new Error('Failed to load image'));
    };

    reader.onerror = () => reject(new Error('Failed to read file'));
  });
};

/**
 * Formats optimized image URLs based on bandwidth availability
 * @param {string} url - Original image URL
 * @returns {string} - Optimized image URL with appropriate parameters
 */
export const getOptimizedImageUrl = url => {
  const qualityLevel = getOptimizedImageQuality();

  // Skip optimization for local files or null URLs
  if (!url || url.startsWith('blob:') || url.startsWith('data:')) {
    return url;
  }

  // Add width parameter based on quality level
  const width = MAX_IMAGE_SIZES[qualityLevel];

  // Check if URL already has query parameters
  const separator = url.includes('?') ? '&' : '?';

  // For CDN services that support width/quality parameters
  if (url.includes('cloudinary.com') || url.includes('imgix.net')) {
    return `${url}${separator}w=${width}&q=${IMAGE_QUALITY[qualityLevel] * 100}`;
  }

  // For custom image API
  if (url.includes('/api/images/')) {
    return `${url}${separator}width=${width}&quality=${qualityLevel}`;
  }

  // Fallback - just append width parameter
  return `${url}${separator}width=${width}`;
};

/**
 * Loads scripts dynamically and with proper prioritization based on bandwidth
 * @param {string} src - Script URL
 * @param {Object} options - Options for script loading
 * @returns {Promise} - Resolves when script is loaded
 */
export const loadOptimizedScript = (src, options = {}) => {
  const { async = true, defer = false, lowBandwidthSkip = false } = options;

  const qualityLevel = getOptimizedImageQuality();

  // Skip non-essential scripts in ultra-low bandwidth mode
  if (lowBandwidthSkip && qualityLevel === 'ultraLow') {
    return Promise.resolve();
  }

  return new Promise((resolve, reject) => {
    const script = document.createElement('script');
    script.src = src;
    script.async = async;
    script.defer = defer;

    script.onload = () => resolve();
    script.onerror = () => reject(new Error(`Failed to load script: ${src}`));

    document.body.appendChild(script);
  });
};

/**
 * Returns appropriate content elements based on bandwidth availability
 * @param {Object} contentOptions - Content options for different bandwidth levels
 * @returns {React.ReactNode} - Content component for current bandwidth level
 */
export const getOptimizedContent = contentOptions => {
  const qualityLevel = getOptimizedImageQuality();

  // Return specific content for bandwidth level, or fall back to higher quality
  return (
    contentOptions[qualityLevel] ||
    contentOptions.low ||
    contentOptions.medium ||
    contentOptions.high
  );
};

/**
 * Determines if a feature should be enabled based on bandwidth
 * @param {Object} feature - Feature configuration object
 * @returns {boolean} - Whether the feature should be enabled
 */
export const shouldEnableFeature = feature => {
  const qualityLevel = getOptimizedImageQuality();
  const { minimumQuality = 'ultraLow', disabledInLowBandwidth = false } = feature;

  const qualityRanking = {
    ultraLow: 1,
    low: 2,
    medium: 3,
    high: 4,
  };

  // Check for explicit disable in low bandwidth mode
  if (disabledInLowBandwidth && qualityLevel !== 'high') {
    return false;
  }

  // Check minimum quality requirement
  return qualityRanking[qualityLevel] >= qualityRanking[minimumQuality];
};

export default {
  compressImage,
  getOptimizedImageUrl,
  loadOptimizedScript,
  getOptimizedContent,
  shouldEnableFeature,
};
