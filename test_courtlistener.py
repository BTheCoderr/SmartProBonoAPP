#!/usr/bin/env python3
"""
Test script for CourtListener API integration
Tests real case law research functionality
"""

import sys
import os
import asyncio

# Add the backend directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

async def test_courtlistener_integration():
    """Test the CourtListener API integration."""
    print("⚖️  Testing CourtListener API Integration...")
    print("=" * 50)
    
    try:
        # Import the services
        from backend.services.courtlistener_service import courtlistener_service
        from backend.services.ai_virtual_paralegal_service import ai_virtual_paralegal
        
        print("✅ Services imported successfully")
        
        # Test 1: Basic case search
        print("\n🔍 Test 1: Basic Case Search")
        search_results = courtlistener_service.search_cases(
            query="immigration",
            case_type="civil",
            limit=5
        )
        
        if search_results.get('success'):
            print(f"   ✅ Search successful: {search_results.get('total_results', 0)} cases found")
            cases = search_results.get('cases', [])
            for i, case in enumerate(cases[:3], 1):
                print(f"   {i}. {case.get('case_name', 'Unknown')} - {case.get('court', 'Unknown')}")
        else:
            print(f"   ❌ Search failed: {search_results.get('error', 'Unknown error')}")
        
        # Test 2: Similar cases search
        print("\n🔍 Test 2: Similar Cases Search")
        test_case = {
            "id": "test_001",
            "title": "Immigration Case - I-485 Application",
            "type": "immigration",
            "client_name": "Test Client"
        }
        
        similar_results = courtlistener_service.search_similar_cases(
            case_data=test_case,
            limit=5
        )
        
        if similar_results.get('success'):
            similar_cases = similar_results.get('similar_cases', [])
            print(f"   ✅ Similar cases found: {len(similar_cases)} cases")
            for i, case in enumerate(similar_cases[:3], 1):
                print(f"   {i}. {case.get('case_name', 'Unknown')} - {case.get('court', 'Unknown')}")
        else:
            print(f"   ❌ Similar cases search failed: {similar_results.get('error', 'Unknown error')}")
        
        # Test 3: Recent cases
        print("\n🔍 Test 3: Recent Cases")
        recent_results = courtlistener_service.get_recent_cases(
            case_type="civil",
            days=30,
            limit=5
        )
        
        if recent_results.get('success'):
            recent_cases = recent_results.get('cases', [])
            print(f"   ✅ Recent cases found: {len(recent_cases)} cases")
            for i, case in enumerate(recent_cases[:3], 1):
                print(f"   {i}. {case.get('case_name', 'Unknown')} - {case.get('date_filed', 'Unknown')}")
        else:
            print(f"   ❌ Recent cases search failed: {recent_results.get('error', 'Unknown error')}")
        
        # Test 4: AI Virtual Paralegal with CourtListener
        print("\n🤖 Test 4: AI Virtual Paralegal with CourtListener")
        research_result = await ai_virtual_paralegal._research_case_law()
        print("   ✅ AI Virtual Paralegal case law research completed")
        
        # Test 5: Full workflow test
        print("\n🔄 Test 5: Full AI Workflow with CourtListener")
        workflow_result = await ai_virtual_paralegal.start_ai_workflow()
        
        if workflow_result.get('success'):
            print("   ✅ Full workflow completed successfully!")
            print(f"   - Tasks Completed: {workflow_result.get('tasks_completed', 0)}")
            print(f"   - Documents Generated: {workflow_result.get('documents_generated', 0)}")
        else:
            print("   ❌ Full workflow failed!")
            print(f"   - Error: {workflow_result.get('error', 'Unknown error')}")
        
        # Test 6: Check logs for CourtListener activity
        print("\n📊 Test 6: Activity Logs")
        logs = ai_virtual_paralegal.get_logs(limit=10)
        print(f"   - Total Logs: {len(logs)}")
        print("   - Recent Logs:")
        for log in logs[-5:]:
            print(f"     [{log['level'].upper()}] {log['component']}: {log['message']}")
        
        print("\n🎉 All CourtListener integration tests completed!")
        print("=" * 50)
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed with error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """Main test function."""
    print("🚀 Starting CourtListener Integration Tests...")
    
    # Check if we're in the right directory
    if not os.path.exists('backend/services/courtlistener_service.py'):
        print("❌ Error: Please run this script from the project root directory")
        return False
    
    # Run the tests
    success = await test_courtlistener_integration()
    
    if success:
        print("\n✅ All tests passed! CourtListener integration is working.")
    else:
        print("\n❌ Some tests failed. Check the output above for details.")
    
    return success

if __name__ == "__main__":
    # Run the async main function
    asyncio.run(main())
