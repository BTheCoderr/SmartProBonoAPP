/**
 * SmartProBono CourtListener Integration Test
 * Tests the complete flow: Frontend → Backend → CourtListener API
 */

const testCourtListenerIntegration = async () => {
  console.log('🧪 Testing SmartProBono CourtListener Integration...\n');

  // Test 1: Backend Health Check
  console.log('1️⃣ Testing Backend Health...');
  try {
    const healthResponse = await fetch('http://localhost:3001/api/courtlistener/health');
    const healthData = await healthResponse.json();
    console.log('✅ Backend Health:', healthData.message);
  } catch (error) {
    console.log('❌ Backend Health Failed:', error.message);
    return;
  }

  // Test 2: Search Functionality
  console.log('\n2️⃣ Testing Case Law Search...');
  const searchTerms = [
    'probation violation',
    'landlord tenant',
    'immigration bond'
  ];

  for (const term of searchTerms) {
    try {
      console.log(`\n🔍 Searching for: "${term}"`);
      const searchResponse = await fetch(`http://localhost:3001/api/courtlistener/search?q=${encodeURIComponent(term)}&page_size=2`);
      const searchData = await searchResponse.json();
      
      if (searchData.success) {
        console.log(`✅ Found ${searchData.totalResults.toLocaleString()} cases`);
        console.log(`📄 Sample case: ${searchData.data.rawResults[0]?.caseName || 'N/A'}`);
      } else {
        console.log(`❌ Search failed: ${searchData.error}`);
      }
    } catch (error) {
      console.log(`❌ Search error for "${term}":`, error.message);
    }
  }

  // Test 3: Frontend Integration (if React is running)
  console.log('\n3️⃣ Testing Frontend Integration...');
  try {
    const frontendResponse = await fetch('http://localhost:3000');
    if (frontendResponse.ok) {
      console.log('✅ React Frontend is running on port 3000');
      console.log('🌐 You can now test the integration at:');
      console.log('   - Main Navigation: http://localhost:3000/caselaw');
      console.log('   - Lawyer Dashboard: http://localhost:3000/lawyer-dashboard (Case Law Research tab)');
    } else {
      console.log('⚠️ React Frontend not responding on port 3000');
      console.log('💡 To start the frontend, run: cd frontend && npm start');
    }
  } catch (error) {
    console.log('⚠️ React Frontend not running');
    console.log('💡 To start the frontend, run: cd frontend && npm start');
  }

  console.log('\n🎉 CourtListener Integration Test Complete!');
  console.log('\n📋 Next Steps:');
  console.log('1. Start React frontend: cd frontend && npm start');
  console.log('2. Visit http://localhost:3000/caselaw');
  console.log('3. Search for cases and test the integration');
  console.log('4. Check Lawyer Dashboard for Case Law Research tab');
};

// Run the test
testCourtListenerIntegration().catch(console.error);
