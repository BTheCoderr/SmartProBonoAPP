import React, { useState } from 'react';
import { courtlistenerApi } from '../services/api';

/**
 * CourtListener Integration Test Component
 * Demonstrates the complete flow: Frontend → Backend → CourtListener → AI → User
 */
const CourtListenerTest = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSearch = async () => {
    if (!searchTerm.trim()) {
      setError('Please enter a search term');
      return;
    }

    setLoading(true);
    setError(null);
    setResults(null);

    try {
      console.log(`🔍 Frontend: Searching for "${searchTerm}"`);
      
      const response = await courtlistenerApi.searchCaseLaw({
        q: searchTerm,
        jurisdiction: 'federal',
        page_size: 5
      });

      console.log(`📊 Frontend: Received ${response.totalResults} results`);
      setResults(response);
    } catch (err) {
      console.error('❌ Frontend: Search failed:', err);
      setError(err.message || 'Search failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: '20px', maxWidth: '800px', margin: '0 auto' }}>
      <h2>🧪 CourtListener Integration Test</h2>
      <p>Test the complete flow: Frontend → Backend → CourtListener → AI → User</p>
      
      <div style={{ marginBottom: '20px' }}>
        <input
          type="text"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          placeholder="Enter search term (e.g., 'employment discrimination')"
          style={{
            padding: '10px',
            marginRight: '10px',
            width: '300px',
            border: '1px solid #ccc',
            borderRadius: '4px'
          }}
        />
        <button
          onClick={handleSearch}
          disabled={loading}
          style={{
            padding: '10px 20px',
            backgroundColor: loading ? '#ccc' : '#007bff',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: loading ? 'not-allowed' : 'pointer'
          }}
        >
          {loading ? 'Searching...' : 'Search Case Law'}
        </button>
      </div>

      {error && (
        <div style={{ 
          padding: '10px', 
          backgroundColor: '#f8d7da', 
          color: '#721c24', 
          border: '1px solid #f5c6cb',
          borderRadius: '4px',
          marginBottom: '20px'
        }}>
          ❌ Error: {error}
        </div>
      )}

      {results && (
        <div>
          <h3>📊 Search Results</h3>
          <div style={{ 
            padding: '10px', 
            backgroundColor: '#d4edda', 
            color: '#155724', 
            border: '1px solid #c3e6cb',
            borderRadius: '4px',
            marginBottom: '20px'
          }}>
            ✅ Found {results.totalResults} cases for "{results.searchTerm}"
            <br />
            ⏱️ AI Processing Time: {results.data.searchMetadata.aiProcessingTime}
            <br />
            🤖 AI Confidence: {results.data.aiSummaries.aiConfidence}
          </div>

          <h4>🤖 AI-Enhanced Summaries</h4>
          {results.data.aiSummaries.summaries.map((caseData, index) => (
            <div key={caseData.caseId} style={{
              border: '1px solid #ddd',
              borderRadius: '8px',
              padding: '15px',
              marginBottom: '15px',
              backgroundColor: '#f9f9f9'
            }}>
              <h5 style={{ margin: '0 0 10px 0', color: '#333' }}>
                {caseData.caseName}
              </h5>
              <p style={{ margin: '5px 0', fontSize: '14px', color: '#666' }}>
                <strong>Court:</strong> {caseData.court} | 
                <strong> Decided:</strong> {caseData.dateDecided}
              </p>
              
              <div style={{ marginTop: '10px' }}>
                <h6 style={{ margin: '0 0 5px 0', color: '#555' }}>Key Points:</h6>
                <p style={{ margin: '0 0 10px 0', fontSize: '14px' }}>
                  {caseData.aiSummary.keyPoints}
                </p>
                
                <h6 style={{ margin: '0 0 5px 0', color: '#555' }}>Legal Principles:</h6>
                <p style={{ margin: '0 0 10px 0', fontSize: '14px' }}>
                  {Array.isArray(caseData.aiSummary.legalPrinciples) 
                    ? caseData.aiSummary.legalPrinciples.join(', ')
                    : caseData.aiSummary.legalPrinciples
                  }
                </p>
                
                <a 
                  href={caseData.absolute_url} 
                  target="_blank" 
                  rel="noopener noreferrer"
                  style={{ color: '#007bff', textDecoration: 'none' }}
                >
                  🔗 View Full Case
                </a>
              </div>
            </div>
          ))}

          <h4>📋 Raw CourtListener Data</h4>
          <details style={{ marginTop: '10px' }}>
            <summary style={{ cursor: 'pointer', fontWeight: 'bold' }}>
              Click to view raw data (for debugging)
            </summary>
            <pre style={{ 
              backgroundColor: '#f8f9fa', 
              padding: '10px', 
              borderRadius: '4px',
              overflow: 'auto',
              fontSize: '12px'
            }}>
              {JSON.stringify(results, null, 2)}
            </pre>
          </details>
        </div>
      )}

      <div style={{ 
        marginTop: '30px', 
        padding: '15px', 
        backgroundColor: '#e7f3ff', 
        border: '1px solid #b3d9ff',
        borderRadius: '4px'
      }}>
        <h4>🔄 Complete Flow Tested:</h4>
        <ol style={{ margin: '10px 0', paddingLeft: '20px' }}>
          <li><strong>Frontend:</strong> React component calls courtlistenerApi.searchCaseLaw()</li>
          <li><strong>Backend:</strong> Flask receives request at /api/courtlistener/search</li>
          <li><strong>CourtListener:</strong> Backend queries CourtListener API (or uses mock data)</li>
          <li><strong>AI Summarizer:</strong> Backend sends cases to AI for summarization</li>
          <li><strong>User:</strong> Frontend displays AI-enhanced case summaries</li>
        </ol>
        <p style={{ margin: '10px 0 0 0', fontSize: '14px', color: '#666' }}>
          <strong>Phase 1 MVP:</strong> REST API integration with AI enhancement ✅
        </p>
      </div>
    </div>
  );
};

export default CourtListenerTest;
