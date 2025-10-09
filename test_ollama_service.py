#!/usr/bin/env python3
"""
Test Ollama Service Directly
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from backend.services.ollama_ai_service import OllamaAIService

def test_service():
    print("🧪 Testing Ollama AI Service...")
    
    service = OllamaAIService()
    
    print(f"Available models: {service.available_models}")
    print(f"Working models: {service.working_models}")
    
    # Test model status
    status = service.test_models()
    print(f"Service status: {status}")
    
    # Test response generation
    print("\n🧪 Testing response generation...")
    response = service.generate_legal_response(
        message="What are my rights as a tenant?",
        task_type="chat",
        model="auto"
    )
    
    print(f"Response: {response}")
    
    return response

if __name__ == "__main__":
    test_service()
