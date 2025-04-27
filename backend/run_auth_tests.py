"""
Script to run authentication tests for SmartProBono
"""
import unittest
import sys
from test_auth_flow import AuthenticationTestCase

def run_tests():
    """Run all authentication tests"""
    loader = unittest.TestLoader()
    auth_tests = loader.loadTestsFromTestCase(AuthenticationTestCase)
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(auth_tests)
    
    return result.wasSuccessful()

if __name__ == "__main__":
    print("Running SmartProBono Authentication Tests...")
    success = run_tests()
    
    if success:
        print("\n✅ All authentication tests passed!")
        sys.exit(0)
    else:
        print("\n❌ Some authentication tests failed.")
        sys.exit(1) 