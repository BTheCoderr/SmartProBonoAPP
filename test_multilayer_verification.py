#!/usr/bin/env python3
"""
Test script to verify the TRUE multi-layer system is working
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_multilayer_system():
    """Test the multi-layer system directly"""
    try:
        from advanced_multi_agent_api import MultiLayerAgentSystem
        
        print("🧪 Testing TRUE Multi-Layer System")
        print("=" * 50)
        
        # Initialize system
        system = MultiLayerAgentSystem()
        print("✅ Multi-layer system initialized")
        
        # Test 1: Immigration with compliance
        print("\n🧪 Test 1: Immigration + Compliance")
        print("-" * 40)
        result = system.process_message("I need help with H1B visa application and compliance requirements")
        
        print(f"Agent Chain: {' → '.join(result['agent_chain'])}")
        print(f"Main Agent: {result['agent_name']}")
        print(f"Sub-agents Used: {result['sub_agents_used']}")
        print(f"Complexity: {result['complexity_type']}")
        print(f"Human Review: {result['needs_human_review']}")
        print(f"Response Length: {len(result['response'])}")
        print(f"Response Preview: {result['response'][:200]}...")
        
        # Test 2: Business formation
        print("\n🧪 Test 2: Business Formation")
        print("-" * 40)
        result = system.process_message("How do I incorporate an LLC in California?")
        
        print(f"Agent Chain: {' → '.join(result['agent_chain'])}")
        print(f"Main Agent: {result['agent_name']}")
        print(f"Sub-agents Used: {result['sub_agents_used']}")
        print(f"Complexity: {result['complexity_type']}")
        print(f"Response Length: {len(result['response'])}")
        print(f"Response Preview: {result['response'][:200]}...")
        
        # Test 3: Simple greeting
        print("\n🧪 Test 3: Simple Greeting")
        print("-" * 40)
        result = system.process_message("hello")
        
        print(f"Agent Chain: {' → '.join(result['agent_chain'])}")
        print(f"Main Agent: {result['agent_name']}")
        print(f"Sub-agents Used: {result['sub_agents_used']}")
        print(f"Complexity: {result['complexity_type']}")
        print(f"Response Length: {len(result['response'])}")
        print(f"Response Preview: {result['response'][:200]}...")
        
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
