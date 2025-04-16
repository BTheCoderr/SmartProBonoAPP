import pytest
import json
from unittest.mock import patch, MagicMock
from services.legal_assistant_service import LegalAssistantService


class TestLegalAssistantService:
    """Test cases for the Legal Assistant Service."""

    @pytest.fixture
    def legal_service(self):
        """Create a legal assistant service for testing."""
        with patch('services.legal_assistant_service.VectorDatabaseManager') as mock_vector_db:
            with patch('services.legal_assistant_service.AIServiceManager') as mock_ai_manager:
                # Configure mocks
                mock_vector_db_instance = MagicMock()
                mock_vector_db.return_value = mock_vector_db_instance
                
                mock_ai_manager_instance = MagicMock()
                mock_ai_manager.return_value = mock_ai_manager_instance
                
                # Create service with patched dependencies
                service = LegalAssistantService()
                
                # Use __dict__ to directly set private attributes without triggering type checking
                service.__dict__['_vector_db'] = mock_vector_db_instance
                service.__dict__['_ai_service'] = mock_ai_manager_instance
                
                return service
    
    @pytest.mark.asyncio
    async def test_detect_legal_domain(self, legal_service):
        """Test detecting legal domain from query."""
        # Arrange
        query = "I need help with my divorce case"
        # Access the mock via __dict__ to avoid type checking issues
        legal_service.__dict__['_ai_service'].get_response.return_value = {
            "content": "Family Law",
            "confidence": 0.92
        }
        
        # Act
        domain, confidence = legal_service.detect_legal_domain(query)
        
        # Assert
        assert domain == "Family Law"
        assert confidence == 0.92
        legal_service.__dict__['_ai_service'].get_response.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_detect_jurisdiction(self, legal_service):
        """Test detecting jurisdiction from query."""
        # Arrange
        query = "I have a legal issue in California"
        legal_service.__dict__['_ai_service'].detect_jurisdictions.return_value = ["California"]
        
        # Act
        jurisdiction = legal_service.detect_jurisdiction(query)
        
        # Assert
        assert jurisdiction == "California"
        legal_service.__dict__['_ai_service'].detect_jurisdictions.assert_called_once_with(query)
    
    @pytest.mark.asyncio
    async def test_get_legal_response_with_citations(self, legal_service):
        """Test getting legal response with citations."""
        # Arrange
        query = "What are my rights as a tenant in New York?"
        jurisdiction = "New York"
        
        search_results = [
            {"id": "doc1", "content": "Tenant rights in NY include...", "source": "NY Tenant Law"},
            {"id": "doc2", "content": "Landlords must provide...", "source": "NY Housing Regulations"}
        ]
        
        legal_service.__dict__['_vector_db'].search_by_jurisdiction.return_value = search_results
        
        mock_response = {
            "content": "As a tenant in New York, you have several rights including...",
            "citations": [{"id": "cite1", "text": "NY Tenant Law Sec. 123"}],
            "confidence": 0.85
        }
        
        legal_service.__dict__['_ai_service'].get_response.return_value = mock_response
        legal_service._get_from_cache = MagicMock(return_value=None)
        legal_service._add_to_cache = MagicMock()
        
        # Act
        response = await legal_service.get_legal_response_with_citations(query, jurisdiction)
        
        # Assert
        assert "content" in response
        assert "citations" in response
        assert response["content"] == mock_response["content"]
        legal_service.__dict__['_vector_db'].search_by_jurisdiction.assert_called_once()
        legal_service.__dict__['_ai_service'].get_response.assert_called_once()
        legal_service._add_to_cache.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_get_legal_response_from_cache(self, legal_service):
        """Test getting legal response from cache."""
        # Arrange
        query = "What are my rights as a tenant?"
        cached_response = {
            "content": "Cached response about tenant rights",
            "citations": [{"id": "cite1", "text": "Citation 1"}],
            "timestamp": "2023-01-01T00:00:00"
        }
        
        legal_service._get_from_cache = MagicMock(return_value=cached_response)
        
        # Act
        response = await legal_service.get_legal_response_with_citations(query)
        
        # Assert
        assert response == cached_response
        legal_service._get_from_cache.assert_called_once()
        # Ensure search is not called when we have a cache hit
        legal_service.__dict__['_vector_db'].search.assert_not_called()
    
    def test_parse_citations_from_text(self, legal_service):
        """Test parsing citations from text."""
        # Arrange
        text = "According to Smith v. Jones (2020) and Section 123 of Housing Law..."
        expected_citations = [
            {"id": "citation1", "text": "Smith v. Jones (2020)"},
            {"id": "citation2", "text": "Section 123 of Housing Law"}
        ]
        
        legal_service.__dict__['_ai_service'].extract_citations.return_value = expected_citations
        
        # Act
        citations = legal_service.parse_citations_from_text(text)
        
        # Assert
        assert citations == expected_citations
        legal_service.__dict__['_ai_service'].extract_citations.assert_called_once_with(text)
    
    def test_get_legal_resources(self, legal_service):
        """Test getting legal resources by domain and jurisdiction."""
        # Arrange
        domain = "Housing"
        jurisdiction = "California"
        expected_resources = [
            {"title": "CA Tenant Handbook", "url": "https://example.com/tenant-handbook"},
            {"title": "Legal Aid Housing Clinic", "url": "https://example.com/housing-clinic"}
        ]
        
        # Mock the internal implementation
        legal_service._load_resources = MagicMock(return_value={
            "Housing": {
                "California": expected_resources,
                "New York": [{"title": "NY Resource", "url": "https://example.com/ny"}]
            }
        })
        
        # Act
        resources = legal_service.get_legal_resources(domain, jurisdiction)
        
        # Assert
        assert resources == expected_resources
    
    def test_get_citation_details(self, legal_service):
        """Test getting citation details by ID."""
        # Arrange
        citation_id = "citation123"
        expected_details = {
            "id": citation_id,
            "title": "Smith v. Jones",
            "full_text": "Smith v. Jones (2020) 123 Cal.4th 456",
            "summary": "A landmark case about...",
            "url": "https://example.com/case/smith-v-jones"
        }
        
        legal_service.__dict__['_vector_db'].get_document_by_id.return_value = expected_details
        
        # Act
        details = legal_service.get_citation_details(citation_id)
        
        # Assert
        assert details == expected_details
        legal_service.__dict__['_vector_db'].get_document_by_id.assert_called_once_with(citation_id)
    
    @pytest.mark.asyncio
    async def test_get_specialized_legal_response(self, legal_service):
        """Test getting specialized legal response for a specific domain."""
        # Arrange
        query = "What is the eviction process?"
        domain = "Housing"
        jurisdiction = "California"
        model_id = "housing-model-v1"
        
        search_results = [
            {"id": "doc1", "content": "The eviction process in CA...", "source": "CA Eviction Guide"},
            {"id": "doc2", "content": "Landlords must provide notice...", "source": "CA Housing Code"}
        ]
        
        legal_service.__dict__['_vector_db'].search_by_jurisdiction.return_value = search_results
        
        expected_response = {
            "content": "The eviction process in California requires landlords to...",
            "citations": [{"id": "cite1", "text": "CA Civil Code 1946.2"}],
            "confidence": 0.95,
            "model": model_id
        }
        
        legal_service.__dict__['_ai_service'].get_response.return_value = expected_response
        legal_service._get_from_cache = MagicMock(return_value=None)
        legal_service._add_to_cache = MagicMock()
        
        # Act
        response = await legal_service.get_specialized_legal_response(
            query, domain, jurisdiction, model_id
        )
        
        # Assert
        assert response == expected_response
        legal_service.__dict__['_vector_db'].search_by_jurisdiction.assert_called_once()
        legal_service.__dict__['_ai_service'].get_response.assert_called_once()
        legal_service._add_to_cache.assert_called_once() 