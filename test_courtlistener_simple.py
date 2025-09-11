#!/usr/bin/env python3
"""
Simple CourtListener API Test
Tests the CourtListener integration without requiring the full Flask app
"""

import os
import sys
from datetime import datetime, timedelta

# Add the backend directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'backend')))

from services.courtlistener_service import CourtListenerService

def test_courtlistener_simple():
    """Test CourtListener service directly"""
    print("🔍 Testing CourtListener API Integration (Simple)")
    print("=" * 60)
    
    # Create service instance
    courtlistener = CourtListenerService()
    
    print(f"🔑 API Key Status: {'✅ Found' if courtlistener.api_key else '⚠️ Not found (using fallback)'}")
    print(f"🌐 API URL: {courtlistener.base_url}")
    print(f"📊 Fallback Mode: {'Yes' if courtlistener.fallback_mode else 'No'}")
    
    # Test 1: Search Cases
    print("\n📊 Test 1: Search Cases")
    print("-" * 40)
    search_query = "immigration"
    search_results = courtlistener.search_cases(query=search_query, limit=3)
    
    if search_results['success']:
        print(f"✅ Search successful: {search_results['total_results']} cases found")
        print(f"   Query: '{search_results['query']}'")
        print(f"   Fallback mode: {search_results.get('fallback_mode', False)}")
        
        for i, case in enumerate(search_results['cases'][:3], 1):
            print(f"   Case {i}: {case.get('case_name', 'N/A')}")
            print(f"   Court: {case.get('court', 'N/A')}")
            print(f"   Date: {case.get('date_filed', 'N/A')}")
            print(f"   Type: {case.get('case_type', 'N/A')}")
            print()
    else:
        print(f"❌ Search failed: {search_results['error']}")
    
    # Test 2: Recent Cases
    print("\n📅 Test 2: Recent Cases")
    print("-" * 40)
    recent_results = courtlistener.get_recent_cases(days=30, limit=3)
    
    if recent_results['success']:
        print(f"✅ Recent cases successful: {recent_results['total_results']} cases found")
        print(f"   Date range: {recent_results['date_range']['start']} to {recent_results['date_range']['end']}")
        print(f"   Fallback mode: {recent_results.get('fallback_mode', False)}")
        
        for i, case in enumerate(recent_results['cases'][:3], 1):
            print(f"   Case {i}: {case.get('case_name', 'N/A')}")
            print(f"   Court: {case.get('court', 'N/A')}")
            print(f"   Date: {case.get('date_filed', 'N/A')}")
            print()
    else:
        print(f"❌ Recent cases failed: {recent_results['error']}")
    
    # Test 3: Similar Cases
    print("\n🔍 Test 3: Similar Cases")
    print("-" * 40)
    case_data = {
        'title': 'immigration case involving work visa',
        'type': 'immigration',
        'client_name': 'Test Client'
    }
    similar_results = courtlistener.search_similar_cases(
        case_data=case_data,
        limit=3
    )
    
    if similar_results['success']:
        cases = similar_results.get('similar_cases', [])
        print(f"✅ Similar cases successful: {len(cases)} cases found")
        print(f"   Query: '{similar_results.get('query', 'N/A')}'")
        print(f"   Fallback mode: {similar_results.get('fallback_mode', False)}")
        
        for i, case in enumerate(cases[:3], 1):
            print(f"   Case {i}: {case.get('case_name', 'N/A')}")
            print(f"   Court: {case.get('court', 'N/A')}")
            print(f"   Similarity: {case.get('similarity_score', 'N/A')}")
            print()
    else:
        print(f"❌ Similar cases failed: {similar_results['error']}")
    
    # Test 4: API Status
    print("\n🔑 Test 4: API Configuration")
    print("-" * 40)
    print(f"Base URL: {courtlistener.base_url}")
    print(f"Search URL: {courtlistener.search_url}")
    print(f"Opinions URL: {courtlistener.opinions_url}")
    print(f"API Key: {'Set' if courtlistener.api_key else 'Not set'}")
    print(f"Headers: {courtlistener.headers}")
    print(f"Rate limiting: {courtlistener.min_request_interval}s between requests")
    
    print("\n🎉 CourtListener integration test completed!")
    print("=" * 60)
    
    if courtlistener.fallback_mode:
        print("\n💡 To use real CourtListener data:")
        print("   1. Get API key from: https://www.courtlistener.com/api/")
        print("   2. Set environment variable: export COURTLISTENER_API_KEY='your_key'")
        print("   3. Or add to .env file: COURTLISTENER_API_KEY=your_key")
    else:
        print("\n✅ Using real CourtListener API data!")

if __name__ == "__main__":
    test_courtlistener_simple()
