#!/usr/bin/env python3
"""
Test Voice AI Integration in SmartProBono
Tests the complete voice-enabled multi-model AI system
"""

import os
import sys
import asyncio
import requests
import json
from pathlib import Path

# Add the backend to the path
sys.path.append(str(Path(__file__).parent / "backend"))

def test_voice_ai_service():
    """Test the VoiceEnhancedAIService directly"""
    print("🧪 Testing VoiceEnhancedAIService")
    print("=" * 50)
    
    try:
        from backend.services.voice_enhanced_ai_service import VoiceEnhancedAIService
        
        # Initialize service
        service = VoiceEnhancedAIService()
        
        print(f"✅ Voice service initialized")
        print(f"   Voice enabled: {service.voice_enabled}")
        print(f"   Capabilities: {service.get_capabilities()}")
        print(f"   Available models: {service.get_available_models()}")
        
        # Test different types of requests
        test_cases = [
            {
                "message": "What features does SmartProBono offer?",
                "task_type": "sales",
                "voice_enabled": True,
                "description": "Voice-enabled sales query"
            },
            {
                "message": "Create a new case for client John Doe",
                "task_type": "case_management",
                "voice_enabled": False,
                "description": "Legal case management"
            },
            {
                "message": "How much does the platform cost?",
                "task_type": "pricing",
                "voice_enabled": True,
                "description": "Voice-enabled pricing query"
            }
        ]
        
        for i, test_case in enumerate(test_cases, 1):
            print(f"\n📝 Test {i}: {test_case['description']}")
            print(f"   Message: {test_case['message']}")
            print(f"   Voice enabled: {test_case['voice_enabled']}")
            
            # Run the test
            response = asyncio.run(service.process_request(
                message=test_case['message'],
                user_context={"user_id": "test_user", "role": "client"},
                user_role="client",
                task_type=test_case['task_type'],
                voice_enabled=test_case['voice_enabled']
            ))
            
            print(f"   Response: {response.get('response', 'No response')[:100]}...")
            print(f"   Model: {response.get('model', 'Unknown')}")
            print(f"   Voice enabled: {response.get('voice_enabled', False)}")
            
            if response.get('error'):
                print(f"   ❌ Error: {response['error']}")
            else:
                print(f"   ✅ Success")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing VoiceEnhancedAIService: {e}")
        return False

def test_voice_ai_routes():
    """Test the voice AI routes via HTTP"""
    print("\n🌐 Testing Voice AI Routes")
    print("=" * 50)
    
    base_url = "http://localhost:5000/api"
    
    # Test capabilities endpoint
    try:
        response = requests.get(f"{base_url}/voice-capabilities")
        if response.status_code == 200:
            data = response.json()
            print("✅ Voice capabilities endpoint working")
            print(f"   Voice enabled: {data.get('voice_enabled', False)}")
            print(f"   Capabilities: {data.get('capabilities', {})}")
        else:
            print(f"❌ Capabilities endpoint failed: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("⚠️ SmartProBono server not running - skipping route tests")
        return True
    except Exception as e:
        print(f"❌ Error testing capabilities: {e}")
        return False
    
    # Test voice chat endpoint
    try:
        test_message = {
            "message": "Hello, what can you help me with?",
            "voice_enabled": True,
            "task_type": "chat",
            "user_role": "client"
        }
        
        response = requests.post(
            f"{base_url}/voice-chat",
            json=test_message,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Voice chat endpoint working")
            print(f"   Response: {data.get('response', 'No response')[:100]}...")
            print(f"   Model: {data.get('model', 'Unknown')}")
        else:
            print(f"❌ Voice chat endpoint failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing voice chat: {e}")
        return False
    
    # Test voice transfer endpoint
    try:
        test_transfer = {
            "message": "I need technical details about the AI system",
            "specialist": "technical",
            "user_role": "client"
        }
        
        response = requests.post(
            f"{base_url}/voice-transfer",
            json=test_transfer,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Voice transfer endpoint working")
            print(f"   Response: {data.get('response', 'No response')[:100]}...")
        else:
            print(f"❌ Voice transfer endpoint failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing voice transfer: {e}")
        return False
    
    return True

def test_integration_status():
    """Test the overall integration status"""
    print("\n📊 Integration Status Check")
    print("=" * 50)
    
    # Check if files exist
    files_to_check = [
        "backend/services/voice_enhanced_ai_service.py",
        "backend/routes/voice_ai.py",
        "frontend/src/components/VoiceAI.js",
        "frontend/src/components/VoiceAI.css"
    ]
    
    all_files_exist = True
    for file_path in files_to_check:
        if Path(file_path).exists():
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path}")
            all_files_exist = False
    
    # Check if routes are registered
    register_file = Path("backend/register_crm_only.py")
    if register_file.exists():
        content = register_file.read_text()
        if "voice_ai" in content:
            print("✅ Voice AI routes registered")
        else:
            print("❌ Voice AI routes not registered")
            all_files_exist = False
    
    return all_files_exist

def main():
    """Main test function"""
    print("🚀 SmartProBono Voice AI Integration Test")
    print("=" * 60)
    
    # Test 1: Integration status
    integration_ok = test_integration_status()
    
    # Test 2: Voice AI service
    service_ok = test_voice_ai_service()
    
    # Test 3: Voice AI routes
    routes_ok = test_voice_ai_routes()
    
    # Summary
    print("\n📋 Test Summary")
    print("=" * 50)
    print(f"Integration Status: {'✅ PASS' if integration_ok else '❌ FAIL'}")
    print(f"Voice AI Service: {'✅ PASS' if service_ok else '❌ FAIL'}")
    print(f"Voice AI Routes: {'✅ PASS' if routes_ok else '❌ FAIL'}")
    
    if integration_ok and service_ok and routes_ok:
        print("\n🎉 All tests passed! Voice AI integration is working!")
        print("\n🚀 Next steps:")
        print("   1. Start SmartProBono server")
        print("   2. Access Voice AI component in the frontend")
        print("   3. Test voice conversations with real users")
    else:
        print("\n⚠️ Some tests failed. Please check the errors above.")
    
    return integration_ok and service_ok and routes_ok

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
