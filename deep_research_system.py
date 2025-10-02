#!/usr/bin/env python3
"""
SmartProBono Deep Research System
Perplexity-style deep research using Cerebras and Exa
"""

import os
import time
from typing import List, Dict, Any
from exa_py import Exa
from cerebras.cloud.sdk import Cerebras

# Configure API keys
EXA_API_KEY = "a031df87-f273-4d4c-b3e8-89145c37c074"
CEREBRAS_API_KEY = os.environ.get("CEREBRAS_API_KEY", "csk-yfmevnrjp54jfmym4h2cynte6vec6f6er5v383xtc3txk4km")

# Initialize clients
try:
    client = Cerebras(api_key=CEREBRAS_API_KEY)
    exa = Exa(api_key=EXA_API_KEY)
    print("✅ Deep Research System initialized successfully")
except Exception as e:
    print(f"❌ Error initializing research system: {e}")

def search_web(query: str, num: int = 5) -> List[Dict[str, Any]]:
    """Search the web using Exa's auto search"""
    try:
        result = exa.search_and_contents(
            query,
            type="auto",
            num_results=num,
            text={"max_characters": 1000}
        )
        return result.results
    except Exception as e:
        print(f"❌ Search error: {e}")
        return []

def ask_ai(prompt: str, max_tokens: int = 600) -> str:
    """Get AI response from Cerebras"""
    try:
        chat_completion = client.chat.completions.create(
            messages=[{
                "role": "user",
                "content": prompt,
            }],
            model="llama-4-scout-17b-16e-instruct",
            max_tokens=max_tokens,
            temperature=0.2
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        print(f"❌ AI analysis error: {e}")
        return "Error in AI analysis"

def research_topic(query: str) -> Dict[str, Any]:
    """Main research function that orchestrates the entire process"""
    print(f"🔍 Researching: {query}")

    # Search for sources
    results = search_web(query, 5)
    print(f"📊 Found {len(results)} sources")

    # Get content from sources
    sources = []
    for result in results:
        content = result.text
        title = result.title
        if content and len(content) > 200:
            sources.append({
                "title": title,
                "content": content,
                "url": result.url
            })

    print(f"📄 Scraped {len(sources)} sources")

    if not sources:
        return {"summary": "No sources found", "insights": []}

    # Create context for AI analysis
    context = f"Research query: {query}\n\nSources:\n"
    for i, source in enumerate(sources[:4], 1):
        context += f"{i}. {source['title']}: {source['content'][:400]}...\n\n"

    # Ask AI to analyze and synthesize
    prompt = f"""{context}

Based on these sources, provide:
1. A comprehensive summary (2-3 sentences)
2. Three key insights as bullet points

Format your response exactly like this:
SUMMARY: [your summary here]

INSIGHTS:
- [insight 1]
- [insight 2]
- [insight 3]"""

    response = ask_ai(prompt)
    print("🧠 Analysis complete")

    return {
        "query": query, 
        "sources": len(sources), 
        "response": response,
        "source_details": sources
    }

def deeper_research_topic(query: str) -> Dict[str, Any]:
    """Two-layer research for better depth"""
    print(f"🔍 Deep Research: {query}")

    # Layer 1: Initial search
    results = search_web(query, 6)
    sources = []
    for result in results:
        if result.text and len(result.text) > 200:
            sources.append({
                "title": result.title, 
                "content": result.text,
                "url": result.url
            })

    print(f"Layer 1: Found {len(sources)} sources")

    if not sources:
        return {"summary": "No sources found", "insights": []}

    # Get initial analysis and identify follow-up topic
    context1 = f"Research query: {query}\n\nSources:\n"
    for i, source in enumerate(sources[:4], 1):
        context1 += f"{i}. {source['title']}: {source['content'][:300]}...\n\n"

    follow_up_prompt = f"""{context1}

Based on these sources, what's the most important follow-up question that would deepen our understanding of "{query}"?

Respond with just a specific search query (no explanation):"""

    follow_up_query = ask_ai(follow_up_prompt).strip().strip('"')
    print(f"Layer 2: Investigating '{follow_up_query}'")

    # Layer 2: Follow-up search
    follow_results = search_web(follow_up_query, 4)

    for result in follow_results:
        if result.text and len(result.text) > 200:
            sources.append({
                "title": f"[Follow-up] {result.title}", 
                "content": result.text,
                "url": result.url
            })

    print(f"Total sources: {len(sources)}")

    # Final synthesis
    all_context = f"Research query: {query}\nFollow-up: {follow_up_query}\n\nAll Sources:\n"
    for i, source in enumerate(sources[:7], 1):
        all_context += f"{i}. {source['title']}: {source['content'][:300]}...\n\n"

    final_prompt = f"""{all_context}

Provide a comprehensive analysis:

SUMMARY: [3-4 sentences covering key findings from both research layers]

INSIGHTS:
- [insight 1]
- [insight 2]
- [insight 3]
- [insight 4]

DEPTH GAINED: [1 sentence on how the follow-up search enhanced understanding]"""

    response = ask_ai(final_prompt)
    return {
        "query": query, 
        "follow_up_query": follow_up_query,
        "sources": len(sources), 
        "response": response,
        "source_details": sources
    }

def anthropic_multiagent_research(query: str) -> Dict[str, Any]:
    """
    Multi-agent research approach inspired by Anthropic:
    1. Lead agent plans and delegates
    2. Specialized subagents work in parallel
    3. Lead agent synthesizes results
    """
    print(f"🤖 Multi-Agent Research: {query}")
    print("-" * 50)

    # Step 1: Lead Agent - Task Decomposition & Delegation
    print("👨‍💼 LEAD AGENT: Planning and delegating...")

    delegation_prompt = f"""You are a Lead Research Agent. Break down this complex query into 3 specialized subtasks for parallel execution: "{query}"

For each subtask, provide:
- Clear objective
- Specific search focus
- Expected output

SUBTASK 1: [Core/foundational aspects]
SUBTASK 2: [Recent developments/trends]
SUBTASK 3: [Applications/implications]

Make each subtask distinct to avoid overlap."""

    plan = ask_ai(delegation_prompt)
    print("  ✓ Subtasks defined and delegated")

    # Step 2: Simulate Parallel Subagents
    print("\n🔍 SUBAGENTS: Working in parallel...")

    # Extract subtasks and create targeted searches
    subtask_searches = [
        f"{query} fundamentals principles",  # Core aspects
        f"{query} latest developments",      # Recent trends
        f"{query} applications real world"   # Implementation
    ]

    subagent_results = []
    for i, search_term in enumerate(subtask_searches, 1):
        print(f"  🤖 Subagent {i}: Researching {search_term}")
        results = search_web(search_term, 2)

        sources = []
        for result in results:
            if result.text and len(result.text) > 200:
                sources.append({
                    "title": result.title,
                    "content": result.text[:300],
                    "url": result.url
                })

        subagent_results.append({
            "subtask": i,
            "search_focus": search_term,
            "sources": sources
        })

    total_sources = sum(len(r["sources"]) for r in subagent_results)
    print(f"  📊 Combined: {total_sources} sources from {len(subagent_results)} agents")

    # Step 3: Lead Agent - Synthesis
    print("\n👨‍💼 LEAD AGENT: Synthesizing parallel findings...")

    # Combine all subagent findings
    synthesis_context = f"ORIGINAL QUERY: {query}\n\nSUBAGENT FINDINGS:\n"
    for result in subagent_results:
        synthesis_context += f"\nSubagent {result['subtask']} ({result['search_focus']}):\n"
        for source in result['sources'][:2]:  # Limit for brevity
            synthesis_context += f"- {source['title']}: {source['content']}...\n"

    synthesis_prompt = f"""{synthesis_context}

As the Lead Agent, synthesize these parallel findings into a comprehensive report:

EXECUTIVE SUMMARY:
[2-3 sentences covering the most important insights across all subagents]

INTEGRATED FINDINGS:
• [Key finding from foundational research]
• [Key finding from recent developments]
• [Key finding from applications research]
• [Cross-cutting insight that emerged]

RESEARCH QUALITY:
- Sources analyzed: {total_sources} across {len(subagent_results)} specialized agents
- Coverage: [How well the subtasks covered the topic]"""

    final_synthesis = ask_ai(synthesis_prompt)

    print("\n" + "=" * 50)
    print("🎯 MULTI-AGENT RESEARCH COMPLETE")
    print("=" * 50)
    print(final_synthesis)

    return {
        "query": query,
        "subagents": len(subagent_results),
        "total_sources": total_sources,
        "synthesis": final_synthesis,
        "subagent_results": subagent_results
    }

def legal_research_specialist(query: str) -> Dict[str, Any]:
    """Specialized research function for legal topics"""
    print(f"⚖️ Legal Research: {query}")
    
    # Add legal-specific search terms
    legal_query = f"{query} legal law case precedent statute regulation"
    
    # Use deeper research for legal topics
    result = deeper_research_topic(legal_query)
    
    # Add legal-specific analysis
    legal_analysis_prompt = f"""Based on this legal research about "{query}", provide:

LEGAL ANALYSIS:
- Key legal principles identified
- Relevant case law or statutes
- Current regulatory landscape
- Practical implications for legal practice

Format as:
LEGAL ANALYSIS:
[comprehensive legal analysis]

PRACTICAL IMPLICATIONS:
- [implication 1]
- [implication 2]
- [implication 3]"""

    legal_analysis = ask_ai(legal_analysis_prompt)
    
    return {
        **result,
        "legal_analysis": legal_analysis,
        "research_type": "legal_specialist"
    }

def main():
    """Demo the deep research system"""
    print("🔬 SmartProBono Deep Research System")
    print("=" * 50)
    
    # Test basic research
    print("\n1. Basic Research Test:")
    result1 = research_topic("artificial intelligence in legal practice")
    print(f"Query: {result1['query']}")
    print(f"Sources: {result1['sources']}")
    print(f"Response: {result1['response'][:200]}...")
    
    # Test deep research
    print("\n2. Deep Research Test:")
    result2 = deeper_research_topic("AI legal ethics and compliance")
    print(f"Query: {result2['query']}")
    print(f"Follow-up: {result2['follow_up_query']}")
    print(f"Total Sources: {result2['sources']}")
    
    # Test multi-agent research
    print("\n3. Multi-Agent Research Test:")
    result3 = anthropic_multiagent_research("legal technology trends 2024")
    print(f"Query: {result3['query']}")
    print(f"Subagents: {result3['subagents']}")
    print(f"Total Sources: {result3['total_sources']}")
    
    # Test legal specialist
    print("\n4. Legal Specialist Research Test:")
    result4 = legal_research_specialist("data privacy laws")
    print(f"Query: {result4['query']}")
    print(f"Research Type: {result4['research_type']}")
    
    print("\n🎉 Deep Research System Demo Complete!")

if __name__ == "__main__":
    main()
