/**
 * legalResearchConnector.js
 * Utility for connecting to various legal research databases and APIs
 * Provides standardized interfaces for searching, retrieving, and working with legal research content
 */

import axios from 'axios';
import { logDataAccess, logSecurityEvent } from './auditLogger';
import { getBandwidthLevel } from './bandwidthOptimizer';

// Supported legal research providers
export const RESEARCH_PROVIDERS = {
  WESTLAW: 'westlaw',
  LEXIS: 'lexis_nexis',
  CASETEXT: 'casetext',
  GOOGLE_SCHOLAR: 'google_scholar',
  OPEN_ACCESS: 'open_access', // Free legal resources like CourtListener, etc.
  FASTCASE: 'fastcase',
  LAW_NET: 'law_net',
  BLOOMBERG_LAW: 'bloomberg_law',
  HW_WILSON: 'hw_wilson',
};

// Research content types
export const CONTENT_TYPES = {
  CASE_LAW: 'case_law',
  STATUTES: 'statutes',
  REGULATIONS: 'regulations',
  SECONDARY_SOURCES: 'secondary_sources',
  BRIEFS: 'briefs',
  JOURNALS: 'journals',
  FORMS: 'forms',
  TREATIES: 'treaties',
};

// Jurisdiction constants
export const JURISDICTIONS = {
  US_FEDERAL: 'us_federal',
  US_STATE: 'us_state',
  INTERNATIONAL: 'international',
};

// Search result sort options
export const SORT_OPTIONS = {
  RELEVANCE: 'relevance',
  DATE_DESC: 'date_desc',
  DATE_ASC: 'date_asc',
  COURT_HIERARCHY: 'court_hierarchy',
  CITATIONS: 'citations',
};

// Default API timeout (15 seconds)
const API_TIMEOUT = 15000;

// Maximum results per request
const MAX_RESULTS_PER_REQUEST = 50;

// API endpoint configuration
const API_ENDPOINTS = {
  [RESEARCH_PROVIDERS.WESTLAW]: '/api/research/westlaw',
  [RESEARCH_PROVIDERS.LEXIS]: '/api/research/lexis',
  [RESEARCH_PROVIDERS.CASETEXT]: '/api/research/casetext',
  [RESEARCH_PROVIDERS.GOOGLE_SCHOLAR]: '/api/research/google-scholar',
  [RESEARCH_PROVIDERS.OPEN_ACCESS]: '/api/research/open-access',
  [RESEARCH_PROVIDERS.FASTCASE]: '/api/research/fastcase',
  [RESEARCH_PROVIDERS.LAW_NET]: '/api/research/law-net',
  [RESEARCH_PROVIDERS.BLOOMBERG_LAW]: '/api/research/bloomberg',
  [RESEARCH_PROVIDERS.HW_WILSON]: '/api/research/hw-wilson',
};

/**
 * Creates a legal research client for a specified provider
 * @param {string} provider - Provider from RESEARCH_PROVIDERS
 * @param {Object} config - Configuration options
 * @returns {Object} - Research client with methods for interacting with the provider
 */
export const createResearchClient = (provider, config = {}) => {
  // Validate provider is supported
  if (!Object.values(RESEARCH_PROVIDERS).includes(provider)) {
    throw new Error(`Unsupported legal research provider: ${provider}`);
  }

  // Set up client configuration with defaults
  const clientConfig = {
    baseUrl: config.baseUrl || API_ENDPOINTS[provider],
    apiKey: config.apiKey || null,
    timeout: config.timeout || API_TIMEOUT,
    maxResultsPerRequest: config.maxResultsPerRequest || MAX_RESULTS_PER_REQUEST,
    defaultContentTypes: config.defaultContentTypes || [CONTENT_TYPES.CASE_LAW],
    defaultJurisdictions: config.defaultJurisdictions || [JURISDICTIONS.US_FEDERAL],
    defaultSort: config.defaultSort || SORT_OPTIONS.RELEVANCE,
  };

  // Create axios instance for this provider
  const apiClient = axios.create({
    baseURL: clientConfig.baseUrl,
    timeout: clientConfig.timeout,
    headers: {
      'Content-Type': 'application/json',
      Accept: 'application/json',
      ...(clientConfig.apiKey && { Authorization: `Bearer ${clientConfig.apiKey}` }),
      ...(config.headers || {}),
    },
  });

  // Standard methods for all providers
  return {
    /**
     * Search for legal content across the provider's database
     * @param {string} query - Search query text
     * @param {Object} options - Search options
     * @returns {Promise<Object>} - Search results
     */
    search: async (query, options = {}) => {
      try {
        const searchParams = {
          query,
          contentTypes: options.contentTypes || clientConfig.defaultContentTypes,
          jurisdictions: options.jurisdictions || clientConfig.defaultJurisdictions,
          dateRange: options.dateRange || null,
          courts: options.courts || null,
          judges: options.judges || null,
          limit: options.limit || clientConfig.maxResultsPerRequest,
          offset: options.offset || 0,
          sort: options.sort || clientConfig.defaultSort,
          filters: options.filters || null,
          includeSnippets: options.includeSnippets !== undefined ? options.includeSnippets : true,
          bandwidthLevel: getBandwidthLevel() || 'high',
        };

        // Optimize for low bandwidth if needed
        if (searchParams.bandwidthLevel === 'low') {
          searchParams.includeSnippets = false;
          searchParams.limit = Math.min(searchParams.limit, 20);
        }

        // Log the search attempt
        logDataAccess('legal_research_search', provider, {
          query,
          contentTypes: searchParams.contentTypes,
          jurisdictions: searchParams.jurisdictions,
        });

        // Make the API call
        const response = await apiClient.post('/search', searchParams);

        // Format results to standard structure
        return formatSearchResults(response.data, provider);
      } catch (error) {
        logSecurityEvent('api_error', 'legal_research', provider, { error: error.message });
        throw new Error(`Legal research search error (${provider}): ${error.message}`);
      }
    },

    /**
     * Retrieve a specific document by ID
     * @param {string} documentId - Document identifier
     * @param {Object} options - Retrieval options
     * @returns {Promise<Object>} - Document data
     */
    getDocument: async (documentId, options = {}) => {
      try {
        const retrievalParams = {
          documentId,
          format: options.format || 'html',
          includeCitations:
            options.includeCitations !== undefined ? options.includeCitations : true,
          includeMetadata: options.includeMetadata !== undefined ? options.includeMetadata : true,
          bandwidthLevel: getBandwidthLevel() || 'high',
        };

        // Log the document access
        logDataAccess('legal_research_document', documentId, {
          provider,
          format: retrievalParams.format,
        });

        // Make the API call
        const response = await apiClient.get(`/document/${documentId}`, {
          params: retrievalParams,
        });

        // Format document to standard structure
        return formatDocumentResult(response.data, provider);
      } catch (error) {
        logSecurityEvent('api_error', 'legal_research', documentId, {
          error: error.message,
          provider,
        });
        throw new Error(`Legal document retrieval error (${provider}): ${error.message}`);
      }
    },

    /**
     * Get citation analysis for a document
     * @param {string} citation - Citation string (e.g., "410 U.S. 113")
     * @param {Object} options - Analysis options
     * @returns {Promise<Object>} - Citation analysis data
     */
    getCitationAnalysis: async (citation, options = {}) => {
      try {
        const analysisParams = {
          citation,
          depth: options.depth || 1,
          includeNegative: options.includeNegative !== undefined ? options.includeNegative : true,
          includePositive: options.includePositive !== undefined ? options.includePositive : true,
          includeCiting: options.includeCiting !== undefined ? options.includeCiting : true,
          includeCited: options.includeCited !== undefined ? options.includeCited : true,
          limit: options.limit || 25,
        };

        // Log the citation analysis request
        logDataAccess('legal_citation_analysis', citation, {
          provider,
          depth: analysisParams.depth,
        });

        // Make the API call
        const response = await apiClient.get('/citation-analysis', {
          params: analysisParams,
        });

        return formatCitationAnalysis(response.data, provider);
      } catch (error) {
        logSecurityEvent('api_error', 'legal_citation_analysis', citation, {
          error: error.message,
          provider,
        });
        throw new Error(`Citation analysis error (${provider}): ${error.message}`);
      }
    },

    /**
     * Get related documents based on a source document
     * @param {string} documentId - Source document ID
     * @param {Object} options - Related document options
     * @returns {Promise<Object>} - Related documents
     */
    getRelatedDocuments: async (documentId, options = {}) => {
      try {
        const relatedParams = {
          documentId,
          contentTypes: options.contentTypes || clientConfig.defaultContentTypes,
          limit: options.limit || 10,
          minRelevanceScore: options.minRelevanceScore || 0.7,
        };

        // Log the related documents request
        logDataAccess('legal_related_documents', documentId, {
          provider,
          contentTypes: relatedParams.contentTypes,
        });

        // Make the API call
        const response = await apiClient.get(`/related/${documentId}`, {
          params: relatedParams,
        });

        return formatRelatedDocuments(response.data, provider);
      } catch (error) {
        logSecurityEvent('api_error', 'legal_related_documents', documentId, {
          error: error.message,
          provider,
        });
        throw new Error(`Related documents error (${provider}): ${error.message}`);
      }
    },

    /**
     * Save a document to user's research folder
     * @param {string} documentId - Document to save
     * @param {Object} options - Save options
     * @returns {Promise<Object>} - Save confirmation
     */
    saveDocument: async (documentId, options = {}) => {
      try {
        const saveParams = {
          documentId,
          folderId: options.folderId || 'default',
          notes: options.notes || '',
          labels: options.labels || [],
        };

        // Log the document save
        logDataAccess('legal_save_document', documentId, {
          provider,
          folderId: saveParams.folderId,
        });

        // Make the API call
        const response = await apiClient.post('/save-document', saveParams);

        return {
          success: response.data.success,
          documentId,
          folderId: saveParams.folderId,
          savedAt: new Date().toISOString(),
          provider,
        };
      } catch (error) {
        logSecurityEvent('api_error', 'legal_save_document', documentId, {
          error: error.message,
          provider,
        });
        throw new Error(`Document save error (${provider}): ${error.message}`);
      }
    },

    /**
     * Get account usage and limits information
     * @returns {Promise<Object>} - Account usage data
     */
    getAccountUsage: async () => {
      try {
        const response = await apiClient.get('/account/usage');

        return {
          provider,
          searchesUsed: response.data.searchesUsed,
          searchesLimit: response.data.searchesLimit,
          documentsViewed: response.data.documentsViewed,
          documentsLimit: response.data.documentsLimit,
          downloadsUsed: response.data.downloadsUsed,
          downloadsLimit: response.data.downloadsLimit,
          periodStart: response.data.periodStart,
          periodEnd: response.data.periodEnd,
          isUnlimited: response.data.isUnlimited || false,
        };
      } catch (error) {
        logSecurityEvent('api_error', 'legal_account_usage', provider, { error: error.message });
        throw new Error(`Account usage error (${provider}): ${error.message}`);
      }
    },

    // Return the provider and configuration for reference
    getConfig: () => ({ provider, ...clientConfig }),
  };
};

/**
 * Format search results into a standardized structure
 * @param {Object} data - Raw API response data
 * @param {string} provider - Research provider
 * @returns {Object} - Standardized search results
 */
const formatSearchResults = (data, provider) => {
  // Default structure for search results
  const formattedResults = {
    provider,
    query: data.query || '',
    totalResults: data.totalResults || 0,
    results: [],
    facets: data.facets || {},
    pagination: {
      offset: data.offset || 0,
      limit: data.limit || MAX_RESULTS_PER_REQUEST,
      hasMore: data.hasMore || false,
    },
  };

  // Map results from provider-specific format to standard format
  if (data.results && Array.isArray(data.results)) {
    formattedResults.results = data.results.map(result => ({
      id: result.id || result.documentId,
      title: result.title || result.name || 'Untitled Document',
      citation: result.citation || result.cite || null,
      contentType: result.contentType || result.type || CONTENT_TYPES.CASE_LAW,
      jurisdiction: result.jurisdiction || null,
      court: result.court || null,
      date: result.date || result.filingDate || result.publicationDate || null,
      snippet: result.snippet || result.excerpt || null,
      url: result.url || null,
      relevanceScore: result.relevanceScore || result.score || null,
      source: provider,
      meta: {
        judges: result.judges || result.judge || null,
        parties: result.parties || null,
        docketNumber: result.docketNumber || result.docket || null,
        ...result.meta,
      },
    }));
  }

  return formattedResults;
};

/**
 * Format document result into a standardized structure
 * @param {Object} data - Raw API response data
 * @param {string} provider - Research provider
 * @returns {Object} - Standardized document result
 */
const formatDocumentResult = (data, provider) => {
  return {
    id: data.id || data.documentId,
    title: data.title || data.name || 'Untitled Document',
    citation: data.citation || data.cite || null,
    contentType: data.contentType || data.type || CONTENT_TYPES.CASE_LAW,
    content: data.content || data.text || data.html || null,
    contentFormat: data.contentFormat || 'html',
    jurisdiction: data.jurisdiction || null,
    court: data.court || null,
    date: data.date || data.filingDate || data.publicationDate || null,
    url: data.url || null,
    provider,
    meta: {
      judges: data.judges || data.judge || null,
      parties: data.parties || null,
      docketNumber: data.docketNumber || data.docket || null,
      summary: data.summary || null,
      headnotes: data.headnotes || null,
      syllabus: data.syllabus || null,
      outcome: data.outcome || null,
      procedural_history: data.proceduralHistory || data.history || null,
      ...data.meta,
    },
    citations: {
      citing: data.citations?.citing || data.citingReferences || [],
      cited: data.citations?.cited || data.citedReferences || [],
    },
  };
};

/**
 * Format citation analysis into a standardized structure
 * @param {Object} data - Raw API response data
 * @param {string} provider - Research provider
 * @returns {Object} - Standardized citation analysis
 */
const formatCitationAnalysis = (data, provider) => {
  return {
    citation: data.citation,
    provider,
    document: data.document ? formatDocumentResult(data.document, provider) : null,
    citingDocuments: Array.isArray(data.citingDocuments)
      ? data.citingDocuments.map(doc => formatDocumentResult(doc, provider))
      : [],
    citedDocuments: Array.isArray(data.citedDocuments)
      ? data.citedDocuments.map(doc => formatDocumentResult(doc, provider))
      : [],
    treatment: {
      positive: data.treatment?.positive || data.positiveCount || 0,
      negative: data.treatment?.negative || data.negativeCount || 0,
      neutral: data.treatment?.neutral || data.neutralCount || 0,
      discussed: data.treatment?.discussed || data.discussedCount || 0,
    },
    visualData: data.visualData || null,
  };
};

/**
 * Format related documents into a standardized structure
 * @param {Object} data - Raw API response data
 * @param {string} provider - Research provider
 * @returns {Object} - Standardized related documents
 */
const formatRelatedDocuments = (data, provider) => {
  return {
    sourceDocumentId: data.sourceDocumentId || data.documentId,
    provider,
    totalRelated: data.totalRelated || data.total || 0,
    documents: Array.isArray(data.documents || data.results)
      ? (data.documents || data.results).map(doc => ({
          id: doc.id || doc.documentId,
          title: doc.title || doc.name || 'Untitled Document',
          citation: doc.citation || doc.cite || null,
          contentType: doc.contentType || doc.type || CONTENT_TYPES.CASE_LAW,
          relevanceScore: doc.relevanceScore || doc.score || null,
          relationshipType: doc.relationshipType || 'related',
          snippet: doc.snippet || doc.excerpt || null,
          date: doc.date || doc.filingDate || doc.publicationDate || null,
          court: doc.court || null,
          url: doc.url || null,
        }))
      : [],
  };
};

/**
 * Unified search across multiple providers
 * @param {string} query - Search query
 * @param {Array<string>} providers - Array of providers to search
 * @param {Object} options - Search options
 * @returns {Promise<Object>} - Combined search results
 */
export const multiProviderSearch = async (query, providers, options = {}) => {
  if (!providers || !Array.isArray(providers) || providers.length === 0) {
    throw new Error('Must specify at least one provider for multi-provider search');
  }

  const searchPromises = providers.map(provider => {
    try {
      const client = createResearchClient(provider);
      return client.search(query, options).catch(error => {
        console.error(`Error searching ${provider}:`, error);
        // Return empty results for this provider rather than failing the entire operation
        return {
          provider,
          query,
          totalResults: 0,
          results: [],
          error: error.message,
        };
      });
    } catch (error) {
      console.error(`Error creating client for ${provider}:`, error);
      return Promise.resolve({
        provider,
        query,
        totalResults: 0,
        results: [],
        error: error.message,
      });
    }
  });

  const results = await Promise.all(searchPromises);

  // Combine and deduplicate results
  const combinedResults = {
    query,
    totalResults: results.reduce((sum, result) => sum + (result.totalResults || 0), 0),
    providers: providers,
    providerResults: results.reduce((acc, result) => {
      acc[result.provider] = result;
      return acc;
    }, {}),
    // Merge and sort all results together
    results: results
      .flatMap(result => (result.results || []).map(r => ({ ...r, provider: result.provider })))
      .sort((a, b) => (b.relevanceScore || 0) - (a.relevanceScore || 0)),
    errors: results
      .filter(result => result.error)
      .reduce((acc, result) => {
        acc[result.provider] = result.error;
        return acc;
      }, {}),
  };

  return combinedResults;
};

/**
 * Generate proper citation for a legal document
 * @param {Object} document - Document to cite
 * @param {string} style - Citation style ('bluebook', 'apa', 'mla', etc.)
 * @returns {string} - Formatted citation
 */
export const generateCitation = (document, style = 'bluebook') => {
  if (!document) return '';

  // If document already has a citation, return it
  if (document.citation) return document.citation;

  // Basic citation generation based on document type and available information
  let citation = '';

  try {
    switch (document.contentType) {
      case CONTENT_TYPES.CASE_LAW:
        if (style === 'bluebook') {
          // Bluebook format for cases
          const parties = document.meta?.parties || document.title || 'Unknown Parties';
          const reporter = document.meta?.reporter || 'Unknown Reporter';
          const volume = document.meta?.volume || '';
          const page = document.meta?.page || '';
          const court = document.court || '';
          const year = document.date ? new Date(document.date).getFullYear() : '';

          citation = `${parties}, ${volume} ${reporter} ${page} (${court} ${year})`;
        } else {
          // Default format
          citation = `${document.title} (${document.court}, ${document.date})`;
        }
        break;

      case CONTENT_TYPES.STATUTES:
        if (style === 'bluebook') {
          // Bluebook format for statutes
          const title = document.meta?.title || '';
          const section = document.meta?.section || '';
          const code = document.meta?.code || '';
          const year = document.date ? new Date(document.date).getFullYear() : '';

          citation = `${title} ${section}, ${code} (${year})`;
        } else {
          // Default format
          citation = `${document.title} (${document.jurisdiction}, ${document.date})`;
        }
        break;

      default:
        // Generic citation for other document types
        citation = `${document.title} (${document.date})`;
    }
  } catch (error) {
    console.error('Error generating citation:', error);
    citation = document.title || 'Citation unavailable';
  }

  return citation;
};

/**
 * Access the legal research database to find similar cases to the given facts
 * @param {string} factPattern - Description of the legal situation
 * @param {Object} options - Search options
 * @returns {Promise<Object>} - Similar cases and relevant statutes
 */
export const findSimilarCases = async (factPattern, options = {}) => {
  const provider = options.provider || RESEARCH_PROVIDERS.OPEN_ACCESS;
  const client = createResearchClient(provider);

  try {
    // Extract key legal concepts from the fact pattern
    const searchParams = {
      query: factPattern,
      contentTypes: [CONTENT_TYPES.CASE_LAW],
      jurisdictions: options.jurisdictions || [JURISDICTIONS.US_FEDERAL, JURISDICTIONS.US_STATE],
      limit: options.limit || 5,
      includeSnippets: true,
    };

    const results = await client.search(factPattern, searchParams);

    // Enhance results with relevance explanations
    const enhancedResults = {
      ...results,
      results: results.results.map(result => ({
        ...result,
        relevanceExplanation: generateRelevanceExplanation(result, factPattern),
        keyConcepts: extractKeyConcepts(result),
      })),
    };

    return enhancedResults;
  } catch (error) {
    console.error('Error finding similar cases:', error);
    throw new Error(`Error finding similar cases: ${error.message}`);
  }
};

/**
 * Generate an explanation of why a case is relevant to the fact pattern
 * @param {Object} caseResult - Case search result
 * @param {string} factPattern - User's fact pattern
 * @returns {string} - Relevance explanation
 */
const generateRelevanceExplanation = (caseResult, factPattern) => {
  // This would ideally be implemented with a proper NLP or ML approach
  // For now, a simplified version that extracts from snippets
  if (!caseResult.snippet) {
    return 'This case appears to have similar legal issues.';
  }

  // Extract key phrases from the snippet
  const snippet = caseResult.snippet.toLowerCase();
  const facts = factPattern.toLowerCase();

  // Look for common legal terms that appear in both
  const legalTerms = [
    'negligence',
    'contract',
    'breach',
    'duty',
    'damages',
    'liability',
    'injury',
    'plaintiff',
    'defendant',
    'rights',
    'property',
    'criminal',
    'statute',
    'regulation',
    'violation',
  ];

  const commonTerms = legalTerms.filter(term => snippet.includes(term) && facts.includes(term));

  if (commonTerms.length > 0) {
    return `This case addresses similar legal concepts including: ${commonTerms.join(', ')}.`;
  }

  return 'This case has factual or legal similarities to your situation.';
};

/**
 * Extract key legal concepts from a case result
 * @param {Object} caseResult - Case search result
 * @returns {Array<string>} - Key legal concepts
 */
const extractKeyConcepts = caseResult => {
  // In a real implementation, this would use NLP to extract legal concepts
  // For now, return some placeholder concepts based on content
  const concepts = [];

  if (caseResult.snippet) {
    // Look for common legal phrases in the snippet
    const snippet = caseResult.snippet.toLowerCase();

    if (snippet.includes('negligence') || snippet.includes('duty of care')) {
      concepts.push('Negligence');
    }

    if (snippet.includes('contract') || snippet.includes('agreement')) {
      concepts.push('Contract Law');
    }

    if (snippet.includes('damages') || snippet.includes('compensation')) {
      concepts.push('Damages');
    }

    if (snippet.includes('property') || snippet.includes('ownership')) {
      concepts.push('Property Rights');
    }

    if (snippet.includes('constitutional') || snippet.includes('amendment')) {
      concepts.push('Constitutional Law');
    }
  }

  // Add some based on court and jurisdiction
  if (caseResult.court && caseResult.court.includes('Supreme')) {
    concepts.push('Supreme Court Precedent');
  }

  // If we couldn't extract any concepts, add a placeholder
  if (concepts.length === 0) {
    concepts.push('Case Precedent');
  }

  return concepts;
};

export default {
  RESEARCH_PROVIDERS,
  CONTENT_TYPES,
  JURISDICTIONS,
  SORT_OPTIONS,
  createResearchClient,
  multiProviderSearch,
  generateCitation,
  findSimilarCases,
};
