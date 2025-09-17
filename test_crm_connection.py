#!/usr/bin/env python3
"""
Test script to verify CRM system is properly connected
"""
import requests
import json

def test_crm_endpoints():
    """Test CRM API endpoints"""
    base_url = "http://localhost:3001"
    
    print("🧪 Testing CRM System Connection...")
    print("=" * 50)
    
    # Test 1: Health check
    print("1. Testing health check...")
    try:
        response = requests.get(f"{base_url}/api/health")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ Health check working")
        else:
            print("   ❌ Health check failed")
    except Exception as e:
        print(f"   ❌ Health check error: {e}")
    
    # Test 2: CRM API root (should exist now)
    print("\n2. Testing CRM API availability...")
    try:
        response = requests.get(f"{base_url}/api/v1/crm/")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ CRM API is accessible")
            print(f"   Response: {response.text[:200]}...")
        else:
            print("   ❌ CRM API not accessible")
    except Exception as e:
        print(f"   ❌ CRM API error: {e}")
    
    # Test 3: Test client intake endpoint
    print("\n3. Testing client intake endpoint...")
    try:
        test_data = {
            "first_name": "Test",
            "last_name": "User",
            "email": "test@example.com",
            "phone": "555-1234",
            "legal_issue_type": "immigration",
            "case_description": "Test case for CRM connection"
        }
        
        response = requests.post(
            f"{base_url}/api/v1/crm/client/intake",
            json=test_data,
            headers={'Content-Type': 'application/json'}
        )
        print(f"   Status: {response.status_code}")
        if response.status_code == 201:
            print("   ✅ Client intake endpoint working")
            print(f"   Response: {response.json()}")
        else:
            print(f"   ❌ Client intake failed: {response.text}")
    except Exception as e:
        print(f"   ❌ Client intake error: {e}")
    
    # Test 4: Check if all CRM routes are registered
    print("\n4. Testing CRM route registration...")
    crm_routes = [
        "/api/v1/crm/client/intake",
        "/api/v1/crm/lawyer/clients",
        "/api/v1/crm/bondsman/bonds",
        "/api/v1/crm/court-dates",
        "/api/v1/crm/notifications"
    ]
    
    for route in crm_routes:
        try:
            response = requests.get(f"{base_url}{route}")
            print(f"   {route}: Status {response.status_code}")
        except Exception as e:
            print(f"   {route}: Error - {e}")
    
    print("\n" + "=" * 50)
    print("🎯 CRM Connection Test Complete!")

if __name__ == "__main__":
    test_crm_endpoints()
