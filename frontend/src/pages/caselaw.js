import React from 'react';
import Head from 'next/head';
import CourtListenerSearch from '../components/CourtListenerSearch';

const CaseLawPage = () => {
  return (
    <>
      <Head>
        <title>Case Law Search - SmartProBono</title>
        <meta name="description" content="Search millions of court cases using CourtListener" />
      </Head>
      
      <div className="container">
        <CourtListenerSearch 
          showQuickSearches={true}
          maxResults={20}
        />
      </div>
    </>
  );
};

export default CaseLawPage;
