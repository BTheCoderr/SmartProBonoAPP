#!/usr/bin/env python3
"""
Simple test for SmartProBono Agent Integration
Tests basic functionality without external dependencies
"""

import sys
import os

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

def test_imports():
    """Test that we can import all the components"""
    print("🔍 Testing Imports...")
    
    try:
        # Test backend imports
        from backend.services.smartprobono_agent_service import SmartProBonoAgentService
        print("✅ SmartProBono Agent Service imported successfully")
        
        from backend.services.enhanced_ai_service import EnhancedAIService
        print("✅ Enhanced AI Service imported successfully")
        
        # Test model imports
        from backend.models.case import Case
        from backend.models.user import User
        from backend.models.document import Document
        print("✅ Database models imported successfully")
        
        return True
    except Exception as e:
        print(f"❌ Import test failed: {e}")
        return False

def test_agent_initialization():
    """Test agent initialization"""
    print("\n🔍 Testing Agent Initialization...")
    
    try:
        from backend.services.smartprobono_agent_service import SmartProBonoAgentService
        
        agent = SmartProBonoAgentService()
        print(f"✅ Agent initialized successfully")
        print(f"   - Mock mode: {agent.mock_mode}")
        print(f"   - Functions available: {len(agent.available_functions.function_declarations)}")
        
        return True
    except Exception as e:
        print(f"❌ Agent initialization failed: {e}")
        return False

def test_function_schemas():
    """Test function schema creation"""
    print("\n🔍 Testing Function Schemas...")
    
    try:
        from backend.services.smartprobono_agent_service import SmartProBonoAgentService
        
        agent = SmartProBonoAgentService()
        
        # Test a few key schemas
        schemas = agent.available_functions.function_declarations
        schema_names = [schema.name for schema in schemas]
        
        expected_schemas = [
            "create_case",
            "search_cases", 
            "analyze_document",
            "search_case_law",
            "send_notification"
        ]
        
        missing_schemas = [name for name in expected_schemas if name not in schema_names]
        
        if not missing_schemas:
            print("✅ All expected function schemas present")
            print(f"   - Total schemas: {len(schema_names)}")
            print(f"   - Key schemas: {', '.join(expected_schemas)}")
            return True
        else:
            print(f"❌ Missing schemas: {missing_schemas}")
            return False
            
    except Exception as e:
        print(f"❌ Function schemas test failed: {e}")
        return False

def test_enhanced_ai_service():
    """Test enhanced AI service"""
    print("\n🔍 Testing Enhanced AI Service...")
    
    try:
        from backend.services.enhanced_ai_service import EnhancedAIService
        
        enhanced_ai = EnhancedAIService()
        print("✅ Enhanced AI Service initialized successfully")
        
        # Test service status
        status = enhanced_ai.get_service_status()
        print(f"   - Service status: {status}")
        
        return True
    except Exception as e:
        print(f"❌ Enhanced AI Service test failed: {e}")
        return False

def main():
    """Run all simple tests"""
    print("🚀 SmartProBono Agent Simple Integration Tests")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_agent_initialization,
        test_function_schemas,
        test_enhanced_ai_service
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
        print("🎉 All basic tests passed! SmartProBono Agent integration is ready.")
        print("\n📋 Next Steps:")
        print("1. Set up your GEMINI_API_KEY in the backend/.env file")
        print("2. Start your SmartProBono backend server")
        print("3. Test the agent via API endpoints")
        print("4. Integrate the frontend components")
        return True
    else:
        print("⚠️ Some tests failed. Please check the integration.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
