#!/usr/bin/env python3
"""
SmartProBono LiveKit Voice Agent System
Real-time voice conversations with multi-agent capabilities
"""

import os
import asyncio
from pathlib import Path
from livekit import agents
from livekit.agents import Agent, AgentSession, JobContext, WorkerOptions
from livekit.plugins import openai, silero, deepgram
from livekit.agents import function_tool

# Configure API keys
DEEPGRAM_API_KEY = os.environ.get("DEEPGRAM_API_KEY", "56a34725a43e0999b9e3159545be8ff94948fc56")
CEREBRAS_API_KEY = os.environ.get("CEREBRAS_API_KEY", "csk-yfmevnrjp54jfmym4h2cynte6vec6f6er5v383xtc3txk4km")
LIVEKIT_API_KEY = os.environ.get("LIVEKIT_API_KEY", "APIDfFD86iZa6mQ")
LIVEKIT_API_SECRET = os.environ.get("LIVEKIT_API_SECRET", "OPatlk2JCTKKtzLeocVgce0Af5XfldXO0lL8aMDv9qbA")
LIVEKIT_WS_URL = os.environ.get("LIVEKIT_WS_URL", "wss://smartprobono-lr9wv8ch.livekit.cloud")

# Set environment variables
os.environ["DEEPGRAM_API_KEY"] = DEEPGRAM_API_KEY
os.environ["CEREBRAS_API_KEY"] = CEREBRAS_API_KEY
os.environ["LIVEKIT_API_KEY"] = LIVEKIT_API_KEY
os.environ["LIVEKIT_API_SECRET"] = LIVEKIT_API_SECRET
os.environ["LIVEKIT_WS_URL"] = LIVEKIT_WS_URL

print("✅ API keys configured for LiveKit Voice Agent")

def load_context():
    """Load all files from context directory"""
    context_dir = Path("context")
    context_dir.mkdir(exist_ok=True)
    
    all_content = ""
    for file_path in context_dir.glob("*"):
        if file_path.is_file():
            try:
                content = file_path.read_text(encoding='utf-8')
                all_content += f"\n=== {file_path.name} ===\n{content}\n"
            except Exception as e:
                print(f"Warning: Could not read {file_path}: {e}")
                pass
    
    return all_content.strip() or "No context files found"

# Load context once
SALES_CONTEXT = load_context()
print(f"📄 Loaded context: {len(SALES_CONTEXT)} characters")

class SalesAgent(Agent):
    """Main sales agent for SmartProBono platform"""
    
    def __init__(self):
        # Initialize components
        llm = openai.LLM.with_cerebras(model="llama-3.3-70b")
        stt = deepgram.STT()
        tts = deepgram.TTS()
        vad = silero.VAD.load()
        
        # System instructions with context
        instructions = f"""
        You are a sales agent for SmartProBono, an AI-powered legal assistance platform. 
        All text that you return will be spoken aloud, so don't use things like bullets, 
        slashes, or any other non-pronounceable punctuation.
        
        You have access to the following company information:
        
        {SALES_CONTEXT}
        
        CRITICAL RULES:
        - ONLY use information from the context above
        - If asked about something not in the context, say "I don't have that information"
        - DO NOT make up prices, features, or any other details
        - Quote directly from the context when possible
        - Be helpful and professional as a sales representative
        - Focus on the value proposition and benefits for legal professionals
        
        You can transfer to specialists when needed:
        - Use switch_to_tech_support() for technical questions
        - Use switch_to_pricing() for pricing discussions
        """
        
        super().__init__(
            instructions=instructions,
            stt=stt, llm=llm, tts=tts, vad=vad
        )
    
    async def on_enter(self):
        """Called when entering this agent"""
        print("Current Agent: 🏷️ Sales Agent 🏷️")
        await self.session.generate_reply(user_input="Give a short, 1 sentence greeting. Offer to answer any questions about SmartProBono.")
    
    @function_tool
    async def switch_to_tech_support(self):
        """Switch to a technical support representative"""
        await self.session.generate_reply(user_input="Confirm you are transferring to technical support")
        return TechnicalAgent()
    
    @function_tool
    async def switch_to_pricing(self):
        """Switch to pricing specialist"""
        await self.session.generate_reply(user_input="Confirm you are transferring to a pricing specialist")
        return PricingAgent()

class TechnicalAgent(Agent):
    """Technical specialist for detailed product specifications"""
    
    def __init__(self):
        # Initialize components with different voice
        llm = openai.LLM.with_cerebras(model="llama-3.3-70b")
        stt = deepgram.STT()
        tts = deepgram.TTS()  # Will use different voice settings
        vad = silero.VAD.load()
        
        instructions = f"""
        You are a technical specialist for SmartProBono communicating by voice. 
        All text that you return will be spoken aloud, so don't use things like 
        bullets, slashes, or any other non-pronounceable punctuation.
        
        You specialize in technical details, specifications, and implementation questions.
        Focus on technical accuracy and depth while explaining concepts clearly.
        
        You have access to the following company information:
        
        {SALES_CONTEXT}
        
        CRITICAL RULES:
        - ONLY use information from the context above
        - Focus on technical specifications and features
        - Explain technical concepts clearly for non-technical users
        - DO NOT make up technical details
        - Discuss AI models, integrations, security, and voice capabilities
        
        You can transfer to other specialists:
        - Use switch_to_sales() to return to general sales
        - Use switch_to_pricing() for pricing questions
        """
        
        super().__init__(
            instructions=instructions,
            stt=stt, llm=llm, tts=tts, vad=vad
        )
    
    async def on_enter(self):
        """Called when entering this agent"""
        print("Current Agent: 💻 Technical Specialist 💻")
        await self.session.say("Hi, I'm the technical specialist. I can help you with detailed technical questions about our SmartProBono platform.")
    
    @function_tool
    async def switch_to_sales(self):
        """Switch to a sales representative"""
        await self.session.generate_reply(user_input="Confirm you are transferring to the sales team")
        return SalesAgent()
    
    @function_tool
    async def switch_to_pricing(self):
        """Switch to pricing specialist"""
        await self.session.generate_reply(user_input="Confirm you are transferring to a pricing specialist")
        return PricingAgent()

class PricingAgent(Agent):
    """Pricing specialist for budget and cost discussions"""
    
    def __init__(self):
        # Initialize components with different voice
        llm = openai.LLM.with_cerebras(model="llama-3.3-70b")
        stt = deepgram.STT()
        tts = deepgram.TTS()  # Will use different voice settings
        vad = silero.VAD.load()
        
        instructions = f"""
        You are a pricing specialist for SmartProBono communicating by voice. 
        All text that you return will be spoken aloud, so don't use things like 
        bullets, slashes, or any other non-pronounceable punctuation.
        
        You specialize in pricing, budgets, discounts, and financial aspects.
        Help customers find the best value for their needs and understand ROI.
        
        You have access to the following company information:
        
        {SALES_CONTEXT}
        
        CRITICAL RULES:
        - ONLY use pricing information from the context above
        - Focus on value proposition and ROI
        - Help customers understand pricing tiers and options
        - DO NOT make up prices or discounts
        - Discuss cost savings and efficiency gains
        
        You can transfer to other specialists:
        - Use switch_to_sales() to return to general sales
        - Use switch_to_technical() for technical questions
        """
        
        super().__init__(
            instructions=instructions,
            stt=stt, llm=llm, tts=tts, vad=vad
        )
    
    async def on_enter(self):
        """Called when entering this agent"""
        print("Current Agent: 💰 Pricing Agent 💰")
        await self.session.say("Hello, I'm the pricing specialist. I can help you understand our pricing options and find the best value for your legal practice.")
    
    @function_tool
    async def switch_to_sales(self):
        """Switch back to sales representative"""
        await self.session.generate_reply(user_input="Confirm you are transferring to the sales team")
        return SalesAgent()
    
    @function_tool
    async def switch_to_technical(self):
        """Switch to technical specialist"""
        await self.session.generate_reply(user_input="Confirm you are transferring to technical support")
        return TechnicalAgent()

async def multi_agent_entrypoint(ctx: JobContext):
    """Multi-agent entry point for LiveKit"""
    print("🚀 Starting SmartProBono Voice Agent Session")
    print(f"📡 Connecting to room: {ctx.room.name}")
    
    await ctx.connect()
    
    # Create session
    session = AgentSession()
    
    # Start with sales agent
    await session.start(
        agent=SalesAgent(),
        room=ctx.room
    )
    
    print("✅ Voice agent session started successfully")

def main():
    """Main function to run the voice agent"""
    print("🎤 SmartProBono LiveKit Voice Agent")
    print("=" * 50)
    print("✅ Components initialized:")
    print(f"   • Deepgram STT/TTS: {DEEPGRAM_API_KEY[:10]}...")
    print(f"   • Cerebras LLM: {CEREBRAS_API_KEY[:10]}...")
    print(f"   • LiveKit: {LIVEKIT_WS_URL}")
    print(f"   • Context loaded: {len(SALES_CONTEXT)} characters")
    
    print("\n🎯 Available Agents:")
    print("   • Sales Agent - General inquiries and platform overview")
    print("   • Technical Agent - Technical specifications and integrations")
    print("   • Pricing Agent - Pricing tiers and ROI discussions")
    
    print("\n🔄 Agent Transfers:")
    print("   • Say 'I need technical details' → Technical Agent")
    print("   • Say 'Let's discuss pricing' → Pricing Agent")
    print("   • Any agent can transfer to any other agent")
    
    print("\n🚀 Starting LiveKit agent...")
    
    # Run the agent
    agents.run(
        WorkerOptions(
            entrypoint_fnc=multi_agent_entrypoint,
            api_key=LIVEKIT_API_KEY,
            api_secret=LIVEKIT_API_SECRET,
            ws_url=LIVEKIT_WS_URL
        )
    )

if __name__ == "__main__":
    main()
