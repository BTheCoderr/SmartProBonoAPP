#!/usr/bin/env python3
"""
Simple API test for Saul integration
"""

import requests
import json
import time

def test_saul_api():
    """Test the Saul API endpoints"""
    base_url = "http://localhost:3001/api/v1"
    
    print("🧪 Testing Saul API Integration...")
    print("=" * 50)
    
    # Wait a moment for server to start
    print("⏳ Waiting for server to start...")
    time.sleep(3)
    
    # Test 1: Model Info
    print("\n📋 Testing /ai/saul/info endpoint...")
    try:
        response = requests.get(f"{base_url}/ai/saul/info", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Success! Status: {response.status_code}")
            print(f"   Model: {data['model_info']['model_name']}")
            print(f"   Device: {data['model_info']['device']}")
            print(f"   Health: {data['health_status']['status']}")
        else:
            print(f"❌ Failed with status: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    # Test 2: Available Models
    print("\n📋 Testing /ai/models/available endpoint...")
    try:
        response = requests.get(f"{base_url}/ai/models/available", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Success! Status: {response.status_code}")
            models = data['available_models']
            print(f"   Available models: {len(models)}")
            for model_name, model_info in models.items():
                print(f"      - {model_name}: {model_info['name']} ({model_info['status']})")
        else:
            print(f"❌ Failed with status: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    # Test 3: Saul Chat
    print("\n💬 Testing /ai/saul/chat endpoint...")
    try:
        payload = {
            "message": "What is contract law?",
            "task_type": "legal",
            "max_tokens": 100
        }
        response = requests.post(f"{base_url}/ai/saul/chat", json=payload, timeout=30)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Success! Status: {response.status_code}")
            print(f"   Model: {data.get('model', 'unknown')}")
            print(f"   Success: {data.get('success', False)}")
            print(f"   Response length: {len(data.get('text', ''))}")
            if data.get('text'):
                print(f"   Preview: {data['text'][:150]}...")
        else:
            print(f"❌ Failed with status: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    # Test 4: Enhanced AI Chat
    print("\n💬 Testing /ai/chat endpoint (Enhanced)...")
    try:
        payload = {
            "message": "How do I file for bankruptcy?",
            "task_type": "legal",
            "model": "auto"
        }
        response = requests.post(f"{base_url}/ai/chat", json=payload, timeout=30)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Success! Status: {response.status_code}")
            print(f"   Model used: {data.get('model_used', 'unknown')}")
            print(f"   Fallback used: {data.get('fallback_used', False)}")
            print(f"   Response length: {len(data.get('text', ''))}")
            if data.get('text'):
                print(f"   Preview: {data['text'][:150]}...")
        else:
            print(f"❌ Failed with status: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    test_saul_api()
