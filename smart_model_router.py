#!/usr/bin/env python3
"""
SmartProBono Intelligent Model Router
====================================
Automatically selects the best lightweight model based on question complexity
and system resources to prevent freezing.
"""

import requests
import json
import time
import re
from typing import Dict, List, Optional

class SmartModelRouter:
    def __init__(self):
        self.ollama_url = "http://localhost:11434"
        
        # Model configurations with performance characteristics
        self.models = {
            "tinyllama:1.1b": {
                "size_gb": 0.6,
                "speed": "ultra_fast",
                "quality": "basic",
                "best_for": ["simple_questions", "quick_responses", "greetings"],
                "max_tokens": 200,
                "context_window": 512
            },
            "qwen2.5:0.5b": {
                "size_gb": 0.4,
                "speed": "fast",
                "quality": "good",
                "best_for": ["general_legal", "moderate_complexity", "balanced"],
                "max_tokens": 300,
                "context_window": 1024
            },
            "gemma2:2b": {
                "size_gb": 1.5,
                "speed": "moderate",
                "quality": "high",
                "best_for": ["complex_analysis", "detailed_responses", "legal_reasoning"],
                "max_tokens": 500,
                "context_window": 2048
            },
            "llama3.2:3b": {
                "size_gb": 1.9,
                "speed": "slow",
                "quality": "very_high",
                "best_for": ["complex_legal", "detailed_analysis", "comprehensive"],
                "max_tokens": 800,
                "context_window": 4096
            }
        }
        
        # Question complexity patterns
        self.complexity_patterns = {
            "simple": [
                r"\b(hello|hi|hey|thanks|thank you)\b",
                r"\b(what|how|when|where|who)\b.*\?$",
                r"^.{1,50}\?$"  # Short questions
            ],
            "moderate": [
                r"\b(explain|describe|tell me about)\b",
                r"\b(legal|law|rights|contract|agreement)\b",
                r".{50,200}\?$"  # Medium length questions
            ],
            "complex": [
                r"\b(analyze|compare|evaluate|assess)\b",
                r"\b(dispute|litigation|court|lawsuit|settlement)\b",
                r".{200,}\?$"  # Long questions
            ]
        }
    
    def get_system_resources(self) -> Dict:
        """Get current system resource usage (simplified version)"""
        # Simplified version - assume normal load for now
        return {
            "cpu_percent": 30,  # Assume normal CPU usage
            "memory_percent": 50,  # Assume normal memory usage
            "memory_available_gb": 4,  # Assume 4GB available
            "is_high_load": False  # Assume normal load
        }
    
    def analyze_question_complexity(self, question: str) -> str:
        """Analyze question complexity based on patterns"""
        question_lower = question.lower()
        
        # Check for complex patterns first
        for pattern in self.complexity_patterns["complex"]:
            if re.search(pattern, question_lower):
                return "complex"
        
        # Check for moderate patterns
        for pattern in self.complexity_patterns["moderate"]:
            if re.search(pattern, question_lower):
                return "moderate"
        
        # Check for simple patterns
        for pattern in self.complexity_patterns["simple"]:
            if re.search(pattern, question_lower):
                return "simple"
        
        # Default based on length
        if len(question) < 50:
            return "simple"
        elif len(question) < 200:
            return "moderate"
        else:
            return "complex"
    
    def select_optimal_model(self, question: str, user_preference: str = None) -> Dict:
        """Select the optimal model based on question complexity and system resources"""
        complexity = self.analyze_question_complexity(question)
        resources = self.get_system_resources()
        
        print(f"🔍 Question complexity: {complexity}")
        print(f"💻 System resources: CPU {resources['cpu_percent']:.1f}%, RAM {resources['memory_percent']:.1f}%")
        
        # If user has a preference and system can handle it
        if user_preference and user_preference in self.models:
            model_config = self.models[user_preference]
            if not resources['is_high_load'] or model_config['size_gb'] < 1.0:
                return {
                    "model": user_preference,
                    "reason": f"User preference with {complexity} complexity",
                    "config": model_config
                }
        
        # Auto-select based on complexity and resources
        if resources['is_high_load']:
            # High system load - use smallest models
            if complexity == "simple":
                return {
                    "model": "tinyllama:1.1b",
                    "reason": "High system load, simple question - using ultra-lightweight model",
                    "config": self.models["tinyllama:1.1b"]
                }
            else:
                return {
                    "model": "qwen2.5:0.5b",
                    "reason": "High system load - using lightweight model",
                    "config": self.models["qwen2.5:0.5b"]
                }
        
        # Normal system load - select based on complexity
        if complexity == "simple":
            return {
                "model": "tinyllama:1.1b",
                "reason": "Simple question - using ultra-fast model",
                "config": self.models["tinyllama:1.1b"]
            }
        elif complexity == "moderate":
            return {
                "model": "qwen2.5:0.5b",
                "reason": "Moderate complexity - using balanced model",
                "config": self.models["qwen2.5:0.5b"]
            }
        else:  # complex
            if resources['memory_available_gb'] > 2.0:
                return {
                    "model": "gemma2:2b",
                    "reason": "Complex question with sufficient resources - using high-quality model",
                    "config": self.models["gemma2:2b"]
                }
            else:
                return {
                    "model": "qwen2.5:0.5b",
                    "reason": "Complex question but limited resources - using lightweight model",
                    "config": self.models["qwen2.5:0.5b"]
                }
    
    def generate_response(self, question: str, user_preference: str = None) -> Dict:
        """Generate response using the optimal model"""
        selection = self.select_optimal_model(question, user_preference)
        model = selection["model"]
        config = selection["config"]
        
        print(f"🤖 Selected model: {model}")
        print(f"📝 Reason: {selection['reason']}")
        
        # Prepare optimized payload
        payload = {
            "model": model,
            "prompt": question,
            "stream": False,
            "options": {
                "temperature": 0.7,
                "top_p": 0.9,
                "num_predict": config["max_tokens"],
                "num_ctx": config["context_window"],
                "num_thread": 1,  # Single thread for stability
                "num_gpu": 0,     # Force CPU usage
                "low_vram": True  # Optimize for low memory
            }
        }
        
        start_time = time.time()
        try:
            response = requests.post(f"{self.ollama_url}/api/generate", 
                                   json=payload, timeout=20)
            
            if response.status_code == 200:
                result = response.json()
                response_time = time.time() - start_time
                
                return {
                    "success": True,
                    "model_used": model,
                    "response": result.get('response', ''),
                    "response_time": response_time,
                    "selection_reason": selection["reason"],
                    "model_config": config
                }
            else:
                return {
                    "success": False,
                    "error": f"HTTP {response.status_code}",
                    "model_used": model
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "model_used": model
            }

def test_router():
    """Test the smart model router with different question types"""
    router = SmartModelRouter()
    
    test_questions = [
        "Hello, how are you?",  # Simple
        "What are my rights as a tenant?",  # Moderate
        "I have a complex landlord dispute involving multiple lease violations and need detailed legal analysis of my options for resolution.",  # Complex
        "Thanks for your help!",  # Simple
        "Can you explain the difference between civil and criminal law?",  # Moderate
    ]
    
    print("🧪 Testing Smart Model Router")
    print("=" * 40)
    
    for i, question in enumerate(test_questions, 1):
        print(f"\n📝 Test {i}: {question[:50]}...")
        result = router.generate_response(question)
        
        if result["success"]:
            print(f"✅ Success: {result['model_used']} ({result['response_time']:.2f}s)")
            print(f"📝 Response: {result['response'][:100]}...")
        else:
            print(f"❌ Failed: {result['error']}")

if __name__ == "__main__":
    test_router()
