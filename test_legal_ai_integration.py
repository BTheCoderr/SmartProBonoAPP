#!/usr/bin/env python3
"""
Test script for Legal AI Integration
Tests the integration between the main backend and legal AI backend
"""

import sys
import os
import requests
import json
from datetime import datetime

# Add the legal_ai_backend to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'legal_ai_backend'))

def test_legal_ai_backend_direct():
    """Test the legal AI backend directly"""
    print("🧪 Testing Legal AI Backend Directly...")
    
    try:
        from langgraph.main_graph import run_pipeline
        
        # Test with a simple query
        test_query = "I was charged with gun possession in Rhode Island, what should I do?"
        print(f"Query: {test_query}")
        
        result = run_pipeline(test_query)
        
        print("✅ Legal AI Backend Response:")
        print(f"Success: {result.get('success', False)}")
        print(f"Analysis: {result.get('analysis', {}).get('case_summary', 'No summary')[:200]}...")
        print(f"Disclaimers: {len(result.get('disclaimers', []))}")
        print(f"Warnings: {len(result.get('warnings', []))}")
        
        return True
        
    except ImportError as e:
        print(f"❌ Legal AI Backend not available: {e}")
        return False
    except Exception as e:
        print(f"❌ Error testing Legal AI Backend: {e}")
        return False

def test_backend_api():
    """Test the backend API endpoint"""
    print("\n🧪 Testing Backend API Endpoint...")
    
    try:
        # Test the legal analysis endpoint
        url = "http://localhost:3001/api/legal-analysis"
        payload = {
            "query": "I need help with a landlord dispute in Massachusetts",
            "jurisdiction": "ma"
        }
        
        response = requests.post(url, json=payload, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Backend API Response:")
            print(f"Success: {data.get('success', False)}")
            print(f"Source: {data.get('source', 'unknown')}")
            print(f"Analysis: {data.get('analysis', {}).get('case_summary', 'No summary')[:200]}...")
            print(f"Disclaimers: {len(data.get('disclaimers', []))}")
            return True
        else:
            print(f"❌ API Error: {response.status_code} - {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Backend server not running. Please start the backend server first.")
        return False
    except Exception as e:
        print(f"❌ Error testing API: {e}")
        return False

def test_frontend_integration():
    """Test the frontend integration"""
    print("\n🧪 Testing Frontend Integration...")
    
    try:
        # Test if frontend is running
        response = requests.get("http://localhost:3002", timeout=10)
        
        if response.status_code == 200:
            print("✅ Frontend is running")
            return True
        else:
            print(f"❌ Frontend error: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Frontend not running. Please start the frontend first.")
        return False
    except Exception as e:
        print(f"❌ Error testing frontend: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Legal AI Integration Test Suite")
    print("=" * 50)
    
    # Test 1: Legal AI Backend Direct
    backend_direct = test_legal_ai_backend_direct()
    
    # Test 2: Backend API
    backend_api = test_backend_api()
    
    # Test 3: Frontend Integration
    frontend = test_frontend_integration()
    
    print("\n📊 Test Results Summary:")
    print("=" * 50)
    print(f"Legal AI Backend Direct: {'✅ PASS' if backend_direct else '❌ FAIL'}")
    print(f"Backend API Endpoint: {'✅ PASS' if backend_api else '❌ FAIL'}")
    print(f"Frontend Integration: {'✅ PASS' if frontend else '❌ FAIL'}")
    
    if all([backend_direct, backend_api, frontend]):
        print("\n🎉 All tests passed! Legal AI integration is working correctly.")
    else:
        print("\n⚠️  Some tests failed. Please check the errors above.")
        
        if not backend_direct:
            print("\n💡 To fix Legal AI Backend issues:")
            print("   1. Install dependencies: pip install -r legal_ai_backend/requirements.txt")
            print("   2. Set up environment variables (ANTHROPIC_API_KEY)")
            print("   3. Check that all agents are properly implemented")
            
        if not backend_api:
            print("\n💡 To fix Backend API issues:")
            print("   1. Start the backend server: cd backend && python combined_server.py")
            print("   2. Check that the legal_ai route is properly registered")
            print("   3. Verify the legal AI backend is accessible")
            
        if not frontend:
            print("\n💡 To fix Frontend issues:")
            print("   1. Start the frontend: cd frontend && npm start")
            print("   2. Check that the API endpoint URL is correct")

if __name__ == "__main__":
    main()
