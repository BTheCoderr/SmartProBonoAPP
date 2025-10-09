#!/usr/bin/env python3
"""
Test Multi-Agent System with FREE Models
Tests all 6 agents and multi-agent collaboration
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:3001/api/multi-agent"

def print_header(title):
    """Print formatted header"""
    print("\n" + "=" * 60)
    print(f"🤖 {title}")
    print("=" * 60)

def test_get_agents():
    """Test getting list of agents"""
    print_header("Testing: Get Available Agents")
    
    try:
        response = requests.get(f"{BASE_URL}/agents", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Success!")
            print(f"Total Agents: {data['agents']['total_agents']}")
            print(f"Gemini Available: {data['agents']['gemini_available']}")
            print(f"Gemini Free Tier: {data['agents']['gemini_free_tier']}")
            
            print("\n📋 Available Agents:")
            for agent_id, agent in data['agents']['agents'].items():
                print(f"  • {agent['name']} ({agent['model']})")
                print(f"    └─ {agent['description']}")
            
            return True
        else:
            print(f"❌ Failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_agent(agent_endpoint, payload, agent_name):
    """Test a specific agent endpoint"""
    print_header(f"Testing: {agent_name}")
    
    try:
        response = requests.post(
            f"{BASE_URL}/{agent_endpoint}",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=60
        )
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get('success'):
                print(f"✅ Success!")
                print(f"Agent: {data.get('agent', 'Unknown')}")
                print(f"Model: {data.get('model', 'Unknown')}")
                print(f"Response Length: {len(data.get('text', ''))} chars")
                print(f"\n📄 Response Preview:")
                print(data.get('text', '')[:300] + "...")
                return True
            else:
                print(f"⚠️ Agent returned failure: {data.get('error', 'Unknown error')}")
                return False
        else:
            print(f"❌ Failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_auto_routing():
    """Test automatic agent routing"""
    print_header("Testing: Auto-Routing (Smart Agent Selection)")
    
    test_cases = [
        {
            "message": "Research tenant rights case law",
            "expected_agent": "Legal Research Agent"
        },
        {
            "message": "Analyze this contract",
            "expected_agent": "Document Analysis Agent"
        },
        {
            "message": "What's the deadline for case #123?",
            "expected_agent": "Case Manager Agent"
        },
        {
            "message": "How do I file a motion?",
            "expected_agent": "Court Filing Agent"
        }
    ]
    
    results = []
    for test_case in test_cases:
        try:
            response = requests.post(
                f"{BASE_URL}/process",
                json={"message": test_case["message"]},
                headers={"Content-Type": "application/json"},
                timeout=60
            )
            
            if response.status_code == 200:
                data = response.json()
                routed_to = data.get('agent', 'Unknown')
                print(f"\n✅ Message: \"{test_case['message']}\"")
                print(f"   Routed to: {routed_to}")
                results.append(data.get('success', False))
            else:
                print(f"\n❌ Failed to route message: {test_case['message']}")
                results.append(False)
                
        except Exception as e:
            print(f"\n❌ Error: {e}")
            results.append(False)
    
    return all(results)

def test_multi_agent_collaboration():
    """Test multi-agent collaboration"""
    print_header("Testing: Multi-Agent Collaboration")
    
    try:
        response = requests.post(
            f"{BASE_URL}/collaborate",
            json={
                "message": "Help me understand my tenant rights and how to file a complaint",
                "agents": ["legal_research", "document_analysis", "court_filing"]
            },
            headers={"Content-Type": "application/json"},
            timeout=120  # Longer for multi-agent
        )
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get('success'):
                print(f"✅ Success!")
                print(f"Agents Consulted: {data.get('agents_consulted', 0)}")
                print(f"Total Response Length: {len(data.get('text', ''))} chars")
                
                if 'individual_responses' in data:
                    print(f"\n📋 Individual Agent Responses:")
                    for response in data['individual_responses']:
                        print(f"\n  🤖 {response['agent_name']}:")
                        print(f"     {response['response'][:150]}...")
                
                return True
            else:
                print(f"⚠️ Collaboration failed: {data.get('error', 'Unknown error')}")
                return False
        else:
            print(f"❌ Failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_system_status():
    """Test system status endpoint"""
    print_header("Testing: System Status")
    
    try:
        response = requests.get(f"{BASE_URL}/status", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Success!")
            print(f"Status: {data.get('status', 'Unknown')}")
            print(f"Free Models: {data.get('free_models', False)}")
            print(f"Message: {data.get('message', 'N/A')}")
            
            if 'endpoints' in data:
                print(f"\n📋 Available Endpoints:")
                for endpoint, description in data['endpoints'].items():
                    print(f"  • {endpoint}: {description}")
            
            return True
        else:
            print(f"❌ Failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Run all tests"""
    print("\n🚀 MULTI-AGENT SYSTEM TEST SUITE")
    print("Testing FREE models: Ollama + Google Gemini")
    print(f"Timestamp: {datetime.now().isoformat()}")
    
    results = []
    
    # Test 1: Get agents
    results.append(("Get Agents", test_get_agents()))
    
    # Test 2: System status
    results.append(("System Status", test_system_status()))
    
    # Test 3: Legal Research Agent
    results.append(("Legal Research Agent", test_agent(
        "legal-research",
        {"query": "What are the key precedents for tenant rights in wrongful eviction cases?"},
        "Legal Research Agent"
    )))
    
    # Test 4: Document Analysis Agent
    results.append(("Document Analysis Agent", test_agent(
        "document-analysis",
        {"document": "This lease agreement states that the tenant must pay rent on the 1st of each month..."},
        "Document Analysis Agent"
    )))
    
    # Test 5: Case Management Agent
    results.append(("Case Management Agent", test_agent(
        "case-management",
        {"task": "Track deadlines for case #12345 - wrongful termination lawsuit"},
        "Case Management Agent"
    )))
    
    # Test 6: Client Support Agent
    results.append(("Client Support Agent", test_agent(
        "client-support",
        {"question": "How do I file a small claims case against my landlord?"},
        "Client Support Agent"
    )))
    
    # Test 7: Court Filing Agent
    results.append(("Court Filing Agent", test_agent(
        "court-filing",
        {"filing_task": "Help me prepare a motion to dismiss for lack of jurisdiction"},
        "Court Filing Agent"
    )))
    
    # Test 8: Compliance Agent
    results.append(("Compliance Agent", test_agent(
        "compliance",
        {"compliance_question": "What are the ethical requirements for attorney-client privilege?"},
        "Compliance Agent"
    )))
    
    # Test 9: Auto-routing
    results.append(("Auto-Routing", test_auto_routing()))
    
    # Test 10: Multi-agent collaboration
    results.append(("Multi-Agent Collaboration", test_multi_agent_collaboration()))
    
    # Print summary
    print_header("TEST SUMMARY")
    
    total_tests = len(results)
    passed_tests = sum(1 for _, result in results if result)
    failed_tests = total_tests - passed_tests
    
    print(f"\n📊 Results:")
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status} - {test_name}")
    
    print(f"\n🎯 Overall: {passed_tests}/{total_tests} tests passed")
    
    if passed_tests == total_tests:
        print("\n🎉 ALL TESTS PASSED!")
        print("Your multi-agent system is fully operational with FREE models!")
    else:
        print(f"\n⚠️ {failed_tests} tests failed")
        print("Some agents may need attention or Gemini API key configuration")
    
    print(f"\n💰 Cost: $0/month (100% FREE models)")
    print(f"📋 Agents: 6 specialized agents")
    print(f"🤖 Models: Ollama (3 models) + Gemini (FREE tier)")
    print(f"🌐 System: http://localhost:3001/api/multi-agent")

if __name__ == "__main__":
    main()
