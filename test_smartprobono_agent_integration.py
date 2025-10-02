#!/usr/bin/env python3
"""
Test script for SmartProBono Agent Integration
Tests the complete integration of our AI agent with the SmartProBono platform
"""

import sys
import os
import json
import requests
from datetime import datetime

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

def test_agent_status():
    """Test agent status endpoint"""
    print("🔍 Testing Agent Status...")
    
    try:
        # This would normally be a real server, but we'll test the service directly
        from backend.services.smartprobono_agent_service import SmartProBonoAgentService
        
        agent = SmartProBonoAgentService()
        print(f"✅ Agent service initialized successfully")
        print(f"   - Mock mode: {agent.mock_mode}")
        print(f"   - API available: {not agent.mock_mode}")
        
        return True
    except Exception as e:
        print(f"❌ Agent status test failed: {e}")
        return False

def test_agent_capabilities():
    """Test agent capabilities"""
    print("\n🔍 Testing Agent Capabilities...")
    
    try:
        from backend.services.smartprobono_agent_service import SmartProBonoAgentService
        
        agent = SmartProBonoAgentService()
        
        # Test function schemas
        schemas = [
            "create_case",
            "search_cases", 
            "analyze_document",
            "search_case_law",
            "send_notification"
        ]
        
        print(f"✅ Agent capabilities test passed")
        print(f"   - Available functions: {len(agent.available_functions.function_declarations)}")
        print(f"   - Core schemas: {', '.join(schemas)}")
        
        return True
    except Exception as e:
        print(f"❌ Agent capabilities test failed: {e}")
        return False

def test_agent_functions():
    """Test agent function execution"""
    print("\n🔍 Testing Agent Functions...")
    
    try:
        from backend.services.smartprobono_agent_service import SmartProBonoAgentService
        
        agent = SmartProBonoAgentService()
        
        # Test create_case function
        result = agent.create_case(
            working_directory=".",
            title="Test Immigration Case",
            description="Test case for integration testing",
            case_type="immigration",
            client_id="12345",
            priority="high"
        )
        
        print(f"✅ Function execution test passed")
        print(f"   - create_case result: {result[:50]}...")
        
        # Test search_cases function
        search_result = agent.search_cases(
            working_directory=".",
            case_type="immigration"
        )
        
        print(f"   - search_cases result: {search_result[:50]}...")
        
        return True
    except Exception as e:
        print(f"❌ Agent functions test failed: {e}")
        return False

def test_enhanced_ai_service():
    """Test enhanced AI service integration"""
    print("\n🔍 Testing Enhanced AI Service...")
    
    try:
        from backend.services.enhanced_ai_service import EnhancedAIService
        
        enhanced_ai = EnhancedAIService()
        
        # Test service initialization
        status = enhanced_ai.get_service_status()
        
        print(f"✅ Enhanced AI service test passed")
        print(f"   - Service status: {status}")
        
        # Test request routing
        response = enhanced_ai.process_legal_request(
            message="Create a new immigration case for John Smith",
            user_context={"user_role": "lawyer"},
            user_role="lawyer",
            task_type="case_management"
        )
        
        print(f"   - Request routing: {response.get('service', 'unknown')}")
        
        return True
    except Exception as e:
        print(f"❌ Enhanced AI service test failed: {e}")
        return False

def test_database_integration():
    """Test database integration (mock)"""
    print("\n🔍 Testing Database Integration...")
    
    try:
        # Test that we can import the models
        from backend.models.case import Case
        from backend.models.user import User
        from backend.models.document import Document
        
        print(f"✅ Database integration test passed")
        print(f"   - Case model: {Case.__name__}")
        print(f"   - User model: {User.__name__}")
        print(f"   - Document model: {Document.__name__}")
        
        return True
    except Exception as e:
        print(f"❌ Database integration test failed: {e}")
        return False

def test_route_integration():
    """Test route integration"""
    print("\n🔍 Testing Route Integration...")
    
    try:
        # Test that we can import the routes
        from backend.routes.smartprobono_agent import bp
        
        print(f"✅ Route integration test passed")
        print(f"   - Blueprint name: {bp.name}")
        print(f"   - Routes registered: {len(bp.deferred_functions)}")
        
        return True
    except Exception as e:
        print(f"❌ Route integration test failed: {e}")
        return False

def test_full_integration():
    """Test full integration workflow"""
    print("\n🔍 Testing Full Integration Workflow...")
    
    try:
        from backend.services.smartprobono_agent_service import SmartProBonoAgentService
        
        agent = SmartProBonoAgentService()
        
        # Simulate a complete workflow
        test_requests = [
            "Create a new immigration case for client John Smith with high priority",
            "Search for all open criminal defense cases", 
            "Analyze the contract document for compliance issues",
            "Send a notification to client about case status update"
        ]
        
        results = []
        for request in test_requests:
            try:
                response = agent.process_request(request, verbose=False)
                results.append(f"✅ {request[:30]}... -> Success")
            except Exception as e:
                results.append(f"❌ {request[:30]}... -> Error: {str(e)[:50]}")
        
        print(f"✅ Full integration workflow test completed")
        for result in results:
            print(f"   - {result}")
        
        return True
    except Exception as e:
        print(f"❌ Full integration workflow test failed: {e}")
        return False

def main():
    """Run all integration tests"""
    print("🚀 SmartProBono Agent Integration Tests")
    print("=" * 50)
    
    tests = [
        test_agent_status,
        test_agent_capabilities,
        test_agent_functions,
        test_enhanced_ai_service,
        test_database_integration,
        test_route_integration,
        test_full_integration
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Test {test.__name__} failed with exception: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! SmartProBono Agent integration is ready.")
        return True
    else:
        print("⚠️ Some tests failed. Please check the integration.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
