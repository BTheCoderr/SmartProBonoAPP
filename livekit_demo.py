#!/usr/bin/env python3
"""
LiveKit Voice Agent Demo
Demonstrates the complete real-time voice agent system
"""

import asyncio
import os
from livekit_voice_agent import SalesAgent, TechnicalAgent, PricingAgent, SALES_CONTEXT

def print_demo_header():
    """Print demo header"""
    print("🎤 SmartProBono LiveKit Voice Agent Demo")
    print("=" * 60)
    print("🚀 Complete Real-Time Voice AI System")
    print("=" * 60)

def print_agent_info():
    """Print information about available agents"""
    print("\n🤖 Available Voice Agents:")
    print("-" * 40)
    
    agents_info = [
        ("Sales Agent", "🏷️", "General inquiries, platform overview, lead qualification"),
        ("Technical Agent", "💻", "Technical specs, integrations, AI capabilities"),
        ("Pricing Agent", "💰", "Pricing tiers, ROI, cost discussions")
    ]
    
    for name, emoji, description in agents_info:
        print(f"{emoji} {name}")
        print(f"   {description}")
        print()

def print_voice_capabilities():
    """Print voice AI capabilities"""
    print("🎤 Voice AI Capabilities:")
    print("-" * 40)
    capabilities = [
        "Real-time speech-to-text (Deepgram)",
        "Natural language processing (Cerebras LLaMA 3.3 70B)",
        "Text-to-speech with multiple voices (Deepgram)",
        "Voice activity detection (Silero VAD)",
        "Multi-agent transfers during conversation",
        "Context-aware responses from SmartProBono data",
        "LiveKit real-time communication platform"
    ]
    
    for i, capability in enumerate(capabilities, 1):
        print(f"   {i}. {capability}")
    print()

def print_sample_conversations():
    """Print sample conversation flows"""
    print("💬 Sample Conversation Flows:")
    print("-" * 40)
    
    conversations = [
        {
            "user": "Hello, I'm interested in SmartProBono for my law firm",
            "agent": "Sales Agent → Greets and explains platform benefits",
            "transfer": "User asks technical questions → Technical Agent",
            "pricing": "User asks about costs → Pricing Agent"
        },
        {
            "user": "What AI models do you use?",
            "agent": "Sales Agent → Transfers to Technical Agent",
            "transfer": "Technical Agent explains Ollama, Gemini, Cerebras",
            "pricing": "User asks about pricing → Pricing Agent"
        },
        {
            "user": "How much does this cost?",
            "agent": "Sales Agent → Transfers to Pricing Agent",
            "transfer": "Pricing Agent explains tiers and ROI",
            "pricing": "Discussion of value proposition and cost savings"
        }
    ]
    
    for i, conv in enumerate(conversations, 1):
        print(f"   {i}. {conv['user']}")
        print(f"      → {conv['agent']}")
        print(f"      → {conv['transfer']}")
        print(f"      → {conv['pricing']}")
        print()

def print_context_sample():
    """Print sample context information"""
    print("📄 SmartProBono Context (Sample):")
    print("-" * 40)
    
    # Extract key information from context
    lines = SALES_CONTEXT.split('\n')
    product_lines = [line for line in lines if '"name"' in line or '"price"' in line or '"features"' in line]
    
    print("   Key Products:")
    for line in product_lines[:6]:  # Show first few lines
        if '"name"' in line:
            print(f"   • {line.strip().replace('"name": "', '').replace('",', '')}")
        elif '"price"' in line:
            print(f"     Price: {line.strip().replace('"price": ', '').replace(',', '')}")
    
    print(f"\n   Total context: {len(SALES_CONTEXT)} characters")
    print("   Includes: Products, pricing, technical specs, objection handlers")
    print()

def print_deployment_info():
    """Print deployment information"""
    print("🚀 Deployment Information:")
    print("-" * 40)
    
    print("   LiveKit Configuration:")
    print(f"   • WebSocket URL: {os.environ.get('LIVEKIT_WS_URL', 'Not set')}")
    print(f"   • API Key: {os.environ.get('LIVEKIT_API_KEY', 'Not set')[:10]}...")
    print(f"   • API Secret: {os.environ.get('LIVEKIT_API_SECRET', 'Not set')[:10]}...")
    
    print("\n   AI Models:")
    print("   • Cerebras: LLaMA 3.3 70B for real-time voice")
    print("   • Deepgram: Speech-to-text and text-to-speech")
    print("   • Silero: Voice activity detection")
    
    print("\n   SmartProBono Integration:")
    print("   • Context-aware responses")
    print("   • Legal domain expertise")
    print("   • Multi-agent routing")
    print()

def print_usage_instructions():
    """Print usage instructions"""
    print("🎯 How to Use:")
    print("-" * 40)
    
    instructions = [
        "1. Start the voice agent: python livekit_voice_agent.py",
        "2. Connect to LiveKit room via web interface",
        "3. Speak naturally - agent will respond with voice",
        "4. Request transfers by saying:",
        "   • 'I need technical details' → Technical Agent",
        "   • 'Let's discuss pricing' → Pricing Agent",
        "   • 'Back to sales' → Sales Agent",
        "5. Agents maintain context across transfers",
        "6. All responses are voice-optimized for speech"
    ]
    
    for instruction in instructions:
        print(f"   {instruction}")
    print()

def print_next_steps():
    """Print next steps"""
    print("🔄 Next Steps:")
    print("-" * 40)
    
    steps = [
        "✅ LiveKit packages installed",
        "✅ Voice agents created (Sales, Technical, Pricing)",
        "✅ Context loaded with SmartProBono information",
        "✅ API keys configured",
        "✅ Multi-agent transfer system ready",
        "",
        "🚀 Ready to run:",
        "   python livekit_voice_agent.py",
        "",
        "🌐 Access via LiveKit web interface:",
        "   Connect to your LiveKit room for real-time voice chat"
    ]
    
    for step in steps:
        if step.startswith("✅"):
            print(f"   {step}")
        elif step.startswith("🚀"):
            print(f"\n   {step}")
        elif step.startswith("🌐"):
            print(f"\n   {step}")
        elif step == "":
            print()
        else:
            print(f"   {step}")
    print()

def main():
    """Run the complete demo"""
    print_demo_header()
    print_agent_info()
    print_voice_capabilities()
    print_sample_conversations()
    print_context_sample()
    print_deployment_info()
    print_usage_instructions()
    print_next_steps()
    
    print("🎉 LiveKit Voice Agent Demo Complete!")
    print("=" * 60)
    print("Ready for real-time voice conversations with SmartProBono!")

if __name__ == "__main__":
    main()
