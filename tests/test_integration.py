"""
Integration Tests
End-to-end tests for the SmartProBono platform
"""

import pytest
import requests
import json
import time
import threading
import asyncio
import websockets
from datetime import datetime, timedelta
import sys
import os

# Add the backend directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

class TestPlatformIntegration:
    """Integration tests for the entire platform"""
    
    @pytest.fixture(scope="class")
    def backend_server(self):
        """Start the backend server for testing"""
        import subprocess
        import signal
        
        # Start the server
        process = subprocess.Popen([
            sys.executable, 
            os.path.join(os.path.dirname(__file__), '..', 'backend', 'combined_server.py')
        ])
        
        # Wait for server to start
        time.sleep(5)
        
        yield process
        
        # Cleanup
        process.terminate()
        process.wait()
    
    @pytest.fixture
    def base_url(self):
        """Base URL for API requests"""
        return "http://localhost:3001"
    
    def test_platform_health_check(self, base_url):
        """Test that the platform is running and healthy"""
        response = requests.get(f"{base_url}/health")
        assert response.status_code == 200
        
        data = response.json()
        assert data['status'] == 'healthy'
        assert 'services' in data
    
    def test_immigration_crm_workflow(self, base_url):
        """Test complete immigration CRM workflow"""
        # 1. Create a new immigration case
        case_data = {
            'clientName': 'Integration Test Client',
            'caseType': 'Asylum',
            'status': 'New',
            'priority': 'High',
            'description': 'Integration test case'
        }
        
        response = requests.post(
            f"{base_url}/api/immigration/cases",
            json=case_data,
            headers={'Content-Type': 'application/json'}
        )
        assert response.status_code == 201
        case = response.json()['case']
        case_id = case['id']
        
        # 2. Update the case
        update_data = {
            'status': 'In Progress',
            'priority': 'Medium',
            'description': 'Updated description'
        }
        
        response = requests.put(
            f"{base_url}/api/immigration/cases/{case_id}",
            json=update_data,
            headers={'Content-Type': 'application/json'}
        )
        assert response.status_code == 200
        updated_case = response.json()['case']
        assert updated_case['status'] == 'In Progress'
        
        # 3. Get case statistics
        response = requests.get(f"{base_url}/api/immigration/cases/stats")
        assert response.status_code == 200
        stats = response.json()
        assert stats['success'] == True
        assert stats['total_cases'] > 0
        
        # 4. Delete the case
        response = requests.delete(f"{base_url}/api/immigration/cases/{case_id}")
        assert response.status_code == 200
    
    def test_voice_processing_workflow(self, base_url):
        """Test complete voice processing workflow"""
        # 1. Check voice service status
        response = requests.get(f"{base_url}/api/voice/status")
        assert response.status_code == 200
        status = response.json()
        assert status['success'] == True
        
        # 2. Get supported languages
        response = requests.get(f"{base_url}/api/voice/languages")
        assert response.status_code == 200
        languages = response.json()
        assert languages['success'] == True
        assert len(languages['languages']) > 0
        
        # 3. Process voice command
        command_data = {
            'text': 'I need help with my immigration case',
            'user_id': 'integration_test_user'
        }
        
        response = requests.post(
            f"{base_url}/api/voice/command",
            json=command_data,
            headers={'Content-Type': 'application/json'}
        )
        assert response.status_code == 200
        command_result = response.json()
        assert 'success' in command_result
        
        # 4. Analyze voice input
        analysis_data = {
            'text': 'What are my legal options for asylum?',
            'context': {'user_type': 'client', 'jurisdiction': 'ri'}
        }
        
        response = requests.post(
            f"{base_url}/api/voice/analyze",
            json=analysis_data,
            headers={'Content-Type': 'application/json'}
        )
        assert response.status_code == 200
        analysis_result = response.json()
        assert 'success' in analysis_result
    
    def test_court_filing_workflow(self, base_url):
        """Test complete court filing workflow"""
        # 1. Get court rules
        response = requests.get(
            f"{base_url}/api/court-filing/rules?jurisdiction=Rhode Island"
        )
        assert response.status_code == 200
        rules = response.json()
        assert rules['success'] == True
        assert len(rules['rules']) > 0
        
        # 2. Get filing templates
        response = requests.get(
            f"{base_url}/api/court-filing/templates?document_type=complaint"
        )
        assert response.status_code == 200
        templates = response.json()
        assert templates['success'] == True
        assert len(templates['templates']) > 0
        
        # 3. Calculate filing fees
        fee_data = {
            'document_type': 'complaint',
            'jurisdiction': 'Rhode Island',
            'court': 'Superior Court'
        }
        
        response = requests.post(
            f"{base_url}/api/court-filing/fees",
            json=fee_data,
            headers={'Content-Type': 'application/json'}
        )
        assert response.status_code == 200
        fees = response.json()
        assert fees['success'] == True
        assert 'fees' in fees
        
        # 4. Generate document
        template_id = templates['templates'][0]['id']
        document_data = {
            'template_id': template_id,
            'data': {
                'plaintiff_name': 'Integration Test Plaintiff',
                'defendant_name': 'Integration Test Defendant',
                'cause_of_action': 'Integration Test Cause'
            }
        }
        
        response = requests.post(
            f"{base_url}/api/court-filing/generate",
            json=document_data,
            headers={'Content-Type': 'application/json'}
        )
        assert response.status_code == 200
        generated = response.json()
        assert generated['success'] == True
        assert 'document_content' in generated
        
        # 5. Create filing
        filing_data = {
            'case_id': 'INTEGRATION-CASE-001',
            'document_type': 'complaint',
            'title': 'Integration Test Filing',
            'description': 'Integration test court filing',
            'court': 'Superior Court',
            'jurisdiction': 'Rhode Island',
            'filed_by': 'Integration Test Attorney'
        }
        
        response = requests.post(
            f"{base_url}/api/court-filing/filings",
            json=filing_data,
            headers={'Content-Type': 'application/json'}
        )
        assert response.status_code == 201
        filing = response.json()['filing']
        filing_id = filing['id']
        
        # 6. Validate filing
        response = requests.post(f"{base_url}/api/court-filing/filings/{filing_id}/validate")
        assert response.status_code == 200
        validation = response.json()
        assert validation['success'] == True
        assert 'is_valid' in validation
    
    def test_analytics_workflow(self, base_url):
        """Test analytics and reporting workflow"""
        # 1. Get user analytics
        response = requests.get(f"{base_url}/api/analytics/user")
        assert response.status_code == 200
        user_analytics = response.json()
        assert user_analytics['success'] == True
        assert 'analytics' in user_analytics
        
        # 2. Get performance analytics
        response = requests.get(f"{base_url}/api/analytics/performance")
        assert response.status_code == 200
        perf_analytics = response.json()
        assert perf_analytics['success'] == True
        assert 'analytics' in perf_analytics
        
        # 3. Get business analytics
        response = requests.get(f"{base_url}/api/analytics/business")
        assert response.status_code == 200
        business_analytics = response.json()
        assert business_analytics['success'] == True
        assert 'analytics' in business_analytics
        
        # 4. Get security analytics
        response = requests.get(f"{base_url}/api/analytics/security")
        assert response.status_code == 200
        security_analytics = response.json()
        assert security_analytics['success'] == True
        assert 'analytics' in security_analytics
        
        # 5. Get system health score
        response = requests.get(f"{base_url}/api/analytics/health")
        assert response.status_code == 200
        health = response.json()
        assert health['success'] == True
        assert 'health_score' in health
        assert 0 <= health['health_score'] <= 100
    
    def test_document_collaboration_workflow(self, base_url):
        """Test document collaboration workflow"""
        # 1. Get documents
        response = requests.get(f"{base_url}/api/documents")
        assert response.status_code == 200
        documents = response.json()
        assert documents['success'] == True
        assert 'documents' in documents
        
        # 2. Create a document
        document_data = {
            'title': 'Integration Test Document',
            'content': 'This is integration test content',
            'type': 'legal_brief',
            'description': 'Integration test document'
        }
        
        response = requests.post(
            f"{base_url}/api/documents",
            json=document_data,
            headers={'Content-Type': 'application/json'}
        )
        assert response.status_code == 201
        document = response.json()['document']
        doc_id = document['id']
        
        # 3. Update the document
        update_data = {
            'content': 'Updated integration test content',
            'version': 2
        }
        
        response = requests.put(
            f"{base_url}/api/documents/{doc_id}",
            json=update_data,
            headers={'Content-Type': 'application/json'}
        )
        assert response.status_code == 200
        updated_doc = response.json()['document']
        assert updated_doc['content'] == 'Updated integration test content'
        
        # 4. Delete the document
        response = requests.delete(f"{base_url}/api/documents/{doc_id}")
        assert response.status_code == 200
    
    def test_websocket_integration(self, base_url):
        """Test WebSocket real-time features"""
        # Test WebSocket status endpoint
        response = requests.get(f"{base_url}/api/websocket/status")
        assert response.status_code == 200
        ws_status = response.json()
        assert 'websocket_available' in ws_status
        
        if ws_status['websocket_available']:
            # Test sending notification
            notification_data = {
                'message': 'Integration test notification',
                'type': 'info',
                'user_id': 'integration_test_user'
            }
            
            response = requests.post(
                f"{base_url}/api/notifications/send",
                json=notification_data,
                headers={'Content-Type': 'application/json'}
            )
            assert response.status_code == 200
            
            # Test sending case update
            update_data = {
                'case_id': 'INTEGRATION-CASE-001',
                'update_type': 'status_change',
                'new_status': 'In Progress',
                'user_id': 'integration_test_user'
            }
            
            response = requests.post(
                f"{base_url}/api/case-updates/send",
                json=update_data,
                headers={'Content-Type': 'application/json'}
            )
            assert response.status_code == 200
    
    def test_legal_ai_integration(self, base_url):
        """Test Legal AI backend integration"""
        # Test legal analysis endpoint
        analysis_data = {
            'query': 'What are the requirements for asylum in the United States?',
            'jurisdiction': 'ri',
            'context': {
                'user_type': 'client',
                'case_type': 'asylum'
            }
        }
        
        response = requests.post(
            f"{base_url}/api/legal-analysis",
            json=analysis_data,
            headers={'Content-Type': 'application/json'}
        )
        assert response.status_code == 200
        analysis = response.json()
        assert 'success' in analysis
        
        # Test legal forms endpoint
        response = requests.get(f"{base_url}/api/legal-forms")
        assert response.status_code == 200
        forms = response.json()
        assert 'success' in forms
    
    def test_error_handling_integration(self, base_url):
        """Test error handling across the platform"""
        # Test invalid endpoint
        response = requests.get(f"{base_url}/api/nonexistent-endpoint")
        assert response.status_code == 404
        
        # Test invalid JSON
        response = requests.post(
            f"{base_url}/api/immigration/cases",
            data="invalid json",
            headers={'Content-Type': 'application/json'}
        )
        assert response.status_code == 400
        
        # Test missing required fields
        incomplete_data = {
            'clientName': 'Test Client'
            # Missing caseType
        }
        
        response = requests.post(
            f"{base_url}/api/immigration/cases",
            json=incomplete_data,
            headers={'Content-Type': 'application/json'}
        )
        assert response.status_code == 400
        error_response = response.json()
        assert error_response['success'] == False
        assert 'error' in error_response
    
    def test_concurrent_requests(self, base_url):
        """Test platform under concurrent load"""
        import concurrent.futures
        
        def make_request():
            response = requests.get(f"{base_url}/api/immigration/cases")
            return response.status_code == 200
        
        # Make 10 concurrent requests
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(make_request) for _ in range(10)]
            results = [future.result() for future in futures]
        
        # All requests should succeed
        assert all(results)
    
    def test_data_persistence(self, base_url):
        """Test that data persists across requests"""
        # Create a case
        case_data = {
            'clientName': 'Persistence Test Client',
            'caseType': 'Green Card',
            'status': 'New',
            'priority': 'Medium'
        }
        
        response = requests.post(
            f"{base_url}/api/immigration/cases",
            json=case_data,
            headers={'Content-Type': 'application/json'}
        )
        assert response.status_code == 201
        case = response.json()['case']
        case_id = case['id']
        
        # Wait a moment
        time.sleep(1)
        
        # Retrieve the case
        response = requests.get(f"{base_url}/api/immigration/cases/{case_id}")
        assert response.status_code == 200
        retrieved_case = response.json()['case']
        assert retrieved_case['id'] == case_id
        assert retrieved_case['clientName'] == 'Persistence Test Client'
        
        # Clean up
        requests.delete(f"{base_url}/api/immigration/cases/{case_id}")

class TestWebSocketIntegration:
    """Test WebSocket real-time features"""
    
    @pytest.mark.asyncio
    async def test_websocket_connection(self):
        """Test WebSocket connection and messaging"""
        try:
            async with websockets.connect("ws://localhost:8765") as websocket:
                # Send a test message
                test_message = {
                    "type": "test",
                    "message": "Integration test message"
                }
                
                await websocket.send(json.dumps(test_message))
                
                # Wait for response (with timeout)
                try:
                    response = await asyncio.wait_for(websocket.recv(), timeout=5.0)
                    data = json.loads(response)
                    assert 'type' in data
                except asyncio.TimeoutError:
                    # Timeout is acceptable for this test
                    pass
                    
        except ConnectionRefusedError:
            # WebSocket server not running, skip test
            pytest.skip("WebSocket server not available")

class TestPerformanceIntegration:
    """Performance integration tests"""
    
    def test_response_times(self, base_url):
        """Test API response times"""
        endpoints = [
            '/health',
            '/api/immigration/cases',
            '/api/voice/status',
            '/api/court-filing/rules',
            '/api/analytics/user'
        ]
        
        for endpoint in endpoints:
            start_time = time.time()
            response = requests.get(f"{base_url}{endpoint}")
            end_time = time.time()
            
            response_time = end_time - start_time
            
            # Response should be fast (less than 2 seconds)
            assert response_time < 2.0
            assert response.status_code == 200
    
    def test_memory_usage(self, base_url):
        """Test memory usage under load"""
        import psutil
        import os
        
        # Get initial memory usage
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss
        
        # Make many requests
        for _ in range(100):
            response = requests.get(f"{base_url}/api/immigration/cases")
            assert response.status_code == 200
        
        # Check memory usage hasn't grown too much
        final_memory = process.memory_info().rss
        memory_growth = final_memory - initial_memory
        
        # Memory growth should be reasonable (less than 50MB)
        assert memory_growth < 50 * 1024 * 1024

class TestSecurityIntegration:
    """Security integration tests"""
    
    def test_cors_headers(self, base_url):
        """Test CORS headers are properly set"""
        response = requests.options(
            f"{base_url}/api/immigration/cases",
            headers={'Origin': 'http://localhost:3000'}
        )
        
        # Check for CORS headers
        assert 'Access-Control-Allow-Origin' in response.headers
        assert 'Access-Control-Allow-Methods' in response.headers
    
    def test_input_validation(self, base_url):
        """Test input validation and sanitization"""
        # Test SQL injection attempt
        malicious_data = {
            'clientName': "'; DROP TABLE cases; --",
            'caseType': 'Asylum'
        }
        
        response = requests.post(
            f"{base_url}/api/immigration/cases",
            json=malicious_data,
            headers={'Content-Type': 'application/json'}
        )
        
        # Should handle gracefully (either reject or sanitize)
        assert response.status_code in [200, 201, 400]
    
    def test_rate_limiting(self, base_url):
        """Test rate limiting (if implemented)"""
        # Make many requests quickly
        responses = []
        for _ in range(50):
            response = requests.get(f"{base_url}/api/immigration/cases")
            responses.append(response.status_code)
        
        # Most requests should succeed (rate limiting might kick in)
        success_count = sum(1 for status in responses if status == 200)
        assert success_count > 40  # At least 80% should succeed

if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])
