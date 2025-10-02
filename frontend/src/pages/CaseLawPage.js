import React from 'react';
import CourtListenerSearch from '../components/CourtListenerSearch';

const CaseLawPage = () => {
  return (
    <div className="case-law-page">
      <div className="page-header">
        <h1>🔍 Case Law Search</h1>
        <p>Search millions of court cases using CourtListener</p>
      </div>
      
      <CourtListenerSearch 
        showQuickSearches={true}
        maxResults={20}
      />
    </div>
  );
};

export default CaseLawPage;
