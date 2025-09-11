#!/usr/bin/env python3
"""
Test Enhanced API with DRF-like features
Demonstrates pagination, serialization, and better API structure
"""

import requests
import json
import time

def test_enhanced_api():
    """Test the enhanced API endpoints"""
    base_url = "http://localhost:3001"
    
    print("🚀 Testing Enhanced API with DRF-like Features")
    print("=" * 60)
    
    # Test 1: API Root
    print("\n📋 Test 1: API Root Documentation")
    print("-" * 40)
    try:
        response = requests.get(f"{base_url}/api/v2/")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API Root: {data['data']['name']} v{data['data']['version']}")
            print(f"   Features: {', '.join(data['data']['features'])}")
            print(f"   Available endpoints: {len(data['data']['endpoints'])}")
        else:
            print(f"❌ API Root failed: {response.status_code}")
    except Exception as e:
        print(f"❌ API Root error: {e}")
    
    # Test 2: Cases List with Pagination
    print("\n📊 Test 2: Cases List with Pagination")
    print("-" * 40)
    try:
        response = requests.get(f"{base_url}/api/v2/cases/?page=1&per_page=2")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Cases List: {data['data']['pagination']['total']} total cases")
            print(f"   Page: {data['data']['pagination']['page']}/{data['data']['pagination']['total_pages']}")
            print(f"   Has next: {data['data']['pagination']['has_next']}")
            print(f"   Cases: {len(data['data']['data'])}")
            
            for i, case in enumerate(data['data']['data'][:2], 1):
                print(f"   Case {i}: {case['title']} ({case['type']})")
        else:
            print(f"❌ Cases List failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Cases List error: {e}")
    
    # Test 3: Case Detail
    print("\n🔍 Test 3: Case Detail")
    print("-" * 40)
    try:
        response = requests.get(f"{base_url}/api/v2/cases/1/")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Case Detail: {data['data']['title']}")
            print(f"   Type: {data['data']['type']}")
            print(f"   Client: {data['data']['client_name']}")
            print(f"   Status: {data['data']['status']}")
        else:
            print(f"❌ Case Detail failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Case Detail error: {e}")
    
    # Test 4: Create Case
    print("\n➕ Test 4: Create Case")
    print("-" * 40)
    try:
        new_case = {
            "title": "Test Case - API Enhancement",
            "type": "civil",
            "client_name": "Test Client"
        }
        response = requests.post(
            f"{base_url}/api/v2/cases/",
            json=new_case,
            headers={'Content-Type': 'application/json'}
        )
        if response.status_code == 201:
            data = response.json()
            print(f"✅ Case Created: {data['data']['title']}")
            print(f"   ID: {data['data']['id']}")
            print(f"   Message: {data['message']}")
        else:
            print(f"❌ Create Case failed: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Create Case error: {e}")
    
    # Test 5: Filtering and Search
    print("\n🔍 Test 5: Filtering and Search")
    print("-" * 40)
    try:
        # Test search
        response = requests.get(f"{base_url}/api/v2/cases/?search=immigration")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Search Results: {data['data']['pagination']['total']} cases found")
            for case in data['data']['data'][:2]:
                print(f"   Found: {case['title']}")
        
        # Test filtering by type
        response = requests.get(f"{base_url}/api/v2/cases/?type=civil")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Filter Results: {data['data']['pagination']['total']} civil cases")
        else:
            print(f"❌ Filtering failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Filtering error: {e}")
    
    # Test 6: Users List
    print("\n👥 Test 6: Users List")
    print("-" * 40)
    try:
        response = requests.get(f"{base_url}/api/v2/users/")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Users List: {data['data']['pagination']['total']} users")
            for user in data['data']['data'][:2]:
                print(f"   User: {user['username']} ({user['email']})")
        else:
            print(f"❌ Users List failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Users List error: {e}")
    
    # Test 7: Documents List
    print("\n📄 Test 7: Documents List")
    print("-" * 40)
    try:
        response = requests.get(f"{base_url}/api/v2/documents/")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Documents List: {data['data']['pagination']['total']} documents")
            for doc in data['data']['data'][:2]:
                print(f"   Document: {doc['title']} ({doc['type']})")
        else:
            print(f"❌ Documents List failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Documents List error: {e}")
    
    # Test 8: Health Check
    print("\n🏥 Test 8: Health Check")
    print("-" * 40)
    try:
        response = requests.get(f"{base_url}/api/v2/health/")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health Check: {data['data']['status']}")
            print(f"   Version: {data['data']['version']}")
        else:
            print(f"❌ Health Check failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Health Check error: {e}")
    
    print("\n🎉 Enhanced API testing completed!")
    print("=" * 60)
    print("\n📚 Available Features:")
    print("   ✅ Pagination (page, per_page)")
    print("   ✅ Serialization (structured data)")
    print("   ✅ Filtering (search, type, status)")
    print("   ✅ Standardized responses")
    print("   ✅ Error handling")
    print("   ✅ API documentation")
    print("   ✅ Health checks")
    print("\n🔗 Try these URLs in your browser:")
    print(f"   {base_url}/api/v2/")
    print(f"   {base_url}/api/v2/cases/")
    print(f"   {base_url}/api/v2/cases/?page=1&per_page=5")
    print(f"   {base_url}/api/v2/cases/?search=immigration")

if __name__ == "__main__":
    test_enhanced_api()
