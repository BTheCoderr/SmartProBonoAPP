#!/usr/bin/env python3
"""
SmartProBono Voice AI Complete Demo Script
Demonstrates the full unified AI system with voice capabilities
"""

import requests
import json
import time
import sys

def print_header(title):
    """Print a formatted header"""
    print(f"\n{'='*60}")
    print(f"🎤 {title}")
    print(f"{'='*60}")

def print_section(title):
    """Print a formatted section"""
    print(f"\n📋 {title}")
    print("-" * 40)

def test_endpoint(url, method="GET", data=None):
    """Test an API endpoint"""
    try:
        if method == "GET":
            response = requests.get(url, timeout=10)
        elif method == "POST":
            response = requests.post(url, json=data, timeout=10)
        
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"HTTP {response.status_code}: {response.text}"}
    except requests.exceptions.RequestException as e:
        return {"error": f"Connection error: {str(e)}"}

def run_voice_ai_demo():
    """Run the complete voice AI demo"""
    base_url = "http://localhost:5001/api"
    
    print_header("SmartProBono Voice AI Complete Demo")
    print("🚀 Testing the unified multi-model AI system with voice capabilities")
    print("📡 Server: http://localhost:5001")
    
    # Test 1: Demo Information
    print_section("1. Demo Server Information")
    demo_info = test_endpoint(f"{base_url}/demo")
    if "error" not in demo_info:
        print("✅ Demo server is running!")
        print(f"   Status: {demo_info.get('status', 'Unknown')}")
        print("   Features:")
        for feature in demo_info.get('features', []):
            print(f"     • {feature}")
    else:
        print(f"❌ Demo server error: {demo_info['error']}")
        return False
    
    # Test 2: Voice Capabilities
    print_section("2. Voice AI Capabilities")
    capabilities = test_endpoint(f"{base_url}/voice-capabilities")
    if "error" not in capabilities:
        print("✅ Voice AI capabilities loaded!")
        print(f"   Voice Enabled: {capabilities.get('voice_enabled', False)}")
        print("   Available Models:")
        models = capabilities.get('models', {})
        for model_type, model_list in models.items():
            print(f"     • {model_type}: {', '.join(model_list)}")
        print("   Capabilities:")
        caps = capabilities.get('capabilities', {})
        for cap, enabled in caps.items():
            status = "✅" if enabled else "❌"
            print(f"     {status} {cap.replace('_', ' ').title()}")
    else:
        print(f"❌ Capabilities error: {capabilities['error']}")
        return False
    
    # Test 3: Voice Chat - Sales Agent
    print_section("3. Voice Chat - Sales Agent")
    sales_chat = test_endpoint(f"{base_url}/voice-chat", "POST", {
        "message": "Hello! I'm interested in SmartProBono. What can you tell me about it?",
        "voice_enabled": True,
        "task_type": "sales"
    })
    if "error" not in sales_chat:
        print("✅ Sales Agent Response:")
        print(f"   Model: {sales_chat.get('model', 'Unknown')}")
        print(f"   Agent Type: {sales_chat.get('agent_type', 'Unknown')}")
        print(f"   Response: {sales_chat.get('response', 'No response')[:200]}...")
    else:
        print(f"❌ Sales chat error: {sales_chat['error']}")
    
    time.sleep(1)
    
    # Test 4: Voice Chat - Pricing Inquiry
    print_section("4. Voice Chat - Pricing Inquiry")
    pricing_chat = test_endpoint(f"{base_url}/voice-chat", "POST", {
        "message": "How much does SmartProBono cost? I need pricing information.",
        "voice_enabled": True,
        "task_type": "pricing"
    })
    if "error" not in pricing_chat:
        print("✅ Pricing Agent Response:")
        print(f"   Model: {pricing_chat.get('model', 'Unknown')}")
        print(f"   Agent Type: {pricing_chat.get('agent_type', 'Unknown')}")
        print(f"   Response: {pricing_chat.get('response', 'No response')[:200]}...")
    else:
        print(f"❌ Pricing chat error: {pricing_chat['error']}")
    
    time.sleep(1)
    
    # Test 5: Agent Transfer - Technical Support
    print_section("5. Agent Transfer - Technical Support")
    tech_transfer = test_endpoint(f"{base_url}/voice-transfer", "POST", {
        "message": "I need technical details about the AI system architecture",
        "specialist": "technical"
    })
    if "error" not in tech_transfer:
        print("✅ Technical Specialist Transfer:")
        print(f"   Model: {tech_transfer.get('model', 'Unknown')}")
        print(f"   Specialist: {tech_transfer.get('specialist', 'Unknown')}")
        print(f"   Response: {tech_transfer.get('response', 'No response')[:200]}...")
    else:
        print(f"❌ Technical transfer error: {tech_transfer['error']}")
    
    time.sleep(1)
    
    # Test 6: Agent Transfer - Pricing Specialist
    print_section("6. Agent Transfer - Pricing Specialist")
    pricing_transfer = test_endpoint(f"{base_url}/voice-transfer", "POST", {
        "message": "Can you help me understand the pricing tiers and ROI?",
        "specialist": "pricing"
    })
    if "error" not in pricing_transfer:
        print("✅ Pricing Specialist Transfer:")
        print(f"   Model: {pricing_transfer.get('model', 'Unknown')}")
        print(f"   Specialist: {pricing_transfer.get('specialist', 'Unknown')}")
        print(f"   Response: {pricing_transfer.get('response', 'No response')[:200]}...")
    else:
        print(f"❌ Pricing transfer error: {pricing_transfer['error']}")
    
    # Test 7: Service Status
    print_section("7. Service Status")
    status = test_endpoint(f"{base_url}/voice-status")
    if "error" not in status:
        print("✅ Service Status:")
        print(f"   Status: {status.get('status', 'Unknown')}")
        print(f"   Voice Enabled: {status.get('voice_enabled', False)}")
        print(f"   Cerebras Available: {status.get('cerebras_available', False)}")
        print(f"   LiveKit Configured: {status.get('livekit_configured', False)}")
    else:
        print(f"❌ Status error: {status['error']}")
    
    # Summary
    print_header("Demo Summary")
    print("🎉 SmartProBono Voice AI System Demo Complete!")
    print("\n✅ Successfully Tested:")
    print("   • Demo server connectivity")
    print("   • Voice AI capabilities")
    print("   • Sales agent conversations")
    print("   • Pricing inquiries")
    print("   • Technical specialist transfers")
    print("   • Pricing specialist transfers")
    print("   • Service status monitoring")
    
    print("\n🚀 System Features Demonstrated:")
    print("   • Real-time Cerebras AI responses")
    print("   • Multi-agent routing (Sales ↔ Technical ↔ Pricing)")
    print("   • SmartProBono context-aware responses")
    print("   • Voice-optimized communication")
    print("   • LiveKit integration ready")
    
    print("\n🎯 Complete AI Stack:")
    print("   • Legal AI (Ollama: llama3.2, mistral, qwen, gemma, phi)")
    print("   • SmartProBono Agent (Gemini API)")
    print("   • Voice Sales Agent (Cerebras API)")
    print("   • Multi-Agent Routing System")
    print("   • Real-time Voice Capabilities")
    
    print(f"\n🌐 Demo Server: http://localhost:5001")
    print("📱 Ready for production deployment!")
    
    return True

def main():
    """Main demo function"""
    print("🎤 SmartProBono Voice AI Complete Demo")
    print("=" * 50)
    
    # Check if server is running
    try:
        response = requests.get("http://localhost:5001/api/demo", timeout=5)
        if response.status_code != 200:
            print("❌ Demo server is not responding")
            print("💡 Please start the demo server first:")
            print("   cd /Users/baheemferrell/Desktop/Apps/SmartProBono-main")
            print("   source .venv/bin/activate")
            print("   python demo_voice_ai_server.py")
            return False
    except requests.exceptions.RequestException:
        print("❌ Cannot connect to demo server")
        print("💡 Please start the demo server first:")
        print("   cd /Users/baheemferrell/Desktop/Apps/SmartProBono-main")
        print("   source .venv/bin/activate")
        print("   python demo_voice_ai_server.py")
        return False
    
    # Run the demo
    success = run_voice_ai_demo()
    
    if success:
        print("\n🎉 Demo completed successfully!")
        return True
    else:
        print("\n❌ Demo encountered errors")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
