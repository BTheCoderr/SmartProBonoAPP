#!/usr/bin/env python3
"""
Fix Model Selection - Use Available Ollama Models
Updates the system to use the actual models you have available
"""

import os
import sys
import json
import requests

def test_model_response(model_name):
    """Test a specific model with a legal question"""
    print(f"\n🧪 Testing {model_name}...")
    
    try:
        payload = {
            "model": model_name,
            "prompt": "What are tenant rights in Rhode Island? Give a brief legal explanation.",
            "stream": False,
            "options": {
                "temperature": 0.7,
                "top_p": 0.9,
                "max_tokens": 500
            }
        }
        
        response = requests.post(
            "http://localhost:11434/api/generate",
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            response_text = result.get("response", "").strip()
            print(f"✅ {model_name} - Response length: {len(response_text)} chars")
            print(f"Preview: {response_text[:100]}...")
            return True, response_text
        else:
            print(f"❌ {model_name} - Failed ({response.status_code})")
            return False, None
            
    except Exception as e:
        print(f"❌ {model_name} - Error: {e}")
        return False, None

def find_best_model():
    """Test all available models and find the best one"""
    print("🔍 Testing all available models for legal responses...")
    
    models = ["tinyllama:1.1b", "gemma2:2b", "qwen2.5:0.5b"]
    results = {}
    
    for model in models:
        success, response = test_model_response(model)
        if success:
            results[model] = {
                "success": True,
                "response_length": len(response) if response else 0,
                "has_legal_content": "right" in response.lower() if response else False
            }
        else:
            results[model] = {"success": False}
    
    # Find the best model
    working_models = [m for m, r in results.items() if r["success"]]
    
    if not working_models:
        print("❌ No models are working!")
        return None
    
    # Prefer models that give longer, more detailed responses
    best_model = max(working_models, key=lambda m: results[m]["response_length"])
    
    print(f"\n🏆 Best model: {best_model}")
    print(f"Response length: {results[best_model]['response_length']} chars")
    
    return best_model

def create_model_config(best_model):
    """Create configuration to use the best model"""
    print(f"\n🔧 Creating configuration for {best_model}...")
    
    config = f'''
# Ollama Model Configuration
# Generated automatically based on available models

OLLAMA_BEST_MODEL = "{best_model}"
OLLAMA_CHAT_MODEL = "{best_model}"
OLLAMA_LEGAL_MODEL = "{best_model}"
OLLAMA_RESEARCH_MODEL = "{best_model}"

# Model mapping for different tasks
MODEL_TASK_MAPPING = {{
    "chat": "{best_model}",
    "legal_qa": "{best_model}",
    "document_drafting": "{best_model}",
    "legal_research": "{best_model}",
    "default": "{best_model}"
}}

# Disable paid services
OPENAI_ENABLED = False
CLAUDE_ENABLED = False
ANTHROPIC_ENABLED = False

# Enable Ollama
OLLAMA_ENABLED = True
OLLAMA_URL = "http://localhost:11434"
'''
    
    with open("ollama_model_config.py", "w") as f:
        f.write(config)
    
    print("✅ Model configuration created")

def test_chat_api_with_model(model_name):
    """Test the chat API with the specific model"""
    print(f"\n🧪 Testing chat API with {model_name}...")
    
    try:
        response = requests.post(
            "http://localhost:3001/api/v1/ai/chat",
            json={
                "message": "What are my rights as a tenant?",
                "task_type": "chat",
                "model": model_name
            },
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            response_text = data.get('text', data.get('response', ''))
            print(f"✅ Chat API working with {model_name}")
            print(f"Response: {response_text[:200]}...")
            return True
        else:
            print(f"❌ Chat API failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Chat API test failed: {e}")
        return False

def main():
    """Main function"""
    print("🚀 Model Selection Fix")
    print("=" * 40)
    
    # Find the best available model
    best_model = find_best_model()
    
    if not best_model:
        print("\n❌ No working models found!")
        return
    
    # Create configuration
    create_model_config(best_model)
    
    # Test chat API
    chat_working = test_chat_api_with_model(best_model)
    
    print(f"\n📋 Configuration Summary:")
    print(f"✅ Best model: {best_model}")
    print(f"✅ Configuration file: ollama_model_config.py")
    print(f"✅ Chat API: {'Working' if chat_working else 'Needs restart'}")
    
    print(f"\n🎯 To apply changes:")
    print(f"1. The system should now use {best_model}")
    print(f"2. If chat still gives generic responses, restart the backend")
    print(f"3. No OpenAI API key needed!")

if __name__ == "__main__":
    main()
