#!/usr/bin/env python3
"""
Comprehensive Test Suite for SmartProBono
Tests all components: Backend, LangGraph, Frontend, Database
"""

import requests
import json
import time
import sys
from datetime import datetime

class SmartProBonoTester:
    def __init__(self):
        self.backend_url = "http://localhost:8081"
        self.langgraph_url = "http://localhost:8010"
        self.frontend_url = "http://localhost:3002"
        self.test_results = []
        
    def log_test(self, test_name, status, details=""):
        """Log test results"""
        result = {
            "test": test_name,
            "status": status,
            "details": details,
            "timestamp": datetime.now().isoformat()
        }
        self.test_results.append(result)
        status_emoji = "✅" if status == "PASS" else "❌" if status == "FAIL" else "⚠️"
        print(f"{status_emoji} {test_name}: {status}")
        if details:
            print(f"   Details: {details}")
    
    def test_backend_health(self):
        """Test backend API health"""
        try:
            response = requests.get(f"{self.backend_url}/api/health", timeout=5)
            if response.status_code == 200:
                self.log_test("Backend Health", "PASS", f"Status: {response.status_code}")
                return True
            else:
                self.log_test("Backend Health", "FAIL", f"Status: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Backend Health", "FAIL", str(e))
            return False
    
    def test_langgraph_health(self):
        """Test LangGraph service health"""
        try:
            response = requests.get(f"{self.langgraph_url}/health", timeout=5)
            if response.status_code == 200:
                self.log_test("LangGraph Health", "PASS", f"Status: {response.status_code}")
                return True
            else:
                self.log_test("LangGraph Health", "FAIL", f"Status: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("LangGraph Health", "FAIL", str(e))
            return False
    
    def test_frontend_health(self):
        """Test frontend accessibility"""
        try:
            response = requests.get(self.frontend_url, timeout=5)
            if response.status_code == 200:
                self.log_test("Frontend Health", "PASS", f"Status: {response.status_code}")
                return True
            else:
                self.log_test("Frontend Health", "FAIL", f"Status: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Frontend Health", "FAIL", str(e))
            return False
    
    def test_langgraph_info(self):
        """Test LangGraph system info"""
        try:
            response = requests.get(f"{self.langgraph_url}/graph/info", timeout=10)
            if response.status_code == 200:
                data = response.json()
                self.log_test("LangGraph Info", "PASS", f"Graphs: {len(data.get('graphs', {}))}")
                return data
            else:
                self.log_test("LangGraph Info", "FAIL", f"Status: {response.status_code}")
                return None
        except Exception as e:
            self.log_test("LangGraph Info", "FAIL", str(e))
            return None
    
    def test_simple_intake(self):
        """Test simple LangGraph intake"""
        try:
            payload = {
                "user_id": None,
                "full_text": "I need help with a landlord dispute. My landlord won't fix the heating.",
                "meta": {"source": "test", "priority": "medium"}
            }
            response = requests.post(
                f"{self.langgraph_url}/intake/run",
                json=payload,
                timeout=30
            )
            if response.status_code == 200:
                data = response.json()
                self.log_test("Simple Intake", "PASS", f"Intake ID: {data.get('result', {}).get('intake_id', 'N/A')}")
                return data
            else:
                self.log_test("Simple Intake", "FAIL", f"Status: {response.status_code}")
                return None
        except Exception as e:
            self.log_test("Simple Intake", "FAIL", str(e))
            return None
    
    def test_advanced_intake(self):
        """Test advanced multi-agent intake"""
        try:
            payload = {
                "user_id": None,
                "full_text": "I was arrested for shoplifting at a department store. I took a $50 item without paying. I'm 19 years old and this is my first offense. I'm scared about what will happen to me.",
                "meta": {"source": "test", "priority": "high"}
            }
            response = requests.post(
                f"{self.langgraph_url}/intake/advanced",
                json=payload,
                timeout=60
            )
            if response.status_code == 200:
                data = response.json()
                result = data.get('result', {})
                self.log_test("Advanced Intake", "PASS", 
                    f"Case Type: {result.get('case_type', 'N/A')}, "
                    f"Status: {result.get('status', 'N/A')}, "
                    f"Intake ID: {result.get('intake_id', 'N/A')}")
                return data
            else:
                self.log_test("Advanced Intake", "FAIL", f"Status: {response.status_code}")
                return None
        except Exception as e:
            self.log_test("Advanced Intake", "FAIL", str(e))
            return None
    
    def test_intake_listing(self):
        """Test intake listing functionality"""
        try:
            response = requests.get(f"{self.langgraph_url}/intakes?limit=5", timeout=10)
            if response.status_code == 200:
                data = response.json()
                intakes = data.get('intakes', [])
                self.log_test("Intake Listing", "PASS", f"Found {len(intakes)} intakes")
                return intakes
            else:
                self.log_test("Intake Listing", "FAIL", f"Status: {response.status_code}")
                return None
        except Exception as e:
            self.log_test("Intake Listing", "FAIL", str(e))
            return None
    
    def test_database_connection(self):
        """Test database connectivity through API"""
        try:
            # Test by creating and retrieving an intake
            payload = {
                "user_id": None,
                "full_text": "Database connectivity test case.",
                "meta": {"test": "database_connection"}
            }
            response = requests.post(
                f"{self.langgraph_url}/intake/run",
                json=payload,
                timeout=30
            )
            if response.status_code == 200:
                data = response.json()
                intake_id = data.get('result', {}).get('intake_id')
                if intake_id:
                    # Try to retrieve the intake
                    status_response = requests.get(
                        f"{self.langgraph_url}/intake/status/{intake_id}",
                        timeout=10
                    )
                    if status_response.status_code == 200:
                        self.log_test("Database Connection", "PASS", f"Created and retrieved intake {intake_id}")
                        return True
            self.log_test("Database Connection", "FAIL", "Could not create or retrieve intake")
            return False
        except Exception as e:
            self.log_test("Database Connection", "FAIL", str(e))
            return False
    
    def test_performance_metrics(self):
        """Test system performance"""
        try:
            start_time = time.time()
            
            # Test multiple concurrent requests
            payloads = [
                {
                    "user_id": None,
                    "full_text": f"Performance test case {i}. I need legal help.",
                    "meta": {"test": "performance", "case": i}
                }
                for i in range(3)
            ]
            
            responses = []
            for payload in payloads:
                response = requests.post(
                    f"{self.langgraph_url}/intake/run",
                    json=payload,
                    timeout=30
                )
                responses.append(response)
            
            end_time = time.time()
            duration = end_time - start_time
            
            successful = sum(1 for r in responses if r.status_code == 200)
            self.log_test("Performance Test", "PASS" if successful == 3 else "FAIL", 
                f"3 requests in {duration:.2f}s, {successful}/3 successful")
            return successful == 3
            
        except Exception as e:
            self.log_test("Performance Test", "FAIL", str(e))
            return False
    
    def run_all_tests(self):
        """Run all tests and generate report"""
        print("🧪 SmartProBono Comprehensive Test Suite")
        print("=" * 50)
        print(f"Testing at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        # Health checks
        print("📊 Health Checks:")
        backend_ok = self.test_backend_health()
        langgraph_ok = self.test_langgraph_health()
        frontend_ok = self.test_frontend_health()
        print()
        
        if not langgraph_ok:
            print("❌ LangGraph service not available. Skipping advanced tests.")
            return self.generate_report()
        
        # LangGraph tests
        print("🧠 LangGraph Tests:")
        self.test_langgraph_info()
        self.test_database_connection()
        print()
        
        # Intake tests
        print("📝 Intake Processing Tests:")
        self.test_simple_intake()
        time.sleep(2)  # Brief pause between tests
        self.test_advanced_intake()
        time.sleep(2)
        self.test_intake_listing()
        print()
        
        # Performance tests
        print("⚡ Performance Tests:")
        self.test_performance_metrics()
        print()
        
        return self.generate_report()
    
    def generate_report(self):
        """Generate comprehensive test report"""
        print("📋 Test Report Summary")
        print("=" * 30)
        
        total_tests = len(self.test_results)
        passed = sum(1 for r in self.test_results if r['status'] == 'PASS')
        failed = sum(1 for r in self.test_results if r['status'] == 'FAIL')
        
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed} ✅")
        print(f"Failed: {failed} ❌")
        print(f"Success Rate: {(passed/total_tests*100):.1f}%")
        print()
        
        if failed > 0:
            print("❌ Failed Tests:")
            for result in self.test_results:
                if result['status'] == 'FAIL':
                    print(f"  • {result['test']}: {result['details']}")
            print()
        
        # Save detailed report
        report_file = f"test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump(self.test_results, f, indent=2)
        print(f"📄 Detailed report saved to: {report_file}")
        
        return passed == total_tests

if __name__ == "__main__":
    tester = SmartProBonoTester()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)
