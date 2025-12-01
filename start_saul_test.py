#!/usr/bin/env python3
"""
Startup script for testing Saul integration
"""

import subprocess
import sys
import os
import time
import requests
import json

def check_server_running():
    """Check if the server is already running"""
    try:
        response = requests.get("http://localhost:3001/api/v1/health", timeout=5)
        return response.status_code == 200
    except:
        return False

def start_server():
    """Start the backend server"""
    print("🚀 Starting SmartProBono backend server...")
    
    # Change to backend directory
    backend_dir = os.path.join(os.path.dirname(__file__), 'backend')
    
    # Start server in background
    try:
        process = subprocess.Popen([
            sys.executable, 'combined_server.py'
        ], cwd=backend_dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        print("✅ Server starting...")
        
        # Wait for server to start
        for i in range(30):  # Wait up to 30 seconds
            time.sleep(1)
            if check_server_running():
                print("✅ Server is running on http://localhost:3001")
                return process
            print(f"⏳ Waiting for server... ({i+1}/30)")
        
        print("❌ Server failed to start within 30 seconds")
        return None
        
    except Exception as e:
        print(f"❌ Failed to start server: {e}")
        return None

def test_saul_endpoints():
    """Test the Saul endpoints"""
    print("\n🧪 Testing Saul endpoints...")
    
    base_url = "http://localhost:3001/api/v1"
    
    # Test 1: Saul Info
    print("\n📋 Testing /ai/saul/info...")
    try:
        response = requests.get(f"{base_url}/ai/saul/info", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Success! Model: {data['model_info']['model_name']}")
            print(f"   Device: {data['model_info']['device']}")
            print(f"   Status: {data['health_status']['status']}")
        else:
            print(f"❌ Failed: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 2: Available Models
    print("\n📋 Testing /ai/models/available...")
    try:
        response = requests.get(f"{base_url}/ai/models/available", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Success! Found {len(data['available_models'])} models")
            for model_name in data['available_models'].keys():
                print(f"   - {model_name}")
        else:
            print(f"❌ Failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 3: Saul Chat (with fallback expected due to disk space)
    print("\n💬 Testing /ai/saul/chat...")
    try:
        payload = {
            "message": "What is contract law?",
            "task_type": "legal",
            "max_tokens": 100
        }
        response = requests.post(f"{base_url}/ai/saul/chat", json=payload, timeout=30)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Success! Model: {data.get('model', 'unknown')}")
            print(f"   Success: {data.get('success', False)}")
            print(f"   Response: {data.get('text', 'No response')[:100]}...")
        else:
            print(f"❌ Failed: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 4: Enhanced Chat
    print("\n💬 Testing /ai/chat (Enhanced)...")
    try:
        payload = {
            "message": "How do I file for bankruptcy?",
            "task_type": "legal",
            "model": "auto"
        }
        response = requests.post(f"{base_url}/ai/chat", json=payload, timeout=30)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Success! Model used: {data.get('model_used', 'unknown')}")
            print(f"   Fallback: {data.get('fallback_used', False)}")
            print(f"   Response: {data.get('text', 'No response')[:100]}...")
        else:
            print(f"❌ Failed: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    """Main function"""
    print("🚀 SmartProBono Saul Integration Test")
    print("=" * 50)
    
    # Check if server is already running
    if check_server_running():
        print("✅ Server is already running")
    else:
        # Start server
        server_process = start_server()
        if not server_process:
            print("❌ Failed to start server. Exiting.")
            return
    
    # Test endpoints
    test_saul_endpoints()
    
    print("\n🎉 Saul integration test completed!")
    print("\n📝 Next steps:")
    print("   1. Open http://localhost:3002 in your browser")
    print("   2. Navigate to the Saul test page")
    print("   3. Try the legal chat functionality")
    print("   4. Free up disk space to download the full Saul model")

if __name__ == "__main__":
    main()
