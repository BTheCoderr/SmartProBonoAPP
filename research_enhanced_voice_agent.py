#!/usr/bin/env python3
"""
SmartProBono Research-Enhanced Voice Agent
Combines LiveKit voice agents with deep research capabilities
"""

import os
import asyncio
from pathlib import Path
from livekit import agents
from livekit.agents import Agent, AgentSession, JobContext, WorkerOptions
from livekit.plugins import openai, silero, deepgram
from livekit.agents import function_tool

# Import our deep research system
from deep_research_system import (
    research_topic, 
    deeper_research_topic, 
    anthropic_multiagent_research,
    legal_research_specialist
)

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

def load_context():
    """Load SmartProBono context"""
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

# Load context
SALES_CONTEXT = load_context()
print(f"📄 Loaded context: {len(SALES_CONTEXT)} characters")

class ResearchEnhancedSalesAgent(Agent):
    """Sales agent with deep research capabilities"""
    
    def __init__(self):
        # Initialize components
        llm = openai.LLM.with_cerebras(model="llama-3.3-70b")
        stt = deepgram.STT()
        tts = deepgram.TTS()
        vad = silero.VAD.load()
        
        # Enhanced instructions with research capabilities
        instructions = f"""
        You are a sales agent for SmartProBono with deep research capabilities. 
        All text that you return will be spoken aloud, so don't use things like 
        bullets, slashes, or any other non-pronounceable punctuation.
        
        You have access to the following company information:
        
        {SALES_CONTEXT}
        
        You also have access to real-time web research capabilities that allow you to:
        - Search for current legal industry trends and news
        - Research specific legal topics and regulations
        - Find competitive analysis and market insights
        - Provide up-to-date information on legal technology
        
        CRITICAL RULES:
        - ONLY use information from the context above or from research
        - If asked about current events or trends, use research capabilities
        - DO NOT make up prices, features, or any other details
        - Be helpful and professional as a sales representative
        - Focus on the value proposition and benefits for legal professionals
        
        You can transfer to specialists when needed:
        - Use switch_to_tech_support() for technical questions
        - Use switch_to_pricing() for pricing discussions
        - Use switch_to_research() for complex research tasks
        """
        
        super().__init__(
            instructions=instructions,
            stt=stt, llm=llm, tts=tts, vad=vad
        )
    
    async def on_enter(self):
        """Called when entering this agent"""
        print("Current Agent: 🏷️ Research-Enhanced Sales Agent 🏷️")
        await self.session.generate_reply(user_input="Give a short, 1 sentence greeting. Mention that you can research current legal trends and news.")
    
    @function_tool
    async def research_current_trends(self, topic: str):
        """Research current trends and news on a specific topic"""
        print(f"🔍 Researching current trends: {topic}")
        
        # Use basic research for current trends
        result = research_topic(f"{topic} legal industry trends 2024")
        
        # Format response for voice
        response = f"I researched current trends in {topic}. {result['response']}"
        
        await self.session.generate_reply(user_input=f"Share this research: {response}")
        return response
    
    @function_tool
    async def competitive_analysis(self, competitor: str):
        """Research competitive analysis for a specific competitor"""
        print(f"🔍 Analyzing competitor: {competitor}")
        
        result = research_topic(f"{competitor} legal technology platform features pricing")
        
        response = f"I analyzed {competitor}. {result['response']}"
        
        await self.session.generate_reply(user_input=f"Share this competitive analysis: {response}")
        return response
    
    @function_tool
    async def switch_to_tech_support(self):
        """Switch to a technical support representative"""
        await self.session.generate_reply(user_input="Confirm you are transferring to technical support")
        return ResearchEnhancedTechnicalAgent()
    
    @function_tool
    async def switch_to_pricing(self):
        """Switch to pricing specialist"""
        await self.session.generate_reply(user_input="Confirm you are transferring to a pricing specialist")
        return ResearchEnhancedPricingAgent()
    
    @function_tool
    async def switch_to_research(self):
        """Switch to research specialist"""
        await self.session.generate_reply(user_input="Confirm you are transferring to a research specialist")
        return ResearchSpecialistAgent()

class ResearchEnhancedTechnicalAgent(Agent):
    """Technical agent with research capabilities"""
    
    def __init__(self):
        llm = openai.LLM.with_cerebras(model="llama-3.3-70b")
        stt = deepgram.STT()
        tts = deepgram.TTS()
        vad = silero.VAD.load()
        
        instructions = f"""
        You are a technical specialist for SmartProBono with research capabilities.
        You specialize in technical details, specifications, and implementation questions.
        
        You have access to the following company information:
        
        {SALES_CONTEXT}
        
        You also have access to real-time research capabilities for:
        - Latest AI and legal technology developments
        - Technical specifications and integrations
        - Security and compliance updates
        - Industry standards and best practices
        
        CRITICAL RULES:
        - Focus on technical accuracy and depth
        - Use research for current technical developments
        - Explain technical concepts clearly for non-technical users
        - DO NOT make up technical details
        
        You can transfer to other specialists:
        - Use switch_to_sales() to return to general sales
        - Use switch_to_pricing() for pricing questions
        - Use switch_to_research() for complex research tasks
        """
        
        super().__init__(
            instructions=instructions,
            stt=stt, llm=llm, tts=tts, vad=vad
        )
    
    async def on_enter(self):
        """Called when entering this agent"""
        print("Current Agent: 💻 Research-Enhanced Technical Specialist 💻")
        await self.session.say("Hi, I'm the technical specialist with research capabilities. I can help with technical questions and current AI developments.")
    
    @function_tool
    async def research_ai_developments(self, topic: str):
        """Research latest AI developments in legal technology"""
        print(f"🔍 Researching AI developments: {topic}")
        
        result = deeper_research_topic(f"{topic} AI artificial intelligence legal technology 2024")
        
        response = f"I researched the latest AI developments in {topic}. {result['response']}"
        
        await self.session.generate_reply(user_input=f"Share this technical research: {response}")
        return response
    
    @function_tool
    async def research_security_updates(self, topic: str):
        """Research security and compliance updates"""
        print(f"🔍 Researching security updates: {topic}")
        
        result = research_topic(f"{topic} security compliance legal technology data protection")
        
        response = f"I researched security updates for {topic}. {result['response']}"
        
        await self.session.generate_reply(user_input=f"Share this security research: {response}")
        return response
    
    @function_tool
    async def switch_to_sales(self):
        """Switch to a sales representative"""
        await self.session.generate_reply(user_input="Confirm you are transferring to the sales team")
        return ResearchEnhancedSalesAgent()
    
    @function_tool
    async def switch_to_pricing(self):
        """Switch to pricing specialist"""
        await self.session.generate_reply(user_input="Confirm you are transferring to a pricing specialist")
        return ResearchEnhancedPricingAgent()
    
    @function_tool
    async def switch_to_research(self):
        """Switch to research specialist"""
        await self.session.generate_reply(user_input="Confirm you are transferring to a research specialist")
        return ResearchSpecialistAgent()

class ResearchEnhancedPricingAgent(Agent):
    """Pricing agent with market research capabilities"""
    
    def __init__(self):
        llm = openai.LLM.with_cerebras(model="llama-3.3-70b")
        stt = deepgram.STT()
        tts = deepgram.TTS()
        vad = silero.VAD.load()
        
        instructions = f"""
        You are a pricing specialist for SmartProBono with market research capabilities.
        You specialize in pricing, budgets, discounts, and financial aspects.
        
        You have access to the following company information:
        
        {SALES_CONTEXT}
        
        You also have access to real-time market research for:
        - Current legal technology pricing trends
        - Competitive pricing analysis
        - ROI studies and industry benchmarks
        - Market demand and pricing strategies
        
        CRITICAL RULES:
        - ONLY use pricing information from the context or research
        - Focus on value proposition and ROI
        - Use research for current market trends
        - Help customers understand pricing tiers and options
        
        You can transfer to other specialists:
        - Use switch_to_sales() to return to general sales
        - Use switch_to_technical() for technical questions
        - Use switch_to_research() for complex market research
        """
        
        super().__init__(
            instructions=instructions,
            stt=stt, llm=llm, tts=tts, vad=vad
        )
    
    async def on_enter(self):
        """Called when entering this agent"""
        print("Current Agent: 💰 Research-Enhanced Pricing Agent 💰")
        await self.session.say("Hello, I'm the pricing specialist with market research capabilities. I can help with pricing and current market trends.")
    
    @function_tool
    async def market_pricing_analysis(self, market_segment: str):
        """Research current market pricing for specific segments"""
        print(f"🔍 Analyzing market pricing: {market_segment}")
        
        result = research_topic(f"{market_segment} legal technology pricing market analysis 2024")
        
        response = f"I analyzed current market pricing for {market_segment}. {result['response']}"
        
        await self.session.generate_reply(user_input=f"Share this market analysis: {response}")
        return response
    
    @function_tool
    async def roi_research(self, use_case: str):
        """Research ROI studies for specific use cases"""
        print(f"🔍 Researching ROI for: {use_case}")
        
        result = research_topic(f"{use_case} legal technology ROI return on investment case studies")
        
        response = f"I researched ROI for {use_case}. {result['response']}"
        
        await self.session.generate_reply(user_input=f"Share this ROI research: {response}")
        return response
    
    @function_tool
    async def switch_to_sales(self):
        """Switch back to sales representative"""
        await self.session.generate_reply(user_input="Confirm you are transferring to the sales team")
        return ResearchEnhancedSalesAgent()
    
    @function_tool
    async def switch_to_technical(self):
        """Switch to technical specialist"""
        await self.session.generate_reply(user_input="Confirm you are transferring to technical support")
        return ResearchEnhancedTechnicalAgent()
    
    @function_tool
    async def switch_to_research(self):
        """Switch to research specialist"""
        await self.session.generate_reply(user_input="Confirm you are transferring to a research specialist")
        return ResearchSpecialistAgent()

class ResearchSpecialistAgent(Agent):
    """Dedicated research specialist for complex research tasks"""
    
    def __init__(self):
        llm = openai.LLM.with_cerebras(model="llama-3.3-70b")
        stt = deepgram.STT()
        tts = deepgram.TTS()
        vad = silero.VAD.load()
        
        instructions = f"""
        You are a research specialist for SmartProBono with advanced research capabilities.
        You can perform deep, multi-layer research on complex topics.
        
        You have access to:
        - Basic research for quick insights
        - Deep research with follow-up questions
        - Multi-agent research for comprehensive analysis
        - Legal-specific research for legal topics
        
        CRITICAL RULES:
        - Provide comprehensive, well-researched responses
        - Use multiple research layers for complex topics
        - Focus on accuracy and depth
        - Present findings clearly and professionally
        
        You can transfer to other specialists:
        - Use switch_to_sales() to return to sales
        - Use switch_to_technical() for technical questions
        - Use switch_to_pricing() for pricing discussions
        """
        
        super().__init__(
            instructions=instructions,
            stt=stt, llm=llm, tts=tts, vad=vad
        )
    
    async def on_enter(self):
        """Called when entering this agent"""
        print("Current Agent: 🔬 Research Specialist 🔬")
        await self.session.say("Hello, I'm the research specialist. I can perform deep research on complex topics using multiple sources and analysis methods.")
    
    @function_tool
    async def deep_research(self, topic: str):
        """Perform deep, multi-layer research on a topic"""
        print(f"🔍 Deep research: {topic}")
        
        result = deeper_research_topic(topic)
        
        response = f"I performed deep research on {topic}. {result['response']}"
        
        await self.session.generate_reply(user_input=f"Share this deep research: {response}")
        return response
    
    @function_tool
    async def multi_agent_research(self, topic: str):
        """Perform multi-agent research for comprehensive analysis"""
        print(f"🤖 Multi-agent research: {topic}")
        
        result = anthropic_multiagent_research(topic)
        
        response = f"I performed comprehensive multi-agent research on {topic}. {result['synthesis']}"
        
        await self.session.generate_reply(user_input=f"Share this comprehensive research: {response}")
        return response
    
    @function_tool
    async def legal_research(self, topic: str):
        """Perform specialized legal research"""
        print(f"⚖️ Legal research: {topic}")
        
        result = legal_research_specialist(topic)
        
        response = f"I performed specialized legal research on {topic}. {result['response']}"
        
        await self.session.generate_reply(user_input=f"Share this legal research: {response}")
        return response
    
    @function_tool
    async def switch_to_sales(self):
        """Switch back to sales representative"""
        await self.session.generate_reply(user_input="Confirm you are transferring to the sales team")
        return ResearchEnhancedSalesAgent()
    
    @function_tool
    async def switch_to_technical(self):
        """Switch to technical specialist"""
        await self.session.generate_reply(user_input="Confirm you are transferring to technical support")
        return ResearchEnhancedTechnicalAgent()
    
    @function_tool
    async def switch_to_pricing(self):
        """Switch to pricing specialist"""
        await self.session.generate_reply(user_input="Confirm you are transferring to a pricing specialist")
        return ResearchEnhancedPricingAgent()

async def research_enhanced_entrypoint(ctx: JobContext):
    """Entry point for research-enhanced voice agent"""
    print("🚀 Starting SmartProBono Research-Enhanced Voice Agent")
    print(f"📡 Connecting to room: {ctx.room.name}")
    
    await ctx.connect()
    
    # Create session
    session = AgentSession()
    
    # Start with research-enhanced sales agent
    await session.start(
        agent=ResearchEnhancedSalesAgent(),
        room=ctx.room
    )
    
    print("✅ Research-enhanced voice agent session started")

def main():
    """Main function to run the research-enhanced voice agent"""
    print("🔬 SmartProBono Research-Enhanced Voice Agent")
    print("=" * 60)
    print("✅ Components initialized:")
    print(f"   • Deepgram STT/TTS: {DEEPGRAM_API_KEY[:10]}...")
    print(f"   • Cerebras LLM: {CEREBRAS_API_KEY[:10]}...")
    print(f"   • LiveKit: {LIVEKIT_WS_URL}")
    print(f"   • Exa Research: Ready")
    print(f"   • Context loaded: {len(SALES_CONTEXT)} characters")
    
    print("\n🎯 Available Research-Enhanced Agents:")
    print("   • Sales Agent - General inquiries + current trends research")
    print("   • Technical Agent - Technical specs + AI developments research")
    print("   • Pricing Agent - Pricing + market analysis research")
    print("   • Research Specialist - Deep multi-layer research")
    
    print("\n🔬 Research Capabilities:")
    print("   • Real-time web search with Exa")
    print("   • Multi-layer deep research")
    print("   • Multi-agent parallel research")
    print("   • Legal-specific research")
    print("   • Current trends and competitive analysis")
    
    print("\n🔄 Agent Transfers:")
    print("   • Say 'research current trends' → Research capabilities")
    print("   • Say 'I need technical details' → Technical Agent")
    print("   • Say 'Let's discuss pricing' → Pricing Agent")
    print("   • Say 'deep research on X' → Research Specialist")
    
    print("\n🚀 Starting research-enhanced voice agent...")
    
    # Run the agent
    agents.run(
        WorkerOptions(
            entrypoint_fnc=research_enhanced_entrypoint,
            api_key=LIVEKIT_API_KEY,
            api_secret=LIVEKIT_API_SECRET,
            ws_url=LIVEKIT_WS_URL
        )
    )

if __name__ == "__main__":
    main()
