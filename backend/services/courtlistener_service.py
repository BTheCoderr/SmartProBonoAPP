"""
CourtListener API Integration Service
Provides real case law research using the CourtListener API
"""

import requests
import logging
import os
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import json

logger = logging.getLogger(__name__)

class CourtListenerService:
    """
    Service for integrating with CourtListener API for case law research.
    Provides real case law data instead of simulated research.
    """
    
    def __init__(self):
        self.base_url = "https://www.courtlistener.com/api/rest/v3"
        self.search_url = f"{self.base_url}/search/"
        self.case_url = f"{self.base_url}/cases/"
        self.docket_url = f"{self.base_url}/dockets/"
        
        # API Key configuration
        self.api_key = os.getenv("COURTLISTENER_API_KEY")
        self.headers = {}
        if self.api_key:
            self.headers = {"Authorization": f"Token {self.api_key}"}
            self.fallback_mode = False
            logger.info("CourtListener API key found - using real API")
        else:
            self.fallback_mode = True
            logger.warning("COURTLISTENER_API_KEY not set - using fallback mode")
        
        # Rate limiting
        self.last_request_time = None
        self.min_request_interval = 1.0  # 1 second between requests
    
    def _rate_limit(self):
        """Ensure we don't exceed rate limits."""
        if self.last_request_time:
            elapsed = (datetime.now() - self.last_request_time).total_seconds()
            if elapsed < self.min_request_interval:
                import time
                time.sleep(self.min_request_interval - elapsed)
        self.last_request_time = datetime.now()
    
    def search_cases(self, query: str, case_type: str = None, 
                    court: str = None, date_after: str = None, 
                    date_before: str = None, limit: int = 20) -> Dict[str, Any]:
        """
        Search for cases using CourtListener API.
        
        Args:
            query: Search query (case name, keywords, etc.)
            case_type: Type of case (e.g., 'criminal', 'civil')
            court: Court name or jurisdiction
            date_after: Search cases after this date (YYYY-MM-DD)
            date_before: Search cases before this date (YYYY-MM-DD)
            limit: Maximum number of results to return
            
        Returns:
            Search results with case information
        """
        try:
            # Check if we're in fallback mode
            if self.fallback_mode:
                return self._get_fallback_search_results(query, case_type, court, limit)
            
            self._rate_limit()
            
            # Build search parameters
            params = {
                'q': query,
                'format': 'json',
                'order_by': 'score desc',
                'stat_Precedential': 'on',  # Only precedential cases
                'stat_Non_Precedential': 'on',
                'stat_Unknown': 'on'
            }
            
            if case_type:
                params['type'] = case_type
            if court:
                params['court'] = court
            if date_after:
                params['filed_after'] = date_after
            if date_before:
                params['filed_before'] = date_before
            
            # Add pagination
            params['page_size'] = min(limit, 100)  # API max is 100
            
            # Make the request
            response = requests.get(self.search_url, params=params, headers=self.headers, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            
            # Process results
            results = {
                'success': True,
                'query': query,
                'total_results': data.get('count', 0),
                'cases': [],
                'search_timestamp': datetime.now().isoformat()
            }
            
            # Extract case information
            for result in data.get('results', []):
                case_info = self._extract_case_info(result)
                if case_info:
                    results['cases'].append(case_info)
            
            logger.info(f"CourtListener search successful: {len(results['cases'])} cases found for query '{query}'")
            return results
            
        except requests.exceptions.RequestException as e:
            logger.error(f"CourtListener API request failed: {e}")
            return {
                'success': False,
                'error': f"API request failed: {str(e)}",
                'query': query,
                'cases': []
            }
        except Exception as e:
            logger.error(f"CourtListener search error: {e}")
            return {
                'success': False,
                'error': f"Search error: {str(e)}",
                'query': query,
                'cases': []
            }
    
    def _extract_case_info(self, result: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Extract relevant case information from API result."""
        try:
            case_info = {
                'case_name': result.get('caseName', 'Unknown'),
                'court': result.get('court', 'Unknown'),
                'date_filed': result.get('dateFiled', ''),
                'date_modified': result.get('dateModified', ''),
                'absolute_url': result.get('absolute_url', ''),
                'case_id': result.get('id', ''),
                'docket_number': result.get('docketNumber', ''),
                'citation': result.get('citation', ''),
                'precedential': result.get('precedential', False),
                'jurisdiction': result.get('jurisdiction', ''),
                'case_type': result.get('caseType', ''),
                'status': result.get('status', ''),
                'snippet': result.get('snippet', ''),
                'resource_uri': result.get('resource_uri', '')
            }
            
            # Clean up the case name
            if case_info['case_name'] and case_info['case_name'] != 'Unknown':
                case_info['case_name'] = case_info['case_name'].strip()
            
            return case_info
            
        except Exception as e:
            logger.error(f"Error extracting case info: {e}")
            return None
    
    def get_case_details(self, case_id: str) -> Dict[str, Any]:
        """
        Get detailed information about a specific case.
        
        Args:
            case_id: CourtListener case ID
            
        Returns:
            Detailed case information
        """
        try:
            self._rate_limit()
            
            url = f"{self.case_url}{case_id}/"
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            
            return {
                'success': True,
                'case_details': data,
                'retrieved_at': datetime.now().isoformat()
            }
            
        except requests.exceptions.RequestException as e:
            logger.error(f"CourtListener case details request failed: {e}")
            return {
                'success': False,
                'error': f"Case details request failed: {str(e)}"
            }
        except Exception as e:
            logger.error(f"CourtListener case details error: {e}")
            return {
                'success': False,
                'error': f"Case details error: {str(e)}"
            }
    
    def search_similar_cases(self, case_data: Dict[str, Any], limit: int = 10) -> Dict[str, Any]:
        """
        Search for cases similar to a given case.
        
        Args:
            case_data: Case information to find similar cases for
            limit: Maximum number of similar cases to return
            
        Returns:
            Similar cases found
        """
        try:
            # Build search query from case data
            query_parts = []
            
            if case_data.get('title'):
                query_parts.append(case_data['title'])
            if case_data.get('type'):
                query_parts.append(case_data['type'])
            if case_data.get('client_name'):
                query_parts.append(case_data['client_name'])
            
            query = ' '.join(query_parts)
            
            if not query.strip():
                return {
                    'success': False,
                    'error': 'No search terms available from case data',
                    'similar_cases': []
                }
            
            # Search for similar cases
            results = self.search_cases(
                query=query,
                case_type=case_data.get('type'),
                limit=limit
            )
            
            if results.get('success'):
                return {
                    'success': True,
                    'original_case': case_data,
                    'similar_cases': results['cases'],
                    'total_found': results['total_results'],
                    'search_timestamp': datetime.now().isoformat()
                }
            else:
                return results
                
        except Exception as e:
            logger.error(f"Similar cases search error: {e}")
            return {
                'success': False,
                'error': f"Similar cases search error: {str(e)}",
                'similar_cases': []
            }
    
    def get_recent_cases(self, case_type: str = None, days: int = 30, limit: int = 20) -> Dict[str, Any]:
        """
        Get recent cases from the last N days.
        
        Args:
            case_type: Type of case to filter by
            days: Number of days to look back
            limit: Maximum number of cases to return
            
        Returns:
            Recent cases
        """
        try:
            # Calculate date range
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)
            
            date_after = start_date.strftime('%Y-%m-%d')
            date_before = end_date.strftime('%Y-%m-%d')
            
            # Search for recent cases
            results = self.search_cases(
                query='*',  # Broad search
                case_type=case_type,
                date_after=date_after,
                date_before=date_before,
                limit=limit
            )
            
            if results.get('success'):
                results['search_type'] = 'recent_cases'
                results['date_range'] = {
                    'start': date_after,
                    'end': date_before,
                    'days': days
                }
            
            return results
            
        except Exception as e:
            logger.error(f"Recent cases search error: {e}")
            return {
                'success': False,
                'error': f"Recent cases search error: {str(e)}",
                'cases': []
            }
    
    def _get_fallback_search_results(self, query: str, case_type: str = None, 
                                   court: str = None, limit: int = 20) -> Dict[str, Any]:
        """
        Fallback search results when API key is not available.
        Returns realistic mock data for development/testing.
        """
        logger.info(f"Using fallback mode for search: '{query}'")
        
        # Generate realistic mock case data
        mock_cases = []
        case_types = ['civil', 'criminal', 'immigration', 'family', 'employment']
        courts = ['Supreme Court', 'Court of Appeals', 'District Court', 'State Court']
        
        for i in range(min(limit, 5)):  # Limit to 5 mock cases
            mock_case = {
                'case_name': f"Mock Case {i+1}: {query.title()}",
                'court': courts[i % len(courts)],
                'date_filed': (datetime.now() - timedelta(days=i*30)).strftime('%Y-%m-%d'),
                'citation': f"Mock Citation {i+1}",
                'precedential': i % 2 == 0,
                'snippet': f"This is a mock case related to '{query}' for testing purposes.",
                'url': f"https://example.com/mock-case-{i+1}",
                'case_type': case_type or case_types[i % len(case_types)],
                'status': 'Mock Status'
            }
            mock_cases.append(mock_case)
        
        return {
            'success': True,
            'query': query,
            'total_results': len(mock_cases),
            'cases': mock_cases,
            'search_timestamp': datetime.now().isoformat(),
            'fallback_mode': True,
            'message': 'Using fallback data - CourtListener API key not configured'
        }

# Global instance
courtlistener_service = CourtListenerService()
