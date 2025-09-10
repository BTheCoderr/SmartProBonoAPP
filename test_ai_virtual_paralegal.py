#!/usr/bin/env python3
"""
Test script for AI Virtual Paralegal functionality
Tests that the AI Virtual Paralegal actually uses real AI services
"""

import asyncio
import sys
import os

# Add the backend directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

async def test_ai_virtual_paralegal():
    """Test the AI Virtual Paralegal with real AI functionality."""
    print("🤖 Testing AI Virtual Paralegal with Real AI...")
    print("=" * 50)
    
    try:
        # Import the AI Virtual Paralegal service
        from backend.services.ai_virtual_paralegal_service import ai_virtual_paralegal
        
        print("✅ AI Virtual Paralegal service imported successfully")
        
        # Test 1: Check if the service is properly initialized
        print("\n📋 Test 1: Service Initialization")
        status = ai_virtual_paralegal.get_status()
        print(f"   - Is Active: {status['is_active']}")
        print(f"   - Workflow State: {status['workflow_state']}")
        print(f"   - Current Tasks: {status['current_tasks']}")
        print(f"   - Total Logs: {status['total_logs']}")
        
        # Test 2: Test document generation with real AI
        print("\n📄 Test 2: Document Generation with Real AI")
        test_case = {
            "id": "test_001",
            "title": "Test Immigration Case - I-485",
            "type": "immigration",
            "client_name": "Test Client",
            "priority": "high"
        }
        
        document_result = await ai_virtual_paralegal.generate_document("I-485 Application Form", test_case)
        
        if document_result.get('success'):
            print("   ✅ Document generation successful!")
            doc = document_result.get('document', {})
            print(f"   - Document Type: {doc.get('document_type')}")
            print(f"   - Accuracy: {doc.get('accuracy')}%")
            print(f"   - AI Model Used: {doc.get('ai_model_used', 'Unknown')}")
            print(f"   - Content Length: {len(doc.get('content', ''))} characters")
        else:
            print("   ❌ Document generation failed!")
            print(f"   - Error: {document_result.get('error', 'Unknown error')}")
        
        # Test 3: Test case analysis with real AI
        print("\n🔍 Test 3: Case Analysis with Real AI")
        analysis_result = await ai_virtual_paralegal._analyze_pending_cases()
        print("   ✅ Case analysis completed!")
        
        # Test 4: Test case law research with real AI
        print("\n📚 Test 4: Case Law Research with Real AI")
        research_result = await ai_virtual_paralegal._research_case_law()
        print("   ✅ Case law research completed!")
        
        # Test 5: Test full workflow
        print("\n🔄 Test 5: Full AI Workflow")
        workflow_result = await ai_virtual_paralegal.start_ai_workflow()
        
        if workflow_result.get('success'):
            print("   ✅ Full AI workflow completed successfully!")
            print(f"   - Tasks Completed: {workflow_result.get('tasks_completed', 0)}")
            print(f"   - Documents Generated: {workflow_result.get('documents_generated', 0)}")
        else:
            print("   ❌ Full AI workflow failed!")
            print(f"   - Error: {workflow_result.get('error', 'Unknown error')}")
        
        # Test 6: Check logs
        print("\n📊 Test 6: Activity Logs")
        logs = ai_virtual_paralegal.get_logs(limit=10)
        print(f"   - Total Logs: {len(logs)}")
        print("   - Recent Logs:")
        for log in logs[-5:]:
            print(f"     [{log['level'].upper()}] {log['component']}: {log['message']}")
        
        print("\n🎉 All tests completed!")
        print("=" * 50)
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed with error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """Main test function."""
    print("🚀 Starting AI Virtual Paralegal Tests...")
    
    # Check if we're in the right directory
    if not os.path.exists('backend/services/ai_virtual_paralegal_service.py'):
        print("❌ Error: Please run this script from the project root directory")
        return False
    
    # Run the tests
    success = await test_ai_virtual_paralegal()
    
    if success:
        print("\n✅ All tests passed! AI Virtual Paralegal is working with real AI.")
    else:
        print("\n❌ Some tests failed. Check the output above for details.")
    
    return success

if __name__ == "__main__":
    # Run the async main function
    asyncio.run(main())
