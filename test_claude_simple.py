#!/usr/bin/env python3
"""
Simple test script for Claude API integration
"""
import requests
import json
import os

def test_claude_api():
    """Test Claude API with the provided key"""
    print("🧪 Testing Claude API...")
    
    # The API key from the screenshot
    api_key = "sk-ant-api03-ceS1CHfarlcsD_6qtrn8_HeB0G0268TWZN0JgutkdvE-zuJ2Fkptkhr0QIyrVi53ZpjYxV_nRENWdm5A3wX1Q-91CATQAA"
    
    headers = {
        "x-api-key": api_key,
        "Content-Type": "application/json",
        "anthropic-version": "2023-06-01"
    }
    
    payload = {
        "model": "claude-3-5-sonnet-20241022",
        "max_tokens": 500,
        "messages": [
            {
                "role": "user",
                "content": "Hello! Can you help me understand my rights as a tenant facing eviction? Please provide a brief, helpful response."
            }
        ]
    }
    
    try:
        print("📡 Making request to Claude API...")
        response = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers=headers,
            json=payload,
            timeout=30
        )
        
        print(f"📊 Response status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            content = result.get("content", [{}])[0].get("text", "")
            print("✅ Claude API test successful!")
            print(f"📝 Response: {content}")
            return True
        else:
            print(f"❌ Claude API test failed: {response.status_code}")
            print(f"Error: {response.text}")
            
            # Check if it's an authentication error
            if response.status_code == 401:
                print("\n🔍 Authentication Error Analysis:")
                print("- The API key might be invalid or expired")
                print("- Please check if the key was copied correctly from the Anthropic console")
                print("- Make sure the key has the correct permissions")
            
            return False
            
    except Exception as e:
        print(f"❌ Claude API test error: {str(e)}")
        return False

def test_api_key_format():
    """Test if the API key has the correct format"""
    print("\n🔍 Testing API Key Format...")
    
    api_key = "sk-ant-api03-ceS1CHfarlcsD_6qtrn8_HeB0G0268TWZN0JgutkdvE-zuJ2Fkptkhr0QIyrVi53ZpjYxV_nRENWdm5A3wX1Q-91CATQAA"
    
    # Check if it starts with the correct prefix
    if api_key.startswith("sk-ant-api03-"):
        print("✅ API key has correct prefix")
    else:
        print("❌ API key doesn't have correct prefix")
        return False
    
    # Check length (should be around 100+ characters)
    if len(api_key) > 100:
        print("✅ API key has reasonable length")
    else:
        print("❌ API key seems too short")
        return False
    
    print(f"🔑 Key length: {len(api_key)} characters")
    print(f"🔑 Key preview: {api_key[:20]}...{api_key[-10:]}")
    
    return True

def main():
    """Run the tests"""
    print("🚀 SmartProBono Claude API Simple Test")
    print("=" * 50)
    
    # Test API key format first
    format_ok = test_api_key_format()
    
    if format_ok:
        # Test the actual API call
        api_ok = test_claude_api()
        
        if api_ok:
            print("\n🎉 Claude integration is working!")
            print("✅ You can now use Claude in your SmartProBono application")
        else:
            print("\n⚠️ Claude API test failed")
            print("Please check the API key and try again")
    else:
        print("\n❌ API key format is incorrect")
        print("Please verify the key was copied correctly")

if __name__ == "__main__":
    main()
