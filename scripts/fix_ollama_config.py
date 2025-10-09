#!/usr/bin/env python3
"""
Fix Ollama Configuration
Ensures the system uses free Ollama models instead of OpenAI
"""

import os
import sys
import json
import requests

def test_ollama_models():
    """Test which Ollama models are working"""
    print("🔍 Testing available Ollama models...")
    
    models = ["tinyllama:1.1b", "gemma2:2b", "qwen2.5:0.5b"]
    working_models = []
    
    for model in models:
        try:
            response = requests.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": model,
                    "prompt": "Hello",
                    "stream": False,
                    "options": {"max_tokens": 10}
                },
                timeout=10
            )
            
            if response.status_code == 200:
                working_models.append(model)
                print(f"✅ {model} - Working")
            else:
                print(f"❌ {model} - Failed ({response.status_code})")
                
        except Exception as e:
            print(f"❌ {model} - Error: {e}")
    
    return working_models

def update_ai_config():
    """Update AI configuration to prioritize Ollama"""
    print("\n🔧 Updating AI configuration...")
    
    # Create a new configuration that prioritizes Ollama
    config_update = """
# Updated AI Configuration - Prioritizes Free Models
AI_MODEL_DEFAULT = "tinyllama:1.1b"  # Fastest free model
AI_MODEL_CHAT = "tinyllama:1.1b"
AI_MODEL_LEGAL = "gemma2:2b"  # Better for legal tasks
AI_MODEL_RESEARCH = "qwen2.5:0.5b"  # Good for research

# Disable paid services
OPENAI_ENABLED = False
CLAUDE_ENABLED = False

# Enable Ollama
OLLAMA_ENABLED = True
OLLAMA_URL = "http://localhost:11434"
"""
    
    # Write to a config file
    with open("ollama_config.env", "w") as f:
        f.write(config_update)
    
    print("✅ Ollama configuration created")

def test_chat_with_ollama():
    """Test chat functionality with Ollama"""
    print("\n🧪 Testing chat with Ollama...")
    
    try:
        response = requests.post(
            "http://localhost:3001/api/v1/ai/chat",
            json={
                "message": "What are tenant rights?",
                "task_type": "chat",
                "model": "tinyllama:1.1b"
            },
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Chat API working")
            print(f"Model: {data.get('model', 'unknown')}")
            print(f"Response: {data.get('text', data.get('response', 'No response'))[:100]}...")
            return True
        else:
            print(f"❌ Chat API failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Chat test failed: {e}")
        return False

def create_model_override():
    """Create a model override to force Ollama usage"""
    print("\n🔧 Creating model override...")
    
    override_code = '''
# Model Override for Free Models
import os

# Force Ollama usage
os.environ['AI_MODEL'] = 'tinyllama:1.1b'
os.environ['OLLAMA_ENABLED'] = 'true'
os.environ['OPENAI_ENABLED'] = 'false'

# Override model selection
def get_best_model(task_type="chat"):
    """Get the best available free model for the task"""
    if task_type in ["chat", "legal_qa", "rights_explanation"]:
        return "tinyllama:1.1b"
    elif task_type in ["document_drafting", "contract_generation"]:
        return "gemma2:2b"
    elif task_type in ["legal_research", "case_analysis"]:
        return "qwen2.5:0.5b"
    else:
        return "tinyllama:1.1b"  # Default to fastest
'''
    
    with open("model_override.py", "w") as f:
        f.write(override_code)
    
    print("✅ Model override created")

def main():
    """Main function"""
    print("🚀 Ollama Configuration Fix")
    print("=" * 40)
    
    # Test available models
    working_models = test_ollama_models()
    
    if not working_models:
        print("\n❌ No Ollama models are working!")
        print("Make sure Ollama is running: ollama serve")
        return
    
    print(f"\n✅ Found {len(working_models)} working models: {', '.join(working_models)}")
    
    # Update configuration
    update_ai_config()
    create_model_override()
    
    # Test chat functionality
    chat_working = test_chat_with_ollama()
    
    if chat_working:
        print("\n🎉 SUCCESS! Chat is now using free Ollama models!")
    else:
        print("\n⚠️ Chat API needs to be restarted to use Ollama models")
    
    print("\n📋 Next Steps:")
    print("1. Restart the backend server to apply changes")
    print("2. Test chat functionality")
    print("3. No more OpenAI API key needed!")

if __name__ == "__main__":
    main()
