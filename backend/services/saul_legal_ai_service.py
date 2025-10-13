"""
Saul Legal AI Service - Integration with Equall/Saul-7B-Instruct-v1
A specialized legal language model service for SmartProBono
"""

import logging
import torch
from datetime import datetime
from typing import Dict, List, Optional, Any
import warnings
import sys
import os

# Suppress warnings for cleaner output
warnings.filterwarnings("ignore")

# Add path for config service
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

try:
    from services.model_config_service import model_config_service
    CONFIG_AVAILABLE = True
except ImportError:
    CONFIG_AVAILABLE = False

logger = logging.getLogger(__name__)

class SaulLegalAIService:
    """Saul Legal AI Service using Equall/Saul-7B-Instruct-v1 model"""
    
    def __init__(self):
        # Use smaller legal model for faster CPU inference
        self.model_name = "isaacus/open-australian-legal-gpt2"  # Small legal model (124M parameters)
        self.fallback_model = "Equall/Saul-7B-Instruct-v1"  # Keep Saul as fallback
        self.tokenizer = None
        self.model = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.is_loaded = False
        self.using_fallback = False
        
        logger.info(f"Saul Legal AI Service initialized - Device: {self.device}")
        logger.info(f"Primary model: {self.model_name} (small, fast)")
        logger.info(f"Fallback model: {self.fallback_model} (large, slow)")
    
    def _load_model(self):
        """Load the legal model and tokenizer"""
        if self.is_loaded:
            return
            
        try:
            # Try small model first
            logger.info(f"Loading legal model: {self.model_name}...")
            
            # Import transformers
            from transformers import AutoTokenizer, AutoModelForCausalLM
            
            # Load tokenizer and model
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            
            # Add padding token if not present
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
            
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_name,
                torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
                device_map="auto" if self.device == "cuda" else None,
                trust_remote_code=True
            )
            
            # Move to device if not using device_map
            if self.device != "cuda" or not torch.cuda.is_available():
                self.model = self.model.to(self.device)
            
            self.is_loaded = True
            self.using_fallback = False
            logger.info(f"Legal model loaded successfully on {self.device}")
            
        except Exception as e:
            logger.error(f"Failed to load primary model: {str(e)}")
            logger.info("Trying fallback Saul model...")
            
            try:
                # Fallback to Saul model
                self.model_name = self.fallback_model
                self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
                self.model = AutoModelForCausalLM.from_pretrained(
                    self.model_name,
                    torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
                    device_map="auto" if self.device == "cuda" else None,
                    trust_remote_code=True
                )
                
                if self.device != "cuda" or not torch.cuda.is_available():
                    self.model = self.model.to(self.device)
                
                self.is_loaded = True
                self.using_fallback = True
                logger.info(f"Saul fallback model loaded successfully on {self.device}")
                
            except Exception as fallback_error:
                logger.error(f"Failed to load fallback model: {str(fallback_error)}")
                self.is_loaded = False
                raise fallback_error
    
    def generate_response(self, message: str, task_type: str = "chat", **kwargs) -> Dict[str, Any]:
        """Generate response using Saul legal model"""
        try:
            # Load model if not already loaded
            if not self.is_loaded:
                self._load_model()
            
            # Prepare input for smaller model (GPT-2 style)
            if self.using_fallback:
                # Use chat template for Saul model
                messages = [{"role": "user", "content": message}]
                inputs = self.tokenizer.apply_chat_template(
                    messages,
                    add_generation_prompt=True,
                    tokenize=True,
                    return_dict=True,
                    return_tensors="pt",
                ).to(self.model.device)
            else:
                # Use simple prompt for GPT-2 style model
                prompt = f"Legal Question: {message}\nLegal Answer:"
                inputs = self.tokenizer(
                    prompt,
                    return_tensors="pt",
                    truncation=True,
                    max_length=512
                ).to(self.model.device)
            
            # Get generation parameters from config or kwargs
            if CONFIG_AVAILABLE:
                gen_params = model_config_service.get_generation_params(task_type, **kwargs)
            else:
                gen_params = {
                    'max_tokens': kwargs.get('max_tokens', 100),
                    'temperature': kwargs.get('temperature', 0.7),
                    'top_p': kwargs.get('top_p', 0.9),
                    'repetition_penalty': kwargs.get('repetition_penalty', 1.2)
                }
            
            # Generate response
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_new_tokens=gen_params.get('max_tokens', 100),
                    temperature=gen_params.get('temperature', 0.7),
                    top_p=gen_params.get('top_p', 0.9),
                    repetition_penalty=gen_params.get('repetition_penalty', 1.2),
                    do_sample=True,
                    pad_token_id=self.tokenizer.pad_token_id,
                    eos_token_id=self.tokenizer.eos_token_id,
                    no_repeat_ngram_size=gen_params.get('no_repeat_ngram_size', 2)
                )
            
            # Decode response
            if self.using_fallback:
                response_text = self.tokenizer.decode(
                    outputs[0][inputs["input_ids"].shape[-1]:], 
                    skip_special_tokens=True
                ).strip()
            else:
                response_text = self.tokenizer.decode(
                    outputs[0][inputs["input_ids"].shape[-1]:], 
                    skip_special_tokens=True
                ).strip()
            
            # Add legal disclaimer if not present
            if "legal advice" not in response_text.lower() and "attorney" not in response_text.lower():
                response_text += "\n\n*Note: This is general legal information, not legal advice. Please consult with a qualified attorney for specific legal matters.*"
            
            return {
                "id": f"saul_{hash(message) % 10000}_{int(datetime.now().timestamp())}",
                "created_at": datetime.now().isoformat(),
                "model": self.model_name,
                "task_type": task_type,
                "text": response_text,
                "success": True,
                "conversation_id": kwargs.get('conversation_id'),
                "user_id": kwargs.get('user_id'),
                "device": self.device
            }
            
        except Exception as e:
            logger.error(f"Error generating Saul response: {str(e)}")
            return self._get_fallback_response(message, task_type, **kwargs)
    
    def _get_fallback_response(self, message: str, task_type: str, **kwargs) -> Dict[str, Any]:
        """Get fallback response when Saul model fails"""
        fallback_text = f"""I understand you're asking about '{message}'. 

While our specialized legal AI model (Saul) is currently experiencing technical difficulties, I can still provide some general guidance:

For your legal question, I recommend:
1. **Consulting with a qualified attorney** - This is always the best option for specific legal matters
2. **Contacting your local legal aid organization** - They provide free or low-cost legal assistance
3. **Checking your state's legal resources website** - Many states offer self-help legal resources
4. **Visiting your local law library** - Public law libraries often have helpful resources

*Important: This is general information only, not legal advice. For specific legal matters, please consult with a licensed attorney.*

I apologize for the technical difficulty and encourage you to try again in a few moments."""
        
        return {
            "id": f"saul_fallback_{hash(message) % 10000}_{int(datetime.now().timestamp())}",
            "created_at": datetime.now().isoformat(),
            "model": f"{self.model_name}_fallback",
            "task_type": task_type,
            "text": fallback_text,
            "success": False,
            "conversation_id": kwargs.get('conversation_id'),
            "user_id": kwargs.get('user_id'),
            "error": "Model temporarily unavailable"
        }
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the legal model"""
        if self.using_fallback:
            return {
                "model_name": self.model_name,
                "model_type": "Legal Language Model",
                "base_model": "Mistral-7B",
                "specialization": "Legal Domain",
                "device": self.device,
                "is_loaded": self.is_loaded,
                "using_fallback": True,
                "description": "Saul-7B-Instruct-v1 is a specialized legal language model trained on legal text comprehension and generation",
                "paper": "https://arxiv.org/abs/2403.03883",
                "huggingface_url": "https://huggingface.co/Equall/Saul-7B-Instruct-v1",
                "company": "Equall",
                "website": "https://equall.com/"
            }
        else:
            return {
                "model_name": self.model_name,
                "model_type": "Legal Language Model",
                "base_model": "GPT-2",
                "specialization": "Legal Domain (Australian Law)",
                "device": self.device,
                "is_loaded": self.is_loaded,
                "using_fallback": False,
                "description": "Open Australian Legal GPT-2 is a smaller legal language model trained on Australian legal text",
                "huggingface_url": "https://huggingface.co/isaacus/open-australian-legal-gpt2",
                "company": "Open Source",
                "website": "https://huggingface.co/isaacus/open-australian-legal-gpt2"
            }
    
    def health_check(self) -> Dict[str, Any]:
        """Check the health status of the Saul model service"""
        try:
            if self.is_loaded:
                # Try a simple generation to test functionality
                test_response = self.generate_response("Hello", "test", max_tokens=10)
                return {
                    "status": "healthy",
                    "model_loaded": True,
                    "device": self.device,
                    "test_response": test_response.get("success", False),
                    "timestamp": datetime.now().isoformat()
                }
            else:
                return {
                    "status": "not_loaded",
                    "model_loaded": False,
                    "device": self.device,
                    "timestamp": datetime.now().isoformat()
                }
        except Exception as e:
            return {
                "status": "error",
                "model_loaded": False,
                "device": self.device,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }

# Global instance
saul_legal_ai = SaulLegalAIService()
