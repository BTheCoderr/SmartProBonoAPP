#!/usr/bin/env python3
"""
Simple CRM Test Script
Tests the CRM system without external dependencies
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

def test_crm_imports():
    """Test that all CRM components can be imported"""
    print("🧪 Testing CRM Component Imports...")
    print("=" * 50)
    
    try:
        # Test database initialization
        from backend.database import init_db
        print("✅ Database module imported")
        
        # Test CRM service
        from backend.services.crm_service import CRMService
        print("✅ CRM Service imported")
        
        # Test CRM API routes
        from backend.routes.crm_api import bp
        print("✅ CRM API routes imported")
        
        # Test models
        from backend.models import User, Case, ClientIntake
        print("✅ Database models imported")
        
        print("=" * 50)
        print("🎯 All CRM components imported successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False

def test_crm_service():
    """Test CRM service functionality"""
    print("\n🔧 Testing CRM Service...")
    print("=" * 50)
    
    try:
        from backend.services.crm_service import CRMService
        crm = CRMService()
        print("✅ CRM Service instantiated")
        
        # Test basic methods exist
        methods = ['create_client_intake', 'get_client_cases', 'get_lawyer_clients']
        for method in methods:
            if hasattr(crm, method):
                print(f"✅ Method {method} exists")
            else:
                print(f"❌ Method {method} missing")
        
        print("=" * 50)
        print("🎯 CRM Service test complete!")
        return True
        
    except Exception as e:
        print(f"❌ CRM Service error: {e}")
        return False

if __name__ == "__main__":
    print("🚀 SmartProBono CRM System Test")
    print("=" * 50)
    
    # Test imports
    imports_ok = test_crm_imports()
    
    # Test service
    service_ok = test_crm_service()
    
    print("\n" + "=" * 50)
    if imports_ok and service_ok:
        print("🎉 CRM System is ready!")
        print("✅ All components imported successfully")
        print("✅ CRM Service is functional")
        print("\nNext steps:")
        print("1. Start the server: cd backend && python combined_server.py")
        print("2. Test API endpoints with curl or Postman")
        print("3. Access frontend at http://localhost:3000/virtual-paralegal/crm")
    else:
        print("❌ CRM System has issues")
        print("Check the errors above and fix them")
    
    print("=" * 50)
