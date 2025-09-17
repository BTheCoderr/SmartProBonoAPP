#!/usr/bin/env python3
"""
Integration test for SmartProBono advanced features
Tests all the new APIs and functionality we've implemented
"""

import requests
import json
import time
from datetime import datetime

def test_endpoint(url, description, expected_status=200):
    """Test an API endpoint and return results"""
    print(f"\n🧪 Testing: {description}")
    print(f"   URL: {url}")
    
    try:
        response = requests.get(url, timeout=5)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == expected_status:
            try:
                data = response.json()
                print(f"   ✅ Success: {json.dumps(data, indent=2)[:200]}...")
                return True, data
            except json.JSONDecodeError:
                print(f"   ✅ Success: {response.text[:100]}...")
                return True, response.text
        else:
            print(f"   ❌ Failed: Expected {expected_status}, got {response.status_code}")
            print(f"   Response: {response.text[:200]}...")
            return False, None
            
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Error: {e}")
        return False, None

def main():
    print("🚀 SmartProBono Advanced Features Integration Test")
    print("=" * 60)
    
    base_url = "http://localhost:3001"
    frontend_url = "http://localhost:3002"
    
    # Test basic health
    success_count = 0
    total_tests = 0
    
    # Core API tests
    endpoints_to_test = [
        (f"{base_url}/api/health", "Main API Health Check"),
        (f"{base_url}/crm/health", "CRM System Health Check"),
        (f"{frontend_url}/", "Frontend Homepage", 200),
        (f"{frontend_url}/features-demo", "Features Demo Page", 200),
        (f"{frontend_url}/analytics-dashboard", "Analytics Dashboard", 200),
    ]
    
    print("\n📡 Core System Tests")
    print("-" * 40)
    
    for url, description, *expected in endpoints_to_test:
        expected_status = expected[0] if expected else 200
        success, data = test_endpoint(url, description, expected_status)
        total_tests += 1
        if success:
            success_count += 1
    
    # Test WebSocket server
    print("\n🔌 WebSocket Tests")
    print("-" * 40)
    
    import socket
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('localhost', 8765))
        sock.close()
        
        if result == 0:
            print("   ✅ WebSocket server is running on port 8765")
            success_count += 1
        else:
            print("   ❌ WebSocket server is not accessible on port 8765")
        total_tests += 1
    except Exception as e:
        print(f"   ❌ WebSocket test error: {e}")
        total_tests += 1
    
    # Test CRM endpoints
    print("\n👥 CRM System Tests")
    print("-" * 40)
    
    crm_endpoints = [
        (f"{base_url}/crm/client/cases", "Client Cases"),
        (f"{base_url}/crm/lawyer/dashboard", "Lawyer Dashboard"),
        (f"{base_url}/crm/notifications", "Notifications System"),
    ]
    
    for url, description in crm_endpoints:
        # These might require authentication, so we expect either 200 or 401
        success, data = test_endpoint(url, description, 200)
        if not success:
            # Try again expecting 401 (unauthorized)
            success, data = test_endpoint(url, f"{description} (Auth Required)", 401)
        
        total_tests += 1
        if success:
            success_count += 1
    
    # Test document processing
    print("\n📄 Document Processing Tests")
    print("-" * 40)
    
    doc_endpoints = [
        (f"{base_url}/api/scanner/health", "Document Scanner"),
        (f"{base_url}/api/generator/health", "PDF Generator"),
    ]
    
    for url, description in doc_endpoints:
        success, data = test_endpoint(url, description)
        total_tests += 1
        if success:
            success_count += 1
    
    # Test frontend components availability
    print("\n🎨 Frontend Component Tests")
    print("-" * 40)
    
    frontend_pages = [
        (f"{frontend_url}/dashboard", "Main Dashboard"),
        (f"{frontend_url}/legal-chat", "Legal AI Chat"),
        (f"{frontend_url}/documents", "Documents Page"),
        (f"{frontend_url}/virtual-paralegal", "Virtual Paralegal"),
    ]
    
    for url, description in frontend_pages:
        success, data = test_endpoint(url, description)
        total_tests += 1
        if success:
            success_count += 1
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 60)
    
    success_rate = (success_count / total_tests) * 100 if total_tests > 0 else 0
    
    print(f"✅ Successful tests: {success_count}")
    print(f"❌ Failed tests: {total_tests - success_count}")
    print(f"📈 Success rate: {success_rate:.1f}%")
    
    if success_rate >= 80:
        print("\n🎉 EXCELLENT! Your SmartProBono platform is running great!")
        print("   Most features are working correctly.")
    elif success_rate >= 60:
        print("\n👍 GOOD! Your platform is mostly functional.")
        print("   A few features need attention.")
    else:
        print("\n⚠️  NEEDS WORK! Several features need debugging.")
        print("   Check the failed tests above.")
    
    print(f"\n🚀 Platform Status: {'OPERATIONAL' if success_rate >= 70 else 'NEEDS ATTENTION'}")
    
    return success_rate >= 70

if __name__ == "__main__":
    main()
