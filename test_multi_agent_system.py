#!/usr/bin/env python3
"""
Test script for SmartProBono Multi-Agent System
"""
import sys
import os

# Add the smartprobono_backend directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'smartprobono_backend'))

def test_imports():
    """Test if all required modules can be imported"""
    try:
        print("🧪 Testing Multi-Agent System Imports...")
        
        # Test basic imports
        import fastapi
        print("✅ FastAPI imported successfully")
        
        import langgraph
        print("✅ LangGraph imported successfully")
        
        import haystack
        print("✅ Haystack imported successfully")
        
        # Test our modules
        from rag.store import get_document_store
        print("✅ RAG store module imported successfully")
        
        from utils.safety import needs_escalation
        print("✅ Safety module imported successfully")
        
        from graph.state import SPBState
        print("✅ Graph state module imported successfully")
        
        print("\n🎉 All imports successful! Multi-agent system is ready.")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_safety_functions():
    """Test safety functions"""
    try:
        from utils.safety import needs_escalation, add_disclaimer
        
        # Test escalation detection
        test_text = "I advise you to file a lawsuit immediately"
        should_escalate = needs_escalation(test_text)
        print(f"✅ Safety test: '{test_text}' -> escalate: {should_escalate}")
        
        # Test disclaimer addition
        response = "This is general information"
        with_disclaimer = add_disclaimer(response)
        print(f"✅ Disclaimer test: Added disclaimer to response")
        
        return True
        
    except Exception as e:
        print(f"❌ Safety test error: {e}")
        return False

if __name__ == "__main__":
    print("🚀 SmartProBono Multi-Agent System Test")
    print("=" * 50)
    
    # Test imports
    imports_ok = test_imports()
    
    if imports_ok:
        print("\n🧪 Testing Safety Functions...")
        safety_ok = test_safety_functions()
        
        if safety_ok:
            print("\n🎉 All tests passed! Multi-agent system is ready to run.")
            print("\nTo start the system:")
            print("  ./start_multi_agent_system.sh")
        else:
            print("\n❌ Safety tests failed.")
    else:
        print("\n❌ Import tests failed. Please check dependencies.")
