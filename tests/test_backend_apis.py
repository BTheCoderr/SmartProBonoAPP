"""
Comprehensive Backend API Tests
Tests all the new API endpoints and services we've implemented
"""

import pytest
import json
import os
import sys
import tempfile
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock

# Add the backend directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from combined_server import app
from services.voice_service import voice_service
from services.court_filing_service import court_filing_service
from services.analytics_service import AnalyticsService
from services.audit_service import AuditService

@pytest.fixture
def client():
    """Create a test client for the Flask app"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def auth_headers():
    """Mock authentication headers"""
    return {'Authorization': 'Bearer test-token'}

class TestImmigrationCRMAPI:
    """Test Immigration CRM API endpoints"""
    
    def test_get_immigration_cases(self, client):
        """Test getting immigration cases"""
        response = client.get('/api/immigration/cases')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] == True
        assert 'cases' in data
    
    def test_create_immigration_case(self, client):
        """Test creating a new immigration case"""
        case_data = {
            'clientName': 'John Doe',
            'caseType': 'Asylum',
            'status': 'New',
            'priority': 'High',
            'description': 'Test case'
        }
        
        response = client.post('/api/immigration/cases',
                             data=json.dumps(case_data),
                             content_type='application/json')
        
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['success'] == True
        assert 'case' in data
        assert data['case']['clientName'] == 'John Doe'
    
    def test_create_case_missing_fields(self, client):
        """Test creating case with missing required fields"""
        case_data = {
            'clientName': 'John Doe'
            # Missing caseType
        }
        
        response = client.post('/api/immigration/cases',
                             data=json.dumps(case_data),
                             content_type='application/json')
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['success'] == False
        assert 'error' in data
    
    def test_update_immigration_case(self, client):
        """Test updating an immigration case"""
        # First create a case
        case_data = {
            'clientName': 'John Doe',
            'caseType': 'Asylum',
            'status': 'New'
        }
        
        create_response = client.post('/api/immigration/cases',
                                    data=json.dumps(case_data),
                                    content_type='application/json')
        case_id = json.loads(create_response.data)['case']['id']
        
        # Update the case
        update_data = {
            'status': 'In Progress',
            'priority': 'High'
        }
        
        response = client.put(f'/api/immigration/cases/{case_id}',
                            data=json.dumps(update_data),
                            content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] == True
        assert data['case']['status'] == 'In Progress'
    
    def test_delete_immigration_case(self, client):
        """Test deleting an immigration case"""
        # First create a case
        case_data = {
            'clientName': 'John Doe',
            'caseType': 'Asylum'
        }
        
        create_response = client.post('/api/immigration/cases',
                                    data=json.dumps(case_data),
                                    content_type='application/json')
        case_id = json.loads(create_response.data)['case']['id']
        
        # Delete the case
        response = client.delete(f'/api/immigration/cases/{case_id}')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] == True
    
    def test_get_immigration_stats(self, client):
        """Test getting immigration case statistics"""
        response = client.get('/api/immigration/cases/stats')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] == True
        assert 'total_cases' in data
        assert 'status_breakdown' in data

class TestVoiceAPI:
    """Test Voice API endpoints"""
    
    def test_get_voice_status(self, client):
        """Test getting voice service status"""
        response = client.get('/api/voice/status')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] == True
        assert 'statistics' in data
    
    def test_get_supported_languages(self, client):
        """Test getting supported languages"""
        response = client.get('/api/voice/languages')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] == True
        assert 'languages' in data
        assert len(data['languages']) > 0
    
    def test_get_available_voices(self, client):
        """Test getting available voices"""
        response = client.get('/api/voice/voices?language=en-US')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] == True
        assert 'voices' in data
    
    @patch('routes.voice_api.voice_service.is_available')
    def test_speech_to_text_unavailable(self, mock_available, client):
        """Test speech-to-text when service is unavailable"""
        mock_available.return_value = False
        
        audio_data = {
            'audio_data': 'base64encodedaudio',
            'language': 'en-US'
        }
        
        response = client.post('/api/voice/speech-to-text',
                             data=json.dumps(audio_data),
                             content_type='application/json')
        
        assert response.status_code == 503
        data = json.loads(response.data)
        assert data['success'] == False
    
    def test_text_to_speech_missing_data(self, client):
        """Test text-to-speech with missing data"""
        response = client.post('/api/voice/text-to-speech',
                             data=json.dumps({}),
                             content_type='application/json')
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['success'] == False
    
    def test_process_voice_command(self, client):
        """Test processing voice commands"""
        command_data = {
            'text': 'What are my legal options for immigration?',
            'user_id': 'test_user'
        }
        
        response = client.post('/api/voice/command',
                             data=json.dumps(command_data),
                             content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'success' in data
    
    def test_analyze_voice_input(self, client):
        """Test analyzing voice input"""
        analysis_data = {
            'text': 'I need help with my immigration case',
            'context': {'user_type': 'client'}
        }
        
        response = client.post('/api/voice/analyze',
                             data=json.dumps(analysis_data),
                             content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'success' in data

class TestCourtFilingAPI:
    """Test Court Filing API endpoints"""
    
    def test_get_filing_status(self, client):
        """Test getting court filing service status"""
        response = client.get('/api/court-filing/status')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] == True
        assert 'statistics' in data
    
    def test_get_court_rules(self, client):
        """Test getting court rules"""
        response = client.get('/api/court-filing/rules?jurisdiction=Rhode Island')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] == True
        assert 'rules' in data
        assert len(data['rules']) > 0
    
    def test_get_filing_templates(self, client):
        """Test getting filing templates"""
        response = client.get('/api/court-filing/templates?document_type=complaint')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] == True
        assert 'templates' in data
    
    def test_generate_document_missing_template(self, client):
        """Test document generation with invalid template"""
        data = {
            'template_id': 'nonexistent_template',
            'data': {'test': 'value'}
        }
        
        response = client.post('/api/court-filing/generate',
                             data=json.dumps(data),
                             content_type='application/json')
        
        assert response.status_code == 500
        response_data = json.loads(response.data)
        assert response_data['success'] == False
    
    def test_create_filing(self, client):
        """Test creating a court filing"""
        filing_data = {
            'case_id': 'CASE-001',
            'document_type': 'complaint',
            'title': 'Test Complaint',
            'description': 'Test filing',
            'court': 'Superior Court',
            'jurisdiction': 'Rhode Island'
        }
        
        response = client.post('/api/court-filing/filings',
                             data=json.dumps(filing_data),
                             content_type='application/json')
        
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['success'] == True
        assert 'filing' in data
        assert data['filing']['title'] == 'Test Complaint'
    
    def test_calculate_filing_fees(self, client):
        """Test calculating filing fees"""
        fee_data = {
            'document_type': 'complaint',
            'jurisdiction': 'Rhode Island',
            'court': 'Superior Court'
        }
        
        response = client.post('/api/court-filing/fees',
                             data=json.dumps(fee_data),
                             content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] == True
        assert 'fees' in data
        assert isinstance(data['fees'], (int, float))
    
    def test_calculate_filing_deadlines(self, client):
        """Test calculating filing deadlines"""
        deadline_data = {
            'case_events': [
                {'type': 'complaint_filed', 'date': datetime.now().isoformat()}
            ],
            'jurisdiction': 'Rhode Island',
            'court': 'Superior Court'
        }
        
        response = client.post('/api/court-filing/deadlines',
                             data=json.dumps(deadline_data),
                             content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] == True
        assert 'deadlines' in data
    
    def test_validate_filing(self, client):
        """Test validating a court filing"""
        # First create a filing
        filing_data = {
            'case_id': 'CASE-001',
            'document_type': 'complaint',
            'title': 'Test Complaint',
            'court': 'Superior Court',
            'jurisdiction': 'Rhode Island'
        }
        
        create_response = client.post('/api/court-filing/filings',
                                    data=json.dumps(filing_data),
                                    content_type='application/json')
        filing_id = json.loads(create_response.data)['filing']['id']
        
        # Validate the filing
        response = client.post(f'/api/court-filing/filings/{filing_id}/validate')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] == True
        assert 'is_valid' in data
        assert 'errors' in data

class TestAnalyticsAPI:
    """Test Analytics API endpoints"""
    
    def test_get_user_analytics(self, client):
        """Test getting user analytics"""
        response = client.get('/api/analytics/user')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] == True
        assert 'analytics' in data
    
    def test_get_performance_analytics(self, client):
        """Test getting performance analytics"""
        response = client.get('/api/analytics/performance')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] == True
        assert 'analytics' in data
    
    def test_get_business_analytics(self, client):
        """Test getting business analytics"""
        response = client.get('/api/analytics/business')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] == True
        assert 'analytics' in data
    
    def test_get_security_analytics(self, client):
        """Test getting security analytics"""
        response = client.get('/api/analytics/security')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] == True
        assert 'analytics' in data
    
    def test_get_health_score(self, client):
        """Test getting system health score"""
        response = client.get('/api/analytics/health')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] == True
        assert 'health_score' in data
        assert 0 <= data['health_score'] <= 100

class TestDocumentCollaborationAPI:
    """Test Document Collaboration API endpoints"""
    
    def test_get_documents(self, client):
        """Test getting documents"""
        response = client.get('/api/documents')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] == True
        assert 'documents' in data
    
    def test_create_document(self, client):
        """Test creating a document"""
        document_data = {
            'title': 'Test Document',
            'content': 'This is test content',
            'type': 'legal_brief'
        }
        
        response = client.post('/api/documents',
                             data=json.dumps(document_data),
                             content_type='application/json')
        
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['success'] == True
        assert 'document' in data
        assert data['document']['title'] == 'Test Document'
    
    def test_update_document(self, client):
        """Test updating a document"""
        # First create a document
        document_data = {
            'title': 'Test Document',
            'content': 'Original content',
            'type': 'legal_brief'
        }
        
        create_response = client.post('/api/documents',
                                    data=json.dumps(document_data),
                                    content_type='application/json')
        doc_id = json.loads(create_response.data)['document']['id']
        
        # Update the document
        update_data = {
            'content': 'Updated content',
            'version': 2
        }
        
        response = client.put(f'/api/documents/{doc_id}',
                            data=json.dumps(update_data),
                            content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] == True
        assert data['document']['content'] == 'Updated content'

class TestWebSocketEndpoints:
    """Test WebSocket-related endpoints"""
    
    def test_websocket_status(self, client):
        """Test WebSocket status endpoint"""
        response = client.get('/api/websocket/status')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'websocket_available' in data
    
    def test_send_notification(self, client):
        """Test sending notification via WebSocket"""
        notification_data = {
            'message': 'Test notification',
            'type': 'info',
            'user_id': 'test_user'
        }
        
        response = client.post('/api/notifications/send',
                             data=json.dumps(notification_data),
                             content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] == True
    
    def test_send_case_update(self, client):
        """Test sending case update via WebSocket"""
        update_data = {
            'case_id': 'CASE-001',
            'update_type': 'status_change',
            'new_status': 'In Progress',
            'user_id': 'test_user'
        }
        
        response = client.post('/api/case-updates/send',
                             data=json.dumps(update_data),
                             content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] == True

class TestHealthCheck:
    """Test health check endpoints"""
    
    def test_health_check(self, client):
        """Test main health check endpoint"""
        response = client.get('/health')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'healthy'
        assert 'services' in data
    
    def test_legal_ai_health(self, client):
        """Test legal AI health check"""
        response = client.get('/health/legal-ai')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'status' in data

class TestErrorHandling:
    """Test error handling across APIs"""
    
    def test_invalid_json(self, client):
        """Test handling invalid JSON"""
        response = client.post('/api/immigration/cases',
                             data='invalid json',
                             content_type='application/json')
        
        assert response.status_code == 400
    
    def test_missing_endpoint(self, client):
        """Test 404 handling"""
        response = client.get('/api/nonexistent-endpoint')
        assert response.status_code == 404
    
    def test_method_not_allowed(self, client):
        """Test 405 handling"""
        response = client.delete('/api/immigration/cases')
        assert response.status_code == 405

# Integration Tests
class TestIntegration:
    """Integration tests for complete workflows"""
    
    def test_immigration_case_workflow(self, client):
        """Test complete immigration case workflow"""
        # 1. Create a case
        case_data = {
            'clientName': 'Jane Smith',
            'caseType': 'Green Card',
            'status': 'New',
            'priority': 'High'
        }
        
        create_response = client.post('/api/immigration/cases',
                                    data=json.dumps(case_data),
                                    content_type='application/json')
        assert create_response.status_code == 201
        case_id = json.loads(create_response.data)['case']['id']
        
        # 2. Update the case
        update_data = {'status': 'In Progress'}
        update_response = client.put(f'/api/immigration/cases/{case_id}',
                                   data=json.dumps(update_data),
                                   content_type='application/json')
        assert update_response.status_code == 200
        
        # 3. Get updated case
        get_response = client.get(f'/api/immigration/cases/{case_id}')
        assert get_response.status_code == 200
        case = json.loads(get_response.data)['case']
        assert case['status'] == 'In Progress'
        
        # 4. Delete the case
        delete_response = client.delete(f'/api/immigration/cases/{case_id}')
        assert delete_response.status_code == 200
    
    def test_court_filing_workflow(self, client):
        """Test complete court filing workflow"""
        # 1. Get templates
        templates_response = client.get('/api/court-filing/templates?document_type=complaint')
        assert templates_response.status_code == 200
        templates = json.loads(templates_response.data)['templates']
        
        if templates:
            template_id = templates[0]['id']
            
            # 2. Generate document
            document_data = {
                'template_id': template_id,
                'data': {
                    'plaintiff_name': 'John Doe',
                    'defendant_name': 'Jane Smith',
                    'cause_of_action': 'Breach of Contract'
                }
            }
            
            generate_response = client.post('/api/court-filing/generate',
                                          data=json.dumps(document_data),
                                          content_type='application/json')
            assert generate_response.status_code == 200
            
            # 3. Create filing
            filing_data = {
                'case_id': 'CASE-001',
                'document_type': 'complaint',
                'title': 'Test Complaint',
                'court': 'Superior Court',
                'jurisdiction': 'Rhode Island'
            }
            
            filing_response = client.post('/api/court-filing/filings',
                                        data=json.dumps(filing_data),
                                        content_type='application/json')
            assert filing_response.status_code == 201
            filing_id = json.loads(filing_response.data)['filing']['id']
            
            # 4. Validate filing
            validate_response = client.post(f'/api/court-filing/filings/{filing_id}/validate')
            assert validate_response.status_code == 200

if __name__ == '__main__':
    pytest.main([__file__, '-v'])
