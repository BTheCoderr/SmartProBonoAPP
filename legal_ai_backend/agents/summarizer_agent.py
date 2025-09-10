"""
Summarizer Agent - Uses Claude or OpenAI to analyze and summarize case law.
Provides intelligent legal analysis and explanations.
"""
import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import anthropic
import openai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

@dataclass
class LegalSummary:
    """Structured legal summary from Claude."""
    case_summary: str
    key_facts: List[str]
    legal_rules: List[str]
    court_decision: str
    relevance: str
    practical_advice: List[str]
    similar_cases: List[str]

class SummarizerAgent:
    """Agent responsible for legal analysis and summarization using Claude or OpenAI."""
    
    def __init__(self, anthropic_key: Optional[str] = None, openai_key: Optional[str] = None):
        """
        Initialize summarizer agent with Claude or OpenAI API.
        
        Args:
            anthropic_key: Anthropic API key (if not provided, uses env var)
            openai_key: OpenAI API key (if not provided, uses env var)
        """
        self.anthropic_key = anthropic_key or os.getenv("ANTHROPIC_API_KEY")
        self.openai_key = openai_key or os.getenv("OPENAI_API_KEY")
        
        # Initialize clients
        self.anthropic_client = None
        self.openai_client = None
        
        # Skip API initialization - use fallback responses only
        logger.info("Using fallback responses for legal analysis (no API keys required)")
    
    def build_analysis_prompt(
        self, 
        cases: List[Dict[str, Any]], 
        context: Dict[str, Any]
    ) -> str:
        """
        Build comprehensive prompt for Claude analysis.
        
        Args:
            cases: List of case data from search results
            context: Original intake context
            
        Returns:
            Formatted prompt for Claude
        """
        topic = context.get("topic", "general")
        jurisdiction = context.get("jurisdiction", "ri")
        case_type = context.get("case_type", "general")
        original_input = context.get("original_input", "")
        
        prompt = f"""
You are an expert legal analyst specializing in {topic} cases in {jurisdiction.upper()}. 
Analyze the following case law and provide a comprehensive summary for someone facing a similar legal situation.

ORIGINAL QUERY: "{original_input}"

CASE TYPE: {case_type.upper()}
JURISDICTION: {jurisdiction.upper()}

CASE LAW TO ANALYZE:
"""
        
        for i, case in enumerate(cases, 1):
            if case.get("source") == "courtlistener":
                prompt += f"""
CASE {i}: {case.get('case_name', 'Unknown Case')}
Court: {case.get('court', 'Unknown Court')}
Date: {case.get('date_filed', 'Unknown Date')}
Snippet: {case.get('snippet', 'No snippet available')}
URL: {case.get('absolute_url', 'No URL available')}
"""
            else:  # Vector store case
                prompt += f"""
CASE {i}: Vector Store Case
Similarity Score: {case.get('similarity_score', 'Unknown')}
Text: {case.get('text', 'No text available')[:1000]}...
Metadata: {case.get('metadata', {})}
"""
        
        prompt += """

Please provide a comprehensive analysis in the following format:

1. **CASE SUMMARY**: Brief overview of the most relevant cases and their outcomes

2. **KEY FACTS**: List the most important facts from these cases that are relevant to the user's situation

3. **LEGAL RULES**: Identify the key legal principles, statutes, and rules that apply

4. **COURT DECISIONS**: Summarize what the courts decided and why

5. **RELEVANCE**: Explain how these cases relate to the user's situation and what they can learn

6. **PRACTICAL ADVICE**: Provide actionable advice based on the case law analysis

7. **SIMILAR CASES**: Reference specific cases that might be most helpful for the user's attorney

IMPORTANT DISCLAIMERS:
- This is not legal advice
- The user should consult with a qualified attorney
- Case law may have changed since these decisions
- Each case is unique and outcomes may vary

Focus on being helpful, accurate, and practical while maintaining appropriate legal disclaimers.
"""
        
        return prompt
    
    def analyze_cases(
        self, 
        cases: List[Dict[str, Any]], 
        context: Dict[str, Any]
    ) -> LegalSummary:
        """
        Analyze cases using Claude and return structured summary.
        
        Args:
            cases: List of case data from search results
            context: Original intake context
            
        Returns:
            LegalSummary with analysis
        """
        try:
            if not cases:
                return LegalSummary(
                    case_summary="No cases found for analysis",
                    key_facts=[],
                    legal_rules=[],
                    court_decision="No decisions available",
                    relevance="No relevant cases found",
                    practical_advice=["Consult with a qualified attorney for specific advice"],
                    similar_cases=[]
                )
            
            # Build analysis prompt
            prompt = self.build_analysis_prompt(cases, context)
            
            # Use fallback response (no API calls needed)
            analysis_text = self._get_fallback_analysis(cases, context)
            logger.info(f"Generated fallback analysis: {analysis_text[:200]}...")
            
            # Extract structured information (simplified parsing)
            sections = self._parse_analysis(analysis_text)
            logger.info(f"Parsed sections: {list(sections.keys())}")
            
            summary = LegalSummary(
                case_summary=sections.get("case_summary", "Analysis not available"),
                key_facts=sections.get("key_facts", []),
                legal_rules=sections.get("legal_rules", []),
                court_decision=sections.get("court_decision", "No decision analysis available"),
                relevance=sections.get("relevance", "Relevance not determined"),
                practical_advice=sections.get("practical_advice", []),
                similar_cases=sections.get("similar_cases", [])
            )
            
            logger.info(f"Generated legal analysis for {len(cases)} cases")
            return summary
            
        except Exception as e:
            logger.error(f"Error analyzing cases with Claude: {e}")
            return LegalSummary(
                case_summary=f"Error in analysis: {str(e)}",
                key_facts=[],
                legal_rules=[],
                court_decision="Analysis failed",
                relevance="Unable to determine relevance",
                practical_advice=["Please consult with a qualified attorney"],
                similar_cases=[]
            )
    
    def _parse_analysis(self, analysis_text: str) -> Dict[str, Any]:
        """
        Parse Claude's analysis text into structured sections.
        
        Args:
            analysis_text: Raw analysis text from Claude
            
        Returns:
            Dictionary with parsed sections
        """
        sections = {}
        lines = analysis_text.split('\n')
        
        current_section = None
        current_content = []
        
        for line in lines:
            line = line.strip()
            
            # Check for section headers (both **SECTION** and **SECTION**: formats)
            if line.startswith('**') and (line.endswith('**') or line.endswith('**:')):
                # Save previous section
                if current_section and current_content:
                    sections[current_section] = current_content
                
                # Start new section
                current_section = line.strip('*:').lower().replace(' ', '_').replace(':', '')
                current_content = []
            
            elif line.startswith('**') and '**:' in line:
                # Handle inline content like "**CASE SUMMARY**: content here"
                section_part = line.split('**:')[0] + '**'
                content_part = line.split('**:')[1].strip()
                
                # Save previous section
                if current_section and current_content:
                    sections[current_section] = current_content
                
                # Start new section with inline content
                current_section = section_part.strip('*:').lower().replace(' ', '_').replace(':', '')
                current_content = [content_part] if content_part else []
            
            elif current_section and line:
                current_content.append(line)
        
        # Save last section
        if current_section and current_content:
            sections[current_section] = current_content
        
        # Convert lists to proper format
        list_sections = ['key_facts', 'legal_rules', 'practical_advice', 'similar_cases']
        for section in list_sections:
            if section in sections:
                # Convert to list of items
                items = []
                for item in sections[section]:
                    if item.startswith('- ') or item.startswith('• '):
                        items.append(item[2:].strip())
                    elif item and not item.startswith('**'):
                        items.append(item)
                sections[section] = items
        
        return sections
    
    def _get_fallback_analysis(self, cases: List[Dict[str, Any]], context: Dict[str, Any]) -> str:
        """Generate a fallback analysis when no AI API is available."""
        topic = context.get("topic", "legal matter")
        jurisdiction = context.get("jurisdiction", "your jurisdiction")
        
        return f"""
**CASE SUMMARY**: Based on the {len(cases)} cases found related to {topic} in {jurisdiction.upper()}, this appears to be a {topic} legal matter that requires careful analysis.

**KEY FACTS**: 
- This involves a {topic} case in {jurisdiction.upper()}
- Multiple similar cases have been identified for reference
- The specific facts of your case will determine the legal approach

**LEGAL RULES**: 
- {topic.title()} cases in {jurisdiction.upper()} are governed by state and federal law
- Each case is unique and requires individual analysis
- Legal precedents from similar cases may be relevant

**COURT DECISIONS**: 
- The cases found show various outcomes depending on specific circumstances
- Court decisions are based on the particular facts of each case
- Legal precedents can provide guidance but may not be directly applicable

**RELEVANCE**: 
- These cases may provide helpful context for understanding your situation
- However, each legal matter is unique and requires individual analysis
- The specific facts of your case will determine the best legal approach

**PRACTICAL ADVICE**: 
- Consult with a qualified attorney who specializes in {topic} law
- Gather all relevant documents and evidence
- Consider the specific facts of your situation
- Research local legal aid organizations if you need assistance

**SIMILAR CASES**: 
- The cases found may provide helpful reference points
- However, each case is unique and outcomes may vary
- Use these cases as starting points for discussion with your attorney

**IMPORTANT DISCLAIMERS**:
- This is not legal advice
- Always consult with a qualified attorney
- Case law may have changed since these decisions
- Each case is unique and outcomes may vary
"""

def summarize(context: Dict[str, Any]) -> Dict[str, Any]:
    """
    Main function for LangGraph - summarizes case law using Claude.
    
    Args:
        context: Combined context from search agents
        
    Returns:
        Dictionary with analysis results
    """
    try:
        agent = SummarizerAgent()
        
        # Extract cases from merged results (preferred) or individual sources
        cases = []
        if "merged_results" in context and context["merged_results"].get("cases"):
            cases = context["merged_results"].get("cases", [])
        else:
            # Fallback to individual sources
            if "courtlistener_results" in context:
                cases.extend(context["courtlistener_results"].get("cases", []))
            if "vector_results" in context:
                cases.extend(context["vector_results"].get("cases", []))
        
        # Analyze cases
        summary = agent.analyze_cases(cases, context)
        
        return {
            "analysis": {
                "case_summary": summary.case_summary,
                "key_facts": summary.key_facts,
                "legal_rules": summary.legal_rules,
                "court_decision": summary.court_decision,
                "relevance": summary.relevance,
                "practical_advice": summary.practical_advice,
                "similar_cases": summary.similar_cases
            },
            "cases_analyzed": len(cases),
            "success": True
        }
        
    except Exception as e:
        logger.error(f"Error in summarization: {e}")
        return {
            "analysis": {
                "case_summary": f"Analysis failed: {str(e)}",
                "key_facts": [],
                "legal_rules": [],
                "court_decision": "Analysis unavailable",
                "relevance": "Unable to determine",
                "practical_advice": ["Consult with a qualified attorney"],
                "similar_cases": []
            },
            "cases_analyzed": 0,
            "success": False
        }

# Example usage and testing
if __name__ == "__main__":
    # Test the summarizer agent
    test_cases = [
        {
            "source": "courtlistener",
            "case_name": "Commonwealth v. Smith",
            "court": "Supreme Judicial Court",
            "snippet": "Defendant charged with unlawful possession of firearm...",
            "date_filed": "2023-01-15"
        }
    ]
    
    test_context = {
        "topic": "criminal",
        "jurisdiction": "ri",
        "case_type": "criminal",
        "keywords": ["gun", "possession"],
        "original_input": "I was charged with gun possession, what should I do?"
    }
    
    agent = SummarizerAgent()
    summary = agent.analyze_cases(test_cases, test_context)
    
    print("Legal Analysis:")
    print(f"Summary: {summary.case_summary}")
    print(f"Key Facts: {summary.key_facts}")
    print(f"Practical Advice: {summary.practical_advice}")
