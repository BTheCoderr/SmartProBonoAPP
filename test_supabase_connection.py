#!/usr/bin/env python3
"""
Test Supabase Connection for LangGraph
"""

import requests
import json

# Supabase configuration
SUPABASE_URL = "https://ewtcvsohdgkthuyajyyk.supabase.co"
SUPABASE_SERVICE_KEY = "***REMOVED***"

def test_connection():
    """Test basic Supabase connection"""
    print("🔍 Testing Supabase Connection")
    print("=" * 40)
    
    # Test 1: Basic API access
    print("1. Testing basic API access...")
    url = f"{SUPABASE_URL}/rest/v1/"
    headers = {"apikey": SUPABASE_SERVICE_KEY}
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            print("   ✅ Supabase API accessible")
        else:
            print(f"   ❌ API error: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Connection error: {e}")
        return False
    
    # Test 2: Check if case_intakes table exists
    print("2. Checking case_intakes table...")
    url = f"{SUPABASE_URL}/rest/v1/case_intakes?select=*&limit=1"
    headers = {
        "apikey": SUPABASE_SERVICE_KEY,
        "Authorization": f"Bearer {SUPABASE_SERVICE_KEY}"
    }
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            print("   ✅ case_intakes table exists and accessible")
            data = response.json()
            print(f"   📊 Found {len(data)} records")
        else:
            print(f"   ❌ Table error: {response.status_code}")
            print(f"   📝 Response: {response.text}")
            return False
    except Exception as e:
        print(f"   ❌ Table access error: {e}")
        return False
    
    # Test 3: Try to insert a test record
    print("3. Testing record insertion...")
    url = f"{SUPABASE_URL}/rest/v1/case_intakes"
    headers = {
        "apikey": SUPABASE_SERVICE_KEY,
        "Authorization": f"Bearer {SUPABASE_SERVICE_KEY}",
        "Content-Type": "application/json"
    }
    
    test_data = {
        "user_id": None,
        "raw_text": "Test connection from Python script",
        "meta": {"test": True}
    }
    
    try:
        response = requests.post(url, headers=headers, json=test_data)
        if response.status_code == 201:
            print("   ✅ Record insertion successful")
            result = response.json()
            print(f"   📝 Created record ID: {result[0]['id']}")
            
            # Clean up test record
            record_id = result[0]['id']
            delete_url = f"{SUPABASE_URL}/rest/v1/case_intakes?id=eq.{record_id}"
            delete_response = requests.delete(delete_url, headers=headers)
            if delete_response.status_code == 204:
                print("   🧹 Test record cleaned up")
            else:
                print("   ⚠️  Could not clean up test record")
        else:
            print(f"   ❌ Insertion error: {response.status_code}")
            print(f"   📝 Response: {response.text}")
            return False
    except Exception as e:
        print(f"   ❌ Insertion error: {e}")
        return False
    
    print("\n🎉 All tests passed! Supabase connection is working correctly.")
    return True

if __name__ == "__main__":
    test_connection()
