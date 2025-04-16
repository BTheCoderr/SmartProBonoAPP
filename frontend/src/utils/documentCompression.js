/**
 * documentCompression.js
 * Utility for compressing and optimizing legal documents
 * Especially useful for low-bandwidth environments
 */

import { getBandwidthLevel } from './bandwidthOptimizer';

// Constants for compression quality
const COMPRESSION_LEVELS = {
  HIGH: 0.2, // High compression, lower quality (20% of original)
  MEDIUM: 0.5, // Medium compression, decent quality (50% of original)
  LOW: 0.8, // Low compression, high quality (80% of original)
  NONE: 1.0, // No compression, original quality
};

// Document size thresholds in bytes
const SIZE_THRESHOLDS = {
  SMALL: 1024 * 500, // 500KB
  MEDIUM: 1024 * 1024, // 1MB
  LARGE: 1024 * 1024 * 5, // 5MB
};

// Document format types
const DOCUMENT_FORMATS = {
  TEXT: 'text',
  HTML: 'html',
  PDF: 'pdf',
  IMAGE: 'image',
  DOCX: 'docx',
};

/**
 * Determine appropriate compression level based on document size and bandwidth
 * @param {number} docSize - Document size in bytes
 * @param {string} format - Document format
 * @returns {number} - Compression level between 0-1
 */
export const getCompressionLevel = (docSize, format) => {
  const bandwidth = getBandwidthLevel();

  // For text-based documents, compression strategy differs
  if (format === DOCUMENT_FORMATS.TEXT || format === DOCUMENT_FORMATS.HTML) {
    if (bandwidth === 'low') {
      return docSize > SIZE_THRESHOLDS.MEDIUM ? COMPRESSION_LEVELS.HIGH : COMPRESSION_LEVELS.MEDIUM;
    } else {
      return docSize > SIZE_THRESHOLDS.LARGE ? COMPRESSION_LEVELS.MEDIUM : COMPRESSION_LEVELS.LOW;
    }
  }

  // For PDFs and images
  if (format === DOCUMENT_FORMATS.PDF || format === DOCUMENT_FORMATS.IMAGE) {
    if (bandwidth === 'low') {
      return COMPRESSION_LEVELS.HIGH;
    } else if (bandwidth === 'medium') {
      return COMPRESSION_LEVELS.MEDIUM;
    } else {
      return COMPRESSION_LEVELS.LOW;
    }
  }

  // Default fallback
  return bandwidth === 'low' ? COMPRESSION_LEVELS.MEDIUM : COMPRESSION_LEVELS.LOW;
};

/**
 * Segment a large document into smaller chunks for progressive loading
 * @param {string} content - Document content
 * @param {number} chunkSize - Size of each chunk in characters
 * @returns {Array} - Array of document chunks
 */
export const segmentDocument = (content, chunkSize = 5000) => {
  if (!content || typeof content !== 'string') {
    return [];
  }

  const chunks = [];
  let position = 0;

  while (position < content.length) {
    // Try to break at paragraph or sentence if possible instead of mid-sentence
    let endPos = Math.min(position + chunkSize, content.length);

    // If we're not at the end, try to find a paragraph break
    if (endPos < content.length) {
      const paragraphBreak = content.lastIndexOf('\n\n', endPos);
      if (paragraphBreak > position && paragraphBreak > endPos - 500) {
        endPos = paragraphBreak + 2; // Include the newline characters
      } else {
        // Try to break at a sentence
        const sentenceBreak = content.lastIndexOf('. ', endPos);
        if (sentenceBreak > position && sentenceBreak > endPos - 200) {
          endPos = sentenceBreak + 2; // Include the period and space
        }
      }
    }

    chunks.push(content.substring(position, endPos));
    position = endPos;
  }

  return chunks;
};

/**
 * Calculate estimated download time for a document
 * @param {number} sizeInBytes - Document size in bytes
 * @param {number} bandwidthKbps - Bandwidth in Kbps
 * @returns {number} - Estimated time in seconds
 */
export const calculateDownloadTime = (sizeInBytes, bandwidthKbps) => {
  // Convert kbps to bytes per second (divide by 8)
  const bytesPerSecond = (bandwidthKbps * 1024) / 8;
  return sizeInBytes / bytesPerSecond;
};

/**
 * Removes unnecessary elements from HTML documents to reduce size
 * @param {string} htmlContent - HTML document content
 * @param {boolean} isLowBandwidth - Whether in low bandwidth mode
 * @returns {string} - Optimized HTML content
 */
export const optimizeHtmlDocument = (htmlContent, isLowBandwidth = false) => {
  if (!htmlContent) return htmlContent;

  let optimized = htmlContent;

  // Remove comments
  optimized = optimized.replace(/<!--[\s\S]*?-->/g, '');

  // Remove excessive whitespace
  optimized = optimized.replace(/\s{2,}/g, ' ');

  if (isLowBandwidth) {
    // More aggressive optimization for low bandwidth

    // Remove style attributes
    optimized = optimized.replace(/\sstyle="[^"]*"/g, '');

    // Remove data attributes
    optimized = optimized.replace(/\sdata-[^=]*="[^"]*"/g, '');

    // Replace complex SVGs with placeholders (match SVG tags and their contents)
    optimized = optimized.replace(/<svg[\s\S]*?<\/svg>/g, '<span>[Image]</span>');
  }

  return optimized;
};

/**
 * Split a PDF document into individual pages for progressive loading
 * @param {ArrayBuffer} pdfData - PDF file data
 * @param {Function} onProgress - Progress callback
 * @returns {Promise<Array>} - Array of page data objects
 */
export const splitPdfIntoPages = async (pdfData, onProgress) => {
  // This is a placeholder - actual implementation would use a PDF library like pdf.js
  // which would need to be installed as a dependency
  return new Promise(resolve => {
    setTimeout(() => {
      // Simulate processing of a PDF
      const pages = [
        { pageNum: 1, content: 'Page 1 content...', size: 100000 },
        { pageNum: 2, content: 'Page 2 content...', size: 120000 },
        // ...more pages
      ];

      if (onProgress) {
        onProgress(1.0); // 100% complete
      }

      resolve(pages);
    }, 500);
  });
};

/**
 * Generate a text-only version of a document for the lowest bandwidth scenarios
 * @param {Object} document - Document object with content
 * @returns {string} - Plain text version of the document
 */
export const generateTextOnlyVersion = document => {
  if (!document) return '';

  // For HTML content, strip all HTML tags
  if (document.format === DOCUMENT_FORMATS.HTML) {
    return document.content
      .replace(/<[^>]*>/g, ' ')
      .replace(/\s{2,}/g, ' ')
      .trim();
  }

  // For structured document with sections
  if (document.sections && Array.isArray(document.sections)) {
    return document.sections
      .map(section => {
        if (section.type === 'heading') {
          return `\n\n${section.content.toUpperCase()}\n`;
        }
        return section.content;
      })
      .join('\n');
  }

  // Fallback for simple text
  return document.content || '';
};

/**
 * Compress document images to reduce size
 * @param {string} htmlContent - HTML content with images
 * @param {number} quality - Image quality (0-1)
 * @returns {Promise<string>} - HTML with compressed images
 */
export const compressDocumentImages = async (htmlContent, quality = COMPRESSION_LEVELS.MEDIUM) => {
  // This is a placeholder for a more complex implementation
  // A real implementation would parse the HTML, find images,
  // compress them using canvas, and replace URLs

  // Simulate image compression by adding a compression parameter to image URLs
  const compressed = htmlContent.replace(
    /<img\s+src="([^"]+)"/g,
    `<img src="$1?quality=${Math.round(quality * 100)}"`
  );

  return compressed;
};

/**
 * Create a compressed version of a document for offline use
 * @param {Object} document - Document object
 * @returns {Promise<Object>} - Compressed document
 */
export const createOfflineVersion = async document => {
  if (!document) return null;

  const bandwidth = getBandwidthLevel();
  const compressionLevel = getCompressionLevel(
    document.size || 0,
    document.format || DOCUMENT_FORMATS.TEXT
  );

  // Create a simplified version based on format
  let offlineContent = document.content;

  switch (document.format) {
    case DOCUMENT_FORMATS.HTML:
      offlineContent = optimizeHtmlDocument(document.content, bandwidth === 'low');
      offlineContent = await compressDocumentImages(offlineContent, compressionLevel);
      break;

    case DOCUMENT_FORMATS.TEXT:
      // Text is already compact, just segment if needed
      if (document.content && document.content.length > SIZE_THRESHOLDS.MEDIUM) {
        const chunks = segmentDocument(document.content);
        offlineContent = chunks.join('\n----------\n');
      }
      break;

    // Other format handling would go here

    default:
      // For unknown formats, use text-only version
      if (bandwidth === 'low') {
        offlineContent = generateTextOnlyVersion(document);
      }
  }

  return {
    ...document,
    offlineContent,
    compressionLevel,
    originalSize: document.size || document.content?.length || 0,
    compressedSize: offlineContent.length,
    lastCompressed: new Date().toISOString(),
  };
};

export default {
  COMPRESSION_LEVELS,
  DOCUMENT_FORMATS,
  getCompressionLevel,
  segmentDocument,
  optimizeHtmlDocument,
  generateTextOnlyVersion,
  compressDocumentImages,
  createOfflineVersion,
  calculateDownloadTime,
  splitPdfIntoPages,
};
