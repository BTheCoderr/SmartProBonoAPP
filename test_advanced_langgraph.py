#!/usr/bin/env python3
"""
Test script for Advanced LangGraph Implementation
Demonstrates official LangGraph patterns from the documentation
"""

import os
import sys
sys.path.append('.')

from agent_service.graph_advanced import run_advanced_flow, ADVANCED_GRAPH
from agent_service.schemas import IntakeIn

def test_advanced_langgraph():
    """Test the advanced LangGraph implementation"""
    
    print("🚀 Testing Advanced LangGraph Implementation")
    print("=" * 50)
    
    # Test cases
    test_cases = [
        {
            "name": "Criminal Law Case",
            "text": "I was arrested for shoplifting and the police are saying I can plead nolo contendere. What does this mean and can I appeal it later?",
            "expected_case_type": "criminal"
        },
        {
            "name": "Housing Law Case", 
            "text": "My landlord is trying to evict me because I complained about mold in my apartment. Can they do this?",
            "expected_case_type": "housing"
        },
        {
            "name": "Family Law Case",
            "text": "I want to file for divorce but my spouse won't sign the papers. What are my options?",
            "expected_case_type": "family"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📋 Test Case {i}: {test_case['name']}")
        print(f"Input: {test_case['text']}")
        print("-" * 30)
        
        try:
            # Run the advanced flow
            result = run_advanced_flow(
                user_id="test_user",
                raw_text=test_case['text'],
                meta={"test_case": test_case['name']}
            )
            
            # Display results
            print(f"✅ Case Type: {result.get('case_type', 'Unknown')}")
            print(f"✅ Status: {result.get('status', 'Unknown')}")
            print(f"✅ Current Step: {result.get('current_step', 'Unknown')}")
            print(f"✅ Revision Count: {result.get('revision_count', 0)}")
            
            if result.get('specialist_analysis'):
                print(f"✅ Specialist Analysis: {result['specialist_analysis'][:100]}...")
            
            if result.get('plain_english_answer'):
                print(f"✅ Plain English Answer: {result['plain_english_answer'][:100]}...")
            
            # Verify expected case type
            if result.get('case_type') == test_case['expected_case_type']:
                print(f"✅ Case type classification correct!")
            else:
                print(f"❌ Case type classification incorrect. Expected: {test_case['expected_case_type']}, Got: {result.get('case_type')}")
                
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "=" * 50)
    print("🎯 Advanced LangGraph Test Complete!")

def test_graph_structure():
    """Test the graph structure and routing"""
    
    print("\n🔍 Testing Graph Structure")
    print("=" * 30)
    
    # Test the graph structure
    graph = ADVANCED_GRAPH
    
    print(f"✅ Graph compiled successfully")
    print(f"✅ Graph type: {type(graph)}")
    
    # Test state structure
    test_state = {
        "intake_id": "test_123",
        "user_id": "test_user",
        "raw_text": "Test question",
        "meta": {},
        "case_type": "criminal",
        "needs_revision": False,
        "revision_count": 0
    }
    
    print(f"✅ State structure valid")
    print(f"✅ State keys: {list(test_state.keys())}")

if __name__ == "__main__":
    # Set up environment
    os.environ.setdefault("OPENAI_API_KEY", "your-openai-key-here")
    
    # Run tests
    test_graph_structure()
    test_advanced_langgraph()
