#!/usr/bin/env python3
"""
Test CourtListener v4.3 API Integration
Tests both authenticated and fallback modes
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from services.courtlistener_service import courtlistener_service

def test_courtlistener_v4():
    """Test CourtListener v4.3 API integration"""
    print("🔍 Testing CourtListener v4.3 API Integration")
    print("=" * 50)
    
    # Test 1: Search cases
    print("\n📊 Test 1: Search Cases")
    print("-" * 30)
    search_result = courtlistener_service.search_cases(
        query="immigration",
        case_type="civil",
        limit=3
    )
    
    if search_result.get('success'):
        print(f"✅ Search successful: {search_result['total_results']} cases found")
        print(f"   Fallback mode: {search_result.get('fallback_mode', False)}")
        print(f"   Message: {search_result.get('message', 'N/A')}")
        
        for i, case in enumerate(search_result['cases'][:2], 1):
            print(f"   Case {i}: {case['case_name']}")
            print(f"   Court: {case['court']}")
            print(f"   Date: {case['date_filed']}")
    else:
        print(f"❌ Search failed: {search_result.get('error', 'Unknown error')}")
    
    # Test 2: Recent cases
    print("\n📅 Test 2: Recent Cases")
    print("-" * 30)
    recent_result = courtlistener_service.get_recent_cases(
        days=30,
        limit=3
    )
    
    if recent_result.get('success'):
        print(f"✅ Recent cases successful: {recent_result['total_results']} cases found")
        print(f"   Fallback mode: {recent_result.get('fallback_mode', False)}")
        print(f"   Date range: {recent_result.get('date_range', {}).get('start', 'N/A')} to {recent_result.get('date_range', {}).get('end', 'N/A')}")
        
        for i, case in enumerate(recent_result['cases'][:2], 1):
            print(f"   Case {i}: {case['case_name']}")
            print(f"   Court: {case['court']}")
            print(f"   Date: {case['date_filed']}")
    else:
        print(f"❌ Recent cases failed: {recent_result.get('error', 'Unknown error')}")
    
    # Test 3: API Key status
    print("\n🔑 Test 3: API Key Status")
    print("-" * 30)
    if courtlistener_service.api_key:
        print(f"✅ API Key found: {courtlistener_service.api_key[:8]}...")
        print("   Using real CourtListener API")
    else:
        print("⚠️  No API key found")
        print("   Using fallback mode with mock data")
        print("   To get real data, set COURTLISTENER_API_KEY environment variable")
    
    print("\n🎉 CourtListener v4.3 test completed!")
    print("=" * 50)

if __name__ == "__main__":
    test_courtlistener_v4()
