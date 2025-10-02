/**
 * SmartProBono CourtListener API Route
 * Production-ready endpoint for case law search
 */

export default async function handler(req, res) {
  // Set CORS headers for production
  res.setHeader('Access-Control-Allow-Origin', 'https://smartprobono.org');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');
  
  // Handle preflight requests
  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  // Only allow GET requests
  if (req.method !== 'GET') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    const { search, jurisdiction = 'federal', page_size = 20, page = 1 } = req.query;

    // Validate required parameters
    if (!search) {
      return res.status(400).json({ 
        error: 'Search term is required',
        example: '/api/caselaw?search=probation violation'
      });
    }

    // Get API key from environment
    const apiKey = process.env.COURTLISTENER_API_KEY;
    if (!apiKey) {
      console.error('COURTLISTENER_API_KEY not set in production');
      return res.status(500).json({ 
        error: 'CourtListener API not configured',
        fallback: 'Please contact support'
      });
    }

    // Build CourtListener API URL (V4 for new users)
    const baseUrl = 'https://www.courtlistener.com/api/rest/v4/search/';
    const searchParams = new URLSearchParams({
      q: search,
      stat_Precedential: 'on',
      order_by: 'score desc',
      format: 'json',
      page: page.toString(),
      page_size: page_size.toString()
    });

    if (jurisdiction !== 'federal') {
      searchParams.append('court', jurisdiction);
    }

    const apiUrl = `${baseUrl}?${searchParams.toString()}`;

    // Make authenticated request to CourtListener
    const response = await fetch(apiUrl, {
      headers: {
        'Authorization': `Token ${apiKey}`,
        'User-Agent': 'SmartProBono/1.0 (Legal AI Assistant)',
        'Accept': 'application/json'
      },
      timeout: 10000 // 10 second timeout
    });

    if (!response.ok) {
      console.error(`CourtListener API error: ${response.status} ${response.statusText}`);
      return res.status(500).json({ 
        error: 'Failed to fetch case law data',
        details: `API returned ${response.status}`,
        fallback: 'Please try again or contact support'
      });
    }

    const data = await response.json();

    // Transform CourtListener data to SmartProBono format
    const transformedResults = data.results?.map(caseData => ({
      case_name: caseData.caseName || 'Unknown Case',
      court: caseData.court || 'Unknown Court',
      date_filed: caseData.dateFiled || null,
      date_decided: caseData.dateDecided || null,
      absolute_url: `https://www.courtlistener.com${caseData.absolute_url}`,
      citation: caseData.citation?.[0] || null,
      snippet: caseData.snippet || null,
      case_id: caseData.id || null
    })) || [];

    // Return structured response
    const result = {
      success: true,
      search_term: search,
      jurisdiction: jurisdiction,
      total_results: data.count || 0,
      page: parseInt(page),
      page_size: parseInt(page_size),
      has_more: !!data.next,
      results: transformedResults,
      search_metadata: {
        search_time: new Date().toISOString(),
        courtlistener_url: apiUrl,
        api_version: 'v4'
      }
    };

    // Log successful search for monitoring
    console.log(`✅ CourtListener search: "${search}" -> ${data.count} results`);

    return res.status(200).json(result);

  } catch (error) {
    console.error('CourtListener API error:', error);
    return res.status(500).json({ 
      error: 'Internal server error',
      details: error.message,
      fallback: 'Please try again or contact support'
    });
  }
}
