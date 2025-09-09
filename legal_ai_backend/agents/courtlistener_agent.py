"""
CourtListener Agent - Searches live case law using CourtListener API.
Provides real-time access to court opinions and case data.
"""
import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

from case_sources.courtlistener import CourtListenerClient, CaseResult

logger = logging.getLogger(__name__)

@dataclass
class SearchResult:
    """Structured search result from CourtListener."""
    cases: List[CaseResult]
    total_found: int
    search_query: str
    jurisdiction: str
    case_type: str

class CourtListenerAgent:
    """Agent responsible for searching live case law via CourtListener API."""
    
    def __init__(self):
        self.client = CourtListenerClient()
    
    def build_search_query(self, context: Dict[str, Any]) -> str:
        """
        Build optimized search query from intake context.
        
        Args:
            context: Intake context with topic, keywords, etc.
            
        Returns:
            Optimized search query string
        """
        topic = context.get("topic", "")
        keywords = context.get("keywords", [])
        case_type = context.get("case_type", "")
        suggested_charges = context.get("suggested_charges", [])
        
        # Build query components
        query_parts = []
        
        # Add topic
        if topic and topic != "general":
            query_parts.append(topic)
        
        # Add keywords (limit to most relevant)
        relevant_keywords = keywords[:3]  # Top 3 keywords
        query_parts.extend(relevant_keywords)
        
        # Add case type if specific
        if case_type and case_type != "general":
            query_parts.append(case_type)
        
        # Add suggested charges if available
        if suggested_charges:
            # Take first suggested charge
            charge_words = suggested_charges[0].lower().split()[:2]  # First 2 words
            query_parts.extend(charge_words)
        
        # Join with spaces and clean up
        query = " ".join(query_parts)
        
        # Remove duplicates and clean
        query = " ".join(list(dict.fromkeys(query.split())))
        
        logger.info(f"Built search query: '{query}' from context: {context}")
        return query
    
    def search_cases(self, context: Dict[str, Any]) -> SearchResult:
        """
        Search for cases using CourtListener API.
        
        Args:
            context: Intake context with legal information
            
        Returns:
            SearchResult with found cases
        """
        try:
            # Build search query
            query = self.build_search_query(context)
            jurisdiction = context.get("jurisdiction", "ri")
            case_type = context.get("case_type", "")
            
            # Map case types to CourtListener format
            courtlistener_case_type = None
            if case_type == "criminal":
                courtlistener_case_type = "criminal"
            elif case_type == "civil":
                courtlistener_case_type = "civil"
            
            # Search for cases
            cases = self.client.search_cases(
                query=query,
                jurisdiction=jurisdiction,
                case_type=courtlistener_case_type,
                limit=10
            )
            
            result = SearchResult(
                cases=cases,
                total_found=len(cases),
                search_query=query,
                jurisdiction=jurisdiction,
                case_type=case_type
            )
            
            logger.info(f"Found {len(cases)} cases for query: {query}")
            return result
            
        except Exception as e:
            logger.error(f"Error searching CourtListener: {e}")
            return SearchResult(
                cases=[],
                total_found=0,
                search_query=context.get("original_input", ""),
                jurisdiction=context.get("jurisdiction", "ri"),
                case_type=context.get("case_type", "")
            )
    
    def get_case_details(self, case: CaseResult) -> Optional[Dict[str, Any]]:
        """
        Get detailed information about a specific case.
        
        Args:
            case: CaseResult from search
            
        Returns:
            Detailed case information or None
        """
        try:
            return self.client.get_case_details(case.resource_uri)
        except Exception as e:
            logger.error(f"Error getting case details: {e}")
            return None

def search_live(context: Dict[str, Any]) -> Dict[str, Any]:
    """
    Main function for LangGraph - searches live case law.
    
    Args:
        context: Intake context from previous agent
        
    Returns:
        Dictionary with search results
    """
    agent = CourtListenerAgent()
    result = agent.search_cases(context)
    
    # Convert to serializable format
    cases_data = []
    for case in result.cases:
        cases_data.append({
            "case_name": case.case_name,
            "court": case.court,
            "date_filed": case.date_filed,
            "absolute_url": case.absolute_url,
            "snippet": case.snippet,
            "jurisdiction": case.jurisdiction,
            "case_type": case.case_type,
            "resource_uri": case.resource_uri
        })
    
    return {
        "source": "courtlistener",
        "cases": cases_data,
        "total_found": result.total_found,
        "search_query": result.search_query,
        "jurisdiction": result.jurisdiction,
        "case_type": result.case_type,
        "success": len(cases_data) > 0
    }

# Example usage and testing
if __name__ == "__main__":
    # Test the CourtListener agent
    test_context = {
        "topic": "criminal",
        "jurisdiction": "ri",
        "case_type": "criminal",
        "keywords": ["gun", "possession"],
        "urgency": "high",
        "original_input": "I was charged with gun possession in Rhode Island",
        "suggested_charges": ["Unlawful possession of firearm"]
    }
    
    agent = CourtListenerAgent()
    result = agent.search_cases(test_context)
    
    print(f"Search Query: {result.search_query}")
    print(f"Found {result.total_found} cases:")
    print()
    
    for i, case in enumerate(result.cases[:3], 1):
        print(f"{i}. {case.case_name}")
        print(f"   Court: {case.court}")
        print(f"   Date: {case.date_filed}")
        print(f"   Snippet: {case.snippet[:100]}...")
        print()
