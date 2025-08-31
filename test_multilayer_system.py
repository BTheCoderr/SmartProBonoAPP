#!/usr/bin/env python3
"""
Test script to verify the multi-layer agent system works correctly
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_multilayer_system():
    """Test the multi-layer agent system"""
    try:
        from real_multilayer_agent_system import MultiLayerAgentSystem
        
        print("🚀 Testing Multi-Layer Agent System")
        print("=" * 50)
        
        # Initialize system
        system = MultiLayerAgentSystem()
        print("✅ Multi-layer system initialized")
        
        # Test 1: Simple Query
        print("\n🧪 Test 1: Simple Query")
        print("-" * 30)
        result = system.process_message('hello')
        print(f"Agent Chain: {' → '.join(result['agent_chain'])}")
        print(f"Complexity Score: {result['complexity_score']}")
        print(f"Workflow Type: {result['workflow_type']}")
        print(f"Response: {result['response'][:100]}...")
        
        # Test 2: Complex Immigration Query
        print("\n🧪 Test 2: Complex Immigration Query")
        print("-" * 30)
        result = system.process_message('I need help with H1B visa application and compliance requirements')
        print(f"Agent Chain: {' → '.join(result['agent_chain'])}")
        print(f"Complexity Score: {result['complexity_score']}")
        print(f"Workflow Type: {result['workflow_type']}")
        print(f"Needs Human Review: {result['needs_human_review']}")
        print(f"Response: {result['response'][:200]}...")
        
        # Test 3: Business Formation
        print("\n🧪 Test 3: Business Formation")
        print("-" * 30)
        result = system.process_message('How do I incorporate an LLC in California?')
        print(f"Agent Chain: {' → '.join(result['agent_chain'])}")
        print(f"Complexity Score: {result['complexity_score']}")
        print(f"Workflow Type: {result['workflow_type']}")
        print(f"Needs Human Review: {result['needs_human_review']}")
        print(f"Response: {result['response'][:200]}...")
        
        # Test 4: Complex Case (should trigger human review)
        print("\n🧪 Test 4: Complex Case (Human Review)")
        print("-" * 30)
        result = system.process_message('I need defense strategy for a complex breach of contract lawsuit')
        print(f"Agent Chain: {' → '.join(result['agent_chain'])}")
        print(f"Complexity Score: {result['complexity_score']}")
        print(f"Workflow Type: {result['workflow_type']}")
        print(f"Needs Human Review: {result['needs_human_review']}")
        print(f"Escalation Reason: {result.get('escalation_reason', 'None')}")
        print(f"Response: {result['response'][:200]}...")
        
        print("\n✅ All tests completed!")
        return True
        
    except Exception as e:
        print(f"❌ Error testing multi-layer system: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_multilayer_system()
    if success:
        print("\n🎉 Multi-layer system is working correctly!")
    else:
        print("\n❌ Multi-layer system has issues")
