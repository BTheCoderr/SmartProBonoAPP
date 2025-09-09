"""
Demo script for the complete CourtListener + Claude Legal AI Pipeline.
This script demonstrates the end-to-end workflow in VSCode.
"""
import os
import sys
import json
import time
from datetime import datetime

# Add current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents.intake_agent import intake
from agents.courtlistener_agent import search_live
from agents.vector_agent import search_local
from agents.summarizer_agent import summarize
from agents.compliance_agent import guardrails
from langgraph.main_graph import run_pipeline

def print_header(title):
    """Print a formatted header."""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)

def print_step(step, description):
    """Print a formatted step."""
    print(f"\n🔹 Step {step}: {description}")
    print("-" * 40)

def print_result(data, max_length=200):
    """Print formatted result data."""
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, str) and len(value) > max_length:
                print(f"  {key}: {value[:max_length]}...")
            else:
                print(f"  {key}: {value}")
    else:
        print(f"  Result: {data}")

def demo_individual_agents():
    """Demo individual agents."""
    print_header("INDIVIDUAL AGENTS DEMO")
    
    # Test input
    test_input = "I was charged with gun possession in Boston, what should I do?"
    print(f"Test Input: {test_input}")
    
    # Step 1: Intake Agent
    print_step(1, "Intake Agent - Extracting Legal Context")
    intake_result = intake(test_input)
    print_result(intake_result)
    
    # Step 2: CourtListener Agent
    print_step(2, "CourtListener Agent - Searching Live Case Law")
    try:
        courtlistener_result = search_live(intake_result)
        print_result(courtlistener_result)
    except Exception as e:
        print(f"  Error: {e}")
        print("  Note: This is expected if CourtListener API is not accessible")
    
    # Step 3: Vector Agent
    print_step(3, "Vector Agent - Searching Local Case Embeddings")
    try:
        vector_result = search_local(intake_result)
        print_result(vector_result)
    except Exception as e:
        print(f"  Error: {e}")
        print("  Note: This is expected if vector store is not seeded")
    
    # Step 4: Summarizer Agent (if we have cases)
    print_step(4, "Summarizer Agent - Claude Analysis")
    try:
        # Create mock context for demo
        context = {
            **intake_result,
            "courtlistener_results": courtlistener_result if 'courtlistener_result' in locals() else {"cases": []},
            "vector_results": vector_result if 'vector_result' in locals() else {"cases": []}
        }
        
        # Check if we have Claude API key
        if os.getenv("ANTHROPIC_API_KEY") and not os.getenv("ANTHROPIC_API_KEY").startswith("sk-your"):
            summary_result = summarize(context)
            print_result(summary_result)
        else:
            print("  Skipping Claude analysis - API key not configured")
            print("  Set ANTHROPIC_API_KEY in .env file to enable Claude analysis")
    except Exception as e:
        print(f"  Error: {e}")
        print("  Note: Claude analysis requires valid API key")
    
    # Step 5: Compliance Agent
    print_step(5, "Compliance Agent - Adding Legal Disclaimers")
    try:
        mock_analysis = {
            "case_summary": "Analysis of gun possession cases",
            "key_facts": ["Defendant was found with firearm", "No valid license"],
            "practical_advice": ["Contact criminal defense attorney immediately"],
            "context": intake_result
        }
        compliance_result = guardrails(mock_analysis)
        print_result(compliance_result)
    except Exception as e:
        print(f"  Error: {e}")

def demo_complete_pipeline():
    """Demo the complete LangGraph pipeline."""
    print_header("COMPLETE PIPELINE DEMO")
    
    test_cases = [
        "I was charged with gun possession in Boston, what should I do?",
        "I need help with a divorce case in Rhode Island",
        "My landlord is trying to evict me, is this legal?",
        "I was arrested for DUI last night, urgent help needed"
    ]
    
    for i, test_input in enumerate(test_cases, 1):
        print(f"\n🔸 Test Case {i}: {test_input}")
        print("-" * 50)
        
        try:
            start_time = time.time()
            result = run_pipeline(test_input)
            end_time = time.time()
            
            print(f"✅ Pipeline completed in {end_time - start_time:.2f} seconds")
            print(f"Success: {result.get('success', False)}")
            print(f"Compliance Level: {result.get('compliance_level', 'Unknown')}")
            
            if result.get('analysis', {}).get('case_summary'):
                print(f"Summary: {result['analysis']['case_summary'][:100]}...")
            
            if result.get('disclaimers'):
                print(f"Disclaimers: {len(result['disclaimers'])} added")
            
            if result.get('warnings'):
                print(f"Warnings: {len(result['warnings'])} added")
                
        except Exception as e:
            print(f"❌ Pipeline error: {e}")

def demo_api_endpoints():
    """Demo API endpoints."""
    print_header("API ENDPOINTS DEMO")
    
    print("Available endpoints:")
    print("  POST /api/legal-analysis - Complete legal analysis")
    print("  POST /api/case-search - Case law search only")
    print("  GET /api/vector-stats - Vector store statistics")
    print("  GET /health - Health check")
    
    print("\nExample API call:")
    print("curl -X POST http://localhost:5000/api/legal-analysis \\")
    print("  -H 'Content-Type: application/json' \\")
    print("  -d '{\"query\": \"I was charged with gun possession, what should I do?\"}'")

def demo_vscode_integration():
    """Demo VSCode integration features."""
    print_header("VSCODE INTEGRATION DEMO")
    
    print("VSCode Features Available:")
    print("  📁 Multi-root workspace: SmartProBono.code-workspace")
    print("  🐍 Python interpreter: legal_ai_backend/.venv/bin/python")
    print("  🔧 Tasks: Setup, Start Backend, Test Pipeline, Seed Data")
    print("  🚀 Launch configurations: Backend, Tests, Data Seeding")
    print("  📝 IntelliSense: Full code completion and error detection")
    
    print("\nVSCode Tasks:")
    print("  - Setup Legal AI Backend")
    print("  - Start Legal AI Backend")
    print("  - Test Legal AI Pipeline")
    print("  - Seed Case Law Data")
    print("  - Start Frontend")
    
    print("\nVSCode Launch Configurations:")
    print("  - Legal AI Backend (F5 to start API server)")
    print("  - Test Legal AI Pipeline (F5 to run tests)")
    print("  - Seed Case Law Data (F5 to seed data)")

def check_environment():
    """Check environment setup."""
    print_header("ENVIRONMENT CHECK")
    
    # Check Python version
    print(f"Python version: {sys.version}")
    
    # Check virtual environment
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("✅ Virtual environment active")
    else:
        print("⚠️ Virtual environment not active")
    
    # Check required packages
    required_packages = [
        'langgraph', 'chromadb', 'anthropic', 'requests', 
        'sentence_transformers', 'flask', 'flask_cors'
    ]
    
    print("\nRequired packages:")
    for package in required_packages:
        try:
            __import__(package)
            print(f"  ✅ {package}")
        except ImportError:
            print(f"  ❌ {package} - not installed")
    
    # Check environment variables
    print("\nEnvironment variables:")
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if api_key and not api_key.startswith("sk-your"):
        print("  ✅ ANTHROPIC_API_KEY configured")
    else:
        print("  ⚠️ ANTHROPIC_API_KEY not configured")
    
    openai_key = os.getenv("OPENAI_API_KEY")
    if openai_key and not openai_key.startswith("sk-your"):
        print("  ✅ OPENAI_API_KEY configured")
    else:
        print("  ⚠️ OPENAI_API_KEY not configured (optional)")

def main():
    """Main demo function."""
    print("🚀 Legal AI Backend - CourtListener + Claude Pipeline Demo")
    print("=" * 60)
    print(f"Demo started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Check environment
    check_environment()
    
    # Demo individual agents
    demo_individual_agents()
    
    # Demo complete pipeline
    demo_complete_pipeline()
    
    # Demo API endpoints
    demo_api_endpoints()
    
    # Demo VSCode integration
    demo_vscode_integration()
    
    print_header("DEMO COMPLETE")
    print("🎉 Legal AI Backend is ready for VSCode development!")
    print("\nNext steps:")
    print("1. Configure your Claude API key in .env file")
    print("2. Run: ./quick_start.sh")
    print("3. Open VSCode: code ../SmartProBono.code-workspace")
    print("4. Use F5 to start the backend or run tasks")
    print("5. Test the AI chat in the frontend")

if __name__ == "__main__":
    main()
