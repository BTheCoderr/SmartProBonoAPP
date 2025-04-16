from enum import Enum
import os
from dotenv import load_dotenv
import requests
import aiohttp
import asyncio
import re
import json
from typing import Optional, Dict, Any, List, Tuple
from config.ai_config import AI_CONFIG, PROMPT_TEMPLATES
from services.performance_monitor import performance_monitor
from datetime import datetime

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
        
        # Legal citation patterns for extraction
        self.citation_patterns = {
            'case_law': r'([A-Z][a-z]+\s+v\.\s+[A-Z][a-z]+),\s+(\d+)\s+([A-Z]\.[A-Z]\.[a-z]+\.?)\s+(\d+)\s+\((\d{4})\)',
            'statute': r'(\d+)\s+([A-Z]\.[A-Z]\.[A-Z]\.[A-Z]\.?)\s+§\s+(\d+[a-z]?)',
            'regulation': r'(\d+)\s+C\.F\.R\.\s+§\s+(\d+\.\d+)',
            'constitution': r'([A-Z]\.[A-Z]\.\s+[A-Za-z]+\.?)\s+([IVX]+),\s+§\s+(\d+)'
        }
        
        # Jurisdictions for metadata
        self.jurisdictions = [
            "Federal", "Alabama", "Alaska", "Arizona", "Arkansas", "California", 
            "Colorado", "Connecticut", "Delaware", "Florida", "Georgia", "Hawaii", 
            "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", 
            "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi", 
            "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey", 
            "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio", "Oklahoma", 
            "Oregon", "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota", 
            "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington", 
            "West Virginia", "Wisconsin", "Wyoming", "District of Columbia"
        ]

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
        # First, check the task_to_prompt mapping to determine which prompt template to use
        prompt_type = self.config.get('task_to_prompt', {}).get(task_type, task_type)
        
        # Then check if the model has that prompt template
        if model in PROMPT_TEMPLATES and prompt_type in PROMPT_TEMPLATES[model]:
            return PROMPT_TEMPLATES[model][prompt_type]
        elif model in PROMPT_TEMPLATES and task_type in PROMPT_TEMPLATES[model]:
            # Fallback to direct task type if prompt_type not found
            return PROMPT_TEMPLATES[model][task_type]
        
        # Default template if none found
        return "{prompt}"

    def extract_citations(self, text: str) -> List[Dict[str, Any]]:
        """
        Extract legal citations from text and structure them
        """
        citations = []
        
        # Process for each pattern type
        for citation_type, pattern in self.citation_patterns.items():
            matches = re.finditer(pattern, text)
            
            for match in matches:
                if citation_type == 'case_law':
                    # Example: Smith v. Jones, 123 U.S. 456 (1990)
                    citation = {
                        'type': 'Case Law',
                        'text': match.group(0),
                        'case_name': match.group(1),
                        'volume': match.group(2),
                        'reporter': match.group(3),
                        'page': match.group(4),
                        'year': match.group(5),
                        'url': f"https://caselaw.findlaw.com/search?query={match.group(1).replace(' ', '+')}"
                    }
                
                elif citation_type == 'statute':
                    # Example: 42 U.S.C. § 1983
                    citation = {
                        'type': 'Statute',
                        'text': match.group(0),
                        'title': match.group(1),
                        'code': match.group(2),
                        'section': match.group(3),
                        'year': None,
                        'url': f"https://www.law.cornell.edu/uscode/text/{match.group(1)}/{match.group(3)}"
                    }
                
                elif citation_type == 'regulation':
                    # Example: 24 C.F.R. § 100.204
                    citation = {
                        'type': 'Regulation',
                        'text': match.group(0),
                        'title': match.group(1),
                        'section': match.group(2),
                        'year': None,
                        'url': f"https://www.ecfr.gov/current/title-{match.group(1)}/part-{match.group(2).split('.')[0]}/section-{match.group(2)}"
                    }
                
                elif citation_type == 'constitution':
                    # Example: U.S. Const. art. I, § 8
                    citation = {
                        'type': 'Constitution',
                        'text': match.group(0),
                        'constitution': match.group(1),
                        'article': match.group(2),
                        'section': match.group(3),
                        'year': None,
                        'url': f"https://constitution.congress.gov/browse/article-{self._roman_to_int(match.group(2))}/section-{match.group(3)}/"
                    }
                
                citations.append(citation)
        
        return citations

    def _roman_to_int(self, roman: str) -> int:
        """Convert Roman numeral to integer"""
        values = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
        result = 0
        for i in range(len(roman)):
            if i > 0 and values[roman[i]] > values[roman[i-1]]:
                result += values[roman[i]] - 2 * values[roman[i-1]]
            else:
                result += values[roman[i]]
        return result

    def detect_jurisdictions(self, text: str) -> List[str]:
        """
        Detect jurisdictions mentioned in the text
        """
        found_jurisdictions = []
        
        for jurisdiction in self.jurisdictions:
            # Check for exact mentions or possessive form
            if re.search(rf'\b{jurisdiction}\b|\b{jurisdiction}\'s\b', text, re.IGNORECASE):
                found_jurisdictions.append(jurisdiction)
        
        return found_jurisdictions

    def calculate_confidence_score(
        self, 
        response: str, 
        provider: AIProvider,
        task_type: str,
        citations: List[Dict[str, Any]],
        token_count: int
    ) -> Dict[str, Any]:
        """
        Calculate confidence score based on multiple factors:
        - Number and quality of citations
        - Model expertise for the task type
        - Response coherence and structure
        - Token length and information density
        """
        base_score = 50  # Start with a neutral score
        score_factors = {}
        
        # 1. Factor: Model-task alignment (0-20 points)
        model_config = self.config['models'][provider.value]
        model_specializations = model_config.get('specialization', [])
        
        if task_type in model_specializations:
            alignment_score = 20  # Perfect alignment
        elif any(spec for spec in model_specializations if spec in task_type):
            alignment_score = 15  # Partial alignment
        else:
            alignment_score = 5  # No alignment
            
        score_factors['model_alignment'] = alignment_score
        
        # 2. Factor: Citations (0-25 points)
        citation_score = min(len(citations) * 5, 25)  # 5 points per citation, max 25
        score_factors['citations'] = citation_score
        
        # 3. Factor: Response structure (0-15 points)
        structure_score = 0
        
        # Check for section headers
        if re.search(r'^#+\s+.+|^[A-Z][A-Za-z\s]+:|\d+\.\s+[A-Z]', response, re.MULTILINE):
            structure_score += 5
        
        # Check for organized paragraphs
        if len(re.findall(r'\n\n', response)) >= 2:
            structure_score += 5
        
        # Check for conclusion or summary
        if re.search(r'(In\s+conclusion|Summary|To\s+summarize|Therefore)', response):
            structure_score += 5
            
        score_factors['structure'] = structure_score
        
        # 4. Factor: Information density (0-20 points)
        # Reward information-rich but concise responses
        words = len(response.split())
        unique_words = len(set(response.lower().split()))
        
        if words > 0:
            uniqueness_ratio = unique_words / words
            # Higher ratio = more unique words = higher information density
            density_score = min(int(uniqueness_ratio * 40), 20)
        else:
            density_score = 0
            
        score_factors['information_density'] = density_score
        
        # 5. Factor: Legal terminology (0-20 points)
        legal_terms = [
            'statute', 'regulation', 'precedent', 'provision', 'jurisdiction',
            'plaintiff', 'defendant', 'petitioner', 'respondent', 'appellant',
            'legislation', 'jurisprudence', 'litigation', 'adjudication',
            'stipulation', 'affidavit', 'deposition', 'prima facie', 'de facto',
            'habeas corpus', 'pro bono', 'amicus curiae', 'mens rea', 'negligence',
            'liability', 'jurisdiction', 'venue', 'standing', 'tort', 'remedy'
        ]
        
        legal_term_count = sum(1 for term in legal_terms if re.search(rf'\b{term}\b', response, re.IGNORECASE))
        legal_terms_score = min(legal_term_count * 2, 20)
        score_factors['legal_terminology'] = legal_terms_score
        
        # Calculate final confidence score (0-100)
        total_score = sum(score_factors.values())
        final_score = min(max(total_score, 0), 100)  # Ensure it's between 0-100
        
        # Generate reasoning details for why this score was given
        reasoning_details = [
            f"Model-Task Alignment: {alignment_score}/20 points - {'Specialized model for this task' if alignment_score >= 15 else 'Model has limited specialization for this task'}",
            f"Citations: {citation_score}/25 points - {len(citations)} valid citations found",
            f"Structure: {structure_score}/15 points - {'Well-structured response' if structure_score >= 10 else 'Somewhat structured' if structure_score >= 5 else 'Limited structure'}",
            f"Information Density: {density_score}/20 points - {'Information-rich content' if density_score >= 15 else 'Moderate information density' if density_score >= 10 else 'Limited unique information'}",
            f"Legal Terminology: {legal_terms_score}/20 points - {legal_term_count} legal terms identified"
        ]
        
        return {
            'confidence_score': final_score,
            'factors': score_factors,
            'reasoning_details': '\n'.join(reasoning_details)
        }

    async def _call_ollama(self, model: str, prompt: str) -> Dict[str, Any]:
        """Call Ollama API for local model inference"""
        start_time = datetime.now()
        
        try:
            session = await self._ensure_session()
            base_url = self.config.get('ollama_api_url', 'http://localhost:11434')
            
            # Format the request payload
            payload = {
                "model": model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "top_p": 0.9,
                    "top_k": 40
                }
            }
            
            async with session.post(f"{base_url}/api/generate", json=payload) as response:
                if response.status != 200:
                    error_detail = await response.text()
                    raise Exception(f"Ollama API error ({response.status}): {error_detail}")
                
                response_json = await response.json()
                
                # Calculate elapsed time
                elapsed_time = (datetime.now() - start_time).total_seconds()
                
                # Track performance
                performance_monitor.record_model_performance(
                    model_name=model,
                    response_time=elapsed_time,
                    success=True
                )
                
                # Extract and process the response
                text_response = response_json.get('response', '')
                
                # Extract citations from the response
                citations = self.extract_citations(text_response)
                
                # Detect jurisdictions mentioned in the response
                jurisdictions = self.detect_jurisdictions(text_response)
                
                return {
                    'text': text_response,
                    'model': model,
                    'elapsed_time': elapsed_time,
                    'citations': citations,
                    'jurisdictions': jurisdictions,
                    'token_count': response_json.get('total_tokens', 0),
                    'provider': 'ollama'
                }
                
        except Exception as e:
            # Calculate elapsed time even for failures
            elapsed_time = (datetime.now() - start_time).total_seconds()
            
            # Track performance for failed requests
            performance_monitor.record_model_performance(
                model_name=model,
                response_time=elapsed_time,
                success=False
            )
            
            # Log the error
            print(f"Error calling Ollama API: {str(e)}")
            raise

    async def get_response(
        self,
        prompt: str,
        provider: Optional[AIProvider] = None,
        task_type: str = "chat"
    ) -> Dict[str, Any]:
        """Get response from AI model with error handling and fallbacks"""
        try:
            # If no provider specified, get the best one for the task
            if not provider:
                provider = self.get_best_provider(task_type)
            
            # Get model configuration
            config = AI_CONFIG.get(provider.value, {})
            if not config:
                raise ValueError(f"No configuration found for provider {provider}")
            
            # Apply prompt template if available
            template = self.get_prompt_template(config['name'], task_type)
            formatted_prompt = template.format(prompt=prompt) if template else prompt
            
            # Try primary provider
            try:
                response = await self._get_model_response(formatted_prompt, config, provider.value)
                
                # Validate response
                if not self._is_valid_response(response.get('response', ''), prompt):
                    raise ValueError("Invalid or incomplete response")
                    
                # Extract citations if needed
                if config['response_format'].get('includes_citations', False):
                    citations = self.extract_citations(response['response'])
                    response['citations'] = citations
                
                # Calculate confidence score
                confidence = self.calculate_confidence_score(
                    response['response'],
                    provider,
                    task_type,
                    response.get('citations', []),
                    response.get('tokens', 0)
                )
                response['confidence'] = confidence
                
                return response
                
            except Exception as primary_error:
                # Log primary error
                print(f"Primary provider {provider} failed: {str(primary_error)}")
                
                # Try fallback providers
                for fallback_provider in [p for p in AIProvider if p != provider]:
                    try:
                        fallback_config = AI_CONFIG.get(fallback_provider.value, {})
                        if not fallback_config:
                            continue
                            
                        print(f"Trying fallback provider: {fallback_provider}")
                        response = await self._get_model_response(
                            formatted_prompt,
                            fallback_config,
                            fallback_provider.value
                        )
                        
                        if self._is_valid_response(response.get('response', ''), prompt):
                            response['provider'] = fallback_provider.value
                            response['fallback'] = True
                            return response
                            
                    except Exception as fallback_error:
                        print(f"Fallback provider {fallback_provider} failed: {str(fallback_error)}")
                        continue
                
                # If all providers fail, raise the original error
                raise primary_error
                
        except Exception as e:
            # Handle all errors and return structured error response
            error_response = {
                'error': True,
                'message': str(e),
                'type': type(e).__name__,
                'provider': provider.value if provider else None,
                'timestamp': datetime.now().isoformat()
            }
            
            # Log error for monitoring
            print(f"AI Service Error: {json.dumps(error_response, indent=2)}")
            
            return error_response

    async def _get_model_response(self, prompt: str, config: Dict, provider: str) -> Dict[str, Any]:
        """Implementation for Hugging Face models"""
        session = await self._ensure_session()
        headers = {"Authorization": f"Bearer {self.huggingface_api_key}"}
        api_url = f"{self.huggingface_endpoint}/{config['huggingface_model']}"
        
        try:
            async with session.post(api_url, headers=headers, json={"inputs": prompt}, timeout=aiohttp.ClientTimeout(total=30)) as response:
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
        """Validate AI response"""
        if not response or len(response.strip()) < 10:
            return False
        
        # Check for common error indicators
        error_indicators = [
            "I apologize",
            "I cannot",
            "I am unable",
            "Error:",
            "Failed to"
        ]
        
        if any(indicator in response for indicator in error_indicators):
            return False
        
        # Check response relevance to prompt
        prompt_keywords = set(prompt.lower().split())
        response_keywords = set(response.lower().split())
        keyword_overlap = len(prompt_keywords.intersection(response_keywords))
        
        if keyword_overlap < 2 and len(prompt_keywords) > 3:
            return False
        
        return True

    async def _get_openai_response(self, prompt: str, config: Dict) -> Dict[str, Any]:
        """Implementation for OpenAI models"""
        from openai import AsyncOpenAI
        
        client = AsyncOpenAI(api_key=self.config['api_keys']['openai'])
        
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
            
            if response and response.choices and len(response.choices) > 0:
                return {
                    'text': response.choices[0].message.content,
                    'tokens': response.usage.total_tokens if response.usage else 0,
                    'model': config['model'],
                    'provider': 'openai'
                }
            else:
                return {
                    'text': "No response generated",
                    'tokens': 0,
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