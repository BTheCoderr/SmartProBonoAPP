#!/usr/bin/env python3
"""
Comprehensive Chat System Test Script
Tests all chat endpoints and functionality
"""

import requests
import json
import time
import sys
from datetime import datetime

class ChatSystemTester:
    def __init__(self):
        self.base_url = "http://localhost:3001"
        self.frontend_url = "http://localhost:3002"
        self.test_results = []
        
    def log_test(self, test_name, success, details=""):
        """Log test results"""
        status = "✅ PASS" if success else "❌ FAIL"
        timestamp = datetime.now().strftime("%H:%M:%S")
        result = f"[{timestamp}] {status} - {test_name}"
        if details:
            result += f" - {details}"
        
        print(result)
        self.test_results.append({
            "test": test_name,
            "success": success,
            "details": details,
            "timestamp": timestamp
        })
    
    def test_backend_health(self):
        """Test backend health endpoint"""
        try:
            response = requests.get(f"{self.base_url}/api/health", timeout=10)
            if response.status_code == 200:
                data = response.json()
                self.log_test("Backend Health", True, f"Status: {data.get('status')}")
                return True
            else:
                self.log_test("Backend Health", False, f"HTTP {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Backend Health", False, str(e))
            return False
    
    def test_chat_api(self):
        """Test main chat API endpoint"""
        try:
            payload = {
                "message": "Hello, can you help me with a legal question?",
                "task_type": "chat",
                "model": "auto"
            }
            
            response = requests.post(
                f"{self.base_url}/api/v1/ai/chat",
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    self.log_test("Chat API", True, f"Model: {data.get('model')}")
                    return True
                else:
                    self.log_test("Chat API", False, f"API returned success=False")
                    return False
            else:
                self.log_test("Chat API", False, f"HTTP {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Chat API", False, str(e))
            return False
    
    def test_legal_ai_chat(self):
        """Test legal AI chat endpoint"""
        try:
            payload = {
                "message": "What are my rights as a tenant?",
                "task_type": "chat",
                "model": "default"
            }
            
            response = requests.post(
                f"{self.base_url}/api/legal/chat",
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                self.log_test("Legal AI Chat", True, "Response received")
                return True
            else:
                self.log_test("Legal AI Chat", False, f"HTTP {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Legal AI Chat", False, str(e))
            return False
    
    def test_voice_chat(self):
        """Test voice chat endpoint"""
        try:
            payload = {
                "message": "Test voice message",
                "task_type": "chat",
                "voice_enabled": True
            }
            
            response = requests.post(
                f"{self.base_url}/api/voice/voice-chat",
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            
            if response.status_code == 200:
                self.log_test("Voice Chat", True, "Response received")
                return True
            else:
                self.log_test("Voice Chat", False, f"HTTP {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Voice Chat", False, str(e))
            return False
    
    def test_frontend_accessibility(self):
        """Test if frontend is accessible"""
        try:
            response = requests.get(self.frontend_url, timeout=10)
            if response.status_code == 200:
                self.log_test("Frontend Access", True, "React app loaded")
                return True
            else:
                self.log_test("Frontend Access", False, f"HTTP {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Frontend Access", False, str(e))
            return False
    
    def test_response_times(self):
        """Test response times for chat endpoints"""
        try:
            start_time = time.time()
            payload = {
                "message": "Quick test message",
                "task_type": "chat",
                "model": "auto"
            }
            
            response = requests.post(
                f"{self.base_url}/api/v1/ai/chat",
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            
            end_time = time.time()
            response_time = end_time - start_time
            
            if response.status_code == 200 and response_time < 10:
                self.log_test("Response Time", True, f"{response_time:.2f}s")
                return True
            else:
                self.log_test("Response Time", False, f"{response_time:.2f}s")
                return False
                
        except Exception as e:
            self.log_test("Response Time", False, str(e))
            return False
    
    def run_all_tests(self):
        """Run all tests and provide summary"""
        print("🧪 Starting Chat System Tests...")
        print("=" * 50)
        
        tests = [
            self.test_backend_health,
            self.test_chat_api,
            self.test_legal_ai_chat,
            self.test_voice_chat,
            self.test_frontend_accessibility,
            self.test_response_times
        ]
        
        passed = 0
        total = len(tests)
        
        for test in tests:
            if test():
                passed += 1
            time.sleep(1)  # Brief pause between tests
        
        print("\n" + "=" * 50)
        print("📊 Test Summary")
        print("=" * 50)
        
        success_rate = (passed / total) * 100
        print(f"✅ Passed: {passed}/{total} ({success_rate:.1f}%)")
        
        if passed == total:
            print("🎉 All tests passed! Chat system is working correctly.")
            return True
        else:
            print("⚠️ Some tests failed. Check the details above.")
            return False
    
    def generate_report(self):
        """Generate a detailed test report"""
        report = {
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "total_tests": len(self.test_results),
                "passed": sum(1 for r in self.test_results if r["success"]),
                "failed": sum(1 for r in self.test_results if not r["success"])
            },
            "results": self.test_results
        }
        
        with open("chat_test_report.json", "w") as f:
            json.dump(report, f, indent=2)
        
        print(f"\n📄 Detailed report saved to: chat_test_report.json")

def main():
    """Main function"""
    tester = ChatSystemTester()
    
    print("🔧 SmartProBono Chat System Tester")
    print("==================================")
    print(f"Backend URL: {tester.base_url}")
    print(f"Frontend URL: {tester.frontend_url}")
    print()
    
    success = tester.run_all_tests()
    tester.generate_report()
    
    if success:
        print("\n✅ Chat system is ready for use!")
        sys.exit(0)
    else:
        print("\n❌ Chat system needs attention.")
        sys.exit(1)

if __name__ == "__main__":
    main()
