#!/usr/bin/env python3
"""
Test script for enhanced SmartProBono features
"""
import requests
import json
import os

def test_health_endpoints():
    """Test all health endpoints"""
    print("🔍 Testing Enhanced SmartProBono System...")
    print("=" * 50)
    
    # Test main health endpoint
    try:
        response = requests.get('http://localhost:3001/api/health')
        if response.status_code == 200:
            data = response.json()
            print("✅ Main Health Check:")
            print(f"   Status: {data['status']}")
            print(f"   Version: {data['version']}")
            print(f"   Services: {', '.join(data['services'].keys())}")
            print(f"   Features: {', '.join(data['features'])}")
        else:
            print(f"❌ Main health check failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Main health check error: {e}")
    
    print()
    
    # Test scanner health
    try:
        response = requests.get('http://localhost:3001/api/scanner/health')
        if response.status_code == 200:
            data = response.json()
            print("✅ Scanner Health Check:")
            print(f"   Status: {data['status']}")
            print(f"   Service: {data['service']}")
        else:
            print(f"❌ Scanner health check failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Scanner health check error: {e}")
    
    print()
    
    # Test generator health
    try:
        response = requests.get('http://localhost:3001/api/generator/health')
        if response.status_code == 200:
            data = response.json()
            print("✅ Generator Health Check:")
            print(f"   Status: {data['status']}")
            print(f"   Service: {data['service']}")
        else:
            print(f"❌ Generator health check failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Generator health check error: {e}")

def test_safety_features():
    """Test safety and compliance features"""
    print("\n🛡️ Testing Safety Features...")
    print("=" * 50)
    
    # Test safety analysis with sample text
    sample_texts = [
        "This is a simple lease agreement between John Doe and Jane Smith.",
        "I advise you to file a lawsuit immediately against your landlord.",
        "You should consult with an attorney for this complex legal matter.",
        "This document contains standard rental terms and conditions."
    ]
    
    for i, text in enumerate(sample_texts, 1):
        print(f"\n📝 Test Case {i}: '{text[:50]}...'")
        
        # Test safety analysis
        try:
            # This would normally be done through the API, but we'll test the function directly
            from backend.simple_ai_service import SimpleAIService
            
            needs_escalation = SimpleAIService.needs_escalation(text)
            sanitized = SimpleAIService.sanitize_response(text)
            
            print(f"   Escalation needed: {'Yes' if needs_escalation else 'No'}")
            print(f"   Sanitized: '{sanitized[:50]}...'")
            
            if needs_escalation:
                with_disclaimer = SimpleAIService.add_disclaimer(text)
                print(f"   With disclaimer: '{with_disclaimer[-50:]}...'")
                
        except Exception as e:
            print(f"   ❌ Safety test error: {e}")

def test_document_templates():
    """Test document generation templates"""
    print("\n📄 Testing Document Templates...")
    print("=" * 50)
    
    try:
        response = requests.get('http://localhost:3001/api/generator/templates')
        if response.status_code == 200:
            data = response.json()
            print("✅ Available Templates:")
            for template in data['templates']:
                print(f"   • {template['name']}: {template['description']}")
                print(f"     Fields: {', '.join(template['fields'])}")
        else:
            print(f"❌ Templates request failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Templates test error: {e}")

def main():
    """Run all tests"""
    print("🚀 SmartProBono Enhanced System Test Suite")
    print("=" * 60)
    
    test_health_endpoints()
    test_safety_features()
    test_document_templates()
    
    print("\n" + "=" * 60)
    print("✅ Enhanced system testing complete!")
    print("\n🎯 Key Features Integrated:")
    print("   • Enhanced configuration system")
    print("   • Safety and compliance checks")
    print("   • UPL (Unauthorized Practice of Law) prevention")
    print("   • Advanced document analysis")
    print("   • Professional legal disclaimers")
    print("   • Escalation detection")
    print("   • Response sanitization")

if __name__ == "__main__":
    main()
