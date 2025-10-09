#!/usr/bin/env python3
"""
Simple Ollama Test
"""

import requests
import json

def test_ollama_direct():
    """Test Ollama directly"""
    print("🧪 Testing Ollama directly...")
    
    payload = {
        "model": "gemma2:2b",
        "prompt": "You are a legal assistant. User asks: What are my rights as a tenant? Please provide helpful legal guidance.",
        "stream": False,
        "options": {
            "temperature": 0.7,
            "max_tokens": 1000
        }
    }
    
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            response_text = result.get("response", "").strip()
            print(f"✅ Ollama working - Response length: {len(response_text)} chars")
            print(f"Response: {response_text[:300]}...")
            return True
        else:
            print(f"❌ Ollama failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Ollama error: {e}")
        return False

def test_chat_api():
    """Test chat API"""
    print("\n🧪 Testing chat API...")
    
    try:
        response = requests.post(
            "http://localhost:3001/api/v1/ai/chat",
            json={
                "message": "What are my rights as a tenant?",
                "task_type": "chat",
                "model": "legal"
            },
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Chat API response: {data}")
            return True
        else:
            print(f"❌ Chat API failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Chat API error: {e}")
        return False

if __name__ == "__main__":
    ollama_working = test_ollama_direct()
    chat_working = test_chat_api()
    
    print(f"\n📊 Results:")
    print(f"Ollama: {'✅ Working' if ollama_working else '❌ Failed'}")
    print(f"Chat API: {'✅ Working' if chat_working else '❌ Failed'}")
