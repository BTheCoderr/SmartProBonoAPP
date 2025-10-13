#!/usr/bin/env python3
"""
Simple test script for Saul Legal AI integration
Tests the service structure without downloading the full model
"""

import sys
import os
import json
from datetime import datetime

# Add backend services to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend', 'services'))

def test_service_imports():
    """Test that the services can be imported correctly"""
    print("🧪 Testing Service Imports...")
    print("=" * 50)
    
    try:
        # Test Saul service import
        from saul_legal_ai_service import saul_legal_ai
        print("✅ Saul Legal AI Service imported successfully")
        
        # Test model info (should work without loading model)
        info = saul_legal_ai.get_model_info()
        print(f"   Model: {info['model_name']}")
        print(f"   Company: {info['company']}")
        print(f"   Website: {info['website']}")
        
        # Test health check (should work without loading model)
        health = saul_legal_ai.health_check()
        print(f"   Status: {health['status']}")
        print(f"   Device: {health['device']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Import Error: {str(e)}")
        return False

def test_fallback_response():
    """Test fallback response generation"""
    print("\n🧪 Testing Fallback Response...")
    print("=" * 50)
    
    try:
        from saul_legal_ai_service import saul_legal_ai
        
        # Test fallback response (should work without model)
        response = saul_legal_ai._get_fallback_response(
            message="What is contract law?",
            task_type="legal"
        )
        
        print("✅ Fallback response generated successfully")
        print(f"   Model: {response['model']}")
        print(f"   Success: {response['success']}")
        print(f"   Response length: {len(response['text'])} characters")
        print(f"   Preview: {response['text'][:100]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Fallback Error: {str(e)}")
        return False

def test_enhanced_service_import():
    """Test enhanced service import (without database dependencies)"""
    print("\n🧪 Testing Enhanced Service Import...")
    print("=" * 50)
    
    try:
        # Mock the database import issue
        import sys
        from unittest.mock import MagicMock
        
        # Mock the database module
        sys.modules['database'] = MagicMock()
        sys.modules['database'].db = MagicMock()
        
        from saul_enhanced_ai_service import saul_enhanced_ai
        print("✅ Saul Enhanced AI Service imported successfully")
        
        # Test available models
        models = saul_enhanced_ai.get_available_models()
        print(f"   Available models: {len(models)}")
        for model_name in models.keys():
            print(f"      - {model_name}")
        
        # Test health check
        health = saul_enhanced_ai.health_check()
        print(f"   Service Status: {health['saul_enhanced_service']}")
        print(f"   Recommended Model: {health['recommended_model']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Enhanced Service Error: {str(e)}")
        return False

def test_api_structure():
    """Test that the API routes are properly structured"""
    print("\n🧪 Testing API Structure...")
    print("=" * 50)
    
    try:
        # Test that the unified API file can be read
        api_file = os.path.join(os.path.dirname(__file__), 'backend', 'routes', 'unified_api.py')
        
        with open(api_file, 'r') as f:
            content = f.read()
        
        # Check for Saul-specific endpoints
        endpoints_to_check = [
            '/ai/saul/chat',
            '/ai/saul/info',
            '/ai/models/available'
        ]
        
        found_endpoints = []
        for endpoint in endpoints_to_check:
            if endpoint in content:
                found_endpoints.append(endpoint)
                print(f"✅ Found endpoint: {endpoint}")
            else:
                print(f"❌ Missing endpoint: {endpoint}")
        
        print(f"\n   Found {len(found_endpoints)}/{len(endpoints_to_check)} Saul endpoints")
        
        return len(found_endpoints) == len(endpoints_to_check)
        
    except Exception as e:
        print(f"❌ API Structure Error: {str(e)}")
        return False

def test_requirements():
    """Test that requirements.txt has the necessary dependencies"""
    print("\n🧪 Testing Requirements...")
    print("=" * 50)
    
    try:
        requirements_file = os.path.join(os.path.dirname(__file__), 'requirements.txt')
        
        with open(requirements_file, 'r') as f:
            content = f.read()
        
        required_packages = [
            'transformers',
            'torch',
            'accelerate',
            'safetensors'
        ]
        
        found_packages = []
        for package in required_packages:
            if package in content:
                found_packages.append(package)
                print(f"✅ Found package: {package}")
            else:
                print(f"❌ Missing package: {package}")
        
        print(f"\n   Found {len(found_packages)}/{len(required_packages)} required packages")
        
        return len(found_packages) == len(required_packages)
        
    except Exception as e:
        print(f"❌ Requirements Error: {str(e)}")
        return False

def main():
    """Run all tests"""
    print("🚀 SmartProBono Saul Legal AI Integration Test (Simple)")
    print("=" * 70)
    print(f"Timestamp: {datetime.now().isoformat()}")
    print()
    
    # Run tests
    tests = [
        ("Service Imports", test_service_imports),
        ("Fallback Response", test_fallback_response),
        ("Enhanced Service Import", test_enhanced_service_import),
        ("API Structure", test_api_structure),
        ("Requirements", test_requirements)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {str(e)}")
            results.append((test_name, False))
    
    # Summary
    print("\n📊 Test Summary:")
    print("=" * 30)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("\n🎉 All tests passed! Saul integration is properly set up.")
        print("\n📝 Next steps:")
        print("   1. Free up disk space for model download (~15GB needed)")
        print("   2. Start your server: python backend/combined_server.py")
        print("   3. The model will download automatically on first use")
        print("   4. Test the legal chat functionality")
    else:
        print("\n⚠️  Some tests failed. Check the error messages above.")
        print("\n🔧 Common issues:")
        print("   1. Disk space - Need ~15GB free space for model download")
        print("   2. Import errors - Check Python path and dependencies")
        print("   3. File permissions - Ensure read access to all files")

if __name__ == "__main__":
    main()
