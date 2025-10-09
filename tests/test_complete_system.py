#!/usr/bin/env python3
"""
Comprehensive System Test Suite
Tests ALL services to ensure zero errors for clients
"""

import unittest
import requests
import json
import sys
import os
from datetime import datetime

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

BASE_URL = "http://localhost:3001"

class TestSystemHealth(unittest.TestCase):
    """Test overall system health"""
    
    def test_main_health(self):
        """Test main system health endpoint"""
        response = requests.get(f"{BASE_URL}/api/health", timeout=10)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['status'], 'healthy')
        self.assertIn('scanner', data['services'])
        self.assertIn('generator', data['services'])
    
    def test_scanner_health(self):
        """Test document scanner health"""
        response = requests.get(f"{BASE_URL}/api/scanner/health", timeout=10)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['service'], 'scanner')
        self.assertEqual(data['status'], 'healthy')
    
    def test_generator_health(self):
        """Test PDF generator health"""
        response = requests.get(f"{BASE_URL}/api/generator/health", timeout=10)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['service'], 'generator')
        self.assertEqual(data['status'], 'healthy')

class TestChatAPI(unittest.TestCase):
    """Test chat AI functionality"""
    
    def test_simple_chat(self):
        """Test simple chat query"""
        response = requests.post(
            f"{BASE_URL}/api/v1/ai/chat",
            json={"message": "Hello", "task_type": "chat"},
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data.get('success'))
        self.assertIsNotNone(data.get('text'))
        self.assertGreater(len(data.get('text', '')), 50)
    
    def test_legal_query(self):
        """Test legal query"""
        response = requests.post(
            f"{BASE_URL}/api/v1/ai/chat",
            json={"message": "What are tenant rights?", "task_type": "legal"},
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data.get('success'))
        self.assertGreater(len(data.get('text', '')), 200)
        # Should NOT contain fallback message
        self.assertNotIn("technical difficulties", data.get('text', '').lower())

class TestMultiAgentSystem(unittest.TestCase):
    """Test multi-agent system"""
    
    def test_agent_list(self):
        """Test getting list of agents"""
        response = requests.get(f"{BASE_URL}/api/multi-agent/agents", timeout=10)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data.get('success'))
        self.assertEqual(data['agents']['total_agents'], 6)
    
    def test_system_status(self):
        """Test multi-agent system status"""
        response = requests.get(f"{BASE_URL}/api/multi-agent/status", timeout=10)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['status'], 'operational')
        self.assertTrue(data['free_models'])
    
    def test_client_support_agent(self):
        """Test client support agent"""
        response = requests.post(
            f"{BASE_URL}/api/multi-agent/client-support",
            json={"question": "What are my rights?"},
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data.get('success'))
        self.assertIn('Client Support Agent', data.get('agent', ''))
    
    def test_document_analysis_agent(self):
        """Test document analysis agent"""
        response = requests.post(
            f"{BASE_URL}/api/multi-agent/document-analysis",
            json={"document": "This is a test contract"},
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data.get('success'))
        self.assertIn('Document Analysis Agent', data.get('agent', ''))
    
    def test_case_management_agent(self):
        """Test case management agent"""
        response = requests.post(
            f"{BASE_URL}/api/multi-agent/case-management",
            json={"task": "Track case deadlines"},
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data.get('success'))
    
    def test_compliance_agent(self):
        """Test compliance agent"""
        response = requests.post(
            f"{BASE_URL}/api/multi-agent/compliance",
            json={"compliance_question": "What are ethical requirements?"},
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data.get('success'))

class TestResponseQuality(unittest.TestCase):
    """Test response quality and content"""
    
    def test_no_fallback_responses(self):
        """Ensure we're not getting fallback responses"""
        response = requests.post(
            f"{BASE_URL}/api/v1/ai/chat",
            json={"message": "What are my rights?", "task_type": "legal"},
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        text = data.get('text', '').lower()
        
        # Should NOT contain these fallback phrases
        fallback_phrases = [
            "technical difficulties",
            "currently unable",
            "research databases",
            "i'm currently experiencing"
        ]
        
        for phrase in fallback_phrases:
            self.assertNotIn(phrase, text, f"Response contains fallback phrase: '{phrase}'")
    
    def test_response_length(self):
        """Test that responses are substantial"""
        response = requests.post(
            f"{BASE_URL}/api/v1/ai/chat",
            json={"message": "Explain tenant rights", "task_type": "legal"},
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        # Should have at least 300 characters for a legal query
        self.assertGreater(len(data.get('text', '')), 300)
    
    def test_response_speed(self):
        """Test that responses are reasonably fast"""
        import time
        start_time = time.time()
        
        response = requests.post(
            f"{BASE_URL}/api/multi-agent/client-support",
            json={"question": "Hello"},
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        elapsed = time.time() - start_time
        self.assertEqual(response.status_code, 200)
        # Should respond within 15 seconds for simple query
        self.assertLess(elapsed, 15, f"Response took {elapsed:.1f} seconds (should be < 15)")

class TestAPIEndpoints(unittest.TestCase):
    """Test all major API endpoints exist"""
    
    def test_ai_chat_endpoint(self):
        """Test AI chat endpoint exists"""
        response = requests.post(
            f"{BASE_URL}/api/v1/ai/chat",
            json={"message": "test"},
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        # Should return 200 or validation error, not 404
        self.assertNotEqual(response.status_code, 404)
    
    def test_multi_agent_endpoints(self):
        """Test multi-agent endpoints exist"""
        endpoints = [
            "/api/multi-agent/status",
            "/api/multi-agent/agents",
        ]
        
        for endpoint in endpoints:
            response = requests.get(f"{BASE_URL}{endpoint}", timeout=10)
            self.assertNotEqual(response.status_code, 404, f"Endpoint {endpoint} not found")
    
    def test_document_endpoints(self):
        """Test document endpoints exist"""
        response = requests.get(f"{BASE_URL}/api/scanner/health", timeout=10)
        self.assertNotEqual(response.status_code, 404)
        
        response = requests.get(f"{BASE_URL}/api/generator/health", timeout=10)
        self.assertNotEqual(response.status_code, 404)

class TestErrorHandling(unittest.TestCase):
    """Test error handling"""
    
    def test_missing_message(self):
        """Test handling of missing message"""
        response = requests.post(
            f"{BASE_URL}/api/v1/ai/chat",
            json={},
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        # Should return 400 bad request, not crash
        self.assertEqual(response.status_code, 400)
    
    def test_invalid_agent(self):
        """Test handling of invalid agent"""
        response = requests.post(
            f"{BASE_URL}/api/multi-agent/process",
            json={"message": "test", "agent_id": "nonexistent_agent"},
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        # Should handle gracefully
        self.assertIn(response.status_code, [200, 400, 404])

def run_tests():
    """Run all tests and generate report"""
    print("🧪 COMPREHENSIVE SYSTEM TEST SUITE")
    print("=" * 60)
    print(f"Testing backend: {BASE_URL}")
    print(f"Timestamp: {datetime.now().isoformat()}")
    print("=" * 60)
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestSystemHealth))
    suite.addTests(loader.loadTestsFromTestCase(TestChatAPI))
    suite.addTests(loader.loadTestsFromTestCase(TestMultiAgentSystem))
    suite.addTests(loader.loadTestsFromTestCase(TestResponseQuality))
    suite.addTests(loader.loadTestsFromTestCase(TestAPIEndpoints))
    suite.addTests(loader.loadTestsFromTestCase(TestErrorHandling))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Generate report
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    print(f"Tests Run: {result.testsRun}")
    print(f"✅ Passed: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"❌ Failed: {len(result.failures)}")
    print(f"⚠️ Errors: {len(result.errors)}")
    
    if result.wasSuccessful():
        print("\n🎉 ALL TESTS PASSED!")
        print("Your system is production-ready with ZERO errors!")
        return 0
    else:
        print("\n⚠️ Some tests failed - review above for details")
        return 1

if __name__ == "__main__":
    sys.exit(run_tests())

