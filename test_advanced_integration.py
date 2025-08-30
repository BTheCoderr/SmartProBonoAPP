#!/usr/bin/env python3
"""
Test Advanced LangGraph Integration
Tests all the new features: checkpointing, human-in-the-loop, parallel execution
"""

import os
import sys
import requests
import time
import json
sys.path.append('.')

def test_langgraph_service():
    """Test the LangGraph service endpoints"""
    
    print("🚀 Testing Advanced LangGraph Integration")
    print("=" * 50)
    
    base_url = "http://localhost:8010"
    
    # Test health endpoint
    print("\n1. 🔍 Testing Health Endpoint")
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            print("✅ Health endpoint working")
        else:
            print(f"❌ Health endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Cannot connect to service: {e}")
        return False
    
    # Test graph info endpoint
    print("\n2. 📊 Testing Graph Info Endpoint")
    try:
        response = requests.get(f"{base_url}/graph/info")
        if response.status_code == 200:
            info = response.json()
            print("✅ Graph info endpoint working")
            print(f"   LangSmith tracing: {info.get('langsmith_tracing', False)}")
            print(f"   Human review enabled: {info.get('human_review_enabled', False)}")
            print(f"   Parallel execution enabled: {info.get('parallel_execution_enabled', False)}")
        else:
            print(f"❌ Graph info endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Graph info endpoint error: {e}")
    
    # Test simple intake
    print("\n3. 🔄 Testing Simple Intake")
    try:
        payload = {
            "user_id": "test_user",
            "full_text": "I need help with a landlord dispute",
            "meta": {"test": True}
        }
        response = requests.post(f"{base_url}/intake/run", json=payload)
        if response.status_code == 200:
            result = response.json()
            print("✅ Simple intake working")
            print(f"   Result keys: {list(result.get('result', {}).keys())}")
        else:
            print(f"❌ Simple intake failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Simple intake error: {e}")
    
    # Test advanced intake
    print("\n4. 🚀 Testing Advanced Intake")
    try:
        payload = {
            "user_id": "test_user",
            "full_text": "I was arrested for shoplifting and want to know about nolo contendere pleas",
            "meta": {"test": True, "case_type": "criminal"}
        }
        response = requests.post(f"{base_url}/intake/advanced", json=payload)
        if response.status_code == 200:
            result = response.json()
            print("✅ Advanced intake working")
            result_data = result.get('result', {})
            print(f"   Case type: {result_data.get('case_type', 'Unknown')}")
            print(f"   Status: {result_data.get('status', 'Unknown')}")
            print(f"   Current step: {result_data.get('current_step', 'Unknown')}")
            print(f"   Revision count: {result_data.get('revision_count', 0)}")
        else:
            print(f"❌ Advanced intake failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Advanced intake error: {e}")
    
    # Test human review endpoints
    print("\n5. 👥 Testing Human Review Endpoints")
    try:
        response = requests.get(f"{base_url}/human-reviews/pending")
        if response.status_code == 200:
            reviews = response.json()
            print("✅ Human review endpoints working")
            print(f"   Pending reviews: {len(reviews.get('reviews', []))}")
        else:
            print(f"❌ Human review endpoints failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Human review endpoints error: {e}")
    
    # Test intakes listing
    print("\n6. 📋 Testing Intakes Listing")
    try:
        response = requests.get(f"{base_url}/intakes?limit=5")
        if response.status_code == 200:
            intakes = response.json()
            print("✅ Intakes listing working")
            print(f"   Intakes found: {len(intakes.get('intakes', []))}")
        else:
            print(f"❌ Intakes listing failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Intakes listing error: {e}")
    
    print("\n" + "=" * 50)
    print("🎯 Advanced Integration Test Complete!")

def test_environment_setup():
    """Test environment setup"""
    
    print("\n🔧 Testing Environment Setup")
    print("-" * 30)
    
    # Check environment variables
    env_vars = [
        "LANGCHAIN_TRACING_V2",
        "LANGCHAIN_PROJECT", 
        "ENABLE_HUMAN_REVIEW",
        "ENABLE_PARALLEL_EXECUTION",
        "SUPABASE_URL",
        "SUPABASE_SERVICE_ROLE_KEY"
    ]
    
    for var in env_vars:
        value = os.environ.get(var)
        if value:
            print(f"✅ {var}: {value}")
        else:
            print(f"❌ {var}: Not set")
    
    # Check if service is running
    try:
        response = requests.get("http://localhost:8010/health", timeout=5)
        if response.status_code == 200:
            print("✅ LangGraph service is running")
        else:
            print("❌ LangGraph service not responding")
    except:
        print("❌ LangGraph service not running")

def test_advanced_features():
    """Test advanced features individually"""
    
    print("\n🧪 Testing Advanced Features")
    print("-" * 30)
    
    # Test checkpointing
    print("1. Checkpointing:")
    try:
        from agent_service.checkpointing import get_checkpoint_saver
        saver = get_checkpoint_saver()
        checkpoint_id = saver.save_checkpoint("test_thread", {"test": "data"})
        if checkpoint_id:
            print("   ✅ Checkpointing working")
        else:
            print("   ❌ Checkpointing failed")
    except Exception as e:
        print(f"   ❌ Checkpointing error: {e}")
    
    # Test human-in-the-loop
    print("2. Human-in-the-loop:")
    try:
        from agent_service.human_in_loop import human_manager
        print("   ✅ Human-in-the-loop manager loaded")
    except Exception as e:
        print(f"   ❌ Human-in-the-loop error: {e}")
    
    # Test parallel execution
    print("3. Parallel execution:")
    try:
        from agent_service.parallel_execution import parallel_executor, specialist_pool
        print("   ✅ Parallel execution system loaded")
    except Exception as e:
        print(f"   ❌ Parallel execution error: {e}")

if __name__ == "__main__":
    # Set up environment
    os.environ.setdefault("OPENAI_API_KEY", "your-openai-key-here")
    os.environ.setdefault("SUPABASE_URL", "https://ewtcvsohdgkthuyajyyk.supabase.co")
    os.environ.setdefault("SUPABASE_SERVICE_ROLE_KEY", "***REMOVED***")
    
    # Run tests
    test_environment_setup()
    test_advanced_features()
    test_langgraph_service()
