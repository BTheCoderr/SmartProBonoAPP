#!/usr/bin/env python3
"""
Test script for Claude integration with SmartProBono
"""
import os
import sys
import requests
import json
from datetime import datetime

# Add the backend directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

def test_claude_api_direct():
    """Test Claude API directly"""
    print("🧪 Testing Claude API directly...")
    
    api_key = "sk-ant-api03-ceS1CHfarlcsD_6qtrn8_HeB0G0268TWZN0JgutkdvE-zuJ2Fkptkhr0QIyrVi53ZpjYxV_nRENWdm5A3wX1Q-91CATQAA"
    
    headers = {
        "x-api-key": api_key,
        "Content-Type": "application/json",
        "anthropic-version": "2023-06-01"
    }
    
    payload = {
        "model": "claude-3-5-sonnet-20241022",
        "max_tokens": 500,
        "messages": [
            {
                "role": "user",
                "content": "Hello! Can you help me understand my rights as a tenant facing eviction?"
            }
        ]
    }
    
    try:
        response = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            content = result.get("content", [{}])[0].get("text", "")
            print("✅ Claude API test successful!")
            print(f"📝 Response: {content[:200]}...")
            return True
        else:
            print(f"❌ Claude API test failed: {response.status_code}")
            print(f"Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Claude API test error: {str(e)}")
        return False

def test_enhanced_ai_service():
    """Test the enhanced AI service"""
    print("\n🧪 Testing Enhanced AI Service...")
    
    try:
        from services.enhanced_ai_service import enhanced_ai_service
        
        # Test Claude integration
        response = enhanced_ai_service.generate_legal_response(
            message="I'm being evicted and need to know my rights",
            task_type="chat",
            model="claude"
        )
        
        if response and "response" in response:
            print("✅ Enhanced AI Service test successful!")
            print(f"🤖 Model: {response.get('model_info', {}).get('name', 'Unknown')}")
            print(f"📝 Response: {response['response'][:200]}...")
            return True
        else:
            print("❌ Enhanced AI Service test failed")
            print(f"Response: {response}")
            return False
            
    except Exception as e:
        print(f"❌ Enhanced AI Service test error: {str(e)}")
        return False

def test_available_models():
    """Test getting available models"""
    print("\n🧪 Testing Available Models...")
    
    try:
        from services.enhanced_ai_service import enhanced_ai_service
        
        models = enhanced_ai_service.get_available_models()
        
        print("✅ Available models:")
        for provider, model_list in models.items():
            if model_list:
                print(f"  {provider.upper()}: {', '.join(model_list)}")
            else:
                print(f"  {provider.upper()}: No models available (missing API key)")
        
        return True
        
    except Exception as e:
        print(f"❌ Available models test error: {str(e)}")
        return False

def test_environment_variables():
    """Test environment variable configuration"""
    print("\n🧪 Testing Environment Variables...")
    
    # Set the API key for testing
    os.environ['ANTHROPIC_API_KEY'] = "sk-ant-api03-ceS1CHfarlcsD_6qtrn8_HeB0G0268TWZN0JgutkdvE-zuJ2Fkptkhr0QIyrVi53ZpjYxV_nRENWdm5A3wX1Q-91CATQAA"
    
    try:
        from config.api_keys import ANTHROPIC_API_KEY
        
        if ANTHROPIC_API_KEY:
            print("✅ Anthropic API key loaded successfully")
            print(f"🔑 Key: {ANTHROPIC_API_KEY[:20]}...")
            return True
        else:
            print("❌ Anthropic API key not found")
            return False
            
    except Exception as e:
        print(f"❌ Environment variables test error: {str(e)}")
        return False

def main():
    """Run all tests"""
    print("🚀 SmartProBono Claude Integration Test")
    print("=" * 50)
    
    tests = [
        ("Environment Variables", test_environment_variables),
        ("Claude API Direct", test_claude_api_direct),
        ("Available Models", test_available_models),
        ("Enhanced AI Service", test_enhanced_ai_service)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n📋 Running: {test_name}")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Test failed with exception: {str(e)}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Results Summary:")
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n🎯 Overall: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("🎉 All tests passed! Claude integration is working!")
    else:
        print("⚠️ Some tests failed. Check the errors above.")

if __name__ == "__main__":
    main()
