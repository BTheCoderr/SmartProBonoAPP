#!/usr/bin/env python3
"""
SmartProBono Full API Demo

This script demonstrates a complete workflow using the SmartProBono API:
1. Sign up for the beta program
2. Ask a legal question using different models
3. Submit feedback about the response
"""

import requests
import json
import time
import os
import sys

# API Configuration
API_BASE = "http://localhost:8081/api"
ENDPOINTS = {
    "signup": f"{API_BASE}/beta/signup",
    "legal_chat": f"{API_BASE}/legal/chat",
    "feedback": f"{API_BASE}/feedback",
    "health": f"{API_BASE}/health"
}

def check_api_health():
    """Check if the API is running"""
    print("Checking API health...")
    try:
        response = requests.get(ENDPOINTS["health"])
        if response.status_code == 200:
            print("✅ API is running")
            return True
        else:
            print(f"❌ API returned status code {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Could not connect to API: {str(e)}")
        return False

def beta_signup(email):
    """Sign up for the beta program"""
    print(f"\n===== STEP 1: BETA SIGNUP =====")
    print(f"Signing up with email: {email}")
    
    data = {"email": email}
    
    try:
        response = requests.post(ENDPOINTS["signup"], json=data)
        
        print(f"Status Code: {response.status_code}")
        print("Response:")
        print(json.dumps(response.json(), indent=2))
        
        if response.status_code == 200:
            print("\n✅ Successfully signed up for beta!")
            print("   Check your email for confirmation")
            return True
        else:
            print("\n❌ Failed to sign up for beta")
            return False
    except Exception as e:
        print(f"\n❌ Error signing up: {str(e)}")
        return False

def ask_legal_question(question, model_type):
    """Ask a legal question using a specific model"""
    print(f"\n===== STEP 2: LEGAL CONSULTATION ({model_type.upper()}) =====")
    print(f"Question: {question}")
    print(f"Using model: {model_type}")
    
    data = {
        "message": question,
        "task_type": model_type
    }
    
    try:
        response = requests.post(ENDPOINTS["legal_chat"], json=data)
        
        if response.status_code == 200:
            response_data = response.json()
            model_info = response_data.get("model_info", {})
            
            print(f"\n✅ Received response from {model_info.get('name', 'Unknown')}")
            print(f"   Response time: {model_info.get('response_time_ms', 0)}ms")
            print("\nLegal Response:")
            print("-------------")
            print(response_data.get("response", "No response"))
            print("-------------")
            
            return response_data
        else:
            print(f"\n❌ Error: Status code {response.status_code}")
            print(response.text)
            return None
    except Exception as e:
        print(f"\n❌ Error asking question: {str(e)}")
        return None

def submit_feedback(feedback_text, rating):
    """Submit feedback about the response"""
    print(f"\n===== STEP 3: FEEDBACK SUBMISSION =====")
    print(f"Rating: {rating}/5")
    print(f"Feedback: {feedback_text}")
    
    data = {
        "feedback": feedback_text,
        "rating": rating
    }
    
    try:
        response = requests.post(ENDPOINTS["feedback"], json=data)
        
        print(f"Status Code: {response.status_code}")
        print("Response:")
        print(json.dumps(response.json(), indent=2))
        
        if response.status_code == 200:
            print("\n✅ Successfully submitted feedback!")
            return True
        else:
            print("\n❌ Failed to submit feedback")
            return False
    except Exception as e:
        print(f"\n❌ Error submitting feedback: {str(e)}")
        return False

def run_demo(email, question):
    """Run the complete demo workflow"""
    print("=" * 60)
    print("SmartProBono API Demo - Full Workflow")
    print("=" * 60)
    
    # Step 0: Check API health
    if not check_api_health():
        print("Exiting: API is not available")
        return
    
    # Step 1: Sign up for beta
    if not beta_signup(email):
        print("Skipping to next step due to signup issue...")
    
    time.sleep(1)  # Small delay between steps
    
    # Step 2: Ask legal questions with different models
    models = ["chat", "mistral", "llama", "deepseek", "falcon"]
    responses = {}
    
    for model in models:
        response_data = ask_legal_question(question, model)
        if response_data:
            responses[model] = response_data
        time.sleep(1)  # Small delay between requests
    
    # Step 3: Submit feedback
    feedback_text = "The legal information was helpful and easy to understand. I appreciate the variety of models available."
    submit_feedback(feedback_text, 5)
    
    print("\n" + "=" * 60)
    print("Demo Complete!")
    print("=" * 60)
    print(f"Check {email} for confirmation emails")
    print("Check info@smartprobono.org for admin notifications")
    print("=" * 60)

if __name__ == "__main__":
    # Get email and question from command line or use defaults
    email = sys.argv[1] if len(sys.argv) > 1 else "bferrell514@gmail.com"
    question = sys.argv[2] if len(sys.argv) > 2 else "What are my rights as a tenant in California?"
    
    run_demo(email, question) 