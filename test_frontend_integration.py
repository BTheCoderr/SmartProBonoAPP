#!/usr/bin/env python3
"""
SmartProBono Frontend Integration Test
=====================================
Tests the complete frontend-backend integration with optimized models.
"""

import requests
import json
import time
from datetime import datetime

class FrontendIntegrationTester:
    def __init__(self):
        self.backend_url = "http://localhost:8081"
        self.frontend_url = "http://localhost:3002"
        
    def test_backend_health(self):
        """Test backend health endpoint"""
        print("🔧 Testing Backend Health...")
        try:
            response = requests.get(f"{self.backend_url}/api/health", timeout=5)
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ Backend: {data.get('message', 'OK')}")
                print(f"   🤖 AI System: {data.get('ai_system', 'Unknown')}")
                print(f"   📊 Agents: {len(data.get('agents', []))} available")
                return True
            else:
                print(f"   ❌ Backend: HTTP {response.status_code}")
                return False
        except Exception as e:
            print(f"   ❌ Backend: {str(e)}")
            return False
    
    def test_frontend_accessibility(self):
        """Test frontend accessibility"""
        print("🌐 Testing Frontend Accessibility...")
        try:
            response = requests.get(self.frontend_url, timeout=5)
            if response.status_code == 200:
                print("   ✅ Frontend: Accessible")
                return True
            else:
                print(f"   ❌ Frontend: HTTP {response.status_code}")
                return False
        except Exception as e:
            print(f"   ❌ Frontend: {str(e)}")
            return False
    
    def test_chat_endpoint(self, message, expected_agent=None):
        """Test chat endpoint with different message types"""
        print(f"💬 Testing Chat: '{message[:30]}...'")
        try:
            payload = {
                "message": message,
                "task_type": "chat"
            }
            
            start_time = time.time()
            response = requests.post(
                f"{self.backend_url}/api/legal/chat",
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=15
            )
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                agent_name = data.get('agent_name', 'Unknown')
                agent_type = data.get('agent_type', 'Unknown')
                response_text = data.get('response', '')
                
                print(f"   ✅ Success: {agent_name} ({response_time:.2f}s)")
                print(f"   📝 Response: {response_text[:100]}...")
                
                if expected_agent and expected_agent.lower() in agent_name.lower():
                    print(f"   🎯 Correctly routed to {expected_agent}")
                elif expected_agent:
                    print(f"   ⚠️  Expected {expected_agent}, got {agent_name}")
                
                return True
            else:
                print(f"   ❌ Failed: HTTP {response.status_code}")
                return False
                
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
            return False
    
    def test_model_selection(self):
        """Test different model selections"""
        print("🤖 Testing Model Selection...")
        
        models_to_test = [
            ("tiny", "TinyLlama"),
            ("qwen", "Qwen"),
            ("gemma", "Gemma"),
            ("llama", "Llama")
        ]
        
        for model_type, model_name in models_to_test:
            print(f"   Testing {model_name} model...")
            try:
                payload = {
                    "message": f"Quick test with {model_name}",
                    "task_type": model_type
                }
                
                response = requests.post(
                    f"{self.backend_url}/api/legal/chat",
                    json=payload,
                    headers={"Content-Type": "application/json"},
                    timeout=10
                )
                
                if response.status_code == 200:
                    data = response.json()
                    print(f"   ✅ {model_name}: Working")
                else:
                    print(f"   ❌ {model_name}: HTTP {response.status_code}")
                    
            except Exception as e:
                print(f"   ❌ {model_name}: {str(e)}")
    
    def test_legal_scenarios(self):
        """Test various legal scenarios"""
        print("⚖️  Testing Legal Scenarios...")
        
        scenarios = [
            ("Hello, I need legal help", "Greeting", "greeting"),
            ("I need help with immigration visa", "Immigration", "immigration"),
            ("I have a business law question", "Business", "business"),
            ("Help with family law matter", "Family", "family"),
            ("I need a legal document", "Document", "document"),
            ("GDPR compliance question", "Compliance", "compliance")
        ]
        
        for message, expected_agent, agent_type in scenarios:
            self.test_chat_endpoint(message, expected_agent)
            time.sleep(1)  # Brief pause between tests
    
    def run_comprehensive_test(self):
        """Run comprehensive integration test"""
        print("🚀 SmartProBono Frontend Integration Test")
        print("=" * 50)
        print(f"🕐 Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        # Test basic connectivity
        backend_ok = self.test_backend_health()
        frontend_ok = self.test_frontend_accessibility()
        
        if not backend_ok or not frontend_ok:
            print("\n❌ Basic connectivity failed. Please check services.")
            return False
        
        print()
        
        # Test chat functionality
        self.test_legal_scenarios()
        
        print()
        
        # Test model selection
        self.test_model_selection()
        
        print()
        print("✅ Frontend Integration Test Complete!")
        print("=" * 50)
        
        return True

def main():
    tester = FrontendIntegrationTester()
    tester.run_comprehensive_test()

if __name__ == "__main__":
    main()
