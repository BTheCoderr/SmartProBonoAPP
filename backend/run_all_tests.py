#!/usr/bin/env python3
"""
Test runner script for the SmartProBono application.
Run this script to execute all tests and generate a comprehensive report.
"""

import unittest
import time
import sys
import os
import json
from datetime import datetime

# Add the backend directory to the path so we can import modules
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Import test modules
from tests.test_auth_system import AuthSystemTest
from tests.test_document_management import DocumentManagementTest
from tests.test_form_submission import FormSubmissionTest
from tests.test_navigation_flows import NavigationFlowsTest
from tests.test_deployment_setup import DeploymentSetupTest

def run_test_suite():
    """Run all test cases and generate a report."""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test cases
    suite.addTests(loader.loadTestsFromTestCase(AuthSystemTest))
    suite.addTests(loader.loadTestsFromTestCase(DocumentManagementTest))
    suite.addTests(loader.loadTestsFromTestCase(FormSubmissionTest))
    suite.addTests(loader.loadTestsFromTestCase(NavigationFlowsTest))
    suite.addTests(loader.loadTestsFromTestCase(DeploymentSetupTest))
    
    # Run tests
    start_time = time.time()
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    end_time = time.time()
    
    # Generate report
    test_report = {
        'timestamp': datetime.now().isoformat(),
        'total_tests': result.testsRun,
        'failures': len(result.failures),
        'errors': len(result.errors),
        'skipped': len(result.skipped),
        'execution_time': end_time - start_time,
        'success_percentage': (result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100 if result.testsRun > 0 else 0,
    }
    
    # Print report
    print("\n" + "="*80)
    print(f"SmartProBono Test Report - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*80)
    print(f"Total Tests: {test_report['total_tests']}")
    print(f"Passed: {test_report['total_tests'] - test_report['failures'] - test_report['errors']}")
    print(f"Failed: {test_report['failures']}")
    print(f"Errors: {test_report['errors']}")
    print(f"Skipped: {test_report['skipped']}")
    print(f"Success Rate: {test_report['success_percentage']:.2f}%")
    print(f"Execution Time: {test_report['execution_time']:.2f} seconds")
    print("="*80)
    
    # Save report to file
    report_dir = os.path.join(os.path.dirname(__file__), 'logs')
    os.makedirs(report_dir, exist_ok=True)
    
    report_file = os.path.join(report_dir, f"test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
    with open(report_file, 'w') as f:
        json.dump(test_report, f, indent=4)
    
    print(f"Report saved to {report_file}")
    
    # Return True if all tests passed
    return len(result.failures) == 0 and len(result.errors) == 0

if __name__ == '__main__':
    success = run_test_suite()
    sys.exit(0 if success else 1) 