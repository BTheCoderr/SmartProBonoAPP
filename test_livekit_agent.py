#!/usr/bin/env python3
"""
Test script for LiveKit Voice Agent
Tests the agent setup without requiring full LiveKit connection
"""

import os
import sys
from pathlib import Path

# Add current directory to path
sys.path.append(str(Path(__file__).parent))

def test_imports():
    """Test if all required packages are installed"""
    print("🔍 Testing imports...")
    
    try:
        from livekit import agents
        print("✅ livekit.agents imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import livekit.agents: {e}")
        return False
    
    try:
        from livekit.plugins import openai, silero, deepgram
        print("✅ LiveKit plugins imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import LiveKit plugins: {e}")
        return False
    
    try:
        from livekit.agents import function_tool
        print("✅ function_tool imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import function_tool: {e}")
        return False
    
    return True

def test_context_loading():
    """Test context loading function"""
    print("\n📄 Testing context loading...")
    
    try:
        from livekit_voice_agent import load_context, SALES_CONTEXT
        context = load_context()
        
        if len(context) > 100:
            print(f"✅ Context loaded successfully: {len(context)} characters")
            print(f"   Sample: {context[:100]}...")
            return True
        else:
            print("❌ Context seems too short")
            return False
    except Exception as e:
        print(f"❌ Failed to load context: {e}")
        return False

def test_agent_classes():
    """Test agent class definitions"""
    print("\n🤖 Testing agent classes...")
    
    try:
        from livekit_voice_agent import SalesAgent, TechnicalAgent, PricingAgent
        
        # Test that classes can be instantiated (without full initialization)
        print("✅ All agent classes imported successfully")
        print("   • SalesAgent")
        print("   • TechnicalAgent") 
        print("   • PricingAgent")
        return True
    except Exception as e:
        print(f"❌ Failed to import agent classes: {e}")
        return False

def test_api_keys():
    """Test API key configuration"""
    print("\n🔑 Testing API key configuration...")
    
    required_keys = [
        "DEEPGRAM_API_KEY",
        "CEREBRAS_API_KEY", 
        "LIVEKIT_API_KEY",
        "LIVEKIT_API_SECRET",
        "LIVEKIT_WS_URL"
    ]
    
    all_configured = True
    
    for key in required_keys:
        value = os.environ.get(key)
        if value and len(value) > 10:
            print(f"✅ {key}: {value[:10]}...")
        else:
            print(f"❌ {key}: Not configured or too short")
            all_configured = False
    
    return all_configured

def test_context_files():
    """Test context files exist"""
    print("\n📁 Testing context files...")
    
    context_dir = Path("context")
    if not context_dir.exists():
        print("❌ Context directory does not exist")
        return False
    
    products_file = context_dir / "products.json"
    if products_file.exists():
        print("✅ products.json found")
        try:
            content = products_file.read_text()
            if len(content) > 1000:
                print(f"   Content length: {len(content)} characters")
                return True
            else:
                print("❌ products.json seems too short")
                return False
        except Exception as e:
            print(f"❌ Failed to read products.json: {e}")
            return False
    else:
        print("❌ products.json not found")
        return False

def main():
    """Run all tests"""
    print("🧪 LiveKit Voice Agent Test Suite")
    print("=" * 50)
    
    tests = [
        ("Import Test", test_imports),
        ("Context Loading", test_context_loading),
        ("Agent Classes", test_agent_classes),
        ("API Keys", test_api_keys),
        ("Context Files", test_context_files)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔍 Running {test_name}...")
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} PASSED")
            else:
                print(f"❌ {test_name} FAILED")
        except Exception as e:
            print(f"❌ {test_name} ERROR: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! LiveKit Voice Agent is ready to run.")
        print("\n🚀 To start the voice agent:")
        print("   python livekit_voice_agent.py")
        return True
    else:
        print("⚠️ Some tests failed. Please fix the issues before running the voice agent.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
