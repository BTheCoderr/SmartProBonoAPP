#!/usr/bin/env python3
"""
Complete CRM Integration Test
Tests the full CRM system with both backend and frontend
"""
import requests
import json
import time
import webbrowser
import os

def test_backend_health():
    """Test backend health"""
    print("🏥 Testing Backend Health...")
    try:
        response = requests.get("http://localhost:3001/api/v1/crm/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Backend healthy: {data['message']}")
            return True
        else:
            print(f"   ❌ Backend unhealthy: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Backend error: {e}")
        return False

def test_frontend_health():
    """Test frontend health"""
    print("🌐 Testing Frontend Health...")
    try:
        response = requests.get("http://localhost:3002", timeout=5)
        if response.status_code == 200:
            print("   ✅ Frontend running on port 3002")
            return True
        else:
            print(f"   ❌ Frontend error: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Frontend error: {e}")
        return False

def test_cors_headers():
    """Test CORS headers"""
    print("🔗 Testing CORS Headers...")
    try:
        # Test preflight request
        response = requests.options(
            "http://localhost:3001/api/v1/crm/health",
            headers={
                'Origin': 'http://localhost:3002',
                'Access-Control-Request-Method': 'GET',
                'Access-Control-Request-Headers': 'Content-Type'
            },
            timeout=5
        )
        
        cors_headers = {
            'Access-Control-Allow-Origin': response.headers.get('Access-Control-Allow-Origin'),
            'Access-Control-Allow-Methods': response.headers.get('Access-Control-Allow-Methods'),
            'Access-Control-Allow-Headers': response.headers.get('Access-Control-Allow-Headers')
        }
        
        if cors_headers['Access-Control-Allow-Origin']:
            print("   ✅ CORS headers present")
            print(f"   📋 Allow-Origin: {cors_headers['Access-Control-Allow-Origin']}")
            print(f"   📋 Allow-Methods: {cors_headers['Access-Control-Allow-Methods']}")
            print(f"   📋 Allow-Headers: {cors_headers['Access-Control-Allow-Headers']}")
            return True
        else:
            print("   ❌ CORS headers missing")
            return False
    except Exception as e:
        print(f"   ❌ CORS test error: {e}")
        return False

def test_crm_endpoints():
    """Test CRM endpoints"""
    print("🔧 Testing CRM Endpoints...")
    endpoints = [
        ("/api/v1/crm/health", "GET", None, 200),
        ("/api/v1/crm/client/intake", "POST", {"test": "data"}, 400),  # Expected validation error
        ("/api/v1/crm/lawyer/clients", "GET", None, 401),  # Expected auth error
        ("/api/v1/crm/bondsman/bonds", "GET", None, 401),  # Expected auth error
        ("/api/v1/crm/dashboard/analytics", "GET", None, 401),  # Expected auth error
    ]
    
    success_count = 0
    for endpoint, method, data, expected_status in endpoints:
        try:
            if method == "GET":
                response = requests.get(f"http://localhost:3001{endpoint}", timeout=5)
            else:
                response = requests.post(
                    f"http://localhost:3001{endpoint}",
                    json=data,
                    headers={'Content-Type': 'application/json'},
                    timeout=5
                )
            
            if response.status_code == expected_status:
                print(f"   ✅ {method} {endpoint}: {response.status_code} (expected)")
                success_count += 1
            else:
                print(f"   ⚠️  {method} {endpoint}: {response.status_code} (expected {expected_status})")
        except Exception as e:
            print(f"   ❌ {method} {endpoint}: Error - {e}")
    
    return success_count == len(endpoints)

def test_client_intake_validation():
    """Test client intake with proper validation"""
    print("📝 Testing Client Intake Validation...")
    try:
        # Test with missing required fields
        response = requests.post(
            "http://localhost:3001/api/v1/crm/client/intake",
            json={"first_name": "John"},
            headers={'Content-Type': 'application/json'},
            timeout=5
        )
        
        if response.status_code == 400:
            data = response.json()
            print(f"   ✅ Validation working: {data.get('error', 'Validation error')}")
            return True
        else:
            print(f"   ❌ Unexpected response: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Validation test error: {e}")
        return False

def open_frontend():
    """Open the frontend in browser"""
    print("🌐 Opening Frontend...")
    try:
        webbrowser.open("http://localhost:3002/virtual-paralegal/crm")
        print("   ✅ Frontend opened in browser")
        return True
    except Exception as e:
        print(f"   ❌ Error opening frontend: {e}")
        return False

def main():
    """Run complete integration test"""
    print("🚀 SmartProBono CRM Full Integration Test")
    print("=" * 60)
    
    # Test backend
    backend_ok = test_backend_health()
    
    # Test frontend
    frontend_ok = test_frontend_health()
    
    # Test CORS
    cors_ok = test_cors_headers()
    
    # Test CRM endpoints
    endpoints_ok = test_crm_endpoints()
    
    # Test validation
    validation_ok = test_client_intake_validation()
    
    print("\n" + "=" * 60)
    print("🎯 Integration Test Results:")
    print(f"   Backend Health: {'✅' if backend_ok else '❌'}")
    print(f"   Frontend Health: {'✅' if frontend_ok else '❌'}")
    print(f"   CORS Headers: {'✅' if cors_ok else '❌'}")
    print(f"   CRM Endpoints: {'✅' if endpoints_ok else '❌'}")
    print(f"   Validation: {'✅' if validation_ok else '❌'}")
    
    if all([backend_ok, frontend_ok, cors_ok, endpoints_ok, validation_ok]):
        print("\n🎉 ALL TESTS PASSED! CRM System is fully operational!")
        print("\n📋 Next Steps:")
        print("1. 🌐 Frontend: http://localhost:3002/virtual-paralegal/crm")
        print("2. 🔧 Backend API: http://localhost:3001/api/v1/crm/health")
        print("3. 📝 Test HTML: Open test_crm_frontend.html in browser")
        print("4. 🧪 Full Workflow: Create client intakes, cases, and test features")
        
        # Open frontend
        open_frontend()
        
    else:
        print("\n❌ Some tests failed. Check the errors above.")
    
    print("=" * 60)

if __name__ == "__main__":
    main()
