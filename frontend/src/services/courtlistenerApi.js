/**
 * SmartProBono CourtListener API Service
 * Reusable service for case law search across components
 */

class CourtListenerApiService {
  constructor() {
    // Call Flask backend directly (not Next.js API)
    this.baseUrl = 'http://localhost:3001/api/courtlistener';
  }

  /**
   * Search case law using CourtListener API
   * @param {Object} params - Search parameters
   * @param {string} params.search - Search term
   * @param {string} params.jurisdiction - Court jurisdiction (default: 'federal')
   * @param {number} params.page_size - Number of results per page (default: 20)
   * @param {number} params.page - Page number (default: 1)
   * @returns {Promise<Object>} Search results
   */
  async searchCaseLaw(params) {
    try {
      const {
        search,
        jurisdiction = 'federal',
        page_size = 20,
        page = 1
      } = params;

      if (!search) {
        throw new Error('Search term is required');
      }

      console.log(`🔍 SmartProBono: Searching case law for "${search}"`);

      const searchParams = new URLSearchParams({
        q: search,  // Flask backend expects 'q' parameter
        jurisdiction,
        page_size: page_size.toString(),
        page: page.toString()
      });

      const response = await fetch(`${this.baseUrl}/search?${searchParams.toString()}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.error || `HTTP ${response.status}: ${response.statusText}`);
      }

      const data = await response.json();

      if (!data.success) {
        throw new Error(data.error || 'Search failed');
      }

      console.log(`📊 CourtListener: Found ${data.totalResults} cases`);
      return data;

    } catch (error) {
      console.error('❌ CourtListener API Error:', error);
      throw error;
    }
  }

  /**
   * Search for specific case types commonly used in SmartProBono
   */
  async searchProbationViolations(page_size = 10) {
    return this.searchCaseLaw({
      search: 'probation violation',
      page_size
    });
  }

  async searchLandlordTenant(page_size = 10) {
    return this.searchCaseLaw({
      search: 'landlord tenant',
      page_size
    });
  }

  async searchImmigrationBond(page_size = 10) {
    return this.searchCaseLaw({
      search: 'immigration bond',
      page_size
    });
  }

  /**
   * Get health status of CourtListener integration
   */
  async getHealth() {
    try {
      const response = await fetch('/api/courtlistener/health');
      return await response.json();
    } catch (error) {
      console.error('Health check failed:', error);
      return { success: false, error: error.message };
    }
  }
}

// Export singleton instance
export const courtlistenerApi = new CourtListenerApiService();

// Export class for testing
export { CourtListenerApiService };
