#!/usr/bin/env python3
"""
Test the legal chat API with different models
"""

import requests
import sys
import json
import time

def test_legal_chat(question, model_type="mistral"):
    """
    Test the legal chat API with different models
    """
    if not question:
        print("Error: Please provide a legal question")
        print("Usage: python test_legal_chat.py 'What should I do about a court summons?' [model]")
        print("Available models: chat, mistral, llama, deepseek, falcon, document_drafting")
        return False
    
    # API endpoint - using port 8081 since that's what we're running on
    api_url = "http://localhost:8081/api/legal/chat"
    
    # Data to send
    data = {
        "message": question,
        "task_type": model_type
    }
    
    print(f"Testing legal chat with question: '{question}'")
    print(f"Using model: {model_type}")
    print(f"Sending POST request to: {api_url}")
    
    try:
        # Send the request
        response = requests.post(api_url, json=data)
        
        # Print the response
        print(f"Status Code: {response.status_code}")
        print("\nResponse:")
        if response.status_code == 200:
            response_data = response.json()
            model_info = response_data.get("model_info", {})
            print(f"Model: {model_info.get('name', 'Unknown')}")
            print(f"Version: {model_info.get('version', 'Unknown')}")
            print(f"Response time: {model_info.get('response_time_ms', 0)}ms")
            print("\nLegal Response:")
            print(response_data.get("response", "No response"))
            return True
        else:
            print(json.dumps(response.json(), indent=2))
            print("\nError: API request failed")
            return False
            
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

if __name__ == "__main__":
    # Get question and optional model from command line arguments
    question = sys.argv[1] if len(sys.argv) > 1 else None
    model = sys.argv[2] if len(sys.argv) > 2 else "mistral"
    test_legal_chat(question, model) 