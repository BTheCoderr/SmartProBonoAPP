#!/usr/bin/env python3
"""
Test script for full CourtListener + AI Virtual Paralegal integration
Tests both backend API endpoints and frontend connectivity
"""

import asyncio
import sys
import os
import requests
import json

# Add the backend directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

async def test_backend_apis():
    """Test all backend API endpoints."""
    print("🔧 Testing Backend API Endpoints...")
    print("=" * 50)
    
    base_url = "http://localhost:3001"
    
    # Test 1: AI Virtual Paralegal Status
    print("\n📊 Test 1: AI Virtual Paralegal Status")
    try:
        response = requests.get(f"{base_url}/api/v1/ai-virtual-paralegal/status")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Status API working: {data.get('success', False)}")
            print(f"   - Is Active: {data.get('status', {}).get('is_active', False)}")
            print(f"   - Workflow State: {data.get('status', {}).get('workflow_state', 'unknown')}")
        else:
            print(f"   ❌ Status API failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Status API error: {e}")
    
    # Test 2: CourtListener Case Search
    print("\n🔍 Test 2: CourtListener Case Search")
    try:
        response = requests.post(f"{base_url}/api/v1/ai-virtual-paralegal/search-cases", 
                               json={
                                   "query": "immigration",
                                   "case_type": "civil",
                                   "limit": 5
                               })
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print(f"   ✅ Case search working: {data.get('total_results', 0)} cases found")
                cases = data.get('cases', [])
                for i, case in enumerate(cases[:3], 1):
                    print(f"   {i}. {case.get('case_name', 'Unknown')} - {case.get('court', 'Unknown')}")
            else:
                print(f"   ❌ Case search failed: {data.get('error', 'Unknown error')}")
        else:
            print(f"   ❌ Case search API failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Case search error: {e}")
    
    # Test 3: Similar Cases Search
    print("\n🔍 Test 3: Similar Cases Search")
    try:
        response = requests.post(f"{base_url}/api/v1/ai-virtual-paralegal/similar-cases",
                               json={
                                   "case_data": {
                                       "title": "Immigration Case - I-485",
                                       "type": "immigration",
                                       "client_name": "Test Client"
                                   },
                                   "limit": 3
                               })
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                similar_cases = data.get('similar_cases', [])
                print(f"   ✅ Similar cases working: {len(similar_cases)} cases found")
                for i, case in enumerate(similar_cases[:2], 1):
                    print(f"   {i}. {case.get('case_name', 'Unknown')} - {case.get('court', 'Unknown')}")
            else:
                print(f"   ❌ Similar cases failed: {data.get('error', 'Unknown error')}")
        else:
            print(f"   ❌ Similar cases API failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Similar cases error: {e}")
    
    # Test 4: Recent Cases
    print("\n📅 Test 4: Recent Cases")
    try:
        response = requests.get(f"{base_url}/api/v1/ai-virtual-paralegal/recent-cases?days=30&limit=5")
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                cases = data.get('cases', [])
                print(f"   ✅ Recent cases working: {len(cases)} cases found")
                for i, case in enumerate(cases[:2], 1):
                    print(f"   {i}. {case.get('case_name', 'Unknown')} - {case.get('date_filed', 'Unknown')}")
            else:
                print(f"   ❌ Recent cases failed: {data.get('error', 'Unknown error')}")
        else:
            print(f"   ❌ Recent cases API failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Recent cases error: {e}")
    
    # Test 5: AI Workflow Start
    print("\n🤖 Test 5: AI Workflow Start")
    try:
        response = requests.post(f"{base_url}/api/v1/ai-virtual-paralegal/start")
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print(f"   ✅ AI workflow started successfully")
                print(f"   - Tasks Completed: {data.get('tasks_completed', 0)}")
                print(f"   - Documents Generated: {data.get('documents_generated', 0)}")
            else:
                print(f"   ❌ AI workflow failed: {data.get('error', 'Unknown error')}")
        else:
            print(f"   ❌ AI workflow API failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ AI workflow error: {e}")
    
    # Test 6: Dashboard Data
    print("\n📊 Test 6: Dashboard Data")
    try:
        response = requests.get(f"{base_url}/api/v1/ai-virtual-paralegal/dashboard")
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                dashboard = data.get('dashboard', {})
                print(f"   ✅ Dashboard working")
                print(f"   - Capabilities: {len(dashboard.get('capabilities', []))}")
                print(f"   - Workflow Steps: {len(dashboard.get('workflow_steps', []))}")
                stats = dashboard.get('statistics', {})
                print(f"   - Cases Processed: {stats.get('cases_processed_today', 0)}")
                print(f"   - Documents Generated: {stats.get('documents_generated', 0)}")
            else:
                print(f"   ❌ Dashboard failed: {data.get('error', 'Unknown error')}")
        else:
            print(f"   ❌ Dashboard API failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Dashboard error: {e}")

async def test_services():
    """Test the backend services directly."""
    print("\n🔧 Testing Backend Services...")
    print("=" * 50)
    
    try:
        # Import services
        from backend.services.courtlistener_service import courtlistener_service
        from backend.services.ai_virtual_paralegal_service import ai_virtual_paralegal
        
        print("✅ Services imported successfully")
        
        # Test CourtListener Service
        print("\n⚖️ Testing CourtListener Service")
        search_result = courtlistener_service.search_cases("immigration", limit=3)
        if search_result.get('success'):
            print(f"   ✅ CourtListener search: {search_result.get('total_results', 0)} cases found")
        else:
            print(f"   ❌ CourtListener search failed: {search_result.get('error', 'Unknown error')}")
        
        # Test AI Virtual Paralegal Service
        print("\n🤖 Testing AI Virtual Paralegal Service")
        status = ai_virtual_paralegal.get_status()
        print(f"   ✅ AI Virtual Paralegal status: {status.get('is_active', False)}")
        
        # Test document generation
        test_case = {
            "id": "test_001",
            "title": "Test Immigration Case",
            "type": "immigration",
            "client_name": "Test Client"
        }
        
        doc_result = await ai_virtual_paralegal.generate_document("I-485 Application Form", test_case)
        if doc_result.get('success'):
            print(f"   ✅ Document generation: {doc_result.get('document', {}).get('accuracy', 0)}% accuracy")
        else:
            print(f"   ❌ Document generation failed: {doc_result.get('error', 'Unknown error')}")
        
    except Exception as e:
        print(f"❌ Service test error: {e}")
        import traceback
        traceback.print_exc()

async def main():
    """Main test function."""
    print("🚀 Starting Full Integration Tests...")
    print("=" * 60)
    
    # Check if we're in the right directory
    if not os.path.exists('backend/services/courtlistener_service.py'):
        print("❌ Error: Please run this script from the project root directory")
        return False
    
    # Test backend services
    await test_services()
    
    # Test API endpoints (only if server is running)
    print("\n🌐 Testing API Endpoints (requires running server)...")
    try:
        await test_backend_apis()
    except Exception as e:
        print(f"⚠️ API tests skipped (server not running): {e}")
    
    print("\n🎉 Integration tests completed!")
    print("=" * 60)
    
    return True

if __name__ == "__main__":
    # Run the async main function
    asyncio.run(main())
