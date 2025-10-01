#!/usr/bin/env python3
"""
Test script to check which routes are available
"""
import requests
import json

BASE_URL = "http://localhost:3001"

def test_route(method, endpoint, data=None, headers=None, expected_statuses=[200]):
    """Test a single route"""
    try:
        if method.upper() == "GET":
            response = requests.get(f"{BASE_URL}{endpoint}", headers=headers)
        elif method.upper() == "POST":
            response = requests.post(f"{BASE_URL}{endpoint}", json=data, headers=headers)
        else:
            return f"❌ {method} {endpoint} - Unsupported method"
        
        # Check if status is in expected range
        status = "✅" if response.status_code in expected_statuses else "❌"
        status_msg = f"{response.status_code}"
        if response.status_code == 401:
            status_msg += " (Protected - Auth Required)"
        return f"{status} {method} {endpoint} - {status_msg}"
    except Exception as e:
        return f"❌ {method} {endpoint} - Error: {str(e)}"

def main():
    print("🧪 TESTING SMARTPROBONO ROUTES")
    print("=" * 50)
    
    # Test core routes
    print("\n📋 CORE ROUTES:")
    print(test_route("GET", "/api/health"))
    print(test_route("POST", "/api/contact/submit", {
        "firstName": "Test",
        "lastName": "User",
        "email": "test@example.com",
        "message": "This is a test message for SmartProBono",
        "phone": "555-1234",
        "caseType": "General Inquiry"
    }))
    
    # Test CRM routes
    print("\n👥 CRM ROUTES:")
    print(test_route("GET", "/api/v1/crm/health"))
    print(test_route("GET", "/api/v1/crm/lawyer/clients", expected_statuses=[200, 401]))  # Auth protected
    print(test_route("GET", "/api/v1/virtual-paralegal/clients"))
    
    # Test Voice AI routes
    print("\n🎤 VOICE AI ROUTES:")
    print(test_route("GET", "/api/voice/status"))
    print(test_route("POST", "/api/voice/command", {"text": "help"}))
    print(test_route("POST", "/api/voice/speech-to-text"))
    
    # Test Court Filing routes
    print("\n⚖️ COURT FILING ROUTES:")
    print(test_route("GET", "/api/court-filing/rules"))
    print(test_route("GET", "/api/court-filing/templates"))
    print(test_route("POST", "/api/court-filing/fees", {
        "document_type": "complaint",
        "jurisdiction": "State",
        "court": "Superior Court"
    }))
    
    # Test Enhanced API v2 routes
    print("\n🚀 ENHANCED API v2 ROUTES:")
    print(test_route("GET", "/api/v2/"))
    print(test_route("GET", "/api/v2/cases/"))
    print(test_route("GET", "/api/v2/users/"))
    
    # Test Analytics routes
    print("\n📊 ANALYTICS ROUTES:")
    print(test_route("GET", "/api/analytics/dashboard"))
    print(test_route("GET", "/api/analytics/metrics"))
    
    print("\n" + "=" * 50)
    print("✅ = Working | ❌ = Not Working")

if __name__ == "__main__":
    main()
