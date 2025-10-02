#!/usr/bin/env python3
"""
Demo Voice AI Server for SmartProBono
Simple server to test voice AI integration
"""

import os
import sys
import asyncio
import json
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

app = Flask(__name__)
CORS(app)

# Set up API keys
CEREBRAS_API_KEY = os.environ.get("CEREBRAS_API_KEY", "csk-yfmevnrjp54jfmym4h2cynte6vec6f6er5v383xtc3txk4km")
LIVEKIT_API_KEY = os.environ.get("LIVEKIT_API_KEY", "APIDfFD86iZa6mQ")
LIVEKIT_API_SECRET = os.environ.get("LIVEKIT_API_SECRET", "OPatlk2JCTKKtzLeocVgce0Af5XfldXO0lL8aMDv9qbA")
LIVEKIT_WS_URL = os.environ.get("LIVEKIT_WS_URL", "wss://smartprobono-lr9wv8ch.livekit.cloud")

# Set environment variables
os.environ["CEREBRAS_API_KEY"] = CEREBRAS_API_KEY
os.environ["LIVEKIT_API_KEY"] = LIVEKIT_API_KEY
os.environ["LIVEKIT_API_SECRET"] = LIVEKIT_API_SECRET
os.environ["LIVEKIT_WS_URL"] = LIVEKIT_WS_URL

print("🚀 Demo Voice AI Server for SmartProBono")
print("=" * 50)
print(f"✅ Cerebras API Key: {CEREBRAS_API_KEY[:20]}...")
print(f"✅ LiveKit API Key: {LIVEKIT_API_KEY[:10]}...")
print(f"✅ LiveKit WebSocket URL: {LIVEKIT_WS_URL}")

class VoiceAIDemo:
    """Demo Voice AI Service"""
    
    def __init__(self):
        self.context = self.load_context()
        self.cerebras_available = False
        self.initialize_cerebras()
    
    def initialize_cerebras(self):
        """Initialize Cerebras client"""
        try:
            from cerebras.cloud.sdk import Cerebras
            self.cerebras_client = Cerebras(api_key=CEREBRAS_API_KEY)
            self.cerebras_available = True
            print("✅ Cerebras client initialized successfully")
        except ImportError:
            print("❌ Cerebras SDK not installed. Install with: pip install cerebras-cloud-sdk")
            self.cerebras_available = False
        except Exception as e:
            print(f"❌ Error initializing Cerebras: {e}")
            self.cerebras_available = False
    
    def load_context(self):
        """Load SmartProBono context"""
        return """
SmartProBono is an AI-powered legal assistance platform that connects pro bono lawyers with clients.
Key features include:
- AI-powered case management that increases efficiency by 60%
- Reduces legal costs for clients by 70%
- Seamless lawyer-client communication
- Real-time document analysis and legal research
- AI Legal Assistant for solo practitioners and small law firms

Pricing:
- Starter: $199/month (Basic case management, AI document analysis, client portal, email support)
- Professional: $499/month (Advanced AI agent, case law research, multi-user support, priority support)
- Enterprise: $999/month (White-label solution, API access, custom integrations, dedicated support, advanced analytics)

The platform is designed for Law Firms, Legal Aid Organizations, and Pro Bono Networks.
"""
    
    async def generate_response(self, message, agent_type="sales"):
        """Generate response using Cerebras API"""
        if not self.cerebras_available:
            return "❌ Cerebras API not available. Please check your API key and installation."
        
        try:
            # Agent-specific prompts
            prompts = {
                "sales": f"""
You are a professional sales agent for SmartProBono, an AI-powered legal platform.
You communicate by voice, so avoid bullets, slashes, or non-pronounceable punctuation.

You have access to the following company information:

{self.context}

CRITICAL RULES:
- ONLY use information from the context above
- If asked about something not in the context, say "I don't have that information available"
- DO NOT make up prices, features, or any other details
- Quote directly from the context when possible
- Be professional, helpful, and solution-focused
- Focus on the value proposition and ROI

You can transfer to specialists:
- Use switch_to_tech_support() for technical questions
- Use switch_to_pricing() for detailed pricing discussions
""",
                "technical": f"""
You are a technical specialist for SmartProBono communicating by voice.
You specialize in technical details, specifications, and implementation questions.

You have access to the following company information:

{self.context}

CRITICAL RULES:
- ONLY use information from the context above
- Focus on technical specifications and features
- Explain technical concepts clearly for non-technical users
- DO NOT make up technical details
- Be thorough but accessible in your explanations

You can transfer to other specialists:
- Use switch_to_sales() to return to general sales
- Use switch_to_pricing() for pricing questions
""",
                "pricing": f"""
You are a pricing specialist for SmartProBono communicating by voice.
You specialize in pricing, budgets, discounts, and financial aspects.

You have access to the following company information:

{self.context}

CRITICAL RULES:
- ONLY use pricing information from the context above
- Focus on value proposition and ROI
- Help customers understand pricing tiers and options
- DO NOT make up prices or discounts
- Emphasize the cost savings and efficiency gains

You can transfer to other specialists:
- Use switch_to_sales() to return to general sales
- Use switch_to_technical() for technical questions
"""
            }
            
            system_prompt = prompts.get(agent_type, prompts["sales"])
            
            # Prepare messages for Cerebras
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message}
            ]
            
            # Call Cerebras API
            stream = self.cerebras_client.chat.completions.create(
                messages=messages,
                model="qwen-3-235b-a22b-instruct-2507",
                stream=True,
                max_completion_tokens=1000,
                temperature=0.7,
                top_p=0.8
            )
            
            # Collect response from stream
            response_content = ""
            for chunk in stream:
                if hasattr(chunk, 'choices') and chunk.choices:
                    delta_content = chunk.choices[0].delta.content
                    if delta_content:
                        response_content += delta_content
            
            return response_content.strip() if response_content else "I'm not sure how to help with that. Could you please rephrase your question?"
            
        except Exception as e:
            return f"❌ Error generating response: {str(e)}"

# Initialize voice AI demo
voice_ai = VoiceAIDemo()

@app.route('/api/voice-capabilities', methods=['GET'])
def get_voice_capabilities():
    """Get voice AI capabilities"""
    return jsonify({
        "capabilities": {
            "legal_analysis": True,
            "case_management": True,
            "document_processing": True,
            "voice_conversations": voice_ai.cerebras_available,
            "multi_agent_transfers": voice_ai.cerebras_available,
            "real_time_communication": True
        },
        "models": {
            "ollama": ["llama3.2:3b", "mistral:7b", "qwen2.5:0.5b", "gemma2:2b", "phi3:mini"],
            "smartprobono_agent": ["gemini"],
            "voice_ai": ["cerebras"] if voice_ai.cerebras_available else []
        },
        "voice_enabled": voice_ai.cerebras_available
    })

@app.route('/api/voice-chat', methods=['POST'])
def voice_chat():
    """Voice-enabled AI chat endpoint"""
    try:
        data = request.json
        if not data or not data.get('message'):
            return jsonify({"error": "Missing message"}), 400
        
        message = data['message']
        task_type = data.get('task_type', 'chat')
        voice_enabled = data.get('voice_enabled', True)
        user_role = data.get('user_role', 'client')
        
        print(f"🎤 Voice chat request: {message[:50]}...")
        
        # Determine agent type based on message content
        agent_type = "sales"
        if "technical" in message.lower():
            agent_type = "technical"
        elif "pricing" in message.lower() or "cost" in message.lower() or "price" in message.lower():
            agent_type = "pricing"
        
        # Generate response
        response = asyncio.run(voice_ai.generate_response(message, agent_type))
        
        return jsonify({
            "response": response,
            "model": "cerebras-voice",
            "task_type": task_type,
            "voice_enabled": voice_enabled,
            "agent_type": agent_type,
            "timestamp": "2024-01-01T00:00:00Z"
        })
        
    except Exception as e:
        print(f"❌ Error in voice chat: {e}")
        return jsonify({"error": "Failed to generate response"}), 500

@app.route('/api/voice-transfer', methods=['POST'])
def voice_transfer():
    """Transfer to different AI specialist"""
    try:
        data = request.json
        if not data or not data.get('message'):
            return jsonify({"error": "Missing message"}), 400
        
        message = data['message']
        specialist = data.get('specialist', 'sales')
        user_role = data.get('user_role', 'client')
        
        print(f"🔄 Voice transfer request: {message[:50]}... to {specialist}")
        
        # Generate transfer response
        transfer_message = f"Transfer to {specialist} specialist: {message}"
        response = asyncio.run(voice_ai.generate_response(transfer_message, specialist))
        
        return jsonify({
            "response": response,
            "model": "cerebras-voice-transfer",
            "specialist": specialist,
            "timestamp": "2024-01-01T00:00:00Z"
        })
        
    except Exception as e:
        print(f"❌ Error in voice transfer: {e}")
        return jsonify({"error": "Failed to process transfer"}), 500

@app.route('/api/voice-status', methods=['GET'])
def voice_status():
    """Get voice AI service status"""
    return jsonify({
        "status": "active",
        "voice_enabled": voice_ai.cerebras_available,
        "cerebras_available": voice_ai.cerebras_available,
        "livekit_configured": bool(LIVEKIT_API_KEY and LIVEKIT_API_SECRET and LIVEKIT_WS_URL),
        "timestamp": "2024-01-01T00:00:00Z"
    })

@app.route('/api/demo', methods=['GET'])
def demo():
    """Demo endpoint showing available features"""
    return jsonify({
        "message": "🎤 SmartProBono Voice AI Demo Server",
        "features": [
            "Real-time voice conversations with Cerebras AI",
            "Multi-agent transfers (Sales ↔ Technical ↔ Pricing)",
            "SmartProBono context-aware responses",
            "LiveKit integration ready",
            "Complete voice AI system"
        ],
        "endpoints": [
            "GET /api/voice-capabilities - Get AI capabilities",
            "POST /api/voice-chat - Voice-enabled chat",
            "POST /api/voice-transfer - Transfer to specialists",
            "GET /api/voice-status - Service status",
            "GET /api/demo - This demo page"
        ],
        "status": "🚀 Ready for voice AI demonstrations!"
    })

@app.route('/', methods=['GET'])
def home():
    """Home page"""
    return jsonify({
        "message": "🎤 SmartProBono Voice AI Demo Server",
        "status": "running",
        "voice_ai_enabled": voice_ai.cerebras_available,
        "demo_url": "/api/demo"
    })

if __name__ == '__main__':
    print("\n🚀 Starting Demo Voice AI Server...")
    print("📡 Server will be available at: http://localhost:5001")
    print("🎤 Voice AI capabilities:", "✅ Enabled" if voice_ai.cerebras_available else "❌ Disabled")
    print("\n🔗 Available endpoints:")
    print("   GET  /api/demo - Demo information")
    print("   GET  /api/voice-capabilities - AI capabilities")
    print("   POST /api/voice-chat - Voice chat")
    print("   POST /api/voice-transfer - Transfer to specialists")
    print("   GET  /api/voice-status - Service status")
    print("\n🎯 Ready for testing!")
    
    app.run(host='0.0.0.0', port=5001, debug=True)
