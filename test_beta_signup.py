#!/usr/bin/env python3
"""
Test the beta signup API endpoint to verify email sending
"""

import requests
import sys
import json
import time

def test_beta_signup(test_email):
    """
    Test the beta signup API endpoint
    """
    if not test_email:
        print("Error: Please provide a test email address")
        print("Usage: python test_beta_signup.py your-test-email@example.com")
        return False
    
    # API endpoint - using port 8081 since that's what we're running on
    api_url = "http://localhost:8081/api/beta/signup"
    
    # Data to send
    data = {
        "email": test_email
    }
    
    print(f"Testing beta signup with email: {test_email}")
    print(f"Sending POST request to: {api_url}")
    
    try:
        # Send the request
        response = requests.post(api_url, json=data)
        
        # Print the response
        print(f"Status Code: {response.status_code}")
        print("Response:")
        print(json.dumps(response.json(), indent=2))
        
        if response.status_code == 200:
            print("\nSuccess! Check the following:")
            print("1. Check your email inbox for the confirmation email")
            print("2. Check info@smartprobono.org for the admin notification")
            print("3. Verify DKIM authentication is passing")
            return True
        else:
            print("\nError: API request failed")
            return False
            
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

if __name__ == "__main__":
    # Get test email from command line argument
    test_email = sys.argv[1] if len(sys.argv) > 1 else None
    test_beta_signup(test_email) 