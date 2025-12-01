#!/usr/bin/env python3
"""
Comprehensive Application Flow Test
Tests backend API endpoints and verifies full application functionality
"""

import sys
import os
import time
import requests
import json
from datetime import datetime

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Colors for output
GREEN = '\033[0;32m'
RED = '\033[0;31m'
YELLOW = '\033[1;33m'
BLUE = '\033[0;34m'
NC = '\033[0m'  # No Color

BASE_URL = "http://localhost:3001"
TIMEOUT = 5

class ApplicationTester:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.warnings = 0
        self.results = []
    
    def log(self, message, status="INFO"):
        timestamp = datetime.now().strftime("%H:%M:%S")
        if status == "PASS":
            print(f"{GREEN}✅ [{timestamp}] {message}{NC}")
            self.passed += 1
        elif status == "FAIL":
            print(f"{RED}❌ [{timestamp}] {message}{NC}")
            self.failed += 1
        elif status == "WARN":
            print(f"{YELLOW}⚠️  [{timestamp}] {message}{NC}")
            self.warnings += 1
        else:
            print(f"{BLUE}ℹ️  [{timestamp}] {message}{NC}")
        self.results.append({"time": timestamp, "status": status, "message": message})
    
    def test_endpoint(self, method, endpoint, data=None, expected_status=200, description=None):
        """Test a single API endpoint"""
        url = f"{BASE_URL}{endpoint}"
        desc = description or f"{method} {endpoint}"
        
        try:
            if method == "GET":
                response = requests.get(url, timeout=TIMEOUT)
            elif method == "POST":
                response = requests.post(url, json=data, timeout=TIMEOUT, headers={'Content-Type': 'application/json'})
            else:
                self.log(f"{desc}: Unsupported method {method}", "FAIL")
                return False
            
            # Handle list of acceptable status codes
            if isinstance(expected_status, list):
                if response.status_code in expected_status:
                    self.log(f"{desc}: Status {response.status_code} (acceptable)", "PASS")
                    return True
                else:
                    self.log(f"{desc}: Expected one of {expected_status}, got {response.status_code}", "FAIL")
                    return False
            elif response.status_code == expected_status:
                self.log(f"{desc}: Status {response.status_code}", "PASS")
                return True
            else:
                self.log(f"{desc}: Expected {expected_status}, got {response.status_code}", "FAIL")
                return False
                
        except requests.exceptions.ConnectionError:
            self.log(f"{desc}: Connection refused - is backend running?", "FAIL")
            return False
        except requests.exceptions.Timeout:
            self.log(f"{desc}: Request timed out", "FAIL")
            return False
        except Exception as e:
            self.log(f"{desc}: Error - {str(e)}", "FAIL")
            return False
    
    def test_health_endpoints(self):
        """Test all health check endpoints"""
        self.log("=" * 60, "INFO")
        self.log("Testing Health Endpoints", "INFO")
        self.log("=" * 60, "INFO")
        
        endpoints = [
            ("GET", "/api/health", None, 200, "Main Health Check"),
            ("GET", "/api/contact/health", None, 200, "Contact Service Health"),
            ("GET", "/api/scanner/health", None, 200, "Scanner Service Health"),
            ("GET", "/api/generator/health", None, 200, "Generator Service Health"),
            ("GET", "/api/voice/status", None, 200, "Voice Service Status"),
            ("GET", "/api/websocket/status", None, 200, "WebSocket Status"),
        ]
        
        for method, endpoint, data, status, desc in endpoints:
            self.test_endpoint(method, endpoint, data, status, desc)
            time.sleep(0.2)  # Small delay between requests
    
    def test_api_endpoints(self):
        """Test core API endpoints"""
        self.log("=" * 60, "INFO")
        self.log("Testing Core API Endpoints", "INFO")
        self.log("=" * 60, "INFO")
        
        # Test onboarding endpoint
        self.test_endpoint("GET", "/api/onboarding", None, 200, "Onboarding Data")
        
        # Test court filing endpoints
        self.test_endpoint("GET", "/api/court-filing/rules", None, 200, "Court Filing Rules")
        
        # Test analytics endpoints
        self.test_endpoint("GET", "/api/analytics/dashboard", None, 200, "Analytics Dashboard")
        self.test_endpoint("GET", "/api/analytics/metrics", None, 200, "Analytics Metrics")
        
        # Test enhanced API v2
        self.test_endpoint("GET", "/api/v2/", None, 200, "Enhanced API v2")
    
    def test_ai_endpoints(self):
        """Test AI-related endpoints"""
        self.log("=" * 60, "INFO")
        self.log("Testing AI Endpoints", "INFO")
        self.log("=" * 60, "INFO")
        
        # Test legal AI analyze endpoint
        test_query = {
            "query": "What are my rights as a tenant?",
            "jurisdiction": "ri"
        }
        self.test_endpoint("POST", "/api/v1/legal/analyze", test_query, 200, "Legal AI Analysis")
        
        # Test unified AI chat endpoint
        test_message = {
            "message": "Hello, I need legal help",
            "task_type": "chat"
        }
        # This might return 200 or 500 depending on AI service availability
        self.test_endpoint("POST", "/api/v1/ai/chat", test_message, [200, 500], "Unified AI Chat")
    
    def test_contact_endpoints(self):
        """Test contact form endpoints"""
        self.log("=" * 60, "INFO")
        self.log("Testing Contact Endpoints", "INFO")
        self.log("=" * 60, "INFO")
        
        # Test contact form submission (will fail without valid email config, but endpoint should exist)
        test_contact = {
            "firstName": "Test",
            "lastName": "User",
            "email": "test@example.com",
            "message": "Test message"
        }
        # This might return 200 or 500 depending on email service
        self.test_endpoint("POST", "/api/contact/submit", test_contact, [200, 500], "Contact Form Submit")
    
    def test_backend_import(self):
        """Test that backend can be imported"""
        self.log("=" * 60, "INFO")
        self.log("Testing Backend Import", "INFO")
        self.log("=" * 60, "INFO")
        
        try:
            # Change to backend directory
            backend_path = os.path.join(os.path.dirname(__file__), 'backend')
            sys.path.insert(0, backend_path)
            
            from combined_server import app
            self.log("Backend imports successfully", "PASS")
            return True
        except Exception as e:
            self.log(f"Backend import failed: {str(e)}", "FAIL")
            return False
    
    def check_backend_running(self):
        """Check if backend server is running"""
        self.log("=" * 60, "INFO")
        self.log("Checking if Backend is Running", "INFO")
        self.log("=" * 60, "INFO")
        
        try:
            response = requests.get(f"{BASE_URL}/api/health", timeout=2)
            if response.status_code == 200:
                self.log("Backend server is running", "PASS")
                return True
            else:
                self.log(f"Backend returned status {response.status_code}", "WARN")
                return False
        except requests.exceptions.ConnectionError:
            self.log("Backend server is NOT running - start it with: python3 app.py", "FAIL")
            return False
        except Exception as e:
            self.log(f"Error checking backend: {str(e)}", "FAIL")
            return False
    
    def run_all_tests(self):
        """Run all tests"""
        print(f"\n{BLUE}{'='*60}{NC}")
        print(f"{BLUE}SmartProBono Application Flow Test{NC}")
        print(f"{BLUE}{'='*60}{NC}\n")
        
        # Check backend import first
        self.test_backend_import()
        print()
        
        # Check if backend is running
        backend_running = self.check_backend_running()
        print()
        
        if not backend_running:
            print(f"{YELLOW}⚠️  Backend server is not running.{NC}")
            print(f"{YELLOW}   Start it in another terminal with: python3 app.py{NC}")
            print(f"{YELLOW}   Then run this test again.{NC}\n")
            return
        
        # Run endpoint tests
        self.test_health_endpoints()
        print()
        
        self.test_api_endpoints()
        print()
        
        self.test_ai_endpoints()
        print()
        
        self.test_contact_endpoints()
        print()
        
        # Print summary
        self.print_summary()
    
    def print_summary(self):
        """Print test summary"""
        total = self.passed + self.failed + self.warnings
        print(f"\n{BLUE}{'='*60}{NC}")
        print(f"{BLUE}Test Summary{NC}")
        print(f"{BLUE}{'='*60}{NC}")
        print(f"{GREEN}✅ Passed: {self.passed}{NC}")
        print(f"{RED}❌ Failed: {self.failed}{NC}")
        print(f"{YELLOW}⚠️  Warnings: {self.warnings}{NC}")
        print(f"Total Tests: {total}")
        print(f"{BLUE}{'='*60}{NC}\n")
        
        if self.failed == 0:
            print(f"{GREEN}🎉 All critical tests passed!{NC}\n")
        else:
            print(f"{YELLOW}⚠️  Some tests failed. Check the output above for details.{NC}\n")

if __name__ == "__main__":
    tester = ApplicationTester()
    tester.run_all_tests()

