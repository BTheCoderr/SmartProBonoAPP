import React, { useState, useEffect } from 'react';
import { courtlistenerApi } from '../services/courtlistenerApi';

/**
 * SmartProBono CourtListener Search Component
 * Production-ready component for case law search
 */
const CourtListenerSearch = ({ 
  onCaseSelect = null, 
  showQuickSearches = true,
  maxResults = 10 
}) => {
  const [searchTerm, setSearchTerm] = useState('');
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [jurisdiction, setJurisdiction] = useState('federal');

  // Quick search presets for SmartProBono
  const quickSearches = [
    { label: 'Probation Violations', term: 'probation violation' },
    { label: 'Landlord Tenant', term: 'landlord tenant' },
    { label: 'Immigration Bond', term: 'immigration bond' },
    { label: 'Employment Discrimination', term: 'employment discrimination' },
    { label: 'Personal Injury', term: 'personal injury' }
  ];

  const handleSearch = async (term = searchTerm) => {
    if (!term.trim()) {
      setError('Please enter a search term');
      return;
    }

    setLoading(true);
    setError(null);
    setResults(null);

    try {
      const response = await courtlistenerApi.searchCaseLaw({
        search: term,
        jurisdiction,
        page_size: maxResults
      });

      setResults(response);
      console.log(`✅ Found ${response.total_results} cases for "${term}"`);
    } catch (err) {
      console.error('❌ Search failed:', err);
      setError(err.message || 'Search failed');
    } finally {
      setLoading(false);
    }
  };

  const handleQuickSearch = (term) => {
    setSearchTerm(term);
    handleSearch(term);
  };

  const handleCaseClick = (caseData) => {
    if (onCaseSelect) {
      onCaseSelect(caseData);
    } else {
      // Default: open in new tab
      window.open(caseData.absolute_url, '_blank', 'noopener,noreferrer');
    }
  };

  return (
    <div className="courtlistener-search">
      <div className="search-header">
        <h2>🔍 Case Law Search</h2>
        <p>Search millions of court cases using CourtListener</p>
      </div>

      {/* Search Form */}
      <div className="search-form">
        <div className="search-input-group">
          <input
            type="text"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            placeholder="Enter search term (e.g., 'probation violation')"
            className="search-input"
            onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
          />
          <select
            value={jurisdiction}
            onChange={(e) => setJurisdiction(e.target.value)}
            className="jurisdiction-select"
          >
            <option value="federal">Federal Courts</option>
            <option value="state">State Courts</option>
            <option value="all">All Courts</option>
          </select>
          <button
            onClick={() => handleSearch()}
            disabled={loading}
            className="search-button"
          >
            {loading ? 'Searching...' : 'Search'}
          </button>
        </div>

        {/* Quick Searches */}
        {showQuickSearches && (
          <div className="quick-searches">
            <p>Quick searches:</p>
            <div className="quick-search-buttons">
              {quickSearches.map((search, index) => (
                <button
                  key={index}
                  onClick={() => handleQuickSearch(search.term)}
                  className="quick-search-button"
                  disabled={loading}
                >
                  {search.label}
                </button>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Error Display */}
      {error && (
        <div className="error-message">
          ❌ {error}
        </div>
      )}

      {/* Results Display */}
      {results && (
        <div className="search-results">
          <div className="results-header">
            <h3>📊 Search Results</h3>
            <p>
              Found <strong>{results.total_results.toLocaleString()}</strong> cases for "{results.search_term}"
              {results.has_more && ' (showing first ' + maxResults + ')'}
            </p>
          </div>

          <div className="cases-list">
            {results.results.map((caseData, index) => (
              <div key={caseData.case_id || index} className="case-item">
                <div className="case-header">
                  <h4 className="case-title">{caseData.case_name}</h4>
                  <div className="case-meta">
                    <span className="court">{caseData.court}</span>
                    {caseData.date_filed && (
                      <span className="date">Filed: {new Date(caseData.date_filed).toLocaleDateString()}</span>
                    )}
                  </div>
                </div>
                
                {caseData.snippet && (
                  <div className="case-snippet">
                    {caseData.snippet}
                  </div>
                )}

                <div className="case-actions">
                  <button
                    onClick={() => handleCaseClick(caseData)}
                    className="view-case-button"
                  >
                    🔗 View on CourtListener
                  </button>
                  {caseData.citation && (
                    <span className="citation">{caseData.citation}</span>
                  )}
                </div>
              </div>
            ))}
          </div>

          {results.has_more && (
            <div className="load-more">
              <p>Showing first {maxResults} of {results.total_results.toLocaleString()} results</p>
              <button
                onClick={() => handleSearch(searchTerm)}
                className="load-more-button"
              >
                Load More Results
              </button>
            </div>
          )}
        </div>
      )}

      {/* CSS Styles */}
      <style jsx>{`
        .courtlistener-search {
          max-width: 800px;
          margin: 0 auto;
          padding: 20px;
          font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        }

        .search-header h2 {
          color: #2c3e50;
          margin-bottom: 8px;
        }

        .search-header p {
          color: #7f8c8d;
          margin-bottom: 24px;
        }

        .search-input-group {
          display: flex;
          gap: 12px;
          margin-bottom: 16px;
        }

        .search-input {
          flex: 1;
          padding: 12px;
          border: 2px solid #e1e8ed;
          border-radius: 8px;
          font-size: 16px;
        }

        .search-input:focus {
          outline: none;
          border-color: #3498db;
        }

        .jurisdiction-select {
          padding: 12px;
          border: 2px solid #e1e8ed;
          border-radius: 8px;
          background: white;
        }

        .search-button {
          padding: 12px 24px;
          background: #3498db;
          color: white;
          border: none;
          border-radius: 8px;
          font-size: 16px;
          cursor: pointer;
          transition: background 0.2s;
        }

        .search-button:hover:not(:disabled) {
          background: #2980b9;
        }

        .search-button:disabled {
          background: #bdc3c7;
          cursor: not-allowed;
        }

        .quick-searches {
          margin-bottom: 24px;
        }

        .quick-searches p {
          margin-bottom: 8px;
          color: #7f8c8d;
          font-size: 14px;
        }

        .quick-search-buttons {
          display: flex;
          flex-wrap: wrap;
          gap: 8px;
        }

        .quick-search-button {
          padding: 8px 16px;
          background: #ecf0f1;
          color: #2c3e50;
          border: 1px solid #bdc3c7;
          border-radius: 6px;
          font-size: 14px;
          cursor: pointer;
          transition: all 0.2s;
        }

        .quick-search-button:hover:not(:disabled) {
          background: #d5dbdb;
          border-color: #95a5a6;
        }

        .quick-search-button:disabled {
          opacity: 0.6;
          cursor: not-allowed;
        }

        .error-message {
          padding: 12px;
          background: #f8d7da;
          color: #721c24;
          border: 1px solid #f5c6cb;
          border-radius: 6px;
          margin-bottom: 20px;
        }

        .results-header h3 {
          color: #2c3e50;
          margin-bottom: 8px;
        }

        .results-header p {
          color: #7f8c8d;
          margin-bottom: 20px;
        }

        .case-item {
          border: 1px solid #e1e8ed;
          border-radius: 8px;
          padding: 16px;
          margin-bottom: 16px;
          background: white;
          transition: box-shadow 0.2s;
        }

        .case-item:hover {
          box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }

        .case-title {
          color: #2c3e50;
          margin: 0 0 8px 0;
          font-size: 18px;
          line-height: 1.3;
        }

        .case-meta {
          display: flex;
          gap: 16px;
          margin-bottom: 12px;
          font-size: 14px;
          color: #7f8c8d;
        }

        .case-snippet {
          margin-bottom: 12px;
          color: #34495e;
          line-height: 1.5;
          font-size: 14px;
        }

        .case-actions {
          display: flex;
          justify-content: space-between;
          align-items: center;
        }

        .view-case-button {
          padding: 8px 16px;
          background: #27ae60;
          color: white;
          border: none;
          border-radius: 6px;
          font-size: 14px;
          cursor: pointer;
          transition: background 0.2s;
        }

        .view-case-button:hover {
          background: #229954;
        }

        .citation {
          font-size: 12px;
          color: #7f8c8d;
          font-style: italic;
        }

        .load-more {
          text-align: center;
          margin-top: 24px;
          padding: 20px;
          background: #f8f9fa;
          border-radius: 8px;
        }

        .load-more p {
          margin-bottom: 12px;
          color: #7f8c8d;
        }

        .load-more-button {
          padding: 12px 24px;
          background: #3498db;
          color: white;
          border: none;
          border-radius: 6px;
          font-size: 16px;
          cursor: pointer;
          transition: background 0.2s;
        }

        .load-more-button:hover {
          background: #2980b9;
        }
      `}</style>
    </div>
  );
};

export default CourtListenerSearch;
