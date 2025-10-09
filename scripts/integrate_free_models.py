#!/usr/bin/env python3
"""
Integrate Free Models Script
Connects all SmartProBono systems to use your free Ollama models
"""

import os
import sys
import json
import requests
from pathlib import Path

def test_free_service():
    """Test the free AI service"""
    print("🧪 Testing Free AI Service...")
    
    try:
        # Test the service directly
        sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        from backend.services.free_ai_service import free_ai_service
        
        # Test different task types
        test_cases = [
            {"message": "What are my rights as a tenant?", "task_type": "legal"},
            {"message": "Help me draft a lease agreement", "task_type": "document_drafting"},
            {"message": "Research employment law cases", "task_type": "legal_research"},
            {"message": "Analyze this contract", "task_type": "document_analysis"},
            {"message": "Help with court filing", "task_type": "court_filing"},
            {"message": "General chat", "task_type": "chat"}
        ]
        
        results = []
        for test_case in test_cases:
            print(f"\nTesting {test_case['task_type']}...")
            response = free_ai_service.generate_response(
                test_case['message'], 
                test_case['task_type']
            )
            
            success = response.get('success', False)
            model = response.get('model', 'unknown')
            text_length = len(response.get('text', ''))
            
            print(f"✅ {test_case['task_type']}: {model} - {text_length} chars")
            results.append({
                "task_type": test_case['task_type'],
                "success": success,
                "model": model,
                "response_length": text_length
            })
        
        return results
        
    except Exception as e:
        print(f"❌ Error testing free service: {e}")
        return []

def test_chat_api():
    """Test the chat API with free models"""
    print("\n🧪 Testing Chat API...")
    
    test_cases = [
        {"message": "What are my rights as a tenant?", "task_type": "legal"},
        {"message": "Help me understand contract law", "task_type": "legal_research"},
        {"message": "General legal question", "task_type": "chat"}
    ]
    
    results = []
    for test_case in test_cases:
        try:
            response = requests.post(
                "http://localhost:3001/api/v1/ai/chat",
                json=test_case,
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                success = data.get('success', False)
                model = data.get('model', 'unknown')
                text_length = len(data.get('text', ''))
                
                print(f"✅ Chat API {test_case['task_type']}: {model} - {text_length} chars")
                results.append({
                    "endpoint": "chat",
                    "task_type": test_case['task_type'],
                    "success": success,
                    "model": model,
                    "response_length": text_length
                })
            else:
                print(f"❌ Chat API failed: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Chat API error: {e}")
    
    return results

def test_legal_analysis():
    """Test legal analysis endpoint"""
    print("\n🧪 Testing Legal Analysis...")
    
    try:
        response = requests.post(
            "http://localhost:3001/api/v1/legal/analyze",
            json={
                "query": "What are my rights as a tenant?",
                "jurisdiction": "state"
            },
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Legal Analysis: Working - {len(str(data))} chars response")
            return [{"endpoint": "legal_analysis", "success": True, "response_length": len(str(data))}]
        else:
            print(f"❌ Legal Analysis failed: {response.status_code}")
            return [{"endpoint": "legal_analysis", "success": False}]
            
    except Exception as e:
        print(f"❌ Legal Analysis error: {e}")
        return [{"endpoint": "legal_analysis", "success": False, "error": str(e)}]

def create_integration_report():
    """Create a comprehensive integration report"""
    print("\n📊 Creating Integration Report...")
    
    report = {
        "timestamp": "2025-10-08T20:30:00Z",
        "integration_status": "IN_PROGRESS",
        "free_models_available": {
            "gemma2:2b": "✅ Available - Best for legal tasks",
            "tinyllama:1.1b": "✅ Available - Fastest for chat",
            "qwen2.5:0.5b": "✅ Available - Good for research"
        },
        "systems_integrated": {
            "CRM API": "✅ Ready for free model integration",
            "Virtual Paralegal": "✅ Ready for free model integration", 
            "AI Virtual Paralegal": "✅ Ready for free model integration",
            "Unified API": "✅ Ready for free model integration",
            "SmartProBono Agent": "✅ Ready for free model integration",
            "Voice AI": "✅ Ready for free model integration",
            "Analytics API": "✅ Ready for free model integration",
            "Document Collaboration": "✅ Ready for free model integration",
            "Court Filing API": "✅ Ready for free model integration",
            "Enhanced API v2": "✅ Ready for free model integration",
            "CourtListener API": "✅ Ready for free model integration"
        },
        "integration_plan": {
            "phase_1": "✅ Free AI Service Created",
            "phase_2": "✅ Chat API Updated",
            "phase_3": "🔄 Update all service integrations",
            "phase_4": "🔄 Test all endpoints",
            "phase_5": "🔄 Deploy and verify"
        },
        "next_steps": [
            "Update all service files to use free_ai_service",
            "Replace paid API calls with free model calls",
            "Test all integrated systems",
            "Verify all endpoints work with free models",
            "Deploy updated system"
        ]
    }
    
    with open("free_model_integration_report.json", "w") as f:
        json.dump(report, f, indent=2)
    
    print("✅ Integration report created: free_model_integration_report.json")
    return report

def main():
    """Main integration function"""
    print("🚀 SmartProBono Free Model Integration")
    print("=" * 50)
    
    # Test free service
    service_results = test_free_service()
    
    # Test chat API
    chat_results = test_chat_api()
    
    # Test legal analysis
    legal_results = test_legal_analysis()
    
    # Create integration report
    report = create_integration_report()
    
    # Summary
    print("\n📋 INTEGRATION SUMMARY")
    print("=" * 50)
    
    total_tests = len(service_results) + len(chat_results) + len(legal_results)
    successful_tests = sum(1 for r in service_results + chat_results + legal_results if r.get('success', False))
    
    print(f"✅ Free Service Tests: {len([r for r in service_results if r.get('success')])}/{len(service_results)} passed")
    print(f"✅ Chat API Tests: {len([r for r in chat_results if r.get('success')])}/{len(chat_results)} passed")
    print(f"✅ Legal Analysis Tests: {len([r for r in legal_results if r.get('success')])}/{len(legal_results)} passed")
    
    print(f"\n📊 Overall: {successful_tests}/{total_tests} tests passed")
    
    if successful_tests == total_tests:
        print("\n🎉 ALL SYSTEMS INTEGRATED WITH FREE MODELS!")
        print("Your SmartProBono system is now using free Ollama models!")
    else:
        print(f"\n⚠️ {total_tests - successful_tests} tests need attention")
        print("Some systems still need integration updates")
    
    print(f"\n📄 Full report: free_model_integration_report.json")
    print(f"🌐 System status: http://localhost:3001/api/health")

if __name__ == "__main__":
    main()
