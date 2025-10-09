#!/usr/bin/env python3
"""
Force Ollama Usage - Direct Fix
Directly tests and fixes the chat API to use Ollama models
"""

import requests
import json

def test_direct_ollama():
    """Test Ollama directly with a legal question"""
    print("🧪 Testing Ollama directly...")
    
    payload = {
        "model": "gemma2:2b",
        "prompt": "You are a helpful legal assistant. User asks: What are my rights as a tenant? Please provide a helpful legal response.",
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
            print(f"✅ Ollama working - Response: {response_text[:200]}...")
            return True, response_text
        else:
            print(f"❌ Ollama failed: {response.status_code}")
            return False, None
            
    except Exception as e:
        print(f"❌ Ollama error: {e}")
        return False, None

def test_chat_api_with_ollama_params():
    """Test chat API with parameters that should force Ollama usage"""
    print("\n🧪 Testing chat API with Ollama parameters...")
    
    # Try different model parameters
    test_params = [
        {"model": "ollama", "task_type": "chat"},
        {"model": "gemma2:2b", "task_type": "chat"},
        {"model": "tinyllama:1.1b", "task_type": "chat"},
        {"model": "qwen2.5:0.5b", "task_type": "chat"},
        {"model": "auto", "task_type": "chat"},
        {"model": "default", "task_type": "chat"}
    ]
    
    for params in test_params:
        print(f"\nTesting with {params}...")
        try:
            response = requests.post(
                "http://localhost:3001/api/v1/ai/chat",
                json={
                    "message": "What are my rights as a tenant?",
                    **params
                },
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                response_text = data.get('text', data.get('response', ''))
                model_used = data.get('model', 'unknown')
                
                print(f"✅ Success - Model: {model_used}")
                print(f"Response: {response_text[:150]}...")
                
                # Check if it's a real response or fallback
                if "technical difficulties" in response_text.lower():
                    print("⚠️ Still getting fallback response")
                else:
                    print("🎉 Got real AI response!")
                    return True, params, response_text
            else:
                print(f"❌ Failed: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error: {e}")
    
    return False, None, None

def test_legal_analysis_endpoint():
    """Test the legal analysis endpoint which might be working"""
    print("\n🧪 Testing legal analysis endpoint...")
    
    try:
        response = requests.post(
            "http://localhost:3001/api/v1/legal/analyze",
            json={
                "query": "What are my rights as a tenant?",
                "jurisdiction": "state"
            },
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Legal analysis working")
            print(f"Response: {str(data)[:200]}...")
            return True
        else:
            print(f"❌ Legal analysis failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Legal analysis error: {e}")
        return False

def main():
    """Main function"""
    print("🚀 Force Ollama Usage Test")
    print("=" * 40)
    
    # Test Ollama directly
    ollama_working, ollama_response = test_direct_ollama()
    
    if not ollama_working:
        print("\n❌ Ollama is not working properly!")
        return
    
    # Test chat API
    chat_working, working_params, chat_response = test_chat_api_with_ollama_params()
    
    # Test legal analysis
    legal_analysis_working = test_legal_analysis_endpoint()
    
    print(f"\n📊 Results Summary:")
    print(f"✅ Ollama direct: {'Working' if ollama_working else 'Failed'}")
    print(f"✅ Chat API: {'Working' if chat_working else 'Failed'}")
    print(f"✅ Legal Analysis: {'Working' if legal_analysis_working else 'Failed'}")
    
    if chat_working:
        print(f"\n🎉 SUCCESS! Chat API is working with params: {working_params}")
        print(f"Response preview: {chat_response[:200]}...")
    elif legal_analysis_working:
        print(f"\n✅ Alternative: Use the legal analysis endpoint")
        print(f"Endpoint: POST /api/v1/legal/analyze")
    else:
        print(f"\n⚠️ Chat API needs configuration fix")
        print(f"Ollama is working directly, but the chat service isn't using it properly")

if __name__ == "__main__":
    main()
