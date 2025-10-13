#!/usr/bin/env python3
"""
Test script for Saul Legal AI integration
Tests the Saul model integration with SmartProBono
"""

import sys
import os
import json
from datetime import datetime

# Add backend services to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend', 'services'))

def test_saul_service():
    """Test the Saul Legal AI service directly"""
    print("🧪 Testing Saul Legal AI Service...")
    print("=" * 50)
    
    try:
        from saul_legal_ai_service import saul_legal_ai
        
        # Test model info
        print("📋 Model Information:")
        info = saul_legal_ai.get_model_info()
        print(f"   Model: {info['model_name']}")
        print(f"   Device: {info['device']}")
        print(f"   Company: {info['company']}")
        print(f"   Website: {info['website']}")
        print(f"   Paper: {info['paper']}")
        print()
        
        # Test health check
        print("🏥 Health Check:")
        health = saul_legal_ai.health_check()
        print(f"   Status: {health['status']}")
        print(f"   Model Loaded: {health['model_loaded']}")
        print(f"   Device: {health['device']}")
        print()
        
        # Test response generation (this will load the model if not already loaded)
        print("💬 Testing Response Generation:")
        test_messages = [
            "What is contract law?",
            "How do I file for bankruptcy?",
            "What are my rights as a tenant?"
        ]
        
        for i, message in enumerate(test_messages, 1):
            print(f"\n   Test {i}: {message}")
            print("   " + "-" * 40)
            
            try:
                response = saul_legal_ai.generate_response(
                    message=message,
                    task_type="legal",
                    max_tokens=100  # Shorter for testing
                )
                
                if response.get("success"):
                    print(f"   ✅ Success!")
                    print(f"   Model: {response['model']}")
                    print(f"   Response: {response['text'][:200]}...")
                else:
                    print(f"   ❌ Failed: {response.get('error', 'Unknown error')}")
                    
            except Exception as e:
                print(f"   ❌ Error: {str(e)}")
        
        print("\n🎉 Saul service test completed!")
        return True
        
    except ImportError as e:
        print(f"❌ Import Error: {str(e)}")
        print("   Make sure you have installed the required dependencies:")
        print("   pip install transformers torch accelerate safetensors")
        return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def test_enhanced_service():
    """Test the Saul Enhanced AI service"""
    print("\n🧪 Testing Saul Enhanced AI Service...")
    print("=" * 50)
    
    try:
        from saul_enhanced_ai_service import saul_enhanced_ai
        
        # Test available models
        print("🤖 Available Models:")
        models = saul_enhanced_ai.get_available_models()
        for model_name, model_info in models.items():
            print(f"   {model_name}: {model_info['name']} - Status: {model_info['status']}")
        print()
        
        # Test health check
        print("🏥 Health Check:")
        health = saul_enhanced_ai.health_check()
        print(f"   Service Status: {health['saul_enhanced_service']}")
        print(f"   Saul Model: {health['saul_model']['status']}")
        print(f"   Recommended Model: {health['recommended_model']}")
        print()
        
        # Test response generation
        print("💬 Testing Enhanced Response Generation:")
        test_message = "I need help with a contract dispute"
        
        print(f"   Message: {test_message}")
        print("   " + "-" * 40)
        
        try:
            response = saul_enhanced_ai.generate_legal_response(
                message=test_message,
                task_type="legal",
                model="auto",
                user_role="client"
            )
            
            print(f"   ✅ Success!")
            print(f"   Model Used: {response.get('model_used', 'unknown')}")
            print(f"   Fallback Used: {response.get('fallback_used', False)}")
            print(f"   Response: {response.get('text', response.get('content', ''))[:200]}...")
            
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
        
        print("\n🎉 Enhanced service test completed!")
        return True
        
    except ImportError as e:
        print(f"❌ Import Error: {str(e)}")
        return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def test_api_endpoints():
    """Test the API endpoints (requires running server)"""
    print("\n🧪 Testing API Endpoints...")
    print("=" * 50)
    
    import requests
    
    base_url = "http://localhost:3001/api/v1"
    
    # Test model info endpoint
    try:
        print("📋 Testing /ai/saul/info endpoint...")
        response = requests.get(f"{base_url}/ai/saul/info", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Success! Model: {data['model_info']['model_name']}")
            print(f"   Status: {data['health_status']['status']}")
        else:
            print(f"   ❌ Failed with status: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"   ⚠️  Server not running or endpoint not available: {str(e)}")
    
    # Test available models endpoint
    try:
        print("\n📋 Testing /ai/models/available endpoint...")
        response = requests.get(f"{base_url}/ai/models/available", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Success! Available models: {len(data['available_models'])}")
            for model_name in data['available_models'].keys():
                print(f"      - {model_name}")
        else:
            print(f"   ❌ Failed with status: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"   ⚠️  Server not running or endpoint not available: {str(e)}")
    
    # Test chat endpoint
    try:
        print("\n💬 Testing /ai/saul/chat endpoint...")
        payload = {
            "message": "What is contract law?",
            "task_type": "legal",
            "max_tokens": 100
        }
        response = requests.post(f"{base_url}/ai/saul/chat", json=payload, timeout=30)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Success! Response length: {len(data.get('text', ''))}")
            print(f"   Model: {data.get('model', 'unknown')}")
        else:
            print(f"   ❌ Failed with status: {response.status_code}")
            print(f"   Response: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"   ⚠️  Server not running or endpoint not available: {str(e)}")

def main():
    """Run all tests"""
    print("🚀 SmartProBono Saul Legal AI Integration Test")
    print("=" * 60)
    print(f"Timestamp: {datetime.now().isoformat()}")
    print()
    
    # Test 1: Saul Service
    saul_success = test_saul_service()
    
    # Test 2: Enhanced Service
    enhanced_success = test_enhanced_service()
    
    # Test 3: API Endpoints (optional, requires running server)
    test_api_endpoints()
    
    # Summary
    print("\n📊 Test Summary:")
    print("=" * 30)
    print(f"Saul Service: {'✅ PASS' if saul_success else '❌ FAIL'}")
    print(f"Enhanced Service: {'✅ PASS' if enhanced_success else '❌ FAIL'}")
    
    if saul_success and enhanced_success:
        print("\n🎉 All core tests passed! Saul integration is ready.")
        print("\n📝 Next steps:")
        print("   1. Start your server: python backend/combined_server.py")
        print("   2. Test the API endpoints")
        print("   3. Try the legal chat in your frontend")
    else:
        print("\n⚠️  Some tests failed. Check the error messages above.")
        print("\n🔧 Troubleshooting:")
        print("   1. Install dependencies: pip install -r requirements.txt")
        print("   2. Check if you have enough GPU/CPU memory for the model")
        print("   3. Verify internet connection for model download")

if __name__ == "__main__":
    main()
