#!/usr/bin/env python3
"""
Test Simple Free AI Service Directly
"""

import requests
import json
from datetime import datetime

def test_simple_free_ai():
    """Test the simple free AI service logic directly"""
    print("🧪 Testing Simple Free AI Logic...")
    
    ollama_url = "http://localhost:11434/api/generate"
    message = "What are my rights as a tenant?"
    task_type = "legal"
    model = "gemma2:2b"
    
    # Build prompt
    system_prompt = """You are a legal assistant for SmartProBono. Provide helpful legal guidance.

COMMUNICATION STYLE:
- Be professional but approachable
- Use clear, simple language
- Provide specific, actionable advice
- Always remind users this is general information, not legal advice

RESPONSE FORMAT:
- Start with a direct answer
- Provide relevant legal details
- Suggest next steps or resources
- End with disclaimer about consulting an attorney

Keep responses helpful and informative."""

    full_prompt = f"{system_prompt}\n\nUser: {message}\n\nAssistant:"
    
    payload = {
        "model": model,
        "prompt": full_prompt,
        "stream": False,
        "options": {
            "temperature": 0.7,
            "max_tokens": 1000
        }
    }
    
    try:
        response = requests.post(ollama_url, json=payload, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            response_text = result.get("response", "").strip()
            
            print(f"✅ Ollama working!")
            print(f"Model: {model}")
            print(f"Response length: {len(response_text)} chars")
            print(f"Response preview: {response_text[:200]}...")
            
            return {
                "success": True,
                "model": model,
                "text": response_text,
                "response_length": len(response_text)
            }
        else:
            print(f"❌ Ollama failed: {response.status_code}")
            return {"success": False, "error": f"HTTP {response.status_code}"}
            
    except Exception as e:
        print(f"❌ Ollama error: {e}")
        return {"success": False, "error": str(e)}

def test_chat_api_direct():
    """Test chat API directly"""
    print("\n🧪 Testing Chat API...")
    
    try:
        response = requests.post(
            "http://localhost:3001/api/v1/ai/chat",
            json={
                "message": "What are my rights as a tenant?",
                "task_type": "legal",
                "model": "gemma2:2b"
            },
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            success = data.get('success', False)
            model = data.get('model', 'unknown')
            text_length = len(data.get('text', ''))
            
            print(f"✅ Chat API: {model} - {text_length} chars")
            print(f"Response preview: {data.get('text', '')[:200]}...")
            
            return {
                "success": success,
                "model": model,
                "response_length": text_length,
                "is_fallback": "technical difficulties" in data.get('text', '').lower()
            }
        else:
            print(f"❌ Chat API failed: {response.status_code}")
            return {"success": False, "error": f"HTTP {response.status_code}"}
            
    except Exception as e:
        print(f"❌ Chat API error: {e}")
        return {"success": False, "error": str(e)}

if __name__ == "__main__":
    print("🚀 Testing Free AI Integration")
    print("=" * 50)
    
    # Test Ollama directly
    ollama_result = test_simple_free_ai()
    
    # Test chat API
    api_result = test_chat_api_direct()
    
    # Summary
    print("\n📊 RESULTS SUMMARY")
    print("=" * 50)
    print(f"Ollama Direct: {'✅ Working' if ollama_result.get('success') else '❌ Failed'}")
    print(f"Chat API: {'✅ Working' if api_result.get('success') else '❌ Failed'}")
    
    if api_result.get('is_fallback'):
        print("⚠️ Chat API is using fallback responses - not calling Ollama")
    else:
        print("✅ Chat API is using Ollama models")
    
    if ollama_result.get('success') and api_result.get('is_fallback'):
        print("\n🔧 ISSUE IDENTIFIED:")
        print("Ollama is working perfectly, but the chat API service layer")
        print("is not properly calling it. Need to fix the service integration.")
    elif ollama_result.get('success') and not api_result.get('is_fallback'):
        print("\n🎉 SUCCESS:")
        print("Both Ollama and Chat API are working perfectly!")
    else:
        print("\n❌ ISSUE:")
        print("Ollama itself needs to be checked/fixed.")
