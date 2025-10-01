"""
Simple SmartProBono Agent Service - Mock implementation
"""
import logging
from datetime import datetime
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class SimpleSmartProBonoAgentService:
    """Simple mock implementation of SmartProBono Agent Service"""
    
    def __init__(self):
        self.mock_mode = True
        logger.info("SimpleSmartProBonoAgentService initialized in mock mode")
    
    def process_legal_query(self, user_input: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Process a legal query with mock response"""
        return {
            "response": f"Mock response for legal query: {user_input}",
            "confidence": 0.8,
            "sources": ["Mock legal database"],
            "timestamp": datetime.now().isoformat(),
            "mock": True
        }
    
    def create_case(self, case_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a case with mock response"""
        return {
            "case_id": f"mock_case_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "status": "created",
            "message": "Case created successfully (mock)",
            "mock": True
        }
    
    def search_cases(self, search_params: Dict[str, Any]) -> Dict[str, Any]:
        """Search cases with mock response"""
        return {
            "cases": [
                {
                    "id": "mock_case_1",
                    "title": "Mock Legal Case",
                    "status": "open",
                    "client": "Mock Client"
                }
            ],
            "total": 1,
            "mock": True
        }
    
    def analyze_document(self, document_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze document with mock response"""
        return {
            "analysis": "Mock document analysis",
            "confidence": 0.7,
            "recommendations": ["Mock recommendation 1", "Mock recommendation 2"],
            "mock": True
        }
    
    def get_agent_status(self) -> Dict[str, Any]:
        """Get agent status"""
        return {
            "status": "active",
            "mode": "mock",
            "capabilities": ["legal_query", "case_management", "document_analysis"],
            "mock": True
        }

