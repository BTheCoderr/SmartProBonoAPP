#!/usr/bin/env python3
"""
Test script to verify Ollama integration with SmartProBono
"""

import requests
import json
import sys

def test_ollama_direct():
    """Test Ollama directly"""
    print("🧪 Testing Ollama directly...")
    
    try:
        # Test if Ollama is running
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json().get("models", [])
            print(f"✅ Ollama is running with {len(models)} models available")
            
            # Test a simple generation
            payload = {
                "model": "llama3.2:3b",
                "prompt": "Hello, can you help me with a legal question?",
                "stream": False
            }
            
            response = requests.post("http://localhost:11434/api/generate", json=payload, timeout=15)
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Ollama generation successful: {result.get('response', '')[:100]}...")
                return True
            else:
                print(f"❌ Ollama generation failed: {response.status_code}")
                return False
        else:
            print(f"❌ Ollama not responding: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Cannot connect to Ollama: {e}")
        return False

def test_backend_api():
    """Test the backend API"""
    print("\n🧪 Testing Backend API...")
    
    try:
        # Test if backend is running
        response = requests.get("http://localhost:8081/api/health", timeout=5)
        if response.status_code == 200:
            print("✅ Backend is running")
            
            # Test legal chat endpoint
            payload = {
                "message": "I have a landlord dispute, can you help?",
                "task_type": "chat"
            }
            
            response = requests.post("http://localhost:8081/api/legal/chat", 
                                   json=payload, timeout=20)
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Backend chat successful: {result.get('response', '')[:100]}...")
                return True
            else:
                print(f"❌ Backend chat failed: {response.status_code} - {response.text}")
                return False
        else:
            print(f"❌ Backend not responding: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Cannot connect to backend: {e}")
        return False

def test_frontend():
    """Test if frontend is accessible"""
    print("\n🧪 Testing Frontend...")
    
    try:
        response = requests.get("http://localhost:3002", timeout=5)
        if response.status_code == 200:
            print("✅ Frontend is accessible")
            return True
        else:
            print(f"❌ Frontend not responding: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Cannot connect to frontend: {e}")
        return False

def main():
    print("🚀 SmartProBono Ollama Integration Test")
    print("=" * 50)
    
    ollama_ok = test_ollama_direct()
    backend_ok = test_backend_api()
    frontend_ok = test_frontend()
    
    print("\n📊 Test Results:")
    print(f"  Ollama: {'✅' if ollama_ok else '❌'}")
    print(f"  Backend: {'✅' if backend_ok else '❌'}")
    print(f"  Frontend: {'✅' if frontend_ok else '❌'}")
    
    if ollama_ok and backend_ok and frontend_ok:
        print("\n🎉 All systems are working! You can now:")
        print("  1. Go to http://localhost:3002/legal-chat")
        print("  2. Try different models (Llama, Mistral, Qwen, etc.)")
        print("  3. Test the /scan-document route")
        print("  4. Enjoy conversational AI responses!")
        return 0
    else:
        print("\n⚠️  Some systems need attention. Check the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
