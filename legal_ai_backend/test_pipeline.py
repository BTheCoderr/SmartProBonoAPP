"""
Test script for the Legal AI Pipeline.
Tests individual agents and the complete pipeline.
"""
import logging
import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents.intake_agent import intake
from agents.courtlistener_agent import search_live
from agents.vector_agent import search_local
from agents.summarizer_agent import summarize
from agents.compliance_agent import guardrails
from langgraph.main_graph import run_pipeline

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_intake_agent():
    """Test the intake agent."""
    print("Testing Intake Agent...")
    print("-" * 40)
    
    test_inputs = [
        "I was charged with gun possession in Boston, what should I do?",
        "I need help with a divorce case in Rhode Island",
        "My landlord is trying to evict me, is this legal?",
        "I was arrested for DUI last night, urgent help needed"
    ]
    
    for test_input in test_inputs:
        print(f"Input: {test_input}")
        result = intake(test_input)
        print(f"Topic: {result['topic']}")
        print(f"Jurisdiction: {result['jurisdiction']}")
        print(f"Case Type: {result['case_type']}")
        print(f"Urgency: {result['urgency']}")
        print(f"Keywords: {result['keywords']}")
        print()

def test_courtlistener_agent():
    """Test the CourtListener agent."""
    print("Testing CourtListener Agent...")
    print("-" * 40)
    
    test_context = {
        "topic": "criminal",
        "jurisdiction": "ri",
        "case_type": "criminal",
        "keywords": ["gun", "possession"],
        "original_input": "I was charged with gun possession in Rhode Island"
    }
    
    try:
        result = search_live(test_context)
        print(f"Success: {result['success']}")
        print(f"Cases Found: {result['total_found']}")
        print(f"Search Query: {result['search_query']}")
        
        if result['cases']:
            print("Sample Case:")
            case = result['cases'][0]
            print(f"  Name: {case['case_name']}")
            print(f"  Court: {case['court']}")
            print(f"  Snippet: {case['snippet'][:100]}...")
    except Exception as e:
        print(f"Error: {e}")

def test_vector_agent():
    """Test the vector agent."""
    print("Testing Vector Agent...")
    print("-" * 40)
    
    test_context = {
        "topic": "criminal",
        "jurisdiction": "ri",
        "case_type": "criminal",
        "keywords": ["gun", "possession"],
        "original_input": "I was charged with gun possession in Rhode Island"
    }
    
    try:
        result = search_local(test_context)
        print(f"Success: {result['success']}")
        print(f"Cases Found: {result['total_found']}")
        print(f"Search Query: {result['search_query']}")
        print(f"Collection: {result['collection_name']}")
        
        if result['cases']:
            print("Sample Case:")
            case = result['cases'][0]
            print(f"  Similarity: {case.get('similarity_score', 'N/A')}")
            print(f"  Text: {case['text'][:100]}...")
    except Exception as e:
        print(f"Error: {e}")

def test_summarizer_agent():
    """Test the summarizer agent."""
    print("Testing Summarizer Agent...")
    print("-" * 40)
    
    # Mock case data
    test_cases = [
        {
            "source": "courtlistener",
            "case_name": "State v. Smith",
            "court": "RI Superior Court",
            "snippet": "Defendant charged with unlawful possession of firearm..."
        }
    ]
    
    test_context = {
        "topic": "criminal",
        "jurisdiction": "ri",
        "case_type": "criminal",
        "keywords": ["gun", "possession"],
        "original_input": "I was charged with gun possession, what should I do?",
        "courtlistener_results": {"cases": test_cases},
        "vector_results": {"cases": []}
    }
    
    try:
        result = summarize(test_context)
        print(f"Success: {result['success']}")
        print(f"Cases Analyzed: {result['cases_analyzed']}")
        
        if result['analysis']:
            analysis = result['analysis']
            print(f"Summary: {analysis.get('case_summary', 'N/A')[:100]}...")
            print(f"Key Facts: {len(analysis.get('key_facts', []))}")
            print(f"Practical Advice: {len(analysis.get('practical_advice', []))}")
    except Exception as e:
        print(f"Error: {e}")

def test_compliance_agent():
    """Test the compliance agent."""
    print("Testing Compliance Agent...")
    print("-" * 40)
    
    test_analysis = {
        "case_summary": "Analysis of gun possession cases",
        "key_facts": ["Fact 1", "Fact 2"],
        "practical_advice": ["Advice 1", "Advice 2"],
        "context": {
            "topic": "criminal",
            "case_type": "criminal",
            "urgency": "high"
        }
    }
    
    try:
        result = guardrails(test_analysis)
        print(f"Success: {result['success']}")
        print(f"Compliance Level: {result.get('compliance_level', 'N/A')}")
        print(f"Disclaimers: {len(result.get('disclaimers', []))}")
        print(f"Warnings: {len(result.get('warnings', []))}")
        print(f"Recommendations: {len(result.get('recommendations', []))}")
    except Exception as e:
        print(f"Error: {e}")

def test_complete_pipeline():
    """Test the complete pipeline."""
    print("Testing Complete Pipeline...")
    print("-" * 40)
    
    test_inputs = [
        "I was charged with gun possession in Boston, what should I do?",
        "I need help with a divorce case in Rhode Island"
    ]
    
    for test_input in test_inputs:
        print(f"Input: {test_input}")
        try:
            result = run_pipeline(test_input)
            print(f"Success: {result.get('success', False)}")
            print(f"Compliance Level: {result.get('compliance_level', 'N/A')}")
            print(f"Disclaimers: {len(result.get('disclaimers', []))}")
            print(f"Warnings: {len(result.get('warnings', []))}")
            print(f"Errors: {len(result.get('errors', []))}")
            
            if result.get('analysis', {}).get('case_summary'):
                print(f"Summary: {result['analysis']['case_summary'][:100]}...")
        except Exception as e:
            print(f"Error: {e}")
        print()

def main():
    """Run all tests."""
    print("Legal AI Pipeline Test Suite")
    print("=" * 50)
    
    # Test individual agents
    test_intake_agent()
    test_courtlistener_agent()
    test_vector_agent()
    test_summarizer_agent()
    test_compliance_agent()
    
    # Test complete pipeline
    test_complete_pipeline()
    
    print("Test suite completed!")

if __name__ == "__main__":
    main()
