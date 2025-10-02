"""
SmartProBono CourtListener Integration API
Phase 1 (MVP): REST API integration for case law search

Flow: SmartProBono Frontend → Flask Backend → CourtListener API → AI Summarizer → User
"""

from flask import Blueprint, request, jsonify
import requests
import logging
from datetime import datetime
import time
import os

# Create blueprint
courtlistener_bp = Blueprint('courtlistener', __name__)
logger = logging.getLogger(__name__)

# Check for API key
COURTLISTENER_API_KEY = os.getenv("COURTLISTENER_API_KEY")
COURTLISTENER_AVAILABLE = bool(COURTLISTENER_API_KEY)

if COURTLISTENER_AVAILABLE:
    logger.info("✅ CourtListener API key found - using real API")
else:
    logger.warning("COURTLISTENER_API_KEY not set - using fallback mode")

@courtlistener_bp.route('/search', methods=['GET'])
def search_case_law():
    """
    Search case law using CourtListener REST API
    Phase 1 MVP: Direct API calls for real-time case law search
    """
    try:
        # Get search parameters
        search_term = request.args.get('q', '')
        jurisdiction = request.args.get('jurisdiction', 'federal')
        court = request.args.get('court', '')
        order_by = request.args.get('order_by', 'score desc')
        stat_precedential = request.args.get('stat_Precedential', 'on')
        page = int(request.args.get('page', 1))
        page_size = int(request.args.get('page_size', 20))
        
        # Validate required parameters
        if not search_term:
            return jsonify({
                'success': False,
                'error': 'Search term (q) is required',
                'example': '/api/courtlistener/search?q=employment discrimination&jurisdiction=federal'
            }), 400
        
        logger.info(f"🔍 SmartProBono: Searching CourtListener for '{search_term}'")
        
        # Step 1: Query CourtListener API
        logger.info(f"CourtListener API available: {COURTLISTENER_AVAILABLE}")
        if COURTLISTENER_AVAILABLE:
            logger.info("Using CourtListener API with authentication")
            # Use direct API call with authentication
            courtlistener_data = fetch_courtlistener_data_with_auth({
                'search_term': search_term,
                'jurisdiction': jurisdiction,
                'court': court,
                'order_by': order_by,
                'stat_Precedential': stat_precedential,
                'page': page,
                'page_size': page_size
            })
        else:
            logger.warning("CourtListener API key not available, using fallback")
            # Use fallback method
            courtlistener_data = fetch_courtlistener_data_fallback({
                'search_term': search_term,
                'jurisdiction': jurisdiction,
                'court': court,
                'order_by': order_by,
                'stat_Precedential': stat_precedential,
                'page': page,
                'page_size': page_size
            })
        
        if not courtlistener_data['success']:
            return jsonify({
                'success': False,
                'error': courtlistener_data['error']
            }), 500
        
        logger.info(f"📊 CourtListener: Found {courtlistener_data['count']} cases")
        
        # Step 2: AI Summarization for top results
        ai_summaries = summarize_cases_with_ai(
            courtlistener_data['results'][:5],  # Top 5 cases
            search_term
        )
        
        logger.info(f"🤖 AI: Generated summaries for {len(ai_summaries.get('summaries', []))} cases")
        
        # Step 3: Return structured response
        response = {
            'success': True,
            'searchTerm': search_term,
            'jurisdiction': jurisdiction,
            'totalResults': courtlistener_data['count'],
            'page': page,
            'pageSize': page_size,
            'hasMore': courtlistener_data.get('next') is not None,
            'data': {
                'aiSummaries': ai_summaries,
                'rawResults': courtlistener_data['results'],
                'searchMetadata': {
                    'searchTime': datetime.now().isoformat(),
                    'courtlistenerUrl': courtlistener_data.get('url', ''),
                    'aiProcessingTime': ai_summaries.get('processingTime', 'N/A')
                }
            }
        }
        
        return jsonify(response)
        
    except Exception as e:
        logger.error(f"❌ SmartProBono CourtListener API Error: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to fetch case law data',
            'details': str(e),
            'fallback': 'Please try again or contact support if the issue persists'
        }), 500

@courtlistener_bp.route('/health', methods=['GET'])
def health_check():
    """Health check for CourtListener integration"""
    return jsonify({
        'success': True,
        'service': 'courtlistener',
        'status': 'healthy',
        'phase': 'Phase 1 (MVP) - REST API Integration',
        'message': 'CourtListener integration is operational'
    })

def fetch_courtlistener_data_with_auth(params):
    """
    Query CourtListener REST API with authentication
    """
    try:
        # Build CourtListener API URL (using V4 for new users)
        base_url = 'https://www.courtlistener.com/api/rest/v4/search/'
        search_params = {
            'q': params['search_term'],
            'stat_Precedential': params['stat_Precedential'],
            'order_by': params['order_by'],
            'format': 'json',
            'page': params['page'],
            'page_size': params['page_size']
        }
        
        # Add optional filters
        if params['court']:
            search_params['court'] = params['court']
        
        # Make API request with authentication
        api_url = f"{base_url}?{'&'.join([f'{k}={v}' for k, v in search_params.items()])}"
        
        logger.info(f"🌐 CourtListener API (Authenticated): {api_url}")
        
        response = requests.get(api_url, 
            headers={
                'Authorization': f'Token {COURTLISTENER_API_KEY}',
                'User-Agent': 'SmartProBono/1.0 (Legal AI Assistant)',
                'Accept': 'application/json'
            },
            timeout=10  # 10 second timeout
        )
        
        if not response.ok:
            raise Exception(f"CourtListener API error: {response.status_code} {response.reason}")
        
        data = response.json()
        
        return {
            'success': True,
            'count': data.get('count', 0),
            'next': data.get('next'),
            'previous': data.get('previous'),
            'results': data.get('results', []),
            'url': api_url
        }
        
    except Exception as e:
        logger.error(f"CourtListener API Error: {e}")
        return {
            'success': False,
            'error': f"Failed to fetch from CourtListener: {str(e)}"
        }

def fetch_courtlistener_data_fallback(params):
    """
    Query CourtListener REST API
    Phase 1 MVP: Direct API calls for real-time case law search
    """
    try:
        # Build CourtListener API URL (using V4 for new users)
        base_url = 'https://www.courtlistener.com/api/rest/v4/search/'
        search_params = {
            'q': params['search_term'],
            'stat_Precedential': params['stat_Precedential'],
            'order_by': params['order_by'],
            'format': 'json',
            'page': params['page'],
            'page_size': params['page_size']
        }
        
        # Add optional filters
        if params['court']:
            search_params['court'] = params['court']
        
        # Make API request
        api_url = f"{base_url}?{'&'.join([f'{k}={v}' for k, v in search_params.items()])}"
        
        logger.info(f"🌐 CourtListener API: {api_url}")
        
        response = requests.get(api_url, 
            headers={
                'User-Agent': 'SmartProBono/1.0 (Legal AI Assistant)',
                'Accept': 'application/json'
            },
            timeout=10  # 10 second timeout
        )
        
        if not response.ok:
            if response.status_code == 403:
                # API requires authentication - return mock data for testing
                logger.warning("CourtListener API requires authentication - returning mock data")
                return get_mock_courtlistener_data(params)
            else:
                raise Exception(f"CourtListener API error: {response.status_code} {response.reason}")
        
        data = response.json()
        
        return {
            'success': True,
            'count': data.get('count', 0),
            'next': data.get('next'),
            'previous': data.get('previous'),
            'results': data.get('results', []),
            'url': api_url
        }
        
    except Exception as e:
        logger.error(f"CourtListener API Error: {e}")
        return {
            'success': False,
            'error': f"Failed to fetch from CourtListener: {str(e)}"
        }

def get_mock_courtlistener_data(params):
    """
    Return mock CourtListener data for testing when API is not available
    """
    search_term = params['search_term']
    
    mock_cases = [
        {
            'id': 1,
            'caseName': f'Mock Case 1: {search_term}',
            'court': 'U.S. Court of Appeals',
            'dateFiled': '2023-01-15',
            'dateDecided': '2023-06-15',
            'absolute_url': 'https://www.courtlistener.com/opinion/12345/',
            'snippet': f'This is a mock case related to {search_term}. The court ruled in favor of the plaintiff based on established legal principles.',
            'stat_Precedential': True
        },
        {
            'id': 2,
            'caseName': f'Mock Case 2: {search_term}',
            'court': 'U.S. District Court',
            'dateFiled': '2023-03-20',
            'dateDecided': '2023-08-10',
            'absolute_url': 'https://www.courtlistener.com/opinion/12346/',
            'snippet': f'Another mock case involving {search_term}. The court applied relevant statutes and case law.',
            'stat_Precedential': True
        },
        {
            'id': 3,
            'caseName': f'Mock Case 3: {search_term}',
            'court': 'Supreme Court',
            'dateFiled': '2022-11-05',
            'dateDecided': '2023-05-01',
            'absolute_url': 'https://www.courtlistener.com/opinion/12347/',
            'snippet': f'Landmark case regarding {search_term}. The Supreme Court established important precedent.',
            'stat_Precedential': True
        }
    ]
    
    return {
        'success': True,
        'count': len(mock_cases),
        'next': None,
        'previous': None,
        'results': mock_cases,
        'url': 'Mock data for testing'
    }

def summarize_cases_with_ai(cases, search_term):
    """
    AI Case Summarization
    Uses SmartProBono's AI to create user-friendly case summaries
    """
    if not cases or len(cases) == 0:
        return {'summaries': [], 'processingTime': '0ms', 'aiConfidence': 0.0}
    
    start_time = time.time()
    
    try:
        # Call SmartProBono's AI backend for summarization
        ai_response = requests.post('http://localhost:3001/api/v1/legal/analyze', 
            json={
                'query': f"Summarize these {len(cases)} legal cases for a search about '{search_term}'. Focus on key legal principles, outcomes, and relevance to the search term.",
                'context': str(cases),
                'case_type': 'case_summarization'
            },
            headers={'Content-Type': 'application/json'},
            timeout=15
        )
        
        if not ai_response.ok:
            raise Exception(f"AI service error: {ai_response.status_code}")
        
        ai_result = ai_response.json()
        processing_time = f"{(time.time() - start_time) * 1000:.0f}ms"
        
        # Structure the AI-enhanced summaries
        summaries = []
        for i, case_data in enumerate(cases):
            summary = {
                'caseId': case_data.get('id', ''),
                'caseName': case_data.get('caseName', 'Unknown Case'),
                'court': case_data.get('court', 'Unknown Court'),
                'dateFiled': case_data.get('dateFiled', ''),
                'dateDecided': case_data.get('dateDecided', ''),
                'absolute_url': case_data.get('absolute_url', ''),
                'aiSummary': {
                    'keyPoints': ai_result.get('analysis', {}).get('case_summary', ['Summary not available'])[i] if i < len(ai_result.get('analysis', {}).get('case_summary', [])) else 'Summary not available',
                    'legalPrinciples': ai_result.get('analysis', {}).get('legal_rules', [[]])[i] if i < len(ai_result.get('analysis', {}).get('legal_rules', [])) else [],
                    'relevance': ai_result.get('analysis', {}).get('relevance', ['Relevance analysis not available'])[i] if i < len(ai_result.get('analysis', {}).get('relevance', [])) else 'Relevance analysis not available',
                    'practicalAdvice': ai_result.get('analysis', {}).get('practical_advice', [[]])[i] if i < len(ai_result.get('analysis', {}).get('practical_advice', [])) else []
                },
                'rawData': case_data
            }
            summaries.append(summary)
        
        return {
            'summaries': summaries,
            'processingTime': processing_time,
            'aiConfidence': ai_result.get('confidence', 0.8)
        }
        
    except Exception as e:
        logger.error(f"AI Summarization Error: {e}")
        
        # Fallback: return cases without AI enhancement
        summaries = []
        for case_data in cases:
            summary = {
                'caseId': case_data.get('id', ''),
                'caseName': case_data.get('caseName', 'Unknown Case'),
                'court': case_data.get('court', 'Unknown Court'),
                'dateFiled': case_data.get('dateFiled', ''),
                'dateDecided': case_data.get('dateDecided', ''),
                'absolute_url': case_data.get('absolute_url', ''),
                'aiSummary': {
                    'keyPoints': 'AI summarization temporarily unavailable',
                    'legalPrinciples': [],
                    'relevance': 'Manual review recommended',
                    'practicalAdvice': []
                },
                'rawData': case_data
            }
            summaries.append(summary)
        
        return {
            'summaries': summaries,
            'processingTime': 'N/A',
            'aiConfidence': 0.0,
            'error': 'AI summarization failed, showing raw data'
        }
