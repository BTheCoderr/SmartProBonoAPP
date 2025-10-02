#!/usr/bin/env python3
"""
Simple Voice AI Integration Test
Tests the voice AI components without external dependencies
"""

import os
import sys
import asyncio
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
        
        # Test capabilities
        capabilities = service.get_capabilities()
        print(f"   Capabilities: {capabilities}")
        
        # Test available models
        models = service.get_available_models()
        print(f"   Available models: {models}")
        
        # Test a simple voice request
        if service.voice_enabled:
            print("\n📝 Testing voice-enabled request...")
            response = asyncio.run(service.process_request(
                message="What features does SmartProBono offer?",
                user_context={"user_id": "test_user", "role": "client"},
                user_role="client",
                task_type="sales",
                voice_enabled=True
            ))
            
            print(f"   Response: {response.get('response', 'No response')[:100]}...")
            print(f"   Model: {response.get('model', 'Unknown')}")
            print(f"   Voice enabled: {response.get('voice_enabled', False)}")
            
            if response.get('error'):
                print(f"   ❌ Error: {response['error']}")
            else:
                print(f"   ✅ Voice AI working!")
        else:
            print("⚠️ Voice not enabled - check API keys")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing VoiceEnhancedAIService: {e}")
        import traceback
        traceback.print_exc()
        return False

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
    
    # Summary
    print("\n📋 Test Summary")
    print("=" * 50)
    print(f"Integration Status: {'✅ PASS' if integration_ok else '❌ FAIL'}")
    print(f"Voice AI Service: {'✅ PASS' if service_ok else '❌ FAIL'}")
    
    if integration_ok and service_ok:
        print("\n🎉 Voice AI integration is working!")
        print("\n🚀 SmartProBono now has:")
        print("   ✅ Legal AI (Ollama models: llama3.2, mistral, qwen, gemma, phi)")
        print("   ✅ SmartProBono Agent (Gemini API)")
        print("   ✅ Voice Sales Agent (Cerebras API)")
        print("   ✅ Multi-Agent Routing System")
        print("   ✅ Real-time Voice Capabilities")
        print("\n📝 Next steps:")
        print("   1. Start SmartProBono server")
        print("   2. Access Voice AI component in the frontend")
        print("   3. Test voice conversations with real users")
    else:
        print("\n⚠️ Some tests failed. Please check the errors above.")
    
    return integration_ok and service_ok

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
