"""
CourtListener API client for searching case law.
Free tier provides access to court opinions and case data.
"""
import requests
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class CaseResult:
    """Structured case result from CourtListener API."""
    case_name: str
    court: str
    date_filed: str
    absolute_url: str
    snippet: str
    jurisdiction: str
    case_type: str
    resource_uri: str

class CourtListenerClient:
    """Client for interacting with CourtListener API."""
    
    def __init__(self, base_url: str = "https://www.courtlistener.com/api/rest/v3/opinions/"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'SmartProBono-LegalAI/1.0 (Legal Research Assistant)'
        })
    
    def search_cases(
        self, 
        query: str, 
        jurisdiction: str = "ri",
        case_type: Optional[str] = None,
        order_by: str = "score desc",
        stat_precedential: str = "on",
        limit: int = 10
    ) -> List[CaseResult]:
        """
        Search for cases using CourtListener API.
        
        Args:
            query: Search terms
            jurisdiction: State code (ri, ma, ct, etc.)
            case_type: Type of case (criminal, civil, etc.)
            order_by: Sort order
            stat_precedential: Only precedential cases
            limit: Number of results to return
            
        Returns:
            List of CaseResult objects
        """
        params = {
            "search": query,
            "jurisdiction": jurisdiction,
            "order_by": order_by,
            "stat_precedential": stat_precedential,
            "format": "json",
            "page_size": min(limit, 100)  # API limit
        }
        
        if case_type:
            params["case_type"] = case_type
        
        try:
            response = self.session.get(self.base_url, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            results = []
            
            for case in data.get("results", []):
                try:
                    case_result = CaseResult(
                        case_name=case.get("caseName", "Unknown Case"),
                        court=case.get("court", "Unknown Court"),
                        date_filed=case.get("date_filed", "Unknown Date"),
                        absolute_url=case.get("absolute_url", ""),
                        snippet=case.get("snippet", ""),
                        jurisdiction=case.get("jurisdiction", {}).get("slug", jurisdiction),
                        case_type=case.get("case_type", "Unknown"),
                        resource_uri=case.get("resource_uri", "")
                    )
                    results.append(case_result)
                except Exception as e:
                    logger.warning(f"Error parsing case result: {e}")
                    continue
            
            logger.info(f"Found {len(results)} cases for query: {query}")
            return results
            
        except requests.exceptions.RequestException as e:
            logger.error(f"CourtListener API error: {e}")
            # Return mock data for development when API is not available
            return self._get_mock_cases(query, jurisdiction)
        except Exception as e:
            logger.error(f"Unexpected error in CourtListener search: {e}")
            return self._get_mock_cases(query, jurisdiction)
    
    def get_case_details(self, resource_uri: str) -> Optional[Dict[str, Any]]:
        """
        Get detailed information about a specific case.
        
        Args:
            resource_uri: URI of the case from search results
            
        Returns:
            Detailed case information or None if error
        """
        try:
            response = self.session.get(resource_uri, timeout=30)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error fetching case details: {e}")
            return None
    
    def _get_mock_cases(self, query: str, jurisdiction: str) -> List[CaseResult]:
        """Return mock case data for development when API is not available."""
        logger.info(f"Returning mock cases for query: {query} in {jurisdiction}")
        
        mock_cases = [
            CaseResult(
                case_name="Mock Case v. State",
                court=f"{jurisdiction.upper()} Supreme Court",
                date_filed="2023-01-15",
                absolute_url="https://example.com/mock-case-1",
                snippet=f"This is a mock case related to {query}. In this case, the court considered the legal issues surrounding the matter and provided guidance on how similar cases should be handled.",
                jurisdiction=jurisdiction,
                case_type="civil",
                resource_uri="https://example.com/api/mock-case-1"
            ),
            CaseResult(
                case_name="Sample Legal Matter",
                court=f"{jurisdiction.upper()} Court of Appeals",
                date_filed="2023-03-20",
                absolute_url="https://example.com/mock-case-2",
                snippet=f"Another mock case involving {query}. The court's decision in this matter established important legal principles that may be relevant to your situation.",
                jurisdiction=jurisdiction,
                case_type="criminal",
                resource_uri="https://example.com/api/mock-case-2"
            )
        ]
        
        return mock_cases

def search_courtlistener(
    query: str, 
    jurisdiction: str = "ri",
    case_type: Optional[str] = None,
    limit: int = 10
) -> List[CaseResult]:
    """
    Convenience function for searching CourtListener.
    
    Args:
        query: Search terms
        jurisdiction: State code
        case_type: Type of case
        limit: Number of results
        
    Returns:
        List of case results
    """
    client = CourtListenerClient()
    return client.search_cases(query, jurisdiction, case_type, limit=limit)

# Example usage and testing
if __name__ == "__main__":
    # Test the CourtListener client
    client = CourtListenerClient()
    
    # Search for gun possession cases in Rhode Island
    results = client.search_cases(
        query="gun possession criminal",
        jurisdiction="ri",
        case_type="criminal",
        limit=5
    )
    
    print(f"Found {len(results)} cases:")
    for case in results:
        print(f"- {case.case_name} ({case.court}) - {case.date_filed}")
        print(f"  {case.snippet[:100]}...")
        print()
