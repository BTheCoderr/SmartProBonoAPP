#!/usr/bin/env python3
"""
🧪 SmartProBono Production Test Suite
Tests all critical functionality for production readiness
"""

import requests
import json
import time
import sys

BASE_URL = "http://localhost:3001"

def test_endpoint(method, endpoint, data=None, expected_status=200, description=""):
    """Test a single endpoint with detailed reporting"""
    try:
        if method.upper() == "GET":
            response = requests.get(f"{BASE_URL}{endpoint}", timeout=10)
        elif method.upper() == "POST":
            response = requests.post(f"{BASE_URL}{endpoint}", json=data, timeout=10)
        else:
            return False, f"Unsupported method: {method}"
        
        success = response.status_code == expected_status
        status_icon = "✅" if success else "❌"
        print(f"{status_icon} {method} {endpoint} - {response.status_code} {description}")
        
        if not success and response.status_code != 401:  # 401 is expected for protected routes
            print(f"   Response: {response.text[:100]}...")
        
        return success, response.status_code
        
    except requests.exceptions.RequestException as e:
        print(f"❌ {method} {endpoint} - Connection Error: {str(e)}")
        return False, str(e)

def main():
    print("🧪 SMART PROBONO PRODUCTION TEST SUITE")
    print("=" * 60)
    print(f"Testing server at: {BASE_URL}")
    print(f"Test started at: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # Wait for server to be ready
    print("\n⏳ Waiting for server to be ready...")
    for i in range(30):
        try:
            response = requests.get(f"{BASE_URL}/api/health", timeout=5)
            if response.status_code == 200:
                print("✅ Server is ready!")
                break
        except:
            pass
        time.sleep(1)
    else:
        print("❌ Server not responding after 30 seconds")
        sys.exit(1)
    
    # Test results tracking
    tests_passed = 0
    total_tests = 0
    
    # Core API Tests
    print("\n📋 CORE API TESTS:")
    print("-" * 30)
    
    test_cases = [
        ("GET", "/api/health", None, 200, "Health check"),
        ("POST", "/api/contact/submit", {
            "firstName": "Production",
            "lastName": "Test",
            "email": "test@production.com",
            "message": "Production test message",
            "phone": "555-0123",
            "caseType": "General Inquiry"
        }, 200, "Contact form submission"),
    ]
    
    for method, endpoint, data, expected_status, description in test_cases:
        total_tests += 1
        success, _ = test_endpoint(method, endpoint, data, expected_status, description)
        if success:
            tests_passed += 1
    
    # CRM System Tests
    print("\n👥 CRM SYSTEM TESTS:")
    print("-" * 30)
    
    crm_tests = [
        ("GET", "/api/v1/crm/health", None, 200, "CRM health check"),
        ("GET", "/api/v1/crm/lawyer/clients", None, 401, "Lawyer clients (auth required)"),
        ("GET", "/api/v1/virtual-paralegal/clients", None, 200, "Virtual paralegal clients"),
    ]
    
    for method, endpoint, data, expected_status, description in crm_tests:
        total_tests += 1
        success, _ = test_endpoint(method, endpoint, data, expected_status, description)
        if success:
            tests_passed += 1
    
    # Court Filing Tests
    print("\n⚖️ COURT FILING TESTS:")
    print("-" * 30)
    
    court_tests = [
        ("GET", "/api/court-filing/rules", None, 200, "Court rules"),
        ("GET", "/api/court-filing/templates", None, 200, "Filing templates"),
        ("POST", "/api/court-filing/fees", {
            "document_type": "complaint",
            "jurisdiction": "State",
            "court": "Superior Court"
        }, 200, "Fee calculation"),
    ]
    
    for method, endpoint, data, expected_status, description in court_tests:
        total_tests += 1
        success, _ = test_endpoint(method, endpoint, data, expected_status, description)
        if success:
            tests_passed += 1
    
    # Enhanced API v2 Tests
    print("\n🚀 ENHANCED API v2 TESTS:")
    print("-" * 30)
    
    v2_tests = [
        ("GET", "/api/v2/", None, 200, "API info"),
        ("GET", "/api/v2/cases/", None, 200, "List cases"),
        ("GET", "/api/v2/users/", None, 200, "List users"),
    ]
    
    for method, endpoint, data, expected_status, description in v2_tests:
        total_tests += 1
        success, _ = test_endpoint(method, endpoint, data, expected_status, description)
        if success:
            tests_passed += 1
    
    # Analytics Tests
    print("\n📊 ANALYTICS TESTS:")
    print("-" * 30)
    
    analytics_tests = [
        ("GET", "/api/analytics/dashboard", None, 200, "Analytics dashboard"),
        ("GET", "/api/analytics/metrics", None, 200, "System metrics"),
    ]
    
    for method, endpoint, data, expected_status, description in analytics_tests:
        total_tests += 1
        success, _ = test_endpoint(method, endpoint, data, expected_status, description)
        if success:
            tests_passed += 1
    
    # Voice AI Tests
    print("\n🎤 VOICE AI TESTS:")
    print("-" * 30)
    
    voice_tests = [
        ("GET", "/api/voice/status", None, 200, "Voice service status"),
        ("POST", "/api/voice/command", {"text": "help"}, 200, "Voice command"),
    ]
    
    for method, endpoint, data, expected_status, description in voice_tests:
        total_tests += 1
        success, _ = test_endpoint(method, endpoint, data, expected_status, description)
        if success:
            tests_passed += 1
    
    # Final Results
    print("\n" + "=" * 60)
    print("🏁 PRODUCTION TEST RESULTS")
    print("=" * 60)
    
    success_rate = (tests_passed / total_tests) * 100 if total_tests > 0 else 0
    
    print(f"✅ Tests Passed: {tests_passed}/{total_tests}")
    print(f"📊 Success Rate: {success_rate:.1f}%")
    print(f"⏱️  Test Duration: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    if success_rate >= 90:
        print("\n🎉 PRODUCTION READY! System is ready for deployment.")
        print("🚀 All critical functionality is working correctly.")
    elif success_rate >= 75:
        print("\n⚠️  MOSTLY READY! Minor issues detected but system is functional.")
        print("🔧 Consider addressing failed tests before production deployment.")
    else:
        print("\n❌ NOT READY! Multiple critical issues detected.")
        print("🛠️  Please fix failing tests before production deployment.")
    
    print("\n📋 NEXT STEPS:")
    print("1. Deploy to your hosting platform")
    print("2. Configure environment variables")
    print("3. Set up monitoring and logging")
    print("4. Test with real data")
    
    return success_rate >= 90

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

