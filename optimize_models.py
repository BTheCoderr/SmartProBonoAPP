#!/usr/bin/env python3
"""
SmartProBono Model Optimization Script
=====================================
This script helps optimize models for better performance and reduced resource usage.
"""

import requests
import json
import time
import subprocess
import os

class ModelOptimizer:
    def __init__(self):
        self.ollama_url = "http://localhost:11434"
        
    def get_available_models(self):
        """Get list of available models"""
        try:
            response = requests.get(f"{self.ollama_url}/api/tags")
            return response.json().get('models', [])
        except Exception as e:
            print(f"❌ Error getting models: {e}")
            return []
    
    def test_model_performance(self, model_name, test_prompt="Hello, can you help with a legal question?"):
        """Test model performance and resource usage"""
        print(f"🧪 Testing {model_name}...")
        
        start_time = time.time()
        try:
            payload = {
                "model": model_name,
                "prompt": test_prompt,
                "stream": False,
                "options": {
                    "num_predict": 100,
                    "num_ctx": 512,
                    "num_thread": 1,
                    "temperature": 0.7
                }
            }
            
            response = requests.post(f"{self.ollama_url}/api/generate", 
                                   json=payload, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                response_time = time.time() - start_time
                
                return {
                    "model": model_name,
                    "response_time": response_time,
                    "response_length": len(result.get('response', '')),
                    "success": True,
                    "response": result.get('response', '')[:100] + "..." if len(result.get('response', '')) > 100 else result.get('response', '')
                }
            else:
                return {"model": model_name, "success": False, "error": f"HTTP {response.status_code}"}
                
        except Exception as e:
            return {"model": model_name, "success": False, "error": str(e)}
    
    def create_quantized_model(self, base_model, quantized_name):
        """Create a quantized version of a model"""
        print(f"🔧 Creating quantized model: {quantized_name}")
        
        # This would require Ollama's modelfile functionality
        # For now, we'll create a configuration file
        modelfile_content = f"""
FROM {base_model}

# Quantization settings for reduced memory usage
PARAMETER num_ctx 1024
PARAMETER num_predict 300
PARAMETER temperature 0.7
PARAMETER top_p 0.9
PARAMETER num_thread 1
PARAMETER num_gpu 0
PARAMETER low_vram true

# System prompt for legal assistance
SYSTEM You are a helpful legal assistant. Provide concise, accurate legal guidance.
"""
        
        with open(f"{quantized_name}.Modelfile", "w") as f:
            f.write(modelfile_content)
        
        print(f"✅ Created Modelfile for {quantized_name}")
        print(f"📝 To create the model, run: ollama create {quantized_name} -f {quantized_name}.Modelfile")
        
        return True
    
    def create_model_ensemble_config(self):
        """Create a lightweight model ensemble configuration"""
        ensemble_config = {
            "ensemble_name": "smartprobono-lightweight",
            "models": [
                {
                    "name": "qwen2.5:0.5b",
                    "role": "primary",
                    "weight": 0.6,
                    "use_for": ["general_legal", "quick_responses"]
                },
                {
                    "name": "tinyllama:1.1b", 
                    "role": "fallback",
                    "weight": 0.3,
                    "use_for": ["simple_questions", "fast_responses"]
                },
                {
                    "name": "gemma2:2b",
                    "role": "specialized",
                    "weight": 0.1,
                    "use_for": ["complex_analysis", "detailed_responses"]
                }
            ],
            "routing_rules": {
                "simple_questions": ["tinyllama:1.1b", "qwen2.5:0.5b"],
                "legal_analysis": ["qwen2.5:0.5b", "gemma2:2b"],
                "quick_responses": ["tinyllama:1.1b"],
                "detailed_advice": ["gemma2:2b", "qwen2.5:0.5b"]
            }
        }
        
        with open("model_ensemble_config.json", "w") as f:
            json.dump(ensemble_config, f, indent=2)
        
        print("✅ Created model ensemble configuration")
        return ensemble_config
    
    def benchmark_models(self):
        """Benchmark all lightweight models"""
        print("🏁 Benchmarking Lightweight Models")
        print("=" * 40)
        
        models = self.get_available_models()
        lightweight_models = [m for m in models if m.get('size', 0) < 2 * (1024**3)]  # < 2GB
        
        results = []
        for model in lightweight_models:
            model_name = model.get('name', '')
            size_gb = model.get('size', 0) / (1024**3)
            
            print(f"\n📊 Testing {model_name} ({size_gb:.1f} GB)")
            result = self.test_model_performance(model_name)
            result['size_gb'] = size_gb
            results.append(result)
            
            if result['success']:
                print(f"   ✅ Response time: {result['response_time']:.2f}s")
                print(f"   📝 Response: {result['response']}")
            else:
                print(f"   ❌ Failed: {result.get('error', 'Unknown error')}")
        
        # Sort by performance
        successful_results = [r for r in results if r['success']]
        successful_results.sort(key=lambda x: x['response_time'])
        
        print(f"\n🏆 Performance Ranking:")
        print("=" * 30)
        for i, result in enumerate(successful_results, 1):
            print(f"{i}. {result['model']} - {result['response_time']:.2f}s ({result['size_gb']:.1f} GB)")
        
        return results

def main():
    optimizer = ModelOptimizer()
    
    print("🚀 SmartProBono Model Optimization")
    print("=" * 40)
    
    # Benchmark current models
    results = optimizer.benchmark_models()
    
    # Create ensemble configuration
    ensemble_config = optimizer.create_model_ensemble_config()
    
    # Create quantized model configurations
    print(f"\n🔧 Creating Quantized Model Configurations:")
    print("=" * 45)
    
    quantized_models = [
        ("qwen2.5:0.5b", "qwen2.5-legal-optimized"),
        ("tinyllama:1.1b", "tinyllama-legal-optimized"),
        ("gemma2:2b", "gemma2-legal-optimized")
    ]
    
    for base_model, quantized_name in quantized_models:
        optimizer.create_quantized_model(base_model, quantized_name)
    
    print(f"\n💡 Optimization Recommendations:")
    print("=" * 35)
    print("1. Use Qwen 2.5 (0.5B) as primary model - fastest and smallest")
    print("2. Use TinyLlama (1.1B) for ultra-fast responses")
    print("3. Use Gemma 2B for complex legal analysis")
    print("4. Implement model routing based on question complexity")
    print("5. Consider quantizing models for even smaller memory footprint")
    print("6. Use CPU-only mode to prevent GPU memory issues")

if __name__ == "__main__":
    main()

