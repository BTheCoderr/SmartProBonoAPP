import ApiService from './ApiService';

/**
 * Service for handling paralegal-related operations
 * @class ParalegalService
 */
class ParalegalService {
  /**
   * Get AI-powered paralegal assistance
   * @param {string} query - User's legal question or request
   * @returns {Promise<Object>} Response containing AI-generated assistance
   */
  async getParalegalAssistance(query) {
    try {
      const response = await ApiService.post('/api/paralegal/assist', { 
        query,
        timestamp: new Date().toISOString()
      });
      return response.data;
    } catch (error) {
      console.error('Error getting paralegal assistance:', error);
      throw new Error('Failed to get paralegal assistance. Please try again later.');
    }
  }

  /**
   * Analyze a legal document
   * @param {Object} document - Legal document to analyze
   * @returns {Promise<Object>} Analysis results
   */
  async analyzeLegalDocument(document) {
    try {
      const response = await ApiService.post('/api/paralegal/analyze', { 
        document,
        timestamp: new Date().toISOString()
      });
      return response.data;
    } catch (error) {
      console.error('Error analyzing legal document:', error);
      throw new Error('Failed to analyze document. Please try again later.');
    }
  }

  /**
   * Generate a legal summary
   * @param {string} text - Text to summarize
   * @returns {Promise<Object>} Generated summary
   */
  async generateLegalSummary(text) {
    try {
      const response = await ApiService.post('/api/paralegal/summarize', { 
        text,
        timestamp: new Date().toISOString()
      });
      return response.data;
    } catch (error) {
      console.error('Error generating legal summary:', error);
      throw new Error('Failed to generate summary. Please try again later.');
    }
  }

  /**
   * Check service health status
   * @returns {Promise<Object>} Service status information
   */
  async checkServiceStatus() {
    try {
      const response = await ApiService.get('/api/paralegal/health');
      return response.data;
    } catch (error) {
      console.error('Error checking service status:', error);
      throw new Error('Service health check failed. Please try again later.');
    }
  }
}

// Export singleton instance
export default new ParalegalService(); 