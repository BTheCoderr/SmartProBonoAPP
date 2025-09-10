"""
Merge Agent - Combines results from multiple search sources
"""

import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

def merge_results(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Merge results from live search and vector search into a unified dataset.
    
    Args:
        state: Current state containing courtlistener_results and vector_results
        
    Returns:
        Updated state with merged results
    """
    try:
        # Get results from both sources
        live_results = state.get('courtlistener_results', {})
        vector_results = state.get('vector_results', {})
        
        # Extract cases from each source
        live_cases = live_results.get('cases', [])
        vector_cases = vector_results.get('cases', [])
        
        # Merge cases with source attribution
        merged_cases = []
        
        # Add live cases with source info
        for case in live_cases:
            case['source'] = 'courtlistener'
            case['search_type'] = 'live'
            merged_cases.append(case)
        
        # Add vector cases with source info
        for case in vector_cases:
            case['source'] = 'chromadb'
            case['search_type'] = 'embedded'
            merged_cases.append(case)
        
        # Remove duplicates based on case name and court
        unique_cases = []
        seen_cases = set()
        
        for case in merged_cases:
            case_key = f"{case.get('case_name', '')}_{case.get('court', '')}"
            if case_key not in seen_cases:
                seen_cases.add(case_key)
                unique_cases.append(case)
        
        # Sort by relevance score if available
        unique_cases.sort(key=lambda x: x.get('relevance_score', 0), reverse=True)
        
        # Create merged results
        merged_results = {
            'total_cases': len(unique_cases),
            'live_cases': len(live_cases),
            'vector_cases': len(vector_cases),
            'unique_cases': len(unique_cases),
            'cases': unique_cases,
            'sources': ['courtlistener', 'chromadb'],
            'merge_timestamp': state.get('intake_result', {}).get('timestamp', 'unknown')
        }
        
        # Update state
        state['merged_results'] = merged_results
        
        logger.info(f"Successfully merged {len(unique_cases)} unique cases from {len(live_cases)} live and {len(vector_cases)} vector results")
        
        return state
        
    except Exception as e:
        logger.error(f"Error merging results: {e}")
        state['errors'] = state.get('errors', []) + [f"Merge error: {str(e)}"]
        return state
