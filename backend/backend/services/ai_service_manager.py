from enum import Enum
import os
from dotenv import load_dotenv
import requests
import aiohttp
import asyncio
from typing import Optional, Dict, Any, List
from config.ai_config import AI_CONFIG, PROMPT_TEMPLATES
from services.performance_monitor import performance_monitor

load_dotenv()

class AIProvider(Enum):
    MISTRAL = "mistral"
    LLAMA = "llama"
    FALCON = "falcon"
    DEEPSEEK = "deepseek"
    OPENAI = "openai"

class AIServiceManager:
    def __init__(self):
        self.config = AI_CONFIG
        self.huggingface_api_key = self.config['api_keys']['huggingface']
        self.huggingface_endpoint = self.config['endpoints']['huggingface']
        self._session = None

    async def _ensure_session(self):
        if self._session is None:
            self._session = aiohttp.ClientSession()
        return self._session

    def get_best_provider(self, task_type: str) -> AIProvider:
        """
        Determine the best AI provider based on task type and model specialization
        """
        model_name = self.config['task_routing'].get(task_type, 'mistral')  # Default to Mistral instead of OpenAI
        return AIProvider(model_name)

    def get_prompt_template(self, model: str, task_type: str) -> str:
        """
        Get the appropriate prompt template for the model and task
        """
        if model in PROMPT_TEMPLATES and task_type in PROMPT_TEMPLATES[model]:
            return PROMPT_TEMPLATES[model][task_type]
        return "{prompt}"  # Default template if none found

    async def get_response(self, 
                          prompt: str, 
                          provider: AIProvider, 
                          task_type: str,
                          max_retries: int = 2) -> Dict[str, Any]:
        """
        Get response from specified AI provider with performance monitoring
        """
        start_time = performance_monitor.start_request()
        
        # Order of models to try (free models first, then OpenAI as last resort)
        model_order = [
            AIProvider.MISTRAL,
            AIProvider.LLAMA,
            AIProvider.FALCON,
            AIProvider.DEEPSEEK,
            AIProvider.OPENAI
        ]

        # If a specific provider was requested and it's not OpenAI, try it first
        if provider != AIProvider.OPENAI:
            model_order.remove(provider)
            model_order.insert(0, provider)

        last_error = None
        tried_providers = []
        
        for current_provider in model_order:
            try:
                model_config = self.config['models'][current_provider.value]
                formatted_prompt = self.get_prompt_template(current_provider.value, task_type).format(prompt=prompt)

                # Try to get response from current provider
                if current_provider == AIProvider.OPENAI:
                    response = await self._get_openai_response(formatted_prompt, model_config)
                else:
                    response = await self._get_model_response(formatted_prompt, model_config, current_provider.value)

                if response:
                    # Log successful response
                    performance_monitor.log_request(
                        model=current_provider.value,
                        task_type=task_type,
                        start_time=start_time,
                        response=response['text'],
                        metadata={
                            'tokens': response.get('tokens', 0),
                            'model_name': model_config['name'],
                            'success': True
                        }
                    )

                    return {
                        'text': response['text'],
                        'model': model_config['name'],
                        'tokens': response.get('tokens', 0),
                        'provider': current_provider.value
                    }

            except Exception as e:
                error_msg = str(e)
                print(f"{current_provider.value} error: {error_msg}")
                tried_providers.append(f"{current_provider.value}: {error_msg}")
                last_error = error_msg
                continue

        # If we get here, all providers failed
        error_msg = "All providers failed. Attempts:\n" + "\n".join(tried_providers)
        performance_monitor.log_request(
            model="all",
            task_type=task_type,
            start_time=start_time,
            error=error_msg
        )
        raise Exception(error_msg)

    async def _get_model_response(self, prompt: str, config: Dict, provider: str) -> Dict[str, Any]:
        """Implementation for Hugging Face models"""
        session = await self._ensure_session()
        headers = {"Authorization": f"Bearer {self.huggingface_api_key}"}
        api_url = f"{self.huggingface_endpoint}/{config['huggingface_model']}"
        
        try:
            async with session.post(api_url, headers=headers, json={"inputs": prompt}, timeout=30) as response:
                if response.status == 200:
                    data = await response.json()
                    generated_text = data[0]["generated_text"]
                    
                    # Validate response quality
                    if not self._is_valid_response(generated_text, prompt):
                        raise Exception("Generated response failed quality check")
                    
                    return {
                        'text': generated_text,
                        'tokens': len(generated_text.split())
                    }
                elif response.status == 503:
                    raise Exception("Model is currently unavailable")
                else:
                    raise Exception(f"{provider} API error: Status {response.status}")
        except asyncio.TimeoutError:
            raise Exception(f"{provider} API timeout")
        except Exception as e:
            raise Exception(f"{provider} API error: {str(e)}")

    def _is_valid_response(self, response: str, prompt: str) -> bool:
        """
        Validate the quality of the generated response
        """
        if not response or len(response.strip()) < 10:
            return False
            
        # Check if response is too long (likely hallucination)
        if len(response.split()) > 1000:
            return False
            
        # Check for coherence (basic heuristics)
        sentences = response.split('.')
        if len(sentences) < 2:  # Too short to be meaningful
            return False
            
        # Check if response contains too many repeated words or phrases
        words = response.lower().split()
        word_freq = {}
        for word in words:
            word_freq[word] = word_freq.get(word, 0) + 1
            if word_freq[word] > 5:  # Word appears too many times
                return False
                
        # Check if response is relevant to the prompt
        prompt_keywords = set(prompt.lower().split())
        response_keywords = set(response.lower().split())
        common_keywords = prompt_keywords.intersection(response_keywords)
        if len(common_keywords) < 2:  # Not enough relevance to prompt
            return False
            
        return True

    async def _get_openai_response(self, prompt: str, config: Dict) -> Dict[str, Any]:
        """Implementation for OpenAI models"""
        import openai
        client = openai.AsyncOpenAI(api_key=self.config['api_keys']['openai'])
        
        try:
            response = await client.chat.completions.create(
                model=config['model'],
                messages=[
                    {"role": "system", "content": "You are a helpful legal assistant."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=config['max_tokens'],
                temperature=config['temperature']
            )
            
            # Get token count safely
            token_count = 0
            if hasattr(response, 'usage') and response.usage and hasattr(response.usage, 'total_tokens'):
                token_count = response.usage.total_tokens
            
            return {
                'text': response.choices[0].message.content,
                'tokens': token_count,
                'model': config['model'],
                'provider': 'openai'
            }
        except Exception as e:
            raise Exception(f"OpenAI API error: {str(e)}")

    async def cleanup(self):
        """Cleanup resources"""
        if self._session:
            await self._session.close()
            self._session = None

# Create a singleton instance
ai_service_manager = AIServiceManager() 