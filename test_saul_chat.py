#!/usr/bin/env python3
"""
Quick test script for Saul Legal AI Chat
"""

import requests
import json

BASE_URL = "http://localhost:3001/api/v1"

def test_saul_chat(message, task_type="legal"):
    """Test the Saul chat endpoint"""
    print(f"\n{'='*80}")
    print(f"Testing Saul Chat")
    print(f"Message: {message}")
    print(f"Task Type: {task_type}")
    print(f"{'='*80}\n")
    
    url = f"{BASE_URL}/ai/chat"
    payload = {
        "message": message,
        "task_type": task_type,
        "max_tokens": 150
    }
    
    try:
        response = requests.post(url, json=payload, timeout=60)
        response.raise_for_status()
        
        data = response.json()
        
        print(f"✅ Success: {data.get('success', False)}")
        print(f"📝 Model: {data.get('model', 'unknown')}")
        print(f"🤖 Model Used: {data.get('model_used', 'unknown')}")
        print(f"\n💬 Response:\n{'-'*80}")
        print(data.get('text', 'No response text'))
        print(f"{'-'*80}\n")
        
        if data.get('model_info'):
            print(f"ℹ️  Model Info:")
            print(f"   - Name: {data['model_info'].get('model_name')}")
            print(f"   - Base: {data['model_info'].get('base_model')}")
            print(f"   - Loaded: {data['model_info'].get('is_loaded')}")
        
        return data
        
    except requests.exceptions.Timeout:
        print("❌ Request timed out (model is taking too long to respond)")
        return None
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
        return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def test_saul_info():
    """Test the Saul info endpoint"""
    print(f"\n{'='*80}")
    print(f"Testing Saul Model Info")
    print(f"{'='*80}\n")
    
    url = f"{BASE_URL}/ai/saul/info"
    
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        
        data = response.json()
        
        print(f"📊 Model Status:")
        print(f"   - Name: {data.get('model_info', {}).get('model_name')}")
        print(f"   - Loaded: {data.get('model_info', {}).get('is_loaded')}")
        print(f"   - Status: {data.get('health_status', {}).get('status')}")
        print(f"   - Device: {data.get('model_info', {}).get('device')}")
        
        return data
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

if __name__ == "__main__":
    # Test 1: Check model status
    test_saul_info()
    
    # Test 2: Legal questions
    test_saul_chat(
        "What is a breach of contract?",
        task_type="legal"
    )
    
    test_saul_chat(
        "How do I file for bankruptcy?",
        task_type="research"
    )
    
    test_saul_chat(
        "Explain tenant rights in eviction cases",
        task_type="legal"
    )
    
    # Test 3: General chat (should use fallback)
    test_saul_chat(
        "Hello, how are you?",
        task_type="chat"
    )

