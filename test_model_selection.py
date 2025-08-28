#!/usr/bin/env python3
"""
Test the legal chat API with different models to verify that model selection persists
"""

import urllib.request
import urllib.error
import urllib.parse
import sys
import json
import time
import argparse

def test_model_selection(base_url="http://localhost:8081"):
    """
    Test the legal chat API with different models to verify model selection works correctly
    """
    # API endpoint
    api_url = f"{base_url}/api/legal/chat"
    
    models = ["chat", "mistral", "llama", "deepseek", "falcon", "document_drafting"]
    test_questions = [
        "How do I respond to a court summons?",
        "What steps should I take after a car accident?",
        "How can I dispute a credit report error?",
        "What's the process for small claims court?",
        "How do I file for unemployment benefits?",
        "What are my tenant rights?"
    ]
    
    print("\n===== MODEL SELECTION TEST =====\n")
    print(f"Testing persistence of model selection for {len(models)} models")
    
    # Test each model with different questions
    for i, model in enumerate(models):
        # Get question for this test
        question = test_questions[i % len(test_questions)]
        
        print(f"\n--- Testing model: {model} ---")
        print(f"Question: {question}")
        
        # Data to send
        data = {
            "message": question,
            "task_type": model
        }
        
        try:
            # Convert data to JSON
            data = json.dumps(data).encode('utf-8')
            
            # Create request
            req = urllib.request.Request(
                api_url, 
                data=data,
                headers={'Content-Type': 'application/json'}
            )
            
            # Send the request
            with urllib.request.urlopen(req) as response:
                # Check the response
                if response.getcode() == 200:
                    # Read and parse the response
                    response_data = json.loads(response.read().decode('utf-8'))
                    model_info = response_data.get("model_info", {})
                    returned_model_type = model_info.get("model_type", "Unknown")
                    returned_model_name = model_info.get("name", "Unknown")
                    
                    print(f"Requested model: {model}")
                    print(f"Returned model type: {returned_model_type}")
                    print(f"Returned model name: {returned_model_name}")
                    
                    # Verify the model selection was maintained
                    if returned_model_type == model:
                        print("✅ Test passed: Model selection persisted correctly")
                    else:
                        print("❌ Test failed: Model selection did not persist")
                        print(f"  Expected: {model}")
                        print(f"  Actual: {returned_model_type}")
                else:
                    print(f"❌ Error: API request failed with status code {response.getcode()}")
                
        except urllib.error.HTTPError as e:
            print(f"❌ Error: HTTP Error {e.code}")
            try:
                error_data = json.loads(e.read().decode('utf-8'))
                print(json.dumps(error_data, indent=2))
            except:
                print(f"Response: {e.read().decode('utf-8')}")
        except Exception as e:
            print(f"❌ Error: {str(e)}")
    
    print("\n===== TEST COMPLETE =====\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Test model selection persistence')
    parser.add_argument('--url', default="http://localhost:8081", help='Base URL for the API (default: http://localhost:8081)')
    args = parser.parse_args()
    
    test_model_selection(args.url) 