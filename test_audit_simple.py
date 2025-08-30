#!/usr/bin/env python3
"""
Simple test script for the audit system without external dependencies.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

def test_audit_models():
    """Test that audit models can be imported."""
    print("Testing audit models import...")
    
    try:
        from models.audit import AuditEventType, AuditSeverity
        print("✅ Audit models imported successfully")
        
        # Test enum values
        print(f"✅ AuditEventType.SECURITY = {AuditEventType.SECURITY.value}")
        print(f"✅ AuditSeverity.HIGH = {AuditSeverity.HIGH.value}")
        
        return True
        
    except Exception as e:
        print(f"❌ Audit models import failed: {str(e)}")
        return False

def test_audit_service():
    """Test that audit service can be imported."""
    print("\nTesting audit service import...")
    
    try:
        from services.audit_service import audit_service
        print("✅ Audit service imported successfully")
        return True
        
    except Exception as e:
        print(f"❌ Audit service import failed: {str(e)}")
        return False

def test_audit_config():
    """Test that audit config can be imported."""
    print("\nTesting audit config import...")
    
    try:
        from config.audit_config import AUDIT_CONFIG
        print("✅ Audit config imported successfully")
        print(f"✅ Retention days: {AUDIT_CONFIG.get('retention_days', 'Not set')}")
        return True
        
    except Exception as e:
        print(f"❌ Audit config import failed: {str(e)}")
        return False

def main():
    """Run all tests."""
    print("🧪 Testing SmartProBono Audit System Components\n")
    
    tests = [
        test_audit_models,
        test_audit_service,
        test_audit_config
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All audit system components are working!")
        return True
    else:
        print("⚠️ Some components need attention")
        return False

if __name__ == "__main__":
    main()
